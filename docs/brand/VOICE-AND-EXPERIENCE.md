# Voice, editorial, and product experience

**Prompt Chaining Studio · Proposed application standard · November 12, 2026**

## Write for the next action

Lead with the problem, the choice, or the state of the work. Speak directly to the person using Studio. Put one action in each instruction and keep important nouns near their verbs. Use a short real example wherever a mechanism is easier to see than to define.

| Context | Start here | Example |
| --- | --- | --- |
| Student screen | The story and a decision | “Recess moved inside. Which game fits the rules?” |
| Teacher guide | What learners do and what the teacher sets up | “Project the clues. Ask each pair to pick a game and name the clue that supports it.” |
| Workbench | The user’s intention or saved state | “Two of four steps saved. Review the next prompt when you’re ready.” |
| Technical guide | The action and the actual boundary | “Prepare chain saves a run. The model request begins when you run a step.” |
| Marketing | A visible action with a concrete payoff | “Fix one answer and see your words in the next prompt.” |

Favor short sentences for student directions. Read them aloud. Give students one clear objective, the same clues the sample sees, and a place to explain a choice. Use familiar stories and leave room for alternatives supported by the clues. Give adults enough detail to set up, facilitate, and interpret what they see.

## Words to use consistently

| Term | First use |
| --- | --- |
| **Prompt** | What you ask AI to do. For practitioners, use “instruction to the model” when it adds precision. |
| **Prompt chain** | A series of prompts. An answer from one step can become part of a later prompt. |
| **Draft** | An answer ready to be checked and revised. Label prepared practice content on first contact. |
| **Your fix** | The learner’s edit. Preserve the exact wording when showing what went into the next prompt. |
| **One way to solve it** | A prepared example for comparison. Invite students to test each idea against the clues. |
| **Recipe** | A reusable set of instructions for a chain. |
| **Run** | A saved attempt using a snapshot of a recipe and its inputs. |
| **Trace** | The prompts and answers in order. Name the export **Download prompts and answers** where the action is student-facing. |
| **Live run** | A run that calls a configured model. State the data destination and potential charges at the decision point. |

Use sentence case for headings and controls. Set commands and literal keys in code style or the keyboard treatment. Use “you” for a person’s choices and “Studio” for what the application does. Keep actual UI labels in walkthroughs. Save generic phrases such as “Continue” for a sequence with an obvious next step. Where the action has a cost or a different result, use the specific verb.

## Product patterns

| Pattern | Design and copy |
| --- | --- |
| Entry and return | Show one dominant action per immediate task. Keep **Pick it back up** near the saved topic, progress, and any “Where I left off” note. Keep the work in view during a pause. |
| Classroom sequence | Let learners make a choice before revealing the first answer. Label the clue, draft, fix, and next prompt. Place the carried text near its original so students can point to both. Compare their fix with the example after the handoff. |
| Form | Use a persistent label above the field and a short hint below it. Provide native text inputs for dictation and text expansion. Keep entered text when correction is possible. |
| Step review | Put the next prompt near the source answer. Give a deliberate **Run next step** action for live work and label where the result goes. |
| Running and pausing | “Step 2 is running. Pause after this step” describes when the app can stop. On pause, say what saved and how to resume. |
| Interruption | Show the latest saved state and the next available action. Distinguish retrying a local save from retrying a provider request. Where relevant, say that a previous request may already have used credits. |
| Empty library | Say what will appear and how to create it. Example “Saved runs appear here. Open the Moon example to see how a run works.” |
| Error | Name what failed, preserve work where possible, and give one recovery action. Example “Studio couldn’t save this answer. Retry saving it on this computer.” Avoid displaying raw provider responses or private data. |
| Export | Name the artifact and format. “Download final answer” and “Download prompts and answers” serve different needs. Warn where an export or backup can contain source material the user entered. |

Use visible focus, a skip link, semantic headings, native keyboard behavior, and text cues for status. Associate field errors with the field. Announce newly saved or failed states in the appropriate live region. Keep the same logical reading order if comparison panels stack. Put the definition of a handoff in words alongside the visual cue. Let text wrap in prompts, retain meaningful paragraph breaks, and keep reduced-motion behavior. Document actual key bindings and potential OS conflicts. [Current accessibility features and checks](../DAILY-USE-AND-ACCESSIBILITY.md)

## Editorial rules for product claims

| Topic | Wording to use | Evidence |
| --- | --- | --- |
| Offline | “This challenge uses prepared answers and makes no model requests. Install Studio before class.” | [Demo walkthrough](../DEMOS.md#try-it-with-a-class) |
| Revision | “Your fix appears in the next prompt. Then compare it with a prepared example.” | [Classroom template](../../server/templates/workbench/_classroom.html) |
| Local storage | “Studio saves runs and recipes on the computer running the app. Browser drafts belong to the browser profile and local address.” | [Saving and recovery](../SAVING-EXPORT-AND-RECOVERY.md) |
| Provider boundary | “Live prompts send the relevant inputs and referenced answers to OpenRouter and the selected provider. Provider charges can apply.” | [Setup and models](../SETUP-AND-MODELS.md) |
| Access | “The app has keyboard shortcuts, visible focus, and standard fields that accept system dictation.” | [Daily use and accessibility](../DAILY-USE-AND-ACCESSIBILITY.md) |
| Recovery | “Completed steps are saved. You can return to the last checkpoint. Interrupted provider requests require an explicit next action.” | [Saving and recovery](../SAVING-EXPORT-AND-RECOVERY.md) |

Use specific capabilities in place of blanket privacy, accessibility, learning-outcome, cost, or safety claims. Keep a published claim tied to the version and evidence behind it. Use sample data in public images. Remove personal material and credentials before exporting a trace for demonstration.

## Applying the guide

Use the screen labels and behavior in the current app when updating a walkthrough. In a proposed design, describe the interaction the label would trigger. When a label changes, update the help, screenshots, and scripts that show it. For public reuse, keep editable text beside graphics so an image is never the only source of essential directions. [Copy kit](COPY-KIT.md) · [Creative files](creative/README.md)
