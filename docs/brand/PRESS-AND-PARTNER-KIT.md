# Press and partner kit

Owner-review drafts for educators, partners, and writers. Use the version and access information Ryan has cleared for the intended reader.

## Short description

Prompt Chaining Studio helps people see how one AI answer shapes the next instruction. It includes teacher-led fifth-grade challenges and a personal workbench for reusable recipes and saved runs.

## Standard boilerplate

Prompt Chaining Studio is a local tool for practicing and using prompt chains. In a prompt chain, an answer from one step becomes part of the next instruction. In Classroom Challenges, fifth graders read clues, correct a prepared answer, and find their change in the next prompt. Teachers can lead the activity from one screen with replies written ahead of time. In Workbench, individuals can edit recipes, inspect the prompt for each step, and return to saved runs. The examples run offline after installation. Optional live generation uses the operator's configured OpenRouter key and model.

## Fact sheet

| Question | Detail |
| --- | --- |
| Project name | Prompt Chaining Studio |
| Brand line | Make the next step better. |
| Classroom audience | Fifth-grade groups with a teacher or facilitator leading from a shared screen. |
| First activity | **Rescue rainy recess**. The class checks a game recommendation against the clues and finds its own correction in the next prompt. |
| More classroom activities | **Where did the mascot go?** explores evidence and uncertainty. **Build a bridge for 8 cubes** asks students to repair directions a partner can use. |
| At-home extension | A family drawing game, a four-panel comic, and a paper pencil holder use fictional examples to get students started. |
| Workbench audience | Individuals who want repeatable AI workflows with editable prompts, review pauses and saved runs. |
| First Workbench example | **Explore the Moon example**, a four-step walkthrough with prepared answers. Fictional decision memo, evidence brief, and document review cases provide additional offline practice. |
| Setup | Python 3.11+ and local dependencies. The normal launcher opens a server on the operator's computer. Installation downloads dependencies. Authored examples work offline once installed. |
| Live model data path | The operator sets an OpenRouter key and model configuration. Each dispatched live step sends its inputs and referenced answers to OpenRouter and the chosen provider. Provider charges can apply. |
| Saved work | Recipes and runs are kept in a local SQLite workspace. Explicit exports include the final answer, prompt trace and a restorable run file. Backups can contain text the operator entered. |

[Setup and models](../SETUP-AND-MODELS.md) · [Classroom and Moon walkthroughs](../DEMOS.md) · [Professional cases](../PROFESSIONAL-CASES.md) · [Save and export](../SAVING-EXPORT-AND-RECOVERY.md)

## Owner announcement draft

**See how one answer changes the next prompt**

I’m sharing Prompt Chaining Studio for people who want to see what happens between one AI answer and the next instruction.

Start with **Rescue rainy recess**. Paper basketball got the most votes, and the classroom rules say no throwing. A fifth-grade class can check the draft, choose a fix together, and see that exact sentence appear in the next prompt. The sample replies were written ahead of time. A teacher can run the activity from a single screen after local setup.

For your own work, open **Explore the Moon example**. You can inspect the prompts that built the explanation and return to the saved run. Studio also lets you save and edit recipes for live work with a provider you set up.

Start with the classroom walkthrough or the Moon example, whichever matches what you want to try.

## Direct outreach drafts

### Teacher or instructional coach invitation

**Subject** · A short fifth-grade activity to try on one screen

Hi,

I’m inviting a few educators to try **Rescue rainy recess**, a short activity in Prompt Chaining Studio. Your class reads three clues, corrects a sample answer together, and sees the correction in the next AI prompt. It runs from one local computer with prepared replies, so the activity needs no model account or key.

Would you be open to looking at the walkthrough? If it fits your class, we can start with a projected rehearsal and see whether the setup works on your intended computer. After a class session, a few brief notes on what students understood or where they got stuck would help.

Thanks,

Ryan

### Technology lead or host briefing

**Subject** · Setup for a projected Prompt Chaining Studio activity

Hi,

I’m proposing a short teacher-led trial of **Rescue rainy recess**. The facilitator would run Prompt Chaining Studio on one approved computer and project it. Studio runs locally with Python and browser-based controls. Initial installation downloads dependencies. The activity itself uses prepared replies and runs offline after setup.

The teacher can enter a fictional class correction with no student names. The local workspace keeps the run and correction. The trial can use a dedicated demonstration workspace. The separate live Workbench workflow uses an operator-supplied OpenRouter configuration and is outside this classroom session.

Could you let me know whether this setup fits the intended computer and classroom process? I can share the local setup and data-path notes for review.

Thanks,

Ryan

### Practitioner or newsletter note

**Subject** · A local workbench that shows what the next prompt uses

Hi,

Prompt Chaining Studio keeps prompts, answers and the material passed between steps together in a saved run. Its local Moon walkthrough shows the method with prepared replies, so you can inspect the whole chain before setting up a provider. The workbench also supports editable recipes, review pauses and trace exports.

If you cover practical AI workflows, I can share a short walkthrough with a fictional run and the setup notes. The strongest demonstration is seeing a specific answer inside the next instruction and then opening that same run again in the library.

Thanks,

Ryan

### Adult follow-up after a class session

**Subject** · Where did the Rainy Recess activity work or stall?

Hi,

Thanks for trying Rainy Recess. A short reply is plenty. Were you able to open it and reach the comparison? Roughly how many of the answers you sampled explained where the fix went next? What part would you change before leading it again?

Please send counts and general observations. Keep student names, work, and recordings with your class. If you want a second activity, the mascot mystery is about checking a guess and the bridge challenge is about writing directions another group can follow.

Thanks,

Ryan

**Send checklist.** Add the approved walkthrough or setup link as appropriate. If the recipient needs files, confirm which version and distribution terms apply. Send from Ryan's chosen address so the recipient can reply in the same thread.

## FAQ for a teacher or reviewer

**What is a prompt chain?** A prompt is an instruction for AI. A chain uses an answer in a later instruction. In Rainy Recess, the instruction for writing a class announcement uses the corrected game choice.

**Is the example generated from what the class enters?** The class's actual correction appears in the next prompt. The example answer beside it was written ahead of time. Use the two as a comparison against the clues.

**Does a teacher need a key or student accounts for the activity?** One adult can lead from one projected local installation. The authored activity works offline after the dependencies are installed, with no model account or API key. Ask the host about using the intended computer.

**Where does the class's correction go?** The local workspace saves it with the run. Use a class sentence about the fictional scenario and keep personal information out of the activity. Backups and exports can contain the saved text.

**Does the activity align to a named standard or improve scores?** It is designed for fifth-grade practice in checking an answer against clues and tracing a revision. Educators can judge how that fits their goals. Curriculum alignment and learning outcomes remain to be established.

**How can students take part on a shared screen?** Read the clues aloud and allow students to speak, point, draw, or write. The facilitator can enter one class sentence. Rehearse the projection and keyboard controls with the intended equipment, and ask the host what participation supports the group needs.

**What happens when an adult turns on live answers?** The local installation uses the adult's OpenRouter key and chosen model configuration. A dispatched step sends its inputs and referenced earlier answers to OpenRouter and the chosen provider. Provider charges can apply. The authored examples remain available without a key.

**How do I try Studio?** Start with the setup guide and the walkthrough. Once the local app is running, open Home on the same computer and choose **Try a classroom challenge** or **Explore the Moon example**.

[Setup and models](../SETUP-AND-MODELS.md) · [Demo guide](../DEMOS.md)

## Media handoff

Capture from a fresh fictional run and include the app version and short asset description in the file metadata or accompanying note. Use a crop that preserves the feature's labels and makes the text legible. Use the logo and wordmark variants from the [visual identity guide](VISUAL-IDENTITY.md). Ryan supplies the published media contact and destination when preparing a release.

Use the [campaign artwork](creative/README.md#campaign-artwork) for social previews and the [Rainy Recess teacher pack](creative/rainy-recess.pdf) as an educator handout.

| Frame | Caption | Alternative text |
| --- | --- | --- |
| Classroom hero | The Rainy Recess clues give students a rule to check before they choose a game. | Rainy Recess shows three clues. The class must stay at their desks and may not throw. |
| Visible handoff | The same answer appears in the next prompt, where it takes on a new job. | Two panels show the first answer and the next prompt, with the reused answer marked in both. |
| Student correction | A fictional class correction appears inside the next prompt. | The words “Choose robot drawing” appear inside the prompt asking for a recess announcement. |
| Classroom comparison | The facilitator can compare a fictional class fix with a prepared example. | Your Fix and One Way to Solve It appear side by side. Each uses the rule against throwing. |
| Workbench example | The authored Moon walkthrough lets people inspect the prompt that produced a saved answer. | A saved Moon example shows a prior answer reused in the prompt for the next step. |

For video, include captions and a transcript. Read aloud the important action as it happens. For cards with smaller crops, use one screenshot or a short step diagram. Place longer explanations in the surrounding post.
