from telegram.ext import Filters, MessageHandler


def new_member(update, context):
    try:
        id = update.message.new_chat_members[0].id
        print(id)
        message_id = update.message.message_id
        print("message_id: {}".format(message_id))
        first_name, last_name = "", ""
        first_name = str(update.message.new_chat_members[0].first_name)
        last_name = str(update.message.new_chat_members[0].last_name)
        print("User Name: {} {}".format(first_name, last_name))
    except Exception as e:
        print(e)


get_new_member = MessageHandler(Filters.status_update.new_chat_members, new_member)
