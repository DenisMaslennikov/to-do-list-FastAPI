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
    base_dir: Path = Path(__file__).resolve().parent.parent.parent
    # Надо ли отслеживать изменения в файлах и перезапускать uvicorn
    reload: bool = False
    # Пути к приват и паблик ключам
    private_key_path: Path = base_dir / "certs" / "private_key"
    public_key_path: Path = base_dir / "certs" / "public_key.pub"
    model_config = SettingsConfigDict()

    @property
    def database_uri(self) -> str:
        """Получение асинхронного uri для подключения к базе данных."""
        return (
            f"postgresql+asyncpg://{self.postgres_user}:{self.postgres_password}@{self.postgres_host}:"
            f"{self.postgres_port}/{self.postgres_db}"
        )


class ProductionSettings(BaseSettings):
    """Продакшен конфигурация."""

    pass


class DevelopmentSettings(BaseSettings):
    """Конфигурация разработки."""

    reload: bool = True
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
