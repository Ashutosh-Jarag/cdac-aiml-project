from fastapi import APIRouter

from api.schemas.search import SearchRequest

from services.search_service import search_service

from app.middleware.response import success_response

router = APIRouter(
    prefix="/search",
    tags=["Search"]
)


@router.post("")
def search(
    request: SearchRequest
):

    result = search_service.search(
        request.query,
        request.top_k
    )

    return success_response(
        data=result.model_dump(),
        message="Search completed successfully"
    )