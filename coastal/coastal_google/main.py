import spreadsheet as sheet

col_list = ["name", "age", "exp"]
worksheet_name = "Data"
worksheet = sheet.get_worksheet(worksheet_name, col_list)
sheet.add(worksheet, [1, 2, 3])
sheet.add(worksheet, [77, "a;sdlkfj;sk", 77.7])
