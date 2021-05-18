""" Data input for bot """

BOT_TOKEN = '1790423596:AAFbieU3yo2xwHEjwLosI_WWVEpAtR-nrKI'
PROVIDER_TOKEN ='284685063:TEST:NTcxMWZlZDJkMGUw'
CURRENCY = 'USD'
INVOICE_TITLE = "MerchantPay"
INVOICE_DESCRIPTION = "Use this invoice to make payment"
START_MESSAGE = "Use /createinvoice to create an invoice. \nUse /help to read info."
CREATE_INVOICE_MESSAGE = f"Please enter an amount (in {CURRENCY}).\n (Limit is $10,000.\n Decimal places greater than 2 will be rounded up)."
AMOUNT_INVALID_MESSAGE = "Please enter a valid amount."
AMOUNT_TOO_BIG_MESSAGE = "Amount exceeds limit.\nEnter a valid amount."
CANCEL_MESSAGE = "cancelled operation"
UNKNOWN_COMMAND_MESSAGE = "Sorry, I didn't understand that command."
HELP_MESSAGE = "There is no help here.\nTry /createinvoice ."