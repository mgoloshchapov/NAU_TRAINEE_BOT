import gspread


class Manager:
    none = "---"
    columns = ['ID',
               'Фамилия',
               'Имя',
               'Отчество',
               'Дата рождения',
               'Город проживания',
               'E-mail',
               'Телефон',
               'Город стажировки',
               'Сколько часов в неделю сможешь уделять стажировке?',
               'Когда сможешь приступить к стажировке?',
               'Сможешь продолжать работу после окончания стажировки?',
               'Образование',
               'Наименование учебного заведения',
               'Год поступления-Год окончания',
               'Факультет, специальность',
               'Средний балл',
               'Дополнительное образование(по желанию)',
               'Опыт работы, практики или стажировки',
               'Работа 1',
               'Работа 2',
               'Работа 3',
               'Работа 4',
               'В каких проектах ты принимал участие(включая учебные проекты)',
               'Участовал ли ты в образовательных программах от Naumen? Если да - расскажи об этом подробнее',
               'Ключевые навыки',
               'Профессиональные интересы',
               'Последняя прочитанная профессиональная книга?',
               'Как ты проводишь время, чем увлекаешься?',
               'Что даст тебе прохождение практики в нашей компании?',
               'Какую должность ты хочешь занять через 3-5 лет?',
               'Как ты узнал о компании NAUMEN?',
               'Как ты узнал о стажировке в компании NAUMEN?',
               'Кто может дать тебе рекомендации?(ФИО, должность, контактный телефон)',
               'Ссылка на резюме',
               'Ссылка на тестовое задание',
               'Согласие на обработку персональных данных']

    obligatory = {'ID',
                  'Фамилия',
                  'Имя',
                  'Отчество',
                  'Дата рождения',
                  'Город проживания',
                  'E-mail',
                  'Телефон',
                  'Город стажировки',
                  'E-mail',
                  'Телефон',
                  'Город стажировки',
                  'Сколько часов в неделю сможешь уделять стажировке?',
                  'Когда сможешь приступить к стажировке?',
                  'Сможешь продолжать работу после окончания стажировки?',
                  'Образование',
                  'Наименование учебного заведения',
                  'Год поступления-Год окончания',
                  'Факультет, специальность',
                  'Средний балл',
                  'Ссылка на резюме',
                  'Ссылка на тестовое задание',
                  'Согласие на обработку персональных данных'}

    converted_columns = ['id',
                         'first_name',
                         'second_name',
                         'patronymic',
                         'birthdate',
                         'residence',
                         'email',
                         'phone',
                         'probation_location',
                         'probation_working_time',
                         'probation_starting_time',
                         'probation_work_after',
                         # 'probation_work_other',
                         'education_level',
                         # 'education_other_level',
                         'education_title',
                         'education_starting_year',
                         'education_ending_year',
                         'education_faculty',
                         'education_mean_grade',
                         'education_other',
                         # 'work_count',
                         'work_1',
                         'work_2',
                         'work_3',
                         'work_4',
                         'projects',
                         'naumen_programs',
                         'key_skills',
                         'professional_interests',
                         'last_professional_book',
                         'free_time',
                         'expectation',
                         'future_position',
                         'how_naumen',
                         'how_probation',
                         'recommendations',
                         'resume',
                         'entrance_tasks',
                         'agreement']
    vacancies_names = ['Екатеринбург/Стажер-разработчик java', 'Екатеринбург/Стажер-тестировщик',
                       'Екатеринбург/Стажер-аналитик', 'Екатеринбург/Стажер технический писатель',
                       'Тверь/Стажер-разработчик scala', 'Краснодар/Стажер-разработчик java']

    converter = {}

    def __init__(self, table_name="NAUMEN", make_worksheets=False):
        for col_name, col_key in zip(self.columns, self.converted_columns):
            self.converter[col_key] = col_name
        service_account = gspread.service_account()
        self.sheet = service_account.open(table_name)
        if make_worksheets:
            for name in ["Data"] + self.vacancies_names + ["Waiting list"]:
                self.sheet.add_worksheet(title=name, rows=0, cols=50)
                if name == "Waiting list":
                    self.sheet.worksheet(name).append_row(["ID", "City"])
                else:
                    self.sheet.worksheet(name).append_row(self.columns)  # + self.vacancies_names)
        self.data = self.sheet.worksheet("Data")
        self.waiting_list = self.sheet.worksheet("Waiting list")
        self.vacancies_lists = [self.sheet.worksheet(name) for name in self.vacancies_names]
        self.data_rows = 1
        self.vacancies_rows = {}
        for name in self.vacancies_names:
            self.vacancies_rows[name] = 1
        self.waiting_list_rows = 1
        self.id_to_row = {}
        self.load_id()

    def add_id(self, id):
        if id in self.id_to_row:
            return
        self.data_rows += 1
        self.id_to_row[id] = self.data_rows
        self.data.append_row([id] + [self.none] * (len(self.columns) - 1))

    def set_val_in_col(self, id, col_name, value):
        n_row = self.id_to_row[id]
        self.data.update_cell(n_row, self.columns.index(col_name) + 1, value)

    def get_row(self, id):
        return self.data.row_values(self.id_to_row[id])

    def can_apply(self, id):
        row = self.get_row(id)
        for col_name, value in zip(self.columns, row):
            if col_name not in self.obligatory:
                continue
            if value == self.none:
                return False
        return True

    def apply(self, id, vacancy):  # vacancy from vacancies_names (town + "/" + vacancy)
        row = self.get_row(id)
        index = self.vacancies_names.index(vacancy)
        self.vacancies_lists[index].append_row(row[:len(self.columns)])
        self.vacancies_lists[index].format("B" + str(self.id_to_row[id]) + ":" + "D" + str(self.id_to_row[id]),
                                           {"textFormat": {"bold": True}})

    def load_id(self):
        ids = self.data.col_values(1)[1:]
        self.data_rows = len(ids) + 1
        for n_row, id in enumerate(ids):
            n_row += 2
            self.id_to_row[int(id)] = int(n_row)

    def apply_to_waiting(self, id, city):
        self.waiting_list.append_row([id, city])

    # def apply_row(self, row, vacancy):
    #     index = self.vacancies_names.index(vacancy)
    #     self.vacancies_lists[index].append_row(row)
