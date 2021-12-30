import telegram

import config
from config import TOKEN

bot = telegram.Bot(token=TOKEN)


def get_chat(chat_id):
    chat = bot.get_chat(chat_id=chat_id, timeout=5)
    return chat


def is_bot_admin(user_id):
    return user_id in config.ADMIN


def is_admin_in_this_group(update, user_id, group_id):
    try:
        user = update.message.from_user
        try:
            is_bot = user["is_bot"]
            username = update.effective_user.username
        except Exception as e:
            is_bot = False
            username = update.effective_user.id
        is_group_anonymous_bot = False
        if is_bot and (username == "GroupAnonymousBot" or username == "Channel_Bot"):
            is_group_anonymous_bot = True
        chat_member = bot.get_chat_member(group_id, user_id)
        status = chat_member["status"]
        if status == "creator" or status == "administrator" or user_id in config.ADMIN or is_group_anonymous_bot:
            return True
        else:
            return False
    except Exception as e:
        return False


def send_message(chat_id, message):
    bot.send_message(
        chat_id=chat_id,
        text=message
    )
