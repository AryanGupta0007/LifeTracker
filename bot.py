from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext, ConversationHandler
from commands import *
from todo_conv_handler import *
from config import config


todo_conv_handler = ConversationHandler(
    entry_points=[CommandHandler('todo', start)],
    states={
        GET_TASK_NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_task_name)],
        GET_TASK_DATE: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_task_date)],
        ADD_TODO: [MessageHandler(filters.TEXT & ~filters.COMMAND, add_todo)],
    },
    fallbacks=[CommandHandler('cancel', cancel), MessageHandler(filters.COMMAND, handle_unknown_command)],
)


app = Application.builder().token(config['Telegram']['API']).build()
app.add_handler(CommandHandler('start', send_welcome))
app.add_handler(CommandHandler('audio', download_and_convert_video))
app.add_handler(CommandHandler('menu', show_menu))
app.add_handler(CommandHandler('todo_list', display_todos))
# Add your conversation handler here
app.add_handler(todo_conv_handler)
app.add_error_handler(error)
# Start the stock alert task
app.run_polling()
