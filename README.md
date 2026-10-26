# Prompt Chaining Studio

**A personal thinking workbench. Big ideas, small useful steps.**

Turn a question, rough thought, or stuck point into a sequence you can follow. Each answer becomes material for the next step. Keep the useful result, inspect how it was made, and come back without starting over.

The app runs locally with Python, FastAPI, Jinja2 and HTMX. It keeps the original portable prompt chaining framework, local ChromaDB artifact mirror, and OpenRouter integration. It needs no frontend build system or container.

**Use the [documentation suite](docs/README.md)** for recipe selection, stronger inputs, complete walkthroughs, custom chains, accessible daily use, setup, backups and troubleshooting. See [ROADMAP.md](ROADMAP.md) for the phased direction and deferred scope. For one practical starting point, read [Getting the most out of it](docs/GETTING-THE-MOST-OUT-OF-IT.md).

The same documentation is available inside the app under **Guides**, with full-text search, section links and copyable examples. Use **Alt/Option+G** outside text fields to open it. Contextual help beside your work opens a guide in another tab.

## Start here

Use Python 3.11 or newer. From this folder:

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
./pc
```

Open **http://127.0.0.1:8000**. Choose **Walk through an example** to inspect a complete authored chain about the Moon. It makes no model calls and needs no API key. The interface and its HTMX script are served locally; fonts use the system's installed fallbacks.

If you already have `venv/`, the launcher can use it. The launcher works from another directory and starts one server on loopback. `./start_app.sh` is an alias for the same command. On platforms without Bash, activate the virtual environment and run `python -m tools.studio start`.

## The whole workflow

1. **Choose a recipe.** Make it click, Connect two ideas, Think a decision through, From thought to draft, Untangle a problem, or Build a learning path.
2. **Give it a direction.** Enter or dictate a topic. Adjust the audience and context. Open any step to edit the prompt, add a step, or reorder the method. Recipes have 1–8 steps.
3. **Keep the method.** Save your recipe and starting inputs. Each save creates a new copy, preserving the previous one. Browser drafts also recover changes while editing.
4. **Prepare a chain.** This saves a run and opens its first prompt for review. Preparing sends no requests.
5. **Run at your pace.** Review each step, or run the chain through. Each answer saves before another request begins. You can edit the latest answer of a paused run; the original answer is retained. Request a pause whenever you need one.
6. **Take the result with you.** Copy the final answer, export the chain as Markdown or JSON, or explicitly save the final answer to the existing artifacts library.
7. **Come back.** The workbench offers unfinished work first. Your library finds runs by topic, recipe or status. Back up the workspace and restore it without replacing existing records.

## Live generation

Keep your existing `.env` file. If you do not have one, copy `.env.example` to `.env`, then set:

```dotenv
OPENROUTER_API_KEY="your-key"
OPENROUTER_MODELS="your-chosen-model-id"
MAX_TOKENS=2000
REQUEST_TIMEOUT_SECONDS=30
```

Restart the app after changing settings. Comma-separated model IDs become choices in the recipe editor. Provider wiring stays in `lib/core/llm_client.py`; feature modules do not choose hardcoded models.

A live run sends its topic, audience, context and referenced previous answers to OpenRouter and the chosen provider. **Provider charges apply.** The new workbench dispatches each step once, without automatic retry. An explicit retry can incur another charge, especially after an ambiguous timeout or abrupt stop. `MAX_TOKENS` bounds output length per request; it is not an account spending cap. Advanced tools also send each step once; errors require another explicit action. Their executions remain separate from resumable workbench runs.

The settings indicator means a key is configured; it does not verify provider access, model availability or account credit. A chain can also carry mistakes forward. Review factual claims before using the result. Model-generated critiques and comparisons are not fact-checks.

## Small commands, less setup

| Command | What it does |
| --- | --- |
| `./pc` | Start the local app on port 8000 |
| `./pc start --port 8010` | Use another local port |
| `./pc doctor` | Check local dependencies and configuration; no API requests |
| `./pc backup` | Write a timestamped Studio ZIP archive under `backups/` |
| `./pc backup /path/to/copy.json` | Write a small legacy JSON backup; refuses oversized or existing files |
| `./pc restore /path/to/copy.json` | Add records from Studio ZIP or JSON; never starts a chain |
| `Ctrl+C` | Finish and save the current workbench request, pause, then stop |

An optional shell alias, defined once with this repo's absolute path, makes startup shorter:

```bash
alias pc='/absolute/path/to/promptchaining-for-5th-graders/pc'
```

The UI supports system dictation, visible keyboard focus, a skip link, reduced motion and labelled controls. `Alt+N` opens recipes; `Alt+L` opens the library. In the editor, `Ctrl/Cmd+S` saves the recipe and `Ctrl/Cmd+Enter` prepares a run. On a ready or paused run, `Ctrl/Cmd+Enter` dispatches its next action. Browser or operating-system shortcuts may take precedence.

## Saves, interruptions and backup

- Runs and recipes live in `workspace/studio.sqlite3` by default. Set `PROMPT_STUDIO_DATA` to choose another directory. SQLite transactions protect checkpoints. One server owns the workspace runtime lock, so another process cannot recover an active run or dispatch overlapping work.
- A run is a snapshot of its recipe. Editing a recipe later does not change old runs. A stale tab cannot dispatch the same step twice.
- Leaving a page keeps the server working. A normal shutdown lets the current request finish and pauses. An abrupt stop marks unfinished work interrupted at the next startup. Completed steps survive; the unfinished request is never retried automatically.
- Workspace ZIP archives and legacy JSON backups contain saved recipes, inputs, prompt traces, answers and run progress. Restore validates the complete file before writing, skips identical records, and gives colliding records new IDs. Imported running work becomes interrupted.
- JSON parts accept up to 10 MB and 2,000 recipes/runs each. The default ZIP archive splits larger workspaces into validated parts, up to 128 parts, 128 MB compressed and 256 MB expanded. Backup creation refuses files outside these restore limits. Browser drafts, `.env`, old artifacts and log files are outside workspace backups. Keep the separate `artifacts/` and `logs/` folders if you need those records. Workspace text can contain private material you entered; treat backups accordingly.
- Browser draft recovery belongs to that browser and origin. Save a recipe or prepare a run to include it in computer-level backups. If browser storage is unavailable, the editor says so and keeps explicit save available.

## The portable framework

The original Python API and advanced UI remain available. **Advanced** links to learning tools, reasoning and adversarial patterns, meta-chain design, and the existing artifact library. These legacy flows use their original execution paths, without the new workbench's resume guarantees.

```python
from lib.core.chain import MinimalChainable
from lib.core.llm_client import get_model, prompt

outputs, filled_prompts, usage = MinimalChainable.run(
    context={"topic": "fractions"},
    model=get_model(),
    llm_callable=prompt,
    prompts=[
        "Break {{topic}} into its essential pieces.",
        "Using {{output[-1]}}, give a concrete example.",
    ],
    return_usage=True,
)
```

`lib/core/` also provides `FusionChain`, `ArtifactStore`, `ChainComposer` and `MetaChainGenerator`. `lib/enhancements/` holds natural reasoning, adversarial reasoning and model-based comparisons. Chroma mirrors framework artifacts locally using deterministic hash vectors; these vectors are not semantic embeddings. JSON files remain the artifact source of truth.

## Check the work

Use the focused offline acceptance group for this implementation:

```bash
.venv/bin/python -m pytest -q tests/test_harmony.py tests/test_workbench.py tests/test_workbench_routes.py tests/test_guides.py tests/test_llm_client.py tests/test_server_routes.py
```

Tests substitute model responses and temporary storage. They do not spend provider credits. See [docs/TESTING.md](docs/TESTING.md) for the verification boundary and commands for the broader framework suite. Browser and live-provider acceptance are separate from Python tests.

The architecture and recovery details are in [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md). Existing demos are documented in [docs/DEMOS.md](docs/DEMOS.md); some demos call providers. Exploratory ideas and historical release notes describe earlier work and are not a current feature inventory.
