from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from db_api.db.database import get_db
from db_api.models.user import AppUser, UserResponse
from db_api.utils.jwt_utils import get_current_user

router = APIRouter()

@router.get("/user", response_model=UserResponse)
def get_user(
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> UserResponse:
    """
    Return the AppUser that matches the caller’s JWT ``sub``.

    404 → the JWT is valid but the app-layer profile hasn’t been created yet.
    """
    user = db.query(AppUser).filter(AppUser.sub == current_user["sub"]).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Couldn't find that user",
        )
    return user


@router.post(
    "/user",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_user(
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> UserResponse:
    """
    Create an AppUser using the caller’s JWT claims.

    * 201 → profile created  
    * 400 → profile already exists (same contract as Auth Service)
    """
    try:
        new_user = AppUser(
            sub=current_user["sub"],
            email=current_user["email"],
        )
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user

    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="That user already exists",
        )
