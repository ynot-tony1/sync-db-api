"""
This module outlines the AppUser model for the app database.

The AppUser model uses SQLAlchemy’s declarative Base to represent a record in the
'app_user' table. It includes a pk 'user_id', a unique sub identifier, and a unique email address.

Classes:
    AppUser: Represents a user record in the "app_users" table with columns for user_id, sub, and email.
"""

from sqlalchemy import Column, Integer, String
from db_api.db.database import Base

class AppUser(Base):
    __tablename__ = "app_users"
    user_id = Column(Integer, primary_key=True, index=True)
    sub = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
