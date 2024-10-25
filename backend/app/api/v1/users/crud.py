from typing import Any
from uuid import UUID

from sqlalchemy import select, Result, or_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload
from sqlalchemy.orm.strategy_options import _AbstractLoad
from sqlalchemy.util import await_only

from app.api.v1.users.schemas import CreateUser
from app.db.models import User


async def create_user_repo(session: AsyncSession, new_user_data: CreateUser) -> User:
    """Создание нового пользователя."""
    user = User(
        email=new_user_data.email,
        first_name=new_user_data.first_name,
        second_name=new_user_data.second_name,
        middle_name=new_user_data.middle_name,
        username=new_user_data.username,
    )
    user.password = new_user_data.password
    session.add(user)
    await session.commit()
    return user


async def get_user_by_email_repo(session: AsyncSession, email: str, *option: list[_AbstractLoad]) -> User | None:
    """Получает пользователя по его email."""
    stmt = select(User).where(User.email == email)
    if option:
        stmt = stmt.options(*option)
    results: Result = await session.execute(stmt)
    return results.scalar()


async def get_user_by_email_or_username_repo(
    session: AsyncSession, email: str, username: str, *option: list[_AbstractLoad]
) -> User | None:
    """Получает пользователя по его email или username."""
    stmt = select(User).where(or_(User.email == email, User.username == username))
    if option:
        stmt = stmt.options(*option)
    results: Result = await session.execute(stmt)
    return results.scalars().first()


async def get_user_by_id_repo(session: AsyncSession, user_id: UUID, *option: list[_AbstractLoad]) -> User | None:
    """Возвращает пользователя с заданным id."""
    stmt = select(User).where(User.id == user_id)
    if option:
        stmt = stmt.options(*option)
    results: Result = await session.execute(stmt)
    return results.scalar()


async def delete_user_repo(session: AsyncSession, user: User) -> None:
    """Удаляет пользователя из базы."""
    await session.delete(user)
    await session.commit()
