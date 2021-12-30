from telegram import Chat, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Filters, MessageHandler
from func import keyword_reply, ad_delete, group_info

import config
import utils


def message_dispatcher(update, context):
    user_id = update.effective_user.id
    chat_id = update.effective_message.chat_id
    message_id = update.message.message_id
    user_message_content = update.message.text
    print("message_dispatcher | chat_id: {} | user_id: {} | message_id: {} | content: {}".format(
        chat_id, user_id, message_id, user_message_content))
    ad_check = ad_delete.ad_delete_handler(update, context)
    if ad_check is False:
        keyword_reply.keyword_reply_handler(update, context)
        group_info.info_exec(update, context)


message_dispatcher_handler = MessageHandler(Filters.text, message_dispatcher)
