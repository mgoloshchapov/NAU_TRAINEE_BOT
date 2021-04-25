import gspread


class Manager:
    none = "---"
    columns = ['ID', 'Фамилия', 'Имя', 'Отчество', 'Дата рождения', 'Город проживания', 'E-mail', 'Телефон',
               'Город стажировки',
               'Сколько часов в неделю сможешь уделять стажировке?', 'Когда сможешь приступить к стажировке?',
               'Сможешь продолжать работу после окончания стажировки?', 'Образование',
               'Наименование учебного заведения', 'Год поступления-Год окончания', 'Факультет, специальность',
               'Средний балл', ' Дополнительное образование(по желанию)',
               'Опыт работы, практики или стажировки',
               'В каких проектах ты принимал участие(включая учебные проекты)',
               'Участовал ли ты в образовательных программах от Naumen? Если да - расскажи об этом подробнее',
               ' Ключевые навыки', 'Профессиональные интересы',
               'Последняя прочитанная профессиональная книга?', 'Как ты проводишь время, чем увлекаешься?',
               'Что даст тебе прохождение практики в нашей компании?',
               'Какую должность ты хочешь занять через 3-5 лет?', 'Как ты узнал о компании NAUMEN?',
               'Как ты узнал о стажировке в компании NAUMEN?',
               'Кто может дать тебе рекомендации?(ФИО, должность, контактный телефон)', 'Ссылка на резюме',
               'Ссылка на тестовое задание',
               'Согласие на обработку персональных данных']
    vacancies_names = ['Екатеринбург/Стажер-разработчик java', 'Екатеринбург/Стажер-тестировщик',
                       'Екатеринбург/Стажер-аналитик', 'Екатеринбург/Стажер технический писатель',
                       'Тверь/Стажер-разработчик scala', 'Краснодар/Стажер-разработчик java']

    def __init__(self, table_name="NAUMEN", make_worksheets=False):
        service_account = gspread.service_account()
        self.sheet = service_account.open(table_name)
        if make_worksheets:
            for name in ["Data"] + self.vacancies_names + ["Ожидающие"]:
                self.sheet.add_worksheet(title=name, rows=0, cols=50)
                if name == "Ожидающие":
                    self.sheet.worksheet(name).append_row(["ID", "City"])
                else:
                    self.sheet.worksheet(name).append_row(self.columns + self.vacancies_names)
        self.data = self.sheet.worksheet("Data")
        self.waiting_list = self.sheet.worksheet("Ожидающие")
        self.vacancies_lists = [self.sheet.worksheet(name) for name in self.vacancies_names]
        self.data_rows = 1
        self.vacancies_rows = {}
        for name in self.vacancies_names:
            self.vacancies_rows[name] = 1
        self.waiting_list_rows = 1
        self.id_to_row = {}

    def add_id(self, id):
        self.data_rows += 1
        self.id_to_row[id] = self.data_rows
        self.data.append_row([id] + [self.none] * (len(self.columns) + len(self.vacancies_names) - 1))

    def set_val_in_col(self, id, col_name, value):
        n_row = self.id_to_row[id]
        self.data.update_cell(n_row, self.columns.index(col_name) + 1, value)

    def get_row(self, id):
        return self.data.row_values(self.id_to_row[id])

    def can_apply(self, id):
        row = self.get_row(id)
        if any(map(lambda x: x == self.none, row)):
            return []
        ans = []
        for i, vac in enumerate(self.vacancies_names):
            if row[len(self.columns) + i] != "-1":
                ans.append(vac)
        return ans

    def apply(self, id, vacancy):  # vacancy from vacancies_names (town + "/" + vacancy)
        row = self.get_row(id)
        index = self.vacancies_names.index(vacancy)
        self.vacancies_lists[index].append_row(row[:len(self.columns)])

    def apply_row(self, row, vacancy):
        index = self.vacancies_names.index(vacancy)
        self.vacancies_lists[index].append_row(row)
