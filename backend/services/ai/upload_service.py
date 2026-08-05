from app.core.exceptions import AppException
from app.core.logger import logger
from app.repositories.document_repository import document_repository
from app.repositories.session_repository import session_repository
from services.ai.document.chunker import document_chunker
from services.ai.document.embedding import embedding_service
from services.ai.document.loader import document_loader
from services.ai.document.vector_store import vector_store


class UploadService:

    def upload(
        self,
        db,
        file_path: str,
    ):
        logger.info(f"Uploading file: {file_path}")

        session = session_repository.create(db)
        session_id = str(session.id)

        documents = document_loader.load(file_path)

        if not documents:
            raise AppException(
                "Unable to read uploaded file.",
                400,
            )

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
        logger.success(f"Upload completed for session {session_id}")

        return {
            "session_id": session_id,
            "file": {
                "name": source,
                "pages": len(documents),
                "chunks": len(chunks),
            },
        }


upload_service = UploadService()