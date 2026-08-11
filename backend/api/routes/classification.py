"""
FILE CONTENTS & OVERVIEW:
-------------------------
This file defines the API routing structure for classification-related operations within a FastAPI application.
It creates a dedicated APIRouter instance scoped to the "/classification" endpoint group.

Key endpoints:
  - GET /classification: Health check / status verification route to confirm router availability.
"""

from fastapi import APIRouter

# Initialize the Classification router with a prefix and OpenAPI tags
router = APIRouter(
    prefix="/classification",
    tags=["Classification"]
)


@router.get("")
def test():
    """
    Verifies that the classification route group is active and responding correctly.

    Args:
        None

    Returns:
        dict: A JSON-serializable dictionary containing a confirmation message status.
              Example: {"message": "Classification route working"}
    """
    return {
        "message": "Classification route working"
    }