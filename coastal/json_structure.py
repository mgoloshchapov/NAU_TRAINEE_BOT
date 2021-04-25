import json5


def dict_data():
    data = {'id': 0,
            # credentials
            'first_name': 'Ivan',
            'second_name': 'Ivanvov',
            'patronymic': None,
            'birthdate': '01-01-1970',
            'residence': 'Dolgoprudny',
            'email': 'ivanov.ii@phystech.edu',
            'phone': '84990000000',
            # probation_terms
            'probation_location': '',  # number of option [EKB, MSK, SPB, CHEL, TVER]
            'probation_working_time': 0,  # [40, 30+, 30-]
            'probation_starting_time': '2021',  # year
            'probation_work_after': 0,  # [No, full time, part time, other]
            'probation_work_other': None,  # other
            # education
            'education_level': 0,  # [higher, unfinished higher, middle, other]
            'education_other_level': None,
            'education_title': 'MIPT',
            'education_starting_year': '2020',
            'education_ending_year': '2024',
            'education_faculty': 'FEFM PMF',
            'education_mean_grade': 5,  # 5 grade system
            'education_other': '',
            # work_experience
            'work_count': 0,
            'work_1': '',
            'work_2': '',
            'work_3': '',
            'work_4': '',
            # experience
            'projects': '',
            'naumen_programs': '',
            'key_skills': '',
            'professional_interests': '',
            'last_professional_book': '',
            'free_time': '',
            'expectation': '',
            'future_position': '',
            # naumen
            'how_naumen': 0,
            'how_probation': 0,
            'recommendations': '',
            # other
            'resume': '',
            'entrance_tasks': '',
            'agreement': False
            }
    return data


if __name__ == '__main__':
    file = open('coastal_json/json_template.json5', 'w')
    json5.dump(dict_data, file, indent=2)
