def name_input(name: str, data):
    name.lower()
    names = name.split()
    for n in names:
        if not n.isalpha():
            return False, 'Имя не должно содерждать небуквенных символов'

    if len(names) == 2:
        data['first_name'] = names[0]
        data['second_name'] = names[1]
        return True, 'Имя: {}, Фамилия: {}'.format(names[0], names[1])
    elif len(names) > 2:
        data['first_name'] = names[0]
        data['second_name'] = names[1]
        data['second_name'] = names[2]
        return True, 'Имя: {}, Фамилия: {}, Отчество: {}'.format(names[0], names[1], names[2])
    return False, 'Имя должно содерждать имя и фамилию'


def date_input(date: str, data):
    name = date.split()
    if len(name) == 3:
        for i in name:
            if not i.isdigit():
                return False, 'Формат должен быть: дд мм гггг'
        data['birthdate'] = '-'.join(name)
        return True, '-'.join(name)
    else:
        return False, 'Формат должен быть: дд мм гггг'


def city_input(name: str, data):
    data['residence'] = name
    return True, 'Город: {}'.format(name)


def email_input(email: str, data):
    arr = email.split('@')
    if len(arr) == 2:
        if '.' in arr[1]:
            data['email'] = email
            return True, 'Емайл: {}'.format(email)
    return False, 'Емайл должен иметь формат: aaa@bbb.ccc'


def phone_input(phone: str, data):
    if phone.isdigit():
        if len(phone) == 10:
            data['phone'] = '+7' + phone
            return True, 'Телефон: +7{}'.format(phone)
        elif len(phone) == 11:
            data['phone'] = '+7' + phone[1:]
            return True, 'Телефон: +7{}'.format(phone[1:])
    return False, 'Формат телефона должен быть 10 чисел'


def city_input_prob(name: str, data):
    if name in {'Екатеринбург', 'Санкт-Петербург', 'Москва', 'Челябинск', 'Тверь'}:
        data['probation_location'] = name
        return True, 'Город: {}'.format(name)
    return False, 'В этом городе нет стажировки'


def probation_time_input(string: str, data):
    if string == '< 30 частов':
        data['probation_working_time'] = 0
    elif string == '> 30 часов':
        data['probation_working_time'] = 1
    elif string == '40 часов':
        data['probation_working_time'] = 2
    else:
        return False, 'Неверная опция'
    return True, 'Время: ' + string


def probation_year_input(year: str, data):
    if year.isdigit():
        i_year = int(year)
        if 2020 < i_year < 2050:
            data['probation_starting_time'] = year
            return True, 'Год стажировки: {}'.format(year)
    return False, 'Неверно введён год'


def work_after_input(string: str, data):
    if string == 'Нет':
        data['probation_work_after'] = 0
    elif string == 'Да, full-time':
        data['probation_work_after'] = 1
    elif string == 'Да, part-time':
        data['probation_work_after'] = 2
    else:
        return False, 'Неверная опция'
    return True, 'Время: ' + string


def education_input(string: str, data):
    if string == 'Высшее':
        data['education_level'] = 0
    elif string == 'Незаконченное высшее':
        data['education_level'] = 1
    elif string == 'Среднее профессиональное':
        data['education_level'] = 2
    elif string == 'Другое':
        data['education_level'] = 3
    else:
        return False, 'Неверная опция'
    return True, 'Время: ' + string


def education_university_input(string: str, data):
    data['education_title'] = string
    return True, string


def education_years_input(string: str, data):
    years = string.split()
    for i in years:
        if (not i.isdigit()) or (int(i) < 1970) or (int(i) > 2050):
            return False, 'Неверо укзанные даты'

    data['education_starting_year'] = years[0]
    data['education_ending_year'] = years[1]
    return True, 'Год начала {}, год окончания {}'.format(years[0], years[1])


def education_faculty_input(string: str, data):
    data['education_faculty'] = string
    return True, string


def education_mean_grade(string: str, data):
    if string.isdigit():
        val = float(string)
        if 0 <= val <= 5:
            data['education_mean_grade'] = val
            return True, 'Средний балл: {:.2}'.format(val)
    return False, 'Введите средний балл по 5-ти бальной шкале'


def education_extra_input(string: str, data):
    data['education_other'] = string
    return True, string


def text_input(string: str, data, subsection):
    data[subsection] = string
    return True, string


def link_input(string: str, data, subsection):
    data[subsection] = string
    return True, string