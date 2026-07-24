"""
Common API Dependencies
"""

from fastapi import Depends
from fastapi import HTTPException
from fastapi import status
from fastapi.security import OAuth2PasswordBearer

from jose import JWTError

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import verify_access_token
from app.database.session import get_db
from app.models.user import User
from app.repositories.user_repository import user_repository

# ==========================================================
# OAuth2
# ==========================================================

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/api/v1/login",
)

# ==========================================================
# Database Dependency
# ==========================================================


async def get_database():
    """
    Returns AsyncSession.
    """

    async for db in get_db():
        yield db


# ==========================================================
# Current User
# ==========================================================


async def get_current_user(
    db: AsyncSession = Depends(get_database),
    token: str = Depends(oauth2_scheme),
) -> User:

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials.",
        headers={
            "WWW-Authenticate": "Bearer",
        },
    )

    try:

        payload = verify_access_token(token)

        user_id = payload.get("sub")

        if user_id is None:
            raise credentials_exception

    except JWTError:
        raise credentials_exception

    user = await user_repository.get(
        db,
        int(user_id),
    )

    if user is None:
        raise credentials_exception

    return user


# ==========================================================
# Active User
# ==========================================================


async def get_current_active_user(
    current_user: User = Depends(get_current_user),
) -> User:

    if not current_user.is_active:

        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Inactive account.",
        )

    return current_user


# ==========================================================
# Super User
# ==========================================================


async def get_current_admin(
    current_user: User = Depends(get_current_active_user),
) -> User:

    if not current_user.is_superuser:

        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Administrator privileges required.",
        )

    return current_user