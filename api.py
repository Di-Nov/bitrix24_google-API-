import logging
import requests
from config import settings

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def create_api(rest_req: str, access_token, select=None, query=None):
    url = f"https://{settings.DOMAIN}.bitrix24.ru/rest/{rest_req}"
    headers = {"Authorization": f"Bearer {access_token}"}

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()

        result = response.json()

        user_names = []
        for user in result['result']:
            print(user)
            name = user['NAME']
            last_name = user['LAST_NAME']
            user_names.append({
                "name": name,
                "last_name": last_name,
                "email": user['EMAIL'],
                "type": user['USER_TYPE']
            })

        return user_names

    except requests.exceptions.HTTPError as http_err:
        logger.error('HTTP error occurred: %s', http_err)
        return {"error": str(http_err)}
    except Exception as err:
        logger.error('An error occurred: %s', err)
        return {"error": str(err)}


def get_contacts(access_token: str):
    rest_req = "crm.contact.list"
    contacts = create_api(rest_req, access_token)
    return contacts


def get_tasks(access_token: str):
    rest_req = "crm.contact.list"
    tasks = create_api(rest_req, access_token)
    return tasks


def get_users(access_token: str):
    rest_req = "user.get"
    users = create_api(rest_req, access_token)
    return users
