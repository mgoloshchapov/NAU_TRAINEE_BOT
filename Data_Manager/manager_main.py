from spreadsheet import Manager

m = Manager()
Putin = 85
Medvedev = 99
m.add_id(Putin)
m.add_id(Medvedev)
m.set_val_in_col(Putin, "Фамилия", "Путин")
m.set_val_in_col(Putin, "Имя", "Владимир")
m.set_val_in_col(Putin, "Отчество", "Владимирович")
m.set_val_in_col(Medvedev, "Фамилия", "Медведев")

print(Putin, m.get_row(Putin))
print(Medvedev, m.get_row(Medvedev))
print(m.can_apply(Putin))
print(m.can_apply(Medvedev))

m.apply(Putin, "Екатеринбург/Стажер-разработчик java")
