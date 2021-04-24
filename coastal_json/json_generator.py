import json5

import json_structure


def init_user(user_id):
    if not test_for_user(user_id):
        file = open('users/user_{}.json5'.format(user_id), 'w')
        data = json_structure.dict_data()
        data['id'] = user_id
        json5.dump(data, file, indent=2)


def test_for_user(user_id):
    try:
        open('users/user_{}.json5'.format(user_id), 'r')
    except FileNotFoundError:
        return False
    return True
