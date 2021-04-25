import json5


def dict_data():
    data = {'id': 0,
            # credentials
            'first_name': '',
            'second_name': '',
            'patronymic': None,
            'birthdate': '',
            'residence': '',
            'email': '',
            'phone': '',
            # probation_terms
            'probation_location': '',  # number of option [EKB, MSK, SPB, CHEL, TVER]
            'probation_working_time': '',  # [40, 30+, 30-]
            'probation_starting_time': '',  # year
            'probation_work_after': '',  # [No, full time, part time, other]
            # education
            'education_level': '',  # [higher, unfinished higher, middle, other]
            'education_title': '',
            'education_starting_year': '',
            'education_ending_year': '',
            'education_faculty': '',
            'education_mean_grade': 5,  # 5 grade system
            'education_other': '',
            # work_experience
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
            'how_naumen': '',
            'how_probation': '',
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
