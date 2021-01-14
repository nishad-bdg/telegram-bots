import config
import logging
import time
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    ConversationHandler,
    CallbackContext,
)

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)

CASHOUT = 0


def start(update, context) -> int:
    message = 'Reply to this message with lists of card to cashout, in a line by line format. \n\n'
    message += 'Card:mm:yy:cvv:$$$ Example \n\n'
    message += '4097580505747185:04:20:402:$16.00'
    update.message.reply_text(message)

    return CASHOUT


def cashout(update, context):
    user = update.message.from_user
    text = update.message.text
    if ":" in text:
        result = text.split(":")
        card = ' '.join(result).replace(" ","")
        message = f"{card}\n\n"
        message += f"Started cashing out {result[-1]} worth of cards"
        update.message.reply_text(message)
        time.sleep(3)
        update.message.reply_text(f"Cashing out for {result[-1]}")
        time.sleep(3)
        update.message.reply_text(f"Cash out completed for {result[-1]}")
        update.message.reply_text(f"Process completed")

        return ConversationHandler.END
    else:
        update.message.reply_text("Invalid card format")
    


def cancel(update, context):
    user = update.message.from_user
    logger.info("User %s canceled the conversation.", user.first_name)
    update.message.reply_text(
        'Bye! I hope we can talk again some day.', reply_markup=ReplyKeyboardRemove()
    )
    return ConversationHandler.END


def main() -> None:
    updater = Updater(token=config.TOKEN2, use_context=True)

    dispatcher = updater.dispatcher

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            CASHOUT: [MessageHandler(Filters.text, cashout)]
        },
        fallbacks=[CommandHandler('cancel', cancel)]
    )

    dispatcher.add_handler(conv_handler)

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
