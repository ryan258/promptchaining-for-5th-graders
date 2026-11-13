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
  - 6 initial general recipes, plus dedicated suites for kids, parents/caregivers, and teachers.
  - Offline Chain Lab (`lib/workbench/chain_lab.py`): prompt builder with human answers, starter missions, beginner token attachments (`[Goal]`, `[Clues]`, `[Answer N]`), and remixing.
  - Classroom challenges and dragon prompt-building case (`lib/workbench/classroom_cases.py`) with prepared handoff comparisons.
  - Strict step-by-step execution: each answer is committed before the next request starts. No silent retries.
  - A durable per-attempt claim governs pause and shutdown. A failed checkpoint can be retried as a local save.
  - Resume notes, archived runs, and checkpoint forks preserve the context for returning to work.
  - Three offline professional practice cases with editable handoffs, source packets, rubrics, and separate final and trace exports.

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
  - Test the final-answer and trace Markdown exports against a real handoff.
  - Use that experience to choose an optional local vault destination and frontmatter fields.

- **Phase 4: Selective Model Routing**
  - Enable per-step model selection in custom recipes (e.g., fast model for drafting, reasoning model for critique) via `.env` configured aliases.

---

## §3 Return Point & Deferred Ideas

### Return Point
Start with one of the [professional cases](docs/PROFESSIONAL-CASES.md) and correct the second handoff. Inspect the trace and use the final answer as a handoff. Full-suite compatibility, browser behavior, assistive-technology acceptance and real-provider operation remain owner acceptance gates.

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
   .venv/bin/python -m pytest -q tests/test_local_request_boundary.py tests/test_harmony.py tests/test_workbench.py tests/test_workbench_routes.py tests/test_guides.py tests/test_llm_client.py tests/test_server_routes.py
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

Use the three professional cases to test whether the exported deliverables are useful and how often you return to a saved method. Candidate follow-ups include favorites or tags for saved recipes, additional authored examples for the six starter methods, a configured vault destination, and per-step model choices. Evaluate model comparisons on the same source packet and output rubric before making claims about quality.
