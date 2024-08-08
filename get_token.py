import requests
from fastapi import HTTPException

from config import settings
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def exchange_code_for_tokens(code: str):
    '''Здесь вы можете обменять код на токены'''

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
        raise HTTPException(status_code=http_err.response.status_code, detail=str(http_err))
    except Exception as err:
        logger.error('An error occurred: %s', err)
        raise HTTPException(status_code=500, detail="Failed to obtain tokens")
