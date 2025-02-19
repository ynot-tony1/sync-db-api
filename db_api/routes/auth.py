from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db.database import get_db
from models.user import AppUser
from utils.jwt_utils import get_current_user  

router = APIRouter()

@router.get("/user")
def get_user(current_user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    """
    Getting the authenticated user's details from the database.

    This first verifies the users identity using the JWT in the Authorization header.
    It then queries the database for a user record whose `sub' matches the `sub` extracted from the token.

    Args:
        current_user (dict): A dictionary containing the authenticated user's data 
        extracted from the JWT.
        db (Session): The database session from the dependency injection.

    Returns:
        dict: A JSON response containing the user's `sub` and `email`.

    Raises:
        HTTPException 404 (not found): If no user is found in the database with that `sub`,  it raises a HTTP status code 404.

    Example:
        GET /user
        Authorization: Bearer <valid JWT token>

        JSON response:
        {
            "sub": "123e4567-e89b-12d3-a456-426614174000",
            "email": "tony@oh-synkies.com"
        }
    """
    user = db.query(AppUser).filter(AppUser.sub == current_user["sub"]).first()
    if not user:
        raise HTTPException(status_code=404, detail="Couldn't find that user")
    return {"sub": user.sub, "email": user.email}


@router.post("/user")
def create_user(current_user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    """
    Create a new user in the App DB.

    When a new user registers and is authenticated by the Auth Service, this creates an entry for them
    in the App DB. It checks whether a user with the given `sub` already exists. 
    If so, it raises a  HTTP 400 error, 'bad request'. Otherwise, it creates a new user record,
    commits the transaction and returns the new user's details.

    Args:
        current_user (dict): A dictionary containing the authenticated user's data 
        extracted from the JWT.
        db (Session): The database session provided by dependency injection.

    Returns:
        dict: A JSON response containing the newly created user's `sub` and `email`.

    Raises:
        HTTPException 400 (bad request): If a user with the provided `sub` already exists, raises a HTTP status code 400.

    Example:
        POST /user
        Authorization: Bearer <valid JWT token>

        JSON response:
        {
            "sub": "123e4567-e89b-12d3-a456-426614174000",
            "email": "tony@syncnny-cricket.com"
        }
    """
    if db.query(AppUser).filter(AppUser.sub == current_user["sub"]).first():
        raise HTTPException(status_code=400, detail="That user already exists")
    
    new_user = AppUser(sub=current_user["sub"], email=current_user["email"])
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"sub": new_user.sub, "email": new_user.email}
