"""
Database session configuration.
"""

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from app.core.config import settings

db_url = settings.DATABASE_URL

if db_url.startswith("postgresql://"):
    db_url = db_url.replace(
        "postgresql://",
        "postgresql+asyncpg://",
        1,
    )

engine = create_async_engine(
    db_url,
    echo=settings.DEBUG,
    future=True,
)

SessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    autocommit=False,
    autoflush=False,
    expire_on_commit=False,   # ⭐ IMPORTANT FIX
)


async def get_db():
    """
    Dependency that provides a database session.
    """
    async with SessionLocal() as db:
        yield db