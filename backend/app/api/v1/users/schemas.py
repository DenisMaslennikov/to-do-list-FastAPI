from uuid import UUID

from pydantic import BaseModel, EmailStr, Field


class UserLogin(BaseModel):
    """Сериализатор для логина пользователя."""

    email: EmailStr = Field(..., examples=["username@example.com"])
    password: str = Field(..., examples=["password"])


class BaseUser(BaseModel):
    """Базовая модель пользователя."""

    email: EmailStr = Field(..., examples=["username@example.com"])
    username: str = Field(..., examples=["username"])
    first_name: str | None = Field(None, examples=["Иван"])
    second_name: str | None = Field(None, examples=["Шпак"])
    middle_name: str | None = Field(None, examples=["Васильевич"])


class CreateUser(BaseUser):
    """Сериализатор создания пользователя."""

    password: str = Field(..., examples=["password"], min_length=8)


class UpdateUser(BaseUser):
    """Сериализатор полного обновления пользователя."""

    password: str = Field(..., examples=["password"], min_length=8)


class PartialUpdateUser(BaseUser):
    email: EmailStr | None = Field(None, examples=["username@example.com"])
    username: str | None = Field(None, examples=["username"])


class ReadUser(BaseUser):
    """Сериализатор пользователя для операций чтения."""

    id: UUID


class JWTTokensPairBase(BaseModel):
    """Пара из refresh и access токенов."""

    access_token: str
    refresh_token: str


class JWTTokensPairWithTokenType(JWTTokensPairBase):
    """Пара из refresh и access токенов с указанием типа токенов."""

    access_token: str
    refresh_token: str
    token_type: str = "Bearer"


class JWTTokenForValidation(BaseModel):
    """Токен для валидации."""

    token: str


class RefreshToken(BaseModel):
    """Refresh токен."""

    refresh_token: str


class TokenValidationResult(BaseModel):
    """Результат валидации токена."""

    validation_result: bool
