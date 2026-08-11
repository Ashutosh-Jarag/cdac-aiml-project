"""
FILE CONTENTS & OVERVIEW:
-------------------------
This file defines the `UploadService` class, which manages the complete document ingestion pipeline.
It handles session creation, document loading, text chunking, embedding generation, vector storage persistence,
database record creation, classification predictions, and metadata payload formatting.

Pipeline Steps:
  1. Session Initialization: Creates a new `ChatSession` record in the database.
  2. Document Parsing: Parses the input file using `document_loader`.
  3. Chunking & Embedding: Splits document content into chunked text segments and computes vector embeddings.
  4. Storage Persistence: Indexes chunks and vectors in ChromaDB and records metadata in `document_repository`.
  5. Machine Learning Insights: Runs document classification (`classification_service`) and generates search resource links.

Exports:
  - upload_service: Singleton instance of `UploadService` for application-wide file uploading workflow processing.
"""

from typing import Any

from app.core.exceptions import AppException
from app.core.logger import logger
from app.repositories.document_repository import document_repository
from app.repositories.session_repository import session_repository
from services.ai.document.chunker import document_chunker
from services.ai.document.embedding import embedding_service
from services.ai.document.loader import document_loader
from services.ai.document.vector_store import vector_store
from services.ml.classification_service import classification_service


class UploadService:
    """
    Service class orchestrating document upload, text processing, vector indexing, and database persistence workflows.
    """

    def upload(
        self,
        db: Any,
        file_path: str,
    ) -> dict[str, Any]:
        """
        Executes the file ingestion pipeline and returns structured document ingestion metadata.

        Args:
            db (Session): Active SQLAlchemy database session.
            file_path (str): File system path to the uploaded document.

        Returns:
            dict[str, Any]: Dictionary containing session ID, document metadata, machine learning classification, 
                            and web resource search links.

        Raises:
            AppException: If the uploaded file cannot be read or parsed (400).
        """
        logger.info(f"Uploading file: {file_path}")

        session = session_repository.create(db)
        session_id = str(session.id)

        documents = document_loader.load(file_path)

        if not documents:
            raise AppException(
                "Unable to read uploaded file.",
                400,
            )

        full_text = "\n".join(
            doc.page_content for doc in documents
        )
        sample_text = full_text[:4000]
        recommendation_text = full_text[:10000]

        logger.info(f"Loaded {len(documents)} document(s)")

        chunks = document_chunker.split(documents)
        logger.info(f"Created {len(chunks)} chunk(s)")

        embeddings = embedding_service.embed_documents(
            [chunk.page_content for chunk in chunks]
        )

        vector_store.add_documents(
            collection_name=session_id,
            chunks=chunks,
            embeddings=embeddings,
        )
        logger.info(f"Stored vectors for session {session_id}")

        source = documents[0].metadata.get(
            "source",
            "",
        )

        document_repository.create(
            db=db,
            session_id=session.id,
            file_name=source,
            pages=len(documents),
            chunks=len(chunks),
            chroma_collection=session_id,
        )

        classification = None
        try:
            classification = classification_service.predict(
                title="Uploaded Document",
                abstract=sample_text,
            )
        except Exception as e:
            logger.warning(
                f"Document classification failed: {e}"
            )

        logger.success(f"Upload completed for session {session_id}")

        return {
            "session_id": session_id,
            "file": {
                "name": source,
                "pages": len(documents),
                "chunks": len(chunks),
            },
            "classification": classification,
            "recommendation": {
                "title": source,
                "text": recommendation_text,
            },
            "web_resources": [
                {
                    "title": f"Google search for {source}",
                    "url": f"https://www.google.com/search?q={source}",
                },
                {
                    "title": "Google Scholar",
                    "url": f"https://scholar.google.com/scholar?q={source}",
                },
                {
                    "title": "arXiv Search",
                    "url": f"https://arxiv.org/search/?query={source}&searchtype=all",
                },
            ],
        }


# Global singleton instance of UploadService
upload_service = UploadService()