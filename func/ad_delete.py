import re

from telegram import Chat, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Filters, MessageHandler, CommandHandler

import config
import redis_utils
import utils


def ad_delete_handler(update, context):
    print("enter ad_delete_handler")
    flag = False
    chat_id = update.effective_message.chat_id
    message_id = update.message.message_id
    user_id = update.effective_user.id
    user = update.message.from_user
    username = user['username']
    firstname = user['first_name']
    lastname = user['last_name']
    name = ""
    if utils.is_admin_in_this_group(update, user_id, chat_id):
        return flag
    if username is not None:
        name = username
    else:
        if firstname is not None:
            name = name + firstname + " "
        if lastname is not None:
            name = name + lastname
    user_message_content = update.message.text
    # print(chat_id, user_message_content)
    conn = redis_utils.get_connection()
    group_keyword_set = conn.smembers("adKeywordSet:{}".format(chat_id))
    if group_keyword_set is None:
        return
    # print(group_keyword_set)
    for i in group_keyword_set:
        if str(i) in user_message_content:
            warn_count = redis_utils.get_key("adWarnCount:{}:{}".format(chat_id, user_id))
            if warn_count is None:
                redis_utils.set_key_value("adWarnCount:{}:{}".format(chat_id, user_id), 1)
                warn_count = 1
            else:
                warn_count = int(warn_count)
                warn_count += 1
            if warn_count <= config.AD_WARN_COUNT:
                utils.bot.send_message(
                    chat_id=chat_id,
                    text="[@{}](tg://user?id={})\n您发送的内容中含有违禁词：{}，已自动删除\n"
                         "警告次数：{}/{}\n"
                         "剩余警告次数：{}\n"
                         "⚠️超过将会被踢出本群组！⚠️".format(
                        name, user_id, str(i), warn_count, config.AD_WARN_COUNT, config.AD_WARN_COUNT - warn_count),
                    parse_mode="Markdown"
                )
                utils.bot.deleteMessage(chat_id=update.message.chat.id, message_id=update.message.message_id)
                redis_utils.set_key_value("adWarnCount:{}:{}".format(chat_id, user_id), warn_count)
            else:
                utils.bot.send_message(
                    chat_id=chat_id,
                    text="[@{}](tg://user?id={})\n您发送的内容中含有违禁词：{}，已自动删除\n"
                         "警告次数：{}\n"
                         "✈️飞机票送上".format(name, user_id, str(i), warn_count),
                    parse_mode="Markdown"
                )
                utils.bot.deleteMessage(chat_id=update.message.chat.id, message_id=update.message.message_id)
                utils.bot.ban_chat_member(chat_id=chat_id, user_id=user_id, revoke_messages=True)
                redis_utils.set_key_value("adWarnCount:{}:{}".format(chat_id, user_id), 0)
            flag = True
            break
    return flag


def add_ad_key(update, context):
    # print("add_reply_key")
    chat_id = update.effective_message.chat_id
    user_id = update.effective_user.id
    message_id = update.message.message_id
    user_message_content = update.message.text
    if not utils.is_admin_in_this_group(update, user_id, chat_id):
        utils.send_message(chat_id, "非管理员，无权操作")
        return
    rst = re.search(r"\/add_ad_keyword\n([\w|\b|\\|\n]*)", user_message_content)
    if rst is None:
        utils.bot.send_message(
            chat_id=chat_id,
            text="指令错误，正确示例：\n`/add_ad_keyword\n违禁词`",
            parse_mode="Markdown"
        )
        return
    keyword = rst.group(1)
    conn = redis_utils.get_connection()
    group_ad_keyword_set = conn.smembers("adKeywordSet:{}".format(chat_id))
    if group_ad_keyword_set is not None and keyword in group_ad_keyword_set:
        utils.bot.send_message(
            chat_id=chat_id,
            text="此违禁词已存在\n您输入的违禁词为：{}".format(keyword),
            parse_mode="Markdown"
        )
        return
    # print(group_keyword_set)
    conn.sadd("adKeywordSet:{}".format(chat_id), str(keyword))
    utils.bot.send_message(
        chat_id=chat_id,
        text="添加成功\n违禁词：{}".format(keyword),
        parse_mode="Markdown"
    )


def remove_ad_key(update, context):
    # print("remove_reply_key")
    chat_id = update.effective_message.chat_id
    user_id = update.effective_user.id
    message_id = update.message.message_id
    user_message_content = update.message.text
    if not utils.is_admin_in_this_group(update, user_id, chat_id):
        utils.send_message(chat_id, "非管理员，无权操作")
        return
    rst = re.search(r"\/remove_ad_keyword\n([\w|\b|\\|\n]*)", user_message_content)
    if rst is None:
        utils.bot.send_message(
            chat_id=chat_id,
            text="指令错误，正确示例：\n`/remove_ad_keyword\n需要移除的违禁词`",
            parse_mode="Markdown"
        )
        return
    keyword = rst.group(1)
    conn = redis_utils.get_connection()
    group_keyword_set = conn.smembers("adKeywordSet:{}".format(chat_id))
    if group_keyword_set is None:
        utils.bot.send_message(
            chat_id=chat_id,
            text="不存在此违禁词\n您输入的违禁词为：{}".format(keyword),
            parse_mode="Markdown"
        )
    # print(group_keyword_set)
    if keyword in group_keyword_set:
        conn.srem("adKeywordSet:{}".format(chat_id), str(keyword))
        utils.bot.send_message(
            chat_id=chat_id,
            text="删除成功\n违禁词：{}".format(keyword),
            parse_mode="Markdown"
        )
    else:
        utils.bot.send_message(
            chat_id=chat_id,
            text="不存在此违禁词\n您输入的违禁词为：{}".format(keyword),
            parse_mode="Markdown"
        )


ad_key_add_handler = CommandHandler('add_ad_keyword', add_ad_key)
ad_key_remove_handler = CommandHandler('remove_ad_keyword', remove_ad_key)
