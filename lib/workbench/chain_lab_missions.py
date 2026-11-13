"""Editable starting missions for the offline Chain Lab."""

from .kid_insight_missions import KID_INSIGHT_MISSIONS
from .models import Recipe, SavedRecipe
from .recipes import step


STARTER_MISSIONS: dict[str, SavedRecipe] = {
    "midnight-museum": SavedRecipe(
        topic="Get the moon rock to the display before the museum opens.",
        context=(
            "You have six minutes. The east route takes four minutes through the planet room and the lift. "
            "The west route takes five minutes through the telescope hall and the ramp. "
            "Both start in the storeroom and end at the display. Keep the rock in its padded box."
        ),
        recipe=Recipe(
            title="Race through the Moon Museum",
            description="Make a route, test it when a new clue arrives, then save a plan the night crew can follow.",
            audience="The night crew at the Moon Museum",
            steps=[
                step(
                    "Plan a route",
                    "Give the night crew a first plan they can put to the test.",
                    "Find the quickest route that follows the rules. Name the stops, count the minutes, "
                    "and include the rule about the box.\n\nMission\n{{topic}}\n\nMuseum notes\n{{context}}",
                ),
                step(
                    "Check the lift",
                    "Give this step the old plan and the museum notes so it can check both.",
                    "A radio call just came in. The lift is out of service. Check whether the first route still works. "
                    "If it fails, give a route that fits the time and explain your choice.\n\n"
                    "First route\n{{output[-1]}}\n\nMuseum notes\n{{context}}",
                ),
                step(
                    "Send the crew a plan",
                    "Use the check to update the first plan. Keep the rule about the box.",
                    "Write a three-line radio message the crew can follow. Include the route, the total time, "
                    "and what to do with the box.\n\nFirst route\n{{output[-2]}}\n\nLift check\n{{output[-1]}}",
                ),
            ],
        ),
    ),
    "alien-field-guide": SavedRecipe(
        topic="Make a field guide page for the puddle puff from Planet Ooze.",
        context=(
            "A puddle puff has a round body and two wide feet. The explorer saw it hop over a crack "
            "and slide down a muddy slope. It stopped under a leaf in the shade. Another puff was seen "
            "beside a pool, where it ducked behind a rock. Nobody saw what either puff ate."
        ),
        recipe=Recipe(
            title="Meet a creature from Planet Ooze",
            description="Send two explorers to look for different clues, then combine their notes into a field guide page.",
            audience="The next team of space explorers",
            steps=[
                step(
                    "Watch how it moves",
                    "Give one explorer the sighting notes and a job about movement.",
                    "Write two things the explorer saw the puddle puff do. For each, say where it happened.\n\n"
                    "Sighting notes\n{{context}}",
                ),
                step(
                    "Look for hiding spots",
                    "Give the other explorer the same notes and a different job.",
                    "Name two places a puddle puff might hide. Use a clue for each. "
                    "Add one question about the creature that the notes leave open.\n\nSighting notes\n{{context}}",
                ),
                step(
                    "Make the field guide page",
                    "Give the writer both explorers’ answers. What can the reader learn from each one?",
                    "Make a short field guide page with a title, a clue for spotting the creature in motion, "
                    "a place to look, and one thing to find out next. Make it clear which details the explorers saw "
                    "and which ones are guesses.\n\nMovement notes\n{{output[-2]}}\n\nHiding notes\n{{output[-1]}}",
                ),
            ],
        ),
    ),
    "robot-recess": SavedRecipe(
        topic="Teach the recess robot how to run a round of Freeze Frame.",
        context=(
            "Four to six players stand on their own spots. A caller names something to act out, like a wobbly tower. "
            "Everyone else makes a pose in their spot. When the caller says “Freeze,” hold the pose for a count of three. "
            "Everyone stays in the game. Pick a new caller for the next round."
        ),
        recipe=Recipe(
            title="Teach the recess robot a game",
            description="Give a new player and a referee different directions using the same rules.",
            audience="Kids at indoor recess",
            steps=[
                step(
                    "Write the rules",
                    "Make one set of rules both audiences can use.",
                    "Write the rules in order. Include what the caller does, what the players do, "
                    "and how the next round starts.\n\nGame notes\n{{context}}",
                ),
                step(
                    "Teach a new player",
                    "Use the rules to give a first-time player one turn to try.",
                    "Talk straight to a kid who just joined. Explain what to do in one round in three short lines.\n\n"
                    "Game rules\n{{output[-1]}}",
                ),
                step(
                    "Help the referee",
                    "Reuse the rules from Step 1 for a new audience. This job needs a different kind of answer.",
                    "Make a referee’s cue card. Include when to say “Freeze,” what to do if someone moves, "
                    "and when to switch callers.\n\nGame rules\n{{output[-2]}}",
                ),
                step(
                    "Compare the cards",
                    "Check that the cards teach the same game. Save a card each person can use.",
                    "Check both cards against the rules. The player and the referee should agree on who stays "
                    "in the game and when the caller changes. Return two corrected cards with a title on each.\n\n"
                    "Game rules\n{{output[-3]}}\n\nPlayer card\n{{output[-2]}}\n\nReferee card\n{{output[-1]}}",
                ),
            ],
        ),
    ),
    "sock-arcade": SavedRecipe(
        topic="Invent a sock-toss game two people can learn in one minute.",
        context=(
            "You have two rolled-up socks, an empty laundry basket, and a clear spot on the floor. "
            "Use soft underhand tosses from the same spot. Play for up to five minutes."
        ),
        recipe=Recipe(
            title="Build a sock arcade",
            description="Invent a game, try the rules with a player, and turn what you learn into a better game card.",
            audience="Two players at home",
            steps=[
                step(
                    "Invent a game",
                    "Ask for a short game you could actually try at home.",
                    "Invent a game with a silly name. Say how to set up, what a turn looks like, "
                    "how to score, and when the game ends.\n\nGoal\n{{topic}}\n\nSupplies and rules\n{{context}}",
                ),
                step(
                    "Try two turns",
                    "Let a player use your draft rules. Save what they actually did or asked.",
                    "Try two turns or act them out on paper. For one toss, pretend a sock hits the rim and drops outside. "
                    "Write down what the player did, the score, and one rule that could be clearer.\n\n"
                    "First rules\n{{output[-1]}}",
                ),
                step(
                    "Fix a rule",
                    "Use the playtest answer to decide what to change.",
                    "Name the moment that could confuse a new player. Write one replacement rule, "
                    "then say how it would change that turn.\n\nFirst rules\n{{output[-2]}}\n\n"
                    "Playtest notes\n{{output[-1]}}",
                ),
                step(
                    "Make the game card",
                    "Give the last step both the first rules and your fix.",
                    "Write a rules card a new player can read in one minute. Include the setup, how to take a turn "
                    "and score, and when to stop. Work in the new rule and show a one-turn example.\n\n"
                    "First rules\n{{output[-3]}}\n\nRule fix\n{{output[-1]}}",
                ),
            ],
        ),
    ),
}


CHAIN_LAB_MISSIONS = {**STARTER_MISSIONS, **KID_INSIGHT_MISSIONS}
