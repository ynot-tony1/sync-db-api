"""
Database module for establishing the connection and session management.

This module creates the SQLAlchemy engine and session factory, and
provides a dependency function for obtaining a new database session.
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from typing import Generator
from db_api.config.type_settings import APP_DATABASE_URL
from db_api.db.base import Base

engine = create_engine(APP_DATABASE_URL)
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
