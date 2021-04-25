from config import token
import json_generator
import telebot
import structure_checker

bot = telebot.TeleBot(token)


@bot.message_handler(commands=['form'])
def polling(message, bot_message=None):
    if bot_message is not None:
        bot.delete_message(bot_message.chat.id, bot_message.id)
    user_data = json_generator.get_user_data(message.from_user.id)
    kb = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True, row_width=2)
    kb.add('Личные данные', 'Условия стажировки', 'Образование', 'Опыт работы', 'Опыт кандидата',
           'Как ты узнал о Naumen?', 'Загрузка резюме', 'Отправка задания')
    bot_message = bot.send_message(message.from_user.id, 'Какую часть анкеты вы хотите заполниь?', reply_markup=kb)
    bot.register_next_step_handler(message, polling_distribution, user_data, bot_message=bot_message)
    bot.delete_message(message.from_user.id, message.id)


def end_polling(message, user_data, yn=False, bot_message=None):
    if bot_message is not None:
        bot.delete_message(bot_message.chat.id, bot_message.id)
    if yn:
        if message.text == 'Да':
            polling(message, bot_message=message)

    else:
        json_generator.update_user_data(message.from_user.id, user_data)
        kb = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True)
        kb.row('Да', 'Нет')
        bot_message = bot.send_message(message.from_user.id, 'Хотетие продолжить заполнять анкету?', reply_markup=kb)
        bot.register_next_step_handler(message, end_polling, user_data, yn=True, bot_message=bot_message)

    bot.delete_message(message.from_user.id, message.id)


def polling_distribution(message, user_data, bot_message=None):
    if bot_message is not None:
        bot.delete_message(bot_message.chat.id, bot_message.id)

    t = message.text
    if t == 'Личные данные':
        enter_credentials(message, user_data)
    elif t == 'Условия стажировки':
        enter_probation(message, user_data)
    elif t == 'Образование':
        enter_education(message, user_data)
    elif t == 'Опыт работы':
        enter_work(message, user_data)
    elif t == 'Опыт кандидата':
        enter_experience(message, user_data)
    elif t == 'Как ты узнал о Naumen?':
        enter_naumen(message, user_data)
    elif t == 'Загрузка резюме':
        enter_resume(message, user_data)
    elif t == 'Отправка задания':
        enter_tasks(message, user_data)
        pass

    bot.delete_message(bot_message.chat.id, bot_message.id)


def enter_credentials(message, user_data, step=0, yn=False, bot_message=None, sec_bot_message=None):
    if yn:
        if message.text == 'Да':
            step += 1
        else:
            step -= 1

    if bot_message is not None:
        bot.delete_message(bot_message.chat.id, bot_message.id)

    if step == 0:

        bot_message = bot.send_message(message.from_user.id, "Введите ФИО:")
        bot.register_next_step_handler(message, enter_credentials, user_data, 1, bot_message=bot_message,
                                       sec_bot_message=sec_bot_message)

    elif step == 1:

        b, text = structure_checker.name_input(message.text, user_data)

    elif step == 2:

        bot_message = bot.send_message(message.from_user.id, "Введите вашу дату рождения в формате дд мм гггг:")
        bot.register_next_step_handler(message, enter_credentials, user_data, 3, bot_message=bot_message,
                                       sec_bot_message=sec_bot_message)

    elif step == 3:

        b, text = structure_checker.date_input(message.text, user_data)

    elif step == 4:

        bot_message = bot.send_message(message.from_user.id, "Введите город жительства:")
        bot.register_next_step_handler(message, enter_credentials, user_data, 5, bot_message=bot_message,
                                       sec_bot_message=sec_bot_message)

    elif step == 5:

        b, text = structure_checker.city_input(message.text, user_data)

    elif step == 6:

        bot_message = bot.send_message(message.from_user.id, "Введите ваш адресс электронной почты:")
        bot.register_next_step_handler(message, enter_credentials, user_data, 7, bot_message=bot_message,
                                       sec_bot_message=sec_bot_message)

    elif step == 7:

        b, text = structure_checker.email_input(message.text, user_data)

    elif step == 8:

        bot_message = bot.send_message(message.from_user.id, "Введите ваш номер телефона:")
        bot.register_next_step_handler(message, enter_credentials, user_data, 9, bot_message=bot_message,
                                       sec_bot_message=sec_bot_message)

    elif step == 9:

        b, text = structure_checker.phone_input(message.text, user_data)

    elif step == 10:

        end_polling(message, user_data, bot_message=message)

    if sec_bot_message is not None:
        bot.delete_message(sec_bot_message.from_user.id, sec_bot_message.id)

    if step % 2 == 1:
        if b:
            kb = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True)
            kb.row('Да', 'Нет')
            bot_message = bot.send_message(message.from_user.id,
                                           'Верны ли данные:\n{}'.format(text),
                                           reply_markup=kb)
            bot.delete_message(message.from_user.id, message.id)
            bot.register_next_step_handler(message, enter_credentials, user_data, step, yn=True,
                                           bot_message=bot_message)

        else:
            bot_message = bot.send_message(message.from_user.id, text)
            bot.delete_message(message.from_user.id, message.id)
            enter_credentials(message, user_data, step - 1, sec_bot_message=bot_message)


def enter_probation(message, user_data, step=0, yn=False, bot_message=None, sec_bot_message=None):
    if yn:
        if message.text == 'Да':
            step += 1
        else:
            step -= 1

    if bot_message is not None:
        bot.delete_message(bot_message.chat.id, bot_message.id)

    if step == 0:

        kb = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True, row_width=1)
        kb.add('Екатеринбург', 'Санкт-Петербург', 'Москва', 'Челябинск', 'Тверь')
        bot_message = bot.send_message(message.from_user.id, "В каком городе вы хотите пройти стажировку?",
                                       reply_markup=kb)
        bot.register_next_step_handler(message, enter_probation, user_data, 1, bot_message=bot_message)

    elif step == 1:

        b, text = structure_checker.city_input_prob(message.text, user_data)

    elif step == 2:

        kb = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True)
        kb.row('< 30 частов', '> 30 часов', '40 часов')
        bot_message = bot.send_message(message.from_user.id, "Сколько времени вы готовы уделять стажировке?",
                                       reply_markup=kb)
        bot.register_next_step_handler(message, enter_probation, user_data, 3, bot_message=bot_message)

    elif step == 3:

        print(message.text)
        b, text = structure_checker.probation_time_input(message.text, user_data)
        print(b, text)

    elif step == 4:

        bot_message = bot.send_message(message.from_user.id, "Введите год начала стажировки:")
        bot.register_next_step_handler(message, enter_probation, user_data, 5, bot_message=bot_message)

    elif step == 5:

        b, text = structure_checker.probation_year_input(message.text, user_data)

    elif step == 6:

        kb = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True)
        kb.row('Нет', 'Да, full-time', 'Да, part-time')
        bot_message = bot.send_message(message.from_user.id, "Сможете ли вы работать после стажировки?",
                                       reply_markup=kb)
        bot.register_next_step_handler(message, enter_probation, user_data, 7, bot_message=bot_message)

    elif step == 7:

        b, text = structure_checker.work_after_input(message.text, user_data)

    elif step == 8:

        end_polling(message, user_data, bot_message=message)

    if step % 2 == 1:
        if b:
            kb = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True)
            kb.row('Да', 'Нет')
            bot_message = bot.send_message(message.from_user.id,
                                           'Верны ли данные:\n{}'.format(text),
                                           reply_markup=kb)
            bot.register_next_step_handler(message, enter_probation, user_data, step, yn=True, bot_message=bot_message)
        else:
            bot_message = bot.send_message(message.from_user.id, text)
            enter_probation(message, user_data, step - 1, sec_bot_message=bot_message)

    if sec_bot_message is not None:
        bot.delete_message(sec_bot_message.chat.id, sec_bot_message.id)

    bot.delete_message(message.from_user.id, message.id)


def enter_education(message, user_data, step=0, yn=False, bot_message=None):
    if yn:
        if message.text == 'Да':
            step += 1
        else:
            step -= 1

    if bot_message is not None:
        bot.delete_message(bot_message.chat.id, bot_message.id)

    if step == 0:

        kb = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True, row_width=1)
        kb.add('Высшее', 'Незаконченное высшее', 'Среднее профессиональное', 'Другое')
        bot_message = bot.send_message(message.from_user.id, "Какой уровень образования вы имеете?", reply_markup=kb)
        bot.register_next_step_handler(message, enter_education, user_data, 1, bot_message=bot_message)

    elif step == 1:

        b, text = structure_checker.education_input(message.text, user_data)

    elif step == 2:

        bot_message = bot.send_message(message.from_user.id, "Введите наименование вашего учебного заведения:")
        bot.register_next_step_handler(message, enter_education, user_data, 3, bot_message=bot_message)

    elif step == 3:

        b, text = structure_checker.education_university_input(message.text, user_data)

    elif step == 4:

        bot_message = bot.send_message(message.from_user.id,
                                       "Введите год начала и год окончания обучения через пробел:")
        bot.register_next_step_handler(message, enter_education, user_data, 5, bot_message=bot_message)

    elif step == 5:

        b, text = structure_checker.education_years_input(message.text, user_data)

    elif step == 6:

        bot_message = bot.send_message(message.from_user.id, "Введите ваш факультет и направления обучения:")
        bot.register_next_step_handler(message, enter_education, user_data, 7, bot_message=bot_message)

    elif step == 7:

        b, text = structure_checker.education_faculty_input(message.text, user_data)

    elif step == 8:

        bot_message = bot.send_message(message.from_user.id, "Введите ваш средний балл по 5-ти бальной шкле:")
        bot.register_next_step_handler(message, enter_education, user_data, 9, bot_message=bot_message)

    elif step == 9:

        b, text = structure_checker.education_mean_grade(message.text, user_data)

    elif step == 10:

        bot_message = bot.send_message(message.from_user.id, "Введите что-нибудб про ваше допольнительное образование:")
        bot.register_next_step_handler(message, enter_education, user_data, 11, bot_message=bot_message)

    elif step == 11:

        b, text = structure_checker.education_extra_input(message.text, user_data)

    elif step == 12:

        end_polling(message, user_data, bot_message=message)

    if step % 2 == 1:
        if b:
            kb = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True)
            kb.row('Да', 'Нет')
            bot_message = bot.send_message(message.from_user.id,
                                           'Верны ли данные:\n{}'.format(text),
                                           reply_markup=kb)
            bot.register_next_step_handler(message, enter_education, user_data, step, yn=True, bot_message=bot_message)
        else:
            bot.send_message(message.from_user.id, text)
            enter_education(message, user_data, step - 1, bot_message=None)

    bot.delete_message(message.from_user.id, message.id)


def enter_work(message, user_data, step=0, yn=False, bot_message=None):
    b = True
    if yn:
        if message.text == 'Да':
            if step == 1:
                step += 1
            else:
                step = 10
        else:
            step = 0

    if bot_message is not None:
        bot.delete_message(bot_message.chat.id, bot_message.id)

    if step == 0:

        kb = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True, row_width=1)
        kb.add('1', '2', '3', '4')
        bot_message = bot.send_message(message.from_user.id, "Напишите про ваш опыт работы. Где вы работали, сколько "
                                                             "вы работали, вашу позицию, и умения которые вам были "
                                                             "необходимы. (Всего 4 возможных поля)", reply_markup=kb)
        bot.register_next_step_handler(message, enter_work, user_data, 1, bot_message=bot_message)


    elif step == 1:

        text = message.text

        if text == '1':
            enter_work(message, user_data, 2)
        elif text == '2':
            enter_work(message, user_data, 4)
        elif text == '3':
            enter_work(message, user_data, 6)
        elif text == '4':
            enter_work(message, user_data, 8)
        return

    elif step == 2:

        bot_message = bot.send_message(message.from_user.id, "Напишите про ваше место работы:")
        bot.register_next_step_handler(message, enter_work, user_data, 3, bot_message=bot_message)

    elif step == 3:

        b, text = structure_checker.text_input(message.text, user_data, 'work_1')
        next_step = 10

    elif step == 4:

        bot_message = bot.send_message(message.from_user.id, "Напишите про ваше место работы:")
        bot.register_next_step_handler(message, enter_work, user_data, 5, bot_message=bot_message)
    elif step == 5:

        b, text = structure_checker.text_input(message.text, user_data, 'work_2')
        next_step = 10

    elif step == 6:

        bot_message = bot.send_message(message.from_user.id, "Напишите про ваше место работы:")
        bot.register_next_step_handler(message, enter_work, user_data, 7, bot_message=bot_message)

    elif step == 7:

        b, text = structure_checker.text_input(message.text, user_data, 'work_3')
        next_step = 10

    elif step == 8:

        bot_message = bot.send_message(message.from_user.id, "Напишите про ваше место работы:")
        bot.register_next_step_handler(message, enter_work, user_data, 9, bot_message=bot_message)

    elif step == 9:

        b, text = structure_checker.text_input(message.text, user_data, 'work_4')
        next_step = 10

    elif step == 10:

        end_polling(message, user_data, bot_message=message)

    if step == 1:
        if b:
            kb = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True)
            kb.row('Да', 'Нет')
            bot_message = bot.send_message(message.from_user.id,
                                           'Верны ли данные:\n{}'.format(text),
                                           reply_markup=kb)
            bot.register_next_step_handler(message, enter_work, user_data, 9, yn=True,
                                           bot_message=bot_message)
        else:
            bot.send_message(message.from_user.id, text)
            enter_work(message, user_data, step - 1, bot_message=None)
    elif step % 2 == 1:
        if b:
            kb = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True)
            kb.row('Да', 'Нет')
            bot_message = bot.send_message(message.from_user.id,
                                           'Верны ли данные:\n{}'.format(text),
                                           reply_markup=kb)
            bot.register_next_step_handler(message, enter_work, user_data, 9, yn=True,
                                           bot_message=bot_message)

    bot.delete_message(message.from_user.id, message.id)


def enter_experience(message, user_data, step=0, yn=False, bot_message=None):
    if yn:
        if message.text == 'Да':
            step += 1
        else:
            step -= 1

    if bot_message is not None:
        bot.delete_message(bot_message.chat.id, bot_message.id)

    if step == 0:

        bot_message = bot.send_message(message.from_user.id, "В каких проектах ты принимал участие "
                                                             "(включая учебные проекты)?")
        bot.register_next_step_handler(message, enter_experience, user_data, 1, bot_message=bot_message)

    elif step == 1:

        b, text = structure_checker.text_input(message.text, user_data, 'projects')

    elif step == 2:

        bot_message = bot.send_message(message.from_user.id, "Участвовал ли ты в образовательныъ программах от"
                                                             "Naumen? Если да - расскажи об этом подробнее")
        bot.register_next_step_handler(message, enter_experience, user_data, 3, bot_message=bot_message)

    elif step == 3:

        b, text = structure_checker.text_input(message.text, user_data, 'naumen_programs')

    elif step == 4:

        bot_message = bot.send_message(message.from_user.id, "Какие твои ключевые навыки?")
        bot.register_next_step_handler(message, enter_experience, user_data, 5, bot_message=bot_message)

    elif step == 5:

        b, text = structure_checker.text_input(message.text, user_data, 'key_skills')

    elif step == 6:

        bot_message = bot.send_message(message.from_user.id, "Какие твои профессиональные интересы?")
        bot.register_next_step_handler(message, enter_experience, user_data, 7, bot_message=bot_message)

    elif step == 7:

        b, text = structure_checker.text_input(message.text, user_data, 'professional_interests')

    elif step == 8:

        bot_message = bot.send_message(message.from_user.id, "Последняя прочитаная тобой профессиональная книга?")
        bot.register_next_step_handler(message, enter_experience, user_data, 9, bot_message=bot_message)

    elif step == 9:

        b, text = structure_checker.text_input(message.text, user_data, 'last_professional_book')

    elif step == 10:

        bot_message = bot.send_message(message.from_user.id, "Как ты проводишь свободное время? Чем увлекаешься?")
        bot.register_next_step_handler(message, enter_experience, user_data, 11, bot_message=bot_message)

    elif step == 11:

        b, text = structure_checker.text_input(message.text, user_data, 'free_time')

    elif step == 12:

        bot_message = bot.send_message(message.from_user.id, "Что даст тебе прохождение практики в нашей компании?")
        bot.register_next_step_handler(message, enter_experience, user_data, 13, bot_message=bot_message)

    elif step == 13:

        b, text = structure_checker.text_input(message.text, user_data, 'expectation')

    elif step == 14:

        bot_message = bot.send_message(message.from_user.id, "Какую должность ты хочешь занять через 3-5 лет?")
        bot.register_next_step_handler(message, enter_experience, user_data, 15, bot_message=bot_message)

    elif step == 15:

        b, text = structure_checker.text_input(message.text, user_data, 'future_position')

    elif step == 16:

        end_polling(message, user_data, bot_message=message)

    if step % 2 == 1:
        if b:
            kb = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True)
            kb.row('Да', 'Нет')
            bot_message = bot.send_message(message.from_user.id,
                                           'Верны ли данные:\n{}'.format(text),
                                           reply_markup=kb)
            bot.register_next_step_handler(message, enter_experience, user_data, step, yn=True, bot_message=bot_message)
        else:
            bot.send_message(message.from_user.id, text)
            enter_experience(message, user_data, step - 1, bot_message=None)

    bot.delete_message(message.from_user.id, message.id)


def enter_naumen(message, user_data, step=0, yn=False, bot_message=None):
    if yn:
        if message.text == 'Да':
            step += 1
        else:
            step -= 1

    if bot_message is not None:
        bot.delete_message(bot_message.chat.id, bot_message.id)

    if step == 0:

        kb = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True, row_width=2)
        kb.add('Сайт компании', 'Увидел рекламу в интернете', 'На сайте hh.ru', 'Участвовалв в образовательных'
                                                                                'программах от компании',
               'Социальные сети', 'От друзей или преподавателей', 'Афишы или стенды в университете')
        bot_message = bot.send_message(message.from_user.id, "Как ты узнал о компании Naumen? (Выберите вариант ответа"
                                                             ", либо введите свой)", reply_markup=kb)
        bot.register_next_step_handler(message, enter_naumen, user_data, 1, bot_message=bot_message)

    elif step == 1:

        b, text = structure_checker.text_input(message.text, user_data, 'how_naumen')

    elif step == 2:

        kb = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True, row_width=2)
        kb.add('Сайт компании', 'Увидел рекламу в интернете', 'На сайте hh.ru', 'Участвовалв в образовательных'
                                                                                'программах от компании',
               'Социальные сети', 'От друзей или преподавателей', 'Афишы или стенды в университете')
        bot_message = bot.send_message(message.from_user.id, "Как ты узнал о стажировке в компании Naumen? (Выберите "
                                                             "вариант ответа, либо введите свой)", reply_markup=kb)
        bot.register_next_step_handler(message, enter_naumen, user_data, 3, bot_message=bot_message)

    elif step == 3:

        b, text = structure_checker.text_input(message.text, user_data, 'how_probation')

    elif step == 4:

        bot_message = bot.send_message(message.from_user.id, "Кто может дать тебе рекомендации? (ФИО, должность, "
                                                             "контактный телефон)")
        bot.register_next_step_handler(message, enter_naumen, user_data, 5, bot_message=bot_message)

    elif step == 5:

        b, text = structure_checker.text_input(message.text, user_data, 'recommendations')

    elif step == 6:

        end_polling(message, user_data, bot_message=message)

    if step % 2 == 1:
        if b:
            kb = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True)
            kb.row('Да', 'Нет')
            bot_message = bot.send_message(message.from_user.id,
                                           'Верны ли данные:\n{}'.format(text),
                                           reply_markup=kb)
            bot.register_next_step_handler(message, enter_naumen, user_data, step, yn=True, bot_message=bot_message)
        else:
            bot.send_message(message.from_user.id, text)
            enter_naumen(message, user_data, step - 1, bot_message=None)

    bot.delete_message(message.from_user.id, message.id)


def enter_resume(message, user_data, step=0, yn=False, bot_message=None):
    if yn:
        if message.text == 'Да':
            step += 1
        else:
            step -= 1

    if bot_message is not None:
        bot.delete_message(bot_message.chat.id, bot_message.id)

    if step == 0:
        bot_message = bot.send_message(message.from_user.id, "Введите ссылку на ваше резюме на google-длиске или hh.ru")
        bot.register_next_step_handler(message, enter_resume, user_data, step=1, bot_message=bot_message)
        bot.delete_message(message.from_user.id, message.id)

    elif step == 1:
        b, text = structure_checker.link_input(message.text, user_data, 'resume')
        kb = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True)
        kb.row('Да', 'Нет')
        bot_message = bot.send_message(message.from_user.id,
                                       'Верны ли данные:\n{}'.format(text),
                                       reply_markup=kb)
        bot.register_next_step_handler(message, enter_resume, user_data, bot_message=bot_message, yn=True, step=1)

    elif step == 2:
        end_polling(message, user_data)

    bot.delete_message(message.from_user.id, message.id)


def enter_tasks(message, user_data, step=0, yn=False, bot_message=None):
    if yn:
        if message.text == 'Да':
            step += 1
        else:
            step -= 1

    if bot_message is not None:
        bot.delete_message(bot_message.chat.id, bot_message.id)

    if step == 0:
        bot_message = bot.send_message(message.from_user.id, "Введите ссылку на google-длиск с заданием")
        bot.register_next_step_handler(message, enter_tasks, user_data, step=1, bot_message=bot_message)
        bot.delete_message(message.from_user.id, message.id)

    elif step == 1:
        b, text = structure_checker.link_input(message.text, user_data, 'entrance_tasks')
        kb = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True)
        kb.row('Да', 'Нет')
        bot_message = bot.send_message(message.from_user.id,
                                       'Верны ли данные:\n{}'.format(text),
                                       reply_markup=kb)
        bot.register_next_step_handler(message, enter_tasks, user_data, bot_message=bot_message, yn=True, step=1)

    elif step == 2:
        end_polling(message, user_data)

    bot.delete_message(message.from_user.id, message.id)


bot.polling(none_stop=True)
