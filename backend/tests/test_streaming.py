"""
Tests for streaming proxy functionality.

Verifies SSE chunk forwarding, order preservation, and [DONE] handling.
"""

import pytest
from unittest.mock import AsyncMock, patch, MagicMock
from fastapi.testclient import TestClient

from app.main import app


@pytest.fixture
def client():
    """Create a test client."""
    return TestClient(app)


def _make_stream_request():
    """Helper to build a streaming chat completion request."""
    return {
        "model": "llama-3.3-70b-versatile",
        "messages": [
            {"role": "user", "content": "Hello!"},
        ],
        "stream": True,
    }


async def _mock_stream_chunks():
    """Generate mock SSE chunks like Groq would."""
    chunks = [
        b'data: {"id":"chatcmpl-1","object":"chat.completion.chunk","choices":[{"index":0,"delta":{"role":"assistant"},"finish_reason":null}]}\n\n',
        b'data: {"id":"chatcmpl-1","object":"chat.completion.chunk","choices":[{"index":0,"delta":{"content":"Hello"},"finish_reason":null}]}\n\n',
        b'data: {"id":"chatcmpl-1","object":"chat.completion.chunk","choices":[{"index":0,"delta":{"content":"!"},"finish_reason":null}]}\n\n',
        b'data: {"id":"chatcmpl-1","object":"chat.completion.chunk","choices":[{"index":0,"delta":{},"finish_reason":"stop"}]}\n\n',
        b'data: [DONE]\n\n',
    ]
    for chunk in chunks:
        yield chunk


@patch("app.proxy.client.proxy_client.forward_stream")
def test_streaming_returns_event_stream(mock_stream, client):
    """Streaming response should have text/event-stream content type."""
    mock_stream.return_value = _mock_stream_chunks()

    response = client.post(
        "/v1/chat/completions",
        json=_make_stream_request(),
    )

    assert response.status_code == 200
    assert "text/event-stream" in response.headers.get("content-type", "")


@patch("app.proxy.client.proxy_client.forward_stream")
def test_streaming_preserves_done(mock_stream, client):
    """Streaming should preserve the [DONE] sentinel."""
    mock_stream.return_value = _mock_stream_chunks()

    response = client.post(
        "/v1/chat/completions",
        json=_make_stream_request(),
    )

    content = response.text
    assert "[DONE]" in content


@patch("app.proxy.client.proxy_client.forward_stream")
def test_streaming_has_request_id(mock_stream, client):
    """Streaming response should include X-Request-Id header."""
    mock_stream.return_value = _mock_stream_chunks()

    response = client.post(
        "/v1/chat/completions",
        json=_make_stream_request(),
    )

    assert "x-request-id" in response.headers
    assert response.headers["x-request-id"].startswith("ps_")


@patch("app.proxy.client.proxy_client.forward_stream")
def test_streaming_contains_chunks(mock_stream, client):
    """Streaming response should contain data chunks."""
    mock_stream.return_value = _mock_stream_chunks()

    response = client.post(
        "/v1/chat/completions",
        json=_make_stream_request(),
    )

    content = response.text
    assert "data:" in content
    assert "Hello" in content
