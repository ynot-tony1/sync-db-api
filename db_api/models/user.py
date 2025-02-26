from sqlalchemy import Column, Integer, String
from db_api.db.database import Base
from pydantic import BaseModel

class AppUser(Base):
    __tablename__ = "app_users"
    user_id: int = Column(Integer, primary_key=True, index=True)
    sub: str = Column(String, unique=True, nullable=False)
    email: str = Column(String, unique=True, nullable=False)

class UserResponse(BaseModel):
    sub: str
    email: str

    class Config:
        orm_mode = True
