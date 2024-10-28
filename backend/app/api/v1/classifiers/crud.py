from typing import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import TaskStatus


async def get_list_task_status_repo(session: AsyncSession) -> Sequence[TaskStatus]:
    """Получение списка возможных статусов задач."""
    stmt = select(TaskStatus)
    result = await session.execute(stmt)
    return result.scalars().all()
