# Demonstrate the workbench

[Documentation index](README.md) · [Professional practice cases](PROFESSIONAL-CASES.md) · [Verification](TESTING.md)

## A walkthrough with no provider key

Start with `./pc`. Open the local app and choose **Explore the Moon example**. The Moon example uses four authored answers. Open **Prompt that produced this answer** after each step to see what material was carried forward. The prompts and responses show the visible handoffs of the workflow.

## Try it with a class

Open [Classroom challenges](/studio/practice) on the classroom screen and choose a problem together. Try [rainy recess](/studio/practice#rainy-recess), [the missing mascot](/studio/practice#missing-mascot), or [the paper bridge](/studio/practice#paper-bridge). Each challenge uses written examples and works offline.

1. From Home, choose **Try a classroom challenge**. Read the clues aloud and have students make their own pick. Then show the first answer and ask them to find the same words in the next prompt.
2. Show the draft. Ask which clue it missed. Have the class write one sentence that fixes it.
3. Save the class’s fix. Open the next prompt and have students point to the words they added. A prompt is an instruction. In a chain, one answer can become part of the next instruction.
4. Compare the class’s fix and the example side by side. Ask which clues support each answer and whether both ideas could work. The example answer was written ahead of time.

## Build the next prompt

From Home, open **Build the next prompt** under **Keep exploring** and start [Sneak a dragon through the library](/studio/practice#dragon-library). The challenge saves as you go and uses prepared answers offline.

1. Read the clues and see which route the dragon can take. Ask students to name the route and the library rule they’ll need to carry forward.
2. Choose **Make a map note** or **Give spoken directions**. In the last prompt, find the route from the first answer and the job you chose in the second step.
3. Predict what would change with the other job. Choose **See the prepared answer** and compare the two examples. Can you find the same route in both?

Try a third job at home. The child gives the route to a parent or caregiver and asks for a new result, such as a two-line rhyme. The grown-up plays the AI and makes the rhyme using the route and the library rule.

## Build your own chain in Chain Lab

Choose [Build your own chain](/studio/lab) on Home, in the classroom challenge chooser, or after the dragon challenge. Pick a mission or bring your own idea. Make a chain with two to five steps, each with a job in your words. Add `[Goal]`, `[Clues]`, or an earlier answer such as `[Answer 1]` where that step needs it. Chain Lab puts the actual text into the prompt, and a person supplies the answer. Each answer saves as you go. You can play offline.

| Mission | What the chain lets you try |
| --- | --- |
| **Race through the Moon Museum** | Plan a delivery route, check it when the lift breaks, and write a radio message the night crew can follow. |
| **Meet a creature from Planet Ooze** | Give two explorers different jobs with the same clues, then combine their answers into a field guide page. |
| **Teach the recess robot a game** | Make different cards for a new player and a referee, then check that both follow the same rules. |
| **Build a sock arcade** | Playtest a game with a tricky toss and use what happened to write a clearer game card. |

### Try one change at home

1. Start **Meet a creature from Planet Ooze**. The child runs the chain. A parent or caregiver plays the AI. Read aloud or show only the filled-in prompt for the current step. Ask the grown-up to answer from that prompt and say when they need another clue.
2. Save the first two answers about movement and hiding spots. For the field guide step, find the parts of the prompt that came from `[Answer 1]` and `[Answer 2]`. Save the field guide and mark where it tells readers where to look.
3. Make a remix. The original stays saved, and the remix starts at Step 1. Remove `[Answer 2]` from the field guide prompt and take out its heading if you see one. Keep the job and the movement handoff. Choose **Reuse original answer** for the first two prompts, then give the grown-up the new field guide prompt. Which part of the page is harder to write now? What other clue would help?

### Run the chain in a group of three

The **chain designer** writes the job and chooses which clues or answers to pass along. The **answerer** plays the AI using only the filled-in prompt the designer reads aloud or copies to them. The **checker** looks at the full chain, points to the source of a detail in the answer, and asks what the answerer needed that the prompt left out. Switch roles after a round. Try comparing the two cards in **Teach the recess robot a game** and check that a new player and a referee would agree about what to do when somebody moves.

## Try a discovery mission

On Home, under **Kids**, choose [Try a discovery mission](/studio/lab#insight-missions). Ten offline missions give kids a question and a set of clues to investigate. Take turns reading the filled-in prompt and answering it. Change a clue in a remix and see which parts of the answer change with it.

In **Catch the sticker machine’s rule**, two rules explain the same first results. Ask the chain to find a card the rules would treat differently, then have a partner run the machine in secret. Talk about what that card tells you and what you still need to test.

## Make something to show at home

Choose [Make something to show at home](/studio/practice#make-at-home) from Home. Each challenge works offline. Fix the draft, see your words in the next prompt, and compare your idea with the example. Then make something you can share with a parent or caregiver.

| Challenge | What to try at home |
| --- | --- |
| [Make a game for family night](/studio/practice#family-game) | Teach a five-minute drawing game with one sheet of paper and one pencil. |
| [Turn a memory into a comic](/studio/practice#memory-comic) | Draw four panels about a funny pancake flip or a moment of your own. |
| [Invent a fix for home](/studio/practice#home-invention) | Sketch a paper pencil tray, pitch the idea, and test it with two pencils. |

The completed challenge links to its editable recipe if you want to use live AI for a project of your own. Those recipes use the studio’s [live model setup](SETUP-AND-MODELS.md).

## Try a case for adults

Open [Professional practice](/studio/practice/professional) and choose a decision memo, evidence brief, or document review. These fictional source packets include a deliberately flawed second answer. Correct it using the packet, preview the next prompt, and compare your fix with the reference answer. You can export the run or return to it from **My library**.

## Run the offline smoke checks

From the repository folder:

```bash
./verify_demos.sh
```

This exercises the authored Moon trace, the classroom challenges, the professional cases, and a two-step portable framework example with a fixed local callable. It checks the prompt handoffs and exits with a failure if a fixture does not complete. It starts no server, sends no requests, and does not write to the workspace. [Verification](TESTING.md) covers the separate test groups.

## Choose a live demo deliberately

The scripts in `demos/` show the earlier portable framework. Many examples send multiple paid requests or write logs and artifacts. Read a script’s inputs, call plan, and output paths before choosing an individual example. A timed-out or interrupted request may still appear in provider usage. The interactive scripts can save partial framework artifacts; use the workbench when you need a resumable trace.

For a bounded comparison, choose this single live case. It can send up to seven requests, five for the scientific-method pattern, one for the baseline, and one for the rubric judge.

```bash
.venv/bin/python demos/emergence_measurement_demo.py --demo 2 --live
```

Read the result as the judge model’s assessment of those excerpts. Collect evidence separately when you need to verify a claim. [Comparison contract](ADVANCED-TOOLS.md#execution-limits-and-comparison-records)

[Earlier demo notes](LEGACY-DEMOS.md) describe a previous interface and include unverified historical claims. Use this page for current steps.
