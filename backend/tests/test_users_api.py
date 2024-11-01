from http.client import responses
from pprint import pprint
from uuid import UUID

import pytest
from fastapi import status

from app.api.v1.auth.jwt import decode_token


async def test_create_jwt(user_one, client, user_one_password):
    """Проверяет получение пары из refresh и access токенов."""
    response = await client.post(
        "/api/v1/users/jwt/create/",
        json={
            "email": user_one.email,
            "password": user_one_password,
        },
    )

    response_json = response.json()

    pprint(response_json)

    assert response.status_code == status.HTTP_201_CREATED, "Получен код ответа отличный от ожидаемого"
    assert "access_token" in response_json, "В ответе не найден access токен"
    assert "refresh_token" in response_json, "В ответе не найден refresh токен"
    access_payload = decode_token(response_json["access_token"])
    refresh_payload = decode_token(response_json["refresh_token"])
    assert UUID(access_payload["sub"]) == user_one.id, "ID пользователя в access токене не совпадает"
    assert UUID(refresh_payload["sub"]) == user_one.id, "ID пользователя в refresh токене не совпадает"
    assert access_payload["token_type"] == "access", "Тип токена не правильный"
    assert refresh_payload["token_type"] == "refresh", "Тип токена не правильный"
