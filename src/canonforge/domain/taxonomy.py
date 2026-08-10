"""Canon taxonomy enums with exact pt-BR labels from the README.

The taxonomy is NOT binary true/false. It has four top-level categories
(CANON, INTERPRETAÇÃO, FANDOM, plus three standalone statuses) plus
sub-categories. See README.md:87-111.

Design rule (README.md:474-496): absence of evidence ≠ false.
"Não encontramos evidência de X" -> NÃO CONFIRMADO (never DESMENTIDO).
"""

from __future__ import annotations

from enum import Enum


class ClaimStatus(Enum):
    """Top-level claim status. The enum NAME is ASCII (for code);
    the enum VALUE is the exact pt-BR label (for display and persistence)."""

    CANON = "CANON"
    INTERPRETACAO = "INTERPRETAÇÃO"
    FANDOM = "FANDOM"
    NAO_CONFIRMADO = "NÃO CONFIRMADO"
    CONTRADITORIO = "CONTRADITÓRIO"
    DESMENTIDO = "DESMENTIDO"


class CanonCategory(Enum):
    """Sub-categories of CANON (README.md:90-95)."""

    PRIMARIO = "Primário"
    COMPLEMENTAR = "Complementar"
    ADAPTACAO = "Adaptação"
    AMBIGUO = "Ambíguo"


class Interpretacao(Enum):
    """Sub-categories of INTERPRETAÇÃO (README.md:96-100)."""

    FORTEMENTE_SUSTENTADA = "Fortemente sustentada"
    PLAUSIVEL = "Plausível"
    ESPECULATIVA = "Especulativa"


class Fandom(Enum):
    """Sub-categories of FANDOM (README.md:101-105)."""

    TEORIA = "Teoria"
    HEADCANON = "Headcanon"
    FANON = "Fanon"


class SourceType(Enum):
    """Type of a source, used by the classifier for canon hierarchy.

    README.md:256-268 lists the factors the Canon Classifier considers:
    type of source, continuity, authority, evidence, contradictions, etc.
    """

    PRIMARIA = "Primária"
    COMPLEMENTAR = "Complementar"
    ADAPTACAO = "Adaptação"
    OFICIAL = "Oficial"


class ValidationStatus(Enum):
    """Validation state of a claim (README.md:59-73 pipeline)."""

    PENDENTE = "Pendente"
    VALIDADA = "Validada"
    INVALIDADA = "Invalidada"


__all__ = [
    "CanonCategory",
    "ClaimStatus",
    "Fandom",
    "Interpretacao",
    "SourceType",
    "ValidationStatus",
]
