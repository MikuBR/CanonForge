---
slug: canonforge-v01-foundation
status: approved
intent: clear
review_required: false
pending-action: write .omo/plans/canonforge-v01-foundation.md
approach: Plan the FIRST version (roadmap v0.1 — Foundation) of CanonForge: initial project structure, provider configuration, core models (Work/Source/Claim/Evidence), basic classification, and initial CLI. Constraint from user: AGENTS.md or similar agent-instruction files must be .gitignore'd (NOT committed). User confirmed forks: SQLite via SQLAlchemy; single Python package (src layout).
---

# Draft: canonforge-v01-foundation

## Components (topology ledger)
| id | outcome (one line) | status | evidence path |
|---|---|---|---|
| Monorepo/project skeleton | Initial repo structure + root .gitignore (incl. AGENTS.md + .env) + tooling config | active | README.md:819-821 ("Estrutura inicial do projeto"); README.md:779-798 (security/.gitignore mandate) |
| Core domain models | Work, Source, Claim, Evidence data models with traceability + classification fields | active | README.md:823-829; README.md:59-73; README.md:87-111 (taxonomy) |
| Canon classification system | Basic classifier implementing the pt-BR taxonomy (CANON/INTERPRETAÇÃO/FANDOM/NÃO CONFIRMADO/CONTRADITÓRIO/DESMENTIDO) | active | README.md:87-111; README.md:256-268 |
| Provider abstraction | AI provider-agnostic layer (config + provider interface) per "Provider Agnostic" principle | active | README.md:737-739; README.md:718-720 |
| Initial CLI | CLI for foundation workflows (init work, add source/claim, classify) | active | README.md:827 ("CLI inicial") |
| AGENTS.md handling | AGENTS.md + similar agent instruction files listed in .gitignore, NOT tracked | active | user constraint (this session) |

## Open assumptions (announced defaults)
| assumption | adopted default | rationale | reversible? |
|---|---|---|---|
| Scope = roadmap v0.1 only | v0.2+ (research pipeline, KG, learning) explicitly OUT | User: "planejamento da primeira versão com base no roadmap" → v0.1 Foundation per README.md:819-829 | yes |
| Backend-first foundation | v0.1 is backend/CLI/models; no frontend until v1.0 (README.md:875) | Roadmap places web UI in v1.0, README.md:874-882 | yes |
| Proposed stack honored as starting point | Python/FastAPI + Pydantic + Pytest + PostgreSQL/pgvector + GitHub Actions (README.md:736-773) with provider abstraction | README says "possibilidade" but it is the only stated direction; plan treats it as default unless user overrides | yes |
| Docs language pt-BR | New docs/comments in Brazilian Portuguese | README and repo description are pt-BR | yes |
| Commit messages English | git history uses English | .git/logs confirmed | yes |
| Agent-instruction files not committed | AGENTS.md etc. in .gitignore | Explicit user constraint this session | yes |

## Findings (cited - path:lines)
- Repo has only `README.md` tracked (git ls-files). No code, no .gitignore, no CI, no package manifests (glob `*.{json,...}` → none).
- Status: "🟡 Concepção / Arquitetura", v0.1.0-dev (README.md:924-932).
- Stack explicitly tentative: "A stack definitiva ainda será definida durante a implementação." (README.md:738).
- v0.1 Foundation roadmap: estrutura inicial, configuração de providers, modelos Work/Source/Claim/Evidence, sistema básico de classificação, CLI inicial (README.md:819-829).
- Core principle: claim must carry traceable evidence (README.md:51-79); taxonomy in pt (README.md:87-111); Contradictions Are Data (README.md:710-716); absence-of-evidence ≠ false (README.md:474-496); No Hallucinated Lore (README.md:710-712); Provider Agnostic (README.md:718-720); .env out of git + GitHub Secrets (README.md:779-798).
- 10 dev principles to encode as repo invariants (README.md:690-733).
- Remote: github.com/MikuBR/CanonForge, main branch, 2 English commits (git log).

## Decisions (with rationale)
1. Plan v0.1 Foundation (first version) per roadmap — supersedes the earlier AGENTS.md-only plan (agents-md-canonforge draft): that deliverable is folded in as the "AGENTS.md handling" component with the user's new constraint (gitignored).
2. AGENTS.md (and similar agent-instruction files) go into .gitignore and are NOT committed — user constraint; handled by adding the root .gitignore that the README already mandates.
3. Deliverable is a decision-complete plan; environment restricts this session to .omo/ plan writes, so implementation runs via /start-work.
4. TODO: /hyperplan adversarial planning via team-mode requires team_* tools — verify availability; if missing, instruct user to enable team mode.

## Scope IN
- Roadmap v0.1 Foundation: project skeleton, provider config, Work/Source/Claim/Evidence models, basic classifier, initial CLI.
- Root .gitignore including AGENTS.md, .env, and standard Python/Node excludes.
- AGENTS.md created locally but gitignored (content as drafted in agents-md-canonforge draft).
- Backend/test/CI foundation scaffolding (Pytest + GitHub Actions).

## Scope OUT (Must NOT have)
- v0.2+ pipelines (research, extraction, evidence gathering, KG, timeline, analysis, dossiê, learning, quiz).
- Frontend/web UI (v1.0).
- Any AI provider hard-coding / single-provider coupling; provider abstraction only.
- Fetching/processing any real fictional work content as part of this plan.
- No committed AGENTS.md or other agent-instruction files.

## Open questions
- None blocking. Owner-forks answered by user: persistence = SQLite via SQLAlchemy; repo layout = single Python package (src layout).

## Approval gate
status: approved
- Approach: single decision-complete .omo/plans/canonforge-v01-foundation.md writable by /start-work.
- Follow-up user replies resolved the two owner-decision forks with the recommended defaults: SQLite via SQLAlchemy, single Python package (src layout).
- Next workflow action: scaffold the plan (no --draft-only), mandatory Metis gap analysis, APPEND todo batches, fill TL;DR last, then deliver with the start-or-high-accuracy question.
- If user declines: adjust scope/brief and re-present once.
