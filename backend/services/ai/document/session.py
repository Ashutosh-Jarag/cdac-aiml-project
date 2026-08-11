"""
FILE CONTENTS & OVERVIEW:
-------------------------
This file defines the `SessionManager` utility class, providing session management functionality.
It contains static helper methods for generating unique session identifiers for application workflows.

Key functionality:
  - create_session(): Generates and returns a unique standard UUID v4 string.

Exports:
  - session_manager: Singleton instance of `SessionManager` for application-wide session identification operations.
"""

import uuid


class SessionManager:
    """
    Utility manager class responsible for creating and handling unique session identifiers.
    """

    @staticmethod
    def create_session() -> str:
        """
        Generates a new universally unique identifier (UUID v4) formatted as a string.

        Args:
            None

        Returns:
            str: Standard string representation of a newly generated UUID v4 (e.g., "123e4567-e89b-12d3-a456-426614174000").
        """
        return str(uuid.uuid4())


# Global singleton instance of SessionManager
session_manager = SessionManager()