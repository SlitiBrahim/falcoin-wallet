import time
import json
import math
from hashlib import sha256


class Output:

    def __init__(self, value, pubkey, spent, timestamp=None):
        self._value = value
        self._pubkey = pubkey
        self._timestamp = timestamp if timestamp else time.time()
        self._spent = spent

    def get_value(self):
        return self._value

    def get_pubkey(self):
        return self._pubkey

    def is_spent(self):
        return self._spent

    def set_is_spent(self, spent=True):
        self._spent = spent

    def serialize(self):
        data = {
            "value": self._value,
            "pubkey": self._pubkey,
            "time": self._timestamp,
            "spent": self._spent
        }

        return data

    @staticmethod
    def deserialize(data, include_spent=True):
        value = data['value']
        pubkey = data['pubkey']
        timestamp = data['time']

        if include_spent:
            spent = data['spent']
        else:
            # default value (input.output_ref does not contains spent key)
            spent = False

        return Output(value, pubkey, spent, timestamp)

    def hash(self):
        """Returns hash of output"""
        data = json.dumps(self.serialize())
        hash = sha256(data.encode()).hexdigest()

        return hash

    @staticmethod
    def total_output_values(outputs):
        tx_output_values = [output.get_value() for output in outputs]

        return math.fsum(tx_output_values)

    @staticmethod
    def get_unspent_txos(transactions):
        utxos = []
        for tx in transactions:
            for txo in tx.get_outputs():
                if not txo.is_spent():
                    utxos.append(txo)

        return utxos

    @staticmethod
    def filter_ouputs_by_owner(outputs, user):
        user_txos = []

        for txo in outputs:
            if txo.get_pubkey() == user.get_public_key():
                user_txos.append(txo)

        return user_txos
