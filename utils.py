import telegram
from telegram.ext import MessageHandler, Filters
from telegram.ext.dispatcher import run_async
from config import TOKEN

bot = telegram.Bot(token=TOKEN)


def get_chat(chat_id):
    chat = bot.get_chat(chat_id=chat_id, timeout=5)
    return chat
