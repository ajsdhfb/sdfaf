from telegram.ext import Filters, MessageHandler
import utils


def new_member(update, context):
    try:
        chat_id = update.effective_message.chat_id
        new_user_id = update.message.new_chat_members[0].id
        print(id)
        message_id = update.message.message_id
        print("new_user_id: {} | message_id: {}".format(new_user_id, message_id))
        first_name, last_name = "", ""
        first_name = str(update.message.new_chat_members[0].first_name)
        last_name = str(update.message.new_chat_members[0].last_name)
        print("User Name: {} {}".format(first_name, last_name))
        chat = utils.get_chat(chat_id)
        print(chat)
        print(type(chat))
    except Exception as e:
        print(e)


send_pinned_message_handler = MessageHandler(Filters.status_update.new_chat_members, new_member)
