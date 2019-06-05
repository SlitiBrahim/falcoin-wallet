import crypto
from Output import Output
import math
import json


class Input:

    def __init__(self, prev_tx, index, output_ref):
        self._prev_tx = prev_tx
        self._index = index
        self._output_ref = output_ref
        self._pubsig = None

    def get_prev_tx(self):
        return self._prev_tx

    def get_index(self):
        return self._index

    def set_pubsig(self, pubsig):
        self._pubsig = pubsig

    def get_output_ref(self):
        return self._output_ref

    def is_empty(self):
        return self._prev_tx is None and self._index < 0

    # def can_unlock(self, data, blockchain):
    #     """Check that output_ref could be unlocked.
    #     output_ref's receiver must be the one who signed the current input
    #     """
    #
    #     if self.__output_ref.is_spent(blockchain):
    #         return False
    #
    #     # get output_ref's receiver
    #     txo_receiver_pubkey = self.__output_ref.get_pubkey()
    #
    #     # return True if the signature matches the outputs' public_key
    #     return crypto.verify_signature(self.__pubsig, data, txo_receiver_pubkey)

    def get_value(self):
        return self._output_ref.get_value()

    def serialize(self, with_pubsig=True):
        data = {
            "prev_tx": self._prev_tx,
            "index": self._index,
            "output_ref": self._output_ref.serialize() if self._output_ref else None,
        }

        if with_pubsig:
            data["pubsig"] = self._pubsig

        return data

    @staticmethod
    def deserialize(data):
        prev_tx = data['prev_tx']
        index = data['index']

        if data['output_ref'] is not None:
            output_ref = Output.deserialize(data['output_ref'])
        else:
            output_ref = None

        input = Input(prev_tx, index, output_ref)
        input.set_pubsig(data['pubsig'])

        return input

    def dump_serialization(self, with_pubsig=True):
        data = json.dumps(self.serialize(with_pubsig))

        return data

    @staticmethod
    def generate_pubsig(input, private_key):
        data = input.dump_serialization(with_pubsig=False)
        sig = crypto.sign_message(data, private_key)

        return sig

    @staticmethod
    def total_input_values(inputs):
        tx_input_values = [input.get_output_ref().get_value() for input in inputs]

        return math.fsum(tx_input_values)

