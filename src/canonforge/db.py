"""SQLAlchemy 2.0 ORM models, SQLite engine, and session factory for v0.1.

Database decision (user-confirmed in plan): SQLite for v0.1, via SQLAlchemy 2.0.
PostgreSQL/pgvector is a v0.2+ concern (README.md:753-757).

The ORM models mirror the Pydantic domain models in domain/models.py but
store enum values as strings (the pt-BR labels from taxonomy.py) for
human-readable SQLite inspection. UUIDs are stored as strings (SQLite has no
native UUID type).

Domain invariant: Contradictions Are Data (README.md:714-716) — no CRUD
operation here ever silently deletes or overwrites a claim that participates
in a contradiction. Deletion is plain delete; soft-merge is NOT provided.

NOTE: SQLite does not enforce foreign keys unless PRAGMA foreign_keys=ON is
set per connection. make_engine() enables it via the connect event so FK
violations (e.g. a Claim with an unknown source_id) actually raise.
"""

from __future__ import annotations

import os
from collections.abc import Generator
from datetime import UTC, datetime
from uuid import UUID, uuid4

from sqlalchemy import ForeignKey, String, create_engine, event, select
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    Session,
    mapped_column,
    sessionmaker,
)


class Base(DeclarativeBase):
    pass


def _now() -> datetime:
    return datetime.now(UTC)


def _uuid() -> str:
    return str(uuid4())


# Engine + session factory ------------------------------------------------

DEFAULT_DB_URL = "sqlite:///canonforge.db"


def _get_db_url() -> str:
    return os.environ.get("CANONFORGE_DB", DEFAULT_DB_URL)


def make_engine(db_url: str | None = None):
    """Create a SQLAlchemy engine. Defaults to CANONFORGE_DB env or local file.

    For tests, pass a url like sqlite:///:memory: or use init_db(url=...).

    SQLite: enables PRAGMA foreign_keys=ON per connection so foreign-key
    constraints are actually enforced (SQLite default is OFF).
    """
    url = db_url or _get_db_url()
    connect_args = {"check_same_thread": False} if url.startswith("sqlite") else {}
    eng = create_engine(url, echo=False, connect_args=connect_args)
    if url.startswith("sqlite"):

        @event.listens_for(eng, "connect")
        def _enable_fk(dbapi_conn, _record):
            cursor = dbapi_conn.cursor()
            cursor.execute("PRAGMA foreign_keys=ON")
            cursor.close()

    return eng


engine = make_engine()
SessionLocal = sessionmaker(bind=engine, expire_on_commit=False)


def get_session() -> Generator[Session, None, None]:
    """Context-managed session for dependency injection / CLI use."""
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()


def init_db(db_url: str | None = None) -> None:
    """Create all tables. If db_url is given, use a fresh engine for that url
    (useful for tests with :memory:). Otherwise uses the default engine."""
    eng = make_engine(db_url) if db_url else engine
    Base.metadata.create_all(bind=eng)


# ORM models ---------------------------------------------------------------


class WorkORM(Base):
    __tablename__ = "work"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=_uuid)
    title: Mapped[str] = mapped_column(String(512), nullable=False)
    description: Mapped[str | None] = mapped_column(String, nullable=True)
    work_type: Mapped[str | None] = mapped_column(String(64), nullable=True)
    version: Mapped[str | None] = mapped_column(String(128), nullable=True)
    continuity: Mapped[str | None] = mapped_column(String(128), nullable=True)
    created_at: Mapped[datetime] = mapped_column(default=_now)


class SourceORM(Base):
    __tablename__ = "source"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=_uuid)
    work_id: Mapped[str] = mapped_column(ForeignKey("work.id"), nullable=False, index=True)
    title: Mapped[str] = mapped_column(String(512), nullable=False)
    url: Mapped[str | None] = mapped_column(String(2048), nullable=True)
    source_type: Mapped[str] = mapped_column(String(64), nullable=False, default="Primária")
    authority: Mapped[float | None] = mapped_column(nullable=True)
    origin_source_id: Mapped[str | None] = mapped_column(
        ForeignKey("source.id"), nullable=True
    )
    created_at: Mapped[datetime] = mapped_column(default=_now)


class ClaimORM(Base):
    __tablename__ = "claim"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=_uuid)
    work_id: Mapped[str] = mapped_column(ForeignKey("work.id"), nullable=False, index=True)
    text: Mapped[str] = mapped_column(String, nullable=False)
    source_id: Mapped[str] = mapped_column(ForeignKey("source.id"), nullable=False, index=True)
    context: Mapped[str | None] = mapped_column(String, nullable=True)
    location: Mapped[str | None] = mapped_column(String(512), nullable=True)
    is_primary_source: Mapped[bool] = mapped_column(default=False)
    status: Mapped[str] = mapped_column(String(64), nullable=False, default="NÃO CONFIRMADO")
    status_category: Mapped[str | None] = mapped_column(String(64), nullable=True)
    confidence: Mapped[float] = mapped_column(default=0.0)
    validation: Mapped[str] = mapped_column(String(32), nullable=False, default="Pendente")
    created_at: Mapped[datetime] = mapped_column(default=_now)


class EvidenceORM(Base):
    __tablename__ = "evidence"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=_uuid)
    claim_id: Mapped[str] = mapped_column(ForeignKey("claim.id"), nullable=False, index=True)
    source_id: Mapped[str] = mapped_column(ForeignKey("source.id"), nullable=False, index=True)
    content: Mapped[str] = mapped_column(String, nullable=False)
    supports: Mapped[bool] = mapped_column(nullable=False)
    location: Mapped[str | None] = mapped_column(String(512), nullable=True)
    created_at: Mapped[datetime] = mapped_column(default=_now)


# Conversion helpers (ORM <-> Pydantic domain models) ---------------------


def to_uuid(val: str) -> UUID:
    return UUID(val) if isinstance(val, str) else val


__all__ = [
    "Base",
    "ClaimORM",
    "EvidenceORM",
    "SessionLocal",
    "SourceORM",
    "WorkORM",
    "engine",
    "get_session",
    "init_db",
    "make_engine",
    "select",
    "to_uuid",
]
