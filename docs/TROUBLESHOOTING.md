# Troubleshooting

Start with the smallest check that explains the symptom. Preserve saved work and avoid repeating a provider request until you understand what failed.

[Documentation index](README.md) · [Setup and models](SETUP-AND-MODELS.md) · [Saving and recovery](SAVING-EXPORT-AND-RECOVERY.md)

## Check local setup

From the repository folder:

```bash
./pc doctor
```

This reports dependency availability, workspace location, configured model names and the output token limit. It does not send a request, validate account credit or prove a model is available.

## Startup and configuration

| Symptom | What it usually means | Next action |
| --- | --- | --- |
| The launcher asks for an environment | No supported project/active environment was found. | Follow the first-install steps in [Setup and models](SETUP-AND-MODELS.md). |
| `Permission denied` when invoking `./pc` | The script is not executable in this checkout. | Run `bash pc` from the project folder, or restore the launcher's executable permission. |
| A dependency is missing | The selected environment lacks part of `requirements.txt`. | Use that environment's Python to install the requirements. The launcher chooses `.venv` before `venv`. |
| Port 8000 is already in use | A process is listening there. | Use the Studio already running there if it is yours; otherwise choose `./pc start --port 8010`. Do not kill an unrelated process just to free the port. |
| “This workspace is open in another server” | Another process owns its runtime lock. | Use that server or stop it normally. Another port will not permit two owners of the same workspace. |
| Prepare is disabled | Local key/model settings are missing or invalid. | Read the setup notice. Recipes and the authored example still work without live generation. |
| A changed `.env` seems ignored | Settings are cached for the server lifetime, or shell variables take precedence. | Restart. Check for an already-exported setting overriding the file. |
| Dates show “Date unavailable” | A timestamp or `STUDIO_TIMEZONE` cannot be formatted. | Check the timezone setting; this display problem does not by itself mean the run is lost. |

Use one server worker for this workspace. The leftover presence of a `runtime.lock` file does not prove that a process still owns it. Do not delete it to bypass an active owner's lock.

## A live step fails

| Displayed problem | What to check before retrying |
| --- | --- |
| The provider did not accept the API key | Check `OPENROUTER_API_KEY` privately, then restart. “Key configured” was only a local presence check. |
| A usage or rate limit was reported | Check the provider account's usage/credit and rate state. The app does not know when those conditions will change. |
| A timeout | The provider may already have processed the request. Check its usage before sending another attempt. |
| The app could not reach OpenRouter | Check the connection. If completion is ambiguous, check usage before repeating. Completed local answers remain in the run. |
| The request was rejected | Check the selected model, supported settings and request/context size. |
| The run's model is no longer configured | Re-add that model deliberately, or choose **Use this recipe again** and prepare a fresh run with a current configured choice. |
| The answer stopped at the token limit | Read the saved partial answer. If it is the latest answer in a stopped, unfinished run, revise it before continuing; otherwise use a fresh run with a smaller scope or an adjusted limit. |

The main workbench does not retry automatically. **Retry this step** starts another attempt at the unfinished step; it does not rerun saved successful steps. In run-through mode, subsequent steps can then continue. Provider-side attempts that failed or never checkpointed may not appear in the saved token total.

## A recipe or reference is rejected

| Problem | Resolution |
| --- | --- |
| “Refers to an answer that does not exist yet” | A backward reference reaches before the first step. Check its position after adding/removing/reordering steps. |
| “Unknown placeholder” | Use `topic`, `audience`, `context`, or supported `output[-N]` references. Custom names and framework artifact references are not supported in this editor. |
| “No JSON field” | The prior answer is not plain valid JSON with that top-level field. Correct the latest answer where possible, or reuse the recipe with a whole-answer reference. |
| A name or prompt is blank | Give each step a non-empty name and prompt. Open the indicated step to correct it. |
| A prompt is too large | Shorten the original context, referenced answer or recipe. Reuse the recipe when the needed input is fixed in the current run. |
| The provider rejects a prompt within local limits | Provider token/context limits can be stricter than the app's character limits. Reduce what that step includes. |

Use [Build your own chains](CHAIN-BUILDING.md) for the exact reference syntax and input limits. The editor's step names do not create named output variables.

## Saved work looks missing

**An editor draft disappeared:** reopen the same recipe in the same browser profile and origin. `localhost`, `127.0.0.1`, another port and a private window can have separate browser storage. If browser data was cleared, only an explicit recipe save or prepared run is recoverable from the workspace.

**A recipe save is not in My library:** saved recipe copies appear under **Recipes → Your recipes**. **My library** is the run list. Preparing a chain creates a run.

**A run cannot be found by a sentence inside an answer:** search matches topic, recipe title and state, not answer bodies. Try a word from the original topic.

**The whole library looks empty:** check `./pc doctor` for the workspace directory. A changed `PROMPT_STUDIO_DATA` selects another database; it does not migrate the old one. Check the original folder or restore a backup without replacing it.

**A restored record appears as a second run:** the backup differed from an existing record with the same ID, so restore preserved both. It does not rewind the newer local version.

**A new run did not remember an earlier result:** runs have explicit inputs. Use the earlier result as context where you want it. Neither the workbench library nor the artifacts folder is automatically added to model requests.

## A page or action stops updating

| Symptom | Next action |
| --- | --- |
| Progress looks stale | Choose **Refresh progress**, or reload the run. The worker can continue even when a browser update fails. |
| “This run changed in another tab” | Reload and inspect the saved state before taking another action. The rejected stale action was not dispatched. |
| “A chain is already running” | Find the running chain in My library. Let it finish or request a pause before starting another. |
| A copy button cannot access the clipboard | The app attempts to select the text for your system's copy command. You can also export the chain. |
| A shortcut does nothing | Check keyboard focus, modifier keys and browser/assistive-tool bindings. Alt/Option navigation shortcuts are deliberately inactive while typing in fields. |
| A browser write is rejected as cross-origin | Use the form in the local Studio tab rather than an embedded/cross-site form. Keep one consistent local address. |
| The server was stopped | Restart `./pc`, reopen the run and inspect its recovered state. |

JavaScript adds draft recovery, step-list editing, copy behavior, shortcuts and automatic progress refresh. Standard HTML forms still support saves and run actions without it; progress needs a page refresh.

## A backup or artifact action fails

| Problem | Next action |
| --- | --- |
| Restore rejects a file | Choose a Studio JSON workspace or single-run export, not Markdown, a legacy artifact or a meta-chain design. |
| A file exceeds the 10 MB restore limit | Preserve it, then use a stopped workspace-folder copy or individual run exports. The app does not split large JSON backups for you. |
| A backup has too many records | The backup schema permits up to 2,000 recipes and 2,000 runs. Keep a stopped workspace-folder copy for a larger database. |
| CLI backup says the filename exists | Choose a new filename. The command deliberately preserves the existing copy. |
| Save final to artifacts fails | The answer remains saved in the run. Export it there, then inspect the legacy artifact folder's availability and permissions. |
| Chroma mirroring is unavailable | JSON remains the artifact source of truth; the workbench database is separate. `doctor` checks installation, not the health of every collection. |
| A filesystem/database write fails | Keep the last available exports and inspect free space, workspace path and permissions. Avoid repeatedly dispatching model work until saving is reliable again. |

An invalid JSON restore is validated before any records are imported. See [Saving, export and recovery](SAVING-EXPORT-AND-RECOVERY.md) for a complete recovery route, including a stopped copy of the database directory.

## Preserve useful evidence when asking for help

Keep the error wording, the step name, whether the run was paused/running, and the local output of `./pc doctor`. Describe the last action you took. Do not paste `.env`, credentials or a private trace indiscriminately; exported prompts and original answers can contain the material you entered.

A failed step is a reason to inspect that step. It does not require running the full test suite, every demo, or a live provider comparison.
