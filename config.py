from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env")
    CLIENT_ID: str
    CLIENT_SECRET: str
    DOMAIN: str | None
    REDIRECT_URI: str
    AUTHORIZATION_URL: str
    TOKEN_URL: str


settings = Settings()
