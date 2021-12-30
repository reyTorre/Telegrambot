""""
Project: Log in Program for Telegram Bot
Developed by Rey lawrence Torrecampo
Version History:
1.0 on 12/25/2021
1.1 on 12/30/2021 - added log out and
Associated python files:
    1) Costants.py              --> Contains Bot Key and SMS Authentication
    2) mysql_connection_db.py   --> MySQL Class for easier connection
    3) db_connection_details.py --> defines MySQl Connection Details
    4) responses.py             --> Contains non-command responses

This file contains the full program and sqeuences for login, logout and help.
"""

#  ------------------ Libraries ------------------------------
import constants as keys
import responses as r
from telegram.ext import *
import telegram as t
import db_connection_details as dbd
from twilio.rest import Client
import random
import telebot

bot = telebot.TeleBot(keys.API_KEY)
chat_id = keys.chat_id

#  ------------------ Variables ------------------------------
OTP_generated = 000000
login_status = 'N'
phone = '+630000000000'

#  ------------------ Non-program Specific Functions ------------------------------
# Generate six digit OTP
def generate_otp():
    global OTP_generated
    OTP_generated = random.randint(100000, 999999)
    return OTP_generated

# Generates log in status, A for active and I for Inactive
def check_log_in_status():
    phone_ph_converted = dbd.convert_to_ph_mobile(phone)
    login_status = dbd.do_check_status(phone_ph_converted)
    if (login_status == 'Y'):
        return 'A'
    else:
        return 'I'

# Sends OTP to user; +63 + 10-digit number as input
def send_otp (phone_num):
    account_sid = keys.twilio_accnt_num
    auth_token = keys.twilio_auth_token
    client = Client(account_sid, auth_token)
    otp = generate_otp()
    message = client.messages \
        .create(
        body='Your OTP is - ' + str(otp),
        from_= keys.twilio_phone_num,
        to= phone_num
    )
    print("Message ID" + message.sid, " OTP" + str(otp))
    phone_num_ph = dbd.convert_to_ph_mobile(phone_num)
    dbd.do_update_otp(phone_num_ph,str(otp))

# ---------- defining states ---------
ONE , TWO = range(2)

#  ------------------ Program Specific Functions ------------------------------
# /Start Command to start log in sequence
def start_command (update, context):
    bot.send_message(chat_id,'Welcome to Telegrambot.\nTo start, you will need to share your contact information.') #introdductory Message
    user = update.message.from_user #
    print('You talk with user{} and his user ID:{} '.format(user['username'], user['id']))
    contact_keyboard = t.KeyboardButton('Share contact', request_contact=True) # creating contact button object
    custom_keyboard = [[contact_keyboard]]  # creating keyboard object
    reply_markup = t.ReplyKeyboardMarkup(custom_keyboard, one_time_keyboard=True) #show keyboard
    update.message.reply_text("Would you mind sharing your contact with me?", reply_markup=reply_markup) # prompt Sharing of Contact
    return ONE

# Callback to get Contact; Automatically gets the Phone Number when Contact is shared
def contact_callback(update, context):
    global phone
    contact = update.message.contact #Get contact information
    phone = contact.phone_number #get phone number
    update.message.reply_text('Sent an OTP to your end. Kindly check if you receive it. \nOnce received, input the OTP in the Chat.') #reply with message
    send_otp(phone) #send OTP to Phone
    return TWO

# Start of login sequence once correct OTP is sent
def login_sequence(update, context):
    _otp_input = update.message.text
    phone_ph_converted = dbd.convert_to_ph_mobile(phone) # change +63 to 0
    if (dbd.check_otp_phone_num_in_db(phone_ph_converted,_otp_input) == 'FND'): # search db if Number and OTP matches, if yes then log in is successful
        dbd.do_db_log_in(dbd.convert_to_ph_mobile(phone))
        print('Log in Successful')
        update.message.reply_text('Log in Successful')
    else: #if not log in fails
        print('Log in Failed')
        update.message.reply_text('Log in Failed. Kindly Input Correct OTP!')
        return TWO # If incorrect OTP, returns to OTP Start sequence.
    check_log_in_status() #converts return of status: Y --> A and N --> I
    return ConversationHandler.END

# Non-command handler
def handle_message(update,context):
    global phone
    phone_ph_converted = dbd.convert_to_ph_mobile(phone)  # change +63 to 0
    if (check_log_in_status() == 'A'): #Check if Active
        if (r.check_for_time_out(phone_ph_converted)): # Check Time Out
            text = str(update.message.text).lower()
            response = r.sample_responses(text)
            update.message.reply_text(response)
        else:
            update.message.reply_text('Unable to Proceed due to time out. Logging out of Telegram Bot')
            dbd.do_db_log_out(dbd.convert_to_ph_mobile(phone))
    else:
        update.message.reply_text('Kindly Log in by inputting /start')

# Cancel Log in Process
def cancel(update, context): #Cancels current log in process
    chat_id = update.message.chat_id
    bot.send_message(chat_id, text="Log in Process Canceled.\nKindly input /start to trigger login sequence!")
    return ConversationHandler.END

# User log out
def logout_sequence(update, context): # Log out Process; triggered by /end
    if (check_log_in_status() == 'A'):
        dbd.do_db_log_out(dbd.convert_to_ph_mobile(phone))
        update.message.reply_text('Logout Successful')
    else:
        update.message.reply_text('Unable to Log Out. Kindly Log in by inputting /start')

# Help Command
def help_command (update, context):  # help menu; triggered by /help
    global phone
    phone_ph_converted = dbd.convert_to_ph_mobile(phone)  # change +63 to 0
    if (check_log_in_status() == 'A'):
        if (r.check_for_time_out(phone_ph_converted)):
            update.message.reply_text('If you need help, google it!')
        else:
            update.message.reply_text('Unable to Proceed due to time out. Logging out of Telegram Bot')
            dbd.do_db_log_out(dbd.convert_to_ph_mobile(phone))
    else:
        update.message.reply_text('Kindly Log in by inputting /start')

# Error Handler
def error(update, context): # displays error in console
    print(f"Update {update} caused error {context.error}")

def main():
    updater = Updater(keys.API_KEY, use_context=True)
    dp = updater.dispatcher
    ch1 = ConversationHandler (entry_points= [CommandHandler("start", start_command)],states={ONE: [MessageHandler(Filters.contact, contact_callback)], TWO: [MessageHandler(Filters.text, login_sequence)]},fallbacks=[MessageHandler(Filters.regex('cancel'), cancel)], allow_reentry = True)
    updater.dispatcher.add_handler(ch1) # input /start to trigger message sequence
    dp.add_handler(CommandHandler("help", help_command)) # input /help to prompt help commands
    dp.add_handler(CommandHandler("end", logout_sequence)) # input /end to trigger log out sequence
    dp.add_handler(MessageHandler(Filters.contact, contact_callback)) # gets contact message
    dp.add_handler(MessageHandler(Filters.text,handle_message)) # gets contact message
    dp.add_error_handler(error)

    updater.start_polling(15)

    updater.idle()

# ----------------------- Main Program --------------------------------------
if __name__ == '__main__':
    print("Bot started ....")
    main()