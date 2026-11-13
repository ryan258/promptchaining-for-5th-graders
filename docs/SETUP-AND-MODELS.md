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

On a system without Bash, activate the environment and run `python -m tools.studio start` from the repository folder.

The targeted checks used an existing macOS arm64 environment with Python 3.12.14. For that version baseline, add `-c constraints.txt` to the install command:

```bash
.venv/bin/python -m pip install -r requirements.txt -c constraints.txt
```

The constraints record the installed versions of direct dependencies and Starlette. Pip still resolves the other transitive dependencies. Fresh installation and other platforms remain separate checks.

## Try it before configuring a provider

You can browse and edit recipes, save them, and inspect the authored Moon walkthrough without a provider key. **Prepare chain** is disabled until the local configuration is ready. The example uses fixed authored answers and makes no requests.

## Keep credentials in the local configuration

Keep an existing `.env`. If you do not have one, copy `.env.example` to `.env` once and edit the copy. Do not copy the template over an existing key file.

Studio needs a private API key. Create one in your OpenRouter account and enter it in `.env`. [OpenRouter API keys](https://openrouter.ai/keys)

```dotenv
OPENROUTER_API_KEY="your-private-key"
```

Restart after changing settings. Already-exported shell environment variables take precedence over `.env`, which can explain why an edited file appears to have no effect.

The page's ready state checks the key value and local configuration. OpenRouter validates the key and checks provider access when you send a step. `./pc doctor` checks local configuration without sending requests.

## Use OpenRouter Free

1. In a recipe, choose **OpenRouter Free (openrouter/free)** as the **AI model**.
2. Choose **Prepare chain** to save a run and preview the first prompt.
3. Choose **Run first step** when you're ready to send it. Review the answer before continuing.

In Chain Lab, choose **Prepare free AI run** on the design page. This saves your lab plan and opens a separate live run with review after each step. Your first prompt appears for review before you choose **Run first step**.

OpenRouter Free uses your API key and routes each request to an available free model. The actual model may vary from step to step. Each dispatched step uses one request from your OpenRouter quota, so a three-step run uses three requests when all three steps are sent. Check OpenRouter for the current limits. [Free router](https://openrouter.ai/docs/guides/routing/routers/free-router) · [OpenRouter limits](https://openrouter.ai/docs/api_reference/limits)

When `OPENROUTER_MODELS` and `DEFAULT_MODEL` are unset or blank, Free is Studio's only model choice. The example configuration sets that choice explicitly.

```dotenv
OPENROUTER_MODELS="openrouter/free"
```

For more choices, enter 1–30 comma-separated OpenRouter model IDs in `OPENROUTER_MODELS`. This takes precedence over `DEFAULT_MODEL`. Studio shows the configured models in order and includes Free. Legacy core callers use their own defaults when both model settings are blank.

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
| `OPENROUTER_MODELS` | 1–30 configured IDs, each at most 200 characters | Configured choices in the recipe editor |

A provider can impose stricter settings, output limits or context limits. Token counts differ from character counts. If a response reaches the output limit, the workbench saves and flags the partial answer, then pauses for review before any following step.

The temperature setting is not a factual-accuracy control. The SDK timeout is not a guaranteed total wall-clock duration for a whole chain. Keep output form and scope clear in the prompts as well as choosing a token limit.

## Understand the request count

Preparing, saving, exporting, restoring and opening the authored example make no model requests.

In the workbench, each dispatched step makes one request through the shared client, with automatic SDK retries disabled. Review mode sends the next step and pauses after it saves. Run-through mode continues until completion, failure or a requested pause.

A four-step run can therefore send four successful requests. Manually retrying a failed or ambiguous request adds another attempt; an interrupted request may already have been processed by the provider. With run-through selected, a successful retry can then continue through the remaining steps.

The app reports usage returned for saved answers. It does not show live prices, enforce a dollar spending cap, or account for every possible failed/unfinished provider request. Check provider-side usage when that distinction matters. Advanced tools can make multiple logical calls, but each step now sends once and never retries automatically. Pattern forms show request counts; depth and rounds are bounded to 1–5.

## Choose and compare deliberately

The workbench saves the selected model ID, recipe and inputs with the run. With the Free router selected, each step requests `openrouter/free` and the actual model is recorded when OpenRouter reports it.

Each saved live attempt records the requested token limit, temperature, and timeout. When reported by the provider, the trace also records the returned model, response ID, finish reason, and token counts. A later attempt after restarting with new settings can differ from earlier steps in the same run.

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
