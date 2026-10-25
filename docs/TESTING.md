# Verification

Run focused checks from the repository root, using the environment that runs the app. These checks do not need credentials or spend provider credits.

## Workbench acceptance group

```bash
.venv/bin/python -m pytest -q tests/test_workbench.py tests/test_workbench_routes.py tests/test_llm_client.py tests/test_server_routes.py
```

This covers prompt handoffs, bad references, one-pass substitution, saved inputs, durable checkpoints, explicit retries, output edits, original answer retention, stale tabs, overlapping starts, runtime lock ownership, abrupt-stop recovery, complete-file restore validation, additive restore, backup round trips, authored example behavior, HTML escaping and local-origin restrictions. Route tests use temporary databases and substitute model callables.

`./pc doctor` checks installed modules and local configuration. It does not test provider credentials or availability. `bash -n pc start_app.sh` checks launcher syntax. JavaScript syntax can be checked using a local JavaScript runtime when available; the app itself has no JavaScript build dependency.

## A focused browser pass, when authorized

Use an isolated temporary workspace and no live provider calls. Keep this as one near-completion pass:

1. Open the workbench, recipes, editor, authored example, library and learning page at desktop and narrow widths.
2. Navigate with the keyboard, including the skip link and a recipe shortcut. Inspect visible focus and long text wrapping.
3. Enter a topic, edit a prompt, add/reorder/remove a step, use Undo removed step, reload and confirm browser draft recovery. Save a recipe and confirm starting inputs survive the redirect.
4. Inspect every example answer and sent prompt, copy output if clipboard permissions permit, and download the chain.
5. Back up the temporary workspace and restore the same file. Confirm deduplication and that no provider request was made.
6. Leave live-generation buttons untouched unless a live call is separately authorized. In-process model stubs verify runner transitions; they do not establish actual provider behavior.

An actual screen-reader or voice-control pass requires the person's assistive setup. Keyboard and DOM checks alone cannot establish that acceptance. Print, clipboard permissions and download behavior also depend on the browser.

## Broader framework checks

The full suite is separate and may include legacy tests outside the current change. Let Ryan run it when wanted:

```bash
.venv/bin/python -m pytest -q
```

Do not run all demos as an offline test. `verify_demos.sh` and many demos make live OpenRouter calls and may incur charges. Inspect the chosen demo and authorize those requests first.

## Acceptance boundaries

A passing Python group establishes the tested local state transitions, routes and storage contracts. It does not establish real-provider quality, current model availability, credit balances, network behavior, full-suite compatibility, browser layout, assistive-technology acceptance, or the factual accuracy of generated material. Keep those claims separate in handoffs.
