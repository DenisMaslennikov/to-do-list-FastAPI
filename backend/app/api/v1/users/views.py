from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status
from starlette.status import HTTP_404_NOT_FOUND

from app.api.v1.auth.jwt import create_refresh_token, create_access_token, decode_token
from app.api.v1.dependencies.jwt import user_id_from_refresh_token
from app.api.v1.dependencies.users import auth_user, get_current_user
from app.api.v1.users import crud
from app.api.v1.users.crud import delete_user_repo
from app.api.v1.users.schemas import (
    UserLogin,
    CreateUser,
    ReadUser,
    JWTTokensPairWithTokenType,
    TokenValidationResult,
    JWTTokenForValidation,
)
from app.db import db_helper
from app.db.models import User

router = APIRouter(tags=["Users"])


@router.post(
    "/jwt/create/",
    responses={status.HTTP_401_UNAUTHORIZED: {"description": "Ошибка авторизации"}},
)
async def create_tokens(user: Annotated[User, Depends(auth_user)]) -> JWTTokensPairWithTokenType:
    """Логин пользователя для получения JWT токенов."""
    return JWTTokensPairWithTokenType(
        access_token=create_access_token(user.id),
        refresh_token=create_refresh_token(user.id),
    )


@router.post(
    "/jwt/refresh/",
    responses={status.HTTP_401_UNAUTHORIZED: {"description": "Некорректный refresh токен"}},
)
async def tokens_refresh(user_id: Annotated[UUID, Depends(user_id_from_refresh_token)]) -> JWTTokensPairWithTokenType:
    """Обновление токенов по refresh токену."""
    return JWTTokensPairWithTokenType(
        access_token=create_access_token(user_id),
        refresh_token=create_refresh_token(user_id),
    )


@router.post("/jwt/validate/")
async def token_validate(token: JWTTokenForValidation) -> TokenValidationResult:
    """Валидирует токен."""
    try:
        decode_token(token.token)
    except:
        return TokenValidationResult(validation_result=False)
    else:
        return TokenValidationResult(validation_result=True)


@router.post(
    "/register/",
    response_model=ReadUser,
    responses={
        status.HTTP_400_BAD_REQUEST: {"description": "Пользователь с таким Username или Email уже зарегистрирован"},
    },
)
async def user_register(
    new_user_data: CreateUser, session: Annotated[AsyncSession, Depends(db_helper.get_session)]
) -> User:
    """Создание нового пользователя."""
    user_from_bd = await crud.get_user_by_email_or_username_repo(session, new_user_data.email, new_user_data.username)
    if user_from_bd is not None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email or Username already registered")
    user = await crud.create_user_repo(session=session, new_user_data=new_user_data)
    return user


@router.get(
    "/me/",
    response_model=ReadUser,
    responses={
        status.HTTP_404_NOT_FOUND: {"description": "Пользователь не найден в базе данных"},
        status.HTTP_401_UNAUTHORIZED: {"description": "Ошибка авторизации"},
    },
)
async def get_user_me(user: Annotated[User, Depends(get_current_user)]) -> User:
    """Получает информацию о текущем пользователе."""
    return user


@router.delete(
    "/me/",
    status_code=status.HTTP_204_NO_CONTENT,
    response_description="Пользователь удален",
    responses={
        status.HTTP_404_NOT_FOUND: {"description": "Пользователь не найден в базе данных"},
        status.HTTP_401_UNAUTHORIZED: {"description": "Ошибка авторизации"},
    },
)
async def delete_user_me(
    user: Annotated[User, Depends(get_current_user)],
    session: Annotated[AsyncSession, Depends(db_helper.get_session)],
) -> None:
    """Удаляет текущего пользователя."""
    await crud.delete_user_repo(session, user)
