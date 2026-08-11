"""
FILE CONTENTS & OVERVIEW:
-------------------------
This file defines the API routes for the Artificial Intelligence (/ai) router module built with FastAPI.
It exposes HTTP endpoints for managing AI interaction workflows, including:
  1. File Uploads: Uploading files for AI-assisted operations.
  2. Chat Interactions: Non-streaming AI chat message handling and optional streaming template.
  3. Content Summarization: Requesting summaries for existing chat sessions.
  4. Session & History Management: Fetching chat history, listing all active chat sessions, 
     renaming sessions, and deleting chat sessions.

Helper functions for UUID conversion and uniform HTTP response formatting are also utilized.
"""

from pathlib import Path
import shutil
from uuid import UUID

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session

from api.schemas.ai import AIChatRequest, RenameChat, SummaryRequest
from app.database.connection import get_db
from app.middleware.response import success_response
from app.repositories.chat_repository import chat_repository
from app.repositories.message_repository import message_repository
from services.ai.chat_service import ai_chat_service
from services.ai.summary_service import summary_service
from services.ai.upload_service import upload_service

# Base directory setup for storing uploaded files
UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

# Router initialization for AI endpoints
router = APIRouter(
    prefix="/ai",
    tags=["Artificial Intelligence"],
)


def parse_uuid(session_id: str) -> UUID:
    """
    Parses a string representation of a UUID into a standard Python UUID object.

    Args:
        session_id (str): The raw string ID expected to be in standard UUID format.

    Returns:
        UUID: The parsed UUID object.

    Raises:
        HTTPException: HTTP 400 Bad Request error if the session_id string is not a valid UUID format.
    """
    try:
        return UUID(session_id)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid UUID format: {session_id}",
        )


@router.post("/upload")
async def upload(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    """
    Handles file upload requests by saving incoming files to local storage and processing them.

    Args:
        file (UploadFile): The uploaded file payload provided via form-data.
        db (Session): Database session dependency injected by FastAPI.

    Returns:
        dict: Standardized success response containing upload results and message.
    """
    # Ensure safe file name handling
    file_path = UPLOAD_DIR / Path(file.filename).name

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    result = upload_service.upload(
        db=db,
        file_path=str(file_path),
    )

    return success_response(
        data=result,
        message="File uploaded successfully",
    )


@router.post("/chat")
def chat(
    request: AIChatRequest,
    db: Session = Depends(get_db),
):
    """
    Sends a message to an AI provider and returns the AI-generated response.

    Args:
        request (AIChatRequest): Request body containing chat message, session ID, 
                                 AI provider preference (default: "gemini"), and optional API key.
        db (Session): Database session dependency injected by FastAPI.

    Returns:
        dict: Standardized success response containing the generated chat response payload.
    """
    result = ai_chat_service.chat(
        db=db,
        message=request.message,
        session_id=request.session_id,
        provider=request.provider or "gemini",
        api_key=request.api_key,
    )

    return success_response(
        data=result,
        message="Chat completed",
    )


@router.post("/summary")
def summary(request: SummaryRequest):
    """
    Generates a summary of a chat session based on a requested summary mode.

    Args:
        request (SummaryRequest): Request body containing session_id and summary mode parameters.

    Returns:
        dict: Standardized success response containing the summary output.
    """
    result = summary_service.summarize(
        request.session_id,
        request.mode,
    )

    return success_response(
        data=result,
        message="Summary generated",
    )


@router.get("/history/{session_id}")
def history(
    session_id: str,
    db: Session = Depends(get_db),
):
    """
    Retrieves the complete message history for a given chat session.

    Args:
        session_id (str): The unique string identifier of the chat session.
        db (Session): Database session dependency injected by FastAPI.

    Returns:
        dict: Standardized success response containing a formatted list of messages with role, content, and timestamp.
    """
    session_uuid = parse_uuid(session_id)

    messages = message_repository.get_history(
        db=db,
        session_id=session_uuid,
    )

    return success_response(
        data=[
            {
                "role": m.role,
                "content": m.content,
                "created_at": (
                    m.created_at.isoformat() if hasattr(m, "created_at") and m.created_at else None
                ),
            }
            for m in messages
        ]
    )


@router.get("/sessions")
def sessions(
    db: Session = Depends(get_db),
):
    """
    Fetches a list of all existing chat sessions with their metadata.

    Args:
        db (Session): Database session dependency injected by FastAPI.

    Returns:
        dict: Standardized success response containing a list of sessions with ID, title, created_at, and updated_at timestamps.
    """
    chats = chat_repository.all(db)

    return success_response(
        data=[
            {
                "id": str(chat.id),
                "title": chat.title,
                "created_at": (
                    chat.created_at.isoformat()
                    if hasattr(chat, "created_at") and chat.created_at
                    else None
                ),
                "updated_at": (
                    chat.updated_at.isoformat()
                    if hasattr(chat, "updated_at") and chat.updated_at
                    else None
                ),
            }
            for chat in chats
        ]
    )


@router.delete("/sessions/{session_id}")
def delete_chat(
    session_id: str,
    db: Session = Depends(get_db),
):
    """
    Deletes a specific chat session by its ID.

    Args:
        session_id (str): The unique string identifier of the chat session to delete.
        db (Session): Database session dependency injected by FastAPI.

    Returns:
        dict: Standardized success response confirming chat deletion.
    """
    session_uuid = parse_uuid(session_id)

    chat_repository.delete(
        db,
        session_uuid,
    )

    return success_response(message="Chat deleted")


@router.put("/sessions/{session_id}")
def rename_chat(
    session_id: str,
    request: RenameChat,
    db: Session = Depends(get_db),
):
    """
    Renames the title of an existing chat session.

    Args:
        session_id (str): The unique string identifier of the chat session to rename.
        request (RenameChat): Request body containing the new title for the chat.
        db (Session): Database session dependency injected by FastAPI.

    Returns:
        dict: Standardized success response containing updated session ID and new title.
    """
    session_uuid = parse_uuid(session_id)

    chat = chat_repository.rename(
        db,
        session_uuid,
        request.title,
    )

    return success_response(
        data={
            "id": str(chat.id),
            "title": chat.title,
        }
    )


# @router.post("/chat/stream")
# def stream_chat(
#     request: AIChatRequest,
#     db: Session = Depends(get_db),
# ):
#     """
#     Streams AI chat responses in real-time using text/plain chunks (Currently commented out).
#
#     Args:
#         request (AIChatRequest): Request body containing message, session_id, provider, and API key.
#         db (Session): Database session dependency injected by FastAPI.
#
#     Returns:
#         StreamingResponse: Real-time chunked response from the streaming generator.
#     """
#     generator = ai_chat_service.stream(
#         db=db,
#         message=request.message,
#         session_id=request.session_id,
#         provider=request.provider or "gemini",
#         api_key=request.api_key,
#     )
#
#     return StreamingResponse(
#         generator,
#         media_type="text/plain",
#     )