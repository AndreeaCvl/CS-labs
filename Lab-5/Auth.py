import hashlib


class Auth:
    def __init__(self, db):
        self.db = db

    def register(self, username, password, user_role):

        # utf-8 encoding for the password
        password = password.encode('utf-8')

        hashed_password = hashlib.sha256(password).hexdigest()

        self.db.add_record(username, hashed_password, user_role)
        password = hashed_password

    def login(self, username, password):
        user = self.db.search_by_username(username)

        password = password.encode('utf-8')
        hashed_password = hashlib.sha256(password).hexdigest()

        if hashed_password == user['password']:
            return True
        else:
            return False



