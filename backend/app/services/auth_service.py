"""
Authentication Service

Handles:
- User Registration
- User Login
- Refresh Token
"""

from jose import JWTError
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import (
    create_access_token,
    create_refresh_token,
    get_password_hash,
    verify_password,
    verify_refresh_token,
)

from app.models.user import User

from app.repositories.user_repository import user_repository

from app.schemas.auth import (
    LoginRequest,
    RefreshTokenRequest,
)

from app.schemas.user import UserCreate


class AuthService:
    """
    Authentication Service.
    """

    # =====================================================
    # Register
    # =====================================================

    async def register(
        self,
        db: AsyncSession,
        user: UserCreate,
    ) -> User:

        existing = await user_repository.get_by_email(
            db,
            user.email,
        )

        if existing:
            raise ValueError(
                "Email already registered."
            )

        new_user = await user_repository.create(
            db=db,
            full_name=user.full_name,
            email=user.email,
            password_hash=get_password_hash(
                user.password
            ),
        )

        return new_user

    # =====================================================
    # Login
    # =====================================================

    async def login(
        self,
        db: AsyncSession,
        credentials: LoginRequest,
    ) -> dict:

        user = await user_repository.get_by_email(
            db,
            credentials.email,
        )

        if user is None:
            raise ValueError(
                "Invalid email or password."
            )

        if not verify_password(
            credentials.password,
            user.password_hash,
        ):
            raise ValueError(
                "Invalid email or password."
            )

        access_token = create_access_token(
            subject=user.id,
        )

        refresh_token = create_refresh_token(
            subject=user.id,
        )

        return {
            "user": user,
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer",
        }

    # =====================================================
    # Refresh Access Token
    # =====================================================

    async def refresh_token(
        self,
        request: RefreshTokenRequest,
    ) -> dict:

        try:

            payload = verify_refresh_token(
                request.refresh_token
            )

        except JWTError:

            raise ValueError(
                "Invalid refresh token."
            )

        user_id = payload.get("sub")

        access_token = create_access_token(
            subject=user_id,
        )

        return {
            "access_token": access_token,
            "token_type": "bearer",
        }


auth_service = AuthService()