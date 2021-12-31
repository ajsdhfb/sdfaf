import re

from telegram import Chat, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Filters, MessageHandler, CommandHandler

import config
import redis_utils
import utils


def url_white_list_handler(update, context):
    print("enter url_white_list_handler")
    chat_id = update.effective_message.chat_id
    message_id = update.message.message_id
    user_message_content = update.message.text
    # print(chat_id, user_message_content)
    conn = redis_utils.get_connection()
    group_white_url_set = conn.smembers("whiteUrlSet:{}".format(chat_id))
    if group_white_url_set is None:
        return False
    # print(group_keyword_set)
    for i in group_white_url_set:
        if str(i) in user_message_content:
            return True
    return False


def add_url(update, context):
    print("add_url")
    chat_id = update.effective_message.chat_id
    user_id = update.effective_user.id
    message_id = update.message.message_id
    user_message_content = update.message.text
    chat_type = update.effective_chat.type
    if chat_type == "private":
        update.message.reply_text("此命令只有在群组中有效")
        return
    if not utils.is_admin_in_this_group(update, user_id, chat_id):
        utils.send_message(chat_id, "非管理员，无权操作")
        return
    rst = re.search(r"\/add_url\n(https?:\/\/.*)", user_message_content)
    if rst is None:
        utils.bot.send_message(
            chat_id=user_id,
            text="指令错误，正确示例：\n/add_url\n白名单URL",
        )
        return
    url = rst.group(1)
    conn = redis_utils.get_connection()
    group_white_url_set = conn.smembers("whiteUrlSet:{}".format(chat_id))
    if group_white_url_set is not None and url in group_white_url_set:
        utils.bot.send_message(
            chat_id=user_id,
            text="此白名单URL已存在\n您输入的URL为：\n{}\n".format(url),
        )
        return
    # print(group_keyword_set)
    conn = redis_utils.get_connection()
    conn.sadd("whiteUrlSet:{}".format(chat_id), str(url))
    utils.bot.send_message(
        chat_id=user_id,
        text="添加成功\nURL：\n{}".format(url),
    )


def remove_url(update, context):
    # print("remove_reply_key")
    chat_id = update.effective_message.chat_id
    user_id = update.effective_user.id
    message_id = update.message.message_id
    user_message_content = update.message.text
    chat_type = update.effective_chat.type
    if chat_type == "private":
        update.message.reply_text("此命令只有在群组中有效")
        return
    if not utils.is_admin_in_this_group(update, user_id, chat_id):
        utils.send_message(chat_id, "非管理员，无权操作")
        return
    rst = re.search(r"\/remove_url\n(https?:\/\/.*)", user_message_content)
    if rst is None:
        utils.bot.send_message(
            chat_id=user_id,
            text="指令错误，正确示例：\n/remove_url\n需要删除的URL",
        )
        return
    url = rst.group(1)
    conn = redis_utils.get_connection()
    group_white_url_set = conn.smembers("whiteUrlSet:{}".format(chat_id))
    if group_white_url_set is None:
        utils.bot.send_message(
            chat_id=user_id,
            text="白名单中不存在此URL\n您输入的URL：\n{}".format(url),
        )
    # print(group_keyword_set)
    if url in group_white_url_set:
        conn.srem("whiteUrlSet:{}".format(chat_id), str(url))
        utils.bot.send_message(
            chat_id=user_id,
            text="删除成功\nURL：\n{}".format(url),
        )
    else:
        utils.bot.send_message(
            chat_id=user_id,
            text="白名单中不存在此URL\n您输入的URL为：\n{}".format(url),
        )


url_add_handler = CommandHandler('add_url', add_url)
url_remove_handler = CommandHandler('remove_url', remove_url)
