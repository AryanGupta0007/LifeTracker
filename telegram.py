import telebot
from config import config
from database import *
bot = telebot.TeleBot(config['Telegram']['API'])


class Telegram:
    def __init__(self, message):
        self.username = message.from_user.username
        self.name = message.from_user.first_name + message.from_user.last_name

@bot.message_handler(commands=['start'])
def send_welcome(message):
    obj = UserTable()
    data = {
        'name': message.from_user.name,
        'username': message.from_user.username
    }
    obj.insert(data)
    bot.reply_to(message, "Hello, I'm the bot! Use /begin to start using the bot")


@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.reply_to(message, "message.text")


bot.infinity_polling()