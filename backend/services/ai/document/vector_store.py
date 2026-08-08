from app.core.chroma_manager import chroma_manager


class VectorStore:

    def add_documents(
        self,
        collection_name: str,
        chunks,
        embeddings
    ):

        collection = chroma_manager.get_collection(
            collection_name
        )

        collection.add(
            ids=[
                str(i)
                for i in range(len(chunks))
            ],
            documents=[
                chunk.page_content
                for chunk in chunks
            ],
            embeddings=embeddings,
            metadatas=[
                chunk.metadata
                for chunk in chunks
            ]
        )

    def search(
        self,
        collection_name: str,
        query_embedding,
        top_k: int = 5
    ):

        collection = chroma_manager.get_collection(
            collection_name
        )

        return collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k
        )


vector_store = VectorStore()