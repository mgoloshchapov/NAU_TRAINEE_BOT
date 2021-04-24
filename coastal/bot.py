from config import token
import coastal_json.json_structure as json_structure
import telebot
import structure_checker

bot = telebot.TeleBot(token)


@bot.message_handler(commands=['form'])
def polling(message):
    user_id = message.from_user.id
    user_data = json_structure.dict_data()
    kb = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True)
    kb.row('Да', 'Нет')
    bot.send_message(user_id, 'Приступить к заполнению данных?', reply_markup=kb)
    bot.register_next_step_handler(message, enter_credentials, user_data)


def enter_credentials(message, user_data, step=0, yn=False, bot_msg=None):
    if yn:
        if message.text == 'Да':
            step += 1
        else:
            step -= 1

    if bot_msg is not None:
        bot.delete_message(bot_msg.chat.id, bot_msg.id)

    if step == 0:

        bot_message = bot.send_message(message.from_user.id, "Введите ФИО:")
        bot.register_next_step_handler(message, enter_credentials, user_data, 1, bot_msg=bot_message)

    elif step == 1:

        b, text = structure_checker.name_input(message.text, user_data)

    elif step == 2:

        bot_message = bot.send_message(message.from_user.id, "Введите вашу дату рождения в формате дд мм гггг:")
        bot.register_next_step_handler(message, enter_credentials, user_data, 3, bot_msg=bot_message)

    elif step == 3:

        b, text = structure_checker.date_input(message.text, user_data)

    elif step == 4:

        bot_message = bot.send_message(message.from_user.id, "Введите город жительства:")
        bot.register_next_step_handler(message, enter_credentials, user_data, 5, bot_msg=bot_message)

    elif step == 5:

        b, text = structure_checker.city_input(message.text, user_data)

    elif step == 6:

        bot_message = bot.send_message(message.from_user.id, "Введите ваш адресс электронной почты:")
        bot.register_next_step_handler(message, enter_credentials, user_data, 7, bot_msg=bot_message)

    elif step == 7:

        b, text = structure_checker.email_input(message.text, user_data)

    elif step == 8:

        bot_message = bot.send_message(message.from_user.id, "Введите ваш номер телефона:")
        bot.register_next_step_handler(message, enter_credentials, user_data, 9, bot_msg=bot_message)

    elif step == 9:

        b, text = structure_checker.phone_input(message.text, user_data)

    elif step == 10:
        pass

    if step % 2 == 1:
        if b:
            kb = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True)
            kb.row('Да', 'Нет')
            bot_message = bot.send_message(message.from_user.id,
                                           'Верны ли данные:\n{}'.format(text),
                                           reply_markup=kb)
            bot.register_next_step_handler(message, enter_credentials, user_data, step, yn=True, bot_msg=bot_message)
        else:
            bot.send_message(message.from_user.id, text)
            enter_credentials(message, user_data, step - 1)

    bot.delete_message(message.from_user.id, message.id)


bot.polling(none_stop=True)
