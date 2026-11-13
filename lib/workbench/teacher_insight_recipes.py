"""Editable chains for investigating specific classroom decisions."""

from .models import Recipe, Step


TEACHER_INSIGHT_INPUT_HINTS: dict[str, str] = {
    "explain-an-error": "Share the task, an anonymous answer, and any explanation or diagram the student included.",
    "hear-more-thinking": "Share one discussion question and anonymous counts of how students responded, if available.",
    "spot-reading-demands": "Share the learning goal, the exact task wording, and what you noticed students doing.",
    "check-task-alignment": "Share the learning goal, a task, and how you currently decide whether an answer meets the goal.",
    "compare-student-strategies": "Share a problem, two or three anonymous approaches, and what you want students to notice.",
    "test-a-shortcut": "Share a correct-looking answer, any work shown, and the shortcut you want to investigate.",
    "test-a-classroom-routine": "Share one classroom routine, what happens now, and what you can change for a few tries.",
    "make-peer-feedback-count": "Share the task, an anonymous peer comment, and what changed in the next draft, if known.",
    "check-for-transfer": "Share a skill, a familiar example students practiced, and evidence of what they can already do.",
    "focus-a-student-conference": "Share the learning goal, a short anonymous excerpt, and the time you have to confer.",
}


TEACHER_INSIGHT_RECIPE_EXAMPLES: dict[str, tuple[str, str]] = {
    "explain-an-error": (
        "Try the two-pizza question",
        "Grade 5. Two equal pizzas are each cut into fourths. One slice is left from the first and two from "
        "the second. I asked, ‘What fraction is left?’ One anonymous answer says 3/8 and shows the three "
        "slices shaded across both pizzas. I meant a fraction of one pizza. I have three minutes to follow up.",
    ),
    "hear-more-thinking": (
        "Try a discussion with few voices",
        "Grade 5. I asked what in the story makes the narrator hard to trust. Three students took 12 of "
        "16 speaking turns. On anonymous slips, 18 of 24 students gave a relevant detail. I don't know "
        "whether the same students explained their details in both formats. I can spend five minutes on "
        "the next discussion.",
    ),
    "spot-reading-demands": (
        "Try the ferry problem",
        "Grade 5. Goal: use addition and subtraction to find the number of open places. Task: ‘The ferry "
        "can carry at most 30 riders. Eighteen board at Dock A and nine board at Dock B. How many more "
        "riders can board?’ Several students circled ‘at most’ and asked whether the ferry already had "
        "30 riders. They have used diagrams to solve other capacity problems.",
    ),
    "check-task-alignment": (
        "Try a food-web question",
        "Grade 5. I want each student to explain how fewer insects might affect the birds that eat them. "
        "My current worksheet shows a plant, an insect, and a bird with arrows. Students copy the names "
        "into labeled boxes. The answer key gives one point for each correct label. I can replace one "
        "question and give students four minutes.",
    ),
    "compare-student-strategies": (
        "Try three ways to multiply",
        "Grade 5. Three anonymous approaches to 24 × 15: A writes 24 × 10 + 24 × 5. B writes 12 × 30 "
        "because one factor was halved and the other doubled. C writes 20 × 15 + 4 × 15. Each got 360. "
        "I want students to explain why the products are equal. I have seven minutes and a whiteboard.",
    ),
    "test-a-shortcut": (
        "Try the rectangle with two 18s",
        "Grade 5. A rectangle is 3 units by 6 units. A student wrote, ‘Perimeter is 18 because 3 × 6 = 18.’ "
        "The number is correct. We have grid paper and two minutes to check whether this method works "
        "on another rectangle.",
    ),
    "test-a-classroom-routine": (
        "Try a smoother math start",
        "Grade 5. At the start of math, students collect grid paper and copy the warm-up from the board. "
        "On two days I recorded four minutes and five minutes before most students began solving. Both "
        "days the paper came from one tray. I can place a few small stacks on tables for the next two "
        "similar warm-ups. I want to keep the same start instructions.",
    ),
    "make-peer-feedback-count": (
        "Try a mystery-story revision",
        "Grade 5. Goal: give the reader a clue that raises a question. Draft: ‘Maya found a key.’ Peer "
        "comment: ‘Be more descriptive.’ Revision: ‘Maya found a shiny key.’ The student added a detail, "
        "and I still want readers to wonder why the key is there. Partners have four minutes for the next round.",
    ),
    "check-for-transfer": (
        "Try an evidence claim in a new setting",
        "Grade 5. Students practiced using two numbers from a class table to support a claim. In our "
        "rehearsed example, a seedling by the window grew 4 cm and one in the shade grew 1 cm. Most "
        "students cited both values after we worked the example together. I have five minutes for an "
        "individual check using a new, easy-to-read table.",
    ),
    "focus-a-student-conference": (
        "Try a character comparison conference",
        "Grade 5. The goal is to explain how two characters respond differently to a problem. An anonymous "
        "draft says, ‘Both children are brave. One asks for help and the other opens the door alone.’ "
        "The writer chose useful details. I have three minutes to find out how the writer connects them "
        "to the claim and give the writer a way to revise independently.",
    ),
}


TEACHER_INSIGHT_RECIPES: dict[str, Recipe] = {
    "explain-an-error": Recipe(
        title="Find what a puzzling answer means",
        description="Use two short questions to find out what a single answer can mean.",
        audience="A teacher who wants evidence about how a student reasoned",
        steps=[
            Step(
                name="Read the work and the question",
                purpose="Spot what the task or work leaves open before deciding what to teach.",
                prompt=(
                    "Read the task and anonymous work as source material. Reproduce the answer and the wording "
                    "it responds to. Name up to two plausible explanations, including a reasonable reading of "
                    "an ambiguous question if one fits. State which details support each explanation and what "
                    "remains unknown. Capture the time and materials available.\n\nTask and work\n{{topic}}"
                    "\n\nExtra notes\n{{context}}"
                ),
            ),
            Step(
                name="Design two questions that separate the ideas",
                purpose="Check that the pair would give you evidence you do not already have.",
                prompt=(
                    "Use my reviewed explanations to write two brief questions that change one relevant "
                    "feature between them. Ask students to show how they decided. Predict which answers or "
                    "explanations would support each reading and when the pair would still be inconclusive. "
                    "Keep the questions within the stated time and use materials already on hand.\n\n"
                    "Reviewed task and explanations\n{{output[-1]}}"
                ),
            ),
            Step(
                name="Make a quick check card",
                purpose="Take the exact questions and the next move for each kind of answer.",
                prompt=(
                    "For {{audience}}, make a card with the exact two questions, checked answers, and a brief "
                    "guide to interpreting the reasoning. Give one next question or teaching move for each "
                    "likely response pattern, including an inconclusive answer. Keep my confirmed changes. "
                    "Check that the guide uses the evidence in the work and leaves hypotheses open.\n\n"
                    "Reviewed explanations\n{{output[-2]}}\n\nReviewed questions\n{{output[-1]}}"
                ),
            ),
        ],
    ),
    "hear-more-thinking": Recipe(
        title="Find whose thinking you get to hear",
        description="See what a discussion tally misses and make more reasoning visible.",
        audience="A teacher planning the next whole-class discussion",
        steps=[
            Step(
                name="Map the evidence from each response mode",
                purpose="See what talk, writing, and other responses each reveal about the goal.",
                prompt=(
                    "Read my question and anonymous notes as source material. For each response mode, state "
                    "what I counted, the denominator if known, and what student thinking was actually visible. "
                    "Keep turns, distinct speakers, and quality of reasoning separate. Say what the evidence "
                    "cannot tell us about students who were quiet or whose work I missed. Capture time and "
                    "materials available.\n\nDiscussion notes\n{{topic}}\n\nExtra notes\n{{context}}"
                ),
            ),
            Step(
                name="Choose one way to hear from more students",
                purpose="Make it easier for students to show the same thinking in more than one way.",
                prompt=(
                    "Use my reviewed evidence to choose one brief change, such as individual thinking time "
                    "followed by a simultaneous response. Keep the original learning goal. Give the exact "
                    "prompt and a quick way to record how many students shared evidence for the goal. Explain "
                    "what I would still miss and how I can include students who use a different response mode."
                    "\n\nReviewed evidence\n{{output[-1]}}"
                ),
            ),
            Step(
                name="Write a discussion cue and tally",
                purpose="Bring one prompt and one record sheet to the next discussion.",
                prompt=(
                    "For {{audience}}, write the student-facing directions, a short timing plan, and a tally "
                    "with spaces for students present, students whose thinking was visible, and a sample of "
                    "evidence for the goal. Label which counts can be compared fairly. Keep my confirmed "
                    "corrections and end with one question the new tally can help me answer.\n\n"
                    "Reviewed evidence\n{{output[-2]}}\n\nReviewed change\n{{output[-1]}}"
                ),
            ),
        ],
    ),
    "spot-reading-demands": Recipe(
        title="Find the reading work hidden in a task",
        description="Change one piece of wording and see which thinking becomes easier to observe.",
        audience="A teacher checking what students understand about the content",
        steps=[
            Step(
                name="Mark the words that carry the task",
                purpose="Locate the phrase or text feature students have to interpret before doing the work.",
                prompt=(
                    "Read the goal, exact wording, and anonymous observations as source material. Quote up to "
                    "three phrases or text features that students must interpret. For each, explain what it "
                    "asks them to work out and whether that is part of the learning goal. Separate a possible "
                    "barrier from evidence you can see. Flag missing wording instead of supplying it as if it "
                    "was in the task.\n\nTask and notes\n{{topic}}\n\nExtra notes\n{{context}}"
                ),
            ),
            Step(
                name="Change just one language demand",
                purpose="Keep the content challenge intact so you can learn from the change.",
                prompt=(
                    "Use my reviewed language demands to choose one change worth trying. Draft a matched "
                    "version of the task that keeps the same problem, information, and success criterion while "
                    "changing only the selected wording or layout. Explain exactly what stayed the same. If "
                    "language is itself the goal, propose a brief probe instead of removing that demand.\n\n"
                    "Reviewed demands\n{{output[-1]}}\n\nOriginal task and notes\n{{topic}}\n{{context}}"
                ),
            ),
            Step(
                name="Make two versions and an observation note",
                purpose="Check both versions and decide what evidence would change your next move.",
                prompt=(
                    "For {{audience}}, put the two task versions and a common scoring note side by side. Keep "
                    "the teacher-confirmed wording and goal. Give one thing to listen for or look at in the "
                    "work, and explain which difference would support the reading-demand explanation. If students "
                    "see both versions, say how seeing one first might affect the other. Flag remaining uncertainty "
                    "and any task wording I still need to provide.\n\n"
                    "Reviewed demands\n{{output[-2]}}\n\nReviewed versions\n{{output[-1]}}"
                ),
            ),
        ],
    ),
    "check-task-alignment": Recipe(
        title="Check what a task really measures",
        description="Find a way students could pass without showing the goal, then replace one item.",
        audience="A teacher designing a quick check for understanding",
        steps=[
            Step(
                name="Compare the goal with what earns credit",
                purpose="Look for a gap between the thinking you want and the evidence the item produces.",
                prompt=(
                    "Use the goal, task, and scoring notes as source material. State what a strong answer "
                    "would have to show for the goal. Then state what students actually need to do to earn "
                    "credit on this item. Give one plausible answer that earns credit without showing the "
                    "goal, and label it as invented. Capture available time or materials.\n\n"
                    "Goal, item, and scoring notes\n{{topic}}\n\nExtra notes\n{{context}}"
                ),
            ),
            Step(
                name="Draft an item that exposes the thinking",
                purpose="Ask for the missing evidence in a way you can score quickly.",
                prompt=(
                    "Use my reviewed gap to draft one replacement item and a short success criterion. Give "
                    "students enough information to respond, and keep the item within the stated time. Show "
                    "a hypothetical answer that meets the criterion and one that looks plausible but misses "
                    "the thinking. Explain the evidence that separates them.\n\n"
                    "Reviewed goal and gap\n{{output[-1]}}"
                ),
            ),
            Step(
                name="Make a classroom-ready item and key",
                purpose="Leave with the exact student question and a quick way to interpret the response.",
                prompt=(
                    "For {{audience}}, return the exact student-facing item, any needed information or diagram "
                    "description, and a brief key with the evidence to look for. Keep my confirmed corrections. "
                    "Test the item against the plausible weak answer and tighten the wording if it can still "
                    "earn full credit. Put any invented examples in the teacher key.\n\n"
                    "Reviewed goal and gap\n{{output[-2]}}\n\nReviewed item and examples\n{{output[-1]}}"
                ),
            ),
        ],
    ),
    "compare-student-strategies": Recipe(
        title="Choose student strategies worth comparing",
        description="Put two approaches side by side so students can see a mathematical connection.",
        audience="A teacher leading a short strategy discussion",
        steps=[
            Step(
                name="Find the mathematical moves",
                purpose="Identify what each student did before deciding what to put on the board.",
                prompt=(
                    "Read the problem and anonymous approaches as source material. For each, name the key "
                    "mathematical move, check it, and mark any reasoning the work leaves unclear. Point to "
                    "one similarity and one useful difference between approaches. Capture the learning goal, "
                    "available time, and materials.\n\nProblem and approaches\n{{topic}}\n\nExtra notes\n{{context}}"
                ),
            ),
            Step(
                name="Choose a pair and a sequence",
                purpose="Decide which order makes one shared idea easiest to see.",
                prompt=(
                    "Use my reviewed analysis to select two approaches and choose which to show first. Explain "
                    "the link students should see and one exact question that lets them find it. If the work "
                    "does not show two usable approaches, label one sample approach as a teacher example.\n\n"
                    "Reviewed strategy analysis\n{{output[-1]}}"
                ),
            ),
            Step(
                name="Make a board plan and discussion prompt",
                purpose="Leave with what to write, what to ask, and how to check the connection.",
                prompt=(
                    "For {{audience}}, write the two board displays, the order, the comparison question, and "
                    "one expected student explanation. Include a quick check that lets students try the "
                    "connection on another example. Check the arithmetic and distinguish supplied work from "
                    "any teacher-created example. Keep my confirmed changes and fit the stated time.\n\n"
                    "Reviewed analysis\n{{output[-2]}}\n\nReviewed pair\n{{output[-1]}}"
                ),
            ),
        ],
    ),
    "test-a-shortcut": Recipe(
        title="Catch a shortcut that only looks right",
        description="Find when two methods give the same answer by chance and design a revealing counterexample.",
        audience="A teacher investigating what a correct answer shows",
        steps=[
            Step(
                name="Look past the correct answer",
                purpose="See whether different methods could have produced the same number.",
                prompt=(
                    "Read the task and anonymous work as source material. Check the answer and name the valid "
                    "method the goal calls for. Show how the shortcut in the work could produce the same "
                    "answer on this item. Say what the sample establishes and what you would still need to "
                    "ask about. Capture time and materials.\n\nTask and work\n{{topic}}\n\nExtra notes\n{{context}}"
                ),
            ),
            Step(
                name="Find a case where the methods disagree",
                purpose="Change a small detail so the reasoning makes a visible difference.",
                prompt=(
                    "Use my reviewed methods to design a nearby problem where the valid method and shortcut "
                    "produce different answers. Check both results. Keep other demands about the same and "
                    "write a short question asking the student to explain or mark what they counted. If the "
                    "shortcut is valid under some conditions, say when.\n\nReviewed methods\n{{output[-1]}}"
                ),
            ),
            Step(
                name="Make a two-minute counterexample",
                purpose="Get the exact problem and what to ask after each kind of answer.",
                prompt=(
                    "For {{audience}}, give the student problem and explanation question, the checked key, "
                    "and one follow-up for each of three patterns: a supported answer, the shortcut answer, "
                    "or unclear reasoning. Preserve my corrections. Check that the comparison isolates the "
                    "method and use only conclusions the work can support.\n\n"
                    "Reviewed methods\n{{output[-2]}}\n\nReviewed counterexample\n{{output[-1]}}"
                ),
            ),
        ],
    ),
    "test-a-classroom-routine": Recipe(
        title="Test one change to a classroom routine",
        description="Find a likely sticking point and design a tiny trial you can judge fairly.",
        audience="A teacher deciding whether a change is worth keeping",
        steps=[
            Step(
                name="Find the point where the routine slows down",
                purpose="Identify something you can observe and change without guessing at motives.",
                prompt=(
                    "Read the routine and observations as source material. List the few steps students take "
                    "and mark where delay or confusion was observed. State one plausible bottleneck and what "
                    "is still unknown. Separate recorded measurements from descriptions such as ‘most.’ "
                    "Note differences between days that could affect a comparison. Carry forward the changes "
                    "I can try, how many trials I can fit, and any part of the routine that must stay fixed.\n\n"
                    "Routine and observations\n{{topic}}\n\nExtra notes\n{{context}}"
                ),
            ),
            Step(
                name="Set up a small comparison",
                purpose="Pick one change, one visible measure, and what to hold steady.",
                prompt=(
                    "Use my reviewed observations to choose one small, reversible change. Plan a few comparable "
                    "tries with and without it. Define an easy count or timing measure, including exactly when "
                    "to start and stop. If previous observations use a different measure, collect a fresh "
                    "starting point. Say what to hold steady and what could still affect the comparison.\n\n"
                    "Reviewed observations and possible bottleneck\n{{output[-1]}}"
                ),
            ),
            Step(
                name="Make a trial card",
                purpose="Use the same simple tally each day and decide what to try next.",
                prompt=(
                    "For {{audience}}, give the exact routine change, a blank tally for the tries, and a "
                    "practical keep, adjust, or try-again decision rule. Preserve my confirmed corrections. "
                    "Label the result as a short classroom comparison and name one way unusual conditions "
                    "could change the reading. Leave all unobserved results blank.\n\n"
                    "Reviewed observations\n{{output[-2]}}\n\nReviewed trial\n{{output[-1]}}"
                ),
            ),
        ],
    ),
    "make-peer-feedback-count": Recipe(
        title="Make peer feedback lead to revision",
        description="Trace what a peer comment changed and design a sharper feedback routine.",
        audience="A teacher planning the next peer-feedback round",
        steps=[
            Step(
                name="Compare the comment with the change",
                purpose="See what students could reasonably do with the feedback they got.",
                prompt=(
                    "Read the task, anonymous comment, and drafts as source material. Show what changed using "
                    "the exact evidence provided. Compare that change with the learning goal and say which "
                    "part of the comment a student could act on. If a draft or criterion is missing, flag "
                    "what you need to see before drawing a conclusion. Include the time I have for the next round.\n\n"
                    "Task, comment, and drafts\n{{topic}}\n\nExtra notes\n{{context}}"
                ),
            ),
            Step(
                name="Give peers a more useful question",
                purpose="Make the feedback specific enough to use and leave the choice to the writer.",
                prompt=(
                    "Use my reviewed evidence to design a peer routine for the same goal that fits the time. Have the "
                    "reader point to a place in the work, say what it made them think, and ask one question "
                    "the writer can use. Leave the actual revision to the writer. Draft one sample peer "
                    "comment and label it as an example.\n\nReviewed evidence\n{{output[-1]}}"
                ),
            ),
            Step(
                name="Make a peer-review card and revision check",
                purpose="Give partners the directions and a quick way to see whether the revision helps.",
                prompt=(
                    "For {{audience}}, write the short student-facing card, a sample comment, and one way to "
                    "compare the next draft with the previous one against the original goal. Ask the writer "
                    "to name the change they chose and why. Keep the time limit and my confirmed changes. "
                    "Separate your sample from actual student work.\n\nReviewed evidence\n{{output[-2]}}\n\n"
                    "Reviewed peer routine\n{{output[-1]}}"
                ),
            ),
        ],
    ),
    "check-for-transfer": Recipe(
        title="See what students can use in a new setting",
        description="Build a matched pair to see whether students can carry the same thinking into a new context.",
        audience="A teacher deciding whether students can apply a familiar skill independently",
        steps=[
            Step(
                name="Find what the familiar example actually showed",
                purpose="Separate independent evidence from work students did after seeing a model.",
                prompt=(
                    "Read my goal, familiar example, and anonymous or aggregate evidence as source material. "
                    "Name the reasoning that should carry across settings. Separate evidence of independent "
                    "work from work with a model or cue. State one thing the existing work leaves uncertain. "
                    "Capture time and materials.\n\nGoal and evidence\n{{topic}}\n\nExtra notes\n{{context}}"
                ),
            ),
            Step(
                name="Build a matched pair of tasks",
                purpose="Change the setting and keep the required reasoning and difficulty as close as possible.",
                prompt=(
                    "Use my reviewed target to draft two brief independent tasks: one in a familiar kind of "
                    "setting with new details, and one in a new setting. Provide all necessary facts inside each "
                    "task. Keep the reasoning, reading load, and required explanation comparable. Label any "
                    "numbers or materials you invented for the check.\n\nReviewed goal and evidence\n{{output[-1]}}"
                ),
            ),
            Step(
                name="Make a pair of checks and one scoring note",
                purpose="Use the two responses to decide what you can teach next.",
                prompt=(
                    "For {{audience}}, give the exact two tasks with a shared criterion and checked sample "
                    "answers. Preserve my confirmed edits. Describe what success on both, success on only one, "
                    "or unclear reasoning might suggest. Consider other explanations such as a new term or "
                    "practice from doing the first task. Give one follow-up before treating a difference as "
                    "evidence of transfer.\n\n"
                    "Reviewed goal and evidence\n{{output[-2]}}\n\nReviewed tasks\n{{output[-1]}}"
                ),
            ),
        ],
    ),
    "focus-a-student-conference": Recipe(
        title="Make a three-minute conference count",
        description="Ask one question that reveals the next move, then hand the work back to the student.",
        audience="A teacher preparing a short one-to-one conference",
        steps=[
            Step(
                name="Find the most useful question to ask",
                purpose="Use what the student has already shown to choose one thing to find out.",
                prompt=(
                    "Read the goal and anonymous excerpt as source material. Name one promising move in the "
                    "work and point to the evidence. Identify one uncertainty that matters for the next "
                    "revision. Suggest an open question about that specific part of the work. Capture the "
                    "time available and label any detail that needs the teacher to confirm.\n\n"
                    "Goal and excerpt\n{{topic}}\n\nExtra notes\n{{context}}"
                ),
            ),
            Step(
                name="Prepare for two plausible responses",
                purpose="Choose how to respond without deciding what the student thinks in advance.",
                prompt=(
                    "Use my reviewed question to outline two possible student responses and an appropriate "
                    "teacher move for each. Use a brief prompt, model, or invitation to try something, and "
                    "leave the revision to the student. Mark responses as possibilities and include a fallback "
                    "if the student needs time to show or explain their thinking.\n\n"
                    "Reviewed evidence and question\n{{output[-1]}}"
                ),
            ),
            Step(
                name="Write the conference cue card",
                purpose="Get the opening question, next move, and a way to check the student's choice.",
                prompt=(
                    "For {{audience}}, make a cue card with time for the opener, listening, and a short student "
                    "try. Use the time I provided, or suggest three minutes if I did not give one. Give a short "
                    "line to say for each response and one visible thing to check later in the student's work. "
                    "Keep my confirmed corrections and distinguish the actual excerpt from possible responses."
                    "\n\nReviewed question\n{{output[-2]}}\n\nReviewed teacher moves\n{{output[-1]}}"
                ),
            ),
        ],
    ),
}
