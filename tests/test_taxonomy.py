"""Tests for the canon taxonomy enums — exact pt-BR labels (README.md:87-111)."""

from __future__ import annotations

import pytest

from canonforge.domain.taxonomy import (
    CanonCategory,
    ClaimStatus,
    Fandom,
    Interpretacao,
    SourceType,
    ValidationStatus,
)


class TestClaimStatusLabels:
    def test_todos_os_status_tem_rotulos_pt_br_exatos(self):
        labels = {s.value for s in ClaimStatus}
        assert labels == {
            "CANON",
            "INTERPRETAÇÃO",
            "FANDOM",
            "NÃO CONFIRMADO",
            "CONTRADITÓRIO",
            "DESMENTIDO",
        }

    def test_sem_evidencia_nao_e_falso(self):
        assert ClaimStatus.NAO_CONFIRMADO.value == "NÃO CONFIRMADO"
        assert ClaimStatus.NAO_CONFIRMADO is not ClaimStatus.DESMENTIDO

    def test_status_desmentido_exige_rotulo_proprio(self):
        assert ClaimStatus.DESMENTIDO.value == "DESMENTIDO"


class TestCanonCategoryLabels:
    def test_categorias_canon(self):
        assert {c.value for c in CanonCategory} == {
            "Primário",
            "Complementar",
            "Adaptação",
            "Ambíguo",
        }


class TestInterpretacaoLabels:
    def test_tres_niveis_de_interpretacao(self):
        assert {i.value for i in Interpretacao} == {
            "Fortemente sustentada",
            "Plausível",
            "Especulativa",
        }


class TestFandomLabels:
    def test_tres_categorias_de_fandom(self):
        assert {f.value for f in Fandom} == {"Teoria", "Headcanon", "Fanon"}


class TestSourceTypeAndValidation:
    def test_source_types(self):
        assert SourceType.PRIMARIA.value == "Primária"
        assert SourceType.COMPLEMENTAR.value == "Complementar"

    def test_validation_status(self):
        assert ValidationStatus.PENDENTE.value == "Pendente"

    def test_enum_nao_aceita_valor_desconhecido(self):
        with pytest.raises(ValueError):
            ClaimStatus("inexistente")
