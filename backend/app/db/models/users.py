from typing import TYPE_CHECKING
from uuid import UUID

from passlib.context import CryptContext
from sqlalchemy import String, text
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import Mapped, mapped_column, relationship, validates

from app.constants import EMAIL_REGEX
from app.db.models.base import Base

if TYPE_CHECKING:
    from app.db.models import Task

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class User(Base):
    """Модель пользователя."""

    __tablename__ = "users"
    id: Mapped[UUID] = mapped_column(
        primary_key=True,
        server_default=text("gen_random_uuid()"),
        comment="Идентификатор",
    )
    email: Mapped[str] = mapped_column(String(100), index=True, comment="Почта", unique=True)
    first_name: Mapped[str | None] = mapped_column(String(100), comment="Имя")
    second_name: Mapped[str | None] = mapped_column(String(100), comment="Фамилия")
    middle_name: Mapped[str | None] = mapped_column(String(100), comment="Отчество")
    username: Mapped[str] = mapped_column(String(100), index=True, comment="Имя пользователя", unique=True)
    _password_hash: Mapped[str] = mapped_column(comment="Хеш пароля")

    tasks: Mapped[list["Task"]] = relationship(back_populates="user")

    @validates("email")
    def validate_email(self, key: str, email: str) -> str:
        """Валидирует email."""
        if not EMAIL_REGEX.match(email):
            raise ValueError("Некорректный email")
        if len(email) > 100:
            raise ValueError("максимальная длинна email 100 символов")
        return email

    @hybrid_property
    def password(self):
        """Hybrid property для пароля."""
        raise AttributeError("Атрибут пароль нельзя читать напрямую.")

    @password.setter
    def password(self, plain_password: str) -> None:
        """Сеттер пароля."""
        self._password_hash = self._generate_password_hash(plain_password)

    def _generate_password_hash(self, plain_password: str) -> str:
        """Генерация хеша пароля с использованием bcrypt."""
        return pwd_context.hash(plain_password)

    def verify_password(self, plain_password: str) -> bool:
        """Проверка пароля через сравнение хеша."""
        return pwd_context.verify(plain_password, self._password_hash)
