from typing import Annotated

from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.v1.users.crud import get_user_by_email
from app.api.v1.users.schemas import UserLogin
from app.db import db_helper
from app.db.models import User


async def auth_user(
    user_credentials: UserLogin, session: Annotated[AsyncSession, Depends(db_helper.get_session)]
) -> User:
    """Возвращает авторизованного пользователя."""
    user = await get_user_by_email(session, user_credentials.email)
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect email or password")
    if not user.verify_password(user_credentials.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect email or password")
    return user
