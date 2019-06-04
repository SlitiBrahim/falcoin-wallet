import time
import json
import math
from hashlib import sha256


class Output:

    def __init__(self, value, pubkey, timestamp=None):
        self._value = value
        self._pubkey = pubkey
        self._timestamp = timestamp if timestamp else time.time()

    def get_value(self):
        return self._value

    def get_pubkey(self):
        return self._pubkey

    def serialize(self):
        data = {
            "value": self._value,
            "pubkey": self._pubkey,
            "time": self._timestamp
        }

        return data

    @staticmethod
    def deserialize(data):
        value = data['value']
        pubkey = data['pubkey']
        timestamp = data['time']

        return Output(value, pubkey, timestamp)

    def hash(self):
        """Returns hash of output"""
        data = json.dumps(self.serialize())
        hash = sha256(data.encode()).hexdigest()

        return hash

    @staticmethod
    def total_output_values(outputs):
        tx_output_values = [output.get_value() for output in outputs]

        return math.fsum(tx_output_values)
