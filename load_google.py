import gspread
from oauth2client.service_account import ServiceAccountCredentials

from config import settings


def load_data_in_google_sheets(data):
    # Определяем область доступа
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    # Загружаем учетные данные
    creds = ServiceAccountCredentials.from_json_keyfile_name(settings.PATH_TO_CREDENTIALS, scope)
    # Авторизуемся с помощью gspread
    client = gspread.authorize(creds)
    # Открываем таблицу по имени
    spreadsheet = client.open("For Bitrix24")
    # Выбираем лист (по имени или индексу)
    worksheet = spreadsheet.worksheet("Лист1")
    # Формируем данные из pydantic схемы
    data_list = []
    first_row = list(data[0].dict().keys())
    data_list.append(first_row)
    data_list.extend([list(x.dict().values()) for x in data])

    # Загружаем данные в таблицу, начиная с ячейки A1
    worksheet.insert_rows(data_list, 2)  # 1 - это индекс строки, с которой начнется вставка
