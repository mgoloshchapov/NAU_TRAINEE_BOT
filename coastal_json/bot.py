from config import token
import telebot
import json_generator

bot = telebot.TeleBot(token)


@bot.message_handler(commands=['start'])
def welcome(message):
    user_id = message.from_user.id
    json_generator.init_user(user_id)
    bot.send_message(user_id, 'Bruh cum')


bot.polling(none_stop=True)
