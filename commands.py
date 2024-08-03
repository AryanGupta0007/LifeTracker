from database import db, UserTable, TodoTable
from datetime import datetime

db = db()
db.create_tables()

async def send_welcome(update, context):
    obj = UserTable()
    data = {
        'name': f"{update.message.from_user.first_name} {update.message.from_user.last_name}",
        'username': update.message.from_user.username,
        'userID': update.message.from_user.id
    }
    res = obj.get_or_create_user(data)
    user = res["user"]
    msg = f"Welcome {user}! Enter /menu to see the list of all commands."
    await update.message.reply_text(msg)


async def display(update, context):
    obj = UserTable()
    data = {
        'name': f"{update.message.from_user.first_name} {update.message.from_user.last_name}",
        'username': update.message.from_user.username
    }

    res = obj.get_or_create_user(data)
    user = res["user"]
    msg = f"Welcome {user}! Enter /menu to see the list of all commands."
    await update.message.reply_text(msg)


menu = """ Commands List
1. /todo: to add a new todo
2. /todo_list : to show all todos with id 
3. /todo_edit : to edit a todo 
4. /todo_delete: to delete a todo 
"""

async def show_menu(update, context):
    global menu
    msg = menu
    await update.message.reply_text(msg)


async def error(update, context):
    print(f"update {update} caused error {context.error}")


async def display_todos(update, context):
    username = update.message.from_user.username
    obj_user = UserTable()
    current_user = obj_user.get_user_from_username_or_id(username)
    obj_todo = TodoTable(current_user)
    todos = obj_todo.get_user_todos()
    for todo in todos:
        await update.message.reply_text(f"task name: {todo[1]}  id: {todo[0]}")
    print(f"User todos: {todos}")



