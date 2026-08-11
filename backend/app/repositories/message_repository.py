"""
FILE CONTENTS & OVERVIEW:
-------------------------
This file defines the `MessageRepository` class, providing data access layer (DAL) operations
for managing `ChatMessage` entities in the database.

Key functionality:
  - create(): Instantiates, adds, commits, and returns a new `ChatMessage` associated with a chat session.
  - get_history(): Retrieves all historical chat messages for a specific session ordered chronologically.

Exports:
  - message_repository: Singleton instance of `MessageRepository` for application-wide database operations.
"""

from typing import Any
from sqlalchemy.orm import Session

from app.models.chat_message import ChatMessage


class MessageRepository:
    """
    Repository class providing CRUD and query operations for `ChatMessage` database records.
    """

    def create(
        self,
        db: Session,
        session_id: Any,
        role: str,
        content: str,
    ) -> ChatMessage:
        """
        Creates and persists a new `ChatMessage` record in the database.

        Args:
            db (Session): Active SQLAlchemy database session.
            session_id (UUID | str): Unique ID of the chat session associated with the message.
            role (str): Role of the message sender (e.g., 'user', 'assistant', 'system').
            content (str): The body text/content of the chat message.

        Returns:
            ChatMessage: The newly created and refreshed `ChatMessage` ORM object.
        """
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
        session_id: Any,
    ) -> list[ChatMessage]:
        """
        Retrieves all chat messages for a given session ordered chronologically by creation timestamp.

        Args:
            db (Session): Active SQLAlchemy database session.
            session_id (UUID | str): Unique ID of the target chat session.

        Returns:
            list[ChatMessage]: List of `ChatMessage` ORM objects sorted from oldest to newest.
        """
        return (
            db.query(ChatMessage)
            .filter(ChatMessage.session_id == session_id)
            .order_by(ChatMessage.created_at.asc())
            .all()
        )


# Global singleton instance of MessageRepository
message_repository = MessageRepository()