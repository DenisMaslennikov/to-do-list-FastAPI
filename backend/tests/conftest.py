from typing import Generator

import alembic
import pytest
from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine
from httpx import AsyncClient, ASGITransport

from tests.constants import TEST_MIGRATIONS_HOST, TEST_APP_HOST
from tests.functions import wait_for_port

from app import main_app
from app.config import settings


@pytest.fixture
def client() -> Generator[AsyncClient, None, None]:
    with AsyncClient(app=main_app, transport=ASGITransport(app=main_app), base_url="http://localhost:8000") as ac:
        yield ac


@pytest.fixture
def migration_database_url() -> str:
    """Урл для подключения к базе данных для теста миграций."""
    return (
        f"postgresql+asyncpg://"
        f"{settings.db.postgres_user}:"
        f"{settings.db.postgres_password}@"
        f"{TEST_MIGRATIONS_HOST}:"
        f"{settings.db.postgres_port}/"
        f"{settings.db.postgres_db}"
    )


@pytest.fixture
def app_database_url() -> str:
    """Урл для подключения к базе данных для теста приложения."""
    return (
        f"postgresql+asyncpg://"
        f"{settings.db.postgres_user}:"
        f"{settings.db.postgres_password}@"
        f"{TEST_APP_HOST}:"
        f"{settings.db.postgres_port}/"
        f"{settings.db.postgres_db}"
    )


@pytest.fixture
async def alembic_engine(migrations_test_container, migration_database_url) -> AsyncEngine:
    """Используется pytest-alembic."""
    return create_async_engine(migration_database_url)


@pytest.fixture
def alembic_config(migration_database_url):
    """Используется pytest-alembic, для настройки конфигурации алембика."""
    alembic_config = alembic.config.Config()
    alembic_config.set_main_option("sqlalchemy.url", migration_database_url)
    return alembic_config


@pytest.fixture(scope="session")
def migrations_test_container():
    """Для тестирования миграций alembic."""
    wait_for_port(TEST_MIGRATIONS_HOST, settings.db.postgres_port)


@pytest.fixture(scope="session")
def database_test_container():
    """Для тестирования."""
    if not wait_for_port(TEST_APP_HOST, settings.db.postgres_port):
        pytest.exit(f"Exiting: Failed to connect to {TEST_APP_HOST} container.")
