import uuid

from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey,
)

from sqlalchemy.dialects.postgresql import UUID

from app.database.connection import Base

from sqlalchemy.orm import relationship


class UploadedDocument(Base):

    __tablename__ = "uploaded_documents"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )

    session_id = Column(
        UUID(as_uuid=True),
       ForeignKey(
            "chat_sessions.id",
            ondelete="CASCADE",
        ),
        nullable=False,
    )

    session = relationship(
        "ChatSession",
        back_populates="documents",
    )

    file_name = Column(String)

    pages = Column(Integer)

    chunks = Column(Integer)

    chroma_collection = Column(String)