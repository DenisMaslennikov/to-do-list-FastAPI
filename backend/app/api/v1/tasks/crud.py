from datetime import datetime, timezone
from typing import Sequence
from uuid import UUID

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload
from sqlalchemy.orm.strategy_options import _AbstractLoad

from app.api.v1.tasks.schemas import CreateTask, UpdateTask
from app.constants import COMPLETED_TASK_STATUS_ID, NOT_COMPLETED_TASK_STATUS_ID
from app.db.models import Task


async def get_task_by_id_repo(session: AsyncSession, task_id: UUID, *options: _AbstractLoad) -> Task:
    """Получение задачи по ID."""
    stmt = select(Task).where(Task.id == task_id)
    if options:
        stmt = stmt.options(*options)
    results = await session.execute(stmt)
    return results.scalar()


async def create_task_repo(session: AsyncSession, new_task: CreateTask, user_id: UUID) -> Task:
    """Создание новой задачи в базе данных."""
    task = Task(**new_task.model_dump(), user_id=user_id)
    session.add(task)
    await session.commit()
    task = await get_task_by_id_repo(session, task.id, joinedload(Task.task_status))
    return task


async def get_tasks_for_user_repo(
    session: AsyncSession,
    user_id: UUID,
    *options: _AbstractLoad,
    title: str | None = None,
    task_status_id: int | None = None,
    sort_field: str | None = None,
    sort_direction: str = "desc",
    limit: int = 10,
    offset: int = 0,
) -> tuple[Sequence[Task], int]:
    """Получает список задач для пользователя."""
    stmt = select(Task).where(Task.user_id == user_id)
    if title:
        stmt = stmt.where(Task.title.icontains(title))
    if task_status_id:
        stmt = stmt.where(Task.task_status_id == task_status_id)
    if sort_field and hasattr(Task, sort_field):
        if sort_direction == "asc":
            stmt = stmt.order_by(getattr(Task, sort_field).asc())
        else:
            stmt = stmt.order_by(getattr(Task, sort_field).desc())
    if options:
        stmt = stmt.options(*options)
    count_stmt = select(func.count()).select_from(stmt.subquery())
    count_results = await session.execute(count_stmt)
    count = count_results.scalar()
    if limit:
        stmt = stmt.limit(limit)
    if offset is not None:
        stmt = stmt.offset(offset)
    results = await session.execute(stmt)
    return results.scalars().all(), count


async def delete_task_repo(session: AsyncSession, task: Task) -> None:
    """Удаление задачи."""
    await session.delete(task)
    await session.commit()


async def update_task_repo(session: AsyncSession, task: Task, update_task: UpdateTask, partial=False) -> Task:
    """Обновление задачи."""
    task_data = update_task.model_dump(exclude_unset=partial)
    if (
        task.task_status_id == NOT_COMPLETED_TASK_STATUS_ID
        and update_task.task_status_id == COMPLETED_TASK_STATUS_ID
        and update_task.completed_at is None
    ):
        task.completed_at = datetime.now(tz=timezone.utc)
    for key, value in task_data.items():
        setattr(task, key, value)
    await session.commit()
    await session.refresh(task)
    return task
