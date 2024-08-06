from database import db, UserTable, TodoTable
from datetime import datetime
from download_and_convert_yt_video import *
import os
import time
db = db()
db.create_tables()

async def download_and_convert_video(update, context):
    # shutil.rmtree('./downloads')
    # shutil.rmtree('./mp3_files')
    # os.remove('./mp3_files.zip')
    args = context.args
    obj_user = UserTable()
    current_user = obj_user.get_user_from_username_or_id(username=update.message.from_user.username)
    get_audio(links=args)
    os.chdir("..")
    print("currently", os.getcwd())

    # extension = ".mkv"
    create_zip_for_user()
    print(current_user)
    # download_youtube_video(link, file_name=title)

    # os.mkdir(path)
    # print(file_extensionextension)
    print(os.getcwd())
    # extension = convert_file_to_mp3(file_name=title)
    # extension = ".webm"
    # print(extension)
    # file = title + extension
    #
    # delete_file(file)
    #
    # create_zip_folder()
    with open(f'mp3_files.zip', 'rb') as zip_file:
        "here"
        await context.bot.send_document(chat_id=current_user['chatID'], document=zip_file)

        # i += 1

    #     file_name = "test" + str(i)
        # download_youtube_video(arg, file_name=file_name)
        # convert_file_to_mp3(file_name=file_name)
    # file_name = "test1"
    # audio = get_audio_file(file=f"{file_name}.mp3")
    # with open("test1.mp3", 'rb') as audio:
    #     await context.bot.send_audio(chat_id=current_user['chatID'], audio=audio)
    # print(audio)
    # i += 1
    print(args)

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



