from pydantic import BaseModel, EmailStr, Field


class UserLogin(BaseModel):
    """Сериализатор для логина пользователя."""

    email: EmailStr = Field(..., examples=["username@example.com"])
    password: str = Field(..., examples=["password"])


class BaseUser(BaseModel):
    """Базовая модель пользователя."""

    email: EmailStr = Field(
        ...,
        examples=["username@example.com"],
    )
    username: str = Field(..., examples=["username"])
    first_name: str | None = Field(None, examples=["Иван"])
    second_name: str | None = Field(None, examples=["Шпак"])
    middle_name: str | None = Field(None, examples=["Васильевич"])


class CreateUser(BaseUser):
    """Сериализатор создания пользователя."""

    password: str = Field(..., examples=["password"], max_length=8)


class ReadUser(BaseUser):
    """Сериализатор пользователя для операций чтения."""

    pass