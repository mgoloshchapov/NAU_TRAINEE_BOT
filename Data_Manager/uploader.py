import json_generator
from spreadsheet_ import Manager

m = Manager()


def upload(user_id):
    data = json_generator.get_user_data(user_id)
    for key, value in data.items():
        m.set_val_in_col(user_id, m.converter[key], value)
        print(key, m.converter[key], value)


if 344496469 not in m.id_to_row.keys():
    m.add_id(344496469)
print(m.id_to_row)
upload(344496469)
