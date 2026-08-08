from app.repositories.message_repository import message_repository

from services.ai.retriever import retriever

from app.core.ai_manager import ai_manager
from services.ai.graph.prompts import SYSTEM_PROMPT
from services.ai.title_service import title_service
from app.repositories.chat_repository import chat_repository


def load_history(state):

    history = message_repository.get_history(
        db=state["db"],
        session_id=state["session_uuid"],
    )

    conversation = ""

    for msg in history:

        conversation += f"{msg.role}: {msg.content}\n"

    state["history"] = conversation

    return state

def retrieve_context(state):

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


from app.core.ai_manager import ai_manager


def generate_answer(state):

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


def save_messages(state):

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

def generate_title(state):

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