from urllib import request, parse
import json
from Transaction import Transaction


class ApiManager:

    base_url = 'http://localhost:8080'
    get_balance_url = base_url + '/balance/'
    list_transactions_url = base_url + '/transactions'
    list_transactions_user_url = list_transactions_url + '?pubkey='
    output_info_url = base_url + '/output_information'

    @staticmethod
    def get_balance(public_key):
        url = ApiManager.get_balance_url + public_key

        with request.urlopen(url) as url:
            data = json.loads(url.read().decode())
            balance = float(data['balance'])

        return balance

    @staticmethod
    def get_transactions(pubkey=None):
        if pubkey is not None:
            url = ApiManager.list_transactions_user_url + pubkey
        else:
            url = ApiManager.list_transactions_url

        with request.urlopen(url) as url:
            data = json.loads(url.read().decode())
            txs = [Transaction.deserialize(tx) for tx in data['transactions']]

        return txs

    @staticmethod
    def get_output_info(output):
        url = ApiManager.output_info_url
        data = parse.urlencode(output.serialize()).encode()
        req = request.Request(url, data=data)

        with request.urlopen(req) as resp:
            data = json.loads(resp.read().decode())

            if 'error' in data:
                return None

            return data
