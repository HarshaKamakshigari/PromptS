"""
PromptShield Health API.

GET /health — lightweight health check.
"""

from fastapi import APIRouter

from app.schemas.responses import HealthResponse

router = APIRouter(tags=["health"])


@router.get("/health", response_model=HealthResponse)
async def health_check() -> HealthResponse:
    """
    Check system health.

    Returns proxy status and provider info.
    Does not make upstream calls — kept cheap.
    """
    return HealthResponse(
        status="healthy",
        provider="groq",
        proxy="online",
    )
