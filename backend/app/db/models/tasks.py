from datetime import datetime, timezone
from functools import partial
from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import ForeignKey, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship, validates
from sqlalchemy.sql.sqltypes import DATETIME_TIMEZONE

from app.db.models.base import Base
from app.db.models.mixins import UUIDPrimaryKey

if TYPE_CHECKING:
    from app.db.models import TaskStatus, User


class Task(UUIDPrimaryKey, Base):
    """Модель задачи."""

    __tablename__ = "tasks"
    title: Mapped[str] = mapped_column(String(255), comment="Заголовок задачи", index=True)
    description: Mapped[str] = mapped_column(comment="Описание задачи")
    task_status_id: Mapped[int] = mapped_column(
        ForeignKey("cl_task_status.id", ondelete="RESTRICT"),
        comment="Идентификатор статуса",
        index=True,
    )
    user_id: Mapped[UUID] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        comment="Идентификатор пользователя",
        index=True,
    )
    created_at: Mapped[datetime] = mapped_column(DATETIME_TIMEZONE, server_default=func.now(), comment="Создана")
    updated_at: Mapped[datetime | None] = mapped_column(
        DATETIME_TIMEZONE,
        server_onupdate=func.now(),
        comment="Обновлена",
        onupdate=partial(datetime.now, tz=timezone.utc),
    )
    complete_before: Mapped[datetime | None] = mapped_column(DATETIME_TIMEZONE, comment="Выполнить до")
    completed_at: Mapped[datetime | None] = mapped_column(DATETIME_TIMEZONE, comment="Выполнена")

    user: Mapped["User"] = relationship(back_populates="tasks")
    task_status: Mapped["TaskStatus"] = relationship(back_populates="tasks")

    @validates("title")
    def validate_title(self, key: str, title: str) -> str:
        """Валидация заголовка задачи."""
        if len(title) > 255:
            raise ValueError("Длинна заголовка задачи не может превышать 255 символов")
        if len(title) < 5:
            raise ValueError("Длинна заголовка задачи не может быть меньше 5 символов")
        return title
