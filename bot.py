from telegram import Update, ChatMember
from telegram.ext import Updater, MessageHandler, Filters, CallbackContext, CommandHandler
import os

BOT_TOKEN = os.getenv("BOT_TOKEN", "YOUR_BOT_TOKEN")  # Replace with your actual token
DELETE_DELAY = 3  # Default delete time in seconds

def delete_msg(update: Update, context: CallbackContext):
    global DELETE_DELAY
    if update.effective_message:
        user_id = update.effective_message.from_user.id
        chat_id = update.effective_chat.id
        bot_member = context.bot.get_chat_member(chat_id, context.bot.id)
        user_member = context.bot.get_chat_member(chat_id, user_id)

        # Skip deleting messages from admins (like Auto Filter Bot)
        if user_member.status in [ChatMember.ADMINISTRATOR, ChatMember.CREATOR]:
            return

        context.job_queue.run_once(
            lambda c: context.bot.delete_message(chat_id=chat_id, message_id=update.effective_message.message_id),
            DELETE_DELAY
        )

def set_timer(update: Update, context: CallbackContext):
    global DELETE_DELAY
    if context.args:
        try:
            new_time = int(context.args[0])
            DELETE_DELAY = new_time
            update.message.reply_text(f"Delete timer set to {new_time} seconds.")
        except ValueError:
            update.message.reply_text("Please send a number only.")
    else:
        update.message.reply_text("Usage: /settimer 5")

def main():
    updater = Updater(BOT_TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(MessageHandler(Filters.text & Filters.group, delete_msg))
    dp.add_handler(CommandHandler("settimer", set_timer))

    updater.start_polling()
    updater.idle()

if name == 'main':
    main()
