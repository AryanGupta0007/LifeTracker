from telegram import Update
from telegram.ext import ConversationHandler
from database import UserTable, TodoTable


GET_TASK_NAME, GET_TASK_DATE, ADD_TODO = range(3)


async def start(update: Update, context) -> int:
    user_name = update.message.from_user.username
    context.user_data[user_name] = {}
    context.user_data[user_name]['todo'] = {}
    await update.message.reply_text("Welcome! Please enter your to-do item.")
    return GET_TASK_NAME


async def get_task_name(update: Update, context) -> int:
    user_name = str(update.message.from_user.username)
    task = update.message.text
    context.user_data[user_name]['todo']['task'] = task
    print(f"User {user_name} task name: {task}")  # Replace with actual storage logic
    await update.message.reply_text(f"Enter your task date (Valid format DD-MM-YY). eg: 09-12-2003")
    return GET_TASK_DATE


async def get_task_date(update: Update, context) -> int:
    user_name = str(update.message.from_user.username)
    date = update.message.text
    context.user_data[user_name]['todo']['date'] = date
    print(f"User {user_name} task date {date}")  # Replace with actual storage logic
    await update.message.reply_text(f"Enter the time for the task (24 hr format H:M) ex: 20:02 or 07:09")
    return ADD_TODO


async def add_todo(update: Update, context) -> int:
    user_name = str(update.message.from_user.username)
    time = update.message.text
    obj_user = UserTable()
    current_user = obj_user.get_user_from_username_or_id(user_name)
    print(f"current_user: {current_user}")
    obj_todo = TodoTable(current_user)
    context.user_data[user_name]['todo']['time'] = time
    todo_dict = context.user_data[user_name]['todo']
    print(todo_dict)
    added_todo = obj_todo.insert(todo_dict)
    print(added_todo)
    print(f"Task added")  # Replace with actual storage logic
    await update.message.reply_text(f"Task: {added_todo['task']} added with id: {added_todo['id']}.")
    return ConversationHandler.END


async def handle_unknown_command(update: Update, context) -> int:
    await update.message.reply_text("Unknown command.")
    return ConversationHandler.END


async def cancel(update: Update, context) -> int:
    user_name = str(update.message.from_user.username)
    context.user_data[user_name]['state'] = 'start'
    await update.message.reply_text("Conversation canceled.")
    return ConversationHandler.END
