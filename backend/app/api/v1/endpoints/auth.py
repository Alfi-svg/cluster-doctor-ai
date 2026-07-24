"""
Authentication Endpoints
"""

from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi import status

from sqlalchemy.ext.asyncio import AsyncSession

from app.api.dependencies import (
    get_current_active_user,
    get_database,
)

from app.controllers.auth_controller import auth_controller

from app.models.user import User

from app.schemas.auth import (
    LoginRequest,
    LoginResponse,
    RefreshTokenRequest,
    RefreshTokenResponse,
)

from app.schemas.user import (
    UserCreate,
    UserResponse,
)

router = APIRouter()


# =====================================================
# Register
# =====================================================

@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
)
async def register(
    user: UserCreate,
    db: AsyncSession = Depends(get_database),
):

    try:
        return await auth_controller.register(
            db=db,
            user=user,
        )

    except ValueError as e:

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )


# =====================================================
# Login
# =====================================================

@router.post(
    "/login",
    response_model=LoginResponse,
)
async def login(
    credentials: LoginRequest,
    db: AsyncSession = Depends(get_database),
):

    try:
        return await auth_controller.login(
            db=db,
            credentials=credentials,
        )

    except ValueError as e:

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e),
        )


# =====================================================
# Current User
# =====================================================

@router.get(
    "/me",
    response_model=UserResponse,
)
async def me(
    current_user: User = Depends(
        get_current_active_user
    ),
):
    return current_user


# =====================================================
# Refresh Token
# =====================================================

@router.post(
    "/refresh",
    response_model=RefreshTokenResponse,
)
async def refresh(
    request: RefreshTokenRequest,
):

    try:
        return await auth_controller.refresh_token(
            request,
        )

    except ValueError as e:

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e),
        )


# =====================================================
# Logout
# =====================================================

@router.post("/logout")
async def logout():

    """
    Stateless JWT logout.

    Future:
    - Redis blacklist
    - Refresh token revocation
    """

    return {
        "message": "Logged out successfully."
    }