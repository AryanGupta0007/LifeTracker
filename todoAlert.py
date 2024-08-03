from datetime import datetime
from telegram.ext import Application
from database import db
import asyncio
from config import config


async def do_reminders(bot):
    dates = []
    times = []
    while True:

        current_date = datetime.now().date()
        obj_db = db()
        results = obj_db.get_all_todos()
        for result in results:
            todo_date = result[2]
            todo_time = result[3]
            dt_todo_date = datetime.strptime(todo_date, "%d-%m-%Y").date()
            print(f"dateobj {dt_todo_date}")
            todo_datetime = f"{todo_date} {todo_time}:00"
            print(todo_datetime)
            dt_todo_datetime = datetime.strptime(todo_datetime, "%d-%m-%Y %H:%M:%S")
            print("datetime object", dt_todo_datetime)
            dates.append(dt_todo_date)
            times.append(dt_todo_datetime)
            print(f"date:{todo_date}, time:{todo_time}")

        print(f"current_date: {current_date}")
        if current_date in dates:
            print('Hain')
        else:
            print('nhi H')
        await asyncio.sleep(60)

async def main():
    app = Application.builder().token(config['Telegram']['API']).build()

    asyncio.create_task(do_reminders(app.bot))

    await app.initialize()
    try:
        await app.run_polling()
    finally:
        await app.shutdown()

if __name__ == "__main__":
    asyncio.run(main())
