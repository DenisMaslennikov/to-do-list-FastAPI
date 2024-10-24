from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.v1.auth.jwt import create_refresh_token, create_access_token
from app.api.v1.dependencies.jwt import user_id_from_refresh_token
from app.api.v1.dependencies.users import auth_user
from app.api.v1.users import crud
from app.api.v1.users.schemas import UserLogin, CreateUser, ReadUser, JWTTokensPairWithTokenType
from app.db import db_helper
from app.db.models import User

router = APIRouter(tags=["Users"])


@router.post("/jwt/create/")
async def create_tokens(user: Annotated[User, Depends(auth_user)]) -> JWTTokensPairWithTokenType:
    """Логин пользователя для получения JWT токенов."""
    return JWTTokensPairWithTokenType(
        access_token=create_access_token(user.id),
        refresh_token=create_refresh_token(user.id),
    )


@router.post("/jwt/refresh/")
async def tokens_refresh(user_id: Annotated[UUID, Depends(user_id_from_refresh_token)]) -> JWTTokensPairWithTokenType:
    """Обновление токенов по refresh токену."""
    return JWTTokensPairWithTokenType(
        access_token=create_access_token(user_id),
        refresh_token=create_refresh_token(user_id),
    )


@router.post("/register/", response_model=ReadUser)
async def user_register(
    new_user_data: CreateUser, session: Annotated[AsyncSession, Depends(db_helper.get_session)]
) -> User:
    """Создание нового пользователя."""
    user = await crud.create_user(session=session, new_user_data=new_user_data)
    return user
