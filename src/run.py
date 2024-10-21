import uvicorn

from alembic import command
from alembic.config import Config as AlembicConfig
from fastapi import FastAPI

from config import settings


app = FastAPI()

if __name__ == "__main__":
    alembic_cfg = AlembicConfig("alembic.ini")

    alembic_cfg.set_main_option("sqlalchemy.url", settings.async_database_uri)

    command.upgrade(alembic_cfg, "head")

    # Запуск сервера
    uvicorn.run("run:app", host="0.0.0.0", port=8000, reload=True)
