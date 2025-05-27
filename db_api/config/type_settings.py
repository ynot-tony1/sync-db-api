"""
Type-validated settings for the Auth Service using Pydantic.

This module imports raw environment variables from settings.py and then
defines a Pydantic settings class that validates these values. This provides
an extra layer of type safety for critical configuration values.

"""

from pydantic_settings import BaseSettings
from db_api.config.settings import APP_DATABASE_URL, JWT_SECRET, ACCESS_TOKEN_EXPIRE_MINUTES

class TypeSettings(BaseSettings):
    """Pydantic settings for type-validated configuration."""
    auth_database_url: str = APP_DATABASE_URL
    jwt_secret: str = JWT_SECRET
    token_expire_mins: int = int(ACCESS_TOKEN_EXPIRE_MINUTES) if ACCESS_TOKEN_EXPIRE_MINUTES is not None else 30

type_settings: TypeSettings = TypeSettings()

AUTH_DATABASE_URL: str = type_settings.auth_database_url
JWT_SECRET: str = type_settings.jwt_secret
TOKEN_EXPIRE_MINS: int = type_settings.token_expire_mins
