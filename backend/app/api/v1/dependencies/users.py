from typing import Annotated
from uuid import UUID

from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.util import await_only

from app.api.v1.dependencies.jwt import get_current_user_id
from app.api.v1.users import crud
from app.api.v1.users.crud import get_user_by_email_repo, get_user_by_id_repo
from app.api.v1.users.schemas import UserLogin
from app.db import db_helper
from app.db.models import User


async def auth_user(
    user_credentials: UserLogin, session: Annotated[AsyncSession, Depends(db_helper.get_session)]
) -> User:
    """Возвращает авторизованного пользователя."""
    user = await crud.get_user_by_email_repo(session, user_credentials.email)
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect email or password")
    if not user.verify_password(user_credentials.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect email or password")
    return user


async def get_current_user(
    user_id: Annotated[UUID, Depends(get_current_user_id)],
    session: Annotated[AsyncSession, Depends(db_helper.get_session)],
) -> User:
    """Получает текущего пользователя."""
    user = await crud.get_user_by_id_repo(session, user_id=user_id)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user
