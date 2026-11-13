# Saving, export and recovery

Save the method when you want to repeat it. Keep the run when you want its reasoning and result. Use a backup when you want to bring saved work back into the app later.

[Documentation index](README.md) · [Daily use](DAILY-USE-AND-ACCESSIBILITY.md) · [Troubleshooting](TROUBLESHOOTING.md)

## Know what each save preserves

| Action | What it preserves | Where to return |
| --- | --- | --- |
| Type in the recipe editor | A browser draft of the inputs and steps, when storage is available | The same recipe in that browser and origin |
| **Save recipe** / **Save a new copy** | A new recipe copy, audience, prompts, description, starting topic/context and review pace | **Recipes → Your recipes** |
| **Prepare chain** | A new ready run with its recipe snapshot, inputs, model and pace | **My library** |
| A step succeeds | Its sent prompt, answer, reported tokens and elapsed time | The saved run |
| **Retry saving this answer** | A received answer waiting for its local checkpoint to succeed | The affected run |
| **Save revised answer** | The revised latest answer and a retained original model answer | That step in the run |
| **Save final to artifacts** | A separate copy of a completed run's final answer and provenance metadata | **Advanced → Artifacts library** |

Preparing saves without sending a model request. A prepared run is independent of later recipe copies. You cannot change its model, pace, recipe or original input fields in place; **Use this recipe again** creates a fresh starting point with those inputs.

Browser drafts are not the same as workspace saves. Save a recipe or prepare a run before depending on a workspace backup to preserve editor work.

## Find work again

The workbench shows recent runs and can offer a recent unfinished run. **My library** contains the run list and search.

Search matches the topic, recipe title or saved state, ignoring case. It does not search inside every answer, prompt or context note. Search for a word in the topic, or a state such as `paused`, `failed` or `interrupted`.

Saved recipe copies are listed under **Recipes**, separate from the run list. An old run still contains its recipe even if you never saved that method separately: open the run, choose **Use this recipe again**, then save the recipe if you want it in that list.

Use **Where I left off** to save a short note for your next session. **Archive this run** moves a stopped run into **Archived runs**, where its answers and exports remain available. Use **Move back to My library** before continuing an unfinished archived run.

To try a different handoff without losing the original, open an earlier saved answer in a stopped live run and choose **Fork after this step**. The new run opens paused with the copied answers and their original settings. Edit the latest copied answer before continuing. Forking itself makes no model request.

## Choose the export you need

| Option | Includes | Use it for |
| --- | --- | --- |
| **Copy final answer** | The final answer's text | Paste a result into another tool. |
| **Download final answer** | The final answer with its topic and draft or authored-sample label | Hand off the result without the prompt history. |
| **Download trace** | Supplied context, prompt templates, rendered prompts, saved and original answers, and recorded attempt metadata | Inspect or explain how the result was produced. |
| **Download run JSON** | The complete saved run record | Preserve or restore a particular run with its trace. |
| **Download workspace backup** | Saved recipes and runs together, in a Studio ZIP archive | Bring workspace records back into this app. |

Trace Markdown includes source material and saved answers. Use final-answer Markdown or Copy when you intend to share just the deliverable. JSON is the full machine-readable backup record.

Exports can be made before a run finishes. They contain only the answers completed at the time of export; an unfinished provider request cannot be recovered from an answer that was never saved.

The single-run JSON export uses the same versioned backup format as a workspace backup. Restore it through **My library → Bring a workspace back**. Its recipe stays inside the imported run; use **Use this recipe again** and save a copy to add it to **Your recipes**.

## Make a workspace backup

In the app, open **My library** and choose **Download workspace backup**. The browser downloads `prompt-studio-backup.zip` to the location set in your browser.

Or use:

```bash
./pc backup
```

The command writes a timestamped `.zip` archive under the repository's `backups/` folder and prints its full path. It does not call a model. A chosen path is also supported:

```bash
./pc backup /path/to/a-new-copy.zip
```

The CLI refuses to overwrite an existing filename. Choose a new filename for a later backup. Keep a copy outside this project if you want it to survive loss of the project folder; a copy on the same disk does not protect against losing that disk.

The workspace archive captures a consistent database snapshot. Its manifest checksums every JSON part. A chosen `.json` filename still exports the legacy format when it fits the importer limits; an oversized JSON export is refused before a file is published. You can make it while the app is running. A currently running record will be restored as interrupted; the backup does not create a job that resumes on its own.

When a run shows a pending local save, resolve it before making a new archive. The archive includes committed database records. An answer waiting in the recovery file or process memory is outside that snapshot.

## Restore without replacing newer work

In **My library**, choose a Studio ZIP or JSON backup file under **Bring a workspace back**, then choose **Restore backup**. The CLI equivalent is:

```bash
./pc restore /path/to/prompt-studio-backup.zip
```

Restore validates the complete document before adding records. Identical records are skipped. If a backup contains an older or different version of an existing record with the same ID, it receives another ID, preserving both. Repeating that same colliding import is deduplicated as well.

Restoring an old backup does not rewind a newer run or replace the workspace. It adds preserved copies where needed. Imported running work becomes interrupted and waits for an explicit action. Restoring never makes a provider request.

Only Studio ZIP archives and versioned Studio JSON backups are accepted. ZIP restore validates every part before importing any records and never extracts arbitrary files. A legacy artifact JSON file, a meta-chain design, or a Markdown export is not a workspace backup.

## Understand the JSON limits

A legacy JSON backup or each JSON archive part accepts at most **10,000,000 bytes**, **2,000 recipes** and **2,000 runs**. Single-run JSON exports remain compatible.

Default backups use a ZIP archive of independent JSON parts plus a checksummed manifest. This supports workspaces beyond the old single-JSON limit without manual splitting. Archives accept up to **128 parts**, **128,000,000 compressed bytes** and **256,000,000 expanded bytes**. The same limits apply during creation, so a successful backup is within the restore format's limits. Every record and prompt reference is checked before a transaction adds anything.

If a workspace exceeds archive limits, backup creation refuses it with a recovery instruction. Keep a stopped copy of the entire workspace directory as described below. Already-created oversized legacy JSON exports are preserved, but remain outside the legacy importer limit; make a new ZIP backup from the original workspace when possible.

## Keep the separate material you care about

| Location | Workspace backup includes it? | Notes |
| --- | --- | --- |
| Workspace database recipes and runs | Yes | Includes entered context and retained original answers. |
| Browser drafts | No | Browser/profile/origin-specific; explicitly save important edits. |
| `.env` | No | Preserve credentials separately and privately if needed. |
| Legacy `artifacts/` | No | Includes JSON framework outputs and the local Chroma mirror. |
| Legacy `logs/` | No | Separate framework execution logs. |
| Files downloaded/exported elsewhere | No | Keep the files where you chose to store them. |

API configuration is excluded from JSON backups. Text you entered into context, prompts or answers is included, so a backup can contain private material. Editing an answer also retains its original text. Avoid placing credentials in prompt material, and treat exported traces according to the text they contain.

Artifacts are separate saved output. The main workbench does not automatically search that library or feed its contents into a new run. Paste the specific material you want into context, or use the explicit artifact-reference support in the [advanced Python framework](ADVANCED-TOOLS.md).

## Make a complete local folder copy

Use this when moving the workspace intact or preserving work beyond the JSON size limits.

1. Find the workspace directory using `./pc doctor`. It defaults to `workspace/` inside this project.
2. Stop the server normally with **Ctrl+C** and wait for its process to exit. Stop any other commands writing that workspace.
3. Copy the entire workspace directory to a new backup location with your file manager. Keep it intact, including any SQLite sidecar files that remain.
4. Copy `artifacts/`, `logs/` and private configuration separately if those are part of what you want to recover.

To open a preserved workspace, keep the server stopped, make a working copy of the preserved folder, and point `PROMPT_STUDIO_DATA` at that copy's absolute path in `.env`. Restart and check the library. Keep the original backup unchanged until you are satisfied.

A raw SQLite folder is not a JSON upload. Do not replace database files while a server is using them. The `runtime.lock` filename is normal; the operating system releases the actual process lock when its owner exits.

## Resume according to the run state

| State | What to do |
| --- | --- |
| **Ready to start** | Preview the first prompt, then choose **Run first step** or **Run chain**. |
| **Running** | Let it finish, request a pause, or use **Refresh progress** if the display is stale. |
| **Local save pending** | Resolve the disk or permission error, then choose **Retry saving this answer**. The answer is saved without a provider request and the run pauses before the next step. |
| **Ready for review** (`paused`) | Read the latest answer, optionally revise it, then choose **Continue chain**. |
| **Failed** | Read the error and resolve its cause before **Retry this step**. Completed answers remain saved. |
| **Interrupted** | Check whether the provider processed the unfinished request before retrying. Earlier completed answers are preserved. |
| **Completed** | Copy/export the result, inspect the trace, or reuse the recipe for another run. |

The UI permits edits to the last completed answer of a stopped, unfinished run. Fork a stopped live run when you need to revise an earlier handoff and preserve the original. With review pauses disabled, a successful Continue or Retry action can proceed through later steps as well.

Normal shutdown requests a pause, finishes the current workbench request, saves its answer and stops. An abrupt stop can lose the answer to an in-flight request, even when the provider already processed it. On the next startup, the app marks that unfinished run interrupted and waits for you.

If SQLite cannot save a received answer, the workbench attempts to keep a private `pending-step.json` recovery copy in the workspace. Normal shutdown and startup also try to save that pending answer. If the recovery copy fails too, keep the process open while you fix local storage, then retry the local save.
