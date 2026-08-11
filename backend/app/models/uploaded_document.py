"""
FILE CONTENTS & OVERVIEW:
-------------------------
This file defines the `UploadedDocument` SQLAlchemy database model.
It represents document uploads linked to chat sessions in a PostgreSQL database using UUID keys.

Key attributes & relationships:
  - id: Primary key UUID generated automatically via `uuid.uuid4`.
  - session_id: Foreign key referencing `chat_sessions.id` with ON DELETE CASCADE and non-nullable constraint.
  - file_name: Non-nullable string holding the original filename of the uploaded document.
  - pages: Non-nullable integer representing the total number of pages in the document.
  - chunks: Non-nullable integer representing the total number of text chunks indexed in the vector store.
  - chroma_collection: Non-nullable string naming the ChromaDB collection associated with the document's vector embeddings.
  - created_at: Timestamp recording when the document record was created (server-side default with timezone).
  - session: SQLAlchemy ORM relationship mapping back to the parent `ChatSession` model instance.
"""

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
    """
    SQLAlchemy ORM model representing uploaded documents and their associated index metadata.

    Attributes:
        id (UUID): Unique primary key identifier for the uploaded document.
        session_id (UUID): Foreign key referencing the parent `chat_sessions.id` with CASCADE deletion.
        file_name (str): Original filename of the uploaded document.
        pages (int): Total number of pages extracted from the document.
        chunks (int): Total number of text chunks created for vector storage.
        chroma_collection (str): Name of the ChromaDB vector store collection holding embeddings.
        created_at (datetime): Server-generated timestamp recorded when the document is uploaded/created.
        session (ChatSession): ORM relationship mapping back to the parent `ChatSession` instance.
    """

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