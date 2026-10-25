# Choose a recipe

Pick the method by the result you want. Each recipe is editable, and **Who is it for?** can describe you, a beginner, a class, or a specific reader.

[Documentation index](README.md) · [Better inputs](GETTING-THE-MOST-OUT-OF-IT.md) · [Custom chains](CHAIN-BUILDING.md)

## A quick choice

| I want to leave with… | Recipe | Steps |
| --- | --- | --- |
| An explanation I can understand and use | **Make it click** | 4 |
| A meaningful connection and an activity that demonstrates it | **Connect two ideas** | 3 |
| A provisional choice and one small next action | **Think a decision through** | 3 |
| A complete draft plus facts still needing review | **From thought to draft** | 4 |
| A plausible cause to investigate and one reversible experiment | **Untangle a problem** | 3 |
| A short learning sequence with its first lesson ready | **Build a learning path** | 3 |

The inputs below are author-written examples you can adapt. They have not been run against a live model as part of this documentation.

## Make it click

**Path:** Find the pieces → Build an analogy → Try it out → Make it click.

Use this for an idea that stays abstract when you read a definition. The chain identifies components, builds one analogy with its limits, creates an example, and combines those materials into an explanation with a question and suggested answer.

**Topic**

```text
Help me understand recursion well enough to explain one small example.
```

**Audience:** `Me; I understand functions but recursion still feels slippery.`

**Context**

```text
Use a simple everyday example before code. Keep the final explanation under
400 words. Explain where the analogy stops being accurate.
```

Review the first answer for the right building blocks and the second for a misleading analogy. A useful stopping point is being able to explain the example without rereading the whole chain.

To change the method, adjust the final prompt's desired form: an explanation for yourself, a teaching note, or one worked example. A model's suggested answer still needs your judgment.

## Connect two ideas

**Path:** Meet both ideas → Find the bridge → Put it to use.

Use this to compare mechanisms or bring something familiar into a new subject. Put both ideas in the topic field; there are no separate A/B fields in this workbench recipe.

**Topic**

```text
How are cooking and computer programming connected?
```

**Audience:** `A beginner who cooks but has never written code.`

**Context**

```text
Focus on sequences, changing inputs and correcting mistakes. Finish with an
activity I can do on paper. No new software or equipment.
```

Review the bridge for a shared mechanism, not just similar words. The recipe asks for limits to the comparison. Keep those limits in the final activity so a helpful analogy does not become a false equivalence.

A useful result is an activity that makes one connection visible, with a reflection question you can answer.

## Think a decision through

**Path:** Frame the choice → Test the options → Choose a next step.

Use this when you have a real choice and need to see its tradeoffs. Include what matters to you; the model cannot infer personal priorities from the title of the decision.

**Topic**

```text
Should I finish my current small project before starting another one?
```

**Audience:** `Me; be direct and practical.`

**Context**

```text
The current project needs one guide and a final review. The new idea is still
rough. I want a reversible decision that leaves only one active next action.
Do not invent deadlines, obligations or estimates of my available energy.
```

Review the framing for invented options or constraints. Check whether the second step actually compares effort, reversibility, likely benefit and failure modes. The final recommendation is provisional; you decide whether its assumptions fit.

A useful result names one action and what evidence would make you reconsider. You can add a different decision criterion by editing **Test the options**.

## From thought to draft

**Path:** Find the point → Write the draft → Read it critically → Make it ready to review.

Use this when there is something you want to say but it does not yet have a shape. Supply the reader, purpose and facts you want included.

**Topic**

```text
Draft a short explanation of why I keep reusable methods alongside finished work.
```

**Audience:** `Someone curious about practical uses of AI, with no interest in jargon.`

**Context**

```text
Target about 350 words. Tone: warm, candid and concrete.
Use only experiences and facts I provide. Do not invent quotes or statistics.
My notes: [dictate the actual notes here].
Leave missing facts marked [verify].
```

Check the outline before the draft. Correct an invented experience while it is still the latest answer. In the critique, look for specific structural changes rather than general approval.

The final answer is a draft for review. The recipe asks for facts still needing checks; it does not make the writing verified, published or automatically saved into another project.

## Untangle a problem

**Path:** See what's happening → Look underneath → Try one change.

Use this when a repeated friction point needs a smaller experiment. Start with observations rather than a diagnosis.

**Topic**

```text
I lose track of which file contains the current version of a draft.
```

**Audience:** `Me; keep the effort manageable.`

**Context**

```text
Observed: I sometimes make copies with different names and later reopen an older
copy. I already have a project folder. I want one small change using the tools I
have, with no new service. The cause is not established.
```

Review whether **See what's happening** preserves the difference between what you observed and what it inferred. Possible causes are hypotheses. The final step should suggest a change you can try and an observation that would tell you whether it helped.

A useful result fits into an actual session. If it proposes a whole new organisation system, tighten the final prompt to one reversible action.

## Build a learning path

**Path:** Find the starting point → Map the path → Teach the first lesson.

Use this when a subject is too broad to know where to begin. The recipe limits its proposed path to five small lessons and asks for the first lesson with a worked example and practice question.

**Topic**

```text
Learn enough about Python dictionaries to read and change a small configuration.
```

**Audience:** `Me; I know variables and lists.`

**Context**

```text
Use short examples I can read without running software. Explain one new idea at
a time. Keep the first practice task small. Do not invent links or sources.
```

Review the assumed prerequisites before accepting the plan. Check that the first lesson teaches the stated objective rather than expanding into a complete curriculum.

A useful stopping point is completing the first practice task and knowing the next lesson. The app does not track course completion or automatically teach later lessons; start another run with the next objective when you want one.

## When to make your own copy

Save a recipe after changing an audience instruction, recurring context, a prompt, or the review pace in a way you want to reuse. **Save recipe** and **Save a new copy** both create a new saved copy; they preserve the previous one.

To combine useful parts of two recipes, start **Build my own**, then add the specific prompts you need. Opening two recipes does not automatically combine them. Use [Build your own chains](CHAIN-BUILDING.md) to keep their handoffs explicit.
