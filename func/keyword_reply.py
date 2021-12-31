import re

from telegram import Chat, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Filters, MessageHandler, CommandHandler

import config
import redis_utils
import utils


def keyword_reply_handler(update, context):
    print("enter keyword_reply_handler")
    chat_id = update.effective_message.chat_id
    message_id = update.message.message_id
    user_message_content = update.message.text
    # print(chat_id, user_message_content)
    conn = redis_utils.get_connection()
    group_keyword_set = conn.smembers("keywordReplySet:{}".format(chat_id))
    if group_keyword_set is None:
        return
    # print(group_keyword_set)
    for i in group_keyword_set:
        if str(i) in user_message_content:
            reply_content = redis_utils.get_key("keywordReplyContent:{}:{}".format(chat_id, str(i)))
            if reply_content is not None:
                # print(reply_content)
                utils.bot.send_message(
                    chat_id=chat_id,
                    text=reply_content,
                    reply_to_message_id=message_id
                )


def add_reply_key(update, context):
    # print("add_reply_key")
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
    rst = re.search(
        r"\/add_reply_keyword\n---\n([\w|\\|\s|\d| |，|。|\！|\@|\#|\¥|\%|\:|\/|\.]*?)\n---\n([\w|\d||\\|\n|\s| |，|。|\！|\@|\#|\¥|\%|\/|\.|\:|\-]*)",
        user_message_content)
    if rst is None:
        utils.bot.send_message(
            chat_id=user_id,
            text="指令错误，正确示例：\n/add_reply_keyword\n---\n关键词\n---\n回复内容",
        )
        return
    keyword = rst.group(1)
    answer = rst.group(2)
    conn = redis_utils.get_connection()
    group_keyword_set = conn.smembers("keywordReplySet:{}".format(chat_id))
    if group_keyword_set is not None and keyword in group_keyword_set:
        utils.bot.send_message(
            chat_id=user_id,
            text="此关键词已存在\n您输入的关键词为：{}\n回复内容已经更新为：\n{}".format(keyword, answer),
        )
        redis_utils.set_key_value("keywordReplyContent:{}:{}".format(chat_id, str(keyword)), str(answer))
        return
    # print(group_keyword_set)
    conn = redis_utils.get_connection()
    conn.sadd("keywordReplySet:{}".format(chat_id), str(keyword))
    redis_utils.set_key_value("keywordReplyContent:{}:{}".format(chat_id, str(keyword)), str(answer))
    utils.bot.send_message(
        chat_id=user_id,
        text="添加成功\n关键词：{}\n回复：\n{}".format(keyword, answer),
    )


def remove_reply_key(update, context):
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
    rst = re.search(r"\/remove_reply_keyword\n([\w|\s|\\]*)", user_message_content)
    if rst is None:
        utils.bot.send_message(
            chat_id=user_id,
            text="指令错误，正确示例：\n/remove_reply_keyword\n关键词",
        )
        return
    keyword = rst.group(1)
    conn = redis_utils.get_connection()
    group_keyword_set = conn.smembers("keywordReplySet:{}".format(chat_id))
    if group_keyword_set is None:
        utils.bot.send_message(
            chat_id=user_id,
            text="不存在此关键词\n您输入的关键词为：{}".format(keyword),
        )
    # print(group_keyword_set)
    if keyword in group_keyword_set:
        conn.srem("keywordReplySet:{}".format(chat_id), str(keyword))
        conn.delete("keywordReplyContent:{}:{}".format(chat_id, str(keyword)))
        utils.bot.send_message(
            chat_id=user_id,
            text="删除成功\n关键词：{}".format(keyword),
        )
    else:
        utils.bot.send_message(
            chat_id=user_id,
            text="不存在此关键词\n您输入的关键词为：{}".format(keyword),
        )


reply_key_add_handler = CommandHandler('add_reply_keyword', add_reply_key)
reply_key_remove_handler = CommandHandler('remove_reply_keyword', remove_reply_key)
