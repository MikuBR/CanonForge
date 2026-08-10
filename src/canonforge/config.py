"""Application settings loaded from environment / .env file.

Provider Agnostic principle (README.md:718-720): the system must not depend
on a single AI provider. Settings here only select a provider by name and
carry optional API keys; no provider logic lives in this module.

Security (README.md:779-798): API keys are never stored in the repository.
They come from the environment or a gitignored .env file. .env.example is
committed with empty placeholders; .env is ignored.
"""

from __future__ import annotations

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Runtime settings. Reads env vars and a local .env file if present."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        case_sensitive=False,
    )

    default_provider: str = "noop"
    openai_api_key: str | None = None
    anthropic_api_key: str | None = None
    canonforge_db: str | None = None  # optional override for sqlite path


settings = Settings()


__all__ = ["Settings", "settings"]
