from fastapi import APIRouter

from app.api.v1.users import users_router
from app.api.v1.tasks import tasks_router
from app.config import settings

v1_router = APIRouter()
v1_router.include_router(users_router, prefix=settings.api.v1.endpoints.users)
v1_router.include_router(tasks_router, prefix=settings.api.v1.endpoints.tasks)
