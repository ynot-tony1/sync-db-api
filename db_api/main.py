"""
Main application module for the DB API.

This module creates and configures the FastAPI application instance. It sets up CORS middleware to allow
cross-origin requests, includes the routes from the auth router and sets up the database schema by creating
any missing tables defined in the ORM's Base metadata.

To use:
    TO run it, use something like:
        uvicorn main:app --reload --port (port number)

Attributes:
    app (FastAPI): The FastAPI application instance with middleware and routes configured.
"""

from db.database import engine, Base
from routes import auth  
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(auth.router)
Base.metadata.create_all(bind=engine)
