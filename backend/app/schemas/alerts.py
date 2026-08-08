"""
PromptShield Alert Schemas.

Pydantic models for security alerts.
"""

from enum import Enum

from pydantic import BaseModel


class Severity(str, Enum):
    """Alert severity levels."""

    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class AlertSchema(BaseModel):
    """A single security alert."""

    id: str
    session_id: str
    severity: Severity
    type: str
    score: float
    action: str
    timestamp: str
