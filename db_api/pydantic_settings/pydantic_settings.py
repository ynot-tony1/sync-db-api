"""
Pydantic settings configuration.

This module loads environment variables using python-dotenv and defines a
Pydantic settings class to hold configuration variables for the application.

Attributes:
    app_database_url (str): The URL for connecting to the database.
    jwt_secret (str): The secret key for encoding/decoding JWT tokens.
    access_token_expire_minutes (int): Number of minutes before an access token expires.
"""

from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    """Pydantic settings for the application."""
    app_database_url: str
    jwt_secret: str
    access_token_expire_minutes: int

settings: Settings = Settings()
