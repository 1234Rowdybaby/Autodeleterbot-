import os
import time
from telegram import Bot, Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# Get the bot token from environment variable
BOT_TOKEN = os.getenv("BOT_TOKEN")
DELETE_DELAY = 1  # Set delete delay to 1 second

# Initialize the Updater and Bot
updater = Updater(token=BOT_TOKEN, use_context=True)
dispatcher = updater.dispatcher
bot = Bot(token=BOT_TOKEN)

# Function to delete messages
def delete_msg(update: Update, context: CallbackContext):
    global DELETE_DELAY
    message = update.message
    if message.chat.type == "supergroup":
        user_id = message.from_user.id
        chat_id = message.chat.id
        user_member = bot.get_chat_member(chat_id, user_id)
        if user_member.status in ["administrator", "creator"]:
            return  # Skip deleting admin's messages
        time.sleep(DELETE_DELAY)
        bot.delete_message(chat_id, message.message_id)

# Command to set the delete timer (only for owner or admins)
def set_timer(update: Update, context: CallbackContext):
    global DELETE_DELAY
    user_id = update.message.from_user.id
    chat_id = update.message.chat.id
    user_member = bot.get_chat_member(chat_id, user_id)
    if user_member.status not in ["administrator", "creator"]:
        update.message.reply_text("Only the owner or admins can set the timer.")
        return
    try:
        new_time = int(context.args[0]) if context.args else DELETE_DELAY
        DELETE_DELAY = new_time
        update.message.reply_text(f"Delete timer set to {new_time} seconds.")
    except ValueError:
        update.message.reply_text("Please provide a valid number.")

# Handlers
delete_handler = MessageHandler(Filters.text & Filters.group, delete_msg)
timer_handler = CommandHandler('settimer', set_timer)

# Add handlers to the dispatcher
dispatcher.add_handler(delete_handler)
dispatcher.add_handler(timer_handler)

# Start the bot
updater.start_polling()
updater.idle()
