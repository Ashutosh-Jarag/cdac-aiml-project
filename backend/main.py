"""
FastAPI Application Entry Point Module
---------------------------------------
This module initializes and configures the core FastAPI application instance, including 
middleware, global exception handlers, startup events for machine learning model loading, 
and top-level API router registration.

Key Configurations:
  - CORS Middleware: Configured for frontend origins (e.g., local React/Vite development server).
  - Exception Handlers: Global mapping for `AppException` and generic `Exception` types.
  - Startup Events: Eager model initialization via `model_loader`.
  - API Router: Inclusion of central `api_router` for endpoint routing.

Exports:
  - app: Main FastAPI application instance.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.routes import api_router
from app.middleware.exception_handler import register_exception_handlers
from app.core.model_loader import model_loader

from app.core.exceptions import AppException
from app.core.exception_handler import (
    app_exception_handler,
    generic_exception_handler,
)

from app.core.config import settings

# Optional tracing integration initialization
# import app.core.langsmith

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
)

# Configure Cross-Origin Resource Sharing (CORS) middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register custom global exception handlers
app.add_exception_handler(
    AppException,
    app_exception_handler,
)

app.add_exception_handler(
    Exception,
    generic_exception_handler,
)


@app.on_event("startup")
async def startup():
    """
    FastAPI startup event handler that triggers pre-loading of machine learning
    models and associated assets prior to serving application requests.
    """
    model_loader.load_models()


# Additional middleware exception handler registration
register_exception_handlers(app)

# Include API endpoints router
app.include_router(api_router)