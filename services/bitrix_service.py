from fastapi import HTTPException, Request

from config import settings
from logger import logger
import requests

from schemas import UserSchemaIn


class BitrixService:
    def __init__(self):
        # self.code = code
        self.code = ''
        self.headers = {}

    def get_code(self):
        # url = 'http://localhost:8000/login'
        authorization_url = f"{settings.AUTHORIZATION_URL}?response_type=code&client_id={settings.CLIENT_ID}&redirect_uri={settings.REDIRECT_URI}"
        response = requests.get(authorization_url, allow_redirects=True)
        print(response)

    def auth(self):
        data = {
            'grant_type': 'authorization_code',
            'client_id': settings.CLIENT_ID,
            'client_secret': settings.CLIENT_SECRET,
            'redirect_uri': settings.REDIRECT_URI,
            'code': self.code
        }
        logger.info("Request data: %s", data)

        try:
            response = requests.post(settings.TOKEN_URL, data=data)
            response.raise_for_status()  # Вызывает исключение для статусов 4xx и 5xx

            tokens = response.json()
            self.headers = {"Authorization": f"Bearer {tokens.get('access_token')}"}
            logger.info(self.headers)
        except requests.exceptions.HTTPError as http_err:
            logger.error('HTTP error occurred: %s', http_err)
            raise HTTPException(status_code=http_err.response.status_code, detail=str(http_err))
        except Exception as err:
            logger.error('An error occurred: %s', err)
            raise HTTPException(status_code=500, detail="Failed to obtain tokens")

    def get_users(self):
        try:
            response = requests.get(self.url_constr("user.get"), headers=self.headers)
            response.raise_for_status()

            result = UserSchemaIn(**response.json())

            return result.result

        except requests.exceptions.HTTPError as http_err:
            logger.error('HTTP error occurred: %s', http_err)
            return {"error": str(http_err)}
        except Exception as err:
            logger.error('An error occurred: %s', err)
            return {"error": str(err)}

    @staticmethod
    def url_constr(rest_req):
        return f"https://{settings.DOMAIN}.bitrix24.ru/rest/{rest_req}"
