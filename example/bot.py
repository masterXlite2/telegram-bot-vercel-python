import telebot
from os import getenv

# Initialize the bot with your token
bot = telebot.TeleBot(getenv("TOKEN"))

# Define command handlers
@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "hello world!")

@bot.message_handler(commands=['help'])
def help(message):
    bot.reply_to(message, "help me!")

# Set webhook and handle updates
@bot.message_handler(func=lambda message: True)
def handle_all_messages(message):
    bot.reply_to(message, "Received message: " + message.text)

if __name__ == "__main__":
    # Set webhook
    bot.remove_webhook()
    bot.set_webhook(url=getenv("webhook"))

    # Start polling
    bot.polling()
