"""
FILE CONTENTS & OVERVIEW:
-------------------------
This file defines the `SessionRepository` class, providing data access layer (DAL) operations
for creating and retrieving `ChatSession` entities in the database.

Key functionality:
  - create(): Instantiates, adds, commits, and returns a new `ChatSession` record with an optional custom title.
  - get(): Fetches a single `ChatSession` instance by its primary key ID.

Exports:
  - session_repository: Singleton instance of `SessionRepository` for application-wide database operations.
"""

from typing import Any, Optional
from sqlalchemy.orm import Session

from app.models.chat_session import ChatSession


class SessionRepository:
    """
    Repository class providing creation and retrieval operations for `ChatSession` database records.
    """

    def create(self, db: Session, title: str = "New Chat") -> ChatSession:
        """
        Creates and persists a new `ChatSession` record in the database.

        Args:
            db (Session): Active SQLAlchemy database session.
            title (str, optional): Title for the new chat session. Defaults to "New Chat".

        Returns:
            ChatSession: The newly created and refreshed `ChatSession` ORM object.
        """
        session = ChatSession(title=title)

        db.add(session)
        db.commit()
        db.refresh(session)

        return session

    def get(self, db: Session, session_id: Any) -> Optional[ChatSession]:
        """
        Retrieves a `ChatSession` record by its primary key identifier.

        Args:
            db (Session): Active SQLAlchemy database session.
            session_id (UUID | str): Unique identifier of the chat session to retrieve.

        Returns:
            Optional[ChatSession]: The matching `ChatSession` ORM object if found, otherwise None.
        """
        return db.get(ChatSession, session_id)


# Global singleton instance of SessionRepository
session_repository = SessionRepository()