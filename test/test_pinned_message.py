import telegram
from telegram.ext import MessageHandler, Filters
from telegram.ext.dispatcher import run_async
from config import TOKEN

bot = telegram.Bot(token=TOKEN)


def get_pinned_message(update, context):
    pass


chat = bot.get_chat(chat_id=-725032027, timeout=5)
chat.unpin_all_messages()
# get_pinned_message_handler = MessageHandler()
