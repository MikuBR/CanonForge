"""Initial Typer CLI for the CanonForge v0.1 Foundation.

Commands (README.md:823-829):
    init                 - create the SQLite database
    work add             - register a fictional work
    source add           - register a source for a work
    claim add            - register a claim extracted from a source
    evidence add         - attach evidence supporting/contradicting a claim
    classify             - run the rule-based CanonClassifier on a claim

Output labels are the exact pt-BR taxonomy labels (README.md:87-111).
No v0.2+ commands (research, extraction, KG, learning) exist here.
"""

from __future__ import annotations

from uuid import UUID

import typer

from canonforge import repository as repo
from canonforge.classifier import CanonClassifier
from canonforge.db import SessionLocal, init_db
from canonforge.domain.models import Claim, Evidence, Source, Work
from canonforge.domain.taxonomy import SourceType

CLASSIFIER = CanonClassifier()

app = typer.Typer(
    name="canonforge",
    help="CanonForge — conhecimento orientado por evidências para universos fictícios.",
    no_args_is_help=True,
)

# Command groups (work add / source add / claim add / evidence add)
work_group = typer.Typer(help="Gerenciar obras (Work).", no_args_is_help=True)
source_group = typer.Typer(help="Gerenciar fontes (Source).", no_args_is_help=True)
claim_group = typer.Typer(help="Gerenciar afirmações (Claim).", no_args_is_help=True)
evidence_group = typer.Typer(help="Gerenciar evidências (Evidence).", no_args_is_help=True)
app.add_typer(work_group, name="work")
app.add_typer(source_group, name="source")
app.add_typer(claim_group, name="claim")
app.add_typer(evidence_group, name="evidence")


@app.command()
def init() -> None:
    """Cria o banco de dados (SQLite) e as tabelas."""
    init_db()
    typer.echo("Banco de dados inicializado.")


@work_group.command("add")
def work_add(
    title: str = typer.Option(..., "--title", help="Título da obra"),
    description: str | None = typer.Option(None, "--description"),
    work_type: str | None = typer.Option(None, "--type", help="anime, manga, novel, game..."),
) -> None:
    """Registra uma obra fictícia (Work)."""
    with SessionLocal() as session:
        work = repo.create_work(
            session, Work(title=title, description=description, work_type=work_type)
        )
        session.commit()
    typer.echo(f"Obra criada: {work.title} [{work.id}]")


@source_group.command("add")
def source_add(
    work_id: UUID = typer.Option(..., "--work-id"),
    title: str = typer.Option(..., "--title"),
    url: str | None = typer.Option(None, "--url"),
    source_type: SourceType = typer.Option(
        SourceType.PRIMARIA, "--type", help="Primária | Complementar | Adaptação | Oficial"
    ),
) -> None:
    """Registra uma fonte (Source) para uma obra."""
    with SessionLocal() as session:
        source = repo.create_source(
            session, Source(work_id=work_id, title=title, url=url, source_type=source_type)
        )
        session.commit()
    typer.echo(f"Fonte criada: {source.title} [{source.id}]")


@claim_group.command("add")
def claim_add(
    work_id: UUID = typer.Option(..., "--work-id"),
    text: str = typer.Option(..., "--text"),
    source_id: UUID = typer.Option(..., "--source-id"),
    location: str | None = typer.Option(None, "--location"),
    is_primary: bool = typer.Option(False, "--is-primary"),
) -> None:
    """Registra uma afirmação (Claim) extraída de uma fonte."""
    with SessionLocal() as session:
        claim = repo.create_claim(
            session,
            Claim(
                work_id=work_id,
                text=text,
                source_id=source_id,
                location=location,
                is_primary_source=is_primary,
            ),
        )
        session.commit()
    typer.echo(f"Afirmação criada: {claim.text} [{claim.id}]")


@evidence_group.command("add")
def evidence_add(
    claim_id: UUID = typer.Option(..., "--claim-id"),
    source_id: UUID = typer.Option(..., "--source-id"),
    content: str = typer.Option(..., "--content"),
    supports: bool = typer.Option(True, "--supports", help="True=sustenta, False=contradiz"),
    location: str | None = typer.Option(None, "--location"),
) -> None:
    """Anexa evidência (Evidence) a uma afirmação."""
    with SessionLocal() as session:
        evidence = repo.create_evidence(
            session,
            Evidence(
                claim_id=claim_id,
                source_id=source_id,
                content=content,
                supports=supports,
                location=location,
            ),
        )
        session.commit()
    typer.echo(f"Evidência criada [{evidence.id}]")


@app.command()
def classify(claim_id: UUID = typer.Option(..., "--claim-id")) -> None:
    """Classifica uma afirmação pela taxonomia canon/fanon."""
    with SessionLocal() as session:
        claim = repo.get_claim(session, claim_id)
        if claim is None:
            raise typer.BadParameter(f"Afirmação {claim_id} não encontrada.")
        evidences = repo.list_evidence(session, claim_id=claim_id)
        sources = repo.list_sources(session, work_id=claim.work_id)
        others = [
            c for c in repo.list_claims(session, work_id=claim.work_id) if c.id != claim_id
        ]
        result = CLASSIFIER.classify(
            claim=claim, evidences=evidences, sources=sources, other_claims=others
        )
    category = f" ({result.status_category.value})" if result.status_category else ""
    typer.echo(f"Status: {result.status.value}{category}")
    typer.echo(f"Confiança: {result.confidence:.2f}")
    typer.echo(f"Justificativa: {result.justification}")
    if result.conflicting_claim_ids:
        ids = ", ".join(str(c) for c in result.conflicting_claim_ids)
        typer.echo(f"Afirmações conflitantes preservadas: {ids}")
    if result.resolution_note:
        typer.echo(f"Resolução: {result.resolution_note}")


def main() -> None:
    app()


if __name__ == "__main__":
    main()
