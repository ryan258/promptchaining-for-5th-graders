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

Open **http://127.0.0.1:8000**. Choose **Explore the Moon example** to inspect a complete authored chain about the Moon. It makes no model calls and needs no API key. The interface and its HTMX script are served locally; fonts use the system's installed fallbacks.

Choose **Try a classroom challenge** to solve a rainy recess problem, track down a missing mascot, or plan a paper bridge. Read the clues, fix one mistake in a sample answer, and see your change in the next instruction. The challenges run offline. [Classroom walkthrough](docs/DEMOS.md#try-it-with-a-class)

Choose **Build the next prompt** under **Keep exploring** to sneak a dragon through the library. Pick a map note or spoken directions, see how your choice and the route go into the last prompt, then compare the two prepared answers. The challenge works offline. [Dragon challenge walkthrough](docs/DEMOS.md#build-the-next-prompt)

Choose **Build your own chain** from Home to open Chain Lab. Start with a mission or write your own two-to-five-step chain. Pick what each step can read, have a partner answer the prompt, and remix one handoff to see what changes. Chain Lab saves each answer locally and works offline. [Chain Lab walkthrough](docs/DEMOS.md#build-your-own-chain-in-chain-lab)

Choose **Make something to show at home** for a family game, a four-panel comic, or a paper invention. Each offline challenge gives you a project to try with a parent or caregiver. Use the matching editable recipe if you want live AI to help shape an idea of your own. [Take-home projects](docs/DEMOS.md#make-something-to-show-at-home)

On Home, choose a chain under **Parents and caregivers** or open **All parent recipes** to sort school notices, plan the family week, get dinner unstuck, or draft a school note. Dictate or paste what you have, then check each answer before it goes into the next step. You can run the chain in Studio or copy the starter into the AI chat you already use. [Parent recipe guide](docs/RECIPE-GUIDE.md#for-parents-and-caregivers)

On Home, choose a chain under **Teachers** or open **All teacher recipes** to plan a lesson, adapt an activity, draft feedback from an anonymous excerpt, or use exit tickets to plan what to teach next. Start with a few notes or a fictional example. Review each answer in Studio or copy the starter into the AI chat you already use. [Teacher recipe guide](docs/RECIPE-GUIDE.md#for-teachers)

Each group on Home has ten more chains for finding a useful surprise. Kids can **Try a discovery mission** in the offline Chain Lab. Parents can **Find a better way at home** by investigating a recurring snag. Teachers can **Look closer at student learning** by checking what classroom evidence actually shows. [Discovery missions](docs/DEMOS.md#try-a-discovery-mission) · [Parent and teacher insight chains](docs/RECIPE-GUIDE.md#find-an-insight-you-can-use)

For a decision memo, evidence brief, or document review, open the practice cases for adults. Each case includes a source packet, a rubric, and a reference answer. [Professional practice cases](docs/PROFESSIONAL-CASES.md)

If you already have `venv/`, the launcher can use it. The launcher works from another directory and starts one server on loopback. `./start_app.sh` is an alias for the same command. On platforms without Bash, activate the virtual environment and run `python -m tools.studio start`.

## The whole workflow

1. **Choose a recipe.** Pick a method that fits what you want to learn, decide, write, or make. [Recipe guide](docs/RECIPE-GUIDE.md)
2. **Give it a direction.** Enter or dictate a topic. Adjust the audience and context. Open any step to edit the prompt, add a step, or reorder the method. Recipes have 1–8 steps.
3. **Keep the method.** Save your recipe and starting inputs. Each save creates a new copy, preserving the previous one. Browser drafts also recover changes while editing.
4. **Prepare a chain.** This saves a run and opens its first prompt for review. Preparing sends no requests.
5. **Run at your pace.** Review each step, or run the chain through. Each answer saves before another request begins. You can edit the latest answer of a paused run; the original answer is retained. Request a pause whenever you need one.
6. **Take the result with you.** Download the final answer for handoff or the trace for review. A run JSON download is restorable. Use **Save final to artifacts** to keep an explicit copy in the framework library.
7. **Come back.** The workbench prioritizes the active run. Add a note about where you stopped, archive older runs, or fork from a saved checkpoint to try a different answer. Back up the workspace and restore it without replacing existing records.

## Live generation

Keep your existing `.env` and key. For a new installation, copy `.env.example` to `.env`, then enter your private OpenRouter key. The model setting below offers only the free router in Studio.

```dotenv
OPENROUTER_API_KEY="your-private-key"
OPENROUTER_MODELS="openrouter/free"
MAX_TOKENS=2000
REQUEST_TIMEOUT_SECONDS=30
```

Restart after changing settings. Select **OpenRouter Free (openrouter/free)** in the recipe editor, choose **Prepare chain**, and review the prompt before running it. Studio offers Free when model settings are blank and alongside any model IDs you configured. OpenRouter selects an available free model for each request, subject to its free quotas. [Free router](https://openrouter.ai/docs/guides/routing/routers/free-router) · [OpenRouter limits](https://openrouter.ai/docs/api_reference/limits)

In Chain Lab, **Prepare free AI run** saves your plan and opens a separate live run. Review the preview and choose **Run first step** when you’re ready. That run pauses after each answer. [Setup and models](docs/SETUP-AND-MODELS.md#use-openrouter-free)

A live run sends its rendered prompts to OpenRouter and the selected provider. Paid models can charge for each request. The workbench dispatches each step once and waits for an explicit retry after an error. A manual retry can use another request. `MAX_TOKENS` bounds output length per request. Advanced tools also send each step once and keep their executions separate from saved workbench runs.

The settings indicator checks that a key is present and that local settings are valid. Review factual claims before using a result and use source material to check the model's critiques.

## Small commands, less setup

| Command | What it does |
| --- | --- |
| `./pc` | Start the local app on port 8000 |
| `./pc start --port 8010` | Use another local port |
| `./pc doctor` | Check local dependencies and configuration; no API requests |
| `./pc backup` | Write a timestamped Studio ZIP archive under `backups/` |
| `./pc backup /path/to/copy.json` | Write a small legacy JSON backup; refuses oversized or existing files |
| `./pc restore /path/to/copy.zip` | Add records from Studio ZIP or JSON without starting a chain |
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
- If the app shows **Retry saving this answer**, it can retry the local checkpoint without a new provider call. Keep the app open if the workspace cannot write its recovery journal. A partial provider response is saved for review before a later step can use it.
- Workspace ZIP archives and legacy JSON backups contain saved recipes, inputs, prompt traces, answers and run progress. Restore validates the complete file before writing, skips identical records, and gives colliding records new IDs. Imported running work becomes interrupted.
- JSON parts accept up to 10 MB and 2,000 recipes/runs each. The default ZIP archive splits larger workspaces into validated parts, up to 128 parts, 128 MB compressed and 256 MB expanded. Backup creation refuses files outside these restore limits. Browser drafts, `.env`, old artifacts and log files are outside workspace backups. Keep the separate `artifacts/` and `logs/` folders if you need those records. Workspace text can contain private material you entered; treat backups accordingly.
- Browser draft recovery belongs to that browser and origin. Save a recipe or prepare a run to include it in computer-level backups. If browser storage is unavailable, the editor says so and keeps explicit save available.

## The portable framework

The original Python API and advanced UI remain available. **Advanced** links to learning tools, reasoning and adversarial patterns, meta-chain design, and the artifact library. Advanced workflows have their own execution path. The local API schema is available at `/openapi.json`.

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
.venv/bin/python -m pytest -q tests/test_local_request_boundary.py tests/test_harmony.py tests/test_workbench.py tests/test_workbench_routes.py tests/test_guides.py tests/test_llm_client.py tests/test_server_routes.py
```

Tests substitute model responses and temporary storage. They do not spend provider credits. See [docs/TESTING.md](docs/TESTING.md) for the verification boundary and commands for the broader framework suite. Browser and live-provider acceptance are separate from Python tests.

Run `./verify_demos.sh` for the authored practice cases and portable-chain smoke checks using fixed responses. Individual live demos have separate instructions. [Architecture](docs/ARCHITECTURE.md) · [Demo guide](docs/DEMOS.md)
