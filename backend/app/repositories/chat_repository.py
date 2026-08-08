from typing import Optional
from sqlalchemy.orm import Session

from app.models.chat_session import ChatSession



class ChatRepository:

    def all(self, db: Session) -> list[ChatSession]:
        return (
            db.query(ChatSession)
            .order_by(ChatSession.updated_at.desc())
            .all()
        )

    def get(self, db: Session, session_id: str) -> Optional[ChatSession]:
        return (
            db.query(ChatSession)
            .filter(ChatSession.id == session_id)
            .first()
        )

    def delete(self, db: Session, session_id: str) -> None:
        chat = self.get(db, session_id)
        if chat:
            db.delete(chat)
            db.commit()

    def get_or_create(self, db: Session, session_id: str) -> ChatSession:
        chat = self.get(db, session_id)
        if not chat:
            chat = ChatSession(
                id=session_id,
                title="New Chat",
            )
            db.add(chat)
            db.commit()
            db.refresh(chat)

        return chat

    def rename(
        self,
        db: Session,
        session_id: str,
        title: str,
    ) -> Optional[ChatSession]:
        chat = db.get(ChatSession, session_id)

        if chat:
            chat.title = title
            db.commit()
            db.refresh(chat)

        return chat


chat_repository = ChatRepository()