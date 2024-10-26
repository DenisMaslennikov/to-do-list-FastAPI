from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.v1.dependencies.jwt import get_current_user_id
from app.api.v1.tasks import crud
from app.api.v1.tasks.schemas import CreateTask, ReadTask, PaginatedTaskList
from app.constants import DEFAULT_RESPONSES
from app.db import db_helper

router = APIRouter(tags=["tasks"])


@router.post(
    "/",
    response_model=ReadTask,
    responses=DEFAULT_RESPONSES,
)
async def create_task(
    new_task: CreateTask,
    session: Annotated[AsyncSession, Depends(db_helper.get_session)],
    user_id: Annotated[UUID, Depends(get_current_user_id)],
):
    """Создание новой задачи"""
    return await crud.create_task_repo(session, new_task, user_id)


# @router.get('/', response_model=PaginatedTaskList)
