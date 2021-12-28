from telegram.ext import CommandHandler


def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Welcome!", parse_mode='Markdown')


start_handler = CommandHandler('start', start)
