"""
FILE CONTENTS & OVERVIEW:
-------------------------
This file provides utility helper functions for building standardized HTTP JSON responses across API endpoints.
It ensures uniform formatting for success and error responses returned by FastAPI routes.

Functions:
  - success_response: Constructs a JSONResponse with a `success=True` status, custom payload data, message, and status code.
  - error_response: Constructs a JSONResponse with a `success=False` status, error message, and status code.
"""

from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse


def success_response(
    data=None,
    message="Success",
    status_code=200,
):
    """
    Constructs a standardized JSON success response.

    Encodes complex Python data types (e.g., Pydantic models, datetimes, ORM objects) 
    into JSON-compatible data structures using FastAPI's `jsonable_encoder`.

    Args:
        data (Any, optional): Payload data returned by the API endpoint. Defaults to None.
        message (str, optional): Success message description. Defaults to "Success".
        status_code (int, optional): HTTP status code for the response. Defaults to 200.

    Returns:
        JSONResponse: Standardized JSON response object containing success status, message, and data.
    """
    return JSONResponse(
        status_code=status_code,
        content=jsonable_encoder(
            {
                "success": True,
                "message": message,
                "data": data,
            }
        ),
    )


def error_response(
    message="Error",
    status_code=400,
):
    """
    Constructs a standardized JSON error response.

    Args:
        message (str, optional): Explanatory error message string. Defaults to "Error".
        status_code (int, optional): HTTP error status code. Defaults to 400.

    Returns:
        JSONResponse: Standardized JSON response object containing success status set to False and the error message.
    """
    return JSONResponse(
        status_code=status_code,
        content={
            "success": False,
            "message": message,
        },
    )