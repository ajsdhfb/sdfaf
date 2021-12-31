import re

import jieba as jieba
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CommandHandler
import jieba.posseg as pseg

import config
import redis_utils
import utils


def topic(update, context):
    print("enter topic")
    chat_id = update.effective_message.chat_id
    message_id = update.message.message_id
    user_id = update.effective_user.id
    chat_type = update.effective_chat.type
    if chat_type == "private":
        update.message.reply_text("此命令只有在群组中有效")
        return
    if not utils.is_admin_in_this_group(update, user_id, chat_id):
        utils.send_message(chat_id, "非管理员，无权操作")
        return
    conn = redis_utils.get_connection()
    chat_content = conn.get("groupMessageContent:{}".format(chat_id))
    # print(chat_content)

    jieba.enable_paddle()  # 启动paddle模式。 0.40版之后开始支持，早期版本不支持

    word_list = []
    words = pseg.cut(chat_content, use_paddle=True)  # paddle模式
    for word, flag in words:
        # print(word + "\t" + flag)
        if flag in ["n", "nr", "nz", "PER", "f", "ns", "LOC", "s", "nt", "ORG", "nw"]:
            # 判断该词是否有效，不为空格
            if re.match(r"^\s+?$", word) is None and len(word) > 2:
                word_list.append(word)
        # print(word_list)
    hot_word_string = ""
    if len(word_list) > 0:
        # 分析高频词
        word_amount = {}
        # print(word_amount)
        for word in word_list:
            if re.search(
                    r"[。|，|、|？|！|,|.|!|?|\\|/|+|\-|`|~|·|@|#|￥|$|%|^|&|*|(|)|;|；|‘|’|“|”|'|_|=|•|·|…|\"]",
                    word) is not None:
                continue
            # 判断该词是否之前已经出现
            if word_amount.get(word) is not None:
                word_amount[word] = word_amount.get(word) + 1
            else:
                word_amount[word] = 1
        word_amount = sorted(word_amount.items(), key=lambda kv: (int(kv[1])), reverse=True)
        # print(word_amount)
        if len(word_amount) > 0:
            # print("排序后的热词：" + str(word_amount))
            hot_word_string = ""
            for i in range(min(config.DISPLAY_KEYWORD_AMOUNT, len(word_amount))):
                hot_word_string += "`" + str(word_amount[i][0]) + "`" + ": " + str(word_amount[i][1]) + "\n"
            # print(hot_word_string)
    # print(hot_word_string)
    msg = "群组今日Top {}关键词为：\n\n".format(config.DISPLAY_KEYWORD_AMOUNT) + hot_word_string
    utils.bot.send_message(
        chat_id=user_id,
        text=msg,
        parse_mode="Markdown"
    )


topic_command_handler = CommandHandler('topic', topic)
