import uuid

from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database.connection import Base


class UploadedDocument(Base):

    __tablename__ = "uploaded_documents"

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

    file_name = Column(
        String,
        nullable=False,
    )

    pages = Column(
        Integer,
        nullable=False,
    )

    chunks = Column(
        Integer,
        nullable=False,
    )

    chroma_collection = Column(
        String,
        nullable=False,
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
    )

    session = relationship(
        "ChatSession",
        back_populates="documents",
    )