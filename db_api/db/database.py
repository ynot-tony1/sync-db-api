"""
Database module for establishing the connection and session management.

This module creates the SQLAlchemy engine and session factory, and
provides a dependency function for obtaining a new database session.
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from typing import Generator
from db_api.config.settings import settings
from db_api.db.base import Base

# Create the SQLAlchemy engine using the application database URL.
engine = create_engine(settings.app_database_url)

# SessionLocal is a factory that creates new SQLAlchemy Session objects.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db() -> Generator[Session, None, None]:
    """Create a new database session for a request.

    Yields:
        Session: A new SQLAlchemy session instance.
    """
    db: Session = SessionLocal()
    try:
        yield db
    finally:
        db.close()
