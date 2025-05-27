"""
Unit Test Suite for the DB API Endpoints

This module tests the endpoints defined in db_api by overriding dependencies
with MagicMock objects. It verifies user creation, retrieval, and error handling
without needing a real database.

Example:
    To run the tests from the main dir:
        python -m unittest discover -s tests/unit_tests -p "test_*.py" -v
"""

import unittest
from unittest.mock import MagicMock
from fastapi.testclient import TestClient
from db_api.main import app
from db_api.db.database import get_db
from db_api.utils.jwt_utils import get_current_user

client = TestClient(app)


class TestDBAPI(unittest.TestCase):
    """Unit tests for the DB API endpoints using a dummy database session.

    This class uses FastAPI's TestClient to simulate HTTP requests against the DB API
    endpoints. The dependencies `get_db` and `get_current_user` are overridden with dummy
    objects to simulate interactions with a database without needing an actual database.
    """

    def setUp(self):
        """Set up test fixtures before each test.

        Overrides the `get_db` dependency to provide a dummy database session.
        The dummy database session is created as a MagicMock and will simulate database
        queries and operations.
        """
        self.dummy_db = MagicMock()

        def override_get_db():
            """A generator that yields the dummy database session."""
            yield self.dummy_db

        app.dependency_overrides = {
            get_db: override_get_db,
            get_current_user: lambda: {"sub": "test-sub", "email": "sosynced@intime.com"}
        }

    def tearDown(self):
        """Clean up test fixtures after each test.

        Removes any dependency overrides set during the test to ensure a clean
        state for subsequent tests.
        """
        app.dependency_overrides = {}

    def set_query_first_value(self, value):
        """Helper function to set the return value of the chained query calls.

        This helper encapsulates the following chain:
            self.dummy_db.query.return_value.filter.return_value.first.return_value = value
        It simplifies test code by allowing a single call to configure the dummy
        database session's behavior for query().filter().first().

        Args:
            value: The value to return when first() is called on the dummy query.
        """
        self.dummy_db.query.return_value.filter.return_value.first.return_value = value

    def test_get_user_not_found(self):
        """Test that GET /user returns 404 when no user is found.

        Simulates a scenario where the dummy database session returns None for the user query.
        Sends a GET request to the /user endpoint and verifies that the response status code is 404
        and the error message is correct.

        Returns:
            None
        """
        self.set_query_first_value(None)
        response = client.get("/user")
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json()["detail"], "Couldn't find that user")

    def test_create_user_success(self):
        """Test that POST /user successfully creates a new user.

        Simulates a scenario where the dummy database session finds no existing user (i.e., returns None)
        and a new user is created. Sends a POST request to the /user endpoint and verifies that:
          - The response status code is 200.
          - The returned user details match the expected values.
          - The dummy database session's add, commit, and refresh methods are called.

        Returns:
            None
        """
        self.set_query_first_value(None)
        response = client.post("/user")
        self.assertEqual(response.status_code, 201)
        data = response.json()
        self.assertEqual(data["sub"], "test-sub")
        self.assertEqual(data["email"], "sosynced@intime.com")
        self.dummy_db.add.assert_called()
        self.dummy_db.commit.assert_called()
        self.dummy_db.refresh.assert_called()



    def test_create_user_already_exists(self):
        """Test that POST /user returns a 400 error when the user already exists.
        Simulates a scenario where the dummy database session returns an existing user for the query.
        Sends a POST request to the /user endpoint and verifies that:
          - The response status code is 400.
          - The returned error message indicates that the user already exists.
        Returns:
            None
        """
        from sqlalchemy.exc import IntegrityError
        self.dummy_db.commit.side_effect = IntegrityError("duplicate key","",None)
 
        response = client.post("/user")
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()["detail"], "That user already exists")

    def test_get_user_success(self):
        """Test that GET /user returns user details when the user exists.

        Configures the dummy database session to return a dummy user object with attributes 'sub' and 'email'.
        Sends a GET request to the /user endpoint and verifies that:
          - The response status code is 200.
          - The returned JSON matches the dummy user's details.

        Returns:
            None
        """
        dummy_user = MagicMock()
        dummy_user.sub = "test-sub"
        dummy_user.email = "sosynced@intime.com"
        self.set_query_first_value(dummy_user)
        response = client.get("/user")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["sub"], "test-sub")
        self.assertEqual(data["email"], "sosynced@intime.com")


if __name__ == "__main__":
    unittest.main()
