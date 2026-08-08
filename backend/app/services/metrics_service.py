"""
PromptShield Metrics Service.

In-memory counters for dashboard-level metrics.
Thread-safe via asyncio locks.
"""

import asyncio
import time
from collections import deque

from app.core.logging import get_logger

logger = get_logger(__name__)


class MetricsService:
    """
    In-memory metrics tracker.

    Tracks request counts, latencies, and status aggregations.
    """

    def __init__(self) -> None:
        self._lock = asyncio.Lock()
        self._total_requests: int = 0
        self._flagged: int = 0
        self._blocked: int = 0
        self._latencies: deque[float] = deque(maxlen=1000)  # Last 1000
        self._start_time: float = time.time()

    async def record_request(self, latency_ms: float) -> None:
        """Record a completed request with its latency."""
        async with self._lock:
            self._total_requests += 1
            self._latencies.append(latency_ms)

    async def record_flagged(self) -> None:
        """Increment the flagged counter."""
        async with self._lock:
            self._flagged += 1

    async def record_blocked(self) -> None:
        """Increment the blocked counter."""
        async with self._lock:
            self._blocked += 1

    async def get_total_requests(self) -> int:
        """Return total request count."""
        async with self._lock:
            return self._total_requests

    async def get_average_latency(self) -> float:
        """Return average latency in ms over recent requests."""
        async with self._lock:
            if not self._latencies:
                return 0.0
            return round(sum(self._latencies) / len(self._latencies), 2)

    async def get_uptime(self) -> float:
        """Return uptime percentage (always 100 for Phase 1)."""
        return 100.0

    async def get_summary(self) -> dict:
        """Return all metrics as a dict."""
        async with self._lock:
            avg_latency = 0.0
            if self._latencies:
                avg_latency = round(sum(self._latencies) / len(self._latencies), 2)

            return {
                "requests": self._total_requests,
                "flagged": self._flagged,
                "blocked": self._blocked,
                "average_latency_ms": avg_latency,
                "uptime": 100.0,
            }


# Module-level singleton
metrics_service = MetricsService()
