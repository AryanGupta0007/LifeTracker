import sqlite3
from config import config
from datetime import datetime
# // user details
# // todo details (linked with user table)
class db:
    def __init__(self):
        self.conn = sqlite3.connect(config['database']['name'])
        self.crsr = self.conn.cursor()
    def create_tables(self):
        self.crsr.execute(''' CREATE TABLE IF NOT EXISTS  user(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            username TEXT,
            userID INTEGER
        )''')

        self.crsr.execute(''' CREATE TABLE IF NOT EXISTS todo(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            task TEXT,
            date TEXT,
            time TEXT,
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

    def get_all_todos_of_current_time(self, date, time):
        self.crsr.execute('''SELECT * FROM todo WHERE DATE = ? AND TIME = ?''', (date, time,))
        results = self.crsr.fetchall()
        return results

    def get_all_todos(self):
        self.crsr.execute('''SELECT * FROM todo ''')
        results = self.crsr.fetchall()
        return results


class UserTable:
    def __init__(self):
        self.conn = sqlite3.connect(config['database']['name'])
        self.crsr = self.conn.cursor()


    def get_user_from_username_or_id(self, username=None, id=None):
        if username:
            self.crsr.execute(''' select * from user where
            username = ?''', (username, ))
        if id:
            self.crsr.execute(''' select * from user where
                        id = ?''', (id,))
        user = self.crsr.fetchone()
        if user:
            id = user[0]
            name = user[1]
            username = user[2]
            chat_id = user[3]
            user_details = {
                "id": id,
                "name": name,
                "username": username,
                "chatID": chat_id
            }
        else:
            user_details = None
        return user_details


    def insert(self, data):
        self.crsr.execute('''
        INSERT INTO user (username, name, userID) VALUES (?, ?, ?)''',
                          (data["username"], data["name"], data['userID'])
        )
        self.conn.commit()
        user = self.get_user_from_username_or_id(username=data['username'])
        return user


    def find_user_or_fail(self, data):
        username = data['username']
        print(username)
        user = self.get_user_from_username_or_id(username)
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
        current_datetime = datetime.now()
        print('here')
        # Format the date and time
        formatted_datetime = current_datetime.strftime('%d-%m-%Y %H:%M:%S')
        print(todo['task'], status, todo['date'], todo['time'],  formatted_datetime, self.user['id'])
        self.crsr.execute(''' INSERT INTO todo 
        (task, status, date, time,  createdAt, createdBy) VALUES (?, ?, ?, ?, ?, ?)
        ''', (todo['task'], status, todo['date'], todo['time'], formatted_datetime, int(self.user['id']), ))
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
        obj = UserTable()
        self.crsr.execute("SELECT * FROM todo WHERE id = ?", (id, ))
        todo = self.crsr.fetchone()
        print(f"{todo[8]}:  {type(todo[8])}")
        createdBy = obj.get_user_from_username_or_id(id=todo[8])
        todo_details = {
            "id": todo[0],
            "task": todo[1],
            "date": todo[2],
            "time": todo[3],
            "status": todo[4],
            "timetaken": todo[5],
            "createdAt": todo[6],
            "createdBy": createdBy
        }
        return todo_details


    def get_user_todos(self):
        obj_user = UserTable()
        user = obj_user.get_user_from_username_or_id(username=self.user["username"])
        self.crsr.execute('''SELECT * FROM todo where createdBy = ?''',
                          (user['id'], ))
        results = self.crsr.fetchall()
        return results