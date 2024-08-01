from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, filters, CallbackContext, ConversationHandler
import commands
# Define states for the conversation
GET_NAME, GET_SEARCH_QUERY = range(2)

def start(update: Update, context: CallbackContext) -> int:
    update.message.reply_text('Welcome! Type /profile to enter your profile name or /search to search for something.')
    return ConversationHandler.END

def get_profile_name(update: Update, context: CallbackContext) -> int:
    update.message.reply_text('Please type your name:')
    return GET_NAME

def handle_name(update: Update, context: CallbackContext) -> int:
    user_name = update.message.text
    update.message.reply_text(f'Your name is {user_name}.')
    update.message.reply_text('Would you like to do something else? (Type /profile or /search)')
    return ConversationHandler.END

def get_search_term(update: Update, context: CallbackContext) -> int:
    update.message.reply_text('What do you want to search for?')
    return GET_SEARCH_QUERY

def handle_search_query(update: Update, context: CallbackContext) -> int:
    search_query = update.message.text
    # Implement actual search functionality here
    update.message.reply_text(f'You searched for: {search_query}.')
    update.message.reply_text('Would you like to do something else? (Type /profile or /search)')
    return ConversationHandler.END

def cancel(update: Update, context: CallbackContext) -> int:
    update.message.reply_text('Operation cancelled.')
    return ConversationHandler.END

def main() -> None:
    # Replace 'YOUR_TOKEN' with your bot's token
    updater = Updater("7269123829:AAHKzU7mfJ1V8v01eHe3XFG8IYI-r9NvWZY", use_context=True)

    dispatcher = updater.dispatcher

    # Set up ConversationHandler with the states
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('profile', get_profile_name), CommandHandler('search', get_search_term)],
        states={
            GET_NAME: [MessageHandler(Filters.text & ~Filters.command, handle_name)],
            GET_SEARCH_QUERY: [MessageHandler(Filters.text & ~Filters.command, handle_search_query)],
        },
        fallbacks=[CommandHandler('cancel', cancel)],
    )

    dispatcher.add_handler(conv_handler)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT, SIGTERM or SIGABRT
    updater.idle()

if __name__ == '__main__':
    main()
