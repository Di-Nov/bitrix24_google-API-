from fastapi import FastAPI, Request, HTTPException, status
from fastapi.responses import HTMLResponse, RedirectResponse
import uvicorn
import logging

from bitrix_service import BitrixService
from load_google import load_data_in_google_sheets

from config import settings

from get_token import exchange_code_for_tokens
from api import get_users

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()


@app.get("/")
async def home():
    return HTMLResponse('<a href="/login">Login with Bitrix24</a>')


@app.get("/login")
async def login():
    # Перенаправление пользователя на страницу авторизации
    authorization_url = f"{settings.AUTHORIZATION_URL}?response_type=code&client_id={settings.CLIENT_ID}&redirect_uri={settings.REDIRECT_URI}"
    return RedirectResponse(url=authorization_url)


@app.get("/oauth/authorized")
async def callback(request: Request):
    # Получение кода авторизации из параметров запроса
    if code := request.query_params.get("code"):
        return {'code': code}
    return {'status': '404 not found'}


if __name__ == "__main__":
    uvicorn.run("main:app", host=settings.HOST, port=settings.PORT, reload=True)
