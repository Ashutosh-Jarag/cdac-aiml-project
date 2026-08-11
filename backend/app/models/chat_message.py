"""
FILE CONTENTS & OVERVIEW:
-------------------------
This file defines the `ChatMessage` SQLAlchemy database model.
It represents individual chat messages exchanged within a conversation session in a PostgreSQL database using UUID keys.

Key attributes:
  - id: Primary key UUID automatically generated via `uuid.uuid4`.
  - session_id: Foreign key referencing `chat_sessions.id` with ON DELETE CASCADE and non-nullable constraint.
  - role: Non-nullable string designating message sender role (e.g., 'user', 'assistant', 'system').
  - content: Non-nullable string holding the message body text.
  - created_at: Timestamp registering message creation time (server-side default with timezone).
  - session: SQLAlchemy ORM relationship pointing back to the parent `ChatSession` model.
"""

import uuid

from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.database.connection import Base


class ChatMessage(Base):
    """
    SQLAlchemy ORM model representing individual chat messages within a session.

    Attributes:
        id (UUID): Unique primary key identifier for the message.
        session_id (UUID): Foreign key referencing the parent `chat_sessions.id` with CASCADE deletion.
        role (str): Role identifier of the message sender (e.g., 'user', 'assistant', 'system').
        content (str): Content body of the chat message.
        created_at (datetime): Server-generated timestamp recorded when the message is created.
        session (ChatSession): ORM relationship linking back to the parent `ChatSession` instance.
    """

    __tablename__ = "chat_messages"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    session_id = Column(
        UUID(as_uuid=True),
        ForeignKey(
            "chat_sessions.id",
            ondelete="CASCADE",
        ),
        nullable=False,
    )

    role = Column(
        String,
        nullable=False,
    )

    content = Column(
        String,
        nullable=False,
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
    )

    session = relationship(
        "ChatSession",
        back_populates="messages",
    )