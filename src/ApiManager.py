import urllib.request
import json


class ApiManager:

    base_url = 'http://localhost:8080'
    get_balance_url = base_url + '/balance/'

    @staticmethod
    def get_balance(public_key):
        url = ApiManager.get_balance_url + public_key

        with urllib.request.urlopen(url) as url:
            data = json.loads(url.read().decode())
            balance = float(data['balance'])

        return balance
