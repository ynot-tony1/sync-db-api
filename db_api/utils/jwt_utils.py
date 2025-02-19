import jwt
from fastapi import HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from config.settings import JWT_SECRET

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(HTTPBearer())):
    """
    Extracts and validates the current user's identity from a JWT token.

    This function gets the JWT token from the Authorization header using the HTTPBearer dependency. 
    It then decodes the token using the JWT_SECRET and the HS256 algorithm. 
    Finally, it checks that the token payload contains both 'sub' and 'email'. 
    If either field is missing, a HTTPException with a 401 status code is raised, 'unauthorized.'

    Args:
        credentials (HTTPAuthorizationCredentials): The HTTP credentials extracted 
        from the request's Authorization header in which there should be a bearer token.

    Returns:
        dict: A dictionary containing the 'sub' and 'email' from the decoded JWT payload.
              example json:
              {
                  "sub": "958e4567-e89b-12d3-a456-426668394000",
                  "email": "tony@sync-182.com"
              }

    Raises:
        HTTPException 401 (bad request): Is raised if the token payload does not include 'sub' or 'email'
    """
    payload = jwt.decode(credentials.credentials, JWT_SECRET, algorithms=["HS256"])
    if "sub" not in payload or "email" not in payload:
        raise HTTPException(status_code=401, detail="Invalid token payload")
    return {"sub": payload["sub"], "email": payload["email"]}
