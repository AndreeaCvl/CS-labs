import sqlite3


class DB:
    def __init__(self):
        self.db = None
        self.cursor = None

    def connect(self):
        self.db = sqlite3.connect(':memory:', check_same_thread=False)

        self.db.execute('''CREATE TABLE users
                (USERNAME           TEXT    NOT NULL,
                PASSWORD           TEXT    NOT NULL);''')

        self.db.commit()
        self.cursor = self.db.cursor()
        self.db.row_factory = sqlite3.Row

    def add_record(self, username, password):
        add_record_query = """INSERT INTO users (username, password) \
              VALUES (?, ?);"""

        self.cursor.execute(add_record_query, (username, password))
        self.db.commit()

    def fetch_database(self):
        self.cursor.execute("SELECT * FROM users")
        rows = self.cursor.fetchall()

        users = list()

        # convert row objects to dictionary
        for i in rows:
            user = {"username": i[0], "password": i[1]}
            users.append(user)

        return users
