import re

from telegram import Chat, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Filters, MessageHandler, CommandHandler

import config
import redis_utils
import utils


def get_keyword_list(update, context):
    chat_id = update.effective_message.chat_id
    message_id = update.message.message_id
    user_id = update.effective_user.id
    user = update.message.from_user
    chat_type = update.effective_chat.type
    if chat_type == "private":
        update.message.reply_text("此命令只有在群组中有效")
        return
    if not utils.is_admin_in_this_group(update, user_id, chat_id):
        utils.send_message(chat_id, "非管理员，无权操作")
        return
    conn = redis_utils.get_connection()
    group_keyword_set = conn.smembers("keywordReplySet:{}".format(chat_id))
    if group_keyword_set is None:
        return
    # print(group_keyword_set)
    key_value_list = []
    msg = "该群组存在的关键词：\n"
    num = 1
    for i in group_keyword_set:
        reply_content = redis_utils.get_key("keywordReplyContent:{}:{}".format(chat_id, str(i)))
        key_value_list.append([i, reply_content])
        msg = msg + str(num) + "、{}:\n{}\n\n".format(i, reply_content)
        num += 1
    print(msg)
    utils.bot.send_message(
        chat_id=user_id,
        text=msg,
        disable_web_page_preview=True
    )


def get_ad_list(update, context):
    chat_id = update.effective_message.chat_id
    message_id = update.message.message_id
    user_id = update.effective_user.id
    user = update.message.from_user
    chat_type = update.effective_chat.type
    if chat_type == "private":
        update.message.reply_text("此命令只有在群组中有效")
        return
    if not utils.is_admin_in_this_group(update, user_id, chat_id):
        utils.send_message(chat_id, "非管理员，无权操作")
        return
    conn = redis_utils.get_connection()
    group_keyword_set = conn.smembers("adKeywordSet:{}".format(chat_id))
    if group_keyword_set is None:
        return
    # print(group_keyword_set)
    msg = "该群组存在的违禁词：\n"
    num = 1
    for i in group_keyword_set:
        msg = msg + str(num) + "、{}\n\n".format(i)
        num += 1
    print(msg)
    utils.bot.send_message(
        chat_id=user_id,
        text=msg,
        disable_web_page_preview=True
    )


def get_white_url_list(update, context):
    chat_id = update.effective_message.chat_id
    message_id = update.message.message_id
    user_id = update.effective_user.id
    user = update.message.from_user
    chat_type = update.effective_chat.type
    if chat_type == "private":
        update.message.reply_text("此命令只有在群组中有效")
        return
    if not utils.is_admin_in_this_group(update, user_id, chat_id):
        utils.send_message(chat_id, "非管理员，无权操作")
        return
    conn = redis_utils.get_connection()
    group_white_url_set = conn.smembers("whiteUrlSet:{}".format(chat_id))
    if group_white_url_set is None:
        return
    # print(group_white_url_set)
    msg = "该群组存在的白名单URL：\n"
    num = 1
    for i in group_white_url_set:
        msg = msg + str(num) + "、{}\n\n".format(i)
        num += 1
    # print(msg)
    utils.bot.send_message(
        chat_id=user_id,
        text=msg,
        disable_web_page_preview=True
    )


get_keyword_list_handler = CommandHandler('get_keyword_list', get_keyword_list)
get_ad_list_handler = CommandHandler('get_ad_list', get_ad_list)
get_white_url_list_handler = CommandHandler('get_white_url_list', get_white_url_list)
