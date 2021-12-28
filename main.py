from telegram.ext import Updater
from config import TOKEN
import threading
from telegram.ext import CommandHandler, Filters, MessageHandler
from func import new_member_welcome_message, start_command


updater = Updater(token=TOKEN, use_context=True)
dispatcher = updater.dispatcher


dispatcher.add_handler(start_command)
dispatcher.add_handler(new_member_welcome_message)


updater.start_polling()
