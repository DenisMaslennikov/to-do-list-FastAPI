from pathlib import Path

from pydantic import BaseModel
from pydantic_settings import BaseSettings
from pydantic_settings import SettingsConfigDict

from app.constants import BASE_DIR


class ApiV1Endpoints(BaseModel):
    """Эндпоинты первой версии апи."""

    users: str = "/users"
    tasks: str = "/tasks"
    classifiers: str = "/classifiers"


class ApiV1(BaseModel):
    """Апи первой версии."""

    prefix: str = "/v1"
    endpoints: ApiV1Endpoints = ApiV1Endpoints()


class Api(BaseModel):
    """Апи."""

    prefix: str = "/api"
    v1: ApiV1 = ApiV1()


class DataBaseSettings(BaseModel):
    """Настройки подключения к базе данных."""

    postgres_db: str
    postgres_password: str
    postgres_user: str
    postgres_host: str
    postgres_port: str

    echo: bool = False

    @property
    def database_uri(self):
        return (
            f"postgresql+asyncpg://{self.postgres_user}:{self.postgres_password}@{self.postgres_host}:"
            f"{self.postgres_port}/{self.postgres_db}"
        )


class Settings(BaseSettings):
    """Конфигурация бекенда."""

    # Настройки подключения к базе данных
    db: DataBaseSettings
    # Корневая директория проекта
    # base_dir: Path = Path(__file__).resolve().parent.parent
    # Надо ли отслеживать изменения в файлах и перезапускать uvicorn
    reload: bool = True

    # Структура эндпоинтов API
    api: Api = Api()

    # Пути к приват и паблик ключам
    private_key_path: Path = BASE_DIR / "certs" / "private_key"
    public_key_path: Path = BASE_DIR / "certs" / "public_key.pub"
    model_config = SettingsConfigDict(case_sensitive=False, env_prefix="API_", env_nested_delimiter="__")


settings = Settings()