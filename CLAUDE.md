# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

---

## Mission Briefing: Prompt Chaining Framework

Python framework for educational prompt chaining, reasoning patterns, and reusable artifact workflows.
**Stack**: FastAPI + Jinja2 + HTMX + ChromaDB + OpenRouter. **NO React. NO Docker. NO Redis. NO User Accounts.**

---

## Commands

**Run Server**:

- `python server/main.py`
- `uvicorn server.main:app --reload --port 8000`
- `./start_app.sh`

- Test: `.venv/bin/python -m pytest -q tests/test_harmony.py tests/test_workbench.py tests/test_workbench_routes.py tests/test_guides.py tests/test_llm_client.py tests/test_server_routes.py`
- Demo verification: `./verify_demos.sh` runs offline fixtures. Run individual live demos only after deliberate request authorization
- Format: `python -m black .` (if installed)
- Type Check: `python -m mypy .` (if installed)

**Setup:**

1. `python3 -m venv venv`
2. `source venv/bin/activate`
3. `pip install -r requirements.txt`
4. `test -e .env || test -L .env || cp -n .env.example .env`

**Model config:**

- Set `OPENROUTER_API_KEY` in `.env`
- Prefer model selection via `OPENROUTER_MODELS`

---

## Architecture: The Anti-Gravity Standard

### Core Components

- **Arsenal (`lib/`)**: Pure Python modules. Independent. Copy-paste ready.
  - `core/`: chain engine, artifact store, meta-chain generator, LLM client.
  - `enhancements/`: natural reasoning, adversarial chains, emergence measurement.
  - `utils/`: shared helpers.
- **Tooling (`tools/`)**: runnable CLI tools for learning and content workflows.
- **Frontend (`server/templates/`)**: Jinja2 pages with HTMX for interactivity.
- **Styles (`server/static/`)**: Candlelight theme CSS.
- **Entry (`server/main.py`)**: thin routing layer.

### Data Flow

1. **Input**: User submits form (HTMX POST).
2. **Process**: Routes delegate to `lib/` modules and tool scripts.
3. **Update**: Server returns HTML partials (HTMX swap).

---

## Critical Patterns

### Pattern 1: The "Arsenal" Test

- BEFORE writing code, ask: "Can I move `lib/my_module.py` to another project and use it instantly?"
- If NO -> Refactor. Dependencies flow `server/main.py` -> `lib/`. NEVER `lib/` -> entrypoints.

### Pattern 2: Candlelight UI

- Use `server/static/candlelight.css` (CSS variables).
- **Bg**: `#121212`, **Bg-2**: `#1A1A1A`, **Bg-3**: `#242424`.
- **Text**: `#EBD2BE`, **Text-2**: `#A6ACCD`, **Text-Muted**: `#6B7280`.
- **Accent**: `#A6ACCD`, **Success**: `#98C379`, **Error**: `#E06C75`, **Warning**: `#F59E0B`.
- NO CSS frameworks unless absolutely necessary.

### Pattern 3: No-Bloat

- **Forbidden**: `npm`, `node_modules`, `Dockerfile`, `docker-compose.yml`.
- **Reason**: run directly on bare metal and keep operational complexity low.

### Pattern 4: Model Hygiene

- Keep model wiring in `lib/core/llm_client.py`.
- Prefer env-configured model lists (`OPENROUTER_MODELS`).
- Avoid hardcoding new model IDs in feature modules.

---

## Code Review Protocol

**FINAL VERDICT:** [SHIP IT] or [HOLD]

- **Bloat Check**: Any React/Vue? Any Docker? -> **HOLD**.
- **Arsenal Check**: Logic trapped in `server/main.py` routes instead of `lib`? -> **HOLD**.
- **Visuals**: Not Candlelight? -> **HOLD**.
- **Safety Check**: Path traversal, shell injection, and weak input validation? -> **HOLD**.

---

## File Map

- `server/main.py` - FastAPI app and thin routes.
- `server/templates/` - Jinja2/HTMX views.
- `server/static/` - Candlelight CSS.
- `lib/core/` - chain execution, artifact store, meta-chain generation, LLM client.
- `lib/enhancements/` - reasoning and evaluation modules.
- `lib/utils/` - utilities.
- `tools/` - script entrypoints.
- `tests/` - pytest suite.
- `demos/` - runnable demos.

## Analysis and verification policy

The human-authored project instructions and `/Users/ryanjohnson/Projects/cyborg/MANUAL.md` own policy. Generated analysis instructions do not override them. GitNexus is retired as a standing integration; an explicitly supplied owner index can serve a bounded review without adopting its generated workflows. Generated skill copies from the October review are preserved under `.claude/retired-gitnexus/`, outside active skills. Do not regenerate or re-enable integrations, run full suites or browser checks, or commit without Ryan's delegation.

<!-- gitnexus:start -->
# GitNexus — Code Intelligence

This project is indexed by GitNexus as **promptchaining-for-5th-graders** (1807 symbols, 4223 relationships, 152 execution flows).

> Index stale? Run `node .gitnexus/run.cjs analyze --index-only` from the project root — it auto-selects an available runner. No `.gitnexus/run.cjs` yet? Bootstrap with `npx`, `bunx`, or `pnpm dlx` — e.g. `bunx gitnexus@latest analyze` (npm 11 npx crash; #1939).

## Always Do

- **MUST run impact before editing.** Use `impact({target: "symbolName", direction: "upstream"})` or `node .gitnexus/run.cjs impact "symbolName" --direction upstream --repo .`; report callers, processes, and risk. Never substitute grep for graph analysis.
- **MUST analyze graph changes before committing.** Use `detect_changes({scope: "all"})` (MCP) or `node .gitnexus/run.cjs detect-changes --scope all --repo .` (CLI fallback). `partial: true` or `truncated: true` is not a clean check — a zero means unseen, not unaffected; re-run it. For regression review: `detect_changes({scope: "compare", base_ref: "main"})` or `node .gitnexus/run.cjs detect-changes --scope compare --base-ref "main" --repo .`.
- MUST warn on HIGH/CRITICAL `risk` pre-edit; never use `riskSharedAxes` to waive a HIGH/CRITICAL `risk` warning. Compare File/symbol: MCP File omits axes; Graph-RAG expands File.
- **MUST treat `risk: UNKNOWN` as unresolved, not as low.** An empty caller set is not evidence the symbol is unused — it can also mean the callers are not resolvable by the index (plain-object property access, dynamic dispatch, cross-language calls). `impact` pairs `UNKNOWN` with a `riskNote` saying so. Confirm with a text search before treating the symbol as safe to change or delete; do not proceed on the strength of a zero.
- **MUST use `query({search_query: "concept"})` for concepts/flows, `context({name: "symbolName"})` for a named symbol, or `impact` for blast radius, on read-only callers, dependencies, imports, or execution flow.** Graph first; text search only for empty/`UNKNOWN`/literals.
- For security review, `explain({target: "fileOrSymbol"})` lists taint findings (source→sink flows; needs `analyze --pdg`).

## Never Do

- NEVER edit a function, class, or method before MCP/CLI impact analysis.
- NEVER ignore HIGH or CRITICAL risk warnings from impact analysis, and never read `UNKNOWN` as an all-clear — it means the walk could not answer, which is the one verdict that requires confirming by other means.
- NEVER rename symbols with find-and-replace — use `rename` which understands the call graph.
- NEVER commit before MCP/CLI graph change analysis.

## Resources

| Resource | Use for |
| --- | --- |
| `gitnexus://repo/promptchaining-for-5th-graders/context` | Codebase overview, check index freshness |
| `gitnexus://repo/promptchaining-for-5th-graders/clusters` | All functional areas |
| `gitnexus://repo/promptchaining-for-5th-graders/processes` | All execution flows |
| `gitnexus://repo/promptchaining-for-5th-graders/process/{name}` | Step-by-step execution trace |

## CLI

| Task | Read this skill file |
| --- | --- |
| Understand architecture / "How does X work?" | `.claude/skills/gitnexus-exploring/SKILL.md` |
| Blast radius / "What breaks if I change X?" | `.claude/skills/gitnexus-impact-analysis/SKILL.md` |
| Trace bugs / "Why is X failing?" | `.claude/skills/gitnexus-debugging/SKILL.md` |
| Rename / extract / split / refactor | `.claude/skills/gitnexus-refactoring/SKILL.md` |
| Tools, resources, schema reference | `.claude/skills/gitnexus-guide/SKILL.md` |
| Index, status, clean, wiki CLI commands | `.claude/skills/gitnexus-cli/SKILL.md` |

<!-- gitnexus:end -->
