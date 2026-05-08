import os

from pydantic_settings import BaseSettings, SettingsConfigDict

_env_file = ".env.test" if os.getenv("APP_ENV") == "testing" else ".env"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=_env_file, env_file_encoding="utf-8")

    app_env: str = "development"
    database_url: str = "postgresql+asyncpg://inventory:inventory@localhost:5432/inventory"


settings = Settings()
