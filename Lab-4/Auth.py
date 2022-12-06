import hashlib


class Auth:
    def __init__(self, db):
        self.db = db
        self.username = None
        self.password = None

    def start_auth(self):
        # username = input('Write your username\n')
        # password = input('Write your password?\n')

        self.username = "AndreeaCvl"
        password = 'BLINK182'

        # utf-8 encoding for the password
        password = password.encode('utf-8')

        hashed_password = hashlib.sha256(password).hexdigest()

        self.db.add_record(self.username, hashed_password)
        self.password = hashed_password
