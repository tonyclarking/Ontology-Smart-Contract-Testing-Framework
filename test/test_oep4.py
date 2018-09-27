#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import binascii
import json
import time
import unittest

from ontology.common.address import Address
from ontology.ont_sdk import OntologySdk
from ontology.account.account import Account
from ontology.exception.exception import SDKException
from ontology.crypto.signature_scheme import SignatureScheme

remote_rpc_address = "http://polaris3.ont.io:20336"
local_rpc_address = 'http://localhost:20336'

contract_address = 'f328cb02bb1bd3a25c32f3db9b5f20b6fc4e04ea'

class TestOep4(unittest.TestCase):
    def test_get_abi(self):
        oep4_abi = '{"functions":[{"name":"Main","parameters":[{"name":"operation","type":""},{"name":"args","type":""}],"returntype":""},{"name":"Name","parameters":[{"name":"","type":""}],"returntype":""},{"name":"TotalSupply","parameters":[{"name":"","type":""}],"returntype":""},{"name":"Init","parameters":[{"name":"","type":""}],"returntype":""},{"name":"Symbol","parameters":[{"name":"","type":""}],"returntype":""},{"name":"Transfer","parameters":[{"name":"from_acct","type":""},{"name":"to_acct","type":""},{"name":"amount","type":""}],"returntype":""},{"name":"TransferMulti","parameters":[{"name":"args","type":""}],"returntype":""},{"name":"Approve","parameters":[{"name":"owner","type":""},{"name":"spender","type":""},{"name":"amount","type":""}],"returntype":""},{"name":"TransferFrom","parameters":[{"name":"spender","type":""},{"name":"from_acct","type":""},{"name":"to_acct","type":""},{"name":"amount","type":""}],"returntype":""},{"name":"BalanceOf","parameters":[{"name":"account","type":""}],"returntype":""},{"name":"Decimal","parameters":[{"name":"","type":""}],"returntype":""},{"name":"Allowance","parameters":[{"name":"owner","type":""},{"name":"spender","type":""}],"returntype":""}]}'
        sdk = OntologySdk()
        print("sdk.neo_vm().oep4().get_abi() is ", sdk.neo_vm().oep4().get_abi())
        self.assertEqual(json.loads(oep4_abi), sdk.neo_vm().oep4().get_abi())

    def test_set_contract_address(self):
        sdk = OntologySdk()
        sdk.set_rpc(local_rpc_address)
        oep4 = sdk.neo_vm().oep4()
        oep4.set_contract_address(contract_address)
        # print("ope4 contract address is ", oep4.get_contract_address(is_hex=True), type(oep4.get_contract_address(is_hex=True)))
        # print("Contract address is ", contract_address, type(contract_address))
        self.assertEqual(contract_address, oep4.get_contract_address(is_hex=True))

    def test_get_name(self):
        sdk = OntologySdk()
        sdk.set_rpc(local_rpc_address)
        oep4 = sdk.neo_vm().oep4()
        oep4.set_contract_address(contract_address)
        print("oep4.get_name() is ", oep4.get_name())
        self.assertEqual('TokenName', oep4.get_name())

    def test_get_symbol(self):
        sdk = OntologySdk()
        sdk.set_rpc(local_rpc_address)
        oep4 = sdk.neo_vm().oep4()
        oep4.set_contract_address(contract_address)
        self.assertEqual('Symbol', oep4.get_symbol())

    def test_get_decimal(self):
        sdk = OntologySdk()
        sdk.set_rpc(local_rpc_address)
        oep4 = sdk.neo_vm().oep4()
        oep4.set_contract_address(contract_address)
        self.assertEqual(8, oep4.get_decimal())

    def test_init(self):
        sdk = OntologySdk()
        sdk.set_rpc(local_rpc_address)
        oep4 = sdk.neo_vm().oep4()
        oep4.set_contract_address(contract_address)
        private_key = '5f2fe68215476abb9852cfa7da31ef00aa1468782d5ca809da5c4e1390b8ee45'
        acct = Account(private_key, SignatureScheme.SHA256withECDSA)
        gas_limit = 20000000
        gas_price = 500
        tx_hash = oep4.init(acct, acct, gas_limit, gas_price)
        self.assertEqual(len(tx_hash), 64)

    def test_get_total_supply(self):
        sdk = OntologySdk()
        sdk.set_rpc(local_rpc_address)
        oep4 = sdk.neo_vm().oep4()
        oep4.set_contract_address(contract_address)
        print("oep4.get_total_supply() is ", oep4.get_total_supply())
        self.assertEqual(100000000000000000, oep4.get_total_supply())

    def test_transfer(self):
        sdk = OntologySdk()
        sdk.set_rpc(local_rpc_address)
        oep4 = sdk.neo_vm().oep4()
        oep4.set_contract_address(contract_address)
        private_key1 = '5f2fe68215476abb9852cfa7da31ef00aa1468782d5ca809da5c4e1390b8ee45'
        private_key2 = "f00dd7f5356e8aee93a049bdccc44ce91169e07ea3bec9f4e0142e456fd39bae"
        from_acct = Account(private_key1, SignatureScheme.SHA256withECDSA)
        to_acct = Account(private_key2, SignatureScheme.SHA256withECDSA)
        gas_limit = 20000000
        gas_price = 500
        b58_to_address = to_acct.get_address_base58()
        value = 10
        result = oep4.transfer(from_acct, b58_to_address, value, from_acct, gas_limit, gas_price)
        self.assertEqual(len(result), 64)

    def test_balance_of(self):
        sdk = OntologySdk()
        sdk.set_rpc(local_rpc_address)
        oep4 = sdk.neo_vm().oep4()
        oep4.set_contract_address(contract_address)
        private_key1 = "5f2fe68215476abb9852cfa7da31ef00aa1468782d5ca809da5c4e1390b8ee45"
        private_key2 = "f00dd7f5356e8aee93a049bdccc44ce91169e07ea3bec9f4e0142e456fd39bae"
        acct1 = Account(private_key1, SignatureScheme.SHA256withECDSA)
        acct2 = Account(private_key2, SignatureScheme.SHA256withECDSA)
        b58_address1 = acct1.get_address_base58()
        b58_address2 = acct2.get_address_base58()
        balance = oep4.balance_of(b58_address1)
        print("balance1 is ", balance)
        self.assertGreaterEqual(balance, 10)
        balance = oep4.balance_of(b58_address2)
        print("balance2 is ", balance)
        self.assertGreaterEqual(balance, 10)

    def test_transfer_multi(self):
        sdk = OntologySdk()
        sdk.set_rpc(local_rpc_address)
        oep4 = sdk.neo_vm().oep4()
        oep4.set_contract_address(contract_address)
        private_key1 = "5f2fe68215476abb9852cfa7da31ef00aa1468782d5ca809da5c4e1390b8ee45"
        private_key2 = "f00dd7f5356e8aee93a049bdccc44ce91169e07ea3bec9f4e0142e456fd39bae"
        private_key3 = "da213fb4cb1b12269c20307dadda35a7c89869c0c791b777fd8618d4159db99c"
        acct1 = Account(private_key1, SignatureScheme.SHA256withECDSA)
        acct2 = Account(private_key2, SignatureScheme.SHA256withECDSA)
        acct3 = Account(private_key3, SignatureScheme.SHA256withECDSA)


        b58_from_address1 = acct1.get_address_base58()
        hex_from_address1 = acct1.get_address_hex()
        from_address_list = [hex_from_address1, hex_from_address1]

        b58_to_address2 = acct2.get_address_base58()
        b58_to_address3 = acct3.get_address_base58()

        hex_to_address2 = acct2.get_address_hex()
        hex_to_address3 = acct3.get_address_hex()
        to_address_list = [hex_to_address2, hex_to_address3]

        value_list = [1, 2]
        # print("b58 addr 1 is ", b58_from_address1)
        # print("b58 addr 1 is ", b58_to_address2)
        # print("b58 addr 1 is ", b58_to_address3)

        transfer1 = [b58_from_address1, b58_to_address2, value_list[0]]
        transfer2 = [b58_from_address1, b58_to_address3, value_list[1]]
        signers = [acct1]
        args = []
        args.append(transfer1)
        args.append(transfer2)

        gas_limit = 20000000
        gas_price = 500

        tx_hash = oep4.transfer_multi(args, signers[0], signers, gas_limit, gas_price)
        self.assertEqual(64, len(tx_hash))
        sdk = OntologySdk()
        sdk.set_rpc(local_rpc_address)
        time.sleep(10)
        try:
            event = sdk.rpc.get_smart_contract_event_by_tx_hash(tx_hash)
            # print("event is ", event)
            notify = event['Notify'][0:-1]
            # print("notify is ", notify)
            self.assertEqual(len(args), len(notify))
            for index in range(len(notify)):
                self.assertEqual(from_address_list[index], notify[index]['States'][1])
                self.assertEqual(to_address_list[index], notify[index]['States'][2])
                self.assertEqual(value_list[index], int(notify[index]['States'][3]))
        except SDKException as e:
            raised = False
            self.assertTrue(raised, e)

    def test_approve(self):
        sdk = OntologySdk()
        sdk.set_rpc(local_rpc_address)
        oep4 = sdk.neo_vm().oep4()
        oep4.set_contract_address(contract_address)
        private_key1 = "5f2fe68215476abb9852cfa7da31ef00aa1468782d5ca809da5c4e1390b8ee45"
        private_key2 = "f00dd7f5356e8aee93a049bdccc44ce91169e07ea3bec9f4e0142e456fd39bae"
        owner_acct = Account(private_key1, SignatureScheme.SHA256withECDSA)
        hex_owner_address = owner_acct.get_address_hex()
        spender = Account(private_key2, SignatureScheme.SHA256withECDSA)
        b58_spender_address = spender.get_address_base58()
        hex_spender_address = spender.get_address_hex()
        amount = 100
        gas_limit = 20000000
        gas_price = 0
        tx_hash = oep4.approve(owner_acct, b58_spender_address, amount, owner_acct, gas_limit, gas_price)
        self.assertEqual(len(tx_hash), 64)
        sdk = OntologySdk()
        sdk.set_rpc(local_rpc_address)
        time.sleep(6)
        try:
            event = sdk.rpc.get_smart_contract_event_by_tx_hash(tx_hash)
            notify = event['Notify'][0]
            self.assertEqual(hex_owner_address, notify['States'][1])
            self.assertEqual(hex_spender_address, notify['States'][2])
            self.assertEqual('64', notify['States'][3])
        except SDKException as e:
            raised = False
            self.assertTrue(raised, e)

    def test_allowance(self):
        sdk = OntologySdk()
        sdk.set_rpc(local_rpc_address)
        oep4 = sdk.neo_vm().oep4()
        oep4.set_contract_address(contract_address)
        private_key1 = "5f2fe68215476abb9852cfa7da31ef00aa1468782d5ca809da5c4e1390b8ee45"
        private_key2 = "f00dd7f5356e8aee93a049bdccc44ce91169e07ea3bec9f4e0142e456fd39bae"
        acct1 = Account(private_key1, SignatureScheme.SHA256withECDSA)
        acct2 = Account(private_key2, SignatureScheme.SHA256withECDSA)
        b58_owner_address = acct1.get_address_base58()
        b58_spender_address = acct2.get_address_base58()
        allowance = oep4.allowance(b58_owner_address, b58_spender_address)
        self.assertGreaterEqual(allowance, 1)

    def test_transfer_from(self):
        sdk = OntologySdk()
        sdk.set_rpc(local_rpc_address)
        oep4 = sdk.neo_vm().oep4()
        oep4.set_contract_address(contract_address)
        private_key1 = "5f2fe68215476abb9852cfa7da31ef00aa1468782d5ca809da5c4e1390b8ee45"
        private_key2 = "f00dd7f5356e8aee93a049bdccc44ce91169e07ea3bec9f4e0142e456fd39bae"
        private_key3 = "da213fb4cb1b12269c20307dadda35a7c89869c0c791b777fd8618d4159db99c"
        spender_acct = Account(private_key2, SignatureScheme.SHA256withECDSA)

        from_acct = Account(private_key1, SignatureScheme.SHA256withECDSA)
        hex_from_address = from_acct.get_address_hex()

        to_acct = Account(private_key3, SignatureScheme.SHA256withECDSA)
        hex_to_address = to_acct.get_address_hex()
        b58_to_address = to_acct.get_address_base58()

        gas_limit = 20000000
        gas_price = 0
        value = 1
        tx_hash = oep4.transfer_from(spender_acct, from_acct, b58_to_address, value, from_acct, gas_limit,
                                     gas_price)
        self.assertEqual(64, len(tx_hash))
        sdk = OntologySdk()
        sdk.set_rpc(local_rpc_address)
        time.sleep(6)
        try:
            event = sdk.rpc.get_smart_contract_event_by_tx_hash(tx_hash)
            notify = event['Notify'][0]
            self.assertEqual(2, len(notify))
            self.assertEqual(hex_from_address, notify['States'][1])
            self.assertEqual(hex_to_address, notify['States'][2])
            self.assertEqual('01', notify['States'][3])
        except SDKException as e:
            raised = False
            self.assertTrue(raised, e)


if __name__ == '__main__':
    unittest.main()
