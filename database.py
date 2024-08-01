
import sqlite3
from config import config
from datetime import datetime
# // user details
# // todo details (linked with user table)
class db:
    conn = sqlite3.connect(config['database']['name'])
    crsr = conn.cursor()
    def create_tables(self):
        self.crsr.execute(''' CREATE TABLE IF NOT EXISTS  user(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            username TEXT
        )''')

        self.crsr.execute(''' CREATE TABLE IF NOT EXISTS todo(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            task TEXT,
            start TEXT,
            end TEXT,
            status TEXT,
            timeTaken TEXT,
            createdAt TEXT,
            createdBy INTEGER,
            FOREIGN KEY(createdBy) REFERENCES user(id)
        )''')

        self.crsr.execute(''' CREATE TABLE IF NOT EXISTS log(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            task TEXT,
            start TEXT,
            end TEXT,
            timeElapsed TEXT,
            createdAt TEXT,
            createdBy INTEGER,
            FOREIGN KEY(createdBy) REFERENCES user(id)
        )''')

        self.conn.commit()
        self.conn.close()


class UserTable:
    def __init__(self):
        self.conn = sqlite3.connect(config['database']['name'])
        self.crsr = self.conn.cursor()


    def get_user_from_username(self, username):
        self.crsr.execute(''' select * from user where
        username = ?''', (username, ))
        user = self.crsr.fetchone()
        if user:
            id = user[0]
            name = user[1]
            username = user[2]
            user_details = {
                "id": id,
                "name": name,
                "username": username
            }
        else:
            user_details = None
        return user_details


    def insert(self, data):
        self.crsr.execute('''
        INSERT INTO user (username, name) VALUES (?, ?)''', (data["username"], data["name"],)
        )
        self.conn.commit()
        user = self.get_user_from_username(username=data['username'])
        return user


    def find_user_or_fail(self, data):
        username = data['username']
        print(username)
        user = self.get_user_from_username(username)
        if user:
            return {'user': user, 'present': True}
        else:
            return {'user': None, 'present': False}


    def get_or_create_user(self, data):
        ## check current user or add new user
        user_present = self.find_user_or_fail(data)
        if user_present["present"] == True:
            msg =  "User already a member"
            print(user_present)
            user = user_present["user"]
            print(user)
        else:
            msg =  "User Created"
            user = self.insert(data)
            print(f"user: {user}")
        return {'msg': msg, 'user': user}


class LogTable:
    def __init__(self, user):
        self.conn = sqlite3.connect(config['database']['name'])
        self.crsr = self.conn.cursor()
        self.user = user

    def get_log_from_id(self, id):
        self.crsr.execute('''
        select * from log where id = ?''', (id,))
        log = self.crsr.fetchone()
        return log

    def insert(self, log):
        # Get the current date and time
        current_datetime = datetime.now()
        # Format the date and time
        formatted_datetime = current_datetime.strftime('%Y-%m-%d %H:%M:%S')
        self.crsr.execute('''
        INSERT INTO log (task, start, createdAt, createdBy) VALUES (?, ?, ?, ?)
        ''', (log["task"], log["start"], formatted_datetime, self.user['id'], ))
        self.conn.commit()
        log = self.get_log_from_id(id)


class TodoTable:

    def __init__(self, user):
        self.conn = sqlite3.connect(config['database']['name'])
        self.crsr = self.conn.cursor()
        self.user = user


    def insert(self, todo):
        status = 'created'
        start = f"{todo["date"]} {todo["time"]}"
        current_datetime = datetime.now()
        print('here')
        # Format the date and time
        formatted_datetime = current_datetime.strftime('%d-%m-%Y %H:%M:%S')
        print(todo['task'], status, start,  formatted_datetime, self.user['id'])
        self.crsr.execute(''' INSERT INTO todo 
        (task, status, start,  createdAt, createdBy) VALUES (?, ?, ?, ?, ?)
        ''', (todo['task'], status, start, formatted_datetime, int(self.user['id']), ))
        self.conn.commit()
        print('here2')
        self.crsr.execute('''SELECT * from todo where createdBy = ?''', (int(self.user['id']), ))
        results = self.crsr.fetchall()
        last_row_id = results[-1][0]
        print(last_row_id)

        todo = self.get_todo_from_id(last_row_id)
        print('here23')
        return todo


    def get_todo_from_id(self, id):
        self.crsr.execute("SELECT * FROM todo WHERE id = ?", (id, ))
        todo = self.crsr.fetchone()
        return todo

