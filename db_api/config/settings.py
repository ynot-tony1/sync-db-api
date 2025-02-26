"""
Application settings configuration using Pydantic.

This module loads environment variables using python-dotenv and defines a
Pydantic settings class to hold configuration variables for the application.

Attributes:
    APP_DATABASE_URL (str): The URL for connecting to the database.
    JWT_SECRET (str): The secret key for encoding/decoding JWT tokens.
    ACCESS_TOKEN_EXPIRE_MINUTES (int): Number of minutes before an access token expires.
"""

import os
from dotenv import load_dotenv, find_dotenv
from pydantic_settings import BaseSettings  # Updated import for Pydantic v2.5+

# Load environment variables from a .env file.
load_dotenv(find_dotenv())

class Settings(BaseSettings):
    """Pydantic settings for the application."""
    app_database_url: str
    jwt_secret: str
    access_token_expire_minutes: int

    class Config:
        """
        Pydantic configuration for the settings class.

        The env_file is set to the location found by `find_dotenv()` (or defaults to ".env")
        to ensure environment variables are loaded.
        """
        env_file = find_dotenv() or ".env"

# Instantiate settings.
settings: Settings = Settings()

# Define module-level variables with type annotations.
APP_DATABASE_URL: str = settings.app_database_url
JWT_SECRET: str = settings.jwt_secret
ACCESS_TOKEN_EXPIRE_MINUTES: int = settings.access_token_expire_minutes
