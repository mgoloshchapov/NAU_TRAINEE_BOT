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


def get_user_data(user_id):
    if test_for_user(user_id):
        file = open('users/user_{}.json5'.format(user_id), 'r')
        data = json5.load(file)
        return data
    else:
        return init_user(user_id)


def update_user_data(user_id, data):
    file = open('users/user_{}.json5'.format(user_id), 'w')
    json5.dump(data, file, indent=2)
