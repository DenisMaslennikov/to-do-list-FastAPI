from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field

from app.api.v1.classifiers.schemas import ReadTaskStatus, BaseTaskStatus


class BaseTask(BaseModel):
    """Базовая модель задачи."""

    title: str = Field(..., max_length=255, min_length=5)
    complete_before: datetime | None = None
    completed_at: datetime | None = None


class ReadTask(BaseTask):
    """Модель для операций чтения задач."""

    id: UUID
    description: str
    created_at: datetime
    updated_at: datetime | None
    task_status: ReadTaskStatus


class ReadTaskList(BaseTask):
    """Модель для представления задач в списках."""

    id: UUID
    created_at: datetime
    updated_at: datetime | None
    task_status: BaseTaskStatus


class PaginatedTaskList(BaseModel):
    """Сериализатор пагинации списка задач."""

    count: int
    results: list[ReadTaskList]


class CreateTask(BaseTask):
    """Сериализатор создания новой задачи."""

    description: str = Field(..., min_length=5)
    task_status_id: int
