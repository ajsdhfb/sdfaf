from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CommandHandler

import config
import redis_utils
import utils


def test_command(update, context):
    chat_id = update.effective_message.chat_id
    conn = redis_utils.get_connection()
    if conn.get("welcomeMessageLock:{}".format(chat_id)) is None:
        conn.set("welcomeMessageLock:{}".format(chat_id), "", ex=3)
        utils.bot.send_message(
            chat_id=chat_id,
            text=config.WELCOME_MESSAGE,
            reply_to_message_id=63,
        )
    else:
        return


test_handler = CommandHandler('test', test_command)
