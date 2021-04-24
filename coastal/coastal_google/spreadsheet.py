import gspread
import pandas as pd

gc = None
table_name = "NAUMEN"


def get_worksheet(worksheet_name, columns):
    global gc
    gc = gspread.service_account()
    sh = gc.open(table_name)
    list_name = worksheet_name
    worksheet = sh.worksheet(list_name)

    # df = pd.DataFrame(worksheet.get_all_records())
    df = pd.DataFrame(columns=columns)
    worksheet.update([df.columns.values.tolist()] + df.values.tolist())

    return [worksheet, 0]


def add(worksheet, row_list):
    worksheet[1] = worksheet[1] + 1
    n_rows = worksheet[1]
    for n_col, element in enumerate(row_list):
        worksheet[0].update_cell(n_rows + 1, n_col + 1, element)
