class User:

    def __init__(self, private_key=None):
        self._private_key = private_key
        self._created_at = None

    def get_private_key(self):
        return self._private_key

    def set_private_key(self, private_key):
        self._private_key = private_key

    def get_created_at(self, created_at):
        self._created_at = created_at

    def set_created_at(self, timestamp):
        self._created_at = timestamp
