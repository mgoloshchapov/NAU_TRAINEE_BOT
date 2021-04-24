import telebot
from telebot import types
from config import token


bot = telebot.TeleBot(token)

@bot.message_handler(content_types=["text"])
def any_msg(message):
    keyboardmain = types.InlineKeyboardMarkup(row_width=2)
    first_button = types.InlineKeyboardButton(text="Открытые стажировки", callback_data="vacancies")
    second_button = types.InlineKeyboardButton(text="FAQs", callback_data="FAQ")
    keyboardmain.add(first_button, second_button)
    bot.send_message(message.chat.id, 'Привет!\n'
                     'Это карьерный бот компании Naumen.\n'
                     'Я помогаю узнать информацию о стажировках и отправить заявку.\n'
                    '\n'
                     'Что вам интересно?', reply_markup=keyboardmain)

@bot.callback_query_handler(func=lambda call:True)
def callback_inline(call):
    if call.data == "mainmenu":
        keyboardmain = types.InlineKeyboardMarkup(row_width=2)
        first_button = types.InlineKeyboardButton(text="Направления стажировок", callback_data="vacancies")
        second_button = types.InlineKeyboardButton(text="FAQs", callback_data="FAQ")
        keyboardmain.add(first_button, second_button)
        bot.edit_message_text(chat_id=call.message.chat.id,message_id=call.message.message_id, text="menu",reply_markup=keyboardmain)

    if call.data == "vacancies":
        keyboard = types.InlineKeyboardMarkup()
        # rele1 = types.InlineKeyboardButton(text="Аналитик", callback_data="1")
        # rele2 = types.InlineKeyboardButton(text="Маркетолог", callback_data="2")
        # rele3 = types.InlineKeyboardButton(text="Суетолог", callback_data="3")
        #
        backbutton = types.InlineKeyboardButton(text="back", callback_data="mainmenu")

        keyboard.add(types.InlineKeyboardButton(text="Аналитик", callback_data="1"),
                     types.InlineKeyboardButton(text="Маркетолог", callback_data="2"),
                     types.InlineKeyboardButton(text="Суетолог", callback_data="3"),
                     backbutton)

        bot.edit_message_text(chat_id=call.message.chat.id,message_id=call.message.message_id, text="replaced text",reply_markup=keyboard)

    elif call.data == "FAQ":
        keyboard = types.InlineKeyboardMarkup()
        rele1 = types.InlineKeyboardButton(text="another layer", callback_data="gg")
        backbutton = types.InlineKeyboardButton(text="back", callback_data="mainmenu")
        keyboard.add(rele1,backbutton)
        bot.edit_message_text(chat_id=call.message.chat.id,message_id=call.message.message_id, text="replaced text",reply_markup=keyboard)

    elif call.data == "1" or call.data == "2" or call.data == "3":
        bot.answer_callback_query(callback_query_id=call.id, show_alert=True, text="alert")
        keyboard3 = types.InlineKeyboardMarkup()
        button = types.InlineKeyboardButton(text="lastlayer", callback_data="ll")
        keyboard3.add(button)
        bot.edit_message_text(chat_id=call.message.chat.id,message_id=call.message.message_id, text="last layer",reply_markup=keyboard3)


if __name__ == "__main__":
    bot.polling(none_stop=True)