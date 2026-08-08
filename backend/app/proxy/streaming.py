"""
PromptShield Streaming Layer.

Handles SSE stream forwarding between upstream provider and client.
Preserves chunk order, [DONE] sentinel, and content-type.
Does NOT buffer the entire response.

Future: Detection hooks will observe the stream asynchronously here.
"""

import asyncio
from typing import Any, AsyncIterator, Callable

from app.core.logging import get_logger

logger = get_logger(__name__)


async def stream_sse_response(
    upstream_stream: AsyncIterator[bytes],
    request_id: str,
    on_chunk: Callable[[str, str], None] | None = None,
) -> AsyncIterator[str]:
    """
    Process and yield SSE chunks from the upstream provider.

    Immediately forwards each chunk to the client.
    Optionally calls on_chunk for each content piece (for future detection).

    Args:
        upstream_stream: Raw byte stream from the provider adapter.
        request_id: The PromptShield request ID for logging.
        on_chunk: Optional callback receiving (request_id, chunk_text).
                  Used for future detection hooks.

    Yields:
        SSE-formatted string chunks.
    """
    chunk_count = 0
    accumulated_content = []

    try:
        async for raw_chunk in upstream_stream:
            chunk_text = raw_chunk.decode("utf-8") if isinstance(raw_chunk, bytes) else raw_chunk
            chunk_count += 1

            # Yield immediately — no buffering
            yield chunk_text

            # Future detection hook
            if on_chunk is not None:
                try:
                    on_chunk(request_id, chunk_text)
                except Exception:
                    # Detection must never break the stream
                    pass

        logger.info(
            "stream_complete",
            request_id=request_id,
            chunks=chunk_count,
        )

    except asyncio.CancelledError:
        logger.warning(
            "stream_client_disconnect",
            request_id=request_id,
            chunks_sent=chunk_count,
        )
        raise

    except Exception as e:
        logger.error(
            "stream_error",
            request_id=request_id,
            error=str(e),
            chunks_sent=chunk_count,
        )
        raise
