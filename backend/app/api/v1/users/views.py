from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.v1.users import crud
from app.api.v1.users.schemas import UserLogin, CreateUser, ReadUser
from app.db import db_helper
from app.db.models import User

router = APIRouter(tags=["Users"])


@router.post(
    "/login/",
)
async def user_login(user_credentials: UserLogin):
    """Логин пользователя для получения JWT токенов."""
    print(user_credentials.model_dump())


@router.post("/register/", response_model=ReadUser)
async def user_register(
    new_user_data: CreateUser, session: Annotated[AsyncSession, Depends(db_helper.get_session)]
) -> User:
    """Создание нового пользователя."""
    user = await crud.create_user(session=session, new_user_data=new_user_data)
    return user
