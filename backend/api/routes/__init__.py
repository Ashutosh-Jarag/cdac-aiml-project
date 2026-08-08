from fastapi import APIRouter

from .health import router as health_router
from .search import router as search_router
from .ml import router as ml_router
from .ai import router as ai_router

api_router = APIRouter(prefix="/api/v1")

api_router.include_router(health_router)
api_router.include_router(search_router)
api_router.include_router(ml_router)
api_router.include_router(ai_router)