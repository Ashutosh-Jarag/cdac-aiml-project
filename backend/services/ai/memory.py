"""
FILE CONTENTS & OVERVIEW:
-------------------------
This file defines the `ConversationMemory` class, which manages in-memory conversation history.
It serves as a lightweight, non-persistent store for tracking message history per session ID during runtime.

Key functionality:
  - add(): Appends a message object (`role` and `content`) to the memory list associated with a given `session_id`.
  - get(): Retrieves the full list of stored message dictionaries for a given `session_id`, returning an empty list if not found.

Exports:
  - conversation_memory: Singleton instance of `ConversationMemory` for managing runtime chat memory.
"""

from typing import Any


class ConversationMemory:
    """
    In-memory store for tracking session-based conversation messages.
    """

    def __init__(self):
        """
        Initializes an empty conversation memory storage dictionary.

        Args:
            None

        Returns:
            None
        """
        self.memory: dict[str, list[dict[str, str]]] = {}

    def add(self, session_id: str, role: str, message: str) -> None:
        """
        Appends a new message to the conversation history for a given session ID.

        Args:
            session_id (str): Unique identifier for the chat session.
            role (str): Role of the message sender (e.g., 'user', 'assistant', 'system').
            message (str): Body text of the message to store.

        Returns:
            None
        """
        if session_id not in self.memory:
            self.memory[session_id] = []

        self.memory[session_id].append({
            "role": role,
            "content": message,
        })

    def get(self, session_id: str) -> list[dict[str, str]]:
        """
        Retrieves all stored conversation messages for a specific session ID.

        Args:
            session_id (str): Unique identifier for the chat session.

        Returns:
            list[dict[str, str]]: List of message dictionaries containing 'role' and 'content', 
                                  or an empty list if the session_id does not exist.
        """
        return self.memory.get(session_id, [])


# Global singleton instance of ConversationMemory
conversation_memory = ConversationMemory()