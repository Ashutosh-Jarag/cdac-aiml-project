from sqlalchemy.orm import Session

from app.models.uploaded_document import UploadedDocument


class DocumentRepository:

    def create(
        self,
        db: Session,
        session_id,
        file_name,
        pages,
        chunks,
        chroma_collection,
    ):

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


document_repository = DocumentRepository()