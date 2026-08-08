"""
PromptShield Provider Adapter Registry.

Provides a factory function to get the correct adapter by provider name.
"""

from app.proxy.adapters.base import ProviderAdapter
from app.proxy.adapters.groq import GroqAdapter

# Registry of available adapters
_ADAPTERS: dict[str, type[ProviderAdapter]] = {
    "groq": GroqAdapter,
}

# Cached adapter instances
_instances: dict[str, ProviderAdapter] = {}


def get_adapter(provider: str = "groq") -> ProviderAdapter:
    """
    Get a provider adapter instance by name.

    Adapters are cached as singletons.

    Args:
        provider: Provider name (default: 'groq').

    Returns:
        The corresponding ProviderAdapter instance.

    Raises:
        ValueError: If the provider is not registered.
    """
    if provider not in _ADAPTERS:
        available = ", ".join(_ADAPTERS.keys())
        raise ValueError(f"Unknown provider '{provider}'. Available: {available}")

    if provider not in _instances:
        _instances[provider] = _ADAPTERS[provider]()

    return _instances[provider]


__all__ = ["ProviderAdapter", "GroqAdapter", "get_adapter"]
