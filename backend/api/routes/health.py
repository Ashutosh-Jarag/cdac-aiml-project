from fastapi import APIRouter

from app.middleware.response import success_response

router = APIRouter(
    prefix="/health",
    tags=["Health"],
)


@router.get("")
def health():

    return success_response(
        data={
            "status": "healthy",
            "version": "1.0.0",
        },
        message="API is running",
    )