"""
FILE CONTENTS & OVERVIEW:
-------------------------
This file defines the `DocumentRepository` class, providing data access layer (DAL) operations
for creating and persisting `UploadedDocument` entities in the database.

Key functionality:
  - create(): Instantiates, adds, and commits a new `UploadedDocument` record associated with a specific chat session.

Exports:
  - document_repository: Singleton instance of `DocumentRepository` for application-wide database operations.
"""

from typing import Any
from sqlalchemy.orm import Session

from app.models.uploaded_document import UploadedDocument


class DocumentRepository:
    """
    Repository class providing database operations for `UploadedDocument` records.
    """

    def create(
        self,
        db: Session,
        session_id: Any,
        file_name: str,
        pages: int,
        chunks: int,
        chroma_collection: str,
    ) -> UploadedDocument:
        """
        Creates and persists a new `UploadedDocument` record in the database.

        Args:
            db (Session): Active SQLAlchemy database session.
            session_id (UUID | str): Unique ID of the chat session associated with the document.
            file_name (str): Original name of the uploaded file.
            pages (int): Total number of pages in the document.
            chunks (int): Total number of indexed text chunks generated from the document.
            chroma_collection (str): Name of the associated ChromaDB collection storing document vector embeddings.

        Returns:
            UploadedDocument: The newly created and refreshed `UploadedDocument` ORM object.
        """
        document = UploadedDocument(
            session_id=session_id,
            file_name=file_name,
            pages=pages,
            chunks=chunks,
            chroma_collection=chroma_collection,
        )

        db.add(document)
        db.commit()
        db.refresh(document)

        return document


# Global singleton instance of DocumentRepository
document_repository = DocumentRepository()