from fastapi import FastAPI, Request, HTTPException, status
from fastapi.responses import HTMLResponse, RedirectResponse
import uvicorn
import logging

from button import button
from config import settings
from services.bitrix_service import BitrixService
from services.google_service import GoogleSheetsService

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()


@app.get("/")
async def home():
    return HTMLResponse(button)


@app.get("/login")
async def login():
    # Перенаправление пользователя на страницу авторизации
    authorization_url = f"{settings.AUTHORIZATION_URL}?response_type=code&client_id={settings.CLIENT_ID}&redirect_uri={settings.REDIRECT_URI}"
    return RedirectResponse(url=authorization_url)


@app.get("/oauth/authorized")
async def callback(request: Request):
    print(request)
    # Получение кода авторизации из параметров запроса и выполнение основной логики загрузки данных
    if code := request.query_params.get("code"):
        bitrix_service = BitrixService()
        bitrix_service.code = code
        bitrix_service.auth()
        data = bitrix_service.get_users()
        scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
        google_service = GoogleSheetsService(spreadsheet_name="For Bitrix24", worksheet_name="Лист1", scope=scope)
        google_service.auth()
        google_service.load_data(data)
    else:
        logger.error("Код авторизации не найден.")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Код авторизации не найден.")


if __name__ == "__main__":
    uvicorn.run("main:app", host=settings.HOST, port=settings.PORT, reload=True)
