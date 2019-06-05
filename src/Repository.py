from tinydb import TinyDB
import os
from User import User
from Transaction import Transaction


class Repository:

    _db_path = os.path.abspath('../.db/.wallet.db')
    table_user = 'users'
    table_transaction = 'transactions'

    def __init__(self):
        self._db = None

    def init_db(self):
        self._db = TinyDB(Repository._db_path)

    def get_table(self, table_name):
        table_exists = table_name == Repository.table_transaction \
                    or table_name == Repository.table_user

        assert table_exists, 'Given table does not exist.'

        return self._db.table(table_name)

    def get_user(self, private_key):
        user_docs = self.get_table(Repository.table_user).all()
        users = [User.deserialize_user(doc) for doc in user_docs]

        for user in users:
            if user.get_private_key() == private_key:
                return user

        return None

    def get_transactions(self):
        txs_docs = self.get_table(Repository.table_transaction).all()
        txs = [Transaction.deserialize(doc) for doc in txs_docs]

        return txs

    def save_user(self, user):
        # check if user already exists
        if self.get_user(user.get_private_key()):
            raise Exception("Cannot save user, it already exists in db.")
        else:
            users_tb = self.get_table(Repository.table_user)
            users_tb.insert(user.serialize())

            return user
