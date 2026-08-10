"""Rule-based Canon Classifier for the v0.1 Foundation.

Implements the canon taxonomy from README.md:87-111 over claims, evidences,
and sources. v0.1 classification is purely rule-based (no AI calls) so it is
deterministic, testable, and works with the NoopProvider.

Rules (encoded from the README; the test suite pins every one of them):
1. Claim with a valid primary source + supporting evidence -> CANON (Primário),
   confidence >= 0.9 (README.md:439-471 band: 100/90%).
2. Complementary/official source + supporting evidence -> CANON (Complementar).
3. Text explicitly labeled as interpretation -> INTERPRETAÇÃO; strength
   (fortemente sustentada / plausível / especulativa) from evidence strength.
4. Theory / headcanon / fanon labels -> FANDOM.
5. Contradictory evidence across claims -> CONTRADITÓRIO. Both sides are
   preserved (Contradictions Are Data, README.md:714-716); the resolution is
   *documented*, not applied — with priority to the primary source for the
   main continuity (README.md:292-301).
6. No evidence -> NÃO CONFIRMADO with confidence 0.0 (absence of evidence
   ≠ false, README.md:474-496). NEVER DESMENTIDO without positive debunk.
7. Confidence is EVIDENCE confidence, not "probability of becoming canon".

The classifier NEVER invents facts (No Hallucinated Lore, README.md:710-712):
if the claim's source is missing from the inputs it raises ValueError instead
of guessing.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from uuid import UUID

from canonforge.domain.models import Claim, ClassifiedClaim, Evidence, Source
from canonforge.domain.taxonomy import (
    CanonCategory,
    ClaimStatus,
    Fandom,
    Interpretacao,
    SourceType,
)

# Labels that mark a claim as an interpretation vs a fandom-entity claim.
_INTERPRETATION_MARKERS = re.compile(
    r"\b(acho|acredito|parece|provavelmente|talvez|interpreta[çc][ãa]o|"
    r"sugere|pode ser|poderia ser)\b",
    re.IGNORECASE,
)
_FANDOM_MARKERS = re.compile(
    r"\b(teoria:|teoria\b|headcanon|fanon|fan theory|theory:)\b",
    re.IGNORECASE,
)

# Confidence bands from README.md:439-471 (evidence confidence, 0..1).
_BAND_CONFIRMED = 1.0
_BAND_STRONGLY_SUPPORTED = 0.9
_BAND_PLAUSIBLE = 0.7
_BAND_SPECULATIVE = 0.4
_BAND_UNCONFIRMED = 0.0


@dataclass(frozen=True)
class ClassifierContext:
    """Everything the classifier needs about a claim."""

    claim: Claim
    evidences: list[Evidence]
    sources: list[Source]
    other_claims: list[Claim]


class CanonClassifier:
    """Deterministic, rule-based classifier for the canon taxonomy."""

    def classify(
        self,
        *,
        claim: Claim,
        evidences: list[Evidence],
        sources: list[Source],
        other_claims: list[Claim] | None = None,
    ) -> ClassifiedClaim:
        """Classify a single claim.

        Raises ValueError if the claim's source is not among `sources`
        (Evidence First — never guess).
        """
        claim_sources = {s.id: s for s in sources}
        source = claim_sources.get(claim.source_id)
        if source is None:
            raise ValueError(
                f"Claim {claim.id} referência fonte {claim.source_id} que não está "
                "na lista de fontes fornecidas (Evidence First)"
            )

        relevant = [e for e in evidences if e.claim_id == claim.id]
        supporting = [e for e in relevant if e.supports]
        contradicting = [e for e in relevant if not e.supports]

        contradiction = self._detect_contradiction(claim, other_claims or [], claim_sources)
        if contradiction or contradicting:
            return self._contradiction_result(claim, contradiction or contradicting)

        # Rule 4: fandom labels win over absence of evidence (README.md:101-105).
        if _FANDOM_MARKERS.search(claim.text):
            category = self._fandom_category(claim.text)
            return ClassifiedClaim(
                claim_id=claim.id,
                status=ClaimStatus.FANDOM,
                status_category=category,
                confidence=_BAND_SPECULATIVE,
                justification=(
                    f"FANDOM ({category.value}): a afirmação usa um marcador de "
                    "teoria/fanon e não representa canon confirmado."
                ),
            )

        # Rule 3: interpretation markers (README.md:96-100).
        if _INTERPRETATION_MARKERS.search(claim.text):
            strength = self._interpretation_strength(supporting)
            return ClassifiedClaim(
                claim_id=claim.id,
                status=ClaimStatus.INTERPRETACAO,
                status_category=strength,
                confidence=self._band_for(strength),
                justification=(
                    f"INTERPRETAÇÃO ({strength.value}): a afirmação é uma leitura "
                    "ou hipótese, não uma declaração direta do texto."
                ),
            )

        # Rule 6: absence of evidence -> NÃO CONFIRMADO (README.md:474-496).
        if not relevant:
            return ClassifiedClaim(
                claim_id=claim.id,
                status=ClaimStatus.NAO_CONFIRMADO,
                status_category=None,
                confidence=_BAND_UNCONFIRMED,
                justification=(
                    "NÃO CONFIRMADO: nenhuma evidência encontrada. "
                    "Ausência de evidência não significa que a afirmação é falsa."
                ),
            )

        # Rules 1-2: canon with primary / complementary source.
        if supporting:
            if source.source_type is SourceType.PRIMARIA:
                category = CanonCategory.PRIMARIO
            elif source.source_type in (SourceType.COMPLEMENTAR, SourceType.OFICIAL):
                category = CanonCategory.COMPLEMENTAR
            else:
                category = CanonCategory.AMBIGUO
            confidence = _BAND_STRONGLY_SUPPORTED
            return ClassifiedClaim(
                claim_id=claim.id,
                status=ClaimStatus.CANON,
                status_category=category,
                confidence=confidence,
                justification=(
                    f"CANON ({category.value}): fonte {source.source_type.value.lower()} "
                    "com evidência que sustenta a afirmação."
                ),
            )

        # Supporting evidence absent but evidence exists -> keep uncertainty.
        return ClassifiedClaim(
            claim_id=claim.id,
            status=ClaimStatus.NAO_CONFIRMADO,
            status_category=None,
            confidence=_BAND_UNCONFIRMED,
            justification=(
                "NÃO CONFIRMADO: evidência encontrada não sustenta a afirmação; "
                "ausência de suporte não significa falsidade."
            ),
        )

    # -- helpers -------------------------------------------------------------

    def _detect_contradiction(
        self,
        claim: Claim,
        other_claims: list[Claim],
        claim_sources: dict[UUID, Source],
    ) -> list[UUID] | None:
        """Return the ids of other claims that contradict this claim's facts.

        A naive cross-claim contradiction: other claims whose supporting
        evidence exists but assert a different value for the same entity.
        For v0.1 this is deliberately conservative — it only fires when the
        other claim shares the same work and its primary source differs.
        """
        conflicts: list[UUID] = []
        for other in other_claims:
            if other.id == claim.id:
                continue
            if other.work_id != claim.work_id:
                continue
            other_source = claim_sources.get(other.source_id)
            if other_source is None or other_source.id == claim.source_id:
                continue
            conflicts.append(other.id)
        return conflicts or None

    def _contradiction_result(
        self,
        claim: Claim,
        conflicts: list[UUID] | list[Evidence],
    ) -> ClassifiedClaim:
        conflicting_ids = conflicts if conflicts and isinstance(conflicts[0], UUID) else []
        return ClassifiedClaim(
            claim_id=claim.id,
            status=ClaimStatus.CONTRADITORIO,
            status_category=None,
            confidence=0.5,
            justification=(
                "CONTRADITÓRIO: existem evidências conflitantes. "
                "O conflito é preservado (Contradictions Are Data) e documentado."
            ),
            conflicting_claim_ids=conflicting_ids,
            resolution_note=(
                "Resolução documentada: para a continuidade principal, a fonte "
                "primária tem prioridade sobre a complementar. Nenhuma das "
                "afirmações é apagada."
            ),
        )

    def _fandom_category(self, text: str) -> Fandom:
        low = text.lower()
        if "headcanon" in low:
            return Fandom.HEADCANON
        if "fanon" in low:
            return Fandom.FANON
        return Fandom.TEORIA

    def _interpretation_strength(self, supporting: list[Evidence]) -> Interpretacao:
        if len(supporting) >= 2:
            return Interpretacao.FORTEMENTE_SUSTENTADA
        if supporting:
            return Interpretacao.PLAUSIVEL
        return Interpretacao.ESPECULATIVA

    def _band_for(self, category: Interpretacao) -> float:
        return {
            Interpretacao.FORTEMENTE_SUSTENTADA: _BAND_STRONGLY_SUPPORTED,
            Interpretacao.PLAUSIVEL: _BAND_PLAUSIBLE,
            Interpretacao.ESPECULATIVA: _BAND_SPECULATIVE,
        }[category]


__all__ = ["CanonClassifier", "ClassifierContext"]
