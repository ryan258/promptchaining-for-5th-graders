# A short path to your first useful chain

[Documentation index](README.md) · [Get more out of a session](GETTING-THE-MOST-OUT-OF-IT.md) · [Setup help](SETUP-AND-MODELS.md)

If the project is already installed, start it from the repository folder:

```bash
./pc
```

For a first installation, use Python 3.11+:

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
./pc
```

Open [the local app](http://127.0.0.1:8000). Select **Explore the Moon example** to see an authored Moon explanation built in four steps. The example needs no key and makes no requests. Open the saved answers and **Prompt that produced this answer** to see the handoffs.

Choose **Try a classroom challenge** to catch a mistake in a written example. Save your fix and look for it in the next prompt. [Classroom walkthrough](DEMOS.md#try-it-with-a-class)

To use your own topics with a live model, copy `.env.example` to `.env` only if you do not already have a key file. Set `OPENROUTER_API_KEY` and `OPENROUTER_MODELS` to your chosen key and model IDs. Restart with `./pc`. Never put credentials in a topic, context field, or recipe.

Choose **Recipes**, select a method, and enter or dictate your topic. Adjust the audience or context if needed. **Save recipe** keeps the method and starting inputs on this computer; each save preserves earlier copies. **Prepare chain** saves a new run without sending a request. Inspect its prompt, then choose **Run first step**. Review the saved answer and continue when ready.

Pause after each step is on by default. You can uncheck it in the editor to run through. **Pause after this step** lets the current provider request finish, saves its answer, and stops. The library holds completed and unfinished work. Editing the latest answer of a stopped, unfinished run preserves its original answer and changes what the next step receives.

Use `Alt+N` for recipes and `Alt+L` for the library when focus is outside text fields. `Ctrl/Cmd+S` saves in the editor, and `Ctrl/Cmd+Enter` prepares a run or activates its displayed next action. On a failed/interrupted run, that action can be a retry. System dictation works in every text field. Some systems reserve these shortcuts.

Useful commands:

```bash
./pc doctor
./pc backup
./pc restore /path/to/prompt-studio-backup.zip
```

These commands make no provider requests. `doctor` checks local configuration. Workspace backups include recipes and runs. Keep important browser drafts with an explicit save and preserve credentials and legacy artifacts separately. See [Saving, export and recovery](SAVING-EXPORT-AND-RECOVERY.md) for formats and limits.

Stop with `Ctrl+C`. Normal shutdown finishes the current workbench request and pauses; an abrupt stop is marked interrupted at the next startup and never automatically retried. Provider charges can still apply to a request whose answer was not recovered.

Choose a [recipe](RECIPE-GUIDE.md), follow a [worked example](WORKED-EXAMPLES.md), or [practice a professional workflow](PROFESSIONAL-CASES.md) with a fixed source packet.
