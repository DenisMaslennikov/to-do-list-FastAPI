from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.v1.dependencies.jwt import get_current_user_id
from app.api.v1.tasks import crud
from app.api.v1.tasks.schemas import CreateTask, ReadTask
from app.db import db_helper

router = APIRouter(tags=["tasks"])


@router.post(
    "/",
    response_model=ReadTask,
    responses={
        status.HTTP_400_BAD_REQUEST: {"description": "Такой email или username уже есть в базе"},
        status.HTTP_404_NOT_FOUND: {"description": "Пользователь не найден в базе данных"},
        status.HTTP_401_UNAUTHORIZED: {"description": "Ошибка авторизации"},
        status.HTTP_403_FORBIDDEN: {"description": "Вы не авторизовались"},
    },
)
async def create_task(
    new_task: CreateTask,
    session: Annotated[AsyncSession, Depends(db_helper.get_session)],
    user_id: Annotated[UUID, Depends(get_current_user_id)],
):
    """Создание новой задачи"""
    return await crud.create_task_repo(session, new_task, user_id)
