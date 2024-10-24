from uuid import UUID

from fastapi import HTTPException, status

from app.api.v1.auth.jwt import decode_token
from app.api.v1.users.schemas import RefreshToken


def user_id_from_refresh_token(token: RefreshToken) -> UUID:
    """Получает user_id из refresh токена."""
    payload = decode_token(token.refresh_token)
    if payload.get("token_type") != "refresh":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token type must be 'refresh'")
    return UUID(payload["sub"])
