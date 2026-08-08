"""
PromptShield Metrics API.

GET /metrics — dashboard-level system metrics.
"""

from fastapi import APIRouter

from app.schemas.responses import MetricsResponse
from app.services.metrics_service import metrics_service
from app.sessions.manager import session_manager

router = APIRouter(tags=["metrics"])


@router.get("/metrics", response_model=MetricsResponse)
async def get_metrics() -> MetricsResponse:
    """
    Return dashboard-level metrics.

    Computed from in-memory state.
    """
    summary = await metrics_service.get_summary()
    active_sessions = await session_manager.get_active_count()

    return MetricsResponse(
        requests=summary["requests"],
        active_sessions=active_sessions,
        flagged=summary["flagged"],
        blocked=summary["blocked"],
        average_latency_ms=summary["average_latency_ms"],
        uptime=summary["uptime"],
    )
