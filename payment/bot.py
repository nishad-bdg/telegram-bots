import config
from telegram import *
from telegram.ext import *



def start(update,context):
    message = 'Reply to this message with lists of card to cashout, in a line by line format. \n\n'
    message += 'Card:mm:yy:cvv:$$$ Example \n\n'
    message += '4097580505747185:04:20:402:$16.00'
    update.message.reply_text(message)


def main() -> None:
    bot = Bot(config.TOKEN)

    updater = Updater(token = config.TOKEN, use_context = True)
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler('start',start))

    updater.start_polling()
    updater.idle() 


if __name__ == '__main__':
    main()