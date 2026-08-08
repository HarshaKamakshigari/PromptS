"""
PromptShield Semantic Drift Detection (Phase 3+).

Measures cosine distance between output chunks and the task centroid.
Uses EMA smoothing to prevent single outlier sentences from triggering alerts.

Phase 1: Stub.
"""

import numpy as np


def cosine_distance(a: np.ndarray, b: np.ndarray) -> float:
    """Compute cosine distance between two vectors (1 - cosine_similarity)."""
    norm_a = np.linalg.norm(a)
    norm_b = np.linalg.norm(b)
    if norm_a == 0 or norm_b == 0:
        return 1.0
    similarity = np.dot(a, b) / (norm_a * norm_b)
    return float(1.0 - similarity)


class DriftDetector:
    """
    Semantic drift detector.

    Compares output embeddings against the task centroid using cosine distance.
    Smooths scores with exponential moving average (EMA).

    Phase 1: Stub — always returns 0.0.
    """

    def __init__(self, alpha: float = 0.3) -> None:
        self._alpha = alpha
        self._ema: float = 0.0

    @property
    def current_drift(self) -> float:
        """Return the current smoothed drift score."""
        return self._ema

    async def compute_drift(
        self,
        output_embedding: np.ndarray,
        centroid: np.ndarray,
    ) -> float:
        """
        Compute drift score for an output chunk.

        Phase 3: Real computation with EMA smoothing.
        Phase 1: Returns 0.0.
        """
        if np.all(centroid == 0) or np.all(output_embedding == 0):
            return 0.0

        distance = cosine_distance(output_embedding, centroid)
        self._ema = self._alpha * distance + (1 - self._alpha) * self._ema
        return self._ema
