"""
PromptShield Custom Exceptions.

Hierarchy:
    PromptShieldError
    ├── UpstreamError     — upstream provider returned an error
    ├── ProviderError     — adapter/provider configuration issue
    └── ConfigError       — missing or invalid configuration
"""

from fastapi import Request
from fastapi.responses import JSONResponse


class PromptShieldError(Exception):
    """Base exception for all PromptShield errors."""

    def __init__(self, message: str, status_code: int = 500):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)


class UpstreamError(PromptShieldError):
    """Upstream provider returned an error response."""

    def __init__(self, message: str, status_code: int = 502, upstream_status: int | None = None):
        self.upstream_status = upstream_status
        super().__init__(message, status_code)


class ProviderError(PromptShieldError):
    """Provider adapter or configuration error."""

    def __init__(self, message: str, status_code: int = 503):
        super().__init__(message, status_code)


class ConfigError(PromptShieldError):
    """Configuration error."""

    def __init__(self, message: str, status_code: int = 500):
        super().__init__(message, status_code)


async def promptshield_exception_handler(request: Request, exc: PromptShieldError) -> JSONResponse:
    """Handle PromptShieldError and return structured JSON error responses."""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": {
                "message": exc.message,
                "type": type(exc).__name__,
            }
        },
    )


async def generic_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """Catch-all handler for unhandled exceptions."""
    return JSONResponse(
        status_code=500,
        content={
            "error": {
                "message": "Internal server error",
                "type": "InternalError",
            }
        },
    )
