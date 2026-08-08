"""
PromptShield Proxy API.

POST /v1/chat/completions — the core reverse proxy endpoint.

Forwards OpenAI-compatible requests to the configured provider (Groq).
Supports both streaming and non-streaming modes.
Generates request IDs (ps_<uuid>) for every request.
"""

import time
import uuid

from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse, StreamingResponse

from app.core.logging import get_logger
from app.proxy.client import proxy_client
from app.proxy.streaming import stream_sse_response
from app.schemas.requests import ChatCompletionRequest
from app.services.metrics_service import metrics_service
from app.services.session_service import create_or_get_session, update_session

logger = get_logger(__name__)

router = APIRouter(tags=["proxy"])


def _generate_request_id() -> str:
    """Generate a PromptShield request ID."""
    return f"ps_{uuid.uuid4().hex[:8]}"


@router.post("/v1/chat/completions")
async def chat_completions(request: Request):
    """
    Proxy chat completion requests to Groq.

    Supports streaming (SSE) and non-streaming modes.
    Transparent — clients only need to change base_url.
    """
    request_id = _generate_request_id()
    start_time = time.time()

    # Parse the raw body to preserve all fields
    raw_body = await request.json()

    # Validate with our schema
    try:
        parsed = ChatCompletionRequest(**raw_body)
    except Exception as e:
        logger.error("request_validation_error", request_id=request_id, error=str(e))
        return JSONResponse(
            status_code=400,
            content={
                "error": {
                    "message": f"Invalid request: {str(e)}",
                    "type": "invalid_request_error",
                }
            },
        )

    is_streaming = parsed.stream
    model = parsed.model

    # Extract original headers (lowercase)
    original_headers = {k.lower(): v for k, v in request.headers.items()}

    # Create or update session
    session_id = parsed.ps_session_id or request_id
    await create_or_get_session(session_id, provider="groq", model=model)

    # Store messages for session tracking
    messages_to_store = [
        {"role": m.role, "content": m.content}
        for m in parsed.messages
        if m.content
    ]

    logger.info(
        "proxy_request",
        request_id=request_id,
        session_id=session_id,
        model=model,
        stream=is_streaming,
        message_count=len(parsed.messages),
    )

    # Build the upstream body (strips ps_* fields)
    upstream_body = parsed.to_upstream_body()

    try:
        if is_streaming:
            # --- Streaming path ---
            upstream_stream = proxy_client.forward_stream(upstream_body, original_headers)

            async def event_generator():
                async for chunk in stream_sse_response(upstream_stream, request_id):
                    yield chunk

                # Record metrics after stream completes
                latency_ms = (time.time() - start_time) * 1000
                await metrics_service.record_request(latency_ms)
                await update_session(
                    session_id,
                    model=model,
                    messages=messages_to_store,
                )

            return StreamingResponse(
                event_generator(),
                media_type="text/event-stream",
                headers={
                    "Cache-Control": "no-cache",
                    "Connection": "keep-alive",
                    "X-Request-Id": request_id,
                },
            )

        else:
            # --- Non-streaming path ---
            response = await proxy_client.forward_completion(upstream_body, original_headers)

            latency_ms = (time.time() - start_time) * 1000
            await metrics_service.record_request(latency_ms)

            # Update session
            await update_session(
                session_id,
                model=model,
                messages=messages_to_store,
            )

            logger.info(
                "proxy_response",
                request_id=request_id,
                status=response.status_code,
                latency_ms=round(latency_ms, 2),
                stream=False,
            )

            return JSONResponse(
                status_code=response.status_code,
                content=response.json(),
                headers={"X-Request-Id": request_id},
            )

    except Exception as e:
        latency_ms = (time.time() - start_time) * 1000
        await metrics_service.record_request(latency_ms)

        logger.error(
            "proxy_error",
            request_id=request_id,
            error=str(e),
            latency_ms=round(latency_ms, 2),
        )

        return JSONResponse(
            status_code=502,
            content={
                "error": {
                    "message": f"Upstream error: {str(e)}",
                    "type": "upstream_error",
                }
            },
            headers={"X-Request-Id": request_id},
        )
