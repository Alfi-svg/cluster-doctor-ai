"""
Authentication Schemas
"""

from pydantic import BaseModel, ConfigDict, EmailStr

from app.schemas.user import UserResponse


# ==========================================================
# Login Request
# ==========================================================

class LoginRequest(BaseModel):
    """
    User login request.
    """

    email: EmailStr
    password: str


# ==========================================================
# Access Token
# ==========================================================

class Token(BaseModel):
    """
    JWT token pair.
    """

    access_token: str
    refresh_token: str
    token_type: str = "bearer"


# ==========================================================
# Login Response
# ==========================================================

class LoginResponse(BaseModel):
    """
    Login response.
    """

    model_config = ConfigDict(from_attributes=True)

    user: UserResponse
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


# ==========================================================
# Refresh Token Request
# ==========================================================

class RefreshTokenRequest(BaseModel):
    """
    Refresh access token.
    """

    refresh_token: str


# ==========================================================
# Refresh Token Response
# ==========================================================

class RefreshTokenResponse(BaseModel):
    """
    New access token response.
    """

    access_token: str
    token_type: str = "bearer"