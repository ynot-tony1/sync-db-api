"""
Standard environment settings.

This module loads environment variables using python-dotenv and exposes
the following module-level constants:

    APP_DATABASE_URL (str): The URL for connecting to the database.
    JWT_SECRET (str): The secret key for encoding/decoding JWT tokens.
    ACCESS_TOKEN_EXPIRE_MINUTES (str): The access token expiration in minutes.
"""

import os
from dotenv import load_dotenv, find_dotenv

# Load environment variables from a .env file.
load_dotenv(find_dotenv())

APP_DATABASE_URL = os.environ.get("APP_DATABASE_URL")
JWT_SECRET = os.environ.get("JWT_SECRET")
ACCESS_TOKEN_EXPIRE_MINUTES = os.environ.get("ACCESS_TOKEN_EXPIRE_MINUTES")
