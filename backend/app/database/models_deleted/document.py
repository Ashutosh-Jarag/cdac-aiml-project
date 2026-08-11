"""
FILE CONTENTS & OVERVIEW:
-------------------------
This file defines the `UploadedDocument` SQLAlchemy database model.
It represents document uploads linked to chat sessions in a PostgreSQL database using UUID keys.

Key attributes:
  - id: Unique primary key identifier generated via standard UUID v4.
  - session_id: Foreign key linking the document to an associated record in `chat_sessions` (CASCADE delete enabled).
  - session: SQLAlchemy ORM relationship linking back to the `ChatSession` model.
  - file_name: Original filename of the uploaded document.
  - pages: Total number of pages extracted from the document.
  - chunks: Number of vector chunks created from the document during embedding.
  - chroma_collection: Name/ID of the associated ChromaDB collection where vector embeddings reside.
"""

import uuid

from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.database.connection import Base


class UploadedDocument(Base):
    """
    SQLAlchemy ORM model representing uploaded documents and their processing metadata.

    Attributes:
        id (UUID): Unique primary key identifier for the uploaded document.
        session_id (UUID): Foreign key reference to `chat_sessions.id` with ON DELETE CASCADE.
        session (ChatSession): ORM relationship mapping to the parent ChatSession object.
        file_name (str): Original filename of the uploaded document file.
        pages (int): Total number of pages contained in the uploaded document.
        chunks (int): Total number of text chunks indexed into the vector store.
        chroma_collection (str): Name of the ChromaDB collection storing vector embeddings for this document.
    """

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