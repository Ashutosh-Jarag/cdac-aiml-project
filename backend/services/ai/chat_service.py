from uuid import UUID

from app.core.ai_manager import ai_manager
from app.core.exceptions import AppException
from app.core.logger import logger
from app.repositories.message_repository import message_repository  # Ensure this import path matches your project
from services.ai.graph import chat_graph
from services.ai.graph.prompts import SYSTEM_PROMPT
from services.ai.retriever import retriever


class AIChatService:

    def chat(
        self,
        db,
        message: str,
        session_id: str,
        provider: str = "gemini",
        api_key: str = None,
    ):
        if not session_id:
            raise AppException(
                "Session ID is required.",
                400,
            )

        try:
            session_uuid = UUID(session_id)
        except ValueError:
            raise AppException(
                "Invalid Session ID format.",
                400,
            )

        logger.info(f"Question received for {session_id}")

        state = {
            "db": db,
            "session_id": session_id,
            "session_uuid": session_uuid,
            "provider": provider or "gemini",
            "api_key": api_key,
            "question": message,
        }

        result = chat_graph.invoke(state)

        logger.success("Answer generated successfully")

        return {
            "answer": result["answer"],
            "references": result["references"],
        }

#     def stream(
#         self,
#         db,
#         message: str,
#         session_id: str,
#         provider: str = "gemini",
#         api_key: str = None,
#     ):
#         if not session_id:
#             raise AppException(
#                 "Session ID is required.",
#                 400,
#             )

#         try:
#             session_uuid = UUID(session_id)
#         except ValueError:
#             raise AppException(
#                 "Invalid Session ID format.",
#                 400,
#             )

#         history = message_repository.get_history(
#             db=db,
#             session_id=session_uuid,
#         )

#         conversation = ""
#         for msg in history:
#             conversation += f"{msg.role}: {msg.content}\n"

#         result = retriever.retrieve(
#             session_id=session_id,
#             question=message,
#         )

#         context = "\n\n".join(result["documents"][0]) if result.get("documents") else ""

#         prompt = f"""
# Conversation

# {conversation}

# Context

# {context}

# Question

# {message}
# """

#         llm = ai_manager.get_provider(
#             provider,
#             api_key,
#         )

#         answer = ""

#         for chunk in llm.stream_generate(
#             prompt,
#             SYSTEM_PROMPT,
#         ):
#             answer += chunk
#             yield chunk

#         message_repository.create(
#             db=db,
#             session_id=session_uuid,
#             role="user",
#             content=message,
#         )

#         message_repository.create(
#             db=db,
#             session_id=session_uuid,
#             role="assistant",
#             content=answer,
#         )


ai_chat_service = AIChatService()