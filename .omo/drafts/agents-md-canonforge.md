---
slug: agents-md-canonforge
status: awaiting-approval
intent: clear
review_required: false
pending-action: write .omo/plans/agents-md-canonforge.md
approach: Deliver a decision-complete work plan whose single implementation todo writes AGENTS.md at the repo root with the exact content specified in the plan (pt-BR, compact, evidence-first guidance for future agent sessions).
---

# Draft: agents-md-canonforge

## Components (topology ledger)
| id | outcome (one line) | status | evidence path |
|---|---|---|---|
| AGENTS.md | New root instruction file, pt-BR, 5 short sections, no unverifiable claims | active | repo root (tracked only README.md today: `git ls-files`) |

## Open assumptions (announced defaults)
| assumption | adopted default | rationale | reversible? |
|---|---|---|---|
| Language of AGENTS.md | Portuguese (pt-BR) | User confirmed via question; README and repo description are pt-BR | yes — trivial to translate later |
| Commit messages | English | Existing history uses English ("Initial commit", "Revise README...") — noted in the file so agents don't guess | yes |
| No reviewer gate needed | High-accuracy dual review NOT required | Explicit plan-mode doc task, single-file scope, no code, nothing irreversible; `review_required: false` | n/a |

## Findings (cited - path:lines)
- The only tracked file is `README.md` (`git ls-files` → `README.md`). No package.json, no tests, no CI, no lint config, no root `.gitignore`, no other config anywhere in the tree (glob over `*.{json,jsonc,toml,yaml,yml,lock}` → none; `**/*` → README + git/codegraph internals only).
- README.md is a 932-line project proposal in Brazilian Portuguese: status "🟡 Concepção / Arquitetura", version 0.1.0-dev (README.md:924-932).
- The stack listed in "Stack Inicial" (React/Next.js, Python/FastAPI, PostgreSQL, pgvector, Pydantic, Pytest, GitHub Actions) is explicitly a *possibility*: "A stack definitiva ainda será definida durante a implementação." (README.md:736-738, 775). It is NOT decided — an agent must not treat it as locked.
- Canon taxonomy is specified in Portuguese: CANON (Primário, Complementar, Adaptação, Ambíguo), INTERPRETAÇÃO (Fortemente sustentada, Plausível, Especulativa), FANDOM (Teoria, Headcanon, Fanon), plus NÃO CONFIRMADO / CONTRADITÓRIO / DESMENTIDO (README.md:87-111).
- Named modules/agents in English: Researcher, Claim Extractor, Evidence Engine, Validator, Canon Classifier, Contradiction Detector, Knowledge Graph, Timeline Engine, Analysis Engine, Dossier Engine, Learning Engine (README.md:180-307, 309-386, 528-560, 562-613).
- Canonical pipeline order: Input→Identify→Discover→Collect→Extract Claims→Trace Origins→Gather Evidence→Validate→Classify→Detect Contradictions→Build KG→Build Timeline→Analyze→Generate Dossier (README.md:644-684).
- 10 development principles incl. Evidence First, No Hallucinated Lore, Contradictions Are Data, Provider Agnostic, Uncertainty Preservation (README.md:690-733).
- Security: API keys never in repo; `.env` out of git; GitHub Secrets for automation; a `.gitignore` is mandated "desde o início" but does NOT exist at root today (README.md:779-798 vs tree scan).
- Git: branch `main`, remote `https://github.com/MikuBR/CanonForge.git` (.git/config:6-11), 2 commits both English (git log), clean working tree (git status --porcelain → nothing).
- `.codegraph/` exists locally with its own `.gitignore` (`*` except itself) — machine-local, not tracked, no agent action needed.

## Decisions (with rationale)
1. **Deliverable = plan, not direct edit.** Environment enforces plan-only writes (`.omo/*.md`) for this session; the AGENTS.md content is therefore embedded verbatim in the plan and executed by a worker via `/start-work`.
2. **Content is fully specified in the plan.** The executor gets ZERO judgment calls: exact file path, exact section headers, exact bullets. All content derived from verified README facts; nothing speculative.
3. **Keep the file compact and repo-specific.** Follows "every line must answer: would an agent miss this?" — excluded generic advice, excluded the full taxonomy/pipeline prose (pointed at README instead), excluded exhaustive file trees.
4. **Language split documented:** AGENTS.md body in pt-BR (matches README); commits in English (matches history).

## Scope IN
- Create `/home/caue/Documentos/VSCODE/CanonForge/AGENTS.md` with the exact content given in the plan's todo.

## Scope OUT (Must NOT have)
- No root `.gitignore` creation (README mandates one, but creating it is a separate change — not requested).
- No edits to README.md, no new config files, no code scaffolding.
- No LICENSE, no CI, no CONTRIBUTING.
- No extra sections beyond the plan's specified content (no essay, no file tree, no generic agent advice).
- No `.omo/` files committed or touched by the worker beyond the plan itself.

## Open questions
- None. (Language fork already answered by the user: pt-BR.)

## Approval gate
status: awaiting-approval
- Approach: one implementation todo that writes AGENTS.md (exact content inline in the plan), one final-verification todo verifying the file matches the spec byte-for-byte and that every claim traces to README.md.
- Next workflow action: on approval, run the scaffold without `--draft-only`, APPEND the todo batches, fill the TL;DR last, and hand off for `/start-work`.
- If the user declines: revise the draft's specified content and re-present once.
