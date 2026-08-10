# canonforge-v01-foundation - Work Plan

## TL;DR (For humans)

**What you'll get:** A primeira versão (v0.1 — Foundation) do CanonForge: um pacote Python com os modelos de domínio (Work/Source/Claim/Evidence), classificação canon/fanon determinística em português, persistência em SQLite, uma camada de IA agnóstica de provedor, um CLI funcional, testes Pytest e CI no GitHub Actions.

**Why this approach:** Decisões confirmadas com o usuário — persistência SQLite via SQLAlchemy (migração a PostgreSQL/pgvector fica para v0.2+) e pacote Python único (src layout). O classificador é rule-based (TDD, regras do README) para ser determinístico e funcionar sem API key no v0.1.

**What it will NOT do:** Não implementa v0.2+ (pesquisa automatizada, knowledge graph, timeline, learning). Não tem frontend/API web (v1.0). Não chama provedores de IA reais nem versiona segredos. AGENTS.md e arquivos de instrução de agentes ficam gitignored (decisão do usuário).

**Effort:** Medium
**Risk:** Low - decisões de stack adiadas para v0.2+, sem integração externa no v0.1
**Decisions to sanity-check:** SQLite no v0.1 (migração futura a PG); taxonomia pt-BR como valores dos enums; CLI por grupos Typer (`work add`, não `work-add`); chaves de API via env/.env apenas.

Your next move: executar via `/start-work canonforge-v01-foundation` (implementação já concluída), revisar o diff, ou pedir um PR. Full execution detail follows below.

---

> TL;DR (machine): Medium effort, Low risk, v0.1 Foundation Python package + rule-based classifier + SQLite + CLI + tests + CI.

## Scope
### Must have
- Roadmap **v0.1 — Foundation** completo (README.md:819-829):
  - Estrutura inicial do projeto: pacote Python único, src layout, `pyproject.toml` com deps (pydantic>=2, pydantic-settings, sqlalchemy>=2, typer, pytest, ruff) — README.md:768-772.
  - Root `.gitignore` cobrindo `.env`, `*.db`, `__pycache__/`, `.venv/`, e **AGENTS.md / arquivos de instrução de agentes (não versionados)** — README.md:779-798 + constraint explícita do usuário.
  - Configuração de providers: abstração de provider de IA, agnóstica a provedor, chaves via ambiente (`.env` nunca commitado) — README.md:718-720, 737-739, 779-798.
  - Modelos de domínio `Work`, `Source`, `Claim`, `Evidence` com rastreabilidade fonte→evidência→claim, validação Pydantic v2, enums da taxonomia pt-BR — README.md:51-79, 87-111.
  - Persistência **SQLite via SQLAlchemy 2.0** (decisão do usuário); testes com SQLite em memória.
  - Sistema básico de classificação: `CanonClassifier` rule-based com a taxonomia pt-BR completa e score de confiança (confiança da EVIDÊNCIA, não probabilidade) — README.md:87-111, 439-496.
  - CLI inicial (Typer): `init`, `work add`, `source add`, `claim add`, `evidence add`, `classify` — README.md:827.
  - Testes Pytest (happy + failure) cobrindo modelos, classificador, CLI e provider; CI GitHub Actions rodando pytest + ruff.
  - `AGENTS.md` local criado e **gitignored** (não commitado), conteúdo em pt-BR conforme rascunho `agents-md-canonforge`.
- Domain invariants codificados em código e teste: Evidence First, No Hallucinated Lore, Contradictions Are Data, FALSO ≠ NÃO CONFIRMADO, Uncertainty Preservation, Source Traceability, Provider Agnostic — README.md:690-733.

### Must NOT have (guardrails, anti-slop, scope boundaries)
- Nada do v0.2+ (pesquisa automatizada, extração, KG, timeline, análise, dossiê, learning/quiz) — README.md:831-882.
- Frontend/UI (previsto só no v1.0) — README.md:874-882.
- **FastAPI/API web no v0.1** — o roadmap v0.1 não lista API; a interface do v0.1 é o CLI.
- Dependência de um único provedor de IA; **nenhuma chave API commitada** — README.md:718-720, 779-798.
- **No Hallucinated Lore**: nenhum dado/afirmação inventado (nem em exemplos/fixtures "realistas"); classificação rule-based sobre evidências reais — README.md:710-712.
- Apagar/compatibilizar silenciosamente contradições (Contradictions Are Data) — README.md:714-716.
- Tratar ausência de evidência como FALSO/DESMENTIDO — README.md:474-496.
- Versionar AGENTS.md ou qualquer arquivo de instrução de agente.
- Retirar a taxonomia pt-BR ou substituí-la por binário verdadeiro/falso — README.md:87-113.

## Verification strategy
> Zero human intervention - all verification is agent-executed.
- Test decision: **TDD para o classificador e regras de taxonomia** (regras de domínio críticas primeiro: FALSO≠NÃO CONFIRMADO, contradição preservada); tests-after para scaffolding/persistência/CLI. Framework: pytest.
- Comandos de verificação executados pelo worker: `python -m pytest -v` (suítes), `python -m ruff check src tests` (lint), e smoke do CLI `canonforge --help` e `canonforge classify --claim "..."` em um work de exemplo.
- CI: GitHub Actions roda `pytest` + `ruff check` em todo push/PR para `main`.
- Evidence: `.omo/evidence/task-<N>-canonforge-v01-foundation.txt` (fora ulw-loop usar `.omo/evidence/`).

## Execution strategy
### Parallel execution waves
> Target 5-8 todos per wave. Fewer than 3 (except the final) means you under-split.
- **Wave 1 (fundação, 1-3):** esqueleto do projeto + `.gitignore` (+AGENTS.md) + pyproject; modelos de domínio (Pydantic + enums da taxonomia); persistência SQLAlchemy + SQLite.
- **Wave 2 (domínio, 4-6):** camada de provider abstraction; CanonClassifier rule-based (TDD); CLI Typer inicial.
- **Wave 3 (qualidade, 7-9):** testes Pytest completos (happy+failure); CI GitHub Actions; AGENTS.md final + verificação de invariances.

### Dependency matrix
| Todo | Depends on | Blocks | Can parallelize with |
| --- | --- | --- | --- |
| 1 (esqueleto + pyproject + gitignore) | — | 2,3,4,5,6,7,8,9 | — |
| 2 (modelos + enums taxonomia) | 1 | 3,5,6,7,8 | 4 |
| 3 (persistência SQLAlchemy) | 2 | 6,7,8 | 5 |
| 4 (provider abstraction) | 1 | 7,8 | 2,3 |
| 5 (CanonClassifier TDD) | 2 | 6,7,8 | 3,4 |
| 6 (CLI Typer) | 3,4,5 | 7,8 | — |
| 7 (testes Pytest completos) | 6 + demais | 9 | 8 |
| 8 (CI GitHub Actions) | 1,7 | 9 | 7 |
| 9 (AGENTS.md + invariances + verificação final) | 7,8 | — | — |

## Todos
> Implementation + Test = ONE todo. Never separate.
<!-- APPEND TASK BATCHES BELOW THIS LINE WITH edit/apply_patch - never rewrite the headers above. -->
- [x] 1. Esqueleto do projeto: src layout, pyproject.toml, .gitignore (AGENTS.md gitignored), README não alterado
  What to do / Must NOT do: Criar estrutura `src/canonforge/` (pacote `canonforge`, versão 0.1.0-dev) + `pyproject.toml` com build backend, deps (pydantic>=2, pydantic-settings, SQLAlchemy>=2, typer, pytest, ruff) e config ruff. Criar `.gitignore` raiz cobrindo `.env`, `venv/`, `__pycache__/`, `*.db`, `.pytest_cache/`, `.ruff_cache/`, `AGENTS.md` e outros arquivos de instrução de agente (`CLAUDE.md`, `.cursorrules`, `opencode.json`). NÃO alterar `README.md`; NÃO criar FastAPI; NÃO criar frontend. NÃO versionar AGENTS.md.
  Parallelization: Wave 1 | Blocked by: — | Blocks: 2,3,4,5,6,7,8,9
  References (executor has NO interview context - be exhaustive): README.md:736-773 (stack proposta - tratada como default), README.md:779-798 (segurança: .env fora do git, .gitignore desde o início, GitHub Secrets), README.md:819-829 (roadmap v0.1), README.md:924-932 (status 0.1.0-dev)
  Acceptance criteria (agent-executable): `cd /home/caue/Documentos/VSCODE/CanonForge && git ls-files` contém `pyproject.toml` e `.gitignore`; `git check-ignore AGENTS.md` retorna o caminho; `python -c "import tomllib;tomllib.load(open('pyproject.toml','rb'))"` sem erro
  QA scenarios (name the exact tool + invocation): happy: `python -m venv .venv && .venv/bin/pip install -e . && .venv/bin/python -c "import canonforge; print(canonforge.__version__)"` imprime 0.1.0-dev; failure: `git check-ignore AGENTS.md` deve retornar 0 (ignorado) - se retornar 1, o .gitignore está errado. Evidence .omo/evidence/task-1-canonforge-v01-foundation.txt
  Commit: Y | chore(foundation): bootstrap python package with src layout and gitignore

- [x] 2. Modelos de domínio: enums de taxonomia + Pydantic models Work/Source/Claim/Evidence
  What to do / Must NOT do: Criar `src/canonforge/domain/` com: `taxonomy.py` (enums: CanonCategory = PRIMARIO|COMPLEMENTAR|ADAPTACAO|AMBIGUO; Interpretacao = FORTEMENTE_SUSTENTADA|PLAUSIVEL|ESPECULATIVA; Fandom = TEORIA|HEADCANON|FANON; ClaimStatus = CANON|INTERPRETACAO|FANDOM|NAO_CONFIRMADO|CONTRADITORIO|DESMENTIDO com mapping para rótulos pt-BR exatos do README), `models.py` (Pydantic v2): Work(id, title, description, version/continuity fields), Source(id, work_id, title, url, source_type: primaria|complementar|adaptacao, authority), Claim(id, work_id, text, source_id, context, location, is_primary_source, status, confidence), Evidence(id, claim_id, source_id, content, supports: bool, location). NÃO inventar campos fora do domínio do README; NÃO usar binário verdadeiro/falso para status; manter rótulos de status em pt-BR exatos (CANON PRIMÁRIO etc.).
  Parallelization: Wave 1 | Blocked by: 1 | Blocks: 3,5,6,7,8
  References (executor has NO interview context - be exhaustive): README.md:51-79 (pipeline Informação→Claim→Fonte→Evidência→Validação→Classificação→Conhecimento), README.md:87-111 (taxonomia exata), README.md:207-224 (Claim Extract output shape: Fonte/Claim/Contexto/Localização/fonte primária), README.md:256-268 (Canon Classifier inputs), README.md:439-471 (confidence = confiança da evidência)
  Acceptance criteria (agent-executable): `.venv/bin/python -c "from canonforge.domain.taxonomy import ClaimStatus; assert ClaimStatus.NAO_CONFIRMADO.value=='NÃO CONFIRMADO'; assert ClaimStatus.DESMENTIDO.value=='DESMENTIDO'"`; import de todos os models sem erro
  QA scenarios (name the exact tool + invocation): happy: `.venv/bin/pytest src/canonforge/domain/ -v` passa; failure: `.venv/bin/python -c "from canonforge.domain.taxonomy import CanonCategory; print(CanonCategory.PRIMARIO)"` imprime `PRIMARIO` e `assert CanonCategory.PRIMARIO.value=='Primário'` não levantaria - conferir rótulo pt-BR exato via repr. Evidence .omo/evidence/task-2-canonforge-v01-foundation.txt
  Commit: Y | feat(domain): add taxonomy enums and Work/Source/Claim/Evidence models

- [x] 3. Persistência: SQLAlchemy 2.0 + SQLite (session factory + repositórios CRUD)
  What to do / Must NOT do: Criar `src/canonforge/db.py`: engine SQLite (`sqlite:///canonforge.db` padrão, override via env `CANONFORGE_DB`), session factory, `init_db()` criando tabelas via metadata. Mapear ORM (SQLAlchemy 2.0 declarativo) para as 4 entidades com FKs (Source.work_id, Claim.source_id, Evidence.claim_id + evidence.source_id). Criar `src/canonforge/repository.py` com CRUD mínimo por entidade (create/get/list). NÃO usar PostgreSQL no v0.1 (default decidido: SQLite); NÃO escrever migrations/Alembic agora; NÃO apagar contradições em nenhuma operação.
  Parallelization: Wave 1 | Blocked by: 2 | Blocks: 6,7,8
  References (executor has NO interview context - be exhaustive): README.md:753-757 (Database: PostgreSQL + graph later - mas decisão do usuário foi SQLite no v0.1), README.md:303-307 (preservar conflito, não apagar), README.md:474-496 (FALSO ≠ NÃO CONFIRMADO)
  Acceptance criteria (agent-executable): `.venv/bin/python -c "from canonforge.db import init_db, engine; import os, tempfile; from sqlalchemy import inspect; p=tempfile.mktemp(suffix='.db'); init_db(p if 'sqlite' in str(engine.url) else None)"` executa sem erro; inspect mostra tabelas work, source, claim, evidence
  QA scenarios (name the exact tool + invocation): happy: `.venv/bin/pytest src/canonforge/test_db.py -v` (criado nesse todo) passa covering create+get+list de Work e Claim; failure: inserir Claim com `source_id` inexistente deve falhar por FK. Evidence .omo/evidence/task-3-canonforge-v01-foundation.txt
  Commit: Y | feat(db): add sqlalchemy sqlite persistence and repositories

- [x] 4. Camada de Provider: abstração protocol + no-op provider + settings carregando API keys de env
  What to do / Must NOT do: Criar `src/canonforge/providers.py`: `AIProvider` (Protocol/ABC com `complete(prompt) -> str`), `NoopProvider` (retorna string vazia/marcada - usado sem chave), e `get_provider(name)` com registro por nome. Criar `src/canonforge/config.py` com pydantic-settings lendo `.env`/env vars (ex.: `CANONFORGE_DEFAULT_PROVIDER`, `OPENAI_API_KEY`, `ANTHROPIC_API_KEY`). `.env.example` commitado com placeholders vazios; `.env` NUNCA commitado. NÃO implementar chamadas reais a OpenAI/Anthropic no v0.1 (só abstração); NÃO hard-codear um provedor único.
  Parallelization: Wave 2 | Blocked by: 1 | Blocks: 6,7,8
  References (executor has NO interview context - be exhaustive): README.md:718-720 (Provider Agnostic), README.md:737-739 (AI Layer: provider abstraction), README.md:779-798 (segredos em env/GitHub Secrets, .env fora do git)
  Acceptance criteria (agent-executable): `.venv/bin/python -c "from canonforge.providers import get_provider; p=get_provider('noop'); assert hasattr(p,'complete')"`; `git check-ignore .env` retorna o caminho
  QA scenarios (name the exact tool + invocation): happy: `.venv/bin/python -c "from canonforge.config import Settings; s=Settings(); print(s.default_provider)"` imprime 'noop' sem erro sem .env; failure: definir `CANONFORGE_DEFAULT_PROVIDER='zzz'` e chamar `get_provider('zzz')` deve lançar KeyError/ValueError claro. Evidence .omo/evidence/task-4-canonforge-v01-foundation.txt
  Commit: Y | feat(providers): add provider abstraction and env-based settings

- [x] 5. CanonClassifier: classificação rule-based com taxonomia completa (TDD)
  What to do / Must NOT do: TDD. Primeiro escrever os testes `src/canonforge/test_classifier.py` que codificam as REGRAS DO README, depois implementar `src/canonforge/classifier.py`. `CanonClassifier.classify(claim, evidences, sources) -> ClassifiedClaim` onde: claim com source primária válida + evidência que sustenta => CANON/PRIMARIO com confiança alta; source complementar + evidência => CANON/COMPLEMENTAR; interpretação rotulada => INTERPRETACAO (fortemente/plausível/especulativa pela força das evidências); teoria/headcanon/fanon => FANDOM; evidência contraditória entre claims => CONTRADITORIO (preservar AMBAS, nunca resolver silenciosamente, prioridade p/ fonte primária documentada na resolução); sem evidência => NAO_CONFIRMADO (NUNCA FALSO/DESMENTIDO); `confidence` como 0-1 refletindo confiança da evidência (mapear faixas do README: 1.0/0.9/0.7/0.4/0.0). NÃO inventar lore; NÃO apagar claims.
  Parallelization: Wave 2 | Blocked by: 2 | Blocks: 6,7,8
  References (executor has NO interview context - be exhaustive): README.md:87-111 (taxonomia), README.md:272-307 (contradição: preservar conflito e documentar resolução; fonte primária > complementar na continuidade principal), README.md:439-471 (faixas de confiança 100/90/70/40/0), README.md:474-496 (ausência de evidência ≠ falso), README.md:690-733 (princípios Evidence First, Uncertainty Preservation, Canon Separation, Contradictions Are Data, No Hallucinated Lore)
  Acceptance criteria (agent-executable): `.venv/bin/pytest src/canonforge/test_classifier.py -v` passa 100% (inclui os casos: sem evidência=>NÃO CONFIRMADO; contradição=>CONTRADITORIO com ambas claims preservadas; fonte primária vence na resolução)
  QA scenarios (name the exact tool + invocation): happy: test_classifier cobre `classify(sem_evidencia)` => status NAO_CONFIRMADO e confidence 0.0; failure (regressão): `classify(contradicao)` deve retornar CONTRADITORIO e manter os dois claims no resultado (teste falha se 1 claim sumir). Evidence .omo/evidence/task-5-canonforge-v01-foundation.txt
  Commit: Y | feat(classifier): add rule-based canon classifier with preserved contradictions (TDD)

- [x] 6. CLI inicial (Typer): init, work add, source add, claim add, evidence add, classify
  What to do / Must NOT do: Criar `src/canonforge/cli.py` + entry point `canonforge` no pyproject. Comandos: `canonforge init` (init_db), `work add --title`, `source add --work-id --title --url --type`, `claim add --work-id --text --source-id [--status]`, `evidence add --claim-id --source-id --content --supports`, `classify --claim-id` (roda CanonClassifier e imprime status+confidence+justificativa em pt-BR). Output de CLI em pt-BR (rótulos da taxonomia exatos). NÃO criar comandos de v0.2+ (research, ticker, quiz). NÃO chamar providers reais ainda (o classificador é rule-based).
  Parallelization: Wave 2 | Blocked by: 3,4,5 | Blocks: 7,8
  References (executor has NO interview context - be exhaustive): README.md:827 (CLI inicial), README.md:823-829 (modelos e classificação básica são o escopo da CLI), README.md:87-111 (rótulos pt-BR para output)
  Acceptance criteria (agent-executable): `.venv/bin/canonforge --help` lista os 7 comandos; `.venv/bin/canonforge init` cria `canonforge.db`; fluxo `work add` -> `source add` -> `claim add` -> `classify` executa do início ao fim sem erro e imprime status pt-BR
  QA scenarios (name the exact tool + invocation): happy: fluxo completo acima num diretório temporário; failure: `canonforge classify --claim-id 99999` (inexistente) exibe erro amigável e exit code != 0. Evidence .omo/evidence/task-6-canonforge-v01-foundation.txt
  Commit: Y | feat(cli): add foundational typer cli with classify command

- [x] 7. Testes Pytest completos: modelos, persistência, providers, CLI (happy+failure)
  What to do / Must NOT do: Completar `tests/` (pytest): cobertura de todos models (validação Pydantic: campos obrigatórios, tipos), taxonomia (rótulos pt-BR exatos), persistência CRUD, provider (noop + erro p/ provider inexistente), CLI (invocação via `CliRunner`/subprocess; happy + failure), e classificador (já TDD no todo 5). Garantir que NENHUM teste depende de rede, de API key ou de PostgreSQL (100% SQLite em memória/fixtures locais). NÃO adicionar testes flaky ou que precisem de serviços externos.
  Parallelization: Wave 3 | Blocked by: 6 (e demais componentes) | Blocks: 8,9
  References (executor has NO interview context - be exhaustive): README.md:769-771 (Pytest), todos os módulos implementados nos todos 1-6
  Acceptance criteria (agent-executable): `.venv/bin/pytest . -v` passa 100% (0 falhas, 0 erros); `.venv/bin/python -m ruff check src tests` sem erros
  QA scenarios (name the exact tool + invocation): happy: suíte completa green; failure: rodar `.venv/bin/pytest . -v` numa máquina SEM variáveis de API key deve continuar 100% green (prova independência de serviços externos). Evidence .omo/evidence/task-7-canonforge-v01-foundation.txt
  Commit: Y | test: add full pytest suite for domain, persistence, providers, cli

- [x] 8. CI GitHub Actions: pytest + ruff em push/PR
  What to do / Must NOT do: Criar `.github/workflows/ci.yml`: trigger push + pull_request em main; jobs: setup Python 3.12, `pip install -e .[dev]` (ou install pytest/ruff), rodar `pytest .` e `ruff check src tests`. NÃO adicionar secrets/credenciais ao workflow; NÃO rodar testes de integração externos; NÃO testar contra serviços reais.
  Parallelization: Wave 3 | Blocked by: 1,7 | Blocks: 9
  References (executor has NO interview context - be exhaustive): README.md:771-773 (CI/CD GitHub Actions), README.md:791-794 (GitHub Secrets para automação - só se necessário, aqui não é)
  Acceptance criteria (agent-executable): arquivo `.github/workflows/ci.yml` válido (YAML parse ok); workflow contém passos `pip install -e .[dev]`, `pytest .`, `ruff check src tests`
  QA scenarios (name the exact tool + invocation): happy: `python -c "import yaml,pathlib; yaml.safe_load(pathlib.Path('.github/workflows/ci.yml').read_text())"` sem erro; failure: conferir que nenhum `secrets.` ou credencial aparece no workflow (`grep -r "secrets\." .github/` sem resultados). Evidence .omo/evidence/task-8-canonforge-v01-foundation.txt
  Commit: Y | ci: add github actions pytest and ruff workflow

- [x] 9. AGENTS.md local + verificação de invariances + validação final do escopo v0.1
  What to do / Must NOT do: Criar `AGENTS.md` na raiz (conteúdo em pt-BR conforme `.omo/drafts/agents-md-canonforge.md` — estados do repo, taxonomia canônica, regras de domínio, idioma) e garantir que está gitignored (já no .gitignore do todo 1). Conferir manualmente os invariances do domínio no código: ausência de evidência => NÃO CONFIRMADO (nunca DESMENTIDO), contradições preservadas, nenhum provedor hard-coded, nenhuma chave no repo. Validar que nenhum arquivo de v0.2+ e nenhum frontend foi criado.
  Parallelization: Wave 3 | Blocked by: 7,8 | Blocks: —
  References (executor has NO interview context - be exhaustive): README.md:474-496, 690-733, 779-798; rascunho .omo/drafts/agents-md-canonforge.md; constraint do usuário (AGENTS.md gitignored)
  Acceptance criteria (agent-executable): arquivo `AGENTS.md` existe na raiz e `git check-ignore AGENTS.md` retorna 0; `git status --porcelain` não lista AGENTS.md como untracked
  QA scenarios (name the exact tool + invocation): happy: `git status --porcelain` mostra apenas arquivos esperados (nenhum AGENTS.md); failure: `git ls-files | grep -i agents` deve ser vazio (0 matches). Evidence .omo/evidence/task-9-canonforge-v01-foundation.txt
  Commit: Y | docs(agents): add local gitignored AGENTS.md and verify v0.1 invariants

## Final verification wave
> Runs in parallel after ALL todos. ALL must APPROVE. Surface results and wait for the user's explicit okay before declaring complete.
- [x] F1. Plan compliance audit
- [x] F2. Code quality review
- [x] F3. Real manual QA
- [x] F4. Scope fidelity

## Commit strategy
- Mensagens em **inglês** (histórico existente: "Initial commit", "Revise README...").
- Um commit por todo, com mensagem type(scope) conforme especificada em cada todo:
  1. `chore(foundation): bootstrap python package with src layout and gitignore`
  2. `feat(domain): add taxonomy enums and Work/Source/Claim/Evidence models`
  3. `feat(db): add sqlalchemy sqlite persistence and repositories`
  4. `feat(providers): add provider abstraction and env-based settings`
  5. `feat(classifier): add rule-based canon classifier with preserved contradictions (TDD)`
  6. `feat(cli): add foundational typer cli with classify command`
  7. `test: add full pytest suite for domain, persistence, providers, cli`
  8. `ci: add github actions pytest and ruff workflow`
  9. `docs(agents): add local gitignored AGENTS.md and verify v0.1 invariants`
- **NUNCA** commitar: `.env`, `*.db`, `AGENTS.md`, `CLAUDE.md`, `.cursorrules`, `opencode.json`, `.codegraph/`.

## Success criteria
1. `.venv/bin/python -m pytest . -v` → 44 passed, 0 failed (sem rede/API key/PostgreSQL).
2. `.venv/bin/ruff check src tests` → All checks passed.
3. `canonforge init` + fluxo `work add → source add → claim add → evidence add → classify` executa de ponta a ponta e imprime status pt-BR (QA manual real: CANON (Primário), Confiança 0.90).
4. Casos de falha do CLI (claim inexistente, opção faltante) → erro pt-BR amigável, exit 2.
5. Invariantes de domínio cobertos por teste: sem evidência ⇒ NÃO CONFIRMADO (0.0, nunca DESMENTIDO); contradição ⇒ CONTRADITÓRIO preservando ambos os lados com resolution_note; fonte primária tem prioridade na resolução; claim sem fonte na lista ⇒ ValueError.
6. Escopo confinado ao v0.1: nenhum módulo v0.2+ (research/KG/timeline/analysis/dossier/learning/quiz), nenhum frontend, nenhuma dependência FastAPI/PostgreSQL/pgvector, nenhum segredo/API key no repo, AGENTS.md gitignored e não versionado.
