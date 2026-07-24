"""
Base class for all SQLAlchemy models.
Every database model should inherit from Base.
"""

from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass