"""
Base module for SQLAlchemy models.

This module defines the Base class, which is used as the
declarative base for all SQLAlchemy models in the application.
"""

from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
