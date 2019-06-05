import math
import json
import time
from hashlib import sha256
from Input import Input
from Output import Output


class Transaction:

    def __init__(self, inputs, outputs, fees=0.0):
        self._inputs = inputs
        self._outputs = outputs
        # if fees arg is not passed calculate it dynamically
        self._fees = float(fees)
        self._hash = self.compute_hash()

    def get_hash(self):
        return self._hash

    def set_hash(self, str_hash):
        self._hash = str_hash

    def get_inputs(self):
        return self._inputs

    def get_outputs(self):
        return self._outputs

    def get_output(self, index):
        return self._outputs[index]

    def get_total_inputs(self):
        # get value of all inputs in a list
        tx_input_values = list(map(lambda i: i.get_value(), self._inputs))

        return math.fsum(tx_input_values)

    def get_total_outputs(self):
        # get all values from outputs
        tx_output_values = list(map(lambda o: o.get_value(), self._outputs))

        return math.fsum(tx_output_values)

    def calculate_fees(self):
        return self.get_total_inputs() - self.get_total_outputs()

    def get_fees_amount(self):
        return self._fees

    def set_fees(self, fees):
        self._fees = fees

    def _get_data_obj(self):
        data = {
            "inputs": [i.serialize() for i in self._inputs],
            "outputs": [o.serialize() for o in self._outputs]
        }

        return data

    def serialize(self):
        """Returns object as dictionary"""
        data = {
            "hash": self._hash,
            **self._get_data_obj(),  # use unpack operator to include tx_data
            "fees": self.get_fees_amount()
        }

        return data

    @staticmethod
    def deserialize(data):
        tx_i = [Input.deserialize(s_txi) for s_txi in data['inputs']]
        tx_o = [Output.deserialize(s_txo) for s_txo in data['outputs']]
        fees = data['fees']
        tx = Transaction(tx_i, tx_o, fees)
        tx.set_hash(data['hash'])

        return tx

    def compute_hash(self):
        # get tx data object (dictionary) of current instance and convert it to str
        tx_data = json.dumps(self._get_data_obj())
        # concatenate json + time.time() so the hash is never the same
        # prevent same coinbase txs (on blockchain engine) to have same hashes
        data = (tx_data + str(time.time())).encode().decode("utf-8")

        return sha256(data.encode()).hexdigest()
