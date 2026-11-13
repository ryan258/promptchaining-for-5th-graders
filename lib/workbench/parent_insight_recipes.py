"""Editable chains that help caregivers learn from everyday observations."""

from .models import Recipe, Step


PARENT_INSIGHT_INPUT_HINTS: dict[str, str] = {
    "morning-bottleneck": "Describe two rushed mornings and one smoother one. Include when you meant to leave.",
    "homework-start": "Describe where homework stalled, when starting was easier, and anything your child said helped.",
    "small-spending-pattern": "List a few small purchases, what they cost, and what was happening when you made them.",
    "share-the-remembering": "Pick a recurring job. Say who notices, plans, does, and checks it.",
    "recurring-argument": "Describe a few times the same disagreement came up and a time it went more smoothly.",
    "make-room-this-week": "List what you could do, the time you really have, and any promises you need to keep.",
    "protect-weekend-rest": "Say when you hoped to have a break, what interrupted it, and when you did get a break.",
    "follow-their-interest": "Share what your child chose, returned to, or asked about. Include an option they passed up.",
    "stress-test-a-family-rule": "Share one rule, what it’s meant to help, and two moments when it was hard to follow.",
    "shared-space-reset": "Describe a shared space, where things end up, and where people look for them.",
}


PARENT_INSIGHT_RECIPE_EXAMPLES: dict[str, tuple[str, str]] = {
    "morning-bottleneck": (
        "Try three school mornings",
        "We aim to leave at 7:50. Monday breakfast ended at 7:40, but we searched for a signed form "
        "and left at 7:59. Tuesday the form was ready, but we searched for sneakers and left at 7:57. "
        "Wednesday breakfast still ended at 7:40. Shoes and bags were by the door and we left at 7:49. "
        "There’s room by the door for one basket. I can spend two minutes setting up the night before.",
    ),
    "homework-start": (
        "Try a hard-to-start assignment",
        "Monday and Tuesday, my child took about 15 minutes to begin a short writing assignment. "
        "They said, “I can’t pick what to write about.” They started math in a few minutes. "
        "On Thursday they chose a topic out loud before opening the notebook and began writing right away. "
        "The assignments differed. We have five minutes to get started together after snack.",
    ),
    "small-spending-pattern": (
        "Try a week of snack stops",
        "Last week I bought a $4 snack after practice on Monday, Wednesday, and Thursday. Each time, "
        "we’d left home without food and had a 30-minute wait for the bus. On Tuesday I brought crackers "
        "and skipped the stop. Friday we chose to share a $5 pastry with a friend, which I’d do again. "
        "I already have a small reusable snack container.",
    ),
    "share-the-remembering": (
        "Try sharing library returns",
        "One adult checks when books are due, gathers them from two rooms, puts them in a tote, and "
        "texts a reminder. The other adult walks past the library on Saturdays and usually drops off the "
        "books after the text. Twice we forgot to collect a book from upstairs. Both adults can check the "
        "library account. We haven’t agreed on who will keep track next week.",
    ),
    "recurring-argument": (
        "Try a quieter ride home",
        "On two rides home from practice I asked how things went as soon as we got in the car. "
        "My child said, “Can you stop asking?” and the conversation got tense. On Friday I waited "
        "until we got home and they started telling me about a drill. I want to stay connected. "
        "I haven’t asked when they’d like to talk.",
    ),
    "make-room-this-week": (
        "Try three jobs and 45 minutes",
        "I have 45 minutes free before Sunday. I promised a neighbor I’d mend a costume seam for "
        "Saturday and it should take 25 minutes. I’d also like to sort a box for a swap that happens "
        "again next month, about 40 minutes. I offered to help with a party poster, about 30 minutes, "
        "but I haven’t confirmed. I could send a few layout ideas in 10 minutes instead.",
    ),
    "protect-weekend-rest": (
        "Try finding a real break",
        "I wanted half an hour to read on Sunday. I had an open hour, but kept stopping to find school "
        "supplies, answer questions about Monday, and start laundry. On Saturday I read for 35 minutes "
        "while another adult handled questions after we agreed on it. They’re only available after "
        "lunch next Sunday. The laundry could wait until later.",
    ),
    "follow-their-interest": (
        "Try the child who keeps drawing maps",
        "My child spent 20 minutes drawing a treasure map, then came back the next day to add a key. "
        "On a walk they asked if we could mark where the ducks gather. They finished a coloring sheet "
        "when I invited them but didn’t choose another one. We have ten free minutes Saturday and "
        "already have paper and pencils.",
    ),
    "stress-test-a-family-rule": (
        "Try an after-dinner device rule",
        "Our rule is “Devices away after dinner.” We want a little time together before everyone splits "
        "up. It worked on Monday. Tuesday someone needed to confirm a ride by text. Thursday a child "
        "needed to look up one fact for a school project. Both times the rule turned into a long debate. "
        "We haven’t agreed on what should count as a quick exception.",
    ),
    "shared-space-reset": (
        "Try the art shelf that jams up",
        "Pencils usually go back in a cup right next to the paper. Clean sheets and scraps end up "
        "mixed in the same tray. Twice this week a child pulled out a whole stack to find a clean "
        "sheet. There’s a second shallow tray we already own and space for it on the same low shelf. "
        "Everyone uses the art supplies and we want kids to find and put them back on their own.",
    ),
}


_SOURCE_NOTES = "\n\nMy notes\n{{topic}}\n\nExtra details\n{{context}}"


PARENT_INSIGHT_RECIPES: dict[str, Recipe] = {
    "morning-bottleneck": Recipe(
        title="Find what slows the morning",
        description="Compare rushed and smoother mornings to find one delay you can test changing.",
        audience="The people getting out the door together",
        steps=[
            Step(
                name="Lay out the mornings",
                purpose="See where the time went and what was different on the smoother day.",
                prompt=(
                    "Make a table of facts from my notes. For each morning, list the planned and actual "
                    "departure, what was ready, and any search or wait. If breakfast end is mentioned, "
                    "include a breakfast-end column for every morning. Use only details stated for that "
                    "morning and mark every unstated entry Unknown. A search that goes unmentioned is Unknown. "
                    "List the missing details separately. Record any time or materials available for a future "
                    "trial under Trial constraints. Finish with those constraints."
                    + _SOURCE_NOTES
                ),
            ),
            Step(
                name="Find the likely bottleneck",
                purpose="Check whether the thing you’d fix is the thing that delayed leaving.",
                prompt=(
                    "Check the reviewed timeline against my original notes. Use headings Facts, Unknown, "
                    "Hypotheses, and Trial change. Include a fact only when I stated it in the notes or "
                    "explicitly confirmed it in a correction. Keep an unreported breakfast time or search "
                    "under Unknown. Phrase unreported events as open questions about whether they happened. "
                    "A setup allowance describes a future trial. Under Hypotheses, give two tentative "
                    "explanations for the observed departures. Say what observation would help check each. "
                    "Choose one small change that fits the time and supplies in the notes."
                    "\n\nReviewed timelines\n{{output[-1]}}"
                    + _SOURCE_NOTES
                ),
            ),
            Step(
                name="Make a three-morning trial",
                purpose="Change one thing and learn whether it helped.",
                prompt=(
                    "Make a short plan for {{audience}} with four headings: Facts from the notes, Unknown, "
                    "Hypotheses, and Three-morning trial. Check every fact against my notes or a correction "
                    "I explicitly confirmed. Copy the recorded times as given. Keep missing breakfast times "
                    "and unreported searches visible under Unknown. Under Hypotheses, say what might explain "
                    "the departure pattern. In the trial, describe one change and when to set it up. Leave "
                    "three blank rows for recording whether the suspected delay happened and when we left. "
                    "Use the stated departure goal to describe what would make the change worth keeping. "
                    "Report what the trial could still leave uncertain."
                    "\n\nReviewed bottleneck and change\n{{output[-1]}}"
                    + _SOURCE_NOTES
                ),
            ),
        ],
    ),
    "homework-start": Recipe(
        title="Find where homework gets stuck",
        description="Compare hard and easy starts to find one way to help a child begin their own work.",
        audience="A caregiver getting homework started with their child",
        steps=[
            Step(
                name="Find the first hard part",
                purpose="See exactly where the child stopped or asked for help.",
                prompt=(
                    "Use my notes as source material. For each assignment, identify the first move it "
                    "asked for and what my child did or said before beginning. Separate difficulty "
                    "starting from difficulty with the work itself. Compare the slower and easier "
                    "starts and mark differences between the assignments that could affect the comparison. "
                    "Carry forward when and how much time we have to try a change."
                    + _SOURCE_NOTES
                ),
            ),
            Step(
                name="Choose one small support",
                purpose="Target the first hard move and leave the thinking with the child.",
                prompt=(
                    "Use the reviewed comparison to name one possible hurdle and the observation behind "
                    "it. Give one brief support that helps my child take the first move independently. "
                    "Write the question I could ask and how my child could choose whether to try it. "
                    "State what we still need to learn about what helps them."
                    "\n\nReviewed comparison\n{{output[-1]}}"
                ),
            ),
            Step(
                name="Make a homework kickoff",
                purpose="Try one line out loud and notice what the child does next.",
                prompt=(
                    "Write a short kickoff for {{audience}} to use on the next similar assignment. "
                    "Keep my reviewed wording and corrections. Give the question, a short way to "
                    "wait while the child takes the lead, and one observation to write down after. "
                    "End with a question I can ask my child about what helped."
                    "\n\nReviewed hurdle and support\n{{output[-1]}}"
                ),
            ),
        ],
    ),
    "small-spending-pattern": Recipe(
        title="Find the repeat behind small purchases",
        description="See which purchases fill a recurring gap and try a low-effort alternative.",
        audience="A caregiver looking at a short list of everyday purchases",
        steps=[
            Step(
                name="Sort the actual purchases",
                purpose="Keep the purchases you valued visible as you look for a repeat.",
                prompt=(
                    "Use my notes as source material. Make a short list of each purchase, its stated "
                    "cost, the situation, and what it was for. Group similar situations and total only "
                    "the amounts actually given for the same period. Mark unknown prices and distinguish "
                    "purchases I said I valued from ones I’m questioning. Include occasions where the "
                    "same need came up without a purchase, and any alternatives I already have."
                    + _SOURCE_NOTES
                ),
            ),
            Step(
                name="Look for the recurring gap",
                purpose="Find a specific moment where a different option might meet the same need.",
                prompt=(
                    "Use the reviewed purchases to identify one repeatable situation and what need the "
                    "purchase met in that moment. Cite a purchase and a contrasting occasion if given. "
                    "Suggest a small alternative using something I already have or can do. Keep any "
                    "purchases I chose to keep and flag if the sample is too small to tell."
                    "\n\nReviewed purchases and situations\n{{output[-1]}}"
                ),
            ),
            Step(
                name="Write a one-week check",
                purpose="Find out whether the alternative works when the same situation comes up.",
                prompt=(
                    "Make a one-week check for {{audience}} that keeps my confirmed numbers and choices. "
                    "Give an if-then plan for the repeat situation and a simple way to note whether the "
                    "alternative met the need. Include a place to note any actual cost. Use observed "
                    "amounts for comparisons and say what one week can tell me."
                    "\n\nReviewed purchases\n{{output[-2]}}\n\nReviewed pattern and alternative\n{{output[-1]}}"
                ),
            ),
        ],
    ),
    "share-the-remembering": Recipe(
        title="Share the work of remembering",
        description="Find who has to notice, plan, do, and follow up on a recurring job, then try one handoff.",
        audience="The people who share this household job",
        steps=[
            Step(
                name="Map the job from start to finish",
                purpose="Make the reminders and follow-up as visible as the task itself.",
                prompt=(
                    "Use my notes as source material. Map how the job starts, gets planned, gets done, "
                    "and gets checked. Mark who does each part when the notes say. Identify any point "
                    "where one person depends on another to remember or send a reminder. Label unknown "
                    "parts so we can fill them in. Keep any stated access to tools or information."
                    + _SOURCE_NOTES
                ),
            ),
            Step(
                name="Find a whole piece to hand over",
                purpose="See whether the handoff can include the reminder and follow-up.",
                prompt=(
                    "Use the reviewed map to propose moving one coherent piece of the job. Identify "
                    "the trigger, what that person needs access to, and how they would know it’s "
                    "done. Point to the repeat reminder the change could remove. Frame the change "
                    "as a proposal and flag what needs agreement."
                    "\n\nReviewed job map\n{{output[-1]}}"
                ),
            ),
            Step(
                name="Draft the handoff for a conversation",
                purpose="Make it easy for both people to see what they are trying.",
                prompt=(
                    "Write a short proposed handoff for {{audience}}. Keep any roles and corrections I "
                    "confirmed. Include who will do the piece, the trigger, the finish line, what "
                    "support is needed, and when to check whether reminders dropped. Mark unconfirmed "
                    "ownership as a question to ask before trying it."
                    "\n\nReviewed handoff proposal\n{{output[-1]}}"
                ),
            ),
        ],
    ),
    "recurring-argument": Recipe(
        title="Change the moment an argument starts",
        description="Compare a repeated disagreement with a calmer moment and find a different opening.",
        audience="A caregiver looking for a better way to start a family conversation",
        steps=[
            Step(
                name="Look at what happened just before",
                purpose="Find the point where the conversations began to go differently.",
                prompt=(
                    "Use my notes as source material. Put each example in order: what happened just "
                    "before the disagreement, what each person said or did, and what happened next. "
                    "Compare a calmer example if given. Separate what people said they wanted from "
                    "possible interpretations, and mark whose perspective is missing. Keep the goal "
                    "I want to work toward."
                    + _SOURCE_NOTES
                ),
            ),
            Step(
                name="Try two ways to read the moment",
                purpose="Check your reading of the situation with a question the other person can answer.",
                prompt=(
                    "From the reviewed comparison, give two plausible readings of the repeated moment. "
                    "For each, name the observed clue and what’s still unknown. Propose a different "
                    "opening I control, with room for the other person to say what would work for "
                    "them. Keep the needs people stated in their own words where useful."
                    "\n\nReviewed comparison\n{{output[-1]}}"
                ),
            ),
            Step(
                name="Draft a different opening",
                purpose="Try one short line at a calmer moment.",
                prompt=(
                    "Give {{audience}} one short opening, a genuine question to check what the other "
                    "person needs, and one small change to try if they’re open to it. Keep my reviewed "
                    "wording and confirmed observations. Add one thing to notice next time that would "
                    "tell me whether the opening changed the conversation."
                    "\n\nReviewed readings and opening\n{{output[-1]}}"
                ),
            ),
        ],
    ),
    "make-room-this-week": Recipe(
        title="Choose what to take off the list",
        description="Compare the real cost of a few commitments and decide what to keep, shrink, or pause.",
        audience="A caregiver deciding how much to take on",
        steps=[
            Step(
                name="Check what each commitment costs",
                purpose="Count the time and find out who is counting on you.",
                prompt=(
                    "Use my notes as source material. List each item, its stated time including setup "
                    "or travel if given, its deadline, and who is counting on it. Separate confirmed "
                    "promises from optional work. Note what each item makes possible, the total time "
                    "I have, and any smaller version already mentioned. Leave time estimates blank "
                    "where I haven’t supplied them."
                    + _SOURCE_NOTES
                ),
            ),
            Step(
                name="Compare two realistic versions",
                purpose="See what each version makes room for and what it gives up.",
                prompt=(
                    "Use the reviewed list to sketch two versions that fit the time I have where the "
                    "numbers allow it. Keep fixed promises unless I say they can change. In each version, "
                    "name one thing to keep, shrink, or pause and who would need a heads-up. Compare "
                    "what each version protects and what it costs. Make missing information visible."
                    "\n\nReviewed commitments and time\n{{output[-1]}}"
                ),
            ),
            Step(
                name="Write down the decision",
                purpose="Keep one clear plan and a line you can use if someone needs an update.",
                prompt=(
                    "Make a short keep, shrink, or pause list for {{audience}}. Use the reviewed "
                    "decision and confirmed corrections. If I haven’t picked a version, mark the "
                    "best fit as a proposal with the tradeoff that matters most. Include one draft "
                    "message for any person affected and a point to revisit a paused item."
                    "\n\nReviewed versions and choice\n{{output[-1]}}"
                ),
            ),
        ],
    ),
    "protect-weekend-rest": Recipe(
        title="Find a break that stays a break",
        description="See what interrupts downtime and set up one block you can actually use.",
        audience="A caregiver who wants a short uninterrupted break",
        steps=[
            Step(
                name="Trace the interruptions",
                purpose="See where open time turned into time spent on something else.",
                prompt=(
                    "Use my notes as source material. Compare the break I planned, what actually "
                    "happened, and any break that worked. For each interruption, capture what triggered "
                    "it and whether the notes say it could wait, move earlier, or go to someone else. "
                    "Keep the break length I want, any fixed obligations, and when help is available "
                    "or still to be confirmed."
                    + _SOURCE_NOTES
                ),
            ),
            Step(
                name="Find what protected the better break",
                purpose="Choose one condition you can try setting up again.",
                prompt=(
                    "Use the reviewed examples to identify the strongest candidate for what made "
                    "the better break possible. If there’s no good comparison, name a likely "
                    "interruption to test. Pick one available block and one practical change that "
                    "could protect it. Use the stated availability and keep help tentative until confirmed."
                    "\n\nReviewed breaks and interruptions\n{{output[-1]}}"
                ),
            ),
            Step(
                name="Make a small plan for next weekend",
                purpose="Choose a block, one thing to move, and a way to tell if it worked.",
                prompt=(
                    "Write a compact break plan for {{audience}}. Use my reviewed choice and corrections. "
                    "Include the block, what to set up or ask beforehand, what can wait, and a shorter "
                    "fallback that still gives me time to myself. End with one check: how many "
                    "uninterrupted minutes I actually got and what interrupted the block, if anything."
                    "\n\nReviewed breaks and interruptions\n{{output[-2]}}\n\nReviewed plan\n{{output[-1]}}"
                ),
            ),
        ],
    ),
    "follow-their-interest": Recipe(
        title="Follow an interest they chose",
        description="Notice what a child returns to on their own and offer a small next thing to try.",
        audience="A caregiver offering a child a choice of what to explore",
        steps=[
            Step(
                name="Collect the choices they made",
                purpose="Look for moments when they chose, returned to, or extended an activity.",
                prompt=(
                    "Use my notes as source material. Pull out specific actions or questions that "
                    "the child chose, repeated, or expanded. Note when something happened after "
                    "an invitation, requirement, or suggestion. Put observed choices next to "
                    "anything they passed up, without guessing why. Keep the available time and materials."
                    + _SOURCE_NOTES
                ),
            ),
            Step(
                name="Try two possible explanations",
                purpose="Get more specific about which part of the activity may have caught their attention.",
                prompt=(
                    "Use the reviewed observations to suggest two different features that might "
                    "interest the child. Cite a choice for each. Suggest two short things to try "
                    "that make those features different enough to notice. Use the time and materials "
                    "we have. Give the child room to choose, combine the options, or pass."
                    "\n\nReviewed choices and questions\n{{output[-1]}}"
                ),
            ),
            Step(
                name="Write an invitation",
                purpose="Offer the choice and notice which part they actually take up.",
                prompt=(
                    "Give {{audience}} a two-option invitation they can say out loud and a short "
                    "note about what to look for afterward. Keep the options and corrections I "
                    "reviewed. Focus on which part the child chooses, changes, or returns to. "
                    "Leave their longer-term interests open."
                    "\n\nReviewed possible interests and options\n{{output[-1]}}"
                ),
            ),
        ],
    ),
    "stress-test-a-family-rule": Recipe(
        title="See where a family rule breaks down",
        description="Try a rule on an ordinary day and two tricky cases before deciding what to change.",
        audience="A household discussing a rule together",
        steps=[
            Step(
                name="Find the job the rule does",
                purpose="Separate what the rule is meant to help from the words it uses now.",
                prompt=(
                    "Use my notes as source material. Write the rule as given, its stated purpose, "
                    "and the examples where it worked or was hard to follow. Identify exactly "
                    "what was unclear in each hard example. Distinguish concerns people stated "
                    "from ones we’d need to ask about."
                    + _SOURCE_NOTES
                ),
            ),
            Step(
                name="Try the rule on each case",
                purpose="See if a narrower exception solves the problem and still serves the goal.",
                prompt=(
                    "Use the reviewed cases to compare the current rule with one clearer version. "
                    "Say what each would ask someone to do on the ordinary day and in each tricky "
                    "case. For any exception, define when it starts, when it ends, and how to "
                    "get back to the usual routine. Flag any situation the revision still leaves open."
                    "\n\nReviewed rule, purpose, and cases\n{{output[-1]}}"
                ),
            ),
            Step(
                name="Make a one-week rule to try",
                purpose="Give everyone a way to understand the same rule and offer a correction.",
                prompt=(
                    "Write a proposed one-week rule for {{audience}} using my reviewed wording and "
                    "confirmed corrections. Include the rule, its purpose in one line, and one "
                    "example of when and how an exception ends. Give one question to ask the "
                    "household before trying it and one observation for the review at week’s end."
                    "\n\nReviewed comparison and revision\n{{output[-1]}}"
                ),
            ),
        ],
    ),
    "shared-space-reset": Recipe(
        title="Make a shared space easier to use",
        description="See where things are easiest to grab and hardest to return, then change one spot.",
        audience="The family members who use a shared space",
        steps=[
            Step(
                name="Follow the objects",
                purpose="Compare where things are kept, used, looked for, and put back.",
                prompt=(
                    "Use my notes as source material. For each object or group of objects, trace "
                    "where it starts, where it gets used, and where it actually ends up. Mark "
                    "which part takes a search or a second move. Compare an item people return "
                    "easily with one they struggle to find or put away. Keep what’s available and any "
                    "constraints on where we can put things."
                    + _SOURCE_NOTES
                ),
            ),
            Step(
                name="Change one part of the path",
                purpose="Make the easier action available at the point where people need it.",
                prompt=(
                    "Use the reviewed object paths to identify one likely source of friction. Pick "
                    "one small move, separation, or visible cue using materials we have. Say how "
                    "it would make finding or returning the item easier for the people who use "
                    "it. Point to the observation it addresses and any guess to check."
                    "\n\nReviewed object paths\n{{output[-1]}}"
                ),
            ),
            Step(
                name="Set up and watch three uses",
                purpose="Find out whether the new spot works before rearranging the rest.",
                prompt=(
                    "Write a brief setup and trial for {{audience}}. Keep my reviewed location, "
                    "materials, and confirmed corrections. Show where the item goes, what someone "
                    "will see when they look for it, and what to watch on the next three uses. "
                    "Say what would make us keep or adjust the change."
                    "\n\nReviewed change and reason\n{{output[-1]}}"
                ),
            ),
        ],
    ),
}
