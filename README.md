# DB API

The DB API is a FastAPI-based API for managing application user data. It leverages SQLAlchemy for database interactions and JWT for token-based authentication.

## Features

- **User Management:** Retrieve and create user records.
- **JWT Authentication:** Secures endpoints with JWT tokens.
- **Database Management:** Uses SQLAlchemy ORM for interacting with a PostgreSQL database.
- **CORS Support:** Configured middleware to support cross-origin requests.

## Directory Structure
'''
db_api
├── config
│   ├── __init__.py
│   ├── settings.py
│   └── type_settings.py
├── db
│   ├── base.py
│   ├── database.py
│   └── __init__.py
├── main.py
├── models
│   ├── __init__.py
│   └── user.py
├── routes
│   ├── auth.py
│   └── __init__.py
└── utils
    ├── jwt_utils.py
    └── __init__.py
'''
> Note: Compiled files and __pycache__ directories are omitted for clarity.

## Environment Variables

Before running the service, configure the following environment variables:

- **APP_DATABASE_URL**  
  Example: `postgresql://app_admin:apppassword@localhost/app_db`
- **JWT_SECRET**  
  Example: `supersecretkey`
- **ACCESS_TOKEN_EXPIRE_MINUTES**  
  Example: `30`

You can set these in your shell or use a `.env` file for local development.

## Setting the PYTHONPATH

Ensure that the PYTHONPATH is set to include the project root so that the modules can be correctly imported. You can do this manually in your shell:

- **On Linux/Mac:**

  ```bash
  export PYTHONPATH=$(pwd)

- **On Windows (Command Prompt):**

    set PYTHONPATH=%cd%

You can add these commands to your shell profile (e.g., .bashrc or .zshrc) for convenience.

## Setup and Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/ynot-tony1/sync-auth-api.git
   cd db_api

2. **Create a virtual environment:**

python -m venv venv
source venv/bin/activate    # On Windows: venv\Scripts\activate

3. **Install the dependencies:**

    pip install -r requirements.txt

4. **Configure Environment Variables:**

    Either export the variables manually or create a .env file in the project root with the required settings.

5. **Running the Application**

Start the FastAPI server using Uvicorn:

uvicorn main:app --reload --port 8000

Access the API at http://localhost:8000.

## Running Tests

Ensure that your PYTHONPATH is correctly set then execute:

python -m unittest discover -s tests/unit_tests -p "test_*.py" -v


## API Endpoints

GET /user

    Description: Retrieves the current user's details.
    Response: A JSON object containing:
        sub: Unique subject identifier for the user.
        email: User's email address.
    Error: Returns a 404 error if the user is not found.

POST /user

    Description: Creates a new user based on the current JWT token.
    Response: A JSON object containing:
        sub: Unique subject identifier for the user.
        email: User's email address.
    Error: Returns a 400 error if the user already exists.

## Code Overview

    main.py:
        Initializes the FastAPI app.
        Configures CORS middleware.
        Includes the auth router and creates database tables on startup.

    config/
        Contains application configuration and settings.

    db/
        database.py: Sets up the SQLAlchemy engine and session factory.
        base.py: Defines the base for SQLAlchemy models.

    models/user.py:
        Defines the SQLAlchemy model AppUser for storing user details.
        Contains the Pydantic model UserResponse for serializing user responses.

    routes/auth.py:
        Implements the /user GET and POST endpoints.
        Utilizes dependency injection to manage database sessions and JWT validation.

    utils/jwt_utils.py:
        Provides helper functions for JWT token encoding and decoding.
        Contains a dependency to extract the current user from the JWT token.

## Dependencies

The project relies on several key Python packages:

    FastAPI: Web framework for building APIs.
    SQLAlchemy: ORM for database interactions.
    Pydantic: Data validation.
    bcrypt: Password hashing.
    PyJWT: JWT token encoding and decoding.
    uvicorn: ASGI server for FastAPI.
    (See requirements.txt for the full list of dependencies.)

## Additional Notes

    Database: Ensure the PostgreSQL database specified in APP_DATABASE_URL is running and accessible.
    JWT Tokens: Tokens are set to expire based on the ACCESS_TOKEN_EXPIRE_MINUTES value.
    Security Considerations: This service uses basic security measures and may require additional enhancements (e.g., rate limiting, HTTPS) for production deployment.

