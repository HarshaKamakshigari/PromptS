"""
PromptShield Provider Adapter — Abstract Base.

All LLM provider adapters must implement this interface.
This keeps provider-specific logic isolated from the proxy core.
"""

from abc import ABC, abstractmethod
from typing import Any, AsyncIterator

import httpx


class ProviderAdapter(ABC):
    """Abstract base class for LLM provider adapters."""

    @property
    @abstractmethod
    def provider_name(self) -> str:
        """Return the provider name (e.g., 'groq', 'openai')."""
        ...

    @abstractmethod
    def build_url(self, path: str) -> str:
        """Build the full upstream URL for a given API path."""
        ...

    @abstractmethod
    def build_headers(self, original_headers: dict[str, str]) -> dict[str, str]:
        """
        Build headers for the upstream request.

        Must inject authentication and set correct content-type.
        Must NOT leak internal headers to upstream.
        """
        ...

    @abstractmethod
    async def create_completion(
        self,
        client: httpx.AsyncClient,
        body: dict[str, Any],
        headers: dict[str, str],
    ) -> httpx.Response:
        """
        Send a non-streaming chat completion request to the provider.

        Returns the raw httpx.Response.
        """
        ...

    @abstractmethod
    async def stream_completion(
        self,
        client: httpx.AsyncClient,
        body: dict[str, Any],
        headers: dict[str, str],
    ) -> AsyncIterator[bytes]:
        """
        Send a streaming chat completion request to the provider.

        Yields raw SSE byte chunks as they arrive from upstream.
        Must NOT buffer the entire response.
        """
        ...
