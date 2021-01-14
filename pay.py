import logging
import config
from telegram import LabeledPrice, ShippingOption, Update
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    PreCheckoutQueryHandler,
    ShippingQueryHandler,
    CallbackContext,
)

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)


def start(update, context):
    msg = "Use /pay to get an card"
    update.message.reply_text(msg)


def pay(update, context):
    chat_id = update.message.chat_id
    title = "Payment Example"
    description = "Payment example"
    payload = "Custom-Payload"
    provider_token = config.PROVIDER_TOKEN
    start_parameter = "test-payment"
    currency = "USD"
    price = 1
    prices = [LabeledPrice("Test", price * 100)]

    context.bot.send_invoice(
        chat_id,
        title,
        description,
        payload,
        provider_token,
        start_parameter,
        currency,
        prices,
        need_name=True,
        need_phone_number=True,
        need_email=True,
        need_shipping_address=True,
        is_flexible=True,
    )


def shipping_callback(update, context):
    query = update.shipping_query
    # check the payload, is this from your bot?
    if query.invoice_payload != 'Custom-Payload':
        # answer False pre_checkout_query
        query.answer(ok=False, error_message="Something went wrong...")
        return

    options = list()
    # a single LabeledPrice
    options.append(ShippingOption(
        '1', 'Shipping Option A', [LabeledPrice('A', 100)]))
    # an array of LabeledPrice objects
    price_list = [LabeledPrice('B1', 150), LabeledPrice('B2', 200)]
    options.append(ShippingOption('2', 'Shipping Option B', price_list))
    query.answer(ok=True, shipping_options=options)


# after (optional) shipping, it's the pre-checkout
def precheckout_callback(update: Update, context: CallbackContext) -> None:
    query = update.pre_checkout_query
    # check the payload, is this from your bot?
    if query.invoice_payload != 'Custom-Payload':
        # answer False pre_checkout_query
        query.answer(ok=False, error_message="Something went wrong...")
    else:
        query.answer(ok=True)


# finally, after contacting the payment provider...
def successful_payment_callback(update: Update, context: CallbackContext) -> None:
    # do something after successfully receiving payment?
    update.message.reply_text("Thank you for your payment!")


def main():
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater(config.TOKEN, use_context=True)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # simple start function
    dispatcher.add_handler(CommandHandler("start", start))

    # Add command handler to start the payment invoice
    dispatcher.add_handler(CommandHandler("shipping", pay))
    

    # Optional handler if your product requires shipping
    dispatcher.add_handler(ShippingQueryHandler(shipping_callback))

    # Pre-checkout handler to final check
    dispatcher.add_handler(PreCheckoutQueryHandler(precheckout_callback))

    # Success! Notify your user!
    dispatcher.add_handler(MessageHandler(Filters.successful_payment, successful_payment_callback))

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == "__main__":
    main()