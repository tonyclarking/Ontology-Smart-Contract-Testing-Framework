"""
Wontology Game
Supports different size of ticket pool like 2,5,10 and 20
Every ticket needs 1 ONG
When attendee count reach max of this game round,
game will generate a random number and send all the ONGs to the selected attendee.
This round Game end
"""
from boa.interop.System.Storage import *
from boa.interop.System.ExecutionEngine import *
from boa.interop.System.Runtime import *
from boa.interop.System.Blockchain import GetHeight, GetHeader, GetBlock
from boa.interop.System.Header import GetHash
from boa.interop.Ontology.Native import *
from boa.builtins import state, sha256, concat

# ONG contract address
contractAddress = bytearray(b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x02')
ctx = GetContext()
# the current contract address
selfAddr = GetExecutingScriptHash()

# storage profix
statusKey = "Status"
roundKey = "Round"
attendCntKey = "AttendCnt"
attendeeKey = "Attendee"
indexKey = "Index"
winnerKey = "Winner"
paidKey = "Paid"
starttimeKey = "Starttime"
status_running = "RUNNING"
status_end = "END"
# ONG decimal is 9, ongPerTick is 1 ONG
ongPerTicket = 1000000000
txFee = 16200000
createFee = 3300000

# count =2, 5, 10, 20, After count*timeOutPerAttentee, the game can be ended manually
timeOutPerAttentee = 180

def Main(operation, args):
    if operation == 'attend':
        account = args[0]
        ticketsCount = args[1]
        if ticketsCount != 2 and ticketsCount != 5 and ticketsCount != 10 and ticketsCount != 20:
            return False
        return attend(account, ticketsCount)
    if operation == 'queryWinner':
        count = args[0]
        round = args[1]
        return queryWinner(count, round)
    if operation == 'queryAttendeeCount':
        count = args[0]
        round = args[1]
        return queryAttendeeCount(count, round)
    if operation == 'queryCurrentRound':
        count = args[0]
        return queryCurrentRound(count)
    if operation == 'endGame':
        # When the game last longer than getTimeOut() =  count * timeOutPerAttentee anyone can run this method to end the game
        account = args[0]
        count = args[1]
        currentRound = Get(ctx, concatKey(roundKey, count))
        if not currentRound:
            return False
        status = Get(ctx, concatKey(statusKey, concatKey(count, currentRound)))
        if status == status_end:
            return False
        starttime = Get(ctx, concatKey(starttimeKey, concatKey(count, currentRound)))
        if getTimestamp() - starttime > getTimeOut(count):
            endGame(account, count)
            return True
        Notify('not timeout yet')
        return False
    return False


def attend(acct, count):
    """
    When the player plays Wontology, by default, the method should be invoked.
    :param acct: the address of player account
    :param count: this is the designated type of ticket pool
    :return: True means player participate successfully, false means failure that the palyer attends Wontology
    """
    if CheckWitness(acct):
        key = concatKey(roundKey, count)
        currentRound = Get(ctx, key)
        # initiate a game
        if not currentRound:
            if transONG(acct, selfAddr, ongPerTicket):
                startNewRound(1, count, acct)
                Notify(["For the first time, initiate Wontology Game Round_", count])
                return True
            else:
                Notify("transfer ong failed!")
                return False
        else:
            newKey = concatKey(count, currentRound)
            status = Get(ctx, concatKey(statusKey, newKey))
            # the game is still running
            if status == status_running:
                attendedCount = Get(ctx, concatKey(attendCntKey, newKey))
                newCount = attendedCount + 1
                if transONG(acct, selfAddr, ongPerTicket):
                    # add attend count
                    Put(ctx, concatKey(attendCntKey, newKey), newCount)
                    # get attendee tickets
                    tickets = Get(ctx, concatKey(concatKey(attendeeKey, newKey), acct))
                    if not tickets:
                        # record attendee
                        Put(ctx, concatKey(concatKey(attendeeKey, newKey), acct), 1)
                    else:
                        Put(ctx, concatKey(concatKey(attendeeKey, newKey), acct), tickets + 1)

                    # record attendee index
                    Put(ctx, concatKey(concatKey(indexKey, newKey), newCount), acct)
                else:
                    Notify("transfer ong failed!")
                    return False

                if newCount == count:
                    return endGame(acct, count)
                else:
                    return True
            else:
                # this round is end,should start next round
                if transONG(acct, selfAddr, ongPerTicket):
                    startNewRound(currentRound + 1, count, acct)
                    return True
                else:
                    Notify("transfer ong failed!")
                    return False
    else:
        Notify("CheckWiteness failed!")
        return False


def queryWinner(count, round):
    """
    Get the winner address of [round] round of the game with size of count ticket pool
    :param count: the size of ticket pool
    :param round: the round number
    :return: winner address
    """
    return Get(ctx, concatKey(concatKey(winnerKey, count), round))


def queryAttendeeCount(count, round):
    """
    Get the current player number or sold tickets in [round] round of the game with size of count ticket pool
    :param count: the size of ticket pool
    :param round: the round number
    :return: current player number or sold tickets number
    """
    return Get(ctx, concatKey(concatKey(attendCntKey, count), round))


def queryCurrentRound(count):
    """
    Get the current round number of the game with size of count ticket pool
    :param count: the size of ticket pool
    :return: the current round number
    """
    return Get(ctx, concatKey(roundKey, count))


def endGame(account, count):
    """
    End the Wontology game with ticket pool of count
    Generate random integer, pick the winner randomly
    Transfer all the asset in the pool to the winner
    Make up for the extra fee spent by the last attendee and the first attendee
    :param account: the player who invoke the endGame method
    :param count: this is the designated type of ticket pool
    :return:
    """
    key = concatKey(roundKey, count)
    currentRound = Get(ctx, key)
    newkey = concatKey(count, currentRound)
    paid = Get(ctx, concatKey(paidKey, newkey))

    if not paid:
        attendcount = Get(ctx, concatKey(attendCntKey, newkey))
        # currentTime = getTimestamp()
        idx = abs(getRandom()) % attendcount + 1
        Log(idx)
        attendee = Get(ctx, concatKey(concatKey(indexKey, newkey), idx))

        # winner will pay for the tx fee
        if transONGFromContract(attendee, attendcount * ongPerTicket - txFee - createFee):
            # record the winner of this round
            Put(ctx, concatKey(winnerKey, newkey), attendee)
            # mark this round game end
            Put(ctx, concatKey(statusKey, newkey), status_end)
            # mark ong paid
            Put(ctx, concatKey(paidKey, newkey), 'YES')
        else:
            Notify('transfer ONG failed!')
            return False

        # refund txFee to last attendee
        if transONGFromContract(account, txFee):
            # refund createFee to first attendee
            firstAttendee = Get(ctx, concatKey(concatKey(indexKey, newkey), 1))
            if transONGFromContract(firstAttendee, createFee):
                return True
            Notify('transfer create ONG failed!')
            return False
        else:
            Notify('transfer tx ONG failed!')
            return False

    else:
        return True


def transONG(fromacct, toacct, amount):
    """
     transfer ONG
     :param fromacct:
     :param toacct:
     :param amount:
     :return:
     """
    if CheckWitness(fromacct):

        param = makeState(fromacct, toacct, amount)
        res = Invoke(0, contractAddress, 'transfer', [param])
        Notify(res)

        if res and res == b'\x01':
            Notify('transfer succeed')
            return True
        else:
            Notify('transfer failed')

            return False

    else:
        Notify('checkWitness failed')
        return False


def startNewRound(roundNum, count, acct):
    """
    start a new game round
    :param roundNum:
    :param count:
    :param acct:
    :return:
    """

    key = concatKey(count, roundNum)

    # record current round
    Put(ctx, concatKey(roundKey, count), roundNum)
    # add attend count
    Put(ctx, concatKey(attendCntKey, key), 1)
    # record attendee ticket
    Put(ctx, concatKey(concatKey(attendeeKey, key), acct), 1)
    # record attendee index
    Put(ctx, concatKey(concatKey(indexKey, key), 1), acct)
    # record status
    Put(ctx, concatKey(statusKey, key), status_running)
    # record starttime
    Put(ctx, concatKey(starttimeKey, key), getTimestamp())


def transONGFromContract(toacct, amount):
    """
     transfer ONG from contract
     :param toacct:
     :param amount:
     :return:
     """

    param = makeState(selfAddr, toacct, amount)
    res = Invoke(1, contractAddress, 'transfer', [param])
    Notify(res)

    if res and res == b'\x01':
        Notify('transfer succeed')
        return True
    else:
        Notify('transfer failed')

        return False


def concatKey(str1,str2):
    """
    connect str1 and str2 togeter as a key
    :param str1: string1
    :param str2:  string2
    :return: string1_string2
    """
    return concat(concat(str1, '_'), str2)


def makeState(fromacct, toacct, amount):
    """
    make a tranfer state parameter
    currently due to the compiler problem,
    must be created as this format
    :param fromacct:
    :param toacct:
    :param amount:
    :return:
    """
    return state(fromacct, toacct, amount)


def getTimestamp():
    """
    get the header timestamp
    :return:
    """
    timestamp = GetTime()
    return timestamp


def getRandom():
    """
    get random integer
    :return:
    """
    time = GetTime()
    height = GetHeight()
    header = GetHeader(height)
    return sha256(abs(GetHash(header)) % time)

def getTimeOut(count):
    """
    Calculate timeout value in secounds,
    :param count: size of ticket pool
    :return: timeout based on different games with different size of ticket pool
    """
    return timeOutPerAttentee * count