"""
PromptShield Groq Provider Adapter.

Implements the ProviderAdapter interface for Groq's OpenAI-compatible API.
Handles authentication, URL routing, and request forwarding.
"""

from typing import Any, AsyncIterator

import httpx

from app.config import get_settings
from app.core.logging import get_logger
from app.proxy.adapters.base import ProviderAdapter

logger = get_logger(__name__)


class GroqAdapter(ProviderAdapter):
    """Adapter for Groq's OpenAI-compatible API."""

    @property
    def provider_name(self) -> str:
        return "groq"

    def build_url(self, path: str) -> str:
        """Build the full Groq API URL."""
        settings = get_settings()
        base = settings.proxy_target_url.rstrip("/")
        path = path.lstrip("/")
        return f"{base}/{path}"

    def build_headers(self, original_headers: dict[str, str]) -> dict[str, str]:
        """
        Build headers for Groq upstream request.

        Injects the Groq API key as Bearer token.
        Strips hop-by-hop headers and internal headers.
        """
        settings = get_settings()

        # Headers to forward
        headers: dict[str, str] = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {settings.groq_api_key}",
        }

        # Forward user-agent if present
        if "user-agent" in original_headers:
            headers["User-Agent"] = original_headers["user-agent"]

        return headers

    async def create_completion(
        self,
        client: httpx.AsyncClient,
        body: dict[str, Any],
        headers: dict[str, str],
    ) -> httpx.Response:
        """Send a non-streaming request to Groq."""
        url = self.build_url("/chat/completions")
        upstream_headers = self.build_headers(headers)

        # Ensure stream is false
        body["stream"] = False

        logger.info(
            "groq_request",
            url=url,
            model=body.get("model"),
            stream=False,
        )

        response = await client.post(
            url,
            json=body,
            headers=upstream_headers,
        )

        return response

    async def stream_completion(
        self,
        client: httpx.AsyncClient,
        body: dict[str, Any],
        headers: dict[str, str],
    ) -> AsyncIterator[bytes]:
        """
        Send a streaming request to Groq.

        Yields raw SSE byte lines as they arrive.
        Does NOT buffer the complete response.
        """
        url = self.build_url("/chat/completions")
        upstream_headers = self.build_headers(headers)

        # Ensure stream is true
        body["stream"] = True

        logger.info(
            "groq_stream_request",
            url=url,
            model=body.get("model"),
            stream=True,
        )

        async with client.stream(
            "POST",
            url,
            json=body,
            headers=upstream_headers,
        ) as response:
            # Check for upstream errors before streaming
            if response.status_code != 200:
                error_body = await response.aread()
                logger.error(
                    "groq_upstream_error",
                    status_code=response.status_code,
                    body=error_body.decode("utf-8", errors="replace"),
                )
                # Yield the error as-is so the proxy can return it to the client
                yield error_body
                return

            async for line in response.aiter_lines():
                if line:
                    yield f"{line}\n\n".encode("utf-8")
