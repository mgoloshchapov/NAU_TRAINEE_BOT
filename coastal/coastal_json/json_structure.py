import json5


def dict_data():
    data = {'id': 0,
                 'credentials':
                     {'first_name': 'Ivan',
                      'second_name': 'Ivanvov',
                      'patronymic': None,
                      'birthdate': '01-01-1970',
                      'residence': 'Dolgoprudny',
                      'email': 'ivanov.ii@phystech.edu',
                      'phone': '84990000000'},
                 'probation_terms':
                     {'location': 0,  # number of option [EKB, MSK, SPB, CHEL, TVER]
                      'working_time': 0,  # [40, 30+, 30-]
                      'starting_time': '2021',  # year
                      'work_after': 0,  # [No, full time, part time, other]
                      'other': None},  # other
                 'education':
                     {'level': 0,  # [higher, unfinished higher, middle, other]
                      'other_level': None,
                      'title': 'MIPT',
                      'starting_year': '2020',
                      'ending_year': '2024',
                      'faculty': 'FEFM PMF',
                      'mean_grade': 5,  # 5 grade system
                      'other': ''},
                 'work_experience':
                     {'count': 0,
                      'period': [],
                      'place': [],
                      'position': [],
                      'skills': []},
                 'experience':
                     {'projects': '',
                      'naumen_programs': '',
                      'key_skills': '',
                      'professional_interests': '',
                      'last_professional_book': '',
                      'free_time': '',
                      'expectation': '',
                      'future_position': ''},
                 'naumen':
                     {'how_naumen': 0,
                      'how_probation': 0,
                      'recommendations': ''},
                 'resume': '',
                 'entrance_tasks': '',
                 'agreement': False
                 }
    return data

if __name__ == '__main__':
    file = open('json_template.json5', 'w')
    json5.dump(dict_data, file, indent=2)
