"""Tests for the Typer CLI — happy path and failure cases via CliRunner."""

from __future__ import annotations

from typer.testing import CliRunner

from canonforge.cli import app

runner = CliRunner()


class TestHelp:
    def test_help_lista_comandos(self):
        result = runner.invoke(app, ["--help"])
        assert result.exit_code == 0
        assert "init" in result.output
        assert "work" in result.output
        assert "source" in result.output
        assert "claim" in result.output
        assert "evidence" in result.output
        assert "classify" in result.output


class TestInit:
    def test_init_cria_banco(self, tmp_path, monkeypatch):
        from sqlalchemy.orm import sessionmaker

        import canonforge.cli as cli_mod
        from canonforge.db import Base, make_engine

        eng = make_engine(f"sqlite:///{tmp_path / 'init.db'}")
        Base.metadata.create_all(bind=eng)
        monkeypatch.setattr(cli_mod, "init_db", lambda: Base.metadata.create_all(bind=eng))
        monkeypatch.setattr(
            cli_mod, "SessionLocal", sessionmaker(bind=eng, expire_on_commit=False)
        )
        result = runner.invoke(app, ["init"])
        assert result.exit_code == 0
        assert (tmp_path / "init.db").exists()


class TestClassifyFailure:
    def test_classify_claim_inexistente(self, tmp_path, monkeypatch):
        from sqlalchemy.orm import sessionmaker

        import canonforge.cli as cli_mod
        from canonforge.db import Base, make_engine

        eng = make_engine(f"sqlite:///{tmp_path / 'q.db'}")
        Base.metadata.create_all(bind=eng)
        monkeypatch.setattr(
            cli_mod, "SessionLocal", sessionmaker(bind=eng, expire_on_commit=False)
        )
        result = runner.invoke(
            app, ["classify", "--claim-id", "00000000-0000-0000-0000-000000000000"]
        )
        assert result.exit_code != 0
        assert "encontrada" in result.output.lower()
