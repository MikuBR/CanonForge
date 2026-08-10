"""Tests for the provider abstraction layer — registry, noop, errors."""

from __future__ import annotations

import pytest

from canonforge.providers import (
    AIProvider,
    NoopProvider,
    available_providers,
    get_provider,
    register_provider,
)


class TestNoopProvider:
    def test_instancia_noop(self):
        p = get_provider("noop")
        assert isinstance(p, NoopProvider)
        assert isinstance(p, AIProvider)

    def test_complete_retorna_vazio(self):
        assert get_provider("noop").complete("prompt") == ""


class TestRegistry:
    def test_default_e_noop(self):
        p = get_provider()
        assert p.name == "noop"

    def test_provider_inexistente_levanta_keyerror(self):
        with pytest.raises(KeyError):
            get_provider("zzz")

    def test_registro_de_provider_personalizado(self):
        class FakeProvider(AIProvider):
            name = "fake"

            def complete(self, prompt: str) -> str:
                return "fake-response"

        register_provider("fake", FakeProvider)
        try:
            p = get_provider("fake")
            assert p.complete("x") == "fake-response"
        finally:
            available_providers()
            # remove fake from registry to keep tests independent
            from canonforge.providers import _REGISTRY

            _REGISTRY.pop("fake", None)

    def test_available_providers_inclui_noop(self):
        assert "noop" in available_providers()
