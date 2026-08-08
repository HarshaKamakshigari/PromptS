"""
PromptShield In-Memory Session Manager.

TTL-based in-memory store for session tracking.
No database — Phase 1 only.
Thread-safe via asyncio locks.
"""

import asyncio
import time
from datetime import datetime, timezone

from app.config import get_settings
from app.core.logging import get_logger
from app.schemas.sessions import DriftPoint, SessionSchema, SessionStatus

logger = get_logger(__name__)


class SessionManager:
    """
    In-memory session store with TTL expiration.

    Sessions auto-expire after SESSION_TTL_SECONDS.
    """

    def __init__(self) -> None:
        self._sessions: dict[str, SessionSchema] = {}
        self._drift_data: dict[str, list[DriftPoint]] = {}
        self._messages: dict[str, list[dict]] = {}
        self._lock = asyncio.Lock()

    async def create_session(
        self,
        session_id: str,
        provider: str = "groq",
        model: str = "",
    ) -> SessionSchema:
        """Create a new session or return existing one."""
        async with self._lock:
            if session_id in self._sessions:
                return self._sessions[session_id]

            now = datetime.now(timezone.utc).isoformat()
            session = SessionSchema(
                id=session_id,
                provider=provider,
                model=model,
                started_at=now,
                last_activity=now,
                status=SessionStatus.ACTIVE,
                risk_score=0.0,
                request_count=1,
            )
            self._sessions[session_id] = session
            self._drift_data[session_id] = []
            self._messages[session_id] = []

            logger.info("session_created", session_id=session_id, model=model)
            return session

    async def update_session(
        self,
        session_id: str,
        model: str | None = None,
        status: SessionStatus | None = None,
        risk_score: float | None = None,
        messages: list[dict] | None = None,
    ) -> SessionSchema | None:
        """Update an existing session."""
        async with self._lock:
            session = self._sessions.get(session_id)
            if session is None:
                return None

            now = datetime.now(timezone.utc).isoformat()
            session.last_activity = now
            session.request_count += 1

            if model is not None:
                session.model = model
            if status is not None:
                session.status = status
            if risk_score is not None:
                session.risk_score = risk_score
            if messages is not None:
                self._messages[session_id].extend(messages)

            return session

    async def get_session(self, session_id: str) -> SessionSchema | None:
        """Get a session by ID."""
        async with self._lock:
            self._cleanup_expired()
            return self._sessions.get(session_id)

    async def list_sessions(
        self,
        status_filter: SessionStatus | None = None,
    ) -> list[SessionSchema]:
        """List all sessions, optionally filtered by status."""
        async with self._lock:
            self._cleanup_expired()
            sessions = list(self._sessions.values())

            if status_filter is not None:
                sessions = [s for s in sessions if s.status == status_filter]

            # Sort by last activity, newest first
            sessions.sort(key=lambda s: s.last_activity, reverse=True)
            return sessions

    async def get_drift_data(self, session_id: str) -> list[DriftPoint]:
        """Get drift timeline for a session."""
        async with self._lock:
            return self._drift_data.get(session_id, [])

    async def get_messages(self, session_id: str) -> list[dict]:
        """Get stored messages for a session."""
        async with self._lock:
            return self._messages.get(session_id, [])

    async def add_drift_point(self, session_id: str, point: DriftPoint) -> None:
        """Add a drift data point to a session."""
        async with self._lock:
            if session_id in self._drift_data:
                self._drift_data[session_id].append(point)

    async def get_active_count(self) -> int:
        """Return count of active sessions."""
        async with self._lock:
            self._cleanup_expired()
            return len(self._sessions)

    async def get_status_counts(self) -> dict[str, int]:
        """Return counts by status."""
        async with self._lock:
            self._cleanup_expired()
            counts: dict[str, int] = {
                "active": 0,
                "safe": 0,
                "flagged": 0,
                "blocked": 0,
            }
            for s in self._sessions.values():
                counts[s.status.value] = counts.get(s.status.value, 0) + 1
            return counts

    def _cleanup_expired(self) -> None:
        """Remove expired sessions. Must be called while holding the lock."""
        settings = get_settings()
        ttl = settings.session_ttl_seconds
        now = time.time()

        expired = []
        for sid, session in self._sessions.items():
            try:
                last = datetime.fromisoformat(session.last_activity).timestamp()
                if now - last > ttl:
                    expired.append(sid)
            except (ValueError, TypeError):
                continue

        for sid in expired:
            del self._sessions[sid]
            self._drift_data.pop(sid, None)
            self._messages.pop(sid, None)
            logger.info("session_expired", session_id=sid)


# Module-level singleton
session_manager = SessionManager()
