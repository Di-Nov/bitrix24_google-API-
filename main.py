from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, RedirectResponse
import uvicorn
import requests
import logging

from config import settings

# Настройка логирования
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
    code = request.query_params.get("code")
    if code:
        # Здесь вы можете обменять код на токены
        tokens = exchange_code_for_tokens(code)
        return tokens
    return {"error": "Authorization code not found"}


def exchange_code_for_tokens(code: str):
    data = {
        'grant_type': 'authorization_code',
        'client_id': settings.CLIENT_ID,
        'client_secret': settings.CLIENT_SECRET,
        'redirect_uri': settings.REDIRECT_URI,
        'code': code
    }
    logger.info("Request data: %s", data)

    try:
        response = requests.post(settings.TOKEN_URL, data=data)
        response.raise_for_status()  # Вызывает исключение для статусов 4xx и 5xx

        tokens = response.json()
        access_token = tokens.get('access_token')
        refresh_token = tokens.get('refresh_token')
        logger.info('Access Token: %s', access_token)
        logger.info('Refresh Token: %s', refresh_token)
        return tokens
    except requests.exceptions.HTTPError as http_err:
        logger.error('HTTP error occurred: %s', http_err)
    except Exception as err:
        logger.error('An error occurred: %s', err)

    return {"error": "Failed to obtain tokens"}


if __name__ == "__main__":
    uvicorn.run("main:app", host="localhost", port=8000, reload=True)
