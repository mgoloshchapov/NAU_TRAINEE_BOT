import Data_Manager.json_generator as json_generator
from Data_Manager.spreadsheet import Manager

m = Manager()


def upload(user_id):
    data = json_generator.get_user_data(user_id)
    if user_id not in m.id_to_row:
        m.add_id(user_id)
    for key, value in data.items():
        m.set_val_in_col(user_id, m.converter[key], value)
    if m.can_apply(user_id):
        m.apply(user_id, 'Екатеринбург/Стажер-разработчик java')
