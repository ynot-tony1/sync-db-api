import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

APP_DATABASE_URL = os.environ.get("APP_DATABASE_URL")
JWT_SECRET = os.environ.get("JWT_SECRET")
ACCESS_TOKEN_EXPIRE_MINUTES = os.environ.get("ACCESS_TOKEN_EXPIRE_MINUTES")
