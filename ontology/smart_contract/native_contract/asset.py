#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from time import time

from ontology.utils import util
from ontology.common.define import *
from ontology.common.address import Address
from ontology.account.account import Account
from ontology.common.error_code import ErrorCode
from ontology.core.transaction import Transaction
from ontology.exception.exception import SDKException
from ontology.vm.build_vm import build_native_invoke_code


class Asset(object):
    def __init__(self, sdk):
        self.__sdk = sdk

    @staticmethod
    def get_asset_address(asset: str) -> bytearray:
        if asset.upper() == 'ONT':
            contract_address = ONT_CONTRACT_ADDRESS
        elif asset.upper() == 'ONG':
            contract_address = ONG_CONTRACT_ADDRESS
        else:
            raise ValueError("asset is not equal to ONT or ONG")
        return contract_address  # [20]byte

    @staticmethod
    def new_transfer_transaction(asset: str, from_addr: str, to_addr: str, amount: int, payer: str,
                                 gas_limit: int, gas_price: int):
        contract_address = util.get_asset_address(asset)  # []bytes
        raw_from = Address.b58decode(from_addr)
        raw_to = Address.b58decode(to_addr)
        raw_payer = Address.b58decode(payer)
        state = [{"from": raw_from, "to": raw_to, "amount": amount}]
        invoke_code = build_native_invoke_code(contract_address, bytes([0]), "transfer", state)
        unix_time_now = int(time())
        return Transaction(0, 0xd1, unix_time_now, gas_price, gas_limit, raw_payer, invoke_code, bytearray(), [],
                           bytearray())

    def query_balance(self, asset: str, b58_address: str) -> int:
        raw_address = Address.b58decode(b58_address)
        contract_address = util.get_asset_address(asset)
        invoke_code = build_native_invoke_code(contract_address, bytes([0]), "balanceOf", raw_address)
        unix_time_now = int(time())
        payer = Address(ZERO_ADDRESS).to_array()
        tx = Transaction(0, 0xd1, unix_time_now, 0, 0, payer, invoke_code, bytearray(), [], bytearray())
        res = self.__sdk.rpc.send_raw_transaction_pre_exec(tx)
        return int(res, 16)

    def query_allowance(self, asset: str, b58_from_address: str, b58_to_address: str) -> str:
        contract_address = util.get_asset_address(asset)
        raw_from = Address.b58decode(b58_from_address)
        raw_to = Address.b58decode(b58_to_address)
        args = {"from": raw_from, "to": raw_to}
        invoke_code = build_native_invoke_code(contract_address, bytes([0]), "allowance", args)
        unix_time_now = int(time())
        payer = Address(ZERO_ADDRESS).to_array()
        tx = Transaction(0, 0xd1, unix_time_now, 0, 0, payer, invoke_code, bytearray(), [], bytearray())
        res = self.__sdk.rpc.send_raw_transaction_pre_exec(tx)
        return res

    def unbound_ong(self, addr: str) -> str:
        return self.__sdk.rpc.get_allowance(addr)

    def query_name(self, asset: str) -> str:
        contract_address = util.get_asset_address(asset)
        invoke_code = build_native_invoke_code(contract_address, bytes([0]), "name", bytearray())
        unix_time_now = int(time())
        payer = Address(ZERO_ADDRESS).to_array()
        tx = Transaction(0, 0xd1, unix_time_now, 0, 0, payer, invoke_code, bytearray(), [], bytearray())
        res = self.__sdk.rpc.send_raw_transaction_pre_exec(tx)
        return bytes.fromhex(res).decode()

    def query_symbol(self, asset: str) -> str:
        contract_address = util.get_asset_address(asset)
        invoke_code = build_native_invoke_code(contract_address, bytes([0]), "symbol", bytearray())
        unix_time_now = int(time())
        payer = Address(ZERO_ADDRESS).to_array()
        tx = Transaction(0, 0xd1, unix_time_now, 0, 0, payer, invoke_code, bytearray(), [], bytearray())
        res = self.__sdk.rpc.send_raw_transaction_pre_exec(tx)
        return bytes.fromhex(res).decode()

    def query_decimals(self, asset: str) -> str:
        contract_address = util.get_asset_address(asset)
        invoke_code = build_native_invoke_code(contract_address, bytes([0]), "decimals", bytearray())
        unix_time_now = int(time())
        payer = Address(ZERO_ADDRESS).to_array()
        tx = Transaction(0, 0xd1, unix_time_now, 0, 0, payer, invoke_code, bytearray(), [], bytearray())
        decimal = self.__sdk.rpc.send_raw_transaction_pre_exec(tx)
        return decimal

    @staticmethod
    def new_withdraw_ong_transaction(claimer_addr: str, recv_addr: str, amount: int, payer_addr: str,
                                     gas_limit: int, gas_price: int) -> Transaction:
        ont_contract_address = util.get_asset_address("ont")
        ong_contract_address = util.get_asset_address("ong")
        args = {"sender": Address.b58decode(claimer_addr), "from": ont_contract_address,
                "to": Address.b58decode(recv_addr),
                "value": amount}
        invoke_code = build_native_invoke_code(ong_contract_address, bytes([0]), "transferFrom", args)
        unix_time_now = int(time())
        return Transaction(0, 0xd1, unix_time_now, gas_price, gas_limit, Address.b58decode(payer_addr), invoke_code,
                           bytearray(), [], bytearray())

    def send_withdraw_ong_transaction(self, claimer: Account, recv_addr: str, amount: int, payer: Account,
                                      gas_limit: int, gas_price: int) -> str:
        b58_claimer = claimer.get_address_base58()
        b58_payer = payer.get_address_base58()
        tx = Asset.new_withdraw_ong_transaction(b58_claimer, recv_addr, amount, b58_payer, gas_limit, gas_price)
        tx = self.__sdk.sign_transaction(tx, payer)
        tx = self.__sdk.add_sign_transaction(tx, claimer)
        res = self.__sdk.rpc.send_raw_transaction_pre_exec(tx)
        return res

    @staticmethod
    def new_approve(asset: str, send_addr: str, recv_addr: str, amount: int, payer: str, gas_limit: int,
                    gas_price: int) -> Transaction:
        contract_address = util.get_asset_address(asset)  # []bytes
        raw_send = Address.b58decode(send_addr)
        raw_recv = Address.b58decode(recv_addr)
        raw_payer = Address.b58decode(payer)
        args = {"from": raw_send, "to": raw_recv, "amount": amount}
        invoke_code = build_native_invoke_code(contract_address, bytes([0]), "approve", args)
        unix_time_now = int(time())
        return Transaction(0, 0xd1, unix_time_now, gas_price, gas_limit, raw_payer, invoke_code, bytearray(), [],
                           bytearray())

    def send_approve(self, asset, sender: Account, recv_addr: str, amount: int, payer: Account, gas_limit: int,
                     gas_price: int) -> str:
        b58_sender = sender.get_address_base58()
        b58_payer = payer.get_address_base58()
        tx = Asset.new_approve(asset, b58_sender, recv_addr, amount, b58_payer, gas_limit, gas_price)
        tx = self.__sdk.sign_transaction(tx, sender)
        if sender.get_address_base58() != payer.get_address_base58():
            tx = self.__sdk.add_sign_transaction(tx, payer)
        flag = self.__sdk.rpc.send_raw_transaction(tx)
        return flag

    @staticmethod
    def new_transfer_from(asset: str, send_addr: str, from_addr: str, recv_addr: str, amount: int, payer: str,
                          gas_limit: int, gas_price: int) -> Transaction:
        raw_sender = Address.b58decode(send_addr)
        raw_from = Address.b58decode(from_addr)
        raw_to = Address.b58decode(recv_addr)
        raw_payer = Address.b58decode(payer)
        contract_address = util.get_asset_address(asset)  # []bytes
        args = {"sender": raw_sender, "from": raw_from, "to": raw_to, "amount": amount}
        invoke_code = build_native_invoke_code(contract_address, bytes([0]), "transferFrom", args)
        unix_time_now = int(time())
        return Transaction(0, 0xd1, unix_time_now, gas_price, gas_limit, raw_payer, invoke_code, bytearray(), [],
                           bytearray())

    def send_transfer_from(self, asset: str, sender: Account, from_addr: str, recv_addr: str, amount: int,
                           payer: Account, gas_limit: int, gas_price: int) -> str:
        if sender is None or payer is None:
            raise SDKException(ErrorCode.param_err('parameters should not be null'))
        if amount <= 0 or gas_price < 0 or gas_limit < 0:
            raise SDKException(ErrorCode.param_error)
        b58_payer = payer.get_address_base58()
        b58_sender = sender.get_address_base58()
        tx = Asset.new_transfer_from(asset, b58_sender, from_addr, recv_addr, amount, b58_payer, gas_limit, gas_price)
        tx = self.__sdk.sign_transaction(tx, sender)
        if b58_sender != b58_payer:
            tx = self.__sdk.add_sign_transaction(tx, payer)
        flag = self.__sdk.rpc.send_raw_transaction_pre_exec(tx)
        if flag:
            return tx.hash256(is_hex=True)
        else:
            return ''
