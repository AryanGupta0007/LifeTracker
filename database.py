
import sqlite3
from config import config
# // user details
# // todo details (linked with user table)

class db:
    conn = sqlite3.connect(config['database']['name'])
    crsr = conn.cursor()
    def create_tables():
        db.crsr.execute(''' CREATE TABLE user(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            username TEXT
        )''')

        db.crsr.execute(''' CREATE TABLE todo(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            task TEXT,
            start TEXT,
            end TEXT,
            status TEXT,
            timeTaken TEXT,
            createdAt TEXT
        )''')

        db.conn.commit()
        db.conn.close()


class UserTable:
    def __init__(self, data):
        ## check current user or add new user
        pass

    def insert(self, data):
        db.crsr.execute('''
        INSERT INTO user (username, name) VALUES (?, ?), data['username'], data['name']
        ''')
        db.conn.commit()
        db.conn.close()


