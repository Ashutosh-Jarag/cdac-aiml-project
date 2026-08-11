"""
FILE CONTENTS & OVERVIEW:
-------------------------
This file defines custom asynchronous HTTP exception handlers for a FastAPI application.
It provides error handling logic to transform application-specific exceptions (AppException)
and unhandled generic runtime exceptions (Exception) into standardized JSON error response structures.

Functions:
  - app_exception_handler: Handles custom domain/application exceptions with dynamic status codes and messages.
  - generic_exception_handler: Catch-all handler for unhandled exceptions, returning a generic 500 Internal Server Error.
"""

from fastapi import Request
from fastapi.responses import JSONResponse

from app.core.exceptions import AppException


async def app_exception_handler(
    request: Request,
    exc: AppException,
):
    """
    Handles custom application-level exceptions (AppException) and formats them into a standardized JSON response.

    Args:
        request (Request): The incoming FastAPI HTTP request instance.
        exc (AppException): The caught application exception containing custom `status_code` and `message` attributes.

    Returns:
        JSONResponse: A structured JSON response with the exception's HTTP status code, `success=False`, and the error message.
    """
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "message": exc.message,
            "data": None,
        },
    )


async def generic_exception_handler(
    request: Request,
    exc: Exception,
):
    """
    Catch-all exception handler for unexpected or unhandled server errors.

    Args:
        request (Request): The incoming FastAPI HTTP request instance.
        exc (Exception): The unhandled exception instance caught during request execution.

    Returns:
        JSONResponse: A 500 Internal Server Error JSON response with `success=False` and a standard message.
    """
    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "message": "Internal Server Error",
            "data": None,
        },
    )