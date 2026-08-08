from app.core.exceptions import AppException
from app.core.logger import logger

from services.ai.document.embedding import embedding_service
from services.ai.document.vector_store import vector_store


class Retriever:

    def retrieve(
        self,
        session_id: str,
        question: str,
        top_k: int = 5,
    ):

        embedding = embedding_service.embed_query(question)

        results = vector_store.search(
            collection_name=session_id,
            query_embedding=embedding,
            top_k=top_k,
        )

        if not results["documents"] or not results["documents"][0]:
            raise AppException(
                "No relevant information found.",
                404,
            )

        logger.info(
            f"Retrieved {len(results['documents'][0])} chunk(s)"
        )

        return results


retriever = Retriever()