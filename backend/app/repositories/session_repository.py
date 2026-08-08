from sqlalchemy.orm import Session

from app.models.chat_session import ChatSession


class SessionRepository:

    def create(self, db: Session, title: str = "New Chat"):

        session = ChatSession(title=title)

        db.add(session)

        db.commit()

        db.refresh(session)

        return session

    def get(self, db: Session, session_id):

        return db.get(ChatSession, session_id)


session_repository = SessionRepository()