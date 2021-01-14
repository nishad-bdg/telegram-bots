import config
import wikipedia
import requests
from telegram import *
from telegram.ext import *


bot = Bot(config.TOKEN)

updater = Updater(token=config.TOKEN, use_context=True)

dispatcher = updater.dispatcher

keyword = ''
chat_id = ''


def test1(update, context):
    bot.send_message(
        chat_id=update.effective_chat.id,
        text='working',
        parse_mode=ParseMode.HTML
    )

def start(update,context):
    show_keyboard(update,context)

def show_keyboard(update, context):
    global keyword, chat_id

    keyword = update.message.text
    chat_id = update.message.chat_id

    keyboard = [[
        InlineKeyboardButton('ABOUT', callback_data='ABOUT'),
        InlineKeyboardButton('IMAGE', callback_data='IMAGE')
    ]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text('Please choose:', reply_markup=reply_markup)


def button_click(update, context):
    global keyword, chat_id
    query = update.callback_query

    if query.data == "ABOUT":
        summary = wikipedia.summary(keyword)
        bot.send_message(
            chat_id=update.effective_chat.id,
            text=summary,
            parse_mode=ParseMode.HTML
        )

    if query.data == "IMAGE":
        headers = {
            "apikey": "87cce380-5671-11eb-aa89-0d67d0cb24a0"}


        params = (
            ("q", keyword),
            ("tbm", "isch"),
        )

        response = requests.get(
            'https://app.zenserp.com/api/v2/search', headers=headers, params=params)

        data = response.json()

        first_image = data['image_results'][0]['thumbnail']

        bot.send_photo(chat_id = chat_id,photo = first_image, )


# dispatcher.add_handler(CommandHandler('start',start))
dispatcher.add_handler(MessageHandler(Filters.text, show_keyboard))
dispatcher.add_handler(CallbackQueryHandler(button_click))

updater.start_polling()
