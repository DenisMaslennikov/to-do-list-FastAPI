from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload
from sqlalchemy.orm.strategy_options import _AbstractLoad

from app.api.v1.tasks.schemas import CreateTask
from app.db.models import Task


async def get_task_by_id_repo(session: AsyncSession, task_id: UUID, *options: _AbstractLoad) -> Task:
    """Получение задачи по ID."""
    stmt = select(Task).where(Task.id == task_id)
    if options:
        stmt = stmt.options(*options)
    results = await session.execute(stmt)
    return results.scalar()


async def create_task_repo(session: AsyncSession, new_task: CreateTask, user_id: UUID) -> Task:
    """Создание новой задачи в базе данных"""
    task = Task(**new_task.model_dump(), user_id=user_id)
    session.add(task)
    await session.commit()
    task = await get_task_by_id_repo(session, task.id, joinedload(Task.task_status))
    return task
