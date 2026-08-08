"""
PromptShield Session Service.

Business logic layer wrapping the session manager.
Keeps API routes thin.
"""

from app.schemas.sessions import DriftPoint, SessionDetail, SessionSchema, SessionStatus
from app.sessions.manager import session_manager


async def create_or_get_session(
    session_id: str,
    provider: str = "groq",
    model: str = "",
) -> SessionSchema:
    """Create a new session or return an existing one."""
    return await session_manager.create_session(session_id, provider, model)


async def update_session(
    session_id: str,
    model: str | None = None,
    status: SessionStatus | None = None,
    risk_score: float | None = None,
    messages: list[dict] | None = None,
) -> SessionSchema | None:
    """Update session state after a request."""
    return await session_manager.update_session(
        session_id,
        model=model,
        status=status,
        risk_score=risk_score,
        messages=messages,
    )


async def get_session(session_id: str) -> SessionSchema | None:
    """Get a session by ID."""
    return await session_manager.get_session(session_id)


async def get_session_detail(session_id: str) -> SessionDetail | None:
    """Get detailed session info including drift and messages."""
    session = await session_manager.get_session(session_id)
    if session is None:
        return None

    drift = await session_manager.get_drift_data(session_id)
    messages = await session_manager.get_messages(session_id)

    return SessionDetail(
        session=session,
        drift_timeline=drift,
        messages=messages,
    )


async def list_sessions(
    status_filter: SessionStatus | None = None,
) -> list[SessionSchema]:
    """List sessions with optional status filter."""
    return await session_manager.list_sessions(status_filter)


async def get_session_drift(session_id: str) -> list[DriftPoint]:
    """Get drift timeline for a session."""
    return await session_manager.get_drift_data(session_id)
