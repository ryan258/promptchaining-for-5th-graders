# Worked examples

These walkthroughs show how to use the app, what to enter, and where to apply your judgment. The Moon walkthrough uses the app's fixed authored answers. The other inputs and suggested edits are author-written examples, not transcripts of live model runs.

[Documentation index](README.md) · [Recipe choices](RECIPE-GUIDE.md) · [Build a reusable method](CHAIN-BUILDING.md)

## 1. See a whole chain without a key

**Leave with:** an understanding of how a prompt carries an earlier answer into the next step.

Start the app with `./pc`, open the workbench, and choose **Explore the Moon example**. You will see the Moon question as a completed, authored run. Opening it makes no provider request.

Read the final explanation, then open the four saved steps under **How it got there**:

| Step | What to notice |
| --- | --- |
| **Find the pieces** | It names the pieces of the explanation and a misconception to avoid. |
| **Build an analogy** | Its sent prompt includes the first answer. Its own answer explains both the analogy and its limits. |
| **Try it out** | Its prompt draws on both earlier answers to build a concrete activity. |
| **Make it click** | Its prompt combines all three previous answers into a self-contained explanation. |

Inside each step, open **Prompt that produced this answer**. These are rendered prompts, so you can inspect what was carried forward without decoding placeholders.

Choose **Copy final answer** or **Download final answer** to take the explanation. **Download trace** includes the prompts and answers in Markdown. **Download run JSON** saves the record for restore. Opening the Moon example again reuses the existing sample run.

**Use this recipe again** opens an editable recipe with the topic and context. A live version needs configured credentials and an explicit start. It will not reproduce the authored text exactly.

## 2. Turn rough notes into a short draft

**Leave with:** a draft that uses actual notes and identifies remaining fact checks.

Choose **Recipes → From thought to draft**.

**What would you like to work on?**

```text
Draft a short post about keeping useful methods alongside finished work.
```

**Who is it for?**

```text
Someone interested in practical ways AI can reduce repeated effort.
```

**Anything it should know?**

```text
Target about 350 words. Use plain, warm language.
Do not invent my experiences, quotes, statistics or examples.
My actual notes:
[Dictate or paste the notes you want to use here.]
Mark missing facts [verify].
```

Replace the bracketed instruction with your actual notes before preparing a run. Keep review pauses selected, name the recipe `Short post — my notes, plain language`, and save it if you want to reuse this setup.

Prepare the chain and preview its first prompt. Then run the first step.

| After this step | Your review job |
| --- | --- |
| **Find the point** | Check whether the central point is yours. Revise the latest answer if the outline goes in a different direction. |
| **Write the draft** | Check for invented personal details or facts. At this pause, the draft is still the latest editable answer. |
| **Read it critically** | Check whether the critique proposes useful structural changes and catches unsupported claims. Correct misleading advice before continuing. |
| **Make it ready to review** | Read the complete result and the remaining fact-check notes. Choose what you want to keep. |

The final revision references the draft and critique. Correcting the draft before the critique helps keep later work focused. If the run already continued, use **Fork after this step** at the draft checkpoint to try another revision and keep the original run.

Use **Copy final answer** to move the result into your writing tool. This chain does not publish it, edit another repository, or independently verify the facts. Save a new recipe copy when a change to the method makes the next writing session easier.

## 3. Find one manageable action from a friction point

**Leave with:** a small test you can try, with a way to judge whether it helped.

Choose **Untangle a problem**.

**Topic**

```text
I reopen old drafts because I forget which file is current.
```

**Audience**

```text
Me; prioritise low typing and easy resumption.
```

**Context**

```text
What I have observed: I sometimes create several named copies, then forget
which copy I was working on. I already have a project folder. I want one
change using what I have. The cause is not established. Do not turn this
into a complete productivity system.
```

At **See what's happening**, correct any invented diagnosis or obligation. At **Look underneath**, ask whether the suggested causes could actually be checked. A confident story about the cause is still a hypothesis.

If the answer proposes too much, edit the latest answer so that it preserves one plausible cause and a simple observation. Preview the next prompt to confirm that this revision is the material **Try one change** will use.

Read the final action as a proposal. Decide whether it fits your tools and effort. The point of the run is to help you choose a test; the app does not reorganise files or perform the proposed action.

Keep the completed run in **My library** as a record of the reasoning. A later run can use your actual observations as context, so the next round works from what happened rather than an imagined success.

## 4. Learn one small thing, then practise it

**Leave with:** a short path and a first lesson you can use immediately.

Choose **Build a learning path**.

**Topic**

```text
Learn enough about Python dictionaries to read and change a small configuration.
```

**Audience:** `Me; I understand variables and lists.`

**Context**

```text
Keep examples short enough to read without running software. Explain one new
idea at a time. The first practice task should take only a few minutes. Ask
for an explanation in my own words as well as a proposed answer.
```

After **Find the starting point**, check that the prerequisites match your actual knowledge. After **Map the path**, check that the first lesson serves the goal. Narrow an overly broad curriculum while it is still the latest answer.

After **Teach the first lesson**, try the practice question before reading its suggested answer. Ask yourself whether you can explain why an example works. The model's answer is a useful comparison to inspect, not a checked grading key.

To continue later, open the run from **My library**, choose **Use this recipe again**, and change the topic to the next lesson. Put what you learned and what remains confusing into context. The app keeps runs; it does not automatically advance through a curriculum.

## 5. Make the successful workflow shorter next time

After any of these examples:

1. Identify the instruction that reduced your work: audience, context, a prompt, desired output form, or review pace.
2. Open **Use this recipe again** and keep those stable parts.
3. Give the recipe a recognisable name and choose **Save recipe**.
4. Next time, open that saved recipe and dictate only the new topic or changed notes.

Saving makes a copy and keeps its starting inputs. It does not create an automation or schedule future provider requests.

For a complete custom method you can paste into three steps, use [Build your own chains](CHAIN-BUILDING.md).

To practice correcting a saved answer without a provider key, use the [professional practice cases](PROFESSIONAL-CASES.md).
