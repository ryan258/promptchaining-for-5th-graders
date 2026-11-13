"""Fictional classroom challenges with prepared answers for offline practice."""

from dataclasses import dataclass

from .professional_cases import ProfessionalCase


@dataclass(frozen=True)
class ClassroomCase(ProfessionalCase):
    try_next: str = ""
    last_clue: str = ""


@dataclass(frozen=True)
class PromptChoice:
    label: str
    instruction: str
    example: str


@dataclass(frozen=True, kw_only=True)
class ChainBuildingCase(ClassroomCase):
    choices: tuple[PromptChoice, PromptChoice]

    def choice_for(self, instruction: str) -> PromptChoice | None:
        return next((choice for choice in self.choices if choice.instruction == instruction), None)


_MAP_NOTE = PromptChoice(
    label="Make a map note",
    instruction="Write one line of map labels with arrows between them. Add the library rule under the arrows.",
    example="Reading rug → Blue dots → Past the return cart → Story corner\nKeep voices low. The stairs are closed.",
)
_SPOKEN_DIRECTIONS = PromptChoice(
    label="Give spoken directions",
    instruction="Write two short directions someone can read aloud to Pip. Work the library rule into the directions.",
    example=(
        "1. From the reading rug, follow the blue dots past the book return cart. Skip the stairs.\n"
        "2. Keep following the dots to the story corner. Use a whisper if you need to talk."
    ),
)


CHAIN_BUILDING_CASES = {
    "dragon-library": ChainBuildingCase(
        title="Sneak a dragon through the library",
        topic="Can you get Pip to story time?",
        audience="Pip the dragon",
        description="Choose the last prompt’s job. See how two different prompts use the same answer.",
        context=(
            "A. Pip is on the reading rug. Story time is about to start in the story corner.\n\n"
            "B. Blue dots on the floor lead from the rug, past the book return cart, to the story corner. "
            "The stairs are closed.\n\n"
            "C. Keep your voice low inside the library. That goes for dragons, too."
        ),
        rubric=("Keep the path and the quiet-voice rule in both answers.",),
        steps=(
            ("Find a route", "Trace the path with your finger as you read. Where does Pip start and stop?",
             "Read the library clues:\n{{context}}\n\nFind a path for {{audience}}. Include the quiet-voice rule."),
            ("Pick the next job", "What should the next prompt ask for?",
             "Here is Pip’s route:\n{{output[-1]}}\n\nSuggest two ways to share the route."),
            ("Use both answers", "Keep the route and use the job you picked.",
             "Use this route from the first answer:\n{{output[-2]}}\n\n"
             "Do this job from the second step:\n{{output[-1]}}"),
        ),
        outputs=(
            "Start on the reading rug. Follow the blue dots past the book return cart to the story corner. "
            "The stairs are closed. Keep your voice low.",
            "You could make a map note Pip can glance at, or give a friend directions they can read aloud to Pip.",
        ),
        choices=(_MAP_NOTE, _SPOKEN_DIRECTIONS),
        try_next=(
            "Ask a grown-up to play the AI. Read them the same route, then give it a new job. "
            "Try “Turn this route into a quiet cheer.” Can they keep the path and the library rule? Then switch jobs."
        ),
    ),
}


_FIRST_CLASSROOM_CASES = {
    "rainy-recess": ProfessionalCase(
        title="Rescue rainy recess",
        topic="What can we play when recess moves inside?",
        audience="Our fifth-grade class",
        description="Rain washed out recess. Pick a game your class can play right at their desks.",
        context=(
            "A. The gym is full. All 26 kids have to stay at their desks. The teacher says no throwing.\n\n"
            "B. The class voted. Paper basketball got 11 votes. Robot drawing got 8. "
            "Seated charades got 7.\n\n"
            "C. Everyone has a sheet of paper and a pencil."
        ),
        rubric=(
            "Look at clue A. Which rule would the draft break?",
            "Could you change the game so everyone can play at their desk?",
        ),
        steps=(
            ("Check the choices", "Which game would you pick? Tell a partner which clue helped you decide.",
             "{{topic}}\n\n{{context}}\n\nList the games that fit the rules."),
            ("Pick a game", "Would you pick a different game or find a way to play paper basketball without throwing?",
             "Here are the choices:\n{{output[-1]}}\n\nPick one game for {{audience}} and give a reason."),
            ("Tell the class", "Give everyone something they can do right now.",
             "Use this game choice:\n{{output[-1]}}\n\nCheck it against the class rules:\n{{context}}\n\n"
             "Write a quick announcement with simple directions."),
        ),
        outputs=(
            "Paper basketball got the most votes. Robot drawing and seated charades can both be played "
            "at your desk without throwing.",
            "Let's play paper basketball. It got the most votes! Crumple your paper into a ball "
            "and toss it into the recycling bin from your desk.",
            "Grab your pencil. We're drawing robots for rainy recess! Robot drawing got 8 votes, "
            "the most of the games we can play at our desks. Clue A says we have to stay seated and skip throwing.\n\n"
            "You have one minute to draw a robot that can dry the playground. Then hold up your page "
            "and tell us what your robot's strangest button does.",
        ),
    ),
    "missing-mascot": ProfessionalCase(
        title="Where did the mascot go?",
        topic="Where should we look for our missing stuffed tiger?",
        audience="Our class of clue hunters",
        description="The class tiger is missing. An orange scrap looks like a big clue. Is it?",
        context=(
            "A. Tuck, the class's stuffed tiger, was on the reading chair before lunch. "
            "The chair was empty when the class got back.\n\n"
            "B. A scrap of orange felt was on the library cart. The art club cut orange felt "
            "for bookmarks that morning.\n\n"
            "C. The classroom helpers left a note by the door. “We put toys in the blue basket "
            "before we swept the floor.”"
        ),
        rubric=(
            "Say what the orange scrap could be.",
            "Use the helpers' note to pick a place to look.",
            "Say what you still need to find out.",
        ),
        steps=(
            ("Read the clues", "Which clues tell us what happened? Which leave room for a guess?",
             "Read the clues:\n{{context}}\n\nTell {{audience}} what we know about the missing tiger."),
            ("Check the guess", "Does the scrap tell you where Tuck is?",
             "Read this list:\n{{output[-1]}}\n\nSuggest a place to look. Say what makes it a good guess."),
            ("Plan the search", "Tell the class where to look and what to check next.",
             "Use this checked guess:\n{{output[-1]}}\n\nCheck it against the clues:\n{{context}}\n\n"
             "Write two short things the class can do to find Tuck."),
        ),
        outputs=(
            "Tuck was on the chair before lunch. There's orange felt on the library cart. "
            "The art club also used orange felt. The helpers say they moved toys to the blue basket.",
            "Tuck must be in the library. We found an orange scrap on the library cart, "
            "so that proves the cart carried him away.",
            "Look in the blue basket first. The helpers' note in clue C says they put toys there "
            "before they swept. Tuck could be with them.\n\n"
            "If the basket is empty, ask a helper if they saw Tuck. The scrap on the library cart "
            "could be from a bookmark, so we still need to find out where he went.",
        ),
    ),
    "paper-bridge": ProfessionalCase(
        title="Build a bridge for 8 cubes",
        topic="How can one sheet of paper hold eight cubes?",
        audience="The next group at the building table",
        description="One sheet of paper. Two books. Eight cubes to hold up. Fix the directions before the next team tries them.",
        context=(
            "A. Use one sheet of paper and two books a hand's width apart. Leave the books where they are. No tape.\n\n"
            "B. Three teams tested bridges. Flat paper held 3 cubes. Paper folded once held 6. "
            "Paper folded back and forth like a fan held 12.\n\n"
            "C. The teams put the cubes in the middle, one at a time. The goal is to hold 8."
        ),
        rubric=(
            "Choose a fold that held at least eight cubes.",
            "Tell the next team how to fold and place the paper.",
            "Tell the team how to try the cubes.",
        ),
        steps=(
            ("Read the test results", "Which bridges held eight cubes or more?",
             "Read the test notes:\n{{context}}\n\nSay which fold met the goal. Use the numbers."),
            ("Check the directions", "Would these directions make the bridge that held twelve?",
             "Use these results:\n{{output[-1]}}\n\nDraft two short directions for {{audience}}."),
            ("Pass on the plan", "Write directions the next team can follow from start to finish.",
             "Use these checked directions:\n{{output[-1]}}\n\nCheck them against the test notes:\n{{context}}\n\n"
             "Write three short steps. Use one sheet of paper and say how to check if the bridge works."),
        ),
        outputs=(
            "Eight is the goal. Flat paper held 3 cubes. Paper with one fold held 6. "
            "The fan fold held 12. That's the only one that held at least 8.",
            "Fold the sheet in half once, then open it a little and put it across the books. "
            "This fold held 12 cubes in the test. Add the cubes in the middle, one at a time.",
            "1. Fold one sheet back and forth like a fan. Open the folds a little.\n"
            "2. Lay the paper across the gap with one end on each book.\n"
            "3. Add cubes in the middle, one at a time. Can your bridge hold eight?\n\n"
            "Clue B is why we tried the fan fold. It held twelve cubes in the test.",
        ),
    ),
}


PARENT_CASES = {
    "family-game": ClassroomCase(
        title="Make a game for family night",
        topic="Can we make a five-minute game with one pencil?",
        audience="Four people at a family game night",
        description="Turn one sheet of paper and one pencil into a game everyone can play.",
        context=(
            "A. Four people have five minutes to play. Everyone can sit at the same table.\n\n"
            "B. The whole group has one sheet of paper and one pencil.\n\n"
            "C. The youngest player can draw shapes but is still learning to read."
        ),
        rubric=(
            "Check clue B. How can everyone play with one pencil?",
            "Does a player need to read to take a turn?",
        ),
        steps=(
            ("Find the rules", "What does your game have to make room for?",
             "Read these clues:\n{{context}}\n\nList what a game for {{audience}} needs to do."),
            ("Draft a game", "Check the supplies. Could all four people play this way?",
             "Use these rules:\n{{output[-1]}}\n\nDraft a quick drawing game for {{audience}}."),
            ("Make a game card", "Write rules someone can play from right away.",
             "Use this checked plan:\n{{output[-1]}}\n\nCheck it against these clues:\n{{context}}\n\n"
             "Write a game card with a name, supplies, rules, and one example turn."),
        ),
        outputs=(
            "We need a game for four people at one table. It should take about five minutes, "
            "use one sheet and one pencil for the whole group, and work without reading.",
            "Play Build a Creature. Give everyone their own sheet of paper and pencil. Each person "
            "adds one part to their creature, then everyone passes their drawing to the left. "
            "After two rounds, show all four drawings.",
            "Pass the Creature\n\n"
            "You need one sheet of paper and one pencil for all four players.\n\n"
            "1. The first player draws a shape for the creature's body. Pass the paper and pencil to the left.\n"
            "2. Take turns adding one part. Count slowly to ten for each turn, then pass both. "
            "Keep going until the paper has gone around twice.\n"
            "3. Hold up the drawing. Give your creature a name out loud.\n\n"
            "Example turn. If you get a creature with two feet, give it a third foot or a long tail. "
            "Then pass the paper and pencil together.",
        ),
        try_next=(
            "Teach the game to a parent or another grown-up at home. Play with whoever is there. "
            "After one round, ask which rule you could change to make the creature sillier."
        ),
    ),
    "memory-comic": ClassroomCase(
        title="Turn a memory into a comic",
        topic="How can we draw one funny breakfast in four panels?",
        audience="Someone who missed the pancake breakfast",
        description="A pancake flip went sideways. Keep the real surprise when you plan a four-panel comic.",
        context=(
            "A. Jo and Grandma made pancakes on Saturday. Grandma slid a spatula under the first pancake.\n\n"
            "B. The pancake landed back in the pan folded in half. Jo said, “Pancake taco!”\n\n"
            "C. They both laughed. They cut the folded pancake in two and each ate half."
        ),
        rubric=(
            "Read clue B. Where did the pancake land?",
            "Which words can go in Jo's speech bubble?",
        ),
        steps=(
            ("Pick the moments", "What happened right before the funny part?",
             "Read this memory:\n{{context}}\n\nList the moments {{audience}} needs to see in order."),
            ("Plan the panels", "Check the moment that gets the laugh. What did the draft change?",
             "Use these moments:\n{{output[-1]}}\n\nDraft four panels for a comic."),
            ("Make a drawing plan", "Make each box easy to draw from a short note.",
             "Use this checked plan:\n{{output[-1]}}\n\nCheck it against the memory:\n{{context}}\n\n"
             "Describe what to draw in each of four boxes. Use the words from the memory for any dialogue."),
        ),
        outputs=(
            "Grandma got ready to flip a pancake. It landed in the pan folded in half. "
            "Jo called it a pancake taco. They laughed and shared it.",
            "1. Grandma gets ready to flip.\n"
            "2. The pancake flies out of the pan and lands on the floor.\n"
            "3. Jo says, “Pancake taco!”\n"
            "4. Jo and Grandma share the pancake.",
            "1. Draw Grandma holding a spatula under a flat pancake. Put Jo beside her, watching.\n"
            "2. Draw the pancake back in the pan. Show the bent edge so it looks folded in half.\n"
            "3. Draw Jo pointing toward the pan. Put “Pancake taco!” in Jo's speech bubble.\n"
            "4. Draw them laughing at the table, each with half of the folded pancake.",
        ),
        try_next=(
            "Draw this comic or make four boxes for a memory of your own. Show it to a parent or "
            "another grown-up and ask which box tells them what happened."
        ),
    ),
    "home-invention": ClassroomCase(
        title="Invent a fix for home",
        topic="Can a paper invention keep two pencils from rolling away?",
        audience="The people who share the drawing table",
        description="Pencils keep rolling away. Sketch a paper invention you can build and test at home.",
        context=(
            "A. Two pencils keep rolling off the edge of the table while Mina draws.\n\n"
            "B. The table needs to be clear for dinner. The holder has to lift away in one piece. "
            "Tape can touch the paper but can't stick to the table.\n\n"
            "C. Mina can use one sheet of stiff paper and a little tape. Both pencils should fit."
        ),
        rubric=(
            "Can you clear the table without peeling anything off it? Check clue B.",
            "Where would the two pencils sit? What could stop them from rolling out?",
        ),
        steps=(
            ("Find the job", "What should the invention do when drawing time is over?",
             "Read the clues:\n{{context}}\n\nList the jobs an invention for {{audience}} has to do."),
            ("Sketch a fix", "Check where the tape goes. Can the invention lift away?",
             "Use these jobs:\n{{output[-1]}}\n\nDescribe a quick sketch for a pencil holder."),
            ("Show how it works", "Give someone enough to sketch it, make it, and try it.",
             "Use this checked sketch:\n{{output[-1]}}\n\nCheck it against the clues:\n{{context}}\n\n"
             "Give a drawing plan, a one-sentence pitch, and a simple test with two pencils."),
        ),
        outputs=(
            "The holder needs to stop two pencils from rolling. It should lift off the table in one piece. "
            "We have one sheet of stiff paper and some tape that can stick to the paper.",
            "Fold up the long edges of a sheet to make a tray. Tape the bottom of the tray to the table "
            "so it stays put. Set two pencils in the middle.",
            "Pencil Parking\n\n"
            "Sketch it. Draw a long paper tray with four folded-up edges. Draw two pencils lying side by side "
            "inside. Mark a bit of tape at each corner, where two paper edges meet.\n\n"
            "Make it. Set two pencils on one sheet of stiff paper so you can see how wide the bottom needs to be. "
            "Fold up the four edges and pinch the paper at the corners. Tape the pinched paper together.\n\n"
            "Pitch it. This little tray gives both pencils a parking spot and lifts away when it's time to eat.\n\n"
            "Test it. Give each pencil a gentle sideways push. Does a wall stop it? Pick up the tray with both "
            "pencils inside and set it down somewhere else. Do they stay in?",
        ),
        try_next=(
            "Fold and test your own holder. Show a parent or another grown-up what happened, "
            "then point to one part you'd change for a second try."
        ),
    ),
}


CLASSROOM_CASES = {
    **_FIRST_CLASSROOM_CASES,
    "missing-mascot": ClassroomCase(
        title="Where did the mascot go?",
        topic="Where should we look for Tuck?",
        audience="Our class of clue hunters",
        description="The class photo is in five minutes and Tuck the tiger is missing. Which lead would you follow?",
        context=(
            "A. Tuck, the class's stuffed tiger, was on the reading chair before lunch. "
            "Now the chair is empty, and the class photo is in five minutes.\n\n"
            "B. The library cart rolled past the chair at lunch. There’s orange felt on its handle. "
            "Tuck has orange felt ears, and the art club used the same felt for bookmarks.\n\n"
            "C. A helper’s note says they moved some toys into the blue basket before sweeping."
        ),
        rubric=(
            "Look at clue B. What else could the orange felt be from?",
            "Clue C says the helpers moved some toys. Does it name Tuck?",
        ),
        steps=(
            ("Read the clues", "You have time to check one place before the photo. Where would you look first?",
             "Read the clues:\n{{context}}\n\nTell {{audience}} what we know about the missing tiger."),
            ("Check the guess", "Tell the class where to look first and which clue sent you there.",
             "Read these clues:\n{{output[-1]}}\n\nSuggest a place to look and give one reason."),
            ("Plan the search", "Give the class a first place to look and a backup plan.",
             "Use this search plan:\n{{output[-1]}}\n\nCheck it against the clues:\n{{context}}\n\n"
             "Write two short things the class can do to find Tuck. Say what we still need to check."),
        ),
        outputs=(
            "The cart passed Tuck’s chair. The helpers moved some toys. We have two places to check "
            "and nobody in the clues says they saw Tuck move.",
            "Tuck has orange ears. That orange felt on the cart proves he rode to the library. "
            "Tell everyone we’ve found him.",
            "I’d check the blue basket first. Clue C says a helper put toys there, so Tuck might be in it.\n\n"
            "If it’s empty, ask who pushed the cart and look under the books. The orange scrap could be "
            "from Tuck or from a bookmark.",
        ),
        last_clue=(
            "The basket is empty. Just before the photo, the librarian rolls back the cart and lifts "
            "Tuck out from under a stack of books. The orange scrap was from a bookmark! "
            "What can you say for sure now? Which clue lets you say it?"
        ),
    ),
    "paper-bridge": ClassroomCase(
        title="Build a bridge for 8 cubes",
        topic="Can you fix the bridge before it buckles?",
        audience="The next group at the building table",
        description="Two teams made the same fan fold. One bridge held 12 cubes. The other held 4. What changed?",
        context=(
            "A. Use one sheet of paper and two books a hand’s width apart. No tape.\n\n"
            "B. Both teams folded their paper back and forth like a fan. With the folds running "
            "from book to book, the bridge held 12 cubes. Turned sideways, it held 4.\n\n"
            "C. Both teams added cubes to the middle, one at a time. Your bridge needs to hold 8."
        ),
        rubric=(
            "Trace a raised fold with your finger. Does it lead from one book to the other?",
            "Check clue B for the number of cubes each setup held.",
        ),
        steps=(
            ("Read the test results", "Same paper, same fold, different result. What would you tell the next team to check?",
             "Read the test notes:\n{{context}}\n\nList what the teams kept the same and what they changed."),
            ("Check the directions", "Fix the directions so a partner knows which way to point the folds.",
             "Use these results:\n{{output[-1]}}\n\nWrite directions for {{audience}}."),
            ("Pass on the plan", "Give the next team steps they can build from.",
             "Use these corrected directions:\n{{output[-1]}}\n\nCheck the test notes:\n{{context}}\n\n"
             "Write three short steps that explain the fold, which way it faces, and how to test it."),
        ),
        outputs=(
            "Both teams used the same fan fold and added cubes in the same spot. "
            "They turned the paper different ways and got two different results.",
            "Fold the paper back and forth like a fan. Lay it across the books with the folds "
            "pointing sideways. That’s how the team held 12 cubes!",
            "1. Fold one sheet back and forth like a fan. Open the folds a little.\n"
            "2. Set it across the books. Trace a fold with your finger. Your finger should travel from one book to the other.\n"
            "3. Add cubes in the middle one at a time. Does your bridge hold eight?\n\n"
            "Clue B says this setup held 12 cubes when the teams tested it.",
        ),
        try_next=(
            "Read your fix to a partner. Ask them to point the folds the way you described. "
            "If you have paper, books, and cubes, see if their bridge holds eight."
        ),
    ),
    **PARENT_CASES,
    **CHAIN_BUILDING_CASES,
}


def classroom_case_for_run(slug: str, saved_clues: str) -> ProfessionalCase:
    # The run keeps its original clues, so a resumed challenge needs the matching replies.
    first_case = _FIRST_CLASSROOM_CASES.get(slug)
    if first_case is not None and saved_clues == first_case.context:
        return first_case
    return CLASSROOM_CASES[slug]
