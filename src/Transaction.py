import math
import json
import time
from hashlib import sha256
from Input import Input
from Output import Output


class Transaction:

    fees_default_amount = 0.0

    def __init__(self, inputs, outputs, fees=None):
        self._inputs = inputs
        self._outputs = outputs
        self._fees = float(fees) if fees is not None else None
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

    @staticmethod
    def make_transaction(user, amount, pubkey, fees, api_manager):
        """Construct and return a Transaction object.
        Set the required inputs and outputs (and change too).
        Assumes that the given user has enough funds, check for funds first."""

        # all txs where user is involved, either as sender or receiver
        user_txs = api_manager.get_transactions(user.get_public_key())

        # get all tx outputs for txs where user is involved as sender or receiver
        utxos = Output.get_unspent_txos(user_txs)
        # filter unspent tx outputs by keeping only those belonging to the user
        user_utxos = Output.filter_ouputs_by_owner(utxos, user)

        tx_inputs = []
        total_inputs = 0.0
        # get required outputs so total >= tx's amount
        while total_inputs + fees < amount:
            # get oldest outputs first (no specific reason for that)
            utxo = user_utxos.pop(0)
            utxo_information = api_manager.get_output_info(utxo)
            if utxo_information is None:
                print("Error: Failed to got output information.")
                # TODO: Handle error
                return

            prev_tx = utxo_information['tx_hash']
            index = utxo_information['txo_index']

            tx_input = Input(prev_tx, index, utxo)
            tx_inputs.append(tx_input)
            total_inputs = Input.total_input_values(tx_inputs)

        # sign inputs with user's private_key
        for tx_input in tx_inputs:
            tx_input.set_pubsig(Input.generate_pubsig(tx_input, user.get_private_key()))

        # add a new output for the receiver
        tx_outputs = [Output(amount, pubkey, False)]

        # if fees is set (otherwise all remaining will belongs to the miner)
        # and is there a remaining, create a change output back to the sender
        if fees is not None and (total_inputs + fees) > amount:
            remaining_amount = (total_inputs + fees) - amount
            change_output = Output(remaining_amount, user.get_public_key(), False)
            tx_outputs.append(change_output)

        tx = Transaction(tx_inputs, tx_outputs, fees)

        return tx
