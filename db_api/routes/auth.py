from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db_api.db.database import get_db
from db_api.models.user import AppUser, UserResponse
from db_api.utils.jwt_utils import get_current_user

router = APIRouter()

@router.get("/user", response_model=UserResponse)
def get_user(
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> UserResponse:
    user = db.query(AppUser).filter(AppUser.sub == current_user["sub"]).first()
    if not user:
        raise HTTPException(status_code=404, detail="Couldn't find that user")
    return user  

@router.post("/user", response_model=UserResponse)
def create_user(
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> UserResponse:
    if db.query(AppUser).filter(AppUser.sub == current_user["sub"]).first():
        raise HTTPException(status_code=400, detail="That user already exists")
    
    new_user = AppUser(sub=current_user["sub"], email=current_user["email"])
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user
