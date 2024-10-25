from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api import api_router
from app.config import settings
from app.db import db_helper


@asynccontextmanager
async def lifespan(app: FastAPI) -> None:
    """Жизненный цикл приложения."""
    yield

    db_helper.dispose()


main_app = FastAPI(lifespan=lifespan, debug=settings.debug)
main_app.include_router(api_router, prefix=settings.api.prefix)
