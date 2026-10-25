# Build your own chains

A useful custom chain gives each step a job and gives the following step the specific material it needs. Start with three or four steps. Add another when you can explain what it contributes to the result.

[Documentation index](README.md) · [Recipe guide](RECIPE-GUIDE.md) · [Worked examples](WORKED-EXAMPLES.md)

## Open the editor

Choose **Recipes → Build my own**, or open a starter recipe to adapt it. Each step has a name, a short explanation of its purpose and a prompt.

The name and purpose describe the method in the interface. They are not automatically added to the model request. Put instructions that the model needs inside **Prompt**.

Use **Add a step**, **Move up**, **Move down** and **Remove step** to shape the sequence. **Undo removed step** restores the most recently removed step during that page session, provided there is room for it. It is not a general version-history tool.

## Understand exactly what carries forward

Each workbench request contains the current step's rendered prompt. It does not inherit a hidden conversation with earlier steps. Include earlier answers and original inputs explicitly where they matter.

| Placeholder | What it inserts |
| --- | --- |
| `{{topic}}` | The run's topic or intention |
| `{{audience}}` | The recipe's audience |
| `{{context}}` | The run's context notes, or `No additional context.` when empty |
| `{{output[-1]}}` | The most recent saved answer |
| `{{output[-2]}}` | The answer from two steps ago |
| `{{output[-3]}}` | The answer from three steps ago |
| `{{output[-1].title}}` | The top-level `title` field from a previous answer that is valid JSON |

References count backward from the current step. In step 3, `output[-1]` means step 2 and `output[-2]` means step 1. After moving or removing a step, inspect every affected reference. References are positional; the app does not rewrite them to follow renamed or moved steps.

The first step cannot reference an earlier answer. Only the listed input names and earlier-output references are supported in this editor. It does not provide arbitrary variables, Jinja statements, Python expressions, or workbench `{{artifact:...}}` references. Artifact references belong to the separate framework API.

Input text and inserted answers are substituted once. If your context contains something that looks like `{{output[-1]}}`, it stays literal text inside that context; it does not become another template instruction.

## A complete three-step recipe

This recipe turns rough notes into one next action. The prompts below are complete, author-written suggestions. You can paste each into a separate step; they are checked locally for valid placeholder references, not against a live provider.

**Recipe name:** `Rough notes → one useful next action`

**Audience:** `Me; be concise, concrete and careful about assumptions.`

**Suggested topic:** `Help me decide what to do next with these unfinished notes.`

**Context:** dictate the actual notes, constraints and known commitments. Keep review pauses selected while trying the method.

### Step 1: Sort the notes

**Purpose:** Keep known facts separate from guesses before suggesting action.

**Prompt**

```text
Help {{audience}} with this intention:
{{topic}}

Read these notes:
{{context}}

Separate stated facts, constraints, assumptions and unresolved questions.
Do not invent commitments, deadlines or personal facts.
Finish with a one-sentence description of the result I seem to need.
Keep this under 250 words.
```

### Step 2: Find small options

**Purpose:** Turn the clarified situation into a few manageable choices.

**Prompt**

```text
Intention: {{topic}}
Reader: {{audience}}
Original notes and constraints:
{{context}}

Use this clarified situation:
{{output[-1]}}

Propose three small, reversible next actions. For each, state what I would do,
the effort it seems to require, and what I could learn. Label uncertain effort
estimates as assumptions. Do not introduce a new service or system unless my
notes explicitly ask for one. Keep the whole answer under 250 words.
```

### Step 3: Choose a starting point

**Purpose:** Leave with an action and a place to stop.

**Prompt**

```text
Intention: {{topic}}
Reader: {{audience}}
Original notes and constraints:
{{context}}

Clarified situation:
{{output[-2]}}

Candidate actions:
{{output[-1]}}

Suggest the smallest useful action that fits the stated constraints.
Return four short parts: Next action; Why this one; Stopping point; What would
change this recommendation. If an essential fact is missing, name it rather
than pretending it is known. Keep the answer under 150 words.
```

The final step deliberately uses both earlier answers. It also keeps the original context visible so a summary does not silently replace the user's constraints. Word counts are requests to the model; the separate token setting provides the enforced per-response limit.

## Check the chain before spending a request

1. Read the prompts in order. Each should contribute something the next one uses.
2. Check that the first step uses only original inputs.
3. Check that every backward reference points to the intended answer.
4. Save the recipe, then prepare a run.
5. Open **Preview the exact next prompt**. It should include the actual topic, audience and context where you placed their placeholders.
6. After each saved answer, check the next prompt again. If you edited the latest answer, confirm that the preview contains the revision.

Saving and preparing do not send requests. Starting a step does. A later prompt cannot be previewed with an actual earlier answer until that answer exists; the editor still shows its template.

## Use JSON fields only when you need them

An entire answer is usually the simplest handoff. A top-level JSON field helps when the following step needs one small part.

For example, ask an earlier step to return **only a JSON object without code fences**, with a string field named `title`. A following prompt can then use:

```text
Write a concise introduction for this title:
{{output[-1].title}}
Audience: {{audience}}
```

The earlier answer must be valid JSON containing that field. A fenced JSON block, prose before the object, a missing field, a nested path such as `.outline.title`, or an array expression such as `[0]` will not satisfy this editor's field reference. If parsing fails, correct the latest answer while stopped, or reuse the recipe with a whole-answer reference.

The workbench does not automatically retry a response to make it valid JSON. That keeps request counts explicit.

## Keep changes small enough to understand

| If you need… | Try this change |
| --- | --- |
| A better explanation | Add a concrete example and a question that checks understanding. |
| A better draft | Put a focused critique between drafting and revision; reference both in the revision prompt. |
| More grounded advice | Include the original notes at the decision step and distinguish evidence from assumptions. |
| A shorter result | Specify the final form, approximate length and stopping point. |
| Fewer calls | Remove a step only when the remaining prompts still do its useful work. Recheck references. |

One well-specified prompt can be enough for a simple transformation. A chain is useful when a later step benefits from material produced earlier. It does not guarantee an improvement merely because it has more stages.

## Editor limits

| Item | Limit |
| --- | --- |
| Steps in a recipe | 1–8 |
| Recipe name | 120 characters |
| Recipe description | 600 characters |
| Audience | 200 characters |
| Topic | 3,000 characters |
| Context | 16,000 characters |
| Step name / purpose | 100 / 400 characters |
| Each prompt template | 8,000 characters |
| Each fully rendered prompt | 120,000 characters |
| Each saved answer | 60,000 characters |

These character limits are separate from a provider's token/context limits. A model can reject a request that fits the local character limits. See [Setup and models](SETUP-AND-MODELS.md) for the enforced token and timeout settings.
