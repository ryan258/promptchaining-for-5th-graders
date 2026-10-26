# Roadmap: Prompt Chaining Studio

A production-quality, local, single-user thinking and learning workbench for Ryan that turns intentions into structured prompt chains, preserves work and decisions locally without bloat, and makes resumption effortless.

---

## §0 Big Goal

Build and maintain a distraction-free, bare-metal thinking environment where complex thoughts, multi-step reasoning, and learning workflows are turned into inspectable, step-by-step chains. Every step is transparent, checkpoints survive interruptions, and output can be reused or exported without cloud lock-in or container overhead.

---

## §1 Implemented Foundation

The workbench implementation runs on local Python; acceptance is recorded separately in [Workbench status](docs/WORKBENCH-STATUS.md):

- **Core Workbench Engine (`lib/workbench/`)**:
  - Typed models (`models.py`), curated recipe templates (`recipes.py`), step runner with pause/retry mechanics (`runner.py`), and SQLite WAL transactional persistence with runtime locking (`store.py`).
  - Zero-credential authored Moon walkthrough for immediate offline exploration.
  - 6 initial recipes: *Make it click*, *Connect two ideas*, *Think a decision through*, *From thought to draft*, *Untangle a problem*, and *Build a learning path*.
  - Strict step-by-step execution: each answer is committed before the next request starts. No silent retries.

- **FastAPI + Jinja2 + HTMX Interface (`server/`)**:
  - Full Candlelight theme compliance (`server/static/candlelight.css`).
  - Locally vendored HTMX (`server/static/vendor/htmx-1.9.12.min.js`); no CDN script tags or frontend build pipelines.
  - Accessibility-first design: skip links, visible keyboard focus, system font fallbacks, ARIA live regions, and reduced-motion support.
  - Security hardening: bound to loopback `127.0.0.1`, `TrustedHostMiddleware`, strict same-origin mutation checks, and HTML escaping.

- **Developer Tooling & CLI (`./pc`)**:
  - Standalone bash entry point `./pc` wrapping `tools/studio.py`.
  - Commands: `./pc` (start), `./pc doctor` (zero-network diagnostic), `./pc backup` (atomic ZIP archive with validated JSON parts), `./pc restore` (lossless, non-destructive import).
  - Aliased by `./start_app.sh`.

- **Preserved Core Framework (`lib/core/`, `lib/enhancements/`)**:
  - Public entrypoints retained for `MinimalChainable`, `FusionChain`, `ArtifactStore`, `ChainComposer`, and `MetaChainGenerator`.
  - Legacy tools, reasoning patterns, adversarial debates, and artifact viewers remain accessible via the `/studio/advanced` route.

- **Deterministic Quality Gates**:
  - Focused offline checks cover the workbench, Guides and repaired framework paths. Current commands and evidence are recorded in [Testing](docs/TESTING.md) and [Workbench status](docs/WORKBENCH-STATUS.md).

---

## §2 Small Phased Path (Next Horizons)

Focused, small iterations guided by observed usage rather than speculation:

- **Phase 1: Personal Ergonomics & Dictation Tuning**
  - Observe real-world friction in voice dictation input across long prompts.
  - Refine keyboard navigation flows (`Ctrl/Cmd+Enter`, `Alt+N`, `Alt+L`) based on active usage.

- **Phase 2: Recipe Management & Library Tagging**
  - Allow user-authored recipes to be tagged and filtered within **My library**.
  - Provide lightweight search by recipe tags or topic keywords.

- **Phase 3: Direct Vault / Markdown Export Integrations**
  - Streamline one-click copying and formatting into local Markdown notes or Obsidian vault folders.
  - Support exporting full chain traces with prompt/response metadata in standard frontmatter.

- **Phase 4: Selective Model Routing**
  - Enable per-step model selection in custom recipes (e.g., fast model for drafting, reasoning model for critique) via `.env` configured aliases.

---

## §3 Return Point & Deferred Ideas

### Return Point
The local workbench and Guides are implemented. The harmony repair addresses the reviewed execution, persistence, request-control, prompt-handoff and reporting defects. Full-suite compatibility, browser behavior, assistive-technology acceptance and real-provider operation remain owner acceptance gates. A passing local group does not establish those outcomes.

### Deferred Scope (The Anti-Bloat Law)
Explicitly deferred to keep the system simple, fast, and durable:
- ❌ **No multi-user authentication / user accounts / JWT**: Single-user local tool.
- ❌ **No Docker / Kubernetes / containers**: Runs directly on bare-metal Python.
- ❌ **No Node.js / React / Vue build chains**: Jinja2 + HTMX + Vanilla CSS.
- ❌ **No cloud database services / hosted backends**: Local SQLite WAL database.
- ❌ **No automatic background retries**: User maintains total visibility and control over provider costs.

---

## §4 Focused Quality Gates

Before any changes are committed or released:

1. **Targeted Tests**:
   ```bash
   .venv/bin/python -m pytest -q tests/test_harmony.py tests/test_workbench.py tests/test_workbench_routes.py tests/test_guides.py tests/test_llm_client.py tests/test_server_routes.py
   ```
2. **Setup Diagnostic**:
   ```bash
   ./pc doctor
   ```
3. **Backup & Restore Validation**:
   - Verify the default ZIP backup restores beyond the old JSON size and record limits.
   - Verify `./pc restore` refuses to overwrite existing runs.
4. **Owner acceptance**:
   - Full suite, browser/assistive checks, provider checks and Git publication remain separate owner actions.

## Review backlog after correctness repairs

Optional enhancements remain future work: preserve form values during validation errors; search/favorite saved recipes; dismiss abandoned runs; remember the configured model when reusing a method; retain a short next-step note; warn about another tab replacing an unsaved draft; query lightweight library summaries; provide an authored example for each recipe; and add a tested dependency constraints snapshot. Checkpoint forks, richer Markdown exports, vault integration and per-step models should follow demonstrated use. These are not part of the completed correctness repairs and add no account, hosting or commercial-platform requirement.
