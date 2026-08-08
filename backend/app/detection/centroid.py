"""
PromptShield Task Centroid Module (Phase 2+).

Computes and maintains the task centroid (semantic representation
of the intended task) from system prompt + initial user message.

Phase 1: Stub.
"""

import numpy as np


class TaskCentroid:
    """
    Represents the semantic center of the intended task.

    Phase 2: Computed from system prompt + initial user message embeddings.
    Phase 1: Stub returning zero vector.
    """

    def __init__(self, dimension: int = 384) -> None:
        self._centroid: np.ndarray = np.zeros(dimension, dtype=np.float32)
        self._initialized: bool = False

    @property
    def is_initialized(self) -> bool:
        """Whether the centroid has been computed."""
        return self._initialized

    @property
    def vector(self) -> np.ndarray:
        """Return the centroid vector."""
        return self._centroid

    async def compute(
        self,
        system_embedding: np.ndarray,
        user_embedding: np.ndarray,
    ) -> np.ndarray:
        """
        Compute the task centroid from initial embeddings.

        Phase 2: Weighted average of system + user embeddings.
        Phase 1: Returns zero vector.
        """
        self._centroid = (system_embedding + user_embedding) / 2.0
        self._initialized = True
        return self._centroid
