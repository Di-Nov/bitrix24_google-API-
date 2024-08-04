from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from pydantic import BaseModel
import uvicorn
import requests

from config import settings

app = FastAPI()


# class OAuthCode(BaseModel):
#     code: str
#     state: str | None
#     domain: str
#     member_id: str
#     scope: str
#     server_domain: str


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
    # Обмен кода на токены
    data = {
        'grant_type': 'authorization_code',
        'client_id': settings.CLIENT_ID,
        'client_secret': settings.CLIENT_SECRET,
        'redirect_uri': settings.REDIRECT_URI,
        'code': code
    }
    print("Request data:", data)  # Отладочное сообщение

    response = requests.post(settings.TOKEN_URL, data=data)

    print("Response status code:", response.status_code)
    print("Response text:", response.text)

    if response.status_code == 200:
        tokens = response.json()
        access_token = tokens.get('access_token')
        refresh_token = tokens.get('refresh_token')
        print('Access Token:', access_token)
        print('Refresh Token:', refresh_token)
    else:
        print('Ошибка при получении токенов:', response.json())
    return response.json()


if __name__ == "__main__":
    uvicorn.run("main:app", host="localhost", port=8000, reload=True)
