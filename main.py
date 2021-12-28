from telegram.ext import Updater
from config import TOKEN
# from func import get_new_member_handler, start_handler
from func import start_command, new_member_welcome_message

updater = Updater(token=TOKEN, use_context=True)
dispatcher = updater.dispatcher


dispatcher.add_handler(start_command.start_handler)
dispatcher.add_handler(new_member_welcome_message.send_pinned_message_handler)


updater.start_polling()
