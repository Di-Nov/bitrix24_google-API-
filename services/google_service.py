import gspread
from oauth2client.service_account import ServiceAccountCredentials

from config import settings
from schemas import UserSchema


class GoogleSheetsService:
    def __init__(self, spreadsheet_name: str, worksheet_name: str, scope: list[str]):
        self.spreadsheet_name = spreadsheet_name
        self.worksheet_name = worksheet_name
        self.scope = scope
        self.client = None

    def auth(self):
        """Авторизует клиента для работы с Google Sheets."""
        creds = ServiceAccountCredentials.from_json_keyfile_name(settings.PATH_TO_CREDENTIALS, self.scope)
        self.client = gspread.authorize(creds)

    def load_data(self, data: list[UserSchema]):
        """Загружает данные в Google Sheets."""
        if self.client:
            if not data:
                raise ValueError("Данные для загрузки не могут быть пустыми.")
            try:
                spreadsheet = self.client.open(self.spreadsheet_name)  # Открываем таблицу по имени
                worksheet = spreadsheet.worksheet(self.worksheet_name)  # Выбираем лист по имени
                data_list = []
                first_row = list(data[0].model_dump().keys())  # Достаем первую строку в качестве заголовка таблицы
                data_list.append(first_row)
                data_list.extend([list(x.model_dump().values()) for x in data])  # Достаем остальные строки
                worksheet.insert_rows(data_list, 2)  # Загружаем данные в таблицу, начиная с ячейки A2
            except gspread.exceptions.WorksheetNotFound:
                raise ValueError(
                    f"Лист с именем '{self.worksheet_name}' не найден в таблице '{self.spreadsheet_name}'.")
            except Exception as e:
                raise RuntimeError(f"Произошла ошибка при загрузке данных: {e}")
        else:
            raise ValueError("Клиент Google Sheets не инициализирован.")