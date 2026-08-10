"""Minimal CRUD repositories over the SQLAlchemy ORM for v0.1.

Each repository provides create / get / list for one entity. Conversion
between Pydantic domain models and ORM rows happens at this layer, so the
CLI and classifier work with Pydantic models and stay free of SQLAlchemy.
"""

from __future__ import annotations

from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from canonforge.db import (
    ClaimORM,
    EvidenceORM,
    SourceORM,
    WorkORM,
    to_uuid,
)
from canonforge.domain.models import Claim, Evidence, Source, Work

# ---------------------------------------------------------------------------
# Generic create/get/list
# ---------------------------------------------------------------------------


def _new_id() -> UUID:
    from uuid import uuid4

    return uuid4()


def create_work(session: Session, work: Work) -> Work:
    row = WorkORM(
        id=str(work.id),
        title=work.title,
        description=work.description,
        work_type=work.work_type,
        version=work.version,
        continuity=work.continuity,
        created_at=work.created_at,
    )
    session.add(row)
    session.flush()
    return work


def get_work(session: Session, work_id: UUID) -> Work | None:
    row = session.get(WorkORM, str(work_id))
    if row is None:
        return None
    return Work(
        id=to_uuid(row.id),
        title=row.title,
        description=row.description,
        work_type=row.work_type,
        version=row.version,
        continuity=row.continuity,
        created_at=row.created_at,
    )


def list_works(session: Session) -> list[Work]:
    rows = session.scalars(select(WorkORM).order_by(WorkORM.created_at)).all()
    return [
        Work(
            id=to_uuid(r.id),
            title=r.title,
            description=r.description,
            work_type=r.work_type,
            version=r.version,
            continuity=r.continuity,
            created_at=r.created_at,
        )
        for r in rows
    ]


# Source -------------------------------------------------------------------


def create_source(session: Session, source: Source) -> Source:
    row = SourceORM(
        id=str(source.id),
        work_id=str(source.work_id),
        title=source.title,
        url=source.url,
        source_type=source.source_type.value,
        authority=source.authority,
        origin_source_id=str(source.origin_source_id) if source.origin_source_id else None,
        created_at=source.created_at,
    )
    session.add(row)
    session.flush()
    return source


def get_source(session: Session, source_id: UUID) -> Source | None:
    row = session.get(SourceORM, str(source_id))
    if row is None:
        return None
    from canonforge.domain.taxonomy import SourceType

    return Source(
        id=to_uuid(row.id),
        work_id=to_uuid(row.work_id),
        title=row.title,
        url=row.url,
        source_type=SourceType(row.source_type),
        authority=row.authority,
        origin_source_id=to_uuid(row.origin_source_id) if row.origin_source_id else None,
        created_at=row.created_at,
    )


def list_sources(session: Session, work_id: UUID | None = None) -> list[Source]:
    from canonforge.domain.taxonomy import SourceType

    stmt = select(SourceORM).order_by(SourceORM.created_at)
    if work_id is not None:
        stmt = stmt.where(SourceORM.work_id == str(work_id))
    rows = session.scalars(stmt).all()
    return [
        Source(
            id=to_uuid(r.id),
            work_id=to_uuid(r.work_id),
            title=r.title,
            url=r.url,
            source_type=SourceType(r.source_type),
            authority=r.authority,
            origin_source_id=to_uuid(r.origin_source_id) if r.origin_source_id else None,
            created_at=r.created_at,
        )
        for r in rows
    ]


# Claim --------------------------------------------------------------------


def create_claim(session: Session, claim: Claim) -> Claim:
    row = ClaimORM(
        id=str(claim.id),
        work_id=str(claim.work_id),
        text=claim.text,
        source_id=str(claim.source_id),
        context=claim.context,
        location=claim.location,
        is_primary_source=claim.is_primary_source,
        status=claim.status.value,
        status_category=claim.status_category.value if claim.status_category else None,
        confidence=claim.confidence,
        validation=claim.validation.value,
        created_at=claim.created_at,
    )
    session.add(row)
    session.flush()
    return claim


def get_claim(session: Session, claim_id: UUID) -> Claim | None:
    row = session.get(ClaimORM, str(claim_id))
    if row is None:
        return None
    from canonforge.domain.taxonomy import (
        CanonCategory,
        ClaimStatus,
        Fandom,
        Interpretacao,
        ValidationStatus,
    )

    status_cat = None
    if row.status_category:
        for enum_cls in (CanonCategory, Interpretacao, Fandom):
            try:
                status_cat = enum_cls(row.status_category)
                break
            except ValueError:
                continue
    return Claim(
        id=to_uuid(row.id),
        work_id=to_uuid(row.work_id),
        text=row.text,
        source_id=to_uuid(row.source_id),
        context=row.context,
        location=row.location,
        is_primary_source=row.is_primary_source,
        status=ClaimStatus(row.status),
        status_category=status_cat,
        confidence=row.confidence,
        validation=ValidationStatus(row.validation),
        created_at=row.created_at,
    )


def list_claims(session: Session, work_id: UUID | None = None) -> list[Claim]:
    from canonforge.domain.taxonomy import (
        CanonCategory,
        ClaimStatus,
        Fandom,
        Interpretacao,
        ValidationStatus,
    )

    stmt = select(ClaimORM).order_by(ClaimORM.created_at)
    if work_id is not None:
        stmt = stmt.where(ClaimORM.work_id == str(work_id))
    rows = session.scalars(stmt).all()
    out: list[Claim] = []
    for r in rows:
        status_cat = None
        if r.status_category:
            for enum_cls in (CanonCategory, Interpretacao, Fandom):
                try:
                    status_cat = enum_cls(r.status_category)
                    break
                except ValueError:
                    continue
        out.append(
            Claim(
                id=to_uuid(r.id),
                work_id=to_uuid(r.work_id),
                text=r.text,
                source_id=to_uuid(r.source_id),
                context=r.context,
                location=r.location,
                is_primary_source=r.is_primary_source,
                status=ClaimStatus(r.status),
                status_category=status_cat,
                confidence=r.confidence,
                validation=ValidationStatus(r.validation),
                created_at=r.created_at,
            )
        )
    return out


def update_claim(session: Session, claim: Claim) -> Claim:
    row = session.get(ClaimORM, str(claim.id))
    if row is None:
        raise KeyError(f"Claim {claim.id} not found")
    row.status = claim.status.value
    row.status_category = claim.status_category.value if claim.status_category else None
    row.confidence = claim.confidence
    row.validation = claim.validation.value
    session.flush()
    return claim


# Evidence -----------------------------------------------------------------


def create_evidence(session: Session, evidence: Evidence) -> Evidence:
    row = EvidenceORM(
        id=str(evidence.id),
        claim_id=str(evidence.claim_id),
        source_id=str(evidence.source_id),
        content=evidence.content,
        supports=evidence.supports,
        location=evidence.location,
        created_at=evidence.created_at,
    )
    session.add(row)
    session.flush()
    return evidence


def get_evidence(session: Session, evidence_id: UUID) -> Evidence | None:
    row = session.get(EvidenceORM, str(evidence_id))
    if row is None:
        return None
    return Evidence(
        id=to_uuid(row.id),
        claim_id=to_uuid(row.claim_id),
        source_id=to_uuid(row.source_id),
        content=row.content,
        supports=row.supports,
        location=row.location,
        created_at=row.created_at,
    )


def list_evidence(session: Session, claim_id: UUID | None = None) -> list[Evidence]:
    stmt = select(EvidenceORM).order_by(EvidenceORM.created_at)
    if claim_id is not None:
        stmt = stmt.where(EvidenceORM.claim_id == str(claim_id))
    rows = session.scalars(stmt).all()
    return [
        Evidence(
            id=to_uuid(r.id),
            claim_id=to_uuid(r.claim_id),
            source_id=to_uuid(r.source_id),
            content=r.content,
            supports=r.supports,
            location=r.location,
            created_at=r.created_at,
        )
        for r in rows
    ]


__all__ = [
    "create_claim",
    "create_evidence",
    "create_source",
    "create_work",
    "get_claim",
    "get_evidence",
    "get_source",
    "get_work",
    "list_claims",
    "list_evidence",
    "list_sources",
    "list_works",
    "update_claim",
]
