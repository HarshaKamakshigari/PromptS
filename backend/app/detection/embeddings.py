"""
PromptShield Embeddings Module (Phase 2+).

Will provide text embedding generation using sentence-transformers.
Stub for Phase 1 — architecture ready for future implementation.
"""

from typing import Any

import numpy as np


class EmbeddingService:
    """
    Text embedding service.

    Phase 2+: Will use sentence-transformers/all-MiniLM-L6-v2.
    Phase 1: Stub that returns zero vectors.
    """

    def __init__(self, model_name: str = "all-MiniLM-L6-v2") -> None:
        self._model_name = model_name
        self._model: Any = None  # Loaded lazily in Phase 2

    @property
    def dimension(self) -> int:
        """Embedding vector dimension."""
        return 384  # all-MiniLM-L6-v2 output dimension

    async def encode(self, text: str) -> np.ndarray:
        """
        Encode text into an embedding vector.

        Phase 1: Returns a zero vector.
        Phase 2: Will use the loaded model.
        """
        return np.zeros(self.dimension, dtype=np.float32)

    async def encode_batch(self, texts: list[str]) -> np.ndarray:
        """
        Encode multiple texts into embedding vectors.

        Phase 1: Returns zero vectors.
        """
        return np.zeros((len(texts), self.dimension), dtype=np.float32)


# Module-level singleton
embedding_service = EmbeddingService()
