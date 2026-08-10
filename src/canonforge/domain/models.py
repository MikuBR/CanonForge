"""Pydantic v2 domain models for the CanonForge pipeline.

Pipeline (README.md:59-73):
    Informação -> Afirmação (Claim) -> Fonte -> Evidência
              -> Validação -> Classificação -> Conhecimento

Entities (README.md:823-829):
    Work, Source, Claim, Evidence.

Domain invariants encoded here:
- Evidence First (README.md:694-697): a Claim carries traceable evidence.
- Source Traceability (README.md:698-700): every Source points to an origin.
- Uncertainty Preservation (README.md:701-703): confidence is a 0..1 float
  representing evidence confidence, NOT probability of becoming canon.
- No Hallucinated Lore (README.md:710-712): models never store invented facts;
  a Claim with no evidence is NÃO CONFIRMADO, never FALSO.
- Canon Separation (README.md:704-706): canon/interpretação/fandom stay separated
  via the taxonomy enums in taxonomy.py.
"""

from __future__ import annotations

from datetime import UTC, datetime
from typing import Annotated
from uuid import UUID, uuid4

from pydantic import BaseModel, Field

from canonforge.domain.taxonomy import (
    CanonCategory,
    ClaimStatus,
    Fandom,
    Interpretacao,
    SourceType,
    ValidationStatus,
)

# Confidence is evidence confidence in [0.0, 1.0].
Confidence = Annotated[float, Field(ge=0.0, le=1.0)]


def _now_utc() -> datetime:
    return datetime.now(UTC)


class Work(BaseModel):
    """A fictional work (anime, manga, novel, game, shared universe).

    README.md:117-128 (Arquitetura Conceitual): the pipeline starts by
    identifying the work / version / continuity.
    """

    id: UUID = Field(default_factory=uuid4)
    title: str
    description: str | None = None
    work_type: str | None = None  # anime / manga / novel / game / ...
    version: str | None = None  # e.g. "S1 manga", "anime 2024"
    continuity: str | None = None  # e.g. "main", "anime-only", "filler"
    created_at: datetime = Field(default_factory=_now_utc)


class Source(BaseModel):
    """A source for a claim. README.md:184-200 (Researcher), 256-268 (Classifier).

    Source Traceability (README.md:698-700, 500-525): 50 sites copying the same
    claim may trace to a single primary origin. The `origin_source_id` field
    allows building that trace chain. Copies are NOT independent sources.
    """

    id: UUID = Field(default_factory=uuid4)
    work_id: UUID
    title: str
    url: str | None = None
    source_type: SourceType = SourceType.PRIMARIA
    authority: float | None = None  # 0..1 qualitative authority weight
    origin_source_id: UUID | None = None  # trace chain to primary origin
    created_at: datetime = Field(default_factory=_now_utc)


class Claim(BaseModel):
    """A single verifiable claim extracted from a source.

    README.md:202-224 (Claim Extractor). A claim has a text, the source it
    came from, context, location, and a primary-source flag. Classification
    status and confidence are set by the CanonClassifier.
    """

    id: UUID = Field(default_factory=uuid4)
    work_id: UUID
    text: str
    source_id: UUID
    context: str | None = None
    location: str | None = None  # e.g. "Jujutsu Kaisen, Capítulo X"
    is_primary_source: bool = False
    status: ClaimStatus = ClaimStatus.NAO_CONFIRMADO
    status_category: CanonCategory | Interpretacao | Fandom | None = None
    confidence: Confidence = 0.0
    validation: ValidationStatus = ValidationStatus.PENDENTE
    created_at: datetime = Field(default_factory=_now_utc)


class Evidence(BaseModel):
    """Evidence that supports or contradicts a claim.

    README.md:228-241 (Evidence Engine): CLAIM -> Evidence A/B/C -> Support/Contradiction.
    README.md:243-253 (Validator): "A fonte diz isso ou estamos interpretando a fonte?"

    `supports=True` -> this evidence supports the claim.
    `supports=False` -> this evidence contradicts the claim (Contradictions Are Data,
    README.md:714-716: contradictions are never erased; the Contradiction Detector
    preserves both sides and documents the resolution).
    """

    id: UUID = Field(default_factory=uuid4)
    claim_id: UUID
    source_id: UUID
    content: str
    supports: bool
    location: str | None = None
    created_at: datetime = Field(default_factory=_now_utc)


class ClassifiedClaim(BaseModel):
    """Result of running the CanonClassifier over a claim + its evidence.

    Contradictions Are Data (README.md:714-716): when a claim is in
    CONTRADITORIO status, `conflicting_claim_ids` preserves the other side(s)
    and `resolution_note` documents which source has priority and why.
    Absence of evidence (README.md:474-496): when there is no evidence,
    status is NÃO CONFIRMADO with confidence 0.0 — never DESMENTIDO.
    """

    claim_id: UUID
    status: ClaimStatus
    status_category: CanonCategory | Interpretacao | Fandom | None = None
    confidence: Confidence = 0.0
    justification: str
    conflicting_claim_ids: list[UUID] = Field(default_factory=list)
    resolution_note: str | None = None


__all__ = [
    "Claim",
    "ClassifiedClaim",
    "Confidence",
    "Evidence",
    "Source",
    "Work",
]
