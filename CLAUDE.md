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

- Test: `python -m pytest -q`
- Demo verification: `./verify_demos.sh`
- Format: `python -m black .` (if installed)
- Type Check: `python -m mypy .` (if installed)

**Setup:**

1. `python3 -m venv venv`
2. `source venv/bin/activate`
3. `pip install -r requirements.txt`
4. `cp .env.example .env`

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

<!-- gitnexus:start -->
# GitNexus — Code Intelligence

This project is indexed by GitNexus as **promptchaining-for-5th-graders** (545 symbols, 1323 relationships, 43 execution flows). Use the GitNexus MCP tools to understand code, assess impact, and navigate safely.

> If any GitNexus tool warns the index is stale, run `npx gitnexus analyze` in terminal first.

## Always Do

- **MUST run impact analysis before editing any symbol.** Before modifying a function, class, or method, run `gitnexus_impact({target: "symbolName", direction: "upstream"})` and report the blast radius (direct callers, affected processes, risk level) to the user.
- **MUST run `gitnexus_detect_changes()` before committing** to verify your changes only affect expected symbols and execution flows.
- **MUST warn the user** if impact analysis returns HIGH or CRITICAL risk before proceeding with edits.
- When exploring unfamiliar code, use `gitnexus_query({query: "concept"})` to find execution flows instead of grepping. It returns process-grouped results ranked by relevance.
- When you need full context on a specific symbol — callers, callees, which execution flows it participates in — use `gitnexus_context({name: "symbolName"})`.

## When Debugging

1. `gitnexus_query({query: "<error or symptom>"})` — find execution flows related to the issue
2. `gitnexus_context({name: "<suspect function>"})` — see all callers, callees, and process participation
3. `READ gitnexus://repo/promptchaining-for-5th-graders/process/{processName}` — trace the full execution flow step by step
4. For regressions: `gitnexus_detect_changes({scope: "compare", base_ref: "main"})` — see what your branch changed

## When Refactoring

- **Renaming**: MUST use `gitnexus_rename({symbol_name: "old", new_name: "new", dry_run: true})` first. Review the preview — graph edits are safe, text_search edits need manual review. Then run with `dry_run: false`.
- **Extracting/Splitting**: MUST run `gitnexus_context({name: "target"})` to see all incoming/outgoing refs, then `gitnexus_impact({target: "target", direction: "upstream"})` to find all external callers before moving code.
- After any refactor: run `gitnexus_detect_changes({scope: "all"})` to verify only expected files changed.

## Never Do

- NEVER edit a function, class, or method without first running `gitnexus_impact` on it.
- NEVER ignore HIGH or CRITICAL risk warnings from impact analysis.
- NEVER rename symbols with find-and-replace — use `gitnexus_rename` which understands the call graph.
- NEVER commit changes without running `gitnexus_detect_changes()` to check affected scope.

## Tools Quick Reference

| Tool | When to use | Command |
|------|-------------|---------|
| `query` | Find code by concept | `gitnexus_query({query: "auth validation"})` |
| `context` | 360-degree view of one symbol | `gitnexus_context({name: "validateUser"})` |
| `impact` | Blast radius before editing | `gitnexus_impact({target: "X", direction: "upstream"})` |
| `detect_changes` | Pre-commit scope check | `gitnexus_detect_changes({scope: "staged"})` |
| `rename` | Safe multi-file rename | `gitnexus_rename({symbol_name: "old", new_name: "new", dry_run: true})` |
| `cypher` | Custom graph queries | `gitnexus_cypher({query: "MATCH ..."})` |

## Impact Risk Levels

| Depth | Meaning | Action |
|-------|---------|--------|
| d=1 | WILL BREAK — direct callers/importers | MUST update these |
| d=2 | LIKELY AFFECTED — indirect deps | Should test |
| d=3 | MAY NEED TESTING — transitive | Test if critical path |

## Resources

| Resource | Use for |
|----------|---------|
| `gitnexus://repo/promptchaining-for-5th-graders/context` | Codebase overview, check index freshness |
| `gitnexus://repo/promptchaining-for-5th-graders/clusters` | All functional areas |
| `gitnexus://repo/promptchaining-for-5th-graders/processes` | All execution flows |
| `gitnexus://repo/promptchaining-for-5th-graders/process/{name}` | Step-by-step execution trace |

## Self-Check Before Finishing

Before completing any code modification task, verify:
1. `gitnexus_impact` was run for all modified symbols
2. No HIGH/CRITICAL risk warnings were ignored
3. `gitnexus_detect_changes()` confirms changes match expected scope
4. All d=1 (WILL BREAK) dependents were updated

## Keeping the Index Fresh

After committing code changes, the GitNexus index becomes stale. Re-run analyze to update it:

```bash
npx gitnexus analyze
```

If the index previously included embeddings, preserve them by adding `--embeddings`:

```bash
npx gitnexus analyze --embeddings
```

To check whether embeddings exist, inspect `.gitnexus/meta.json` — the `stats.embeddings` field shows the count (0 means no embeddings). **Running analyze without `--embeddings` will delete any previously generated embeddings.**

> Claude Code users: A PostToolUse hook handles this automatically after `git commit` and `git merge`.

## CLI

| Task | Read this skill file |
|------|---------------------|
| Understand architecture / "How does X work?" | `.claude/skills/gitnexus/gitnexus-exploring/SKILL.md` |
| Blast radius / "What breaks if I change X?" | `.claude/skills/gitnexus/gitnexus-impact-analysis/SKILL.md` |
| Trace bugs / "Why is X failing?" | `.claude/skills/gitnexus/gitnexus-debugging/SKILL.md` |
| Rename / extract / split / refactor | `.claude/skills/gitnexus/gitnexus-refactoring/SKILL.md` |
| Tools, resources, schema reference | `.claude/skills/gitnexus/gitnexus-guide/SKILL.md` |
| Index, status, clean, wiki CLI commands | `.claude/skills/gitnexus/gitnexus-cli/SKILL.md` |

<!-- gitnexus:end -->
