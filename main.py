from telegram.ext import InlineQueryHandler
from telegram.ext import Updater, CommandHandler
from telegram import InlineQueryResultArticle, InputTextMessageContent
import logging
import config

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

updater = Updater(token=config.TOKEN, use_context=True)
dispatcher = updater.dispatcher


def start(update, context):
    context.bot.send_message(
        chat_id=update.effective_chat.id, text="I'm a bot. Please talk to me")


def caps(update, context):
    text_caps = ' '.join(context.args).upper()
    context.bot.send_message(chat_id=update.effective_chat.id, text=text_caps)


def inline_caps(update, context):
    query = update.inline_query.query
    if not query:
        return
    results = list()
    results.append(
        InlineQueryResultArticle(
            id=query.upper(),
            title='Caps',
            input_message_content=InputTextMessageContent(query.upper())
        )
    )
    context.bot.answer_inline_query(update.inline_query.id, results)


inline_caps_handler = InlineQueryHandler(inline_caps)
dispatcher.add_handler(inline_caps_handler)

start_handler = CommandHandler('start', start)
cap_handler = CommandHandler('caps', caps)

dispatcher.add_handler(start_handler)
dispatcher.add_handler(cap_handler)


updater.start_polling()
