from pydantic import BaseModel


class UserValidation(BaseModel):
    name: str
    last_name: str
    email: str
    type: str
