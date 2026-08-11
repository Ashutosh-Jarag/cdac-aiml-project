"""
FILE CONTENTS & OVERVIEW:
-------------------------
This file defines the `ChatMessage` SQLAlchemy database model.
It represents individual message entries exchanged within a chat session stored in a PostgreSQL database using UUID keys.

Key attributes:
  - id: Unique primary key identifier generated via standard UUID v4.
  - session_id: Foreign key reference pointing to the associated `chat_sessions.id`.
  - role: Role or origin of the message (e.g., 'user', 'assistant', 'system').
  - message: The full text body/content of the chat message.
  - created_at: Timestamp indicating when the message was created (defaults to server-side current time with timezone).
"""

import uuid

from sqlalchemy import (
    Column,
    ForeignKey,
    String,
    Text,
    DateTime,
)
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import UUID

from app.database.connection import Base


class ChatMessage(Base):
    """
    SQLAlchemy ORM model representing individual messages in a chat conversation.

    Attributes:
        id (UUID): Unique primary key identifier for the chat message.
        session_id (UUID): Foreign key linking the message to a specific record in `chat_sessions.id`.
        role (str): Role identifier of the sender (e.g., 'user', 'assistant', 'system').
        message (str): Text content of the chat message.
        created_at (datetime): Time at which the message was recorded, automatically set by the database server.
    """

    __tablename__ = "chat_messages"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )

    session_id = Column(
        UUID(as_uuid=True),
        ForeignKey("chat_sessions.id")
    )

    role = Column(String)

    message = Column(Text)

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )