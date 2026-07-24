"""
Authentication Controller
"""

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User

from app.schemas.auth import (
    LoginRequest,
    RefreshTokenRequest,
)

from app.schemas.user import UserCreate

from app.services.auth_service import auth_service


class AuthController:
    """
    Authentication Controller.

    Thin layer between API and Service.
    """

    # =====================================================
    # Register
    # =====================================================

    async def register(
        self,
        db: AsyncSession,
        user: UserCreate,
    ) -> User:

        return await auth_service.register(
            db=db,
            user=user,
        )

    # =====================================================
    # Login
    # =====================================================

    async def login(
        self,
        db: AsyncSession,
        credentials: LoginRequest,
    ) -> dict:

        return await auth_service.login(
            db=db,
            credentials=credentials,
        )

    # =====================================================
    # Refresh Token
    # =====================================================

    async def refresh_token(
        self,
        request: RefreshTokenRequest,
    ) -> dict:

        return await auth_service.refresh_token(
            request=request,
        )


auth_controller = AuthController()