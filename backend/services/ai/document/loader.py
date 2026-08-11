"""
FILE CONTENTS & OVERVIEW:
-------------------------
This file defines the `DocumentLoader` factory class, responsible for parsing and loading raw documents 
of various file formats into standardized LangChain `Document` objects.

Key functionality:
  - Detects file extension from input file path using `pathlib.Path`.
  - Dispatches extension to matching specialized loaders:
      * Text & Markdown (.txt, .md): `TextLoader` with UTF-8 encoding and auto-detection.
      * CSV (.csv): `CSVLoader` with UTF-8 encoding and auto-detection.
      * PDF (.pdf): `PyMuPDFLoader`.
      * Word (.docx): `Docx2txtLoader`.
      * PowerPoint (.pptx): `UnstructuredPowerPointLoader`.
      * Excel (.xlsx): `UnstructuredExcelLoader`.
  - Raises a `ValueError` for unsupported file extensions.
  - load(): Executes document parsing and returns a list of LangChain `Document` objects.

Exports:
  - document_loader: Singleton instance of `DocumentLoader` for application-wide document loading operations.
"""

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
    """
    Factory class for loading and parsing various file types into standardized LangChain Document objects.
    """

    def load(self, file_path: str) -> list[Document]:
        """
        Parses a file based on its extension and returns a list of extracted Document objects.

        Args:
            file_path (str): The absolute or relative system path to the file to be loaded.

        Returns:
            list[Document]: List of parsed LangChain Document instances containing content and metadata.

        Raises:
            ValueError: If the file extension is not supported by any configured loader.
        """
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


# Global singleton instance of DocumentLoader
document_loader = DocumentLoader()