"""
PromptShield Configuration.

Loads settings from environment variables / .env file using pydantic-settings.
"""

from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )

    # Application
    app_name: str = "PromptShield"
    host: str = "0.0.0.0"
    port: int = 8000

    # Provider
    proxy_target_url: str = "https://api.groq.com/openai/v1"
    groq_api_key: str = ""

    # Logging
    log_level: str = "INFO"

    # Sessions
    session_ttl_seconds: int = 3600

    # Detection thresholds (Phase 2+)
    semantic_drift_threshold: float = 0.75
    intent_drift_threshold: float = 0.70
    hard_risk_threshold: float = 0.90


@lru_cache
def get_settings() -> Settings:
    """Return cached singleton settings instance."""
    return Settings()
