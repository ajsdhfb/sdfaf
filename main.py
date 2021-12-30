import threading

from telegram.ext import Updater
from config import TOKEN
from func import start_command, new_member_welcome_message, test_command, message_dispatcher, keyword_reply, \
    ad_delete, group_info, topic_command, task
import schedule

from func.task import clean_db_task

threading.Thread(target=task.schedule_task).start()

# 每天四点定时清理前日的统计数据，该任务不会清理违禁词和关键词回复数据
schedule.every().day.at('04:00').do(clean_db_task)

updater = Updater(token=TOKEN, use_context=True, request_kwargs={
    'proxy_url': 'socks5://127.0.0.1:7890/'
})

dispatcher = updater.dispatcher

dispatcher.add_handler(start_command.start_handler)
dispatcher.add_handler(test_command.test_handler)
dispatcher.add_handler(keyword_reply.reply_key_add_handler)
dispatcher.add_handler(keyword_reply.reply_key_remove_handler)
dispatcher.add_handler(ad_delete.ad_key_add_handler)
dispatcher.add_handler(ad_delete.ad_key_remove_handler)
dispatcher.add_handler(group_info.group_info_command_handler)
dispatcher.add_handler(topic_command.topic_command_handler)
dispatcher.add_handler(new_member_welcome_message.send_pinned_message_handler)
dispatcher.add_handler(message_dispatcher.message_dispatcher_handler)

updater.start_polling()
