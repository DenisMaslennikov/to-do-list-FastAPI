from typing import Literal

from pydantic import BaseModel, ConfigDict


class BaseTaskStatus(BaseModel):
    """Базовый класс для сериализации статуса задачи."""

    model_config = ConfigDict(from_attributes=True)

    name: str


class ReadTaskStatus(BaseTaskStatus):
    """Класс статуса задачи для операций чтения."""

    id: int


class TaskStatusID(BaseModel):
    """Схема id статуса задачи."""

    id: Literal[1, 2]
