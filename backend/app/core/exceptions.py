"""
FILE CONTENTS & OVERVIEW:
-------------------------
This file defines the base application exception class (`AppException`) for custom error handling.
It extends Python's built-in `Exception` class to allow raising domain-specific runtime errors 
accompanied by custom HTTP status codes and user-friendly message strings.

Classes:
  - AppException: Custom base exception class for application-level errors.
"""


class AppException(Exception):
    """
    Custom exception class for application-level operational errors.

    Attributes:
        message (str): Descriptive error message detailing the reason for the exception.
        status_code (int): HTTP status code associated with the error (defaults to 400 Bad Request).
    """

    def __init__(
        self,
        message: str,
        status_code: int = 400,
    ):
        """
        Initializes the AppException with a custom message and HTTP status code.

        Args:
            message (str): Explanatory error message string.
            status_code (int): Corresponding HTTP status code. Defaults to 400.

        Returns:
            None
        """
        self.message = message
        self.status_code = status_code