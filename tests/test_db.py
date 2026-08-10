"""Tests for the database layer — SQLAlchemy SQLite persistence, CRUD, FK."""

from __future__ import annotations

import pytest
from sqlalchemy import inspect
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from canonforge import repository as repo
from canonforge.db import Base, make_engine
from canonforge.domain.models import Claim, Evidence, Source, Work
from canonforge.domain.taxonomy import SourceType


@pytest.fixture()
def session():
    eng = make_engine("sqlite:///:memory:")
    Base.metadata.create_all(bind=eng)
    with Session(eng) as s:
        yield s


class TestTableCreation:
    def test_tabelas_criadas(self):
        eng = make_engine("sqlite:///:memory:")
        Base.metadata.create_all(bind=eng)
        tables = set(inspect(eng).get_table_names())
        assert {"work", "source", "claim", "evidence"} <= tables


class TestWorkCrud:
    def test_create_get_list(self, session):
        w = repo.create_work(session, Work(title="Naruto", work_type="manga"))
        session.commit()
        assert repo.get_work(session, w.id) is not None
        assert len(repo.list_works(session)) == 1

    def test_get_inexistente_retorna_none(self, session):
        from uuid import uuid4

        assert repo.get_work(session, uuid4()) is None


class TestClaimCrud:
    def _work_and_source(self, session) -> tuple[Work, Source]:
        w = repo.create_work(session, Work(title="Naruto"))
        s = repo.create_source(
            session, Source(work_id=w.id, title="Cap 1", source_type=SourceType.PRIMARIA)
        )
        session.commit()
        return w, s

    def test_create_get_list(self, session):
        w, s = self._work_and_source(session)
        c = repo.create_claim(
            session, Claim(work_id=w.id, text="Naruto quer ser Hokage", source_id=s.id)
        )
        session.commit()
        got = repo.get_claim(session, c.id)
        assert got is not None
        assert got.status.value == "NÃO CONFIRMADO"
        assert len(repo.list_claims(session)) == 1

    def test_fk_violation_claim_sem_source(self, session):
        w = repo.create_work(session, Work(title="Naruto"))
        session.commit()
        from uuid import uuid4

        bad = Claim(work_id=w.id, text="X", source_id=uuid4())
        with pytest.raises(IntegrityError):
            repo.create_claim(session, bad)
            session.commit()


class TestEvidenceCrud:
    def test_criar_e_listar_por_claim(self, session):

        w = repo.create_work(session, Work(title="Naruto"))
        s = repo.create_source(
            session, Source(work_id=w.id, title="Cap 1", source_type=SourceType.PRIMARIA)
        )
        c = repo.create_claim(session, Claim(work_id=w.id, text="X", source_id=s.id))
        session.commit()
        e = repo.create_evidence(
            session,
            Evidence(claim_id=c.id, source_id=s.id, content="painel", supports=True),
        )
        session.commit()
        evs = repo.list_evidence(session, claim_id=c.id)
        assert len(evs) == 1
        assert evs[0].id == e.id
        assert evs[0].supports is True
