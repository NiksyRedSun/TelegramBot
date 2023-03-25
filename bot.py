from dotenv import load_dotenv
import os
import telebot

load_dotenv()
bot = telebot.TeleBot(os.getenv("token"))


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    if message.text == "/start":
        bot.send_message(message.from_user.id, "Привет, чем я могу тебе помочь?")


bot.polling(none_stop=True, interval=0)