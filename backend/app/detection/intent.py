"""
PromptShield Intent Drift Detection (Phase 4+).

Detects changes in behavioral intent beyond raw semantic distance.

Phase 1: Stub.
"""


class IntentDetector:
    """
    Intent drift detector.

    Phase 4: Will detect behavioral intent changes
    (e.g., "explain" → "reveal instructions").
    Phase 1: Stub — always returns 0.0.
    """

    async def detect_intent_drift(
        self,
        expected_intent: str,
        observed_text: str,
    ) -> float:
        """
        Measure intent drift between expected and observed behavior.

        Returns a score from 0.0 (no drift) to 1.0 (complete deviation).
        Phase 1: Returns 0.0.
        """
        return 0.0
