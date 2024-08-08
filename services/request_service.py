from typing import Any, Type, Literal

from pydantic import BaseModel, ValidationError
import requests
from json import JSONDecodeError

def castom_request(
        url: str,
        method: Literal['GET', 'POST', 'PUT', 'PATCH', 'DELETE'] = 'GET',
        params: dict[str, Any] | None = None,
        schema: Type[BaseModel] | None = None,
        **kwargs,
):
    """В данном скрипте не используется, надо доработать"""
    try:
        response = requests.request(url=url, method=method, params=params)
        response.raise_for_status()
        if schema:
            return schema(**response.json())

    except TypeError as er:
        raise er
    except JSONDecodeError as er:
        raise er
    except ValidationError as er:
        raise er
    except Exception as Ex:
        raise Ex
