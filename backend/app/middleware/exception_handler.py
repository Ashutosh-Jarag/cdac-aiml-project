"""
FILE CONTENTS & OVERVIEW:
-------------------------
This file defines a registry function for attaching custom global exception handlers to a FastAPI application instance.
It intercepts Pydantic validation errors (`RequestValidationError`) as well as unhandled runtime exceptions (`Exception`),
logs the details via Loguru, and converts them into standardized JSON error responses.

Functions:
  - register_exception_handlers: Binds custom exception handler functions to the provided FastAPI app instance.
"""

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from app.core.logger import logger


def register_exception_handlers(app: FastAPI):
    """
    Registers custom exception handlers on the provided FastAPI application instance.

    Configures handlers for:
      - `RequestValidationError`: Logs validation issues and returns a formatted HTTP 422 response.
      - `Exception`: Logs unhandled server errors with tracebacks and returns a standardized HTTP 500 response.

    Args:
        app (FastAPI): Target FastAPI application instance to attach handlers to.

    Returns:
        None
    """

    @app.exception_handler(RequestValidationError)
    async def validation_exception_handler(
        request: Request,
        exc: RequestValidationError,
    ):
        """
        Handles Pydantic request body/query validation failures.

        Args:
            request (Request): The incoming FastAPI request instance.
            exc (RequestValidationError): The exception containing validation failure details.

        Returns:
            JSONResponse: Standardized 422 response containing error details list.
        """
        logger.error(exc)

        return JSONResponse(
            status_code=422,
            content={
                "success": False,
                "message": "Validation Error",
                "errors": exc.errors(),
            },
        )

    @app.exception_handler(Exception)
    async def global_exception_handler(
        request: Request,
        exc: Exception,
    ):
        """
        Catch-all handler for unexpected runtime exceptions across the app.

        Args:
            request (Request): The incoming FastAPI request instance.
            exc (Exception): The unhandled exception object.

        Returns:
            JSONResponse: Standardized 500 response with internal server error payload.
        """
        logger.exception(exc)

        return JSONResponse(
            status_code=500,
            content={
                "success": False,
                "message": "Internal Server Error",
            },
        )