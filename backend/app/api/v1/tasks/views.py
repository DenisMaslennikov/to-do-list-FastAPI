from typing import Annotated

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from app.api.v1.classifiers.schemas import TaskStatusID
from app.api.v1.dependencies.tasks import get_task_by_id_for_current_user
from app.api.v1.dependencies.users import get_current_user
from app.api.v1.tasks import crud
from app.api.v1.tasks.schemas import CreateTask, PaginatedTaskList, ReadTask, UpdateTask
from app.constants import DEFAULT_RESPONSES
from app.db import db_helper
from app.db.models import Task, User

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
    """Создание новой задачи."""
    return await crud.create_task_repo(session, new_task, user.id)


@router.get("/", response_model=PaginatedTaskList, responses=DEFAULT_RESPONSES)
async def get_task_list_for_user(
    session: Annotated[AsyncSession, Depends(db_helper.get_session)],
    user: Annotated[User, Depends(get_current_user)],
    title: Annotated[str | None, Query(title="Поиск по названию задачи")] = None,
    task_status_id: Annotated[int | None, Query(title="Фильтр по статусу задачи")] = None,
    sort_field: Annotated[str | None, Query(title="Поле для сортировки")] = None,
    sort_direction: Annotated[str, Query(title="Порядок сортировки asc или desc", enum=["asc", "desc"])] = "desc",
    limit: Annotated[int, Query(ge=1, le=100, title="Количество записей на страницу")] = 10,
    offset: Annotated[int, Query(title="Смещение")] = 0,
) -> PaginatedTaskList:
    """Получение списка задач для пользователя."""
    tasks, count = await crud.get_tasks_for_user_repo(
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


@router.get(
    "/{task_id}",
    response_model=ReadTask,
    responses=DEFAULT_RESPONSES | {status.HTTP_404_NOT_FOUND: {"description": "Пользователь или задача не найдены."}},
)
async def get_task(
    task: Annotated[Task, Depends(get_task_by_id_for_current_user)],
) -> Task:
    """Получение задачи по id."""
    return task


@router.delete(
    "/{task_id}",
    responses=DEFAULT_RESPONSES | {status.HTTP_404_NOT_FOUND: {"description": "Пользователь или задача не найдены."}},
    status_code=status.HTTP_204_NO_CONTENT,
    response_description="Задача удалена",
)
async def delete_task(
    task: Annotated[Task, Depends(get_task_by_id_for_current_user)],
    session: Annotated[AsyncSession, Depends(db_helper.get_session)],
) -> None:
    """Удаление задачи по id."""
    await crud.delete_task_repo(session, task)


@router.put(
    "/{task_id}",
    response_model=ReadTask,
    responses=DEFAULT_RESPONSES | {status.HTTP_404_NOT_FOUND: {"description": "Пользователь или задача не найдены."}},
)
async def update_task(
    update_task: UpdateTask,
    task: Annotated[Task, Depends(get_task_by_id_for_current_user)],
    session: Annotated[AsyncSession, Depends(db_helper.get_session)],
) -> Task:
    """Полное обновление задачи."""
    task = await crud.update_task_repo(session, task, update_task)
    return task


@router.patch(
    "/{task_id}",
    response_model=ReadTask,
    responses=DEFAULT_RESPONSES | {status.HTTP_404_NOT_FOUND: {"description": "Пользователь или задача не найдены."}},
)
async def update_task_status(
    task_status: TaskStatusID,
    task: Annotated[Task, Depends(get_task_by_id_for_current_user)],
    session: Annotated[AsyncSession, Depends(db_helper.get_session)],
) -> Task:
    """Обновление статуса задачи."""
    task = await crud.update_task_status_repo(session, task, task_status)
    return task
