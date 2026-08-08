"""
PromptShield Sessions API.

GET /sessions         — list all sessions
GET /sessions/{id}    — session detail
GET /sessions/{id}/drift — drift timeline for a session
"""

from fastapi import APIRouter, HTTPException, Query

from app.schemas.sessions import DriftPoint, SessionDetail, SessionSchema, SessionStatus
from app.services import session_service

router = APIRouter(prefix="/sessions", tags=["sessions"])


@router.get("", response_model=list[SessionSchema])
async def list_sessions(
    status: SessionStatus | None = Query(None, description="Filter by session status"),
) -> list[SessionSchema]:
    """List all sessions, optionally filtered by status."""
    return await session_service.list_sessions(status_filter=status)


@router.get("/{session_id}", response_model=SessionDetail)
async def get_session(session_id: str) -> SessionDetail:
    """Get detailed information about a specific session."""
    detail = await session_service.get_session_detail(session_id)
    if detail is None:
        raise HTTPException(status_code=404, detail=f"Session '{session_id}' not found")
    return detail


@router.get("/{session_id}/drift", response_model=list[DriftPoint])
async def get_session_drift(session_id: str) -> list[DriftPoint]:
    """
    Get drift timeline for a specific session.

    Phase 1: Returns empty list unless detection is enabled.
    """
    session = await session_service.get_session(session_id)
    if session is None:
        raise HTTPException(status_code=404, detail=f"Session '{session_id}' not found")

    return await session_service.get_session_drift(session_id)
