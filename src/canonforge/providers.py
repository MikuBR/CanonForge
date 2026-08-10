"""AI provider abstraction layer.

Provider Agnostic principle (README.md:718-720): components must be able to
evolve independently and the system must not depend on a single AI provider.
The AI Layer is a provider abstraction (README.md:737-739).

v0.1 scope: only the abstraction + a NoopProvider (no external API calls).
Real OpenAI/Anthropic adapters are v0.2+ work. No API key is required to run
the v0.1 foundation — the canonical classifier is rule-based.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import Mapping

from canonforge.config import settings


class AIProvider(ABC):
    """Minimal AI provider contract. Concrete providers implement complete()."""

    name: str = "abstract"

    @abstractmethod
    def complete(self, prompt: str) -> str:
        """Run a completion and return the resulting text."""


class NoopProvider(AIProvider):
    """Provider used when no real AI provider is configured.

    Returns an empty string — it is the safe default for the v0.1 foundation,
    where all classification is rule-based and nothing calls a real model.
    """

    name = "noop"

    def complete(self, prompt: str) -> str:
        return ""


# Registry -----------------------------------------------------------------

_REGISTRY: dict[str, type[AIProvider]] = {
    NoopProvider.name: NoopProvider,
}


def register_provider(name: str, provider_cls: type[AIProvider]) -> None:
    """Register a provider class under a name (open-source extension point,
    README.md:801-814: new providers are community contributions)."""
    _REGISTRY[name] = provider_cls


def get_provider(name: str | None = None) -> AIProvider:
    """Instantiate the named provider (or the configured default).

    Raises KeyError for unknown providers so misconfiguration fails loudly
    instead of silently degrading to a wrong provider.
    """
    provider_name = name or settings.default_provider
    try:
        provider_cls = _REGISTRY[provider_name]
    except KeyError:
        available = ", ".join(sorted(_REGISTRY))
        raise KeyError(
            f"Provider desconhecido: '{provider_name}'. Disponíveis: {available}"
        ) from None
    return provider_cls()


def available_providers() -> Mapping[str, type[AIProvider]]:
    """Return the provider registry (read-only view)."""
    return dict(_REGISTRY)


__all__ = [
    "AIProvider",
    "NoopProvider",
    "available_providers",
    "get_provider",
    "register_provider",
]
