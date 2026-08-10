"""Tests for Pydantic domain models — validation, defaults, invariants."""

from __future__ import annotations

import pytest
from pydantic import ValidationError

from canonforge.domain.models import Claim, Evidence, Source, Work
from canonforge.domain.taxonomy import ClaimStatus, SourceType


class TestWork:
    def test_titulo_obrigatorio(self):
        with pytest.raises(ValidationError):
            Work()  # type: ignore[call-arg]

    def test_campos_opcionais(self):
        w = Work(title="One Piece", description="lol", work_type="manga", version="v1")
        assert w.description == "lol"
        assert w.work_type == "manga"
        assert w.version == "v1"

    def test_ids_gerados_automaticamente(self):
        a = Work(title="A")
        b = Work(title="B")
        assert a.id != b.id


class TestClaim:
    def test_status_default_nao_confirmado(self):
        w = Work(title="W")
        s = Source(work_id=w.id, title="S")
        c = Claim(work_id=w.id, text="X", source_id=s.id)
        assert c.status is ClaimStatus.NAO_CONFIRMADO
        assert c.confidence == 0.0

    def test_confianca_deve_estar_entre_0_e_1(self):
        w = Work(title="W")
        s = Source(work_id=w.id, title="S")
        with pytest.raises(ValidationError):
            Claim(work_id=w.id, text="X", source_id=s.id, confidence=1.5)
        with pytest.raises(ValidationError):
            Claim(work_id=w.id, text="X", source_id=s.id, confidence=-0.1)

    def test_texto_obrigatorio(self):
        w = Work(title="W")
        s = Source(work_id=w.id, title="S")
        with pytest.raises(ValidationError):
            Claim(work_id=w.id, source_id=s.id)  # type: ignore[call-arg]


class TestSource:
    def test_tipo_padrao_primaria(self):
        w = Work(title="W")
        s = Source(work_id=w.id, title="S")
        assert s.source_type is SourceType.PRIMARIA

    def test_error_para_tipo_invalido(self):
        w = Work(title="W")
        with pytest.raises((ValueError, ValidationError)):
            Source(work_id=w.id, title="S", source_type="inexistente")  # type: ignore[arg-type]


class TestEvidence:
    def test_supports_obrigatorio(self):
        w = Work(title="W")
        s = Source(work_id=w.id, title="S")
        c = Claim(work_id=w.id, text="X", source_id=s.id)
        with pytest.raises(ValidationError):
            Evidence(claim_id=c.id, source_id=s.id, content="e")  # type: ignore[call-arg]

    def test_evidence_sustenta_ou_contradiz(self):
        w = Work(title="W")
        s = Source(work_id=w.id, title="S")
        c = Claim(work_id=w.id, text="X", source_id=s.id)
        assert Evidence(claim_id=c.id, source_id=s.id, content="e", supports=True)
        assert Evidence(claim_id=c.id, source_id=s.id, content="e", supports=False)
