"""
PromptShield Policy Engine (Phase 6+).

Makes enforcement decisions based on risk scores.

Phase 1: Always returns ALLOW + LOG (detection not active).
"""

from enum import Enum

from app.core.logging import get_logger

logger = get_logger(__name__)


class PolicyAction(str, Enum):
    """Possible policy enforcement actions."""

    ALLOW = "allow"
    LOG = "log"
    FLAG = "flag"
    WARN = "warn"
    TERMINATE = "terminate"


class PolicyEngine:
    """
    Risk-based policy engine.

    Phase 6 thresholds:
        < 0.50  → ALLOW
        0.50–0.70 → LOG
        0.70–0.90 → WARN / FLAG
        > 0.90  → TERMINATE

    Phase 1: Always ALLOW + LOG.
    """

    def __init__(self) -> None:
        self.thresholds = {
            "low": 0.50,
            "medium": 0.70,
            "high": 0.90,
        }

    async def evaluate(self, risk_score: float) -> PolicyAction:
        """
        Evaluate risk score and return a policy action.

        Phase 1: Always returns ALLOW.
        """
        # Phase 1: detection not active, always allow
        logger.info(
            "policy_evaluation",
            risk_score=risk_score,
            action=PolicyAction.ALLOW.value,
            phase="1",
        )
        return PolicyAction.ALLOW


# Module-level singleton
policy_engine = PolicyEngine()
