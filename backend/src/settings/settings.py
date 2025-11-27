from functools import lru_cache
from pydantic import BaseSettings


class Settings(BaseSettings):
    """Компонент для чтения переменных окружения."""

    database_url: str = "postgresql+asyncpg://postgres:postgres@db:5432/mydb"
    secret_key: str = "change-me"
    algorithm: str = "HS256"

    class Config:
        env_file = ".env"


settings = Settings()
