from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload
from sqlalchemy.sql.functions import count

from app.api.v1.dependencies.users import get_current_user
from app.api.v1.tasks import crud
from app.api.v1.tasks.crud import get_tasks_for_user_repo
from app.api.v1.tasks.schemas import CreateTask, ReadTask, PaginatedTaskList
from app.constants import DEFAULT_RESPONSES
from app.db import db_helper
from app.db.models import User, Task

router = APIRouter(tags=["tasks"])


@router.post(
    "/",
    response_model=ReadTask,
    responses=DEFAULT_RESPONSES,
)
async def create_task(
    new_task: CreateTask,
    session: Annotated[AsyncSession, Depends(db_helper.get_session)],
    user: Annotated[User, Depends(get_current_user)],
) -> Task:
    """Создание новой задачи"""
    return await crud.create_task_repo(session, new_task, user.id)


@router.get("/", response_model=PaginatedTaskList, responses=DEFAULT_RESPONSES)
async def get_task_list_for_user(
    session: Annotated[AsyncSession, Depends(db_helper.get_session)],
    user: Annotated[User, Depends(get_current_user)],
    title: Annotated[str | None, Query(title="Поиск по названию задачи")] = None,
    task_status_id: Annotated[int | None, Query(title="Фильтр по статусу задачи")] = None,
    sort_field: Annotated[str | None, Query(title="Поле для сортировки")] = None,
    sort_direction: Annotated[str, Query(title="Порядок сортировки asc или desc")] = "desc",
    limit: Annotated[int, Query(ge=1, le=100, title="Максимальное количество записей на страницу")] = 10,
    offset: Annotated[int, Query(title="Смещение")] = 0,
) -> PaginatedTaskList:
    """Получение списка задач для пользователя."""
    tasks, count = await get_tasks_for_user_repo(
        session,
        user.id,
        joinedload(Task.task_status),
        title=title,
        task_status_id=task_status_id,
        sort_field=sort_field,
        sort_direction=sort_direction,
        limit=limit,
        offset=offset,
    )
    return PaginatedTaskList(count=count, results=tasks)
