import setup
from telegram import (LabeledPrice, Update,)
from telegram.ext import (Updater, CommandHandler,
                         MessageHandler, Filters, 
                         PreCheckoutQueryHandler, 
                         CallbackContext,
                         ConversationHandler)
import logging

TOKEN = setup.BOT_TOKEN

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)
logger = logging.getLogger(__name__)

def start_callback(update: Update, _: CallbackContext) -> None:
    msg = (setup.START_MESSAGE)
    update.message.reply_text(msg)
    print(f'Start command pressed::User == {update.effective_user.first_name}.')

def start_invoice_callback(update: Update, context: CallbackContext) -> int:
    price = update.message.text
    chat_id = update.message.chat_id
    title = setup.INVOICE_TITLE
    description = setup.INVOICE_DESCRIPTION
    payload = "Custom-Payload"
    provider_token = setup.PROVIDER_TOKEN
    currency = setup.CURRENCY
    try:
        float(price)
    except ValueError:
        update.message.reply_text(setup.AMOUNT_INVALID_MESSAGE)
        print(f'ValueError exception raised (invalid amount)::User == {update.effective_user.first_name}.\nRetrying...')
        return 1
    if float(price) > 10000.00:
        update.message.reply_text(setup.AMOUNT_TOO_BIG_MESSAGE)
        print(f'Exception raised (Amount too big)::User == {update.effective_user.first_name}.\nRetrying...')
        return 1
    prices = [LabeledPrice("Test", int(round(float(price),2) * 100))]

    context.bot.send_invoice(
        chat_id, title, description, payload, provider_token, currency, prices
    )
    print(f'Invoice generated successfully::User == {update.effective_user.first_name}.')
    return ConversationHandler.END
def precheckout_callback(update: Update, _: CallbackContext) -> None:
    query = update.pre_checkout_query
    # check the payload, is this from your bot?
    if query.invoice_payload != 'Custom-Payload':
        query.answer(ok=False, error_message="Something went wrong...")
    else:
        query.answer(ok=True)

def successful_payment_callback(update: Update, _: CallbackContext) -> None:
    update.message.reply_text("Thank you for your payment!")
    print(f'Successful payment::User == {update.effective_user.first_name}.')

def unknown(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text=setup.UNKNOWN_COMMAND_MESSAGE)
    print(f'Unknown command::User == {update.effective_user.first_name}.')

def request_price(update: Update, context: CallbackContext) -> None:
    msg = (setup.CREATE_INVOICE_MESSAGE)
    update.message.reply_text(msg)
    print(f'CreateInvoice command initiated::User == {update.effective_user.first_name}.')
    return 1

def help(update: Update, _: CallbackContext) -> None:
    update.message.reply_text(setup.HELP_MESSAGE)
    print(f'Help command initiated::User == {update.effective_user.first_name}.')

def cancel(update: Update, _: CallbackContext) -> int:
    user = update.message.from_user
    msg = setup.CANCEL_MESSAGE
    update.message.reply_text(msg)
    print(f'Operation cancelled::User == {update.effective_user.first_name}.')
    return ConversationHandler.END

def main() -> None:
    updater = Updater(TOKEN)
    dispatcher = updater.dispatcher

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('createInvoice', request_price)],
        states={1:[MessageHandler(Filters.text & (~Filters.command), start_invoice_callback)]},
        fallbacks=[CommandHandler('cancel', cancel)],
     )

    dispatcher.add_handler(CommandHandler("start", start_callback))
    dispatcher.add_handler(CommandHandler("help", help))
    dispatcher.add_handler(PreCheckoutQueryHandler(precheckout_callback))
    dispatcher.add_handler(MessageHandler(Filters.successful_payment, successful_payment_callback))
    dispatcher.add_handler(conv_handler)
    dispatcher.add_handler(MessageHandler(Filters.command, unknown))
    
    updater.start_polling()
    #updater.idle()

if __name__ == '__main__':
    main()