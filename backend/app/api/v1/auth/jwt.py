from datetime import timedelta, datetime, timezone
from uuid import UUID

import jwt
from cryptography.hazmat.primitives.asymmetric.ec import EllipticCurvePrivateKey
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
from cryptography.hazmat.primitives.asymmetric.ed448 import Ed448PrivateKey
from cryptography.hazmat.primitives.asymmetric.rsa import RSAPrivateKey

from app import settings


def _create_token(
    payload: dict[str, str],
    secret: RSAPrivateKey | EllipticCurvePrivateKey | Ed25519PrivateKey | Ed448PrivateKey | str | bytes,
    algorithm: str,
) -> str:
    """Создание токена."""
    return jwt.encode(
        payload=payload,
        key=secret,
        algorithm=algorithm,
    )


def create_access_token(user_id: UUID) -> str:
    """Создает access token."""
    return _create_token(
        payload={
            "sub": str(user_id),
            "token_type": "access",
            "iat": datetime.now(timezone.utc),
            "exp": datetime.now(timezone.utc) + settings.jwt.access_token_expires_delta
        },
        secret=settings.jwt.private_key_path.read_text(encoding="utf-8"),
        algorithm=settings.jwt.jwt_algorithm,
    )


def create_refresh_token(user_id: UUID) -> str:
    """Создает refresh token."""
    return _create_token(
        payload={
            "sub": str(user_id),
            "token_type": "refresh",
            "iat": datetime.now(timezone.utc),
            "exp": datetime.now(timezone.utc) + settings.jwt.refresh_token_expires_delta,
        },
        secret=settings.jwt.private_key_path.read_text(encoding="utf-8"),
        algorithm=settings.jwt.jwt_algorithm,
    )
