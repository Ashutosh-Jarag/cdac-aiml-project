"""
FILE CONTENTS & OVERVIEW:
-------------------------
This file defines the health check API router module for the FastAPI application.
It exposes system health monitoring routes under the "/health" prefix to verify that the
API service is up, functional, and running the expected version.

Key endpoints:
  - GET /health: Health check endpoint returning status metrics and version info.
"""

from fastapi import APIRouter

from app.middleware.response import success_response

# Initialize the Health router with a prefix and OpenAPI tags
router = APIRouter(
    prefix="/health",
    tags=["Health"],
)


@router.get("")
def health():
    """
    Checks the system health and operational status of the API service.

    Args:
        None

    Returns:
        dict: Standardized success response envelope containing system health metadata:
              - data (dict): Dictionary with service 'status' ("healthy") and application 'version' ("1.0.0").
              - message (str): Status confirmation message ("API is running").
    """
    return success_response(
        data={
            "status": "healthy",
            "version": "1.0.0",
        },
        message="API is running",
    )