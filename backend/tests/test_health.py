"""
Tests for the health endpoint.
"""

import pytest
from fastapi.testclient import TestClient

from app.main import app


@pytest.fixture
def client():
    """Create a test client."""
    return TestClient(app)


def test_health_returns_200(client):
    """GET /health should return 200."""
    response = client.get("/health")
    assert response.status_code == 200


def test_health_response_shape(client):
    """GET /health should return correct JSON shape."""
    response = client.get("/health")
    data = response.json()

    assert "status" in data
    assert "provider" in data
    assert "proxy" in data


def test_health_values(client):
    """GET /health should return expected values."""
    response = client.get("/health")
    data = response.json()

    assert data["status"] == "healthy"
    assert data["provider"] == "groq"
    assert data["proxy"] == "online"


def test_metrics_returns_200(client):
    """GET /metrics should return 200."""
    response = client.get("/metrics")
    assert response.status_code == 200


def test_metrics_response_shape(client):
    """GET /metrics should return correct JSON shape."""
    response = client.get("/metrics")
    data = response.json()

    assert "requests" in data
    assert "active_sessions" in data
    assert "flagged" in data
    assert "blocked" in data
    assert "average_latency_ms" in data
    assert "uptime" in data


def test_sessions_returns_200(client):
    """GET /sessions should return 200."""
    response = client.get("/sessions")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_alerts_returns_200(client):
    """GET /alerts should return 200."""
    response = client.get("/alerts")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_session_not_found(client):
    """GET /sessions/{nonexistent} should return 404."""
    response = client.get("/sessions/nonexistent_id")
    assert response.status_code == 404
