from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env")
    HOST: str
    PORT: int
    CLIENT_ID: str
    CLIENT_SECRET: str
    DOMAIN: str | None
    REDIRECT_URI: str
    AUTHORIZATION_URL: str
    TOKEN_URL: str
    PATH_TO_CREDENTIALS: str


settings = Settings()
