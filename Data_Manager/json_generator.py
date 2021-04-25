import json5

from Data_Manager import json_structure


def init_user(user_id):
    if not test_for_user(user_id):
        file = open('Data_Manager/user_data/user_{}.json5'.format(user_id), 'w')
        data = json_structure.dict_data()
        data['id'] = user_id
        json5.dump(data, file, indent=2)
        return data


def test_for_user(user_id):
    try:
        open('Data_Manager/user_data/user_{}.json5'.format(user_id), 'r')
    except FileNotFoundError:
        return False
    return True


def get_user_data(user_id):
    if test_for_user(user_id):
        file = open('Data_Manager/user_data/user_{}.json5'.format(user_id), 'r')
        data = json5.load(file)
        return data
    else:
        return init_user(user_id)


def update_user_data(user_id, data):
    file = open('Data_Manager/user_data/user_{}.json5'.format(user_id), 'w')
    json5.dump(data, file, indent=2)
