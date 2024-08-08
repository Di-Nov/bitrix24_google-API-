from pydantic import BaseModel, Field


class UserSchema(BaseModel):
    name: str = Field(alias='NAME')
    last_name: str = Field(alias='LAST_NAME')
    email: str = Field(alias='EMAIL')
    type: str = Field(alias='USER_TYPE')


class UserSchemaIn(BaseModel):
    result: list[UserSchema]
