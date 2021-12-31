from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Filters, MessageHandler

import config
import redis_utils
import utils


def new_member(update, context):
    try:
        chat_id = update.effective_message.chat_id
        new_user_id = update.message.new_chat_members[0].id
        message_id = update.message.message_id
        first_name, last_name = "", ""
        first_name = str(update.message.new_chat_members[0].first_name)
        last_name = str(update.message.new_chat_members[0].last_name)
        print("new_user_id: {} | message_id: {} | User Name: {} {}".format(new_user_id, message_id, first_name,
                                                                           last_name))
        chat = utils.get_chat(chat_id)
        if chat.pinned_message is not None:
            pinned_message_id = chat.pinned_message["message_id"]
            print("pinned_message_id: {}".format(pinned_message_id))
            chat_id = update.effective_message.chat_id
            conn = redis_utils.get_connection()
            conn.incrby("newMemberAmount:{}".format(chat_id))
            if not redis_utils.check_key_existence("welcomeMessageLock:{}".format(chat_id)):
                conn.set("welcomeMessageLock:{}".format(chat_id), "", ex=config.WELCOME_MESSAGE_CD)
                # utils.bot.send_message(
                #     chat_id=chat_id,
                #     text=config.WELCOME_MESSAGE,
                #     reply_to_message_id=63,
                # )
                message_url = "https://t.me/c/{}/{}".format(str(chat_id)[4:], pinned_message_id)
                # print(message_url)
                keyboard = [[InlineKeyboardButton("点击查看置顶消息", url=message_url)]]
                reply_markup = InlineKeyboardMarkup(keyboard)

                utils.bot.send_message(
                    chat_id=chat_id,
                    text=config.WELCOME_MESSAGE,
                    reply_markup=reply_markup
                )
            else:
                return
    except Exception as e:
        print(e)


send_pinned_message_handler = MessageHandler(Filters.status_update.new_chat_members, new_member)
