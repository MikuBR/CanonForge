"""Tests for the CanonClassifier — encoded from README domain rules.

Critical domain rules under test (README.md:87-111, 272-307, 439-496, 690-733):
1. Claim with valid primary source + supporting evidence -> CANON (Primário), high confidence.
2. Secondary/complementary source + evidence -> CANON (Complementar).
3. Explicitly labeled interpretation -> INTERPRETAÇÃO (strength by evidence).
4. Theory/headcanon/fanon -> FANDOM.
5. Contradictory evidence -> CONTRADITÓRIO, BOTH claims preserved, never resolved
   silently; resolution documented with primary-source priority (README.md:292-301).
6. No evidence -> NÃO CONFIRMADO with confidence 0.0 (NEVER FALSO/DESMENTIDO —
   README.md:474-496).
7. Confidence is evidence confidence (1.0/0.9/0.7/0.4/0.0 bands, README.md:439-471),
   NOT probability of becoming canon.
"""

from __future__ import annotations

from uuid import uuid4

import pytest

from canonforge.classifier import CanonClassifier
from canonforge.domain.models import Claim, Evidence, Source
from canonforge.domain.taxonomy import (
    CanonCategory,
    ClaimStatus,
    Fandom,
    Interpretacao,
    SourceType,
)

CLASSIFIER = CanonClassifier()


def _source(source_type: SourceType = SourceType.PRIMARIA) -> Source:
    return Source(
        work_id=uuid4(),
        title=f"src-{uuid4()}",
        source_type=source_type,
    )


def _claim(source: Source, text: str = "X aconteceu.") -> Claim:
    return Claim(work_id=source.work_id, text=text, source_id=source.id)


def _evidence(claim: Claim, source: Source, supports: bool) -> Evidence:
    return Evidence(
        claim_id=claim.id,
        source_id=source.id,
        content="evidência",
        supports=supports,
    )


# --- Rule 6: absence of evidence -------------------------------------------


def test_sem_evidencia_nao_confirmado_nunca_falso():
    """Sem evidência => NÃO CONFIRMADO, confidence 0.0 (nunca DESMENTIDO/FALSO)."""
    src = _source()
    claim = _claim(src)
    result = CLASSIFIER.classify(claim=claim, evidences=[], sources=[src])
    assert result.status is ClaimStatus.NAO_CONFIRMADO
    assert result.confidence == 0.0
    low = result.justification.lower()
    assert "não confirm" in low or "sem evid" in low


# --- Rule 1: primary source + supporting evidence -------------------------


def test_fonte_primaria_com_evidencia_canon_primario():
    src = _source(SourceType.PRIMARIA)
    claim = _claim(src, "X aconteceu.")
    ev = _evidence(claim, src, supports=True)
    result = CLASSIFIER.classify(claim=claim, evidences=[ev], sources=[src])
    assert result.status is ClaimStatus.CANON
    assert result.status_category is CanonCategory.PRIMARIO
    assert result.confidence >= 0.9


# --- Rule 2: complementary source -----------------------------------------


def test_fonte_complementar_canon_complementar():
    src = _source(SourceType.COMPLEMENTAR)
    claim = _claim(src)
    ev = _evidence(claim, src, supports=True)
    result = CLASSIFIER.classify(claim=claim, evidences=[ev], sources=[src])
    assert result.status is ClaimStatus.CANON
    assert result.status_category is CanonCategory.COMPLEMENTAR


# --- Rule 3: interpretation ------------------------------------------------


def test_interpretacao_rotulada_eh_interpretacao():
    src = _source()
    claim = _claim(src, "Eu acho que X aconteceu.")
    ev = _evidence(claim, src, supports=True)
    result = CLASSIFIER.classify(claim=claim, evidences=[ev], sources=[src])
    assert result.status is ClaimStatus.INTERPRETACAO
    assert result.status_category in (
        Interpretacao.FORTEMENTE_SUSTENTADA,
        Interpretacao.PLAUSIVEL,
        Interpretacao.ESPECULATIVA,
    )


# --- Rule 4: fandom ---------------------------------------------------------


def test_teoria_eh_fandom():
    src = _source()
    claim = _claim(src, "Teoria: X é na verdade Y.")
    result = CLASSIFIER.classify(claim=claim, evidences=[], sources=[src])
    assert result.status is ClaimStatus.FANDOM
    assert result.status_category is Fandom.TEORIA


def test_headcanon_eh_fandom():
    src = _source()
    claim = _claim(src, "Headcanon: X faria isso.")
    result = CLASSIFIER.classify(claim=claim, evidences=[], sources=[src])
    assert result.status is ClaimStatus.FANDOM
    assert result.status_category is Fandom.HEADCANON


# --- Rule 5: contradictions are data ---------------------------------------


def test_contradicao_preserva_ambos_e_documenta_resolucao():
    """Evidência contraditória => CONTRADITÓRIO; ambos os lados preservados;
    resolução documentada com prioridade para a fonte primária."""
    work_id = uuid4()
    src_primary = Source(work_id=work_id, title="manga", source_type=SourceType.PRIMARIA)
    src_complement = Source(work_id=work_id, title="databook", source_type=SourceType.COMPLEMENTAR)
    claim_a = Claim(work_id=work_id, text="X nasceu em 1982.", source_id=src_primary.id)
    claim_b = Claim(work_id=work_id, text="X nasceu em 1980.", source_id=src_complement.id)

    ev_a = _evidence(claim_a, src_primary, supports=True)
    ev_b = _evidence(claim_b, src_complement, supports=True)

    result = CLASSIFIER.classify(
        claim=claim_a,
        evidences=[ev_a, ev_b],
        sources=[src_primary, src_complement],
        other_claims=[claim_b],
    )
    assert result.status is ClaimStatus.CONTRADITORIO
    # Ambas as claims preservadas — nunca resolver silenciosamente (README.md:303-307)
    assert len(result.conflicting_claim_ids) == 1
    assert claim_b.id in result.conflicting_claim_ids
    # Resolução documentada: fonte primária tem prioridade (README.md:292-301)
    assert result.resolution_note is not None
    assert "primár" in result.resolution_note.lower()


def test_sem_contradicao_sem_falha_de_contradicao():
    src = _source(SourceType.PRIMARIA)
    claim = _claim(src)
    ev = _evidence(claim, src, supports=True)
    result = CLASSIFIER.classify(claim=claim, evidences=[ev], sources=[src])
    assert result.status is not ClaimStatus.CONTRADITORIO
    assert result.conflicting_claim_ids == []


# --- Rule 7: confidence bands -----------------------------------------------


def test_confianca_eh_da_evidencia_nao_probabilidade():
    """Confidence banda 1.0/0.9/0.7/0.4/0.0 — evidência forte => alta,
    sem evidência => 0.0."""
    src = _source(SourceType.PRIMARIA)
    claim = _claim(src)
    no_evidence = CLASSIFIER.classify(claim=claim, evidences=[], sources=[src])
    assert no_evidence.confidence == 0.0

    strong_ev = _evidence(claim, src, supports=True)
    strong = CLASSIFIER.classify(claim=claim, evidences=[strong_ev], sources=[src])
    assert strong.confidence >= 0.9


# --- No hallucinated lore / evidence first ----------------------------------


def test_nao_aceita_claim_sem_fonte():
    """Evidence First (README.md:694-697): classificar um claim cuja fonte
    não está presente na lista deve falhar ou retornar erro — nunca inventar."""
    src = _source()
    claim = _claim(src)
    with pytest.raises(ValueError):
        CLASSIFIER.classify(claim=claim, evidences=[], sources=[])
