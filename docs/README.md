# Get more out of Prompt Chaining Studio

**Inside the app:** choose **Guides** in the top navigation, or use **Alt/Option+G** outside text fields. Search titles and full guide text, then jump to a matching section. Recipe, run and library screens also link directly to relevant help in another tab. The app reads these same Markdown files; edits appear when you refresh a guide.

Start with [Getting the most out of it](GETTING-THE-MOST-OUT-OF-IT.md). It explains how to turn a rough intention into useful work without making every session a prompt-writing project.

These guides describe the current local workbench. They use the labels in the app and distinguish saved work, browser drafts, authored examples and live model output.

For positioning, identity, campaign materials and the SWOT, see the brand and marketing kit in `docs/brand/README.md` (or open `docs/brand/index.html` in a browser).

## Find the guide for your next task

| I want to… | Read this |
| --- | --- |
| Open the app and try something immediately | [Quick start](QUICKSTART.md) |
| Get a better result with less trial and error | [Getting the most out of it](GETTING-THE-MOST-OUT-OF-IT.md) |
| Choose among the six starting methods | [Recipe guide](RECIPE-GUIDE.md) |
| Write my own prompts and connect their answers | [Build your own chains](CHAIN-BUILDING.md) |
| Follow a complete example with realistic inputs | [Worked examples](WORKED-EXAMPLES.md) |
| Try a prompt chain with a fifth-grade class | [Classroom walkthrough](DEMOS.md#try-it-with-a-class) |
| Practice reviewing a professional handoff without a key | [Professional practice cases](PROFESSIONAL-CASES.md) |
| Reduce typing and make sessions easier to resume | [Daily use and accessibility](DAILY-USE-AND-ACCESSIBILITY.md) |
| Set up the app, choose a configured model, or adjust limits | [Setup and models](SETUP-AND-MODELS.md) |
| Understand saves, exports, backups and interrupted runs | [Saving, export and recovery](SAVING-EXPORT-AND-RECOVERY.md) |
| Resolve an error or unexpected behavior | [Troubleshooting](TROUBLESHOOTING.md) |
| Use reasoning patterns, debate, meta-chains or the Python framework | [Advanced tools](ADVANCED-TOOLS.md) |

## Choose a short reading route

**First visit:** [Quick start](QUICKSTART.md) → the authored Moon example in the app → [Recipe guide](RECIPE-GUIDE.md). You can inspect the example without a key or provider requests.

**A useful session today:** [Getting the most out of it](GETTING-THE-MOST-OUT-OF-IT.md) → one example in [Worked examples](WORKED-EXAMPLES.md) → save the method that helped.

**A method you want to repeat:** [Build your own chains](CHAIN-BUILDING.md) → [Daily use and accessibility](DAILY-USE-AND-ACCESSIBILITY.md). Keep stable instructions in the recipe and starting context; change the topic for each run.

**Returning after a break:** open **My library** in the app. Use [Saving, export and recovery](SAVING-EXPORT-AND-RECOVERY.md) if a run is paused, failed or interrupted.

## The vocabulary in one minute

| Term | What it means here |
| --- | --- |
| Recipe | A named sequence of 1–8 prompts, with an audience and short description. A saved copy also keeps starting topic, context and review pace. |
| Topic | What this particular run is about. It can be a question, a writing intention or a problem. |
| Context | Notes, constraints or source material that a prompt can include through `{{context}}`. |
| Step | One instruction to the model. Earlier answers enter it only where its prompt references them. |
| Run | A saved snapshot of a recipe, inputs, selected model and progress. Preparing it makes no model request. |
| Trace | The exact prompts, saved answers, reported token usage and timing for completed steps. Edited answers also retain their original model output. |
| Artifact | A separate saved framework output. A completed run can explicitly copy its final answer into the artifacts library. |
| Browser draft | Editor recovery stored in that browser and origin. Use an explicit save to include the work in workspace backups. |

## Keep the handoff visible

An explanation, critique or recommendation is model output you can inspect. A chain can develop an idea and can also carry an error forward. Use review pauses where a mistaken early answer would change the outcome. The app does not browse the web or independently verify sources for the main workbench.

The authored Moon example has fixed answers and is labelled as an example. New live outputs will vary. The sample inputs and prompts in this guide suite are author-written suggestions, not evidence of a live provider run.

## Technical and historical reference

| Reference | Use it for |
| --- | --- |
| [Architecture](ARCHITECTURE.md) | Modules, execution ownership, persistence and trust boundaries |
| [Roadmap](../ROADMAP.md) | Phased path, current foundation, and deferred scope |
| [Testing](TESTING.md) | Focused offline checks and the boundary between tests and human acceptance |
| [Workbench status](WORKBENCH-STATUS.md) | What was implemented and which local checks were performed |
| [Demo guide](DEMOS.md) | Offline demonstrations and the scope of individual live scripts |
| [Earlier demo notes](LEGACY-DEMOS.md) | Historical material from a previous interface |
| [Ideas](IDEAS.md) | An older idea inventory, including proposals that may not exist |
| [Changelog](CHANGELOG.md) and [earlier release notes](WHATS_NEW.md) | Historical development notes |

The [repository README](../README.md) is the short overview. This folder is the operating guide. See [ROADMAP.md](../ROADMAP.md) for future horizons.
