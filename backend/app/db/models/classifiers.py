from typing import TYPE_CHECKING

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.models.base import Base
from app.db.models.mixins import IntPrimaryKey

if TYPE_CHECKING:
    from app.db.models import Task


class TaskStatus(IntPrimaryKey, Base):
    """Модель статуса задачи."""

    __tablename__ = "cl_task_status"
    name: Mapped[str] = mapped_column(String(50), comment="Наименование статуса")

    tasks: Mapped[list["Task"]] = relationship(back_populates="task_status")
