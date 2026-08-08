from fastapi import APIRouter

router = APIRouter(
    prefix="/classification",
    tags=["Classification"]
)


@router.get("")
def test():
    return {
        "message": "Classification route working"
    }