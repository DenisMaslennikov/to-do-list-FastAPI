from fastapi import FastAPI

from app.api import api_router
from app.config import settings

main_app = FastAPI()
main_app.include_router(api_router, prefix=settings.api.prefix)
