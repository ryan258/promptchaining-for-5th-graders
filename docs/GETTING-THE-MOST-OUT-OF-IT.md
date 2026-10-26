# Getting the most out of it

Use the workbench to finish a small piece of thinking: an explanation you understand, a draft you can revise, a choice you can act on, or a next step you can actually do.

The most useful change is usually to the question or the first handoff. More steps and longer answers can add effort without improving the result.

[Documentation index](README.md) · [Choose a recipe](RECIPE-GUIDE.md) · [Try a worked example](WORKED-EXAMPLES.md)

## Start with what you want to leave with

A topic names the work. A useful intention also names its destination.

| Rough starting point | A more useful direction |
| --- | --- |
| “Explain this topic.” | “Help me understand recursion well enough to explain one example to someone else.” |
| “Write something about backups.” | “Draft a short guide that helps me make one backup and know where it went.” |
| “Help me plan.” | “Turn these unfinished tasks into one manageable action for today.” |
| “Which option is best?” | “Compare these options by effort and reversibility, then suggest one small test.” |

You do not need to supply a polished brief. A dictated sentence plus two or three constraints is enough to begin. If you already know the desired final form, say it: a paragraph, a three-item list, an outline, a worked example or one next action.

## Give the three input fields different jobs

**What would you like to work on?** holds the intention for this run.

**Who is it for?** describes the reader or learner. “Me; I know the basics, use a concrete example” is a useful audience. The fifth-grade default is a starting point for clear explanations; you can change it.

**Anything it should know?** holds constraints and source notes. Use plain language. Labels such as these are ordinary text, not a required syntax:

```text
Outcome: one useful next action, not a complete system.
Constraints: low typing, no new services, easy to stop and resume.
Known facts: [add the facts or notes the chain should work from].
Uncertainty: say what you do not know instead of filling it in.
```

For writing, include intended reader, approximate length and any source facts. For learning, include what you already understand. For decisions, include actual options and non-negotiable constraints. This gives the chain something specific to work with.

In a custom recipe, a field reaches a model only when that prompt includes its placeholder. The [chain-building guide](CHAIN-BUILDING.md) explains this handoff.

## Use review mode where judgment matters

Keep **Pause after each step so I can review or edit the answer** selected while trying a recipe, testing new instructions, or using material where an early mistake would be costly to carry forward.

After an answer arrives, check three things:

1. **Direction:** did it understand the actual job?
2. **Grounding:** which statements came from your notes, and which are guesses or new claims?
3. **Usefulness:** is this the material the next step needs?

If the latest answer needs a correction, open **Edit this answer before continuing**, change it, and choose **Save revised answer**. Then inspect **Preview the exact next prompt**. It should include your revised material where the recipe references that answer.

The original model answer remains available in the trace. Editing changes the next step's input; it does not erase the history or automatically fact-check the correction.

If an earlier answer needs changing after later steps have already run, use **Use this recipe again**, revise the method or context, and prepare a new run. The editor cannot rewind or branch a finished run, or rerun only an arbitrary selection of steps.

## Learn from the first answer

When a result misses, locate the earliest point where it stopped matching your intent.

| What you notice | Change to try |
| --- | --- |
| It chose the wrong problem | Rewrite the topic as an outcome and add one concrete example. |
| It invented facts about you | State the known facts and ask it to label missing information. |
| It gave a generic list | Name the constraints and require a small, specific output. |
| It ignored useful earlier work | Check that the next prompt references the right previous answers. |
| It lost the source notes | Include `{{context}}` in the step that needs those notes. |
| The final answer became much longer than useful | Specify the final form and approximate length in the final prompt. |
| The critique sounds confident but offers no evidence | Ask for specific passages, assumptions and questions to verify. Check important claims against actual sources. |

Change one meaningful thing for the next run: the topic, context, a prompt, or the selected model. Keeping the other parts stable makes it easier to understand the effect. It is a practical comparison, not a formal quality benchmark.

## Run through once the method earns it

For a familiar, low-consequence task, you can uncheck review pauses before preparing the run. The worker continues through the remaining steps and saves each answer.

This trades intermediate review for fewer actions. **Pause after this step** lets the current request finish, saves it, and stops before continuing. Leaving the page does not pause the worker; the server continues while it is running.

A prepared run keeps its own chosen pace, model, recipe and inputs. To change those settings, reuse the recipe and prepare another run.

## Keep the method that reduced your work

Save a recipe when you notice a repeatable improvement: a good audience instruction, a helpful critique, a useful output format, or a constraint you keep retyping.

Give the saved copy a name you can recognise later:

- `Explain it — concrete example, then practice`
- `Rough notes — short draft for my own site`
- `Stuck point — one reversible next action`

Each recipe save creates a copy. Add a short note about when it helps. Open your saved copy next time, change its topic, and keep the recurring context. The [daily-use guide](DAILY-USE-AND-ACCESSIBILITY.md) shows how this reduces input.

## Take the right amount of output with you

| What you need | Use |
| --- | --- |
| Just the result to paste elsewhere | **Copy final answer** |
| A readable record of every completed answer | **Export Markdown** or **Download chain** |
| The recipe, inputs, exact sent prompts and complete saved trace | **Export JSON** |
| A separate framework copy of the finished answer | **Save final to artifacts** |
| Your saved recipes and runs together | **My library → Download workspace backup** (Studio ZIP) |

Markdown contains the step answers and run information; it does not contain the full prompt trace. JSON keeps the fuller record. The [saving guide](SAVING-EXPORT-AND-RECOVERY.md) explains these differences.

## Give yourself a clear stopping point

Before starting, finish the sentence: “This session has done enough when I have…”

The answer might be a clearer question, a usable paragraph, an explanation you can repeat in your own words, or a small test you want to try. You can stop with unfinished thinking saved. A longer chain is not a requirement for a useful session.

For your next session, choose one [worked example](WORKED-EXAMPLES.md) close to the job you already have.
