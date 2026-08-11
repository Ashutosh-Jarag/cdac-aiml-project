"""
FILE CONTENTS & OVERVIEW:
-------------------------
This file defines the `ChatRepository` class, providing data access layer (DAL) operations for managing
`ChatSession` entities in the database.

Key functionality:
  - all(): Retrieves all chat sessions ordered by `updated_at` in descending order.
  - get(): Fetches a single chat session by its UUID string ID.
  - delete(): Removes a chat session record from the database and commits the transaction.
  - get_or_create(): Fetches an existing chat session or creates a new one with a default title if not found.
  - rename(): Updates the title of an existing chat session.

Exports:
  - chat_repository: Singleton instance of `ChatRepository` for application-wide database access.
"""

from typing import Optional
from sqlalchemy.orm import Session

from app.models.chat_session import ChatSession


class ChatRepository:
    """
    Repository class providing CRUD and query operations for `ChatSession` database records.
    """

    def all(self, db: Session) -> list[ChatSession]:
        """
        Retrieves all chat sessions from the database ordered by last updated timestamp descending.

        Args:
            db (Session): Active SQLAlchemy database session.

        Returns:
            list[ChatSession]: List of all `ChatSession` ORM objects sorted from newest to oldest.
        """
        return (
            db.query(ChatSession)
            .order_by(ChatSession.updated_at.desc())
            .all()
        )

    def get(self, db: Session, session_id: str) -> Optional[ChatSession]:
        """
        Retrieves a single chat session by its unique ID.

        Args:
            db (Session): Active SQLAlchemy database session.
            session_id (str): Unique identifier of the target chat session.

        Returns:
            Optional[ChatSession]: The matching `ChatSession` ORM object if found, otherwise None.
        """
        return (
            db.query(ChatSession)
            .filter(ChatSession.id == session_id)
            .first()
        )

    def delete(self, db: Session, session_id: str) -> None:
        """
        Deletes a chat session from the database if it exists.

        Args:
            db (Session): Active SQLAlchemy database session.
            session_id (str): Unique identifier of the chat session to delete.

        Returns:
            None
        """
        chat = self.get(db, session_id)
        if chat:
            db.delete(chat)
            db.commit()

    def get_or_create(self, db: Session, session_id: str) -> ChatSession:
        """
        Fetches an existing chat session by ID or creates, saves, and returns a new session if none exists.

        Args:
            db (Session): Active SQLAlchemy database session.
            session_id (str): Unique identifier of the chat session.

        Returns:
            ChatSession: The existing or newly created `ChatSession` object.
        """
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
        """
        Renames an existing chat session with a new title string.

        Args:
            db (Session): Active SQLAlchemy database session.
            session_id (str): Unique identifier of the chat session to rename.
            title (str): New display title for the chat session.

        Returns:
            Optional[ChatSession]: The updated `ChatSession` ORM object if found, otherwise None.
        """
        chat = db.get(ChatSession, session_id)

        if chat:
            chat.title = title
            db.commit()
            db.refresh(chat)

        return chat


# Global singleton instance of ChatRepository
chat_repository = ChatRepository()