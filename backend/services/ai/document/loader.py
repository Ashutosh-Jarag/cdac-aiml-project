from pathlib import Path
from typing import Any

from langchain_core.documents import Document
from langchain_community.document_loaders import (
    PyMuPDFLoader,
    Docx2txtLoader,
    CSVLoader,
    TextLoader,
    UnstructuredPowerPointLoader,
    UnstructuredExcelLoader,
)


class DocumentLoader:

    def load(self, file_path: str) -> list[Document]:
        extension = Path(file_path).suffix.lower()

        match extension:
            # Text-based loaders (require explicit encoding & auto-detection)
            case ".txt" | ".md":
                loader = TextLoader(
                    file_path=file_path,
                    encoding="utf-8",
                    autodetect_encoding=True,
                )

            case ".csv":
                loader = CSVLoader(
                    file_path=file_path,
                    encoding="utf-8",
                    autodetect_encoding=True,
                )

            # Binary / Structured Document Loaders
            case ".pdf":
                loader = PyMuPDFLoader(file_path)

            case ".docx":
                loader = Docx2txtLoader(file_path)

            case ".pptx":
                loader = UnstructuredPowerPointLoader(file_path)

            case ".xlsx":
                loader = UnstructuredExcelLoader(file_path)

            case _:
                raise ValueError(f"Unsupported file type: {extension}")

        return loader.load()


document_loader = DocumentLoader()