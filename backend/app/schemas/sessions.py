"""
PromptShield Session Schemas.

Pydantic models for session data and drift points.
"""

from enum import Enum

from pydantic import BaseModel


class SessionStatus(str, Enum):
    """Possible session statuses."""

    ACTIVE = "active"
    SAFE = "safe"
    FLAGGED = "flagged"
    BLOCKED = "blocked"


class SessionSchema(BaseModel):
    """Session summary for list endpoints."""

    id: str
    provider: str = "groq"
    model: str = ""
    started_at: str = ""
    last_activity: str = ""
    status: SessionStatus = SessionStatus.ACTIVE
    risk_score: float = 0.0
    request_count: int = 0


class DriftPoint(BaseModel):
    """A single point in a drift timeline."""

    timestamp: str
    semantic_drift: float = 0.0
    intent_drift: float = 0.0
    risk: float = 0.0


class SessionDetail(BaseModel):
    """Detailed session data including drift history."""

    session: SessionSchema
    drift_timeline: list[DriftPoint] = []
    messages: list[dict] = []
