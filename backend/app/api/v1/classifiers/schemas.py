from pydantic import BaseModel


class BaseTaskStatus(BaseModel):
    """Базовый класс для сериализации статуса задачи."""

    name: str


class ReadTaskStatus(BaseTaskStatus):
    """Клас статуса задачи для операций чтения."""

    id: int
