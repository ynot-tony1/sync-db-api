"""
JWT Utilities module.

This module provides helper functions for encoding and decoding JSON Web Tokens (JWT)
used in the authentication process.
"""

import jwt
from typing import Dict, Any
from fastapi import HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from db_api.config.settings import JWT_SECRET

def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(HTTPBearer())
) -> Dict[str, str]:
    """Extract and validate the current user's identity from a JWT token.

    The JWT is decoded using the secret key defined in settings and the HS256 algorithm.
    The function then checks that the token payload contains both 'sub' and 'email'.

    Args:
        credentials (HTTPAuthorizationCredentials): The HTTP credentials containing the JWT token.

    Returns:
        Dict[str, str]: A dictionary with the user's 'sub' and 'email'.

    Raises:
        HTTPException: If the token payload is invalid or missing required fields.
    """
    payload: Dict[str, Any] = jwt.decode(
        credentials.credentials,
        JWT_SECRET,
        algorithms=["HS256"]
    )
    if "sub" not in payload or "email" not in payload:
        raise HTTPException(status_code=401, detail="Invalid token payload")
    return {"sub": payload["sub"], "email": payload["email"]}
