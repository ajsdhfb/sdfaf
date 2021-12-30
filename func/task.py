import time

import redis_utils
import schedule


def clean_db_task():
    conn = redis_utils.get_connection()

    need_clean_prefix = ["groupMessageAmount:*", "userMessageAmount:*", "activeUserSet:*", "groupMessageContent:*"]
    for i in need_clean_prefix:
        for key in conn.scan_iter(i):
            conn.delete(key)


def schedule_task():
    while True:
        schedule.run_pending()
        time.sleep(1)

# clean_task()
