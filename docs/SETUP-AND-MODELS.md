# Setup and models

Use this guide when installing, changing a model choice, moving workspace storage or understanding request limits. Ordinary use starts with `./pc`; you do not need to reinstall before each session.

[Documentation index](README.md) · [Quick start](QUICKSTART.md) · [Troubleshooting](TROUBLESHOOTING.md)

## Start an existing installation

From the repository folder:

```bash
./pc
```

Open [the local app](http://127.0.0.1:8000). The launcher chooses the project's `.venv` first, then `venv`, then an active virtual environment. It changes to the repository directory before starting, so an absolute launcher path also works from another directory.

`./start_app.sh` uses the same launcher. The normal server binds to `127.0.0.1` and uses one worker. It does not open a browser automatically.

## First installation

Use Python 3.11 or newer. If no project environment is already installed:

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
./pc doctor
./pc
```

Installation downloads dependencies. The app's pages, fonts and HTMX asset are local after setup. Live model calls still require network access.

On a system without Bash, activate the environment and run `python -m tools.studio start` from the repository folder. The primary local verification was performed on macOS with Python 3.12; a portable command is not evidence of acceptance on another operating system.

## Try it before configuring a provider

You can browse and edit recipes, save them, and inspect the authored Moon walkthrough without a provider key. **Prepare chain** is disabled until the local configuration is ready. The example uses fixed authored answers and makes no requests.

## Keep credentials in the local configuration

Keep an existing `.env`. If you do not have one, copy `.env.example` to `.env` once and edit the copy. Do not copy the template over an existing key file.

The minimum live settings are:

```dotenv
OPENROUTER_API_KEY="your-private-key"
OPENROUTER_MODELS="your-chosen-model-id"
```

Those values are placeholders, not working credentials or a model recommendation. Use actual OpenRouter model IDs you have deliberately chosen. Several IDs can be separated by commas; the editor exposes them in its model selector. The code accepts 1–30 configured model names.

`OPENROUTER_MODELS` takes precedence over `DEFAULT_MODEL`. When both are absent or empty, the core library has legacy fallback IDs. Configure explicit model IDs for live work rather than assuming those historical defaults are available.

Restart after changing settings. Already-exported shell environment variables take precedence over `.env`, which can explain why an edited file appears to have no effect.

The page's ready state means a key value and local settings are present. It does not contact OpenRouter to validate the key, provider access, model availability or credit balance. `./pc doctor` has the same local-only boundary.

## Set limits you understand

These sample values match `.env.example`; an existing `.env` can have different values. When omitted entirely, the code's output limit is 4096 and its temperature is 0.7.

```dotenv
MAX_TOKENS=2000
DEFAULT_TEMPERATURE=0.5
REQUEST_TIMEOUT_SECONDS=30
```

| Setting | Local validation | What it changes |
| --- | --- | --- |
| `MAX_TOKENS` | Integer, 64–12000 | Maximum output tokens requested for each response |
| `DEFAULT_TEMPERATURE` | Finite number, 0–2 | The sampling setting sent to the selected provider |
| `REQUEST_TIMEOUT_SECONDS` | Finite number, 1–120 | The timeout value supplied to the SDK request |
| `OPENROUTER_MODELS` | 1–30 names, each at most 200 characters | Choices in the editor's model selector |

A provider can impose stricter settings, output limits or context limits. Token counts differ from character counts. A response that stops at the output limit is saved with a note asking you to review it; the workbench does not make another request automatically to extend it.

The temperature setting is not a factual-accuracy control. The SDK timeout is not a guaranteed total wall-clock duration for a whole chain. Keep output form and scope clear in the prompts as well as choosing a token limit.

## Understand the request count

Preparing, saving, exporting, restoring and opening the authored example make no model requests.

In the workbench, each dispatched step makes one request through the shared client, with automatic SDK retries disabled. Review mode sends the next step and pauses after it saves. Run-through mode continues until completion, failure or a requested pause.

A four-step run can therefore send four successful requests. Manually retrying a failed or ambiguous request adds another attempt; an interrupted request may already have been processed by the provider. With run-through selected, a successful retry can then continue through the remaining steps.

The app reports usage returned for saved answers. It does not show live prices, enforce a dollar spending cap, or account for every possible failed/unfinished provider request. Check provider-side usage when that distinction matters. Advanced tools can make multiple logical calls, but each step now sends once and never retries automatically. Pattern forms show request counts; depth and rounds are bounded to 1–5.

## Choose and compare deliberately

The workbench uses one selected model for a run. Its model, recipe and inputs are snapshots; there is no per-step model switch in that run.

To compare two of your configured models manually:

1. Keep one saved recipe and the same topic/context.
2. Prepare and run with the first selected model.
3. Reuse the recipe, select the second model, and run again when you intend the additional calls.
4. Compare a few concrete criteria: following constraints, usefulness of the example, unsupported claims and effort required to revise the result.

This comparison is manual. The main workbench does not automatically run a tournament or declare the model factually correct. Repeating a run can produce a different output even with the same settings.

## Choose where work is stored

The default workspace is `workspace/studio.sqlite3` inside this repository. To use another directory:

```dotenv
PROMPT_STUDIO_DATA="/absolute/path/to/my-workspace"
STUDIO_TIMEZONE="America/Chicago"
```

`PROMPT_STUDIO_DATA` selects the directory for the workspace database and runtime lock. Changing it does not move old work. Stop the server, copy or restore the desired workspace, then restart with the intended setting. Existing legacy `artifacts/` and `logs/` remain separate in the repository.

`STUDIO_TIMEZONE` controls displayed workbench dates and defaults to `America/Chicago`. The database keeps timestamps in UTC. Use a valid IANA zone name; the interface displays “Date unavailable” for a date it cannot format.

## Use another port without changing the workspace

If port 8000 is in use:

```bash
./pc start --port 8010
```

Open [the alternate local address](http://127.0.0.1:8010). The workspace selection is unchanged. Browser drafts are origin-specific, so the new port has separate draft storage. A second server cannot own the same workspace concurrently, even if it tries a different port.

Use [Troubleshooting](TROUBLESHOOTING.md) if startup, configuration or a live request fails.
