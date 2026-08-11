"""
FILE CONTENTS & OVERVIEW:
-------------------------
This file defines the `DocumentChunker` service class, responsible for breaking down high-level
`Document` objects into smaller, overlapping text chunks for downstream vector indexing and RAG retrieval.

Key functionality:
  - Initializes `RecursiveCharacterTextSplitter` with defined chunk size (1000 characters) and overlap (200 characters).
  - split(): Takes a list of LangChain `Document` objects and returns a flattened list of chunked `Document` instances.

Exports:
  - document_chunker: Singleton instance of `DocumentChunker` for application-wide document splitting.
"""

from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document


class DocumentChunker:
    """
    Utility class for chunking documents into smaller text segments suitable for vector embedding and retrieval.
    """

    def __init__(self):
        """
        Initializes DocumentChunker with a pre-configured RecursiveCharacterTextSplitter instance.

        Args:
            None

        Returns:
            None
        """
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            separators=[
                "\n\n",
                "\n",
                ". ",
                " ",
                "",
            ]
        )

    def split(
        self,
        documents: list[Document]
    ) -> list[Document]:
        """
        Splits a list of input LangChain Document instances into smaller, overlapping Document chunks.

        Args:
            documents (list[Document]): List of raw or loaded LangChain Document objects.

        Returns:
            list[Document]: List of chunked LangChain Document objects with preserved metadata.
        """
        return self.text_splitter.split_documents(documents)


# Global singleton instance of DocumentChunker
document_chunker = DocumentChunker()