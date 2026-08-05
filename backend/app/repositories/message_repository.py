from sqlalchemy.orm import Session

from app.models.chat_message import ChatMessage


class MessageRepository:

    def create(
        self,
        db: Session,
        session_id,
        role: str,
        content: str,
    ):

        message = ChatMessage(
            session_id=session_id,
            role=role,
            content=content,
        )

        db.add(message)
        db.commit()
        db.refresh(message)

        return message

    def get_history(
        self,
        db: Session,
        session_id,
    ):

        return (
            db.query(ChatMessage)
            .filter(ChatMessage.session_id == session_id)
            .order_by(ChatMessage.created_at.asc())
            .all()
        )


message_repository = MessageRepository()