"""
Security Utilities

Handles:
- Password Hashing
- Password Verification
- JWT Access Tokens
- JWT Refresh Tokens
- JWT Decoding
"""

from datetime import datetime, timedelta, timezone
from typing import Any

from jose import JWTError, jwt
from passlib.context import CryptContext

from app.core.config import settings

# ==========================================================
# Password Hashing
# ==========================================================

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto",
)

# ==========================================================
# Password Functions
# ==========================================================


def verify_password(
    plain_password: str,
    hashed_password: str,
) -> bool:
    """
    Verify a plain password against its hash.
    """
    return pwd_context.verify(
        plain_password,
        hashed_password,
    )


def get_password_hash(
    password: str,
) -> str:
    """
    Hash a password.
    """
    return pwd_context.hash(password)


# Backward compatibility
hash_password = get_password_hash

# ==========================================================
# JWT Configuration
# ==========================================================

REFRESH_TOKEN_EXPIRE_DAYS = 7

# ==========================================================
# Access Token
# ==========================================================


def create_access_token(
    subject: str | int,
    expires_delta: timedelta | None = None,
) -> str:
    """
    Create JWT access token.
    """

    if expires_delta is None:
        expires_delta = timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )

    expire = datetime.now(timezone.utc) + expires_delta

    payload = {
        "sub": str(subject),
        "type": "access",
        "exp": expire,
        "iat": datetime.now(timezone.utc),
    }

    return jwt.encode(
        payload,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM,
    )


# ==========================================================
# Refresh Token
# ==========================================================


def create_refresh_token(
    subject: str | int,
) -> str:
    """
    Create JWT refresh token.
    """

    expire = datetime.now(timezone.utc) + timedelta(
        days=REFRESH_TOKEN_EXPIRE_DAYS
    )

    payload = {
        "sub": str(subject),
        "type": "refresh",
        "exp": expire,
        "iat": datetime.now(timezone.utc),
    }

    return jwt.encode(
        payload,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM,
    )


# ==========================================================
# Decode Token
# ==========================================================


def decode_token(
    token: str,
) -> dict[str, Any]:
    """
    Decode JWT token.

    Raises JWTError if invalid.
    """

    return jwt.decode(
        token,
        settings.SECRET_KEY,
        algorithms=[settings.ALGORITHM],
    )


# ==========================================================
# Verify Access Token
# ==========================================================


def verify_access_token(
    token: str,
) -> dict[str, Any]:
    """
    Verify access token.
    """

    payload = decode_token(token)

    if payload.get("type") != "access":
        raise JWTError("Invalid access token")

    return payload


# ==========================================================
# Verify Refresh Token
# ==========================================================


def verify_refresh_token(
    token: str,
) -> dict[str, Any]:
    """
    Verify refresh token.
    """

    payload = decode_token(token)

    if payload.get("type") != "refresh":
        raise JWTError("Invalid refresh token")

    return payload