from pydantic import BaseModel, ConfigDict


class BaseTaskStatus(BaseModel):
    """Базовый класс для сериализации статуса задачи."""

    model_config = ConfigDict(from_attributes=True)

    name: str


class ReadTaskStatus(BaseTaskStatus):
    """Клас статуса задачи для операций чтения."""

    id: int
