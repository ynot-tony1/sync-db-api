import unittest
import jwt
from fastapi import HTTPException
from fastapi.security import HTTPAuthorizationCredentials
from db_api.utils.jwt_utils import get_current_user
from db_api.config.settings import JWT_SECRET

class TestJWTUtils(unittest.TestCase):
    def setUp(self):
        self.valid_payload = {"sub": "test-sub", "email": "synxo@fnicket.com"}
        self.valid_token = jwt.encode(self.valid_payload, JWT_SECRET, algorithm="HS256")
        if isinstance(self.valid_token, bytes):
            self.valid_token = self.valid_token.decode("utf-8")
    
    def test_get_current_user_valid(self):
        """Test that a valid JWT returns the expected user dictionary."""
        credentials = HTTPAuthorizationCredentials(scheme="Bearer", credentials=self.valid_token)
        result = get_current_user(credentials)
        self.assertEqual(result, self.valid_payload)
    
    def test_get_current_user_missing_sub(self):
        """Test that a token missing the 'sub' field raises HTTPException."""
        payload = {"email": "synxo@fnicket.com"}
        token = jwt.encode(payload, JWT_SECRET, algorithm="HS256")
        if isinstance(token, bytes):
            token = token.decode("utf-8")
        credentials = HTTPAuthorizationCredentials(scheme="Bearer", credentials=token)
        with self.assertRaises(HTTPException) as context:
            get_current_user(credentials)
        self.assertEqual(context.exception.status_code, 401)
        self.assertEqual(context.exception.detail, "Invalid token payload")
    
    def test_get_current_user_missing_email(self):
        """Test that a token missing the 'email' field raises HTTPException."""
        payload = {"sub": "test-sub"}
        token = jwt.encode(payload, JWT_SECRET, algorithm="HS256")
        if isinstance(token, bytes):
            token = token.decode("utf-8")
        credentials = HTTPAuthorizationCredentials(scheme="Bearer", credentials=token)
        with self.assertRaises(HTTPException) as context:
            get_current_user(credentials)
        self.assertEqual(context.exception.status_code, 401)
        self.assertEqual(context.exception.detail, "Invalid token payload")
    
    def test_get_current_user_invalid_token(self):
        """Test that an invalid token (non-decodable) raises a JWT error."""
        credentials = HTTPAuthorizationCredentials(scheme="Bearer", credentials="not.a.valid.token")
        with self.assertRaises(Exception):
            get_current_user(credentials)

if __name__ == "__main__":
    unittest.main()
