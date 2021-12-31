import threading

from telegram.ext import Updater
from config import TOKEN
from func import new_member, message_dispatcher, keyword_reply, \
    ad_delete, group_info, topic_command, task, get_list, url_white_list
import schedule

from func.task import clean_db_task

threading.Thread(target=task.schedule_task).start()

# 每天四点定时清理前日的统计数据，该任务不会清理违禁词和关键词回复数据
schedule.every().day.at('04:00').do(clean_db_task)

updater = Updater(token=TOKEN, use_context=True)

# 启用 Socks5 代理
# updater = Updater(token=TOKEN, use_context=True, request_kwargs={
#     'proxy_url': 'socks5://127.0.0.1:7890/'
# })

dispatcher = updater.dispatcher

dispatcher.add_handler(keyword_reply.reply_key_add_handler)
dispatcher.add_handler(keyword_reply.reply_key_remove_handler)
dispatcher.add_handler(ad_delete.ad_key_add_handler)
dispatcher.add_handler(ad_delete.ad_key_remove_handler)
dispatcher.add_handler(url_white_list.url_add_handler)
dispatcher.add_handler(url_white_list.url_remove_handler)
dispatcher.add_handler(group_info.group_info_command_handler)
dispatcher.add_handler(topic_command.topic_command_handler)
dispatcher.add_handler(get_list.get_ad_list_handler)
dispatcher.add_handler(get_list.get_keyword_list_handler)
dispatcher.add_handler(get_list.get_white_url_list_handler)
dispatcher.add_handler(new_member.send_pinned_message_handler)
dispatcher.add_handler(message_dispatcher.message_dispatcher_handler)

updater.start_polling()
