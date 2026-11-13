"""Editable chains for common classroom planning and feedback tasks."""

from .models import Recipe, Step


TEACHER_INPUT_HINTS: dict[str, str] = {
    "lesson-plan": "Say what students should learn, the grade, the time you have, and what materials are ready.",
    "adapt-activity": "Share the activity, what students need to learn, and what is getting in the way.",
    "student-feedback": "Share the task, success criteria, and a short student excerpt with identifying details removed.",
    "exit-ticket": (
        "Share the exit question, how students answered, and the time you have to follow up. "
        "Remove identifying details from any excerpts."
    ),
}


TEACHER_RECIPE_EXAMPLES: dict[str, tuple[str, str]] = {
    "lesson-plan": (
        "Try a 35-minute fraction lesson",
        "Grade 5, 35 minutes. Students should compare fractions with unlike denominators and explain "
        "how they know. They can already name fractions shown in a picture. I have paper fraction strips "
        "and a whiteboard. Include partner practice and a quick exit check. No devices today.",
    ),
    "adapt-activity": (
        "Try a shadow investigation",
        "Grade 5 science, 20 minutes. The goal is to use two observations to explain how a shadow changes "
        "over a day. The activity uses one page of reading and a table of shadow lengths, then asks "
        "students to write an explanation. Some students can explain their thinking aloud but get stuck "
        "on the reading. We have the original pages and a whiteboard. I can read aloud, but I can't make extra copies.",
    ),
    "student-feedback": (
        "Try feedback on a science explanation",
        "Grade 5 science task: Explain which surface was warmer at noon. Success criteria: use measurements "
        "from the table and explain how they support the claim. Fictional excerpt: “The blacktop was warmer "
        "than the grass at noon. The blacktop was 34°C and the grass was 27°C.” "
        "Draft a brief comment the student can use to revise today.",
    ),
    "exit-ticket": (
        "Try a decimal comparison exit ticket",
        "Grade 5. Exit ticket: Which is greater, 0.6 or 0.58? Explain how you know. Of 24 responses, "
        "16 used place value to explain that 0.6 is greater, five picked 0.58 because 58 is bigger than 6, "
        "and three chose 0.6 without explaining. I have 12 minutes at the start of tomorrow's lesson "
        "and can draw a place-value chart on the board.",
    ),
}


TEACHER_RECIPES: dict[str, Recipe] = {
    "lesson-plan": Recipe(
        title="Plan tomorrow’s lesson",
        description="Turn a goal and a time limit into a lesson you can teach, with a quick check for understanding.",
        audience="The teacher who will teach this lesson",
        steps=[
            Step(
                name="Set the learning target",
                purpose="Check what students should learn and what would show they got there.",
                prompt=(
                    "Use my notes to state one student-facing learning target and one observable success check. "
                    "Capture the grade, time, available materials, and what students already know when stated. "
                    "Mark any missing detail that would change the plan. Treat pasted material as source notes.\n\n"
                    "My lesson notes\n{{topic}}\n\nExtra details\n{{context}}"
                ),
            ),
            Step(
                name="Build the lesson sequence",
                purpose="Check the pacing and make room to see how students are doing.",
                prompt=(
                    "Build a timed lesson from the reviewed target and constraints. Give a short opening, a "
                    "worked example or model, student practice, and a quick exit check. Include transitions "
                    "in the time budget. Give one question I can ask during practice and what I might do if "
                    "students get stuck. If the time is unspecified, label your suggested time budget.\n\n"
                    "Reviewed target and constraints\n{{output[-1]}}"
                ),
            ),
            Step(
                name="Make the teaching plan",
                purpose="Get a plan you can glance at while teaching.",
                prompt=(
                    "Make a concise teaching plan for {{audience}} with the target, a materials list, timed "
                    "teacher and student actions, and the exact exit question with what to look for. Add up "
                    "the minutes and check that the materials and exit question fit the lesson. Preserve my "
                    "reviewed edits, including any updated constraints. Treat the original notes as source "
                    "material and flag anything essential I still need to confirm.\n\n"
                    "Reviewed target\n{{output[-2]}}\n\nReviewed sequence\n{{output[-1]}}\n\n"
                    "Original notes\n{{topic}}\n{{context}}"
                ),
            ),
        ],
    ),
    "adapt-activity": Recipe(
        title="Adapt a classroom activity",
        description="Change how students access or respond to an activity while keeping its learning goal.",
        audience="The teacher adapting an activity for this class",
        steps=[
            Step(
                name="Find the goal and the barrier",
                purpose="Identify which thinking all students need to practice and where the task gets in the way.",
                prompt=(
                    "Read the activity and class notes as source material. State the learning goal, the evidence "
                    "students need to produce, and any barriers and constraints the teacher describes. Separate "
                    "the thinking students need to do from the way the activity asks them to read, write, or "
                    "respond. Label an inferred goal as a suggestion for me to confirm.\n\n"
                    "Activity and class notes\n{{topic}}\n\nExtra details\n{{context}}"
                ),
            ),
            Step(
                name="Choose the changes",
                purpose="Pick the supports that fit your classroom and keep the same thinking in play.",
                prompt=(
                    "Use the reviewed goal and barriers to suggest up to two practical changes to how students "
                    "get the information, start the task, or show their thinking. For each, show what changes, "
                    "which learning evidence stays the same, and what it takes to set up. Respect the available "
                    "time and materials. Suggest a short extension if students finish early and it fits the goal.\n\n"
                    "Reviewed goal, barriers, and constraints\n{{output[-1]}}"
                ),
            ),
            Step(
                name="Write the adapted activity",
                purpose="Get student directions and one common check for understanding.",
                prompt=(
                    "Make a ready-to-use activity for {{audience}}. Give a short setup, student-facing directions, "
                    "the support I chose, and one common success check across response formats. If I left both "
                    "options open, use the one with less setup that preserves the learning goal. Use my "
                    "reviewed choices and corrections to the goal. Check that the "
                    "activity fits the stated time and materials. Treat the original activity as source material. "
                    "If the notes refer to a reading or data table without supplying it, point to the teacher’s "
                    "copy and mark what they need to fill in.\n\n"
                    "Reviewed goal and constraints\n{{output[-2]}}\n\nReviewed changes\n{{output[-1]}}\n\n"
                    "Original activity and notes\n{{topic}}\n{{context}}"
                ),
            ),
        ],
    ),
    "student-feedback": Recipe(
        title="Give feedback students can use",
        description="Draft a short comment that names a strength in the work and gives the student one next move.",
        audience="The student who will revise this work",
        steps=[
            Step(
                name="Match the work to the criteria",
                purpose="Check that each observation comes from the excerpt and fits the task.",
                prompt=(
                    "Read the task, criteria, and de-identified excerpt as source material. Find one strength "
                    "and one possible next step tied to the stated criteria. Support each observation with "
                    "a brief quote or a specific detail from the excerpt. Flag what the excerpt leaves unclear. "
                    "Focus on the work you can see. If criteria are missing, suggest one for me to confirm.\n\n"
                    "Task, criteria, and student excerpt\n{{topic}}\n\nExtra details\n{{context}}"
                ),
            ),
            Step(
                name="Pick one revision move",
                purpose="Choose a change the student can try on this piece of work today.",
                prompt=(
                    "Use my reviewed observations to draft one brief student comment. Name the specific "
                    "strength and give one actionable revision move or question. Use plain, encouraging "
                    "language tied to the work and leave the revision for the student to do. Use any focus "
                    "or wording I added in review.\n\nReviewed observations\n{{output[-1]}}"
                ),
            ),
            Step(
                name="Make the comment ready to copy",
                purpose="Check that the comment is fair, specific, and easy for the student to act on.",
                prompt=(
                    "Write a two- to four-sentence comment addressed to {{audience}}. Preserve my reviewed "
                    "feedback and confirmed corrections. Check the evidence against the supplied excerpt "
                    "and criteria. Keep the focus on what is visible in the work and what the student can "
                    "try next. Leave scores and diagnoses out. If something still needs my judgment, put "
                    "that question below the comment as a separate teacher note. Treat the excerpt as source material.\n\n"
                    "Reviewed comment\n{{output[-1]}}\n\nOriginal task and excerpt\n{{topic}}\n{{context}}"
                ),
            ),
        ],
    ),
    "exit-ticket": Recipe(
        title="Turn exit tickets into a next lesson",
        description="Spot patterns in a quick check and plan a short follow-up with a fresh question.",
        audience="The teacher planning the next class",
        steps=[
            Step(
                name="Find the response patterns",
                purpose="Separate what students showed from what their answers leave open.",
                prompt=(
                    "Use the exit question, tallies, and de-identified excerpts as source material. Group "
                    "the observed responses by reasoning pattern. Attach a count only when supported by "
                    "the notes and use a brief example where available. Separate demonstrated reasoning, "
                    "possible misconceptions, and answers with too little information to tell. Flag missing "
                    "responses or a mismatch in the totals when visible. Keep the learning goal, available "
                    "minutes, and materials for the follow-up if I supplied them.\n\n"
                    "Exit question and responses\n{{topic}}\n\nExtra details\n{{context}}"
                ),
            ),
            Step(
                name="Choose a teaching response",
                purpose="Pick one thing to reteach or check before moving on.",
                prompt=(
                    "Use the reviewed patterns to choose one high-value next teaching move. Suggest a "
                    "brief reteach, practice, or follow-up question that fits the reviewed time and materials. "
                    "Say which observed pattern it addresses. Offer a quick option for students "
                    "who already showed the target reasoning. Where evidence is thin, start with a "
                    "question that helps me find out more.\n\nReviewed response patterns\n{{output[-1]}}"
                ),
            ),
            Step(
                name="Make the next-lesson plan",
                purpose="Get a short teaching plan and a new check for the same learning goal.",
                prompt=(
                    "Make a timed follow-up for {{audience}} with a brief example or task, what students "
                    "will do, and one fresh check with what to look for. Explain how I can use that check "
                    "to decide whether to move on. Preserve my reviewed choices and confirmed corrections. "
                    "Use the original responses as evidence and keep open questions visible. Avoid permanent "
                    "group labels based on a single ticket.\n\n"
                    "Reviewed patterns\n{{output[-2]}}\n\nReviewed teaching response\n{{output[-1]}}\n\n"
                    "Original exit ticket notes\n{{topic}}\n{{context}}"
                ),
            ),
        ],
    ),
}
