"""
Module for SQLAlchemy and Pydantic models for the application user.

This module defines the SQLAlchemy ORM model for an application user and a corresponding
Pydantic model for serializing user responses.
"""

from sqlalchemy import Column, Integer, String
from db_api.db.database import Base
from pydantic import BaseModel


class AppUser(Base):
    """SQLAlchemy model representing a user in the application.

    Attributes:
        __tablename__ (str): Name of the database table.
        user_id (int): Primary key for the user record.
        sub (str): Unique subject identifier for the user.
        email (str): Unique email address of the user.
    """
    __tablename__ = "app_users"
    user_id: int = Column(Integer, primary_key=True, index=True)
    sub: str = Column(String, unique=True, nullable=False)
    email: str = Column(String, unique=True, nullable=False)


class UserResponse(BaseModel):
    """Pydantic model for serializing user response data.

    Attributes:
        sub (str): Unique subject identifier for the user.
        email (str): Email address of the user.
    """
    sub: str
    email: str

    class Config:
        """Pydantic configuration to enable ORM mode.

        This configuration allows Pydantic to work seamlessly with SQLAlchemy ORM objects.
        """
        orm_mode = True
