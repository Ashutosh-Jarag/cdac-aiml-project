"""
FILE CONTENTS & OVERVIEW:
-------------------------
This file defines the `ChatSession` SQLAlchemy database model.
It represents conversation sessions containing metadata and relational links to both chat messages 
and uploaded documents stored in PostgreSQL using UUID keys.

Key attributes & relationships:
  - id: Primary key UUID generated via `uuid.uuid4`.
  - title: Display title of the chat session (defaults to "New Chat").
  - created_at: Timestamp recording session creation time (server-side default with timezone).
  - updated_at: Timestamp recording the last update time (automatically updated on row modifications).
  - messages: SQLAlchemy ORM relationship linked to `ChatMessage`, configured with cascade delete and passive deletes.
  - documents: SQLAlchemy ORM relationship linked to `UploadedDocument`, configured with cascade delete and passive deletes.
"""

import uuid

from sqlalchemy import Column, DateTime, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database.connection import Base


class ChatSession(Base):
    """
    SQLAlchemy ORM model representing a chat conversation session with associated messages and documents.

    Attributes:
        id (UUID): Unique primary key identifier for the chat session.
        title (str): Display title of the session. Defaults to "New Chat".
        created_at (datetime): Server-side timestamp indicating when the session was created.
        updated_at (datetime): Server-side timestamp automatically updated when the session is modified.
        messages (list[ChatMessage]): One-to-many ORM relationship with associated chat messages, 
                                       configured with orphan deletion cascade rules.
        documents (list[UploadedDocument]): One-to-many ORM relationship with uploaded documents linked 
                                             to this session, configured with orphan deletion cascade rules.
    """

    __tablename__ = "chat_sessions"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    title = Column(
        String,
        default="New Chat",
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
    )

    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
    )

    messages = relationship(
        "ChatMessage",
        back_populates="session",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )

    documents = relationship(
        "UploadedDocument",
        back_populates="session",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )