from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.v1.auth.jwt import create_refresh_token, create_access_token, decode_token
from app.api.v1.dependencies.jwt import user_id_from_refresh_token
from app.api.v1.dependencies.users import auth_user, get_current_user
from app.api.v1.users import crud
from app.api.v1.users.schemas import (
    CreateUser,
    ReadUser,
    JWTTokensPairWithTokenType,
    TokenValidationResult,
    JWTTokenForValidation,
    UpdateUser,
    PartialUpdateUser,
)
from app.constants import DEFAULT_RESPONSES
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
        status.HTTP_400_BAD_REQUEST: {"description": "Пользователь с таким username или email уже зарегистрирован"},
    },
)
async def user_register(
    new_user_data: CreateUser, session: Annotated[AsyncSession, Depends(db_helper.get_session)]
) -> User:
    """Создание нового пользователя."""
    user_from_bd = await crud.get_user_by_email_or_username_repo(session, new_user_data.email, new_user_data.username)
    if user_from_bd is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Пользователь с таким email или username ужк зарегистрирован",
        )
    user = await crud.create_user_repo(session=session, new_user_data=new_user_data)
    return user


@router.get(
    "/me/",
    response_model=ReadUser,
    responses=DEFAULT_RESPONSES,
)
async def get_user_me(user: Annotated[User, Depends(get_current_user)]) -> User:
    """Получает информацию о текущем пользователе."""
    return user


@router.delete(
    "/me/",
    status_code=status.HTTP_204_NO_CONTENT,
    response_description="Пользователь удален",
    responses=DEFAULT_RESPONSES,
)
async def delete_user_me(
    user: Annotated[User, Depends(get_current_user)],
    session: Annotated[AsyncSession, Depends(db_helper.get_session)],
) -> None:
    """Удаляет текущего пользователя."""
    await crud.delete_user_repo(session, user)


@router.put(
    "/me/",
    response_model=ReadUser,
    responses={
        status.HTTP_400_BAD_REQUEST: {"description": "Такой email или username уже есть в базе"},
    }
    | DEFAULT_RESPONSES,
)
async def update_user_me(
    new_user_data: UpdateUser,
    user: Annotated[User, Depends(get_current_user)],
    session: Annotated[AsyncSession, Depends(db_helper.get_session)],
) -> User:
    """Полное обновление информации о пользователе."""
    user_from_bd = await crud.get_user_by_email_or_username_repo(
        session,
        new_user_data.email,
        new_user_data.username,
        exclude_user_id=user.id,
    )
    if user_from_bd is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Пользователь с таким email или username ужк зарегистрирован",
        )
    user = await crud.update_user_repo(session, user, new_user_data)
    return user


@router.patch(
    "/me/",
    response_model=ReadUser,
    responses={
        status.HTTP_400_BAD_REQUEST: {"description": "Такой email или username уже есть в базе"},
    }
    | DEFAULT_RESPONSES,
)
async def partial_update_user_me(
    new_user_data: PartialUpdateUser,
    user: Annotated[User, Depends(get_current_user)],
    session: Annotated[AsyncSession, Depends(db_helper.get_session)],
) -> User:
    """Частичное обновление информации о пользователе."""
    user_from_bd = await crud.get_user_by_email_or_username_repo(
        session,
        new_user_data.email,
        new_user_data.username,
        exclude_user_id=user.id,
    )
    if user_from_bd is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Пользователь с таким email или username ужк зарегистрирован",
        )
    user = await crud.update_user_repo(session, user, new_user_data, partial=True)
    return user
