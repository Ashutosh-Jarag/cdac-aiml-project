"""
FILE CONTENTS & OVERVIEW:
-------------------------
This file defines individual execution node functions utilized within the LangGraph chat workflow pipeline.
Each node takes a shared `ChatState` object, performs a specific stage of processing, and returns the updated state.

Node Pipeline Functions:
  - load_history(): Formats and loads existing conversation history for the session from the database.
  - retrieve_context(): Performs similarity search against vector storage to gather context and build document references.
  - generate_answer(): Constructs prompt templates and invokes the configured LLM provider to generate responses.
  - save_messages(): Persists the incoming user question and the newly generated assistant answer back to the database.
  - generate_title(): Auto-generates a title for new chat sessions following the initial user-assistant interaction.
"""

from app.repositories.message_repository import message_repository
from services.ai.retriever import retriever
from app.core.ai_manager import ai_manager
from services.ai.graph.prompts import SYSTEM_PROMPT
from services.ai.title_service import title_service
from app.repositories.chat_repository import chat_repository


def load_history(state: dict) -> dict:
    """
    Loads historical chat messages for the current session and formats them into a single transcript string.

    Args:
        state (dict): Current workflow state containing database session (`db`) and session UUID (`session_uuid`).

    Returns:
        dict: Updated workflow state containing the formatted conversation `history` string.
    """
    history = message_repository.get_history(
        db=state["db"],
        session_id=state["session_uuid"],
    )

    conversation = ""

    for msg in history:
        conversation += f"{msg.role}: {msg.content}\n"

    state["history"] = conversation

    return state


def retrieve_context(state: dict) -> dict:
    """
    Retrieves relevant document chunks and metadata matching the user's question from vector storage.

    Args:
        state (dict): Current workflow state containing `session_id` and the user `question`.

    Returns:
        dict: Updated workflow state containing joined `context` string and structured `references` metadata.
    """
    result = retriever.retrieve(
        session_id=state["session_id"],
        question=state["question"],
    )

    documents = result["documents"][0]
    metadatas = result["metadatas"][0]

    state["context"] = "\n\n".join(documents)

    state["references"] = []

    for doc, meta in zip(documents, metadatas):
        state["references"].append(
            {
                "text": doc,
                "source": meta.get("source", ""),
                "page": meta.get("page", 1),
            }
        )

    return state


def generate_answer(state: dict) -> dict:
    """
    Generates an AI completion response using the specified LLM provider and system prompt.

    Args:
        state (dict): Current workflow state containing `history`, `context`, `question`, 
                      AI `provider`, and API credentials (`api_key`).

    Returns:
        dict: Updated workflow state containing the generated LLM `answer`.
    """
    prompt = f"""
Conversation

{state["history"]}

Context

{state["context"]}

Question

{state["question"]}
"""

    llm = ai_manager.get_provider(
        provider=state["provider"],
        api_key=state["api_key"],
    )

    answer = llm.generate(
        prompt=prompt,
        system_prompt=SYSTEM_PROMPT,
    )

    state["answer"] = answer

    return state


def save_messages(state: dict) -> dict:
    """
    Persists user input and the newly generated assistant response into the database message repository.

    Args:
        state (dict): Current workflow state containing `db`, `session_uuid`, `question`, and `answer`.

    Returns:
        dict: The state dictionary after persisting the user and assistant messages.
    """
    message_repository.create(
        db=state["db"],
        session_id=state["session_uuid"],
        role="user",
        content=state["question"],
    )

    message_repository.create(
        db=state["db"],
        session_id=state["session_uuid"],
        role="assistant",
        content=state["answer"],
    )

    return state


def generate_title(state: dict) -> dict:
    """
    Triggers chat session title generation after the first exchange (2 messages) and updates the database record.

    Args:
        state (dict): Current workflow state containing `db`, `session_uuid`, `question`, `provider`, and `api_key`.

    Returns:
        dict: The unmodified or updated workflow state.
    """
    history = message_repository.get_history(
        db=state["db"],
        session_id=state["session_uuid"],
    )

    # Only generate title after the first user + assistant exchange
    if len(history) != 2:
        return state

    title = title_service.generate(
        question=state["question"],
        provider=state["provider"],
        api_key=state["api_key"],
    )

    chat_repository.rename(
        db=state["db"],
        session_id=state["session_uuid"],
        title=title,
    )

    return state