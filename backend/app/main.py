"""
PromptShield — Main Application Entry Point.

FastAPI application with lifespan management, CORS, and route registration.

Run with:
    uvicorn app.main:app --reload --port 8000
"""

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import api_router
from app.config import get_settings
from app.core.exceptions import (
    PromptShieldError,
    generic_exception_handler,
    promptshield_exception_handler,
)
from app.core.logging import get_logger, setup_logging
from app.proxy.client import proxy_client

logger = get_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifespan handler.

    Startup: Initialize logging, start proxy client.
    Shutdown: Close proxy client connections.
    """
    # --- Startup ---
    setup_logging()
    settings = get_settings()

    logger.info(
        "starting",
        app_name=settings.app_name,
        host=settings.host,
        port=settings.port,
        provider="groq",
        target_url=settings.proxy_target_url,
    )

    await proxy_client.start()

    yield

    # --- Shutdown ---
    await proxy_client.stop()
    logger.info("shutdown_complete")


def create_app() -> FastAPI:
    """Create and configure the FastAPI application."""
    settings = get_settings()

    app = FastAPI(
        title=settings.app_name,
        description="Semantic & Intent Drift Detection Proxy for LLM Applications",
        version="1.0.0",
        lifespan=lifespan,
    )

    # CORS — allow frontend (Next.js dev server)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[
            "http://localhost:3000",
            "http://127.0.0.1:3000",
            "http://localhost:3001",
        ],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Exception handlers
    app.add_exception_handler(PromptShieldError, promptshield_exception_handler)
    app.add_exception_handler(Exception, generic_exception_handler)

    # Register routes
    app.include_router(api_router)

    return app


# Module-level app instance for uvicorn
app = create_app()
