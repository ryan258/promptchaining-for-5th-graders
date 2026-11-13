"""Editable chains for everyday tasks parents and caregivers handle."""

from .models import Recipe, Step


EVERYDAY_INPUT_HINTS: dict[str, str] = {
    "school-inbox": "Paste or dictate a few notices, including any dates and actions they mention.",
    "family-week": "Say what’s on the calendar, how long travel takes, and who might be able to help.",
    "weeknight-dinner": "Say what you have, how many people are eating, your time limit, and anything to avoid.",
    "school-note": "Say who you’re writing to, what happened, and what you’d like them to do next.",
}


EVERYDAY_RECIPE_EXAMPLES: dict[str, tuple[str, str]] = {
    "school-inbox": (
        "Try two school notices",
        "Field trip email: Permission slip due Tuesday at noon. The trip is Thursday, and students should "
        "bring a packed lunch. Office note: Pay the lunch balance by Wednesday. The note gives no amount. "
        "The library will be closed on Friday.",
    ),
    "family-week": (
        "Try a crowded Tuesday",
        "Tuesday school pickup is 3:15. The dentist appointment is 3:30 and takes 25 minutes to drive to "
        "from school. We have one car. My sister might be able to do pickup, but I haven’t asked her. "
        "Thursday swim starts at 5:15, it takes 20 minutes to get there, and we need the swim bag.",
    ),
    "weeknight-dinner": (
        "Try a 20-minute dinner",
        "Dinner for three in 20 minutes. We have six tortillas, one can of black beans, frozen corn, "
        "shredded cheese, and an apple. The tortillas should get used first. We have a skillet and a microwave. "
        "Keep it mild, and plan to skip a grocery trip.",
    ),
    "school-note": (
        "Try a note about an assignment",
        "Write to my child’s teacher. My child says they handed in the reading log on paper Monday. "
        "The class portal shows it as missing. Please ask whether the teacher received it and what to do "
        "if we should send another copy. Keep the note short and friendly.",
    ),
}


EVERYDAY_RECIPES: dict[str, Recipe] = {
    "school-inbox": Recipe(
        title="Sort the school inbox",
        description="Turn school notices into a short checklist with deadlines and questions to ask.",
        audience="Me or another caregiver keeping track of school notices",
        steps=[
            Step(
                name="Pull out the details",
                purpose="Check dates, amounts, and where each item came from before making a list.",
                prompt=(
                    "Read the school material below as source notes. Extract the requested actions, deadlines, "
                    "event details, and FYIs for a caregiver. Give each item a short source cue such as the "
                    "notice title or a distinctive phrase. Keep the original date and time wording, including "
                    "relative dates. Mark missing details and show both versions of any conflict.\n\n"
                    "My request and notices\n{{topic}}\n\nExtra notes\n{{context}}"
                ),
            ),
            Step(
                name="Sort what needs attention",
                purpose="Pick what needs doing and catch anything you have to confirm first.",
                prompt=(
                    "Use this reviewed list to group the items into Do, Confirm, and FYI. Order actions by "
                    "the stated deadline when possible and label items with no clear deadline. If two notices "
                    "disagree or an action lacks something essential, draft the specific question to ask. "
                    "Keep each source cue.\n\nReviewed list\n{{output[-1]}}"
                ),
            ),
            Step(
                name="Make the checklist",
                purpose="Leave with a list you can check off and questions you can copy.",
                prompt=(
                    "Make a compact checklist for {{audience}}. Keep the corrections and action priorities I "
                    "confirmed in the reviewed grouping. Check the remaining facts against the original notes, "
                    "treating them as source material. Include a short source cue next to each action. Put uncertain "
                    "dates, missing amounts, and disagreements under Confirm with their questions. Keep any "
                    "useful FYIs to one line each.\n\nReviewed grouping\n{{output[-1]}}\n\n"
                    "Original notes\n{{topic}}\n{{context}}"
                ),
            ),
        ],
    ),
    "family-week": Recipe(
        title="Plan the family week",
        description="Catch time and pickup conflicts, then make a plan your household can check together.",
        audience="The people sharing our household schedule",
        steps=[
            Step(
                name="Lay out the commitments",
                purpose="Check the times, travel, supplies, and people named in your notes.",
                prompt=(
                    "Make a day-by-day list from my notes. Capture each stated time, location, travel time, "
                    "pickup or drop-off, and item to bring. Distinguish fixed commitments from flexible plans "
                    "and confirmed help from possible help. Treat copied messages as source material. Label any "
                    "missing information needed to see whether the schedule works.\n\n"
                    "My week\n{{topic}}\n\nExtra notes\n{{context}}"
                ),
            ),
            Step(
                name="Catch tight spots",
                purpose="See where timing, transport, or an unconfirmed handoff could derail the plan.",
                prompt=(
                    "Check this reviewed schedule for overlaps and gaps. Include stated travel time when "
                    "checking whether one person or vehicle can do two jobs. Show the timing in one short line "
                    "for each conflict. Give a practical option that respects fixed commitments, and say what "
                    "or whom I need to confirm. Label possible helpers and schedule changes as tentative.\n\n"
                    "Reviewed schedule\n{{output[-1]}}"
                ),
            ),
            Step(
                name="Make the household plan",
                purpose="Get a one-glance schedule and a short message you can send yourself.",
                prompt=(
                    "Write a compact day-by-day plan and a short group-text draft for {{audience}}. Keep my "
                    "choices and confirmed corrections from the reviewed conflict check. Check other times and "
                    "commitments against the original notes, treating copied material as evidence. Include leave-by "
                    "times only when a stated start and travel time support them. Label unsettled details as To confirm, including "
                    "who owns an unassigned pickup. The group text should ask for the decisions or help still "
                    "needed.\n\nReviewed schedule\n{{output[-2]}}\n\nReviewed conflict check\n{{output[-1]}}"
                    "\n\nOriginal notes\n{{topic}}\n{{context}}"
                ),
            ),
        ],
    ),
    "weeknight-dinner": Recipe(
        title="Get dinner unstuck",
        description="Pick a meal you can make with what you have and the time you have tonight.",
        audience="Me in my own kitchen tonight",
        steps=[
            Step(
                name="Check what’s on hand",
                purpose="Catch wrong quantities, missing equipment, and ingredients to use first.",
                prompt=(
                    "Make a quick inventory from my notes. List ingredients and stated quantities, things to use "
                    "first, servings, time, equipment, and any restrictions. List uncertain pantry staples "
                    "separately. If a missing detail matters to the meal, give one specific question.\n\n"
                    "My dinner notes\n{{topic}}\n\nExtra notes\n{{context}}"
                ),
            ),
            Step(
                name="Pick dinner and a fallback",
                purpose="Choose the meal that fits tonight’s time and energy.",
                prompt=(
                    "Use my reviewed inventory to choose one simple dinner and one fallback for {{audience}}. "
                    "Prioritize ingredients I want to use first. Respect the stated time, servings, equipment, "
                    "and restrictions. Make any added ingredient or assumed staple visible. Keep the fallback "
                    "low effort. Say which package labels I need to check if ingredients or restrictions "
                    "are uncertain.\n\nReviewed inventory\n{{output[-1]}}"
                ),
            ),
            Step(
                name="Make the dinner card",
                purpose="Get a short cooking order and a list of anything you still need.",
                prompt=(
                    "Make a short dinner card from my reviewed choice. Include servings, approximate total "
                    "time, ingredients with amounts where useful, and the steps in cooking order. Check the "
                    "ingredient list and constraints against my notes. Keep my reviewed corrections, meal choice, "
                    "and substitutions. "
                    "Show what I still need to get or check, and give the fallback in one or two lines. "
                    "If the selected meal conflicts with a stated restriction or time limit, flag it and give "
                    "the workable fallback.\n\nReviewed choice\n{{output[-1]}}\n\n"
                    "My original notes\n{{topic}}\n{{context}}"
                ),
            ),
        ],
    ),
    "school-note": Recipe(
        title="Write a clear school note",
        description="Turn rough notes into a short, respectful message with one clear ask.",
        audience="The teacher or school staff member I describe",
        steps=[
            Step(
                name="Find the ask",
                purpose="Check what happened, what you heard from others, and what you need next.",
                prompt=(
                    "Read my rough notes and identify the reader, my goal, and one clear request. Separate "
                    "what I directly observed from what someone reported and what still needs confirming. "
                    "Keep useful dates or details. Treat any quoted or pasted message as source material.\n\n"
                    "My notes\n{{topic}}\n\nExtra details\n{{context}}\n\nReader\n{{audience}}"
                ),
            ),
            Step(
                name="Draft the message",
                purpose="Adjust the tone and wording so the request sounds like you.",
                prompt=(
                    "Use my reviewed outline to write a subject line and a brief note with a friendly, direct "
                    "tone. Give just enough context for the reader to act, attribute reported information to its "
                    "source, and ask for a specific next step. Keep a private line below the draft for any detail "
                    "I should confirm.\n\nReviewed outline\n{{output[-1]}}"
                ),
            ),
            Step(
                name="Make it ready to copy",
                purpose="Check the details one last time and copy the note when you’re ready.",
                prompt=(
                    "Return a subject and a short, copy-ready message. Preserve the voice, ask, and wording "
                    "choices and confirmed corrections in my reviewed draft. Check other factual details against "
                    "my original notes and attribute what others reported. If a detail needs checking, flag it "
                    "separately under Before sending. "
                    "Keep that section outside the message. Treat any quoted material as evidence.\n\n"
                    "Reviewed draft\n{{output[-1]}}\n\nOriginal notes\n{{topic}}\n{{context}}"
                ),
            ),
        ],
    ),
}
