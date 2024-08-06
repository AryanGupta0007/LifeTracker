from datetime import datetime
from telegram.ext import Application
from database import db, UserTable, TodoTable
import asyncio
from config import config

def calculate_time_difference(time1_str, time2_str):
  time1 = datetime.strptime(time1_str, "%H:%M")
  time2 = datetime.strptime(time2_str, "%H:%M")

  datetime_difference = str(time2 - time1).split(' ')
  date_difference = datetime_difference[0]
  time_difference = datetime_difference[2]
  return time_difference

def parse_the_todo(todo):
    return {
        "id": todo[0],
        "task": todo[1],
        "date": todo[2],
        "time": todo[3],
        "status": todo[4],
        "timetaken": todo[5],
        "createdAt": todo[6],
        "createdBy": todo[7]
    }


def get_todo_times(results):
    times = []
    for result in results:
        todo_time = result[3]
        times.append(todo_time)
    return times

async def do_reminders(bot):
    obj_user = UserTable()
    while True:
        now = datetime.now()
        current_date = datetime.strftime(now.date(), "%d-%m-%Y")
        current_time = now.strftime("%H:%M")
        # print(current_time)
        obj_db = db()
        print(f"current_date_str: {current_date}")
        results = obj_db.get_all_todos_of_current_time(current_date, current_time)
        for result in results:
            todo = parse_the_todo(result)
            print(todo)
            user = obj_user.get_user_from_username_or_id(id=todo["createdBy"])
            print(user)
            msg = f"It's the time for the task: {todo['task']}"
            await bot.send_message(chat_id=user["chatID"], text=msg)

        await asyncio.sleep(10)

async def main():
    app = Application.builder().token(config['Telegram']['API']).build()
    bot = app.bot
    await asyncio.create_task(do_reminders(app.bot))
    app.start_polling()

if __name__ == "__main__":
    asyncio.run(main())


