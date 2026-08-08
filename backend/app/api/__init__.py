"""PromptShield API package — router aggregation."""

from fastapi import APIRouter

from app.api.alerts import router as alerts_router
from app.api.health import router as health_router
from app.api.metrics import router as metrics_router
from app.api.proxy import router as proxy_router
from app.api.sessions import router as sessions_router

api_router = APIRouter()

api_router.include_router(health_router)
api_router.include_router(proxy_router)
api_router.include_router(sessions_router)
api_router.include_router(alerts_router)
api_router.include_router(metrics_router)

__all__ = ["api_router"]
