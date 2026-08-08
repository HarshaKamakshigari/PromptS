"""
Tests for the proxy endpoint (non-streaming).

Uses mocked upstream to avoid real Groq calls.
"""

import pytest
from unittest.mock import AsyncMock, patch, MagicMock
from fastapi.testclient import TestClient

from app.main import app


@pytest.fixture
def client():
    """Create a test client."""
    return TestClient(app)


def _make_chat_request(model="llama-3.3-70b-versatile", stream=False):
    """Helper to build a chat completion request body."""
    return {
        "model": model,
        "messages": [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "Hello!"},
        ],
        "stream": stream,
    }


def _mock_groq_response():
    """Create a mock Groq non-streaming response."""
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "id": "chatcmpl-test",
        "object": "chat.completion",
        "created": 1234567890,
        "model": "llama-3.3-70b-versatile",
        "choices": [
            {
                "index": 0,
                "message": {
                    "role": "assistant",
                    "content": "Hello! How can I help you?",
                },
                "finish_reason": "stop",
            }
        ],
        "usage": {
            "prompt_tokens": 10,
            "completion_tokens": 8,
            "total_tokens": 18,
        },
    }
    return mock_response


def test_proxy_rejects_invalid_request(client):
    """POST /v1/chat/completions with missing model should return 400."""
    response = client.post(
        "/v1/chat/completions",
        json={"messages": [{"role": "user", "content": "Hi"}]},
    )
    assert response.status_code == 400


def test_proxy_rejects_empty_messages(client):
    """POST /v1/chat/completions with missing messages should return 400."""
    response = client.post(
        "/v1/chat/completions",
        json={"model": "llama-3.3-70b-versatile"},
    )
    assert response.status_code == 400


@patch("app.proxy.client.proxy_client.forward_completion", new_callable=AsyncMock)
def test_proxy_non_streaming_success(mock_forward, client):
    """Non-streaming request should return upstream response."""
    mock_forward.return_value = _mock_groq_response()

    response = client.post(
        "/v1/chat/completions",
        json=_make_chat_request(stream=False),
    )

    assert response.status_code == 200
    data = response.json()
    assert "choices" in data
    assert data["choices"][0]["message"]["content"] == "Hello! How can I help you?"


@patch("app.proxy.client.proxy_client.forward_completion", new_callable=AsyncMock)
def test_proxy_returns_request_id_header(mock_forward, client):
    """Response should include X-Request-Id header."""
    mock_forward.return_value = _mock_groq_response()

    response = client.post(
        "/v1/chat/completions",
        json=_make_chat_request(stream=False),
    )

    assert "x-request-id" in response.headers
    assert response.headers["x-request-id"].startswith("ps_")


@patch("app.proxy.client.proxy_client.forward_completion", new_callable=AsyncMock)
def test_proxy_creates_session(mock_forward, client):
    """Proxy should create a session for each request."""
    mock_forward.return_value = _mock_groq_response()

    # Make a request
    client.post(
        "/v1/chat/completions",
        json=_make_chat_request(stream=False),
    )

    # Check sessions
    sessions_response = client.get("/sessions")
    assert sessions_response.status_code == 200
    sessions = sessions_response.json()
    assert len(sessions) >= 1


@patch("app.proxy.client.proxy_client.forward_completion", new_callable=AsyncMock)
def test_proxy_upstream_error(mock_forward, client):
    """Proxy should handle upstream errors gracefully."""
    mock_forward.side_effect = Exception("Connection refused")

    response = client.post(
        "/v1/chat/completions",
        json=_make_chat_request(stream=False),
    )

    assert response.status_code == 502
    data = response.json()
    assert "error" in data
