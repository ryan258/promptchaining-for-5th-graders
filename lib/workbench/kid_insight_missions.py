"""Offline Chain Lab missions for investigating a surprising result."""

from .models import Recipe, SavedRecipe, Step


_ICE_REMATCH_PROCEDURE = (
    "1. Set two identical empty cups side by side in the shade. Put a paper sleeve on one cup.\n"
    "2. Put one fresh, equal-size ice cube in each cup at the same time. Start one timer immediately.\n"
    "3. Watch both cups. Record the elapsed time for each cup as its last visible ice disappears.\n"
    "4. Stop the timer as soon as both cups are clear of visible ice."
)


KID_INSIGHT_MISSIONS: dict[str, SavedRecipe] = {
    "ice-cup-test": SavedRecipe(
        topic="Does a paper sleeve help ice last longer?",
        context=(
            "The science club used two identical cups and equal ice cubes. The ice in the bare cup in the sun "
            "melted in 9 minutes. The ice in the cup with a paper sleeve in the shade melted in 18 minutes. "
            "The club has two fresh equal cubes, the same cups, and a timer for one more test."
        ),
        recipe=Recipe(
            title="What really helps the ice last?",
            description="Find the extra change that made a test hard to read, then design a fair rematch.",
            steps=[
                Step(
                    name="Compare the cups",
                    purpose="Find everything that changed between the two cups.",
                    prompt=(
                        "Goal\n{{topic}}\n\nTest notes\n{{context}}\n\nList what stayed the same, what changed, "
                        "and the two times reported for the first test. Explain why the sleeve and the shade could "
                        "both matter. Say which change the club wants to test next."
                    ),
                ),
                Step(
                    name="Set up a fair rematch",
                    purpose="Change one thing so the result answers the club’s question.",
                    prompt=(
                        "Copy the rematch procedure exactly. Use the comparison and notes to explain "
                        "in one sentence why the rematch tests the sleeve."
                        "\n\nComparison\n{{output[-1]}}\n\n"
                        "Test notes\n{{context}}\n\nRematch procedure\n"
                        + _ICE_REMATCH_PROCEDURE
                    ),
                ),
                Step(
                    name="Predict two results",
                    purpose="Decide in advance what each result would tell you.",
                    prompt=(
                        "Write a test card a partner can follow. Copy the rematch procedure exactly. "
                        "Use the earlier plan to explain why the setup is fair if that explanation fits the "
                        "procedure. Leave both new times blank. Label two predictions. A longer melt time "
                        "for the sleeved cup would support the idea. An equal or shorter time would make you "
                        "question it. Treat a difference that's hard to measure as uncertain."
                        "\n\nEarlier plan\n{{output[-1]}}\n\nRematch procedure\n"
                        + _ICE_REMATCH_PROCEDURE
                    ),
                ),
            ],
        ),
    ),
    "sticker-machine-rule": SavedRecipe(
        topic="How could you tell which rule the sticker machine follows?",
        context=(
            "A pretend machine prints a gold dot on some cards. Two red stars got dots. A blue square and "
            "a green circle got no dots. The test pile has a blue star, a red circle, and another red star. "
            "One partner will run the machine using a secret rule."
        ),
        recipe=Recipe(
            title="Catch the sticker machine’s rule",
            description="Find two rules that fit the same clues and pick a card that tells them apart.",
            steps=[
                Step(
                    name="Find two possible rules",
                    purpose="See how color and shape could both fit the first clues.",
                    prompt=(
                        "Use the notes to write one rule about color and one about shape. For each rule, show "
                        "why all the cards tried so far would get the results we saw."
                        "\n\nGoal\n{{topic}}\n\nMachine notes\n{{context}}"
                    ),
                ),
                Step(
                    name="Find the telling card",
                    purpose="Choose a test card that gives the two rules different answers.",
                    prompt=(
                        "Pick one unused card that would give different results under the two rules. Predict "
                        "whether it gets a dot under each rule, and say why another red star would tell us less."
                        "\n\nRules\n{{output[-1]}}\n\nMachine notes\n{{context}}"
                    ),
                ),
                Step(
                    name="Challenge a partner",
                    purpose="Try the test without peeking at the secret rule.",
                    prompt=(
                        "Write a two-person challenge. Tell the machine player how to pick one of the two rules "
                        "in secret, then tell the tester what to try and what a dot or no dot would suggest. "
                        "Leave a blank for the real result.\n\nPossible rules\n{{output[-2]}}\n\nTest card\n{{output[-1]}}"
                    ),
                ),
            ],
        ),
    ),
    "lunch-line-bottleneck": SavedRecipe(
        topic="Which part of the lunch line should we try to speed up?",
        context=(
            "A lunch monitor timed three parts of the line. Sam spent 1 minute getting a tray, 4 at the food "
            "choices, and 1 checking out. Lee spent 1 minute getting a tray, 5 at the food choices, and 1 "
            "checking out. Neither had seen the menu before reaching the food counter. A menu sign could go by the trays."
        ),
        recipe=Recipe(
            title="Where does the lunch line slow down?",
            description="Break a wait into pieces and find where a small change could save the most time.",
            steps=[
                Step(
                    name="Break down the wait",
                    purpose="Compare the parts of both trips through the line.",
                    prompt=(
                        "Add up Sam’s and Lee’s times. Then compare the three parts of the line. Which part took "
                        "longest for both students? Include the minutes that show it."
                        "\n\nGoal\n{{topic}}\n\nLunch monitor notes\n{{context}}"
                    ),
                ),
                Step(
                    name="Aim the change",
                    purpose="Put the fix where it can affect the slow part.",
                    prompt=(
                        "Use the time breakdown to compare a faster tray pickup with an earlier menu sign. "
                        "Which would you try first? Say what the timing shows and what you are guessing about "
                        "the reason for the wait.\n\nTime breakdown\n{{output[-1]}}\n\nNotes\n{{context}}"
                    ),
                ),
                Step(
                    name="Give the monitor a test",
                    purpose="Decide what to time to see whether the change helps.",
                    prompt=(
                        "Write a short proposal for the lunch monitor. Name the change and where it would go. "
                        "Time each part and the whole trip from trays to checkout again under similar conditions. "
                        "Say how you could tell whether the wait got shorter or moved to another part of the line."
                        "\n\nFirst timing\n{{output[-2]}}\n\nYour idea\n{{output[-1]}}"
                    ),
                ),
            ],
        ),
    ),
    "first-vote-trap": SavedRecipe(
        topic="What should the club make based on all 20 votes?",
        context=(
            "The craft club gave each person one vote for making puppets or bookmarks. At the first table, "
            "8 picked puppets and 2 picked bookmarks. At the second table, 0 picked puppets and 10 picked "
            "bookmarks. The club is sharing the results for the 20 people who voted."
        ),
        recipe=Recipe(
            title="Spot the trap in the first vote",
            description="Compare two groups and see how the winner changes when everyone’s vote counts.",
            steps=[
                Step(
                    name="Read the first tally",
                    purpose="Find what the first ten people preferred.",
                    prompt=(
                        "Report the first table’s two vote counts and its winner in one sentence. "
                        "Make clear who voted in this tally.\n\nGoal\n{{topic}}\n\nVote notes\n{{context}}"
                    ),
                ),
                Step(
                    name="Count everyone",
                    purpose="Give each person one vote when you add the tables.",
                    prompt=(
                        "Add the two tables’ votes for each choice and name the overall winner. "
                        "How many votes separate the two choices?\n\nVote notes\n{{context}}"
                    ),
                ),
                Step(
                    name="Announce what changed",
                    purpose="Show why seeing one group first can lead you to the wrong conclusion.",
                    prompt=(
                        "Write a three-line club announcement with the first table’s winner, the overall winner "
                        "and counts, and one reason to wait for both tables. Keep the claim about the people "
                        "who actually voted.\n\nFirst table\n{{output[-2]}}\n\nBoth tables\n{{output[-1]}}"
                    ),
                ),
            ],
        ),
    ),
    "comic-swap-sign": SavedRecipe(
        topic="How can a sign explain a comic swap to more visitors?",
        context=(
            "At the school fair, visitors bring one comic to Table 3 and take one comic home. There’s no charge. "
            "Some visitors read only a few English words. The hallway is too loud to hear announcements, and "
            "signs will be printed in black and white. You can draw pictures and use short words."
        ),
        recipe=Recipe(
            title="Design a comic-swap sign",
            description="See the same directions from different viewpoints and make a sign more visitors can follow.",
            steps=[
                Step(
                    name="Think like a new visitor",
                    purpose="Find what a visitor needs to understand to join the swap.",
                    prompt=(
                        "Imagine you know only a few English words. List the three things you need to understand "
                        "to join the swap. Sketch in words a picture that could show one of them."
                        "\n\nGoal\n{{topic}}\n\nFair notes\n{{context}}"
                    ),
                ),
                Step(
                    name="Check the hallway",
                    purpose="Find which signals still work in a loud room with black-and-white signs.",
                    prompt=(
                        "From the fair notes, say what a sign can use in that hallway. Give one direction "
                        "that would fail if it depended on color or sound and show a replacement."
                        "\n\nFair notes\n{{context}}"
                    ),
                ),
                Step(
                    name="Make a sign to try",
                    purpose="Combine both viewpoints, then find out what a reader actually understands.",
                    prompt=(
                        "Draft a sign with short words and simple pictures described in brackets. Show where to go, "
                        "what to bring, and what happens at the swap. Cover the words and ask a partner to explain "
                        "what the pictures tell them. Then uncover the words and ask what became clearer."
                        "\n\nVisitor’s needs\n{{output[-2]}}\n\nHallway check\n{{output[-1]}}\n\n"
                        "Fair notes\n{{context}}"
                    ),
                ),
            ],
        ),
    ),
    "stamp-station-turns": SavedRecipe(
        topic="What turn rule lets every team finish its poster?",
        context=(
            "Three teams need the same stamp at the art table, which closes in 12 minutes. Moon needs 2 "
            "minutes to finish its required prints, Sun needs 4, and Star needs 6. Only one team can stamp "
            "at a time. Teams can make extra prints if time remains. The first proposal gives each team 4 minutes."
        ),
        recipe=Recipe(
            title="Make the stamp turns fair",
            description="Test equal turns against what each team needs, then write a rule everyone can use.",
            steps=[
                Step(
                    name="Try equal turns",
                    purpose="Look at who can finish with four minutes each.",
                    prompt=(
                        "For each team, compare four minutes with the time it needs. Say who has extra time, "
                        "who has just enough, and who is short.\n\nGoal\n{{topic}}\n\nArt table notes\n{{context}}"
                    ),
                ),
                Step(
                    name="Make a fair schedule",
                    purpose="Decide what fair means when teams need different amounts of time.",
                    prompt=(
                        "Use the first check and the table notes to make a turn schedule. Say when each team starts "
                        "and stops, how you know it fits in 12 minutes, and when a team could make an extra print."
                        "\n\nEqual-turn check\n{{output[-1]}}\n\nArt table notes\n{{context}}"
                    ),
                ),
                Step(
                    name="Try a surprise delay",
                    purpose="See whether the rule can handle a change everyone can see.",
                    prompt=(
                        "Imagine the station opens one minute late. Work out how much time is left and say what "
                        "you’d ask the teams to decide. Write one station rule and one backup question."
                        "\n\nSchedule\n{{output[-1]}}\n\nArt table notes\n{{context}}"
                    ),
                ),
            ],
        ),
    ),
    "seed-swap-countdown": SavedRecipe(
        topic="Can the garden club get its seed bags ready by 3:00?",
        context=(
            "It is 2:42. Writing all the seed labels takes 3 minutes and the ink needs 6 minutes to dry. "
            "Filling and sealing the seed bags takes 8 minutes. You may fill bags while the labels dry. "
            "Once the labels are dry and bags are filled, sticking on the labels takes 2 minutes. "
            "Checking the finished bags takes 2 more minutes. One person is doing the work."
        ),
        recipe=Recipe(
            title="Work backward from the seed swap",
            description="Find two jobs that can share the same minutes, then build a plan from the deadline back.",
            steps=[
                Step(
                    name="Find what has to happen first",
                    purpose="Sort jobs that must wait from work that can share the same minutes.",
                    prompt=(
                        "Draw the order in words. What has to be ready before the labels can go on? Which job can "
                        "happen while something else waits? Add the minutes if every task and wait happened in "
                        "separate blocks.\n\nGoal\n{{topic}}\n\nSeed swap notes\n{{context}}"
                    ),
                ),
                Step(
                    name="Count back from 3:00",
                    purpose="Find the latest safe start for each job.",
                    prompt=(
                        "Start at 3:00 and count backward from the final check. Make a timeline that uses the "
                        "drying time for filling bags. Give the latest time the first job can start."
                        "\n\nJob order\n{{output[-1]}}\n\nSeed swap notes\n{{context}}"
                    ),
                ),
                Step(
                    name="Tell the crew what to do now",
                    purpose="Turn the timeline into a plan someone can follow at 2:42.",
                    prompt=(
                        "Write a short start-now checklist for the garden club. Say what to start at 2:42, "
                        "what to do while the ink dries, and how many spare minutes the plan gives you."
                        "\n\nBackward timeline\n{{output[-1]}}\n\nSeed swap notes\n{{context}}"
                    ),
                ),
            ],
        ),
    ),
    "reading-jar-prediction": SavedRecipe(
        topic="What would it take for the reading jar to reach 40 on Friday?",
        context=(
            "Students add one slip to a jar for every chapter they read in class. At the end of Monday the jar "
            "had 8 slips. Tuesday it had 16, Wednesday 25, and Thursday 33. All four were regular school days. "
            "Friday is a half day and may have less reading time. The class goal is 40 slips."
        ),
        recipe=Recipe(
            title="Will the reading jar reach 40?",
            description="Make a prediction from a pattern, then check whether a shorter day changes what you expect.",
            steps=[
                Step(
                    name="Find the daily gains",
                    purpose="Compare how much the total grew between days.",
                    prompt=(
                        "Use the four totals to find how many slips were added on Tuesday, Wednesday, and Thursday. "
                        "Say what a regular day usually added in these notes."
                        "\n\nGoal\n{{topic}}\n\nReading jar notes\n{{context}}"
                    ),
                ),
                Step(
                    name="Predict a regular day",
                    purpose="Make a prediction that says what conditions it depends on.",
                    prompt=(
                        "Use the usual gain to give a likely range for the total after one more regular day. "
                        "Compare it with the goal of 40. State the condition your prediction depends on."
                        "\n\nDaily gains\n{{output[-1]}}\n\nReading jar notes\n{{context}}"
                    ),
                ),
                Step(
                    name="Update the Friday guess",
                    purpose="Use the pattern without assuming Friday works the same way.",
                    prompt=(
                        "Write a two-line prediction for the class. Say how many more slips you need on Friday, "
                        "why the regular-day pattern might miss, and one time you could check the jar to see how "
                        "close you are.\n\nRegular-day prediction\n{{output[-1]}}\n\nReading jar notes\n{{context}}"
                    ),
                ),
            ],
        ),
    ),
    "parade-one-question": SavedRecipe(
        topic="Which one question could settle where to hold the costume parade?",
        context=(
            "Rain moved the costume parade inside. All 27 kids need to take part together at 2:45. The hall "
            "holds 24. The gym has room for everyone if rehearsal ends before 2:45. The classroom has room "
            "for a seated costume show but too little open space for a parade. You can ask the office one question."
        ),
        recipe=Recipe(
            title="Ask the question that saves the parade",
            description="Work out which missing fact could change the plan, then make a backup for either answer.",
            steps=[
                Step(
                    name="Check the three spaces",
                    purpose="Separate choices you can make now from a choice that needs one more fact.",
                    prompt=(
                        "For each space, say whether it can hold the whole parade at 2:45. Mark which answer "
                        "depends on something we don’t know.\n\nGoal\n{{topic}}\n\nParade notes\n{{context}}"
                    ),
                ),
                Step(
                    name="Pick the deciding question",
                    purpose="Ask for information that changes what you can do.",
                    prompt=(
                        "Write one question for the office whose answer would help decide. Show how a yes and a no "
                        "would change your plan.\n\nSpace check\n{{output[-1]}}\n\nParade notes\n{{context}}"
                    ),
                ),
                Step(
                    name="Give both plans to the class",
                    purpose="Prepare a usable plan even before the answer arrives.",
                    prompt=(
                        "Write a short note for the class. Start with the question you’ll ask. Give one plan if "
                        "the gym is free, and another if it is still occupied. Make sure all 27 kids have a way to join."
                        "\n\nYour deciding question\n{{output[-1]}}\n\nParade notes\n{{context}}"
                    ),
                ),
            ],
        ),
    ),
    "scrap-paper-loop": SavedRecipe(
        topic="Which cleanup routine saves more time over two days?",
        context=(
            "After making posters, Table A recycled all its scraps in 2 minutes. The next day it took 6 minutes "
            "to get new paper. Table B spent 4 minutes saving scraps at least as big as a hand. The next day it "
            "took 1 minute to find enough paper in its scrap box. The tables made the same projects. The box "
            "fills up fast if teams keep tiny scraps too."
        ),
        recipe=Recipe(
            title="Find the hidden cost of a quick cleanup",
            description="Trace what a shortcut makes harder tomorrow, then plan a routine you can test this week.",
            steps=[
                Step(
                    name="Count both days",
                    purpose="Find the work that a quick cleanup can push into tomorrow.",
                    prompt=(
                        "Compare the two tables on cleanup day and on the next day. Add each table’s minutes "
                        "across both days. Say why the fastest cleanup and the fastest two-day routine can be different."
                        "\n\nGoal\n{{topic}}\n\nPaper notes\n{{context}}"
                    ),
                ),
                Step(
                    name="Decide what to keep",
                    purpose="Make the useful scraps easy to find in a small box.",
                    prompt=(
                        "Use the two-day totals to write one rule for what goes in the scrap box and when to look "
                        "there. Say how it keeps the box usable and what you’d do if the box fills up."
                        "\n\nTwo-day comparison\n{{output[-1]}}\n\nPaper notes\n{{context}}"
                    ),
                ),
                Step(
                    name="Make a class experiment",
                    purpose="Check the total work instead of timing only cleanup.",
                    prompt=(
                        "Write a short plan to try the rule on the next two art days. Name both times to record "
                        "and what result would make you keep or change the rule. Include one reason a different art "
                        "project might give a different result.\n\nFirst comparison\n{{output[-2]}}\n\nScrap rule\n{{output[-1]}}"
                    ),
                ),
            ],
        ),
    ),
}
