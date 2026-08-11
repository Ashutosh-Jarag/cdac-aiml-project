"""
FILE CONTENTS & OVERVIEW:
-------------------------
This file defines the `ChatSession` SQLAlchemy database model.
It represents an individual chat session container within a PostgreSQL database using UUID keys.

Key attributes:
  - id: Unique primary key identifier generated via standard UUID v4.
  - title: Display title of the chat conversation session (defaults to "New Chat").
  - created_at: Timestamp indicating when the session was created (defaults to server-side current time with timezone).
  - updated_at: Timestamp indicating when the session was last updated (automatically updated on row modifications).
"""

import uuid

from sqlalchemy import Column, DateTime, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func

from app.database.connection import Base


class ChatSession(Base):
    """
    SQLAlchemy ORM model representing a chat conversation session.

    Attributes:
        id (UUID): Unique primary key identifier for the chat session.
        title (str): Display title of the chat session. Defaults to "New Chat".
        created_at (datetime): Timestamp recording session creation time, set by the database server.
        updated_at (datetime): Timestamp recording the last update time, automatically updated on row changes.
    """

    __tablename__ = "chat_sessions"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )

    title = Column(
        String,
        default="New Chat"
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now()
    )