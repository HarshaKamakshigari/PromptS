"""
PromptShield Alerts API.

GET /alerts — list security alerts.

Phase 1: Returns empty list. The endpoint exists so frontend
architecture is stable from day one.
"""

from fastapi import APIRouter

from app.schemas.alerts import AlertSchema

router = APIRouter(tags=["alerts"])


# In-memory alert store (Phase 1: empty)
_alerts: list[AlertSchema] = []


@router.get("/alerts", response_model=list[AlertSchema])
async def list_alerts() -> list[AlertSchema]:
    """
    List all security alerts.

    Phase 1: Returns empty list unless detection is enabled.
    """
    return _alerts
