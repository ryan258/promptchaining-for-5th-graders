# Architecture

The project has one local Python server and a portable library. The main experience is a saved thinking workbench. Earlier framework tools remain available under Advanced.

## The main path

```text
Jinja editor → validated recipe and intention → ready run in SQLite
                                                 ↓ explicit Start
                                           background worker
                                                 ↓
                               render prompt → one provider request
                                                 ↓
                                     transactional checkpoint
                                                 ↓
                              pause for review / continue / complete
```

`server/main.py` creates the FastAPI app, mounts local static assets, installs the loopback host/origin boundary and owns lifecycle shutdown. `server/workbench.py` adapts forms to library operations. It holds no provider execution loop or persistence implementation. Templates use ordinary forms for saves, starts, pauses, edits and restores; HTMX polls only running status. Small vanilla JavaScript adds browser drafts, step editing, shortcuts, copy fallback and announcements.

## Reusable workbench modules

| File | Responsibility |
| --- | --- |
| `lib/workbench/models.py` | Bounded typed recipes, run snapshots, results and versioned backups |
| `lib/workbench/recipes.py` | Editable starter and take-home recipes, plus the authored Moon walkthrough |
| `lib/workbench/store.py` | SQLite transactions, revision checks, claims, recovery and additive restore |
| `lib/workbench/runner.py` | Prompt reference validation, single-request steps, checkpoints, pause, output review and Markdown export |
| `tools/studio.py` | Local startup, configuration checks, atomic backup files and restore |
| `lib/core/llm_client.py` | Shared environment/model configuration and provider client; `prompt_once` and the compatible `prompt` name both send one request |

Recipes contain 1–8 named steps. Inputs have explicit length limits. Templates accept `topic`, `audience`, `context`, earlier outputs, and optional top-level JSON fields on earlier outputs. Invalid/forward references fail before dispatch. Substitution visits the original template once; placeholder-shaped text in user inputs or model answers is not reinterpreted.

## Ownership and execution

A platform file lock permits one workbench runner to own a workspace. This lock is held until its thread pool closes and released by the OS if the process dies. A second server fails startup instead of marking another server's live run interrupted. The database is still available to read-only backups and transactional additive imports.

The worker pool has one thread. A SQLite write transaction checks for any running chain and claims the requested run, using a page revision to reject stale actions. This prevents overlapping work and double dispatch across tabs. Reading a page, preparing a run, exporting, restoring or opening the example never calls a provider.

`prompt_once` performs one request with the SDK's retries disabled at client construction. A failure stops the run and keeps prior answers. The framework also makes one callable invocation per step, without automatic transport or JSON-format retries. Advanced operations do not acquire the workbench runtime claim and do not gain its resumable-run contract.

At each successful response, the worker saves the sent prompt, answer, reported usage, and duration in one checkpoint. With review enabled, it then pauses. If the response reaches the output limit, the saved answer is flagged and the run pauses before sending that partial answer forward. An explicit output edit preserves the original model answer and changes what the next step receives. Finished runs remain available for inspection and reuse.

## State and recovery

```text
ready ──Start──> running ──checkpoint──> paused ──Continue──> running
                    │                                        │
                    ├──last checkpoint──> completed          │
                    ├──request/validation error──> failed ──Retry
                    └──abrupt stop──> interrupted ──────────Retry
```

Every saved answer commits before another request begins. Pause finishes the dispatched request and stops at the next checkpoint. Normal shutdown requests pause, waits for the worker and releases its runtime lock. On startup, the new lock owner marks saved `running` records interrupted. It never automatically repeats unfinished work.

A process can die after a provider accepts a request and before its answer is committed. The interruption and timeout messages explain how to check the provider before retrying. If the worker has the answer and cannot commit it, it holds the checkpoint in memory and attempts an atomic private recovery file. A retry of that local save can recover the answer and pause the run without dispatching another model request.

## Persistence and portability

`workspace/studio.sqlite3` is the default workspace. SQLite uses WAL, a busy timeout and full synchronous commits. Connections close after each transaction. `PROMPT_STUDIO_DATA` can move the workspace to another absolute directory. Relative paths resolve from the server's working directory; prefer absolute paths for portable commands.

Workspace backup reads recipes and runs in a single database transaction. JSON uses format `prompt-chaining-studio`, version 1. Restore validates the entire document and its prompt references before opening a write transaction. Each JSON part rejects unknown fields, invalid states, invalid IDs, more than 2,000 recipes/runs and files over 10 MB. Default workspace downloads and CLI backups use a ZIP manifest with SHA-256 checksums and importable JSON parts. Archives accept at most 128 parts, 128 MB compressed and 256 MB expanded; creation enforces these limits too. Restore validates every part and prompt reference before a single transaction adds records. ZIP members are read in memory and never extracted to filesystem paths. Identical records are skipped, collisions get fresh IDs, and imported running work becomes interrupted. It does not dispatch, replace, delete or merge into existing runs.

The launcher does not rewrite `.env`, install packages automatically, spawn a browser, kill process groups, or create Git commits. `./pc backup` writes a temporary file, fsyncs it and publishes a new filename atomically; it refuses to overwrite existing backups.

Browser drafts live in localStorage, scoped to browser and origin. They recover unsaved editor fields and step lists. Explicit save also persists starting topic/context, avoiding a retyping round trip after saving a recipe. Workspace backups exclude browser storage and credentials. Legacy JSON export refuses an oversized file and directs the user to ZIP. Prompt text and output may contain private material supplied by the user.

## Existing framework

`lib/core/chain.py` provides `MinimalChainable` and `FusionChain`. `artifact_store.py` persists framework artifacts as JSON and mirrors them to local Chroma. The deterministic hash vectors are not semantic embeddings. `chain_composer.py` composes steps and tools. `meta_chain_generator.py` asks a model to propose a chain. `lib/enhancements/` contains reasoning, adversarial and model-comparison helpers.

The main workbench uses a separate checkpoint executor because the older synchronous chain API has no resume contract. This keeps old demos and library signatures intact. Both paths share provider wiring, configuration and the `{{output[-1]}}` vocabulary. Completed workbench answers enter the old artifact system only through an explicit Save final to artifacts action, with a run-specific key to avoid replacing older work.

## Local boundary and interface

The launcher binds to `127.0.0.1`. Trusted hosts and same-origin checks cover legacy and workbench endpoints. The `testserver` host is also permitted for in-process route tests. Cross-origin browser mutations are rejected. Outputs render as escaped text; prompt content is never executable Jinja or JavaScript. Provider exceptions are reduced to helpful messages without echoing raw response bodies or keys.

HTMX is vendored with its license. It cannot evaluate scripts or issue cross-origin requests. The interface uses local system fonts, the palette in `server/static/candlelight.css`, reduced-motion rules, visible focus and text-labelled controls. It does not add accounts, containers, a frontend build chain or hosted infrastructure.

## In-app guides

`server/guides.py` exposes the read-only `/studio/guides` library, search, individual pages and Markdown downloads. It delegates to `lib/workbench/guides.py`, which reads an explicit catalog of documentation files from this checkout. Guide bodies remain in Markdown; the app does not maintain a second content copy or a search database.

The library uses `markdown-it-py` with raw HTML disabled. It rewrites known documentation links to app routes, adds stable section anchors, and renders copyable code blocks and keyboard-scrollable tables. Images do not load remote resources automatically. Unknown file links and unsafe URL schemes are not rendered as clickable file access. File access is catalog-only, bounded in size, and rejects source-path symlink substitutions.

Search scans current installed guides and ranks matching sections. Earlier notes remain available from their catalog group. Files are reread on request so a guide refresh reflects saved documentation changes. Contextual guide links open another tab to preserve the current workflow.

## Advanced execution and evidence

`lib/advanced.py` contains provider/tool operations and bounded payload validation without importing an app entrypoint. API and HTML routes call it through Starlette's worker pool so synchronous providers and subprocesses do not block workbench requests. Setup is inside the protected execution path. Safe errors expose application-authored instructions and exception types rather than raw provider bodies or subprocess diagnostics.

Depth and rounds are integers from 1 to 5. Meta-design execution accepts 1–8 prompts; the portable sequential chain accepts 1–32. The shared provider client has SDK retries disabled and both public prompt helpers make one attempt. The chain engine never repeats a call to repair JSON. One-pass template rendering prevents inserted context or answers from becoming new template instructions; four braces quote a literal placeholder for prompt-design lessons.

Artifact JSON files publish through a temporary file, fsync and atomic replacement. Per-instance writes serialize; FusionChain uses separate run/model namespaces. Metadata sidecars have content digests so stale provenance is ignored after an interrupted metadata write. An unreadable artifact is reported through `load_warnings` and skipped without changing its source file. Atomic per-file writes are not a transaction across an entire legacy chain or its metadata sidecars.

Composer accounting resets for every composition and returns independent step traces. Tools that do not return usage mark the total as an incomplete known subtotal. Cost is unknown until explicitly estimated from configured token prices; logs and the cost report do not claim provider billing totals.

Model comparisons stop after a failed phase, validate all ten scores as finite numbers from 1 to 10, exclude failed comparisons from win/tie rates, and disclose the 2,000-character excerpt limit. They summarize model preferences and perform no statistical significance test. Scientific and root-cause prompts distinguish supplied observations from generated hypotheses; content drafts require verification of factual claims and label illustrative examples.
