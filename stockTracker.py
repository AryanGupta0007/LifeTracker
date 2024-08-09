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
target_price = 110
stop_loss_price = 80



async def send_stock_alert(bot):
    global symbol
    while True:
        try:
            obj_share_data = ShareData(symbol)
            regular_price = round(obj_share_data.get_market_price(), 3)
            print(f"Regular price: {regular_price}")

            if regular_price > (target_price - 2):
                await bot.send_message(chat_id=chat_id, text=f"symbol: {symbol} price: {regular_price} near target")
                print("Sent bot message")
            elif regular_price < (stop_loss_price + 3):
                await bot.send_message(chat_id=chat_id, text=f"symbol: {symbol} price: {regular_price} near stop loss")
                print("Sent bot message")

        except Exception as e:
            print(f"Error occurred during stock alert: {e}")  # Log or retry

        await asyncio.sleep(60)

async def main():
    try:
        # Initialize your bot
        token = config['Telegram']['API']
        app = Application.builder().token(token).build()

        bot = app.bot
        await asyncio.create_task(send_stock_alert(bot))
        app.start_polling()

    except Exception as e:
        print(f"An error occurred: {e}")



if __name__ == '__main__':
    asyncio.run(main())