# Workbench status — October 24, 2026

The repository now opens as a local personal thinking workbench. Its complete path is recipe → intention → saved run → reviewed steps → reusable output. The original framework remains available through Advanced.

## Implemented

- Six editable starter recipes, a blank-chain editor, and a four-step authored Moon walkthrough requiring no model requests.
- Browser draft recovery, explicit computer-level recipe saves, saved starting topic/context and review pace, 1–8 steps, keyboard shortcuts, dictation-friendly fields and undo for a removed step.
- Ready runs that preview their first request, explicit live starts, review between steps or continuous execution, pause, saved prompt traces, output edits with original-answer retention, and reported token counts.
- SQLite checkpoints, stale-tab protection, one active run, one runtime owner, graceful shutdown and abrupt-stop recovery. Failed/interrupted calls require an explicit retry.
- Searchable run library, reuse, final-answer copy, Markdown/JSON exports, additive JSON backup/restore, stable deduplication of colliding imports, and an explicit handoff into the original JSON/Chroma artifact library.
- A loopback-only launcher, local assets, system font fallbacks, escaped output, same-origin write checks, reduced motion and visible focus.
- `./pc`, `./pc doctor`, `./pc backup` and `./pc restore FILE`. Dependencies installed in the ignored project `.venv`. The original `.env` was preserved.

## Local verification

The focused group covering workbench behavior, HTML routes, shared LLM configuration, legacy routes and artifact persistence passed **54 checks**. Final workbench refinements, including workspace configuration load order and saved review pace, also passed all tests. The launcher relocation passed its specific backup writer regression. Next phases and scope boundaries are tracked in [ROADMAP.md](../ROADMAP.md).

The real launcher was exercised from another working directory using a temporary workspace: loopback page serving, the local HTMX asset, authored-example creation and graceful shutdown passed. A separate CLI backup/restore round trip preserved the complete saved run, and the backup writer refused to overwrite an existing file. Temporary workspace data was removed.

`./pc doctor`, JavaScript syntax, launcher shell syntax and `git diff --check` passed. Verification used Python 3.12.14, FastAPI 0.162.0 and ChromaDB 1.5.9. The Chroma artifact test used a temporary local collection, supplied deterministic vectors and made no embedding downloads. Provider calls in tests were replaced with deterministic callables.

## Acceptance boundary

Ryan chose local checks only. No browser pass, live model request, full framework suite, screen-reader acceptance or voice-control acceptance was performed. Existing model choices were read from configuration; their availability, quality and account credit were not tested. The interface is ready for Ryan's own review, without claiming that review has happened.

Workspace JSON restore is bounded to 10 MB and 2,000 recipes/runs each. Browser drafts, `.env`, old artifacts and log files are outside workspace backups. Generated answers and model critiques still require human judgment and factual review.

No staging, commits, pushes, deployment or publication were performed. Existing artifacts and owner configuration were preserved.

## Resume

Run `./pc` from the repository and open `http://127.0.0.1:8000`. Start with the authored example, or open Recipes and prepare a chain. Preparation saves locally; the next page previews the prompt and provides the explicit live start.

See [README.md](../README.md) for daily use and [TESTING.md](TESTING.md) for the optional broader acceptance commands.
