"""
FILE CONTENTS & OVERVIEW:
-------------------------
This file configures the SQLAlchemy relational database connection and session management for the application.
It constructs the PostgreSQL database connection string from central configuration settings, initializes
the SQLAlchemy engine, defines the declarative `Base` class for ORM models, and provides a database session dependency worker.

Components & Exports:
  - DATABASE_URL: Formatted PostgreSQL connection URL generated from settings.
  - Base: Declarative Base class inherited by all ORM models.
  - engine: Core SQLAlchemy Engine managing the connection pool to the PostgreSQL database.
  - SessionLocal: Bound `sessionmaker` factory for instantiating database sessions.
  - get_db(): Dependency generator function that yields database sessions and guarantees cleanup/closure.
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from app.core.config import settings

# Construct PostgreSQL connection string using central application settings
DATABASE_URL = (
    f"postgresql://{settings.DB_USER}:"
    f"{settings.DB_PASSWORD}@"
    f"{settings.DB_HOST}:"
    f"{settings.DB_PORT}/"
    f"{settings.DB_NAME}"
)


class Base(DeclarativeBase):
    """
    Declarative Base class used as the parent class for all ORM models.
    """
    pass


# Initialize SQLAlchemy core database engine
engine = create_engine(DATABASE_URL)

# Create session factory configured without autocommit/autoflush by default
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)


def get_db():
    """
    FastAPI dependency function that provides a database session instance per request context.
    Yields the session and ensures it is properly closed in the `finally` block when the request finishes.

    Yields:
        Session: SQLAlchemy database session instance.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()