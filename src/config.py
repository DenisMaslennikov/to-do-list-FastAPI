import os
from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings as PydanticBaseSettings, SettingsConfigDict


class BaseSettings(PydanticBaseSettings):
    """Базовая конфигурация."""

    # Настройки подключения к базе данных
    postgres_db: str
    postgres_password: str
    postgres_user: str
    postgres_host: str
    postgres_port: str
    # Корневая директория проекта
    base_dir: Path = Field(default=Path(__file__).resolve().parent)

    model_config = SettingsConfigDict()

    @property
    def async_database_uri(self) -> str:
        """Получение асинхронного uri для подключения к базе данных."""
        return (
            f"postgresql+asyncpg://{self.postgres_user}:{self.postgres_password}@{self.postgres_host}:"
            f"{self.postgres_port}/{self.postgres_db}"
        )

    @property
    def database_uri(self) -> str:
        """Получение синхронного uri для подключения к базе данных."""
        return (
            f"postgresql+psycopg2://{self.postgres_user}:{self.postgres_password}@{self.postgres_host}:"
            f"{self.postgres_port}/{self.postgres_db}"
        )


class ProductionSettings(BaseSettings):
    """Продакшен конфигурация."""

    pass


class DevelopmentSettings(BaseSettings):
    """Конфигурация разработки."""

    pass


class TestingSettings(BaseSettings):
    """Конфигурация для тестов."""

    pass


def get_settings():
    """Получение конфигурации в зависимости от переменной окружения."""
    env = os.getenv("ENV", None)
    match env.lower():
        case "development":
            return DevelopmentSettings()
        case "testing":
            return TestingSettings()
        case "production":
            return ProductionSettings()
        case _:
            raise ValueError("Неправильно задано окружение в файле конфигурации")


settings = get_settings()
