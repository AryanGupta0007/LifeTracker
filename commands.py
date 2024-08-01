from database import db, UserTable, TodoTable

db = db()
db.create_tables()

async def send_welcome(update, context):
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
2. /todo-list : to show all todos with id 
3. /todo-edit : to edit a todo 
4. /todo-delete: to delete a todo 
"""


async def show_menu(update, context):
    global menu
    msg = menu
    await update.message.reply_text(msg)


async def error(update, context):
    print(f"update {update} caused error {context.error}")



