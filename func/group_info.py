from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CommandHandler

import config
import redis_utils
import utils


def info_exec(update, context):
    print("enter info_exec")

    chat_id = update.effective_message.chat_id
    message_id = update.message.message_id
    user_id = update.effective_user.id
    if not utils.is_admin_in_this_group(update, user_id, chat_id):
        utils.send_message(chat_id, "非管理员，无权操作")
        return
    user = update.message.from_user
    username = user['username']
    firstname = user['first_name']
    lastname = user['last_name']
    user_message_content = update.message.text
    conn = redis_utils.get_connection()
    # 更新群组活跃用户Set
    conn.sadd("activeUserSet:{}".format(chat_id), user_id)
    # 更新用户元数据
    user_info = {
        "user_id": str(user_id),
        "username": str(username),
        "firstname": str(firstname),
        "lastname": str(lastname)
    }
    conn.hmset("userInfo:{}".format(user_id), user_info)
    # 更新群组消息内容
    if "/" in user_message_content:
        # print("这是一条指令信息，跳过")
        return
    else:
        if user_message_content[-1] not in ["，", "。", "！", "：", "？", "!", "?", ",", ":", "."]:
            conn.append("groupMessageContent:{}".format(chat_id), user_message_content + "。")
        else:
            conn.append("groupMessageContent:{}".format(chat_id), user_message_content)
    # 更新群组消息数量
    conn.incrby("groupMessageAmount:{}".format(chat_id))
    # 更新用户消息数量
    conn.incrby("userMessageAmount:{}:{}".format(chat_id, user_id))


def group_info_command(update, context):
    chat_id = update.effective_message.chat_id
    conn = redis_utils.get_connection()
    group_active_user_amount = conn.scard("activeUserSet:{}".format(chat_id))
    new_member_amount = conn.get("newMemberAmount:{}".format(chat_id))
    if new_member_amount is None:
        new_member_amount = 0
    group_message_amount = conn.get("groupMessageAmount:{}".format(chat_id))
    if group_message_amount is None:
        group_message_amount = 0
    print("group_active_user_amount: {}".format(group_active_user_amount))
    print("new_member_amount: {}".format(new_member_amount))
    print("group_message_amount: {}".format(group_message_amount))
    active_user_set = conn.smembers("activeUserSet:{}".format(chat_id))
    active_user_message_amount_list = []
    for user in active_user_set:
        user_message_amount = conn.get("userMessageAmount:{}:{}".format(chat_id, user))
        active_user_message_amount_list.append([user, int(user_message_amount)])
    # print(active_user_message_amount_list)
    most_activate_user_msg = ""
    if len(active_user_message_amount_list) > 0:
        sorted_list = sorted(active_user_message_amount_list, key=lambda user_info: user_info[1], reverse=True)
        # print(sorted_list)
        most_activate_user = sorted_list[0]
        user_meta_info = conn.hmget("userInfo:{}".format(most_activate_user[0]),
                                    ["user_id", "username", "firstname", "lastname"])
        print(user_meta_info)
        firstname = user_meta_info[2]
        lastname = user_meta_info[3]
        name = ""
        if firstname is not None:
            name = name + firstname + " "
        if lastname is not None:
            name = name + lastname
        most_activate_user_msg = "最活跃用户：[@{}](tg://user?id={})，发言数量 {}".format(
            name, most_activate_user[0], most_activate_user[1])
    msg = "群组当日信息一览：\n" \
          "活跃人数：{}\n" \
          "入群人数：{}\n" \
          "消息总数：{}\n{}".format(
        group_active_user_amount, new_member_amount, group_message_amount, most_activate_user_msg
    )

    utils.bot.send_message(
        chat_id=chat_id,
        text=msg,
        parse_mode="Markdown"
    )


group_info_command_handler = CommandHandler('info', group_info_command)
