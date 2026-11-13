"""Built-in starting points and a labelled, authored example."""

from .everyday_recipes import EVERYDAY_INPUT_HINTS, EVERYDAY_RECIPE_EXAMPLES, EVERYDAY_RECIPES
from .models import Recipe, Result, Run, Step
from .parent_insight_recipes import PARENT_INSIGHT_INPUT_HINTS, PARENT_INSIGHT_RECIPE_EXAMPLES, PARENT_INSIGHT_RECIPES
from .teacher_insight_recipes import TEACHER_INSIGHT_INPUT_HINTS, TEACHER_INSIGHT_RECIPE_EXAMPLES, TEACHER_INSIGHT_RECIPES
from .teacher_recipes import TEACHER_INPUT_HINTS, TEACHER_RECIPE_EXAMPLES, TEACHER_RECIPES


def step(name: str, purpose: str, prompt: str) -> Step:
    return Step(name=name, purpose=purpose, prompt=prompt)


_PARENT_AUDIENCE = "A parent or caregiver. Write directions a fifth grader can follow."

PARENT_RECIPE_EXAMPLES = {
    "family-game": (
        "Try a silly drawing game",
        "Make a five-minute game where two people draw silly animals with paper and pencils.",
    ),
    "memory-comic": (
        "Try the picnic squirrel",
        "Make a comic about an imaginary picnic where a squirrel grabs the napkin instead of the sandwich.",
    ),
    "home-invention": (
        "Try a pencil holder",
        "Invent a cardboard holder that keeps pencils from rolling off a table.",
    ),
}

RECIPE_EXAMPLES = {
    **PARENT_RECIPE_EXAMPLES, **EVERYDAY_RECIPE_EXAMPLES, **TEACHER_RECIPE_EXAMPLES,
    **PARENT_INSIGHT_RECIPE_EXAMPLES, **TEACHER_INSIGHT_RECIPE_EXAMPLES,
}
RECIPE_INPUT_HINTS = {
    **EVERYDAY_INPUT_HINTS, **TEACHER_INPUT_HINTS, **PARENT_INSIGHT_INPUT_HINTS, **TEACHER_INSIGHT_INPUT_HINTS,
}

PARENT_RECIPES = {
    "family-game": Recipe(
        title="Make a game for family night",
        description="Make up a game you can teach at the kitchen table in a few minutes.",
        audience=_PARENT_AUDIENCE,
        steps=[
            step("Make up a game", "Pick a theme your grown-up would enjoy and say what you have to play with.",
                 "Help me invent a five-minute game.\n\nAudience\n{{audience}}\n\n"
                 "Here’s my idea.\n{{topic}}\n\n"
                 "Here’s what I have in mind for players and supplies.\n{{context}}\n\n"
                 "Use supplies I list or just paper and a pencil. "
                 "Draft the setup, one turn, and how the game ends. Point out one rule I can change."),
            step("Try a pretend turn", "Read the draft. Change a rule or add a twist before you keep going.",
                 "Here are my rules. Walk through one pretend turn with them.\n{{output[-1]}}\n\n"
                 "Show what two players could do and what happens next. Find one place a new player might "
                 "get stuck and suggest a fix. Keep any rule or twist I added."),
            step("Make a rules card", "Read the sample turn. Fix a confusing rule before you make the card.",
                 "Here’s my game.\n{{output[-2]}}\n\nHere’s my checked sample turn.\n{{output[-1]}}\n\n"
                 "Write a short rules card I can read aloud.\n\nAudience\n{{audience}}\n\n"
                 "Include the name, supplies, "
                 "setup, what to do on a turn, how the game ends, and how to win or succeed. "
                 "Include a one-line example turn. Use the checked turn to clarify the rules, "
                 "and use my version of any rule I changed."),
        ],
    ),
    "memory-comic": Recipe(
        title="Turn a memory into a comic",
        description="Draw a four-panel comic from a funny moment or a scene you make up.",
        audience=_PARENT_AUDIENCE,
        steps=[
            step("Pick the moment", "Share a few details you’re comfortable showing, or make up the whole scene.",
                 "Help me plan a comic.\n\nAudience\n{{audience}}\n\nHere’s my moment.\n{{topic}}\n\n"
                 "Here are my details.\n{{context}}\n\n"
                 "Suggest a beginning, a surprise, and an ending using the details I gave. "
                 "Call an imagined scene fiction. Use roles such as 'my grown-up' for real people. "
                 "Leave space for a detail I want to draw."),
            step("Plan four pictures", "Change the ending or add one detail you want your grown-up to notice.",
                 "Turn my plan below into four easy-to-draw panels.\n{{output[-1]}}\n\n"
                 "Describe the action in each picture and suggest a short caption if it helps. "
                 "Use only the details I shared for a real memory. Leave speech bubbles blank for me to fill."),
            step("Make a storyboard", "Check the four pictures. Keep the details you want to share.",
                 "Make a four-panel storyboard from my revised panels below.\n{{output[-1]}}\n\n"
                 "Give it a title and one short drawing direction per panel, with room for my own words. "
                 "Keep my changes and label an imagined scene as fiction. Leave out identifying details "
                 "and keep real dialogue for me to write. "
                 "Make it easy to copy onto one sheet of paper."),
        ],
    ),
    "home-invention": Recipe(
        title="Invent a fix for home",
        description="Design a paper or cardboard prototype and show how you would test it.",
        audience=_PARENT_AUDIENCE,
        steps=[
            step("Sketch two fixes", "Pick one small problem you see at home, like pencils rolling off the table.",
                 "Here’s my problem.\n{{topic}}\n\nHere’s what I have and what I’ve noticed.\n{{context}}\n\n"
                 "Suggest two simple tabletop prototypes I can make from paper or cardboard and tape. "
                 "Give each a name and say what it would help with. Offer one change I could try for each."),
            step("Plan one test", "Keep the idea you want to build and change one part to make it yours.",
                 "Use my prototype idea below.\n{{output[-1]}}\n\nMy problem and notes are below.\n{{topic}}\n{{context}}\n\n"
                 "Follow my choice if I picked a design. If I left both options open, use the one with "
                 "fewer materials. Describe the design, including any changes I made. Plan one short test "
                 "that compares what happens with and without the prototype. Say what to count or watch for."),
            step("Pitch the invention", "Check the plan, then show your grown-up what you built or want to try.",
                 "Use my invention and test plan below.\n{{output[-1]}}\n\n"
                 "My problem and notes are below.\n{{topic}}\n{{context}}\n\n"
                 "Audience\n{{audience}}\n\nGive me labels for a sketch, short build directions, the test, "
                 "and a 30-second pitch I can say out loud. Carry forward my design choices. "
                 "Describe the test as a plan and leave a blank for what I actually observe."),
        ],
    ),
}


RECIPES = {
    "explain": Recipe(
        title="Make it click",
        description="Turn a tricky idea into an explanation you can actually use.",
        steps=[
            step("Find the pieces", "A clear explanation starts with the right building blocks.",
                 "Explain the core pieces of {{topic}} for {{audience}}. Context: {{context}}. Identify 3–5 pieces and a common misconception. Separate established facts from uncertainty. Use plain language."),
            step("Build an analogy", "Use the pieces you just found to make something familiar.",
                 "Topic: {{topic}}. For {{audience}}, create one everyday analogy for these pieces:\n{{output[-1]}}\nExplain where the analogy helps and where it breaks down. Do not present the analogy as a literal description."),
            step("Try it out", "A concrete example shows whether the analogy holds up.",
                 "Using these pieces:\n{{output[-2]}}\nAnd this analogy:\n{{output[-1]}}\nGive a small, worked example of {{topic}} for {{audience}}. Include one check-for-understanding question with its answer."),
            step("Make it click", "Bring the pieces, analogy and example into one useful explanation.",
                 "Write a self-contained explanation of {{topic}} for {{audience}}. Context: {{context}}. Use the building blocks:\n{{output[-3]}}\nThe analogy and its limits:\n{{output[-2]}}\nAnd the example:\n{{output[-1]}}\nKeep it concise. End with a question, then put the suggested answer after a clear 'Suggested answer' label. Avoid unsupported facts."),
        ],
    ),
    "connect": Recipe(
        title="Connect two ideas",
        description="Find the useful bridge between things that seem unrelated.",
        steps=[
            step("Meet both ideas", "Understand each idea before looking for similarities.",
                 "The two ideas are: {{topic}}. Context: {{context}}. Explain each separately to {{audience}}, including its main parts and how it works."),
            step("Find the bridge", "Look for a shared mechanism, not just similar words.",
                 "Find three meaningful connections between the ideas described here:\n{{output[-1]}}\nFor each, explain the shared mechanism and a limit of the comparison."),
            step("Put it to use", "A useful connection changes what you can explain or do.",
                 "Using this analysis:\n{{output[-2]}}\nAnd these connections:\n{{output[-1]}}\nDesign a small activity for {{audience}} that makes the strongest connection tangible. Include materials, steps, and a reflection question. Context: {{context}}."),
        ],
    ),
    "decide": Recipe(
        title="Think a decision through",
        description="Lay out the options, examine the tradeoffs, find a next step.",
        audience="Me; be direct and practical",
        steps=[
            step("Frame the choice", "Name the decision and the constraints that matter.",
                 "Help {{audience}} think through: {{topic}}. Context: {{context}}. State the decision, known constraints, unknowns, and 2–4 plausible options. Do not invent personal facts."),
            step("Test the options", "Consider what could change your mind.",
                 "Examine these options:\n{{output[-1]}}\nCompare effort, reversibility, likely benefit and failure modes. Distinguish facts, assumptions and missing information. For each option, say what would make it the wrong choice."),
            step("Choose a next step", "Leave with a small action and a reason to revisit it.",
                 "Decision: {{topic}}. Context: {{context}}. Based on the framing:\n{{output[-2]}}\nAnd tradeoffs:\n{{output[-1]}}\nOffer a provisional recommendation for {{audience}}, the main uncertainty, one small reversible next action, and a clear reason to reconsider. This is decision support, not professional advice."),
        ],
    ),
    "write": Recipe(
        title="From thought to draft",
        description="Give a rough idea a shape, a first draft, and a careful revision.",
        audience="The intended reader described in my context",
        steps=[
            step("Find the point", "Decide what the reader should take away.",
                 "Writing intention: {{topic}}. Context: {{context}}. Reader: {{audience}}. Identify the central point and sketch a short outline. Flag any factual claims needing a source. Do not invent personal experiences."),
            step("Write the draft", "Build a complete draft from that specific outline.",
                 "Write a complete draft using this outline:\n{{output[-1]}}\nIntention: {{topic}}. Context: {{context}}. Reader: {{audience}}. Use warm, plain language. Do not invent experiences, quotes, sources or statistics. Mark missing facts as [verify]."),
            step("Read it critically", "Check the draft against its purpose.",
                 "Critique this draft for clarity, structure, usefulness and unsupported claims:\n{{output[-1]}}\nOriginal intention: {{topic}}. Context: {{context}}. Give specific changes; do not congratulate the writer."),
            step("Make it ready to review", "Apply the critique without losing the writer's intent.",
                 "Revise this draft:\n{{output[-2]}}\nUsing this critique:\n{{output[-1]}}\nIntention: {{topic}}. Context: {{context}}. Return the revised draft, then a short list of facts the author still needs to check. Never claim the piece is fact-checked."),
        ],
    ),
    "untangle": Recipe(
        title="Untangle a problem",
        description="Separate symptoms from causes, then try one manageable fix.",
        audience="Me; keep the effort manageable",
        steps=[
            step("See what's happening", "Describe observations before guessing causes.",
                 "Problem: {{topic}}. Context: {{context}}. For {{audience}}, separate observed symptoms, constraints, assumptions and missing evidence. Do not invent causes."),
            step("Look underneath", "Treat causes as hypotheses you can check.",
                 "Given these observations:\n{{output[-1]}}\nPropose up to three possible causes. For each, name a simple observation that would support or weaken it. Avoid certainty without evidence."),
            step("Try one change", "Choose a low-effort test that teaches you something.",
                 "Problem: {{topic}}. Context: {{context}}. Observations:\n{{output[-2]}}\nPossible causes:\n{{output[-1]}}\nFor {{audience}}, propose one small reversible change, what to observe, and what to try if it does not help."),
        ],
    ),
    "learn": Recipe(
        title="Build a learning path",
        description="Go from a big topic to a small first lesson and a way to practise.",
        steps=[
            step("Find the starting point", "Name the essentials without making a huge syllabus.",
                 "I want to learn {{topic}}. Learner: {{audience}}. Context: {{context}}. Identify the essential prerequisites and three achievable learning goals. Flag assumptions about prior knowledge."),
            step("Map the path", "Put the goals in an order that builds understanding.",
                 "Build a short learning path from:\n{{output[-1]}}\nTopic: {{topic}}. Learner: {{audience}}. Context: {{context}}. Use at most five small lessons with one practice task each. Do not invent links or sources."),
            step("Teach the first lesson", "Make it possible to start right now.",
                 "Teach the first lesson in this path:\n{{output[-1]}}\nLearner: {{audience}}. Context: {{context}}. Include a plain explanation, worked example, practice question and suggested answer. End by naming the next lesson. Distinguish simplifications from literal facts."),
        ],
    ),
    **PARENT_RECIPES,
    **EVERYDAY_RECIPES,
    **TEACHER_RECIPES,
    **PARENT_INSIGHT_RECIPES,
    **TEACHER_INSIGHT_RECIPES,
}


EXAMPLE_OUTPUTS = [
    "The Moon does not make its own light. Sunlight lights half of it. As the Moon travels around Earth, we see different amounts of that sunlit half. Those changing views are called phases.\n\nA common mix-up: Earth's shadow does not cause the ordinary phases. Earth's shadow is involved in a lunar eclipse, which is a different event.",
    "Imagine a ball with a lamp shining on it in a dark room. Half the ball is lit. If you walk around the ball, you see different amounts of its bright side. The lamp is like the Sun, and the ball is like the Moon.\n\nWhere it helps: it shows how a half-lit ball can appear as different shapes.\nWhere it breaks down: in space, the Moon travels around Earth; you do not walk around a stationary Moon. Distances and sizes in this room model are also very different.",
    "Try a lamp-and-ball model. Keep the lamp in one place and hold a ball at arm's length. Turn slowly while watching the ball, keeping it out of your head's shadow.\n\nWhen the lamp is behind you, the side facing you looks almost fully lit. When the lamp is off to your side, you see about half of the lit side. When the ball is toward the lamp, its side facing you looks mostly dark.\n\nCheck: does the ball actually change shape? No. Only your view of its lit half changes. This room model leaves out the Moon's tilted orbit; real eclipses do not happen every month.",
    "The Moon keeps its round shape. The bright shape we see changes because we see different amounts of its sunlit half as it travels around Earth.\n\nPicture a lamp shining on a ball. From one spot, the ball looks bright. From another, you see a thin bright curve. The lamp keeps lighting half the ball; your view changes. That is the useful part of the model, even though the real Moon moves around Earth.\n\nA full Moon happens when we see almost all of its sunlit side. At a quarter Moon, we see about half of its sunlit side. A crescent is a thinner view. Earth's shadow does not cause these ordinary phases.\n\nTry it: use a lamp and ball to make a crescent without changing the ball's shape. Keep the ball out of your head's shadow.\n\nQuestion: What changes during the Moon's phases: the Moon's shape, or our view of its sunlit half?\n\nSuggested answer: Our view of its sunlit half changes.",
]


def worked_example() -> Run:
    # Imported lazily to keep the catalog independent of persistence and providers.
    from .runner import render_prompt

    run = Run(recipe=RECIPES["explain"].model_copy(deep=True),
              topic="Why does the Moon change shape?", model="Authored example")
    for output in EXAMPLE_OUTPUTS:
        text = render_prompt(run.recipe.steps[len(run.results)].prompt, run)
        run.results.append(Result(prompt=text, output=output))
    run.state = "completed"
    run.mode = "example"
    return run
