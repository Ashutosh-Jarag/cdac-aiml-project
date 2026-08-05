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

UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

router = APIRouter(
    prefix="/ai",
    tags=["Artificial Intelligence"],
)


def parse_uuid(session_id: str) -> UUID:
    """Helper to safely parse string IDs to UUID or raise a 400 Bad Request."""
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
#     generator = ai_chat_service.stream(
#         db=db,
#         message=request.message,
#         session_id=request.session_id,
#         provider=request.provider or "gemini",
#         api_key=request.api_key,
#     )

#     return StreamingResponse(
#         generator,
#         media_type="text/plain",
#     )