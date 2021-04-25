import telebot
from telebot import types
from config import token
from get_vacancies import get_dict
from FAQ import make_faq

bot = telebot.TeleBot(token)


# Welcome message
@bot.message_handler(commands=["start"])
def welcome(message):
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    first_button = types.InlineKeyboardButton(text="Открытые стажировки",
                                              callback_data="vacancies")

    second_button = types.InlineKeyboardButton(text="FAQ",
                                               callback_data="FAQ")

    keyboard.add(first_button)
    keyboard.add(second_button)
    bot.send_photo(message.chat.id,
                   welcome_photo
                   )

    bot.send_message(message.chat.id, 'Привет!\n'
                                      'Это карьерный бот компании Naumen.\n'
                                      'Я помогаю узнать информацию о стажировках и отправить заявку.\n'
                                      '\n'
                                      'Что вам интересно?', reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    # Start message
    if call.data == "mainmenu":
        keyboard = types.InlineKeyboardMarkup(row_width=2)

        first_button = types.InlineKeyboardButton(text="Направления стажировок",
                                                  callback_data="vacancies")

        second_button = types.InlineKeyboardButton(text="FAQ",
                                                   callback_data="FAQ")
        keyboard.add(first_button)
        keyboard.add(second_button)

        bot.edit_message_text(chat_id=call.message.chat.id,
                              message_id=call.message.message_id,
                              text='Что вам интересно?',
                              reply_markup=keyboard)

    #  Show vacancies
    if call.data == 'vacancies':
        keyboard = types.InlineKeyboardMarkup()
        for city in vacancies.keys():
            keyboard.add(types.InlineKeyboardButton(text=city.split(':')[1] + '({})'.format(len(vacancies[city])),
                                                    callback_data='{}'.format(city)))

        back_button = types.InlineKeyboardButton(text='<<Назад',
                                                 callback_data='mainmenu')
        keyboard.add(back_button)

        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.id,
                              text='В каком городе вы бы хотели пройти стажировку?',
                              reply_markup=keyboard)

    #  Show FAQ
    elif call.data == "FAQ":
        keyboard = types.InlineKeyboardMarkup()

        for idx, q in enumerate(faqs.keys()):
            keyboard.add(types.InlineKeyboardButton(text=q,
                                                    callback_data=q))

        back_button = types.InlineKeyboardButton(text="<<Назад",
                                                 callback_data="mainmenu")
        keyboard.add(back_button)

        bot.edit_message_text(chat_id=call.message.chat.id,
                              message_id=call.message.id,
                              text='Часто задаваемые вопросы:',
                              reply_markup=keyboard)

    # Vacancies process
    elif call.data in vacancies.keys():

        keyboard = types.InlineKeyboardMarkup()

        if not vacancies[call.data]:

            subscribe_button = types.InlineKeyboardButton(text='Да!',
                                                          callback_data='subscribe')

            back_button = types.InlineKeyboardButton(text="<<Назад",
                                                     callback_data="vacancies")

            keyboard.add(subscribe_button, back_button)
            bot.edit_message_text(chat_id=call.message.chat.id,
                                  message_id=call.message.message_id,
                                  text="В этом городе сейчас нет набора на стажировки.\n"
                                       "Хотите первым узнавать о новых стажировках?",
                                  reply_markup=keyboard)
        else:
            for vac in vacancies[call.data]:
                keyboard.add(types.InlineKeyboardButton(text=vac.split(':')[1],
                                                        callback_data=vac.split(':')[0]
                                                        ))

            back_button = types.InlineKeyboardButton(text="<<Назад",
                                                     callback_data='vacancies')
            keyboard.add(back_button)

            bot.edit_message_text(chat_id=call.message.chat.id,
                                  message_id=call.message.message_id,
                                  text="Сейчас доступны следующие позиции",
                                  reply_markup=keyboard)

    elif call.data.isdigit():
        keyboard = types.InlineKeyboardMarkup()
        back_button = types.InlineKeyboardButton(text='<<Назад',
                                                 callback_data='vacancies')
        apply_button = types.InlineKeyboardButton(text='Отправить заявку',
                                                  callback_data='apply')

        keyboard.add(apply_button)
        keyboard.add(back_button)

        text = ''
        find = False
        for city in vacancies.keys():
            if find:
                break
            segm = city.split(':')[0].split(',')
            try:
                if int(segm[0]) < int(call.data) <= int(segm[1]):
                    for vac in vacancies[city].keys():
                        if vac.split(':')[0] == call.data:
                            find = True
                            text_proc = vacancies[city][vac]
                            for req in text_proc:
                                text += '\n ▬ {}'.format(req)
                            break

            except ValueError:
                pass

        bot.edit_message_text(chat_id=call.message.chat.id,
                              message_id=call.message.message_id,
                              text=text,
                              reply_markup=keyboard)


    # Subscribe or return to vacancies
    elif call.data == 'subscribe':
        keyboard = types.InlineKeyboardMarkup()
        vacs = types.InlineKeyboardButton(text='Да!',
                                          callback_data='vacancies')
        end = types.InlineKeyboardButton(text='Буду ждать \n новых стажировок',
                                         callback_data='wait')
        keyboard.add(vacs)
        keyboard.add(end)
        bot.edit_message_text(chat_id=call.message.chat.id,
                              message_id=call.message.message_id,
                              text="Спасибо за подписку!\n"
                                   "Хотите посмотреть стажировки в других городах?",
                              reply_markup=keyboard)

    # Wait for new positions
    elif call.data == 'wait':
        keyboard = types.InlineKeyboardMarkup()
        ask_button = types.InlineKeyboardButton(text='Задать вопрос',
                                                callback_data='ask')
        more_button = types.InlineKeyboardButton(text='Сайт компании',
                                                 url='https://www.naumen.ru/career/trainee/')
        keyboard.add(ask_button, more_button)

        bot.edit_message_text(chat_id=call.message.chat.id,
                              message_id=call.message.message_id,
                              text="Спасибо, что использовали бота!\n"
                                   "Вопросы можно задать здесь или отправить на почту `nautrainee@naumen.ru`\n\n"
                                   "Ответы на частые вопросы также можно посмотреть на сайте",
                              parse_mode='MarkDown',
                              reply_markup=keyboard)

    # FAQs process
    elif call.data in faqs.keys():
        keyboard = types.InlineKeyboardMarkup()

        for q in faqs.keys():
            keyboard.add(types.InlineKeyboardButton(text=q,
                                                    callback_data=q))
        backbutton = types.InlineKeyboardButton(text="<<Назад",
                                                callback_data="mainmenu")
        keyboard.add(backbutton)

        bot.edit_message_text(chat_id=call.message.chat.id,
                              message_id=call.message.message_id,
                              text=faqs[call.data],
                              reply_markup=keyboard)


if __name__ == "__main__":
    vacancies = get_dict()
    faqs = make_faq()
    q_limit = 38
    welcome_photo = open(
        '/Users/michaelgoloshchapov/PycharmProjects/Physics/URFU_best_21/Miscellaneous/Bot_Welcome.jpeg', 'rb')

    bad_keys = set()
    for key in faqs.keys():
        if len(key) > q_limit:
            bad_keys.add(key)

    for key in bad_keys:
        del faqs[key]

    while True:
        bot.polling(none_stop=True)
