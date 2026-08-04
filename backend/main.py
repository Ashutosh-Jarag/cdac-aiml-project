from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.routes import api_router
from app.middleware.exception_handler import register_exception_handlers
from app.core.model_loader import model_loader

from app.core.config import settings

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.CORS_ORIGINS],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup():

    model_loader.load_models()

# @app.on_event("startup")
# async def startup():

#     logger.info("Starting ResearchAI API")

#     model_loader.load_models()

#     logger.success("API Ready")


register_exception_handlers(app)

app.include_router(api_router)