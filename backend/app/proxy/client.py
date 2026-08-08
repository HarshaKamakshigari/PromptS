"""
PromptShield Proxy Client.

Manages the HTTPX async client lifecycle and proxies requests through
the provider adapter layer.
"""

from typing import Any, AsyncIterator

import httpx

from app.config import get_settings
from app.core.logging import get_logger
from app.proxy.adapters import ProviderAdapter, get_adapter

logger = get_logger(__name__)


class ProxyClient:
    """
    Async HTTP client for proxying LLM requests.

    Wraps httpx.AsyncClient with connection pooling and timeout config.
    Uses the adapter pattern to support multiple providers.
    """

    def __init__(self) -> None:
        self._client: httpx.AsyncClient | None = None
        self._adapter: ProviderAdapter = get_adapter("groq")

    @property
    def adapter(self) -> ProviderAdapter:
        """Return the current provider adapter."""
        return self._adapter

    async def start(self) -> None:
        """Initialize the HTTPX async client."""
        settings = get_settings()
        self._client = httpx.AsyncClient(
            timeout=httpx.Timeout(
                connect=10.0,
                read=120.0,  # LLM responses can be slow
                write=10.0,
                pool=10.0,
            ),
            limits=httpx.Limits(
                max_connections=100,
                max_keepalive_connections=20,
            ),
            follow_redirects=True,
        )
        logger.info(
            "proxy_client_started",
            provider=self._adapter.provider_name,
            target_url=settings.proxy_target_url,
        )

    async def stop(self) -> None:
        """Close the HTTPX async client."""
        if self._client:
            await self._client.aclose()
            self._client = None
            logger.info("proxy_client_stopped")

    def _get_client(self) -> httpx.AsyncClient:
        """Get the initialized client or raise."""
        if self._client is None:
            raise RuntimeError("ProxyClient not started. Call start() first.")
        return self._client

    async def forward_completion(
        self,
        body: dict[str, Any],
        headers: dict[str, str],
    ) -> httpx.Response:
        """
        Forward a non-streaming chat completion request.

        Returns the raw upstream response.
        """
        client = self._get_client()
        return await self._adapter.create_completion(client, body, headers)

    async def forward_stream(
        self,
        body: dict[str, Any],
        headers: dict[str, str],
    ) -> AsyncIterator[bytes]:
        """
        Forward a streaming chat completion request.

        Yields raw SSE byte chunks from upstream.
        """
        client = self._get_client()
        async for chunk in self._adapter.stream_completion(client, body, headers):
            yield chunk


# Module-level singleton
proxy_client = ProxyClient()
