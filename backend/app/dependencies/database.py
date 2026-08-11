"""
FILE CONTENTS & OVERVIEW:
-------------------------
This file provides a database session retrieval helper function.
It utility wraps the `get_db` generator dependency to fetch a standalone active SQLAlchemy `Session` 
instance outside of FastAPI's standard dependency injection pipeline.

Functions:
  - get_database: Returns a single active SQLAlchemy database Session from the `get_db` generator.
"""

from sqlalchemy.orm import Session

from app.database.connection import get_db


def get_database() -> Session:
    """
    Retrieves and returns an active SQLAlchemy database Session object.

    Advances the `get_db()` generator once to retrieve a fresh session instance for synchronous 
    or standalone background usage.

    Returns:
        Session: Active SQLAlchemy ORM session.
    """
    return next(get_db())