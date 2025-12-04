#!/usr/bin/env python3
"""
🎭 Character Evolution Engine (adult mode)

Design a character arc with traits, flaw, crucible challenge, growth, and a follow-on adventure.

Usage:
    python tools/writing/character_evolution_engine.py "Character type (e.g., washed-up PI)"
    python tools/writing/character_evolution_engine.py "Character" --context "Genre, constraints, tone"
"""

import os
import json
from datetime import datetime

try:
    from tools.tool_utils import setup_project_root, load_user_context, get_input_from_args
except ImportError:
    import sys
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
    from tools.tool_utils import setup_project_root, load_user_context, get_input_from_args

project_root = setup_project_root(__file__)

from chain import MinimalChainable
from main import build_models, prompt


def character_evolution_engine(character_type: str, additional_context: str = ""):
    print("🎭 Character Evolution Engine")
    print(f"Character type: {character_type}")
    if additional_context:
        print(f"Context: {additional_context}")
    print()

    user_profile = load_user_context(project_root)
    tone = user_profile.get("writing_style", {}).get("tone", "Lean and evocative")
    genre = user_profile.get("writing_style", {}).get("genre", "")

    client, model_names = build_models()
    model_info = (client, model_names[0])

    context_data = {
        "char_type": character_type,
        "tone": tone,
        "genre": genre,
        "additional_context": additional_context,
    }

    result, context_filled_prompts, usage_stats = MinimalChainable.run(
        context=context_data,
        model=model_info,
        callable=prompt,
        prompts=[
            # Baseline character
            """You are a Screenwriter and Narrative Designer. Create a "Compelling Protagonist".

Tone: {{tone}} | Genre: {{genre}} | Context: {{additional_context}}
Character Type: {{char_type}}

Perspective Framework:
- The "Ghost": A past event that haunts them.
- The "Lie": A misconception they have about themselves.

Constraints:
- Description: Exactly 2 sentences (Appearance + Vibe).
- Virtue: A specific skill or moral strength (e.g., "Loyalty to a fault").
- Name: Genre-appropriate.

Respond in JSON:
{
  "name": "Name",
  "positive_trait": "Specific Virtue",
  "description": "Evocative description."
}""",
            # Flaw
            """Give {{output[-1].name}} a "Fatal Flaw" (Hamartia).

Constraints:
- Flaw: A psychological or moral weakness (not physical).
- Origin: The "Ghost" event that created this flaw (Max 1 sentence).

Respond in JSON:
{
  "flaw": "Specific flaw (e.g., 'Cannot trust authority')",
  "flaw_origin": "Backstory event (e.g., 'Betrayed by mentor')"
}""",
            # Crucible challenge
            """Design the "Inciting Incident" or "Midpoint Climax". Force them to face the Flaw.

Constraints:
- Challenge: A specific external pressure (e.g., "Must trust a rival").
- Stakes: Exactly 2 consequences of failure (Internal + External).

Respond in JSON:
{
  "challenge": "Scenario description",
  "stakes": ["Internal Stake (e.g., 'Self-respect')", "External Stake (e.g., 'The mission')"]
}""",
            # Growth
            """Show the "Character Arc". How do they overcome the Flaw?

Constraints:
- Growth: A specific behavioral change (Action, not just thought).
- New Capability: What they can do now that they couldn't before.
- Cost: What they lost to get here (e.g., "Innocence").

Respond in JSON:
{
  "growth": "Description of change",
  "new_capability": "New skill/perspective",
  "cost": "Sacrifice made"
}""",
            # New adventure hook
            """Pitch the sequel. Where does the "New Self" go next?

Constraints:
- Synopsis: Exactly 3 sentences.
- Logline: One punchy sentence.
- Foil: A character who tests the *new* strength.

Respond in JSON:
{
  "new_adventure": "Synopsis",
  "logline": "Logline",
  "foil_or_ally": "Character description"
}"""
        ],
        return_usage=True,
    )

    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    output_dir = os.path.join(project_root, "output", "writing", "character_evolution_engine")
    os.makedirs(output_dir, exist_ok=True)

    output_path = os.path.join(output_dir, f"{timestamp}-character_evolution.json")
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2)

    log_file = MinimalChainable.log_to_markdown("character_evolution_engine", context_filled_prompts, result, usage_stats)

    print(f"✅ Saved JSON to: {output_path}")
    print(f"✅ Log saved to: {log_file}")


def main():
    character_type, context = get_input_from_args(
        description="Generate a character arc with flaw, challenge, growth, and new adventure"
    )
    character_evolution_engine(character_type, context)


if __name__ == "__main__":
    main()
