from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.v1.auth.jwt import create_refresh_token, create_access_token
from app.api.v1.dependencies.users import auth_user
from app.api.v1.users import crud
from app.api.v1.users.schemas import UserLogin, CreateUser, ReadUser, JWTTokensPair
from app.db import db_helper
from app.db.models import User

router = APIRouter(tags=["Users"])


@router.post("/jwt/create/", response_model=JWTTokensPair)
async def user_login(user: Annotated[User, Depends(auth_user)]) -> dict[str, str]:
    """Логин пользователя для получения JWT токенов."""
    return {
        "access_token": create_access_token(user.id),
        "refresh_token": create_refresh_token(user.id),
    }


@router.post("/register/", response_model=ReadUser)
async def user_register(
    new_user_data: CreateUser, session: Annotated[AsyncSession, Depends(db_helper.get_session)]
) -> User:
    """Создание нового пользователя."""
    user = await crud.create_user(session=session, new_user_data=new_user_data)
    return user
