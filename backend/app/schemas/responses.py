"""
PromptShield Response Schemas.

Pydantic models for API responses from PromptShield endpoints.
"""

from pydantic import BaseModel


class HealthResponse(BaseModel):
    """Response from GET /health."""

    status: str = "healthy"
    provider: str = "groq"
    proxy: str = "online"


class MetricsResponse(BaseModel):
    """Response from GET /metrics."""

    requests: int = 0
    active_sessions: int = 0
    flagged: int = 0
    blocked: int = 0
    average_latency_ms: float = 0.0
    uptime: float = 100.0


class ErrorResponse(BaseModel):
    """Standard error response shape."""

    error: dict
