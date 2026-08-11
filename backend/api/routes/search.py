"""
FILE CONTENTS & OVERVIEW:
-------------------------
This file defines the search API router module for the FastAPI application.
It exposes HTTP POST endpoints under the "/search" prefix to process query-based searches
using an underlying search service.

Key endpoints:
  - POST /search: Executes search queries with a configurable result limit (top_k).
"""

from fastapi import APIRouter

from api.schemas.search import SearchRequest

from services.search_service import search_service

from app.middleware.response import success_response

# Initialize the Search router with a prefix and OpenAPI tags
router = APIRouter(
    prefix="/search",
    tags=["Search"]
)


@router.post("")
def search(
    request: SearchRequest
):
    """
    Executes a search operation based on the user's query parameters.

    Args:
        request (SearchRequest): Request body containing the search 'query' string 
                                 and an optional 'top_k' integer limit for returned results.

    Returns:
        dict: Standardized success response containing:
              - data (dict): The serialized dictionary representation of the search results object.
              - message (str): Status confirmation message ("Search completed successfully").
    """
    result = search_service.search(
        request.query,
        request.top_k
    )

    return success_response(
        data=result.model_dump(),
        message="Search completed successfully"
    )