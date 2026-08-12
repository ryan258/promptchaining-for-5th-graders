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
