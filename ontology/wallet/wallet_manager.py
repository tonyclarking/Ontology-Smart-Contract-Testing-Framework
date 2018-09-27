#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import uuid
import base64
from datetime import datetime
from collections import namedtuple

from ontology.crypto.scrypt import Scrypt
from ontology.wallet.control import Control
from ontology.common.address import Address
from ontology.account.account import Account
from ontology.utils.util import is_file_exist
from ontology.wallet.wallet import WalletData
from ontology.wallet.account import AccountData
from ontology.common.error_code import ErrorCode
from ontology.wallet.account_info import AccountInfo
from ontology.exception.exception import SDKException
from ontology.wallet.identity import Identity, did_ont
from ontology.wallet.identity_info import IdentityInfo
from ontology.crypto.signature_scheme import SignatureScheme
from ontology.utils.util import get_random_bytes, get_random_str


class WalletManager(object):
    def __init__(self, scheme=SignatureScheme.SHA256withECDSA):
        self.scheme = scheme
        self.wallet_file = WalletData()
        self.wallet_in_mem = WalletData()
        self.wallet_path = ""

    def open_wallet(self, wallet_path: str):
        self.wallet_path = wallet_path
        if is_file_exist(wallet_path) is False:
            # create a new wallet file
            self.wallet_in_mem.createTime = datetime.today().strftime("%Y-%m-%d %H:%M:%S")
            self.save()
        # wallet file exists now
        self.wallet_file = self.load()
        self.wallet_in_mem = self.wallet_file
        return self.wallet_file

    def load(self):
        with open(self.wallet_path, "r") as f:
            fstr = f.read()
            r = json.loads(fstr.replace("enc-", "enc_"), object_hook=lambda d: namedtuple('X', d.keys())(*d.values()))
            # r = json.load(f, object_hook=lambda d: namedtuple('X', d.keys())(*d.values()))
            scrypt = Scrypt(r.scrypt.n, r.scrypt.r, r.scrypt.p, r.scrypt.dkLen)
            identities = []
            try:
                for index in range(len(r.identities)):
                    r_identities = r.identities[index]
                    control = [Control(id=r_identities.controls[0].id,
                                       algorithm=r_identities.controls[0].algorithm,
                                       param=r_identities.controls[0].parameters,
                                       key=r_identities.controls[0].key,
                                       address=r_identities.controls[0].address,
                                       salt=r_identities.controls[0].salt,
                                       enc_alg=r_identities.controls[0].enc_alg,
                                       hash_value=r_identities.controls[0].hash,
                                       public_key=r_identities.controls[0].publicKey)]
                    identities.append(Identity(r_identities.ont_id, r_identities.label, r_identities.lock, control))
            except AttributeError as e:
                pass

            accounts = []
            try:
                for index in range(len(r.accounts)):
                    temp = AccountData(label=r.accounts[index].label, public_key=r.accounts[index].publicKey,
                                       sign_scheme=r.accounts[index].signatureScheme,
                                       isDefault=r.accounts[index].isDefault,
                                       lock=r.accounts[index].lock, address=r.accounts[index].address,
                                       algorithm=r.accounts[index].algorithm, param=r.accounts[index].parameters,
                                       key=r.accounts[index].key, enc_alg=r.accounts[index].enc_alg,
                                       salt=r.accounts[index].salt)
                    accounts.append(temp)
            except AttributeError as e:
                pass
            default_ont_id = ""
            try:
                default_ont_id = r.defaultOntid
            except AttributeError as e:
                pass
            default_account_address = ""
            try:
                default_account_address = r.defaultAccountAddress
            except AttributeError as e:
                pass
            create_time = datetime.today().strftime("%Y-%m-%d %H:%M:%S")
            try:
                create_time = r.createTime
            except Exception as e:
                pass
            res = WalletData(r.name, r.version, create_time, default_ont_id, default_account_address, scrypt,
                             identities, accounts)
            return res

    def save(self):
        fstr = json.dumps(self.wallet_in_mem, default=lambda obj: obj.__dict__, sort_keys=True, indent=4)
        temp = fstr.replace("enc_", "enc-")
        f = open(self.wallet_path, "w")
        f.write(temp)
        f.close()

    def get_wallet(self):
        return self.wallet_in_mem

    def write_wallet(self):
        self.save()
        self.wallet_file = self.wallet_in_mem
        return self.wallet_file

    def reset_wallet(self):
        self.wallet_in_mem = self.wallet_file.clone()
        return self.wallet_in_mem

    def get_signature_scheme(self):
        return self.scheme

    def set_signature_scheme(self, scheme):
        self.scheme = scheme

    def import_identity(self, label: str, encrypted_pri_key: str, pwd: str, salt: str, address: str):
        pri_key = Account.get_gcm_decoded_private_key(encrypted_pri_key, pwd, address, salt,
                                                      Scrypt().get_n(), self.scheme)
        info = self.__create_identity(label, pwd, salt, pri_key)
        for index in range(len(self.wallet_in_mem.identities)):
            if self.wallet_in_mem.identities[index].ont_id == info.ont_id:
                return self.wallet_in_mem.identities[index]
        return None

    def create_identity(self, label: str, pwd: str):
        priv_key = get_random_str(64)
        salt = get_random_str(16)
        return self.__create_identity(label, pwd, salt, priv_key)

    def __create_identity(self, label: str, pwd: str, salt: str, private_key: str):
        acct = self.__create_account(label, pwd, salt, private_key, False)
        info = IdentityInfo()
        info.ont_id = did_ont + acct.get_address_base58()
        info.pubic_key = acct.serialize_public_key().hex()
        info.private_key = acct.serialize_private_key().hex()
        info.pri_key_wif = acct.export_wif()
        info.encrypted_pri_key = acct.export_gcm_encrypted_private_key(pwd, salt, Scrypt().get_n())
        info.address_u160 = acct.get_address().to_array().hex()
        return self.wallet_in_mem.get_identity_by_ont_id(info.ont_id)

    def create_identity_from_pri_key(self, label: str, pwd: str, private_key: str):
        salt = get_random_str(16)
        identity = self.__create_identity(label, pwd, salt, private_key)
        return identity

    def create_account(self, label: str, pwd: str) -> AccountData:
        pri_key = get_random_str(64)
        salt = get_random_str(16)
        account = self.__create_account(label, pwd, salt, pri_key, True)
        return self.wallet_file.get_account_by_address(account.get_address_base58())

    def __create_account(self, label: str, pwd: str, salt: str, priv_key: str, account_flag: bool):
        print(priv_key)
        account = Account(priv_key, self.scheme)
        # initialization
        if self.scheme == SignatureScheme.SHA256withECDSA:
            acct = AccountData()
        else:
            raise ValueError("scheme type is error")
        # set key
        if pwd is not None:
            acct.key = account.export_gcm_encrypted_private_key(pwd, salt, Scrypt().get_n())
        else:
            acct.key = account.serialize_private_key().hex()

        acct.address = account.get_address_base58()
        # set label
        if label is None or label == "":
            label = str(uuid.uuid4())[0:8]
        if account_flag:
            for index in range(len(self.wallet_in_mem.accounts)):
                if acct.address == self.wallet_in_mem.accounts[index].address:
                    raise ValueError("wallet account exists")

            if len(self.wallet_in_mem.accounts) == 0:
                acct.isDefault = True
                self.wallet_in_mem.defaultAccountAddress = acct.address
            acct.label = label
            acct.salt = base64.b64encode(salt.encode()).decode('ascii')
            acct.publicKey = account.serialize_public_key().hex()
            self.wallet_in_mem.accounts.append(acct)
        else:
            for index in range(len(self.wallet_in_mem.identities)):
                if self.wallet_in_mem.identities[index].ont_id == did_ont + acct.address:
                    raise ValueError("wallet identity exists")
            idt = Identity()
            idt.ontid = did_ont + acct.address
            idt.label = label
            if len(self.wallet_in_mem.identities) == 0:
                idt.isDefault = True
                self.wallet_in_mem.defaultOntid = idt.ontid
            ctl = Control(id="keys-1", key=acct.key, salt=base64.b64encode(salt.encode()).decode('ascii'),
                          address=acct.address,
                          public_key=account.serialize_public_key().hex())
            idt.controls.append(ctl)
            self.wallet_in_mem.identities.append(idt)
        return account

    def import_account(self, label: str, encrypted_pri_key: str, pwd: str, base58_addr: str, base64_salt: str):
        salt = base64.b64decode(base64_salt.encode('ascii')).decode('latin-1')
        private_key = Account.get_gcm_decoded_private_key(encrypted_pri_key, pwd, base58_addr, salt, Scrypt().get_n(),
                                                          self.scheme)
        info = self.create_account_info(label, pwd, salt, private_key)
        for index in range(len(self.wallet_in_mem.accounts)):
            if info.address_base58 == self.wallet_in_mem.accounts[index].address:
                return self.wallet_in_mem.accounts[index]
        return None

    def create_account_info(self, label: str, pwd: str, salt: str, private_key: str):
        acct = self.__create_account(label, pwd, salt, private_key, True)
        info = AccountInfo()
        info.address_base58 = Address.address_from_bytes_pubkey(acct.serialize_public_key()).b58encode()
        info.public_key = acct.serialize_public_key().hex()
        info.encrypted_pri_key = acct.export_gcm_encrypted_private_key(pwd, salt, Scrypt().get_n())
        info.address_u160 = acct.get_address().to_array().hex()
        info.salt = salt
        return info

    def create_account_from_prikey(self, label: str, pwd: str, private_key: str):
        salt = get_random_str(16)
        info = self.create_account_info(label, pwd, salt, private_key)
        for index in range(len(self.wallet_in_mem.accounts)):
            if info.address_base58 == self.wallet_in_mem.accounts[index].address:
                return self.wallet_in_mem.accounts[index]
        return None

    def get_account(self, address: str, pwd: str):
        for index in range(len(self.wallet_in_mem.accounts)):
            if self.wallet_in_mem.accounts[index].address == address:
                key = self.wallet_in_mem.accounts[index].key
                addr = self.wallet_in_mem.accounts[index].address
                salt = base64.b64decode(self.wallet_in_mem.accounts[index].salt)
                private_key = Account.get_gcm_decoded_private_key(key, pwd, addr, salt, Scrypt().get_n(), self.scheme)
                return Account(private_key, self.scheme)

        for index in range(len(self.wallet_in_mem.identities)):
            if self.wallet_in_mem.identities[index].ont_id == did_ont + address:
                addr = self.wallet_in_mem.identities[index].ont_id.replace(did_ont, "")
                key = self.wallet_in_mem.identities[index].controls[0].key
                salt = base64.b64decode(self.wallet_in_mem.identities[index].controls[0].salt)
                private_key = Account.get_gcm_decoded_private_key(key, pwd, addr, salt, Scrypt().get_n(), self.scheme)
                return Account(private_key, self.scheme)
        return None

    def get_default_identity(self) -> Identity:
        for identity in self.wallet_in_mem.identities:
            if identity.isDefault:
                return identity
        raise SDKException(ErrorCode.param_error)

    def get_default_account(self) -> AccountData:
        for acct in self.wallet_in_mem.accounts:
            if acct.isDefault:
                return acct
        raise SDKException(ErrorCode.get_default_account_err)

