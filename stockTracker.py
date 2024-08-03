from database import db, UserTable
from ShareData import ShareData
from telegram.ext import Application
import asyncio
from config import config

obj_user = UserTable()
me = "AryanGupta777"
my_account = obj_user.get_user_from_username_or_id(username=me)
chat_id = my_account['chatID']
symbol = "PCJEWELLER.NS"
target_price = 90

async def send_stock_alert(bot):
    print("Hello")
    global symbol
    while True:
        try:
            obj_share_data = ShareData(symbol)
            regular_price = round(obj_share_data.get_market_price(), 3)
            print("regular_price")
            if regular_price < (target_price + 6):
                await bot.send_message(chat_id=chat_id, text=f"symbol: {symbol} price: {regular_price}")
                print("bot msg")
                await asyncio.sleep(60)
                print("Wait time")
        except Exception as e:
            print(f"Error occurred during stock alert: {e}")  # Log or retry

async def main():
    # Initialize your bot and other handlers here
    app = Application.builder().token(config['Telegram']['API']).build()

    # Start the stock alert task
    asyncio.create_task(send_stock_alert(app.bot))

    await app.initialize()
    try:
        await app.run_polling()
    finally:
        await app.shutdown()

if __name__ == '__main__':
    asyncio.run(main())
