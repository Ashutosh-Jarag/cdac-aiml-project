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