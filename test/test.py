#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time
import unittest
import base58
import base64
import binascii


from ontology.utils import util
from ontology.common.define import *
from ontology.common.address import Address
from ontology.account.account import Account
from ontology.ont_sdk import OntologySdk
from ontology.crypto.signature_scheme import SignatureScheme
from ontology.smart_contract.native_contract.asset import Asset
from ontology.crypto.signature_scheme import SignatureScheme
from ontology.core.transaction import Transaction
from ontology.vm.build_vm import build_native_invoke_code, build_neo_vm_param
from ontology.smart_contract.neo_vm import NeoVm
from ontology.smart_contract.neo_contract.abi.build_params import BuildParams
from ontology.smart_contract.neo_contract.abi.abi_function import AbiFunction

#rpc_address = "http://polaris3.ont.io:20336"
rpc_address = "http://127.0.0.1:20336"
sdk = OntologySdk()
#sdk.rpc.set_address(rpc_address)
sdk.set_rpc((rpc_address))
private_key = "523c5fcf74823831756f0bcb3634234f10b3beb1c05595058534577752ad2d9f"
private_key2 = "75de8489fcb2dcaf2ef3cd607feffde18789de7da129b5e97c81e001793cb7cf"
private_key3 = "1383ed1fe570b6673351f1a30a66b21204918ef8f673e864769fa2a653401114"
acc = Account(private_key, SignatureScheme.SHA256withECDSA)
acc2 = Account(private_key2, SignatureScheme.SHA256withECDSA)
acc3 = Account(private_key3, SignatureScheme.SHA256withECDSA)


class TestAsset(unittest.TestCase):
    def test_a(self):
        tx_hash='2425f5b29766ece045fc3967ec18d56a2c9c23650541c6a3850b8037fb613b22'
        event=sdk.rpc.get_smart_contract_event_by_tx_hash(tx_hash)
        print(event)


    def test_transfer_Ont(self):
        wallet_path = "C:\\Go_WorkSpace\\src\\github.com\\ontio\\ontology\\_Wallet_\\wallet.dat"
        sdk.wallet_manager.open_wallet(wallet_path)
        acct1_addr = "AQf4Mzu1YJrhz9f3aRkkwSm9n3qhXGSh4p"
        acct1_pwd = "xinhao"
        acct1 = sdk.wallet_manager.get_account(acct1_addr, acct1_pwd)
        # export several keys
        wif_key = acct1.export_wif()
        print("wif_key is ", wif_key)
        private_key_bytes = acct1.get_privatekey_from_wif(wif_key)
        print("private_key_bytes is ", private_key_bytes, type(private_key_bytes))
        private_key_str = private_key_bytes.hex()
        print("private_key_str is ", private_key_str)

        contract_address_str = "0000000000000000000000000000000000000001"
        contract_address_bytearray = bytearray.fromhex(contract_address_str)
        contract_address = contract_address_bytearray
        # contract_address.reverse()
        print("my converted contract_address is ", contract_address)
        print("the givencontract_address is ", ONT_CONTRACT_ADDRESS)

        print('contract_address is ', contract_address)
        mybalance_1 = sdk.rpc.get_balance(acct1.get_address_base58())
        print("acc wif_key is ", acc.export_wif())

        from_acc = acct1
        to_acc = acc
        asset = "ong"
        balance_1 = sdk.rpc.get_balance(from_acc.get_address_base58())
        print("mybalance_1 is ", mybalance_1)
        print("balance_1 is ", balance_1)
        ass = Asset(sdk)
        from_addr = from_acc.get_address_base58()
        to_addr = to_acc.get_address_base58()
        print("Transfer from " + from_addr + " to " + to_addr)
        amount = int(int(balance_1[asset])/2)
        print("amount is ", amount, type(amount))
        payer = acct1.get_address_base58()
        gaslimit = 20000
        gasprice = 500

        # print('ong balance is ', sdk.rpc.get_balance(from_acc.get_address_base58()))
        # # int(ass.unbound_ong(from_addr))
        # ass.send_withdraw_ong_transaction(from_acc, to_addr, 100, to_acc,gaslimit, gasprice)
        #
        # print('ong balance is ', sdk.rpc.get_balance(from_acc.get_address_base58()))

        tx = ass.new_transfer_transaction(asset,from_addr, to_addr, amount, payer, gaslimit, gasprice)
        sdk.sign_transaction(tx, acct1)
        # sdk.sign_transaction(tx, to_acc)
        res = sdk.rpc.send_raw_transaction(tx)
        print("res in test_transfer_Ont is ", res)



    def test_open_wallet_account_from_path(self):
        ''' Open wallet and get account'''
        wallet_path = "C:\\Go_WorkSpace\\src\\github.com\\ontio\\ontology\\_Wallet_\\wallet.dat"
        sdk.wallet_manager.open_wallet(wallet_path)
        acct1_addr = "AQf4Mzu1YJrhz9f3aRkkwSm9n3qhXGSh4p"
        acct2_addr = "ASUwFccvYFrrWR6vsZhhNszLFNvCLA5qS6"
        acct3_addr = "AWf8NiLzXSDf1JB2Ae6YUKSHke4yLHMVCm"
        acct1_pwd = "xinhao"
        acct1 = sdk.wallet_manager.get_account(acct1_addr, acct1_pwd)
        acct2 = sdk.wallet_manager.get_account(acct2_addr, acct1_pwd)
        acct3 = sdk.wallet_manager.get_account(acct3_addr, acct1_pwd)
        '''export several keys'''
        account = acct3
        wif_key = account.export_wif()
        print("wif_key is ", wif_key)
        private_key_bytes = account.get_privatekey_from_wif(wif_key)
        print("private_key_bytes is ", private_key_bytes, type(private_key_bytes))
        private_key_str = private_key_bytes.hex()
        print("private_key_str is ", private_key_str, type(private_key_str))


        pwd = acct1_pwd
        addr = "ANjLDUU9htLKe41yxzVKpiPmFNseA3N9gc"
        salt = "XeK1Nkv8F8qKxXtLEPSbRw=="
        nounce = 16384
        scheme = SignatureScheme.SHA256withECDSA
        private_key_str = private_key_bytes.hex()
        print("private_key_str is ", private_key_str, type(private_key_str))
        ''' send transaction without signer'''
        version = 0
        tx_type = 0xd1
        unix_time_now = int(time.time())
        nonce = unix_time_now
        gas_price = 0
        gas_limit = 20000
        payer = None
        payload = None
        attributes = None
        sigs = None
        hash = None
        '''
        contract_address_str = "749a701ae89c0dbdab9b4b660ba84ee478004219"
        contract_address_bytearray = bytearray.fromhex(contract_address_str)
        contract_address = contract_address_bytearray
        contract_address.reverse()
        print('contract_address is ', contract_address)
        '''
        '''
        contract_address = util.get_asset_address("ont")
        #state = [{"address": "ASUwFccvYFrrWR6vsZhhNszLFNvCLA5qS6", "to": "AQf4Mzu1YJrhz9f3aRkkwSm9n3qhXGSh4p", "amount": 10000}]
        b58_address = "ASUwFccvYFrrWR6vsZhhNszLFNvCLA5qS6"
        raw_address = Address.b58decode(b58_address)
        #sdk.neo_vm().send_transaction(contract_address, acct1,[],20000, 0, )
        invoke_code = build_native_invoke_code(contract_address, bytes([0]), "balanceOf", raw_address)
        payer = raw_address
        tx = Transaction(0, 0xd1, unix_time_now, gas_price, gas_limit, payer, invoke_code, bytearray(), [], bytearray())
        #Transaction(0, 0xd1, unix_time_now, 0, 0, payer, invoke_code, bytearray(), [], bytearray())
        res = sdk.rpc.send_raw_transaction_pre_exec(tx)
        print('res is ', res)
        '''

        # Check balanceOf through NeoVm.make_invoke_transaction
        contract_address_str = "f328cb02bb1bd3a25c32f3db9b5f20b6fc4e04ea"
        contract_address_bytearray = bytearray.fromhex(contract_address_str)
        contract_address = contract_address_bytearray
        contract_address.reverse()
        print('contract_address is ', contract_address)
        params_list = []
        params_list.append(str("BalanceOf").encode())
        param = []
        b58_address = "AQf4Mzu1YJrhz9f3aRkkwSm9n3qhXGSh4p"
        param.append(Address.b58decode(b58_address).to_array())
        params_list.append(param)
        params = BuildParams.create_code_params_script(params_list)
        # when pre-execute, don't use 0x67
        tx = NeoVm.make_invoke_transaction(bytearray(contract_address), bytearray(params), b'', 20000, 0)
        res = sdk.rpc.send_raw_transaction_pre_exec(tx)
        print("BalanceOf is ", res)

        # # Check totalsupply
        # params_list = []
        # params_list.append(str("totalSupply").encode())
        # param = [10]
        # params_list.append(param)
        # params = BuildParams.create_code_params_script(params_list)
        # # when pre-execute, don't use 0x67
        # tx = NeoVm.make_invoke_transaction(bytearray(contract_address), bytearray(params), b'', 20000, 0)
        # res = sdk.rpc.send_raw_transaction_pre_exec(tx)
        # print('totalsupply is ', res)
        #
        # # Transfer through Transaction, send_raw_transaction
        # params_list = []
        # params_list.append(str("transfer").encode())
        # from_addr = "ASUwFccvYFrrWR6vsZhhNszLFNvCLA5qS6"
        # to_addr = "AQf4Mzu1YJrhz9f3aRkkwSm9n3qhXGSh4p"
        # value = 100
        # param = []
        # param.append(Address.b58decode(from_addr).to_array())
        # param.append(Address.b58decode(to_addr).to_array())
        # param.append(value)
        # params_list.append(param)
        # params = BuildParams.create_code_params_script(params_list)
        # # when execute, use 0x67, then add the contract_address
        # params.append(0x67)
        # for i in contract_address:
        #     params.append(i)
        # payer_raw_address = acct2.get_address().to_array()
        # payer_acct = acc2
        # unix_time_now = int(time.time())
        # tx = Transaction(0, 0xd1, unix_time_now, gas_price, gas_limit, payer_raw_address, params, bytearray(), [], bytearray())
        # sdk.sign_transaction(tx, acct2)
        # #sdk.add_sign_transaction(tx, payer_acct)
        # sdk.rpc.send_raw_transaction(tx)
        # # # Transfer through send_Transaction
        # # balance_Of_Addr = "ASUwFccvYFrrWR6vsZhhNszLFNvCLA5qS6"
        # # func = AbiFunction("balanceOf", "Integer", [])
        # # func.set_params_value((binascii.a2b_hex(balance_Of_Addr)))
        # # balance = sdk.neo_vm().send_transaction(contract_address, None, None, 0, 0, func, True)
        # # Transfer through Transaction, send_raw_transaction

        ### check balance before transferMulti###
        print('### check balance Before transferMulti ###')
        params_list = []
        params_list.append(str("BalanceOf").encode())
        param = []
        b58_address = "AQf4Mzu1YJrhz9f3aRkkwSm9n3qhXGSh4p"
        param.append(Address.b58decode(b58_address).to_array())
        params_list.append(param)
        params = BuildParams.create_code_params_script(params_list)
        # when pre-execute, don't use 0x67
        tx = NeoVm.make_invoke_transaction(bytearray(contract_address), bytearray(params), b'', 20000, 0)
        res = sdk.rpc.send_raw_transaction_pre_exec(tx)
        print("before TransferMulti, the balance is ", res)

        ### transferMulti
        params_list = []
        params_list.append(str("TransferMulti").encode())
        from_addr1 = "AQf4Mzu1YJrhz9f3aRkkwSm9n3qhXGSh4p"
        from_addr2 = "AQf4Mzu1YJrhz9f3aRkkwSm9n3qhXGSh4p"
        to_addr1 = "ASUwFccvYFrrWR6vsZhhNszLFNvCLA5qS6"
        to_addr2 = "AWf8NiLzXSDf1JB2Ae6YUKSHke4yLHMVCm"
        value1 = 10000
        value2 = 10000
        param1 = []
        param1.append(Address.b58decode(from_addr1).to_array())
        param1.append(Address.b58decode(to_addr1).to_array())
        param1.append(value1)
        param2 = []
        param2.append(Address.b58decode(from_addr2).to_array())
        param2.append(Address.b58decode(to_addr2).to_array())
        param2.append(value2)
        params_list_tmp = []
        params_list_tmp.append(param1)
        params_list_tmp.append(param2)
        params_list.append(params_list_tmp)
        # params_list.append(param1)
        # params_list.append(param2)
        print(" params_list is ", params_list)
        print(" contract_address is ", contract_address)
        params = BuildParams.create_code_params_script(params_list)
        # when execute, use 0x67, then add the contract_address
        params.append(0x67)
        for i in contract_address:
            params.append(i)
        payer_raw_address = acct1.get_address().to_array()
        unix_time_now = int(time.time())
        tx = Transaction(0, 0xd1, unix_time_now, gas_price, gas_limit, payer_raw_address, params, bytearray(), [],
                         bytearray())
        tx = sdk.sign_transaction(tx, acct1)
        # sdk.add_sign_transaction(tx, payer_acct)
        tx_hash = sdk.rpc.send_raw_transaction(tx)
        print('tx_hash is ', tx_hash)
        time.sleep(12)
        event=sdk.rpc.get_smart_contract_event_by_tx_hash(tx_hash)
        # event = sdk.rpc.get_block_by_hash(tx_hash)
        print("event is ", event)
        # print("tx_hash is ", tx_hash)
        # event = sdk.rpc.get_smart_contract_event_by_tx_hash(tx_hash)
        # print("event is ", event)


        #check balance After transferMulti
        print('### check balance After transferMulti ###')
        params_list = []
        params_list.append(str("BalanceOf").encode())
        param = []
        b58_address = "AQf4Mzu1YJrhz9f3aRkkwSm9n3qhXGSh4p"
        param.append(Address.b58decode(b58_address).to_array())
        params_list.append(param)
        params = BuildParams.create_code_params_script(params_list)
        # when pre-execute, don't use 0x67
        tx = NeoVm.make_invoke_transaction(bytearray(contract_address), bytearray(params), b'', 20000, 0)

        res = sdk.rpc.send_raw_transaction_pre_exec(tx)
        print("After TransferMulti, the balance is ", res)






if __name__ == '__main__':
    unittest.main()