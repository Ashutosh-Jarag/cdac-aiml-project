"""
FILE CONTENTS & OVERVIEW:
-------------------------
This file defines standard, reusable API response wrapper schemas using Pydantic.
It provides generic models for structuring consistent JSON responses across all HTTP endpoints:
  1. APIResponse: Universal wrapper for successful or stateful responses, carrying payload data and messages.
  2. ErrorResponse: Dedicated schema for standardized error responses with default failure status.
"""

from typing import Any, Optional
from pydantic import BaseModel


class APIResponse(BaseModel):
    """
    Generic wrapper schema for standard API responses.

    Attributes:
        success (bool): Indicates whether the request was processed successfully.
        message (str): Descriptive status message accompanying the response.
        data (Optional[Any]): Payload returned by the endpoint. Can be any valid JSON-serializable structure. Defaults to None.
    """
    success: bool
    message: str
    data: Optional[Any] = None


class ErrorResponse(BaseModel):
    """
    Standardized schema for error responses returned during request failures.

    Attributes:
        success (bool): Indicates request success state. Hardcoded default is False.
        message (str): Detailed error message or reason for the request failure.
    """
    success: bool = False
    message: str