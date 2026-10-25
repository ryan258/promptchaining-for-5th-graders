# Daily use and accessibility

Use saved methods to reduce the amount you have to enter. A productive session can be one dictated topic, one reviewed answer and a saved stopping point.

[Documentation index](README.md) · [Getting useful results](GETTING-THE-MOST-OUT-OF-IT.md) · [Recover saved work](SAVING-EXPORT-AND-RECOVERY.md)

## A small session from start to finish

1. Start with `./pc` and open the same browser address you normally use.
2. If unfinished work is offered on the workbench, choose **Pick it back up**. Otherwise open a saved recipe.
3. Dictate the new topic. Keep existing audience and context when they still apply.
4. Prepare the chain and inspect the next prompt.
5. Run what you need. Leave an unfinished run saved when you reach a useful stopping point.

You do not have to finish every chain in one sitting. Closing the page does not pause a running chain, so request a pause when you want generation to stop after the current step.

## Save the recurring instructions once

A saved recipe keeps its audience, prompts, description, starting topic, context and review pace. Save a copy for each method you actually return to.

For example:

| Saved method | Keep stable | Change for a new run |
| --- | --- | --- |
| Explain a concept in my own terms | Familiar examples, current knowledge, final explanation length | The concept and any new source notes |
| Turn rough notes into a short draft | Reader, tone, facts-to-check instruction, output form | The topic and actual notes |
| Find one next action | Effort constraints, reversibility, stopping-point requirement | The current situation and observations |

The selected model is kept in a prepared run, rather than in the saved recipe record. Check the model selector when opening another recipe or using a different browser. An available browser draft may restore a model selection that is still configured.

**Save a new copy** preserves the previous recipe. Use names that tell you the job the method does. A recipe description is a useful place for a brief note about when to choose it.

## Use dictation in ordinary fields

The topic, audience, context, recipe notes, step names, prompts and editable answers are standard text fields. They accept your operating system's dictation or text-expansion input. The app does not supply its own microphone or speech-recognition service.

Put the intention in the topic field, recurring constraints in context, and the output instruction in the relevant prompt. That separation lets you dictate a fresh topic without repeating the whole method.

If a dictated name or detail is wrong, correct it before the chain builds on it. Review mode gives you a place to make that correction in the latest answer.

## Keyboard controls

On macOS, **Alt** means **Option**. These shortcuts need JavaScript; operating system, browser and assistive-tool bindings can take precedence.

| Shortcut or control | Action |
| --- | --- |
| **Tab** / **Shift+Tab** | Move between links, fields and buttons |
| **Skip to content** | Move past the header when the skip link receives keyboard focus |
| **Enter** or **Space** on a step's summary | Open or close that step using the browser's native disclosure control |
| **Alt+N** | Open Recipes when focus is outside a text field, selector or editable region |
| **Alt+L** | Open My library when focus is outside a text field, selector or editable region |
| **Ctrl/Cmd+S** in the recipe editor | Save the recipe as a copy |
| **Ctrl/Cmd+Enter** in the editor | Prepare a chain when live setup is available and the form is valid |
| **Ctrl/Cmd+Enter** on an unfinished run with a primary action | Activate its displayed Run, Continue or Retry action |
| **Ctrl+C** in the terminal running the server | Request a normal shutdown after the current workbench request |

The run-page shortcut can activate **Retry this step** when a run failed or was interrupted. Read the displayed state before using it. With run-through mode, continuing or retrying can also run subsequent steps after the next answer succeeds.

## Browser drafts help you resume editing

The recipe editor writes a browser draft as fields change. Opening the same recipe in that browser can recover it. Recovery announces that nothing has been sent to a model.

**Discard recovered draft** returns the editor to the recipe and starting inputs supplied by the server. It discards that recovered browser draft, not your saved recipes or runs. Save anything you still want before using it.

Drafts belong to the browser profile and origin: scheme, hostname and port. For example, `http://127.0.0.1:8000` and `http://localhost:8000` use separate browser storage, even when they reach the same server. A different port also has different browser drafts.

Use one editor tab for a particular recipe while making changes. Tabs editing the same recipe share its browser draft key, so a later edit can replace that browser draft. Saving recipes as copies and protecting run actions from stale pages do not make unsaved drafts independently versioned across tabs.

If browser storage is unavailable, the editor says so. Use **Save recipe** or **Prepare chain** to keep work in the workspace. Browser drafts are excluded from workspace JSON backups.

## Stop in a way that matches what you need

| What you want | Action |
| --- | --- |
| Leave the page while work continues | Navigate elsewhere; keep the server running. |
| Stop generation at the next saved answer | Choose **Pause after this step**. |
| Review every answer | Keep review pauses selected when preparing the run. |
| Stop the server normally | Use **Ctrl+C** once in its terminal and allow the current request to finish. |
| Return tomorrow | Start the server again and open My library or the workbench's unfinished run. |

Review pauses and the pause button apply to workbench runs. The original Advanced tools have their own execution behavior.

## Optional shorter terminal access

From the project folder, the existing command is:

```bash
./pc
```

For Ryan's current checkout, this optional alias makes the command available in the current shell from any folder:

```bash
alias pc='/Users/ryanjohnson/Projects/promptchaining-for-5th-graders/pc'
```

It is a suggested shell definition, not an alias installed by the app or this documentation. Keeping it in your shell configuration is a separate personal setup choice. Once defined, `pc`, `pc doctor` and `pc backup` use the same launcher.

If you use a text expander, save the context or prompt fragments you repeatedly need. A saved recipe is often enough for recurring instructions; expansion snippets help when the same wording also belongs in other tools.

## What has and has not been checked

The implementation includes visible focus, text labels, a skip link, native form controls and reduced-motion styles. Local route and state checks do not establish behavior with your actual browser, screen reader, dictation setup or voice-control bindings. Those interfaces remain for your own acceptance; no browser review was performed for this guide suite.
