from telegram.ext import Updater
from config import TOKEN
from func import new_member_welcome_message, start_command


updater = Updater(token=TOKEN, use_context=True)
dispatcher = updater.dispatcher


dispatcher.add_handler(start_command)
dispatcher.add_handler(new_member_welcome_message)


updater.start_polling()
