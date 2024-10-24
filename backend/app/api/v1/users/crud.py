from sqlalchemy import select, Result
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.v1.users.schemas import CreateUser
from app.db.models import User


async def create_user(session: AsyncSession, new_user_data: CreateUser) -> User:
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


async def get_user_by_email(session: AsyncSession, email: str) -> User:
    """Получает пользователя по его email."""
    stmt = select(User).where(User.email == email)
    results: Result = await session.execute(stmt)
    return results.scalar()
