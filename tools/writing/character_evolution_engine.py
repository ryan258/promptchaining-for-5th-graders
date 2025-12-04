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
            """Describe the core character as {{char_type}} with name, virtue, and a grounding detail.
Tone: {{tone}} | Genre: {{genre}} | Context: {{additional_context}}

Provide 1-2 sentence description; keep virtue specific.

Respond in JSON:
{
  "name": "name",
  "positive_trait": "trait",
  "description": "tight description"
}""",
            # Flaw
            """Give {{output[-1].name}} a specific, story-relevant flaw.
Keep it adult and stakes-bearing (not twee).

Respond in JSON:
{
  "flaw": "flaw description",
  "flaw_origin": "why this flaw exists"
}""",
            # Crucible challenge
            """Design a crucible challenge that forces {{output[-2].name}} to confront {{output[-1].flaw}}.
Make it situational, with external pressure.

Respond in JSON:
{
  "challenge": "scenario",
  "stakes": ["stake1", "stake2"]
}""",
            # Growth
            """Show the growth beat: how does {{output[-3].name}} adapt when facing {{output[-1].challenge}} with stakes {{output[-1].stakes}}?
Keep it concise and credible.

Respond in JSON:
{
  "growth": "behavior change",
  "new_capability": "what they can now do",
  "cost": "what it costs them"
}""",
            # New adventure hook
            """Pitch a new adventure that showcases the transformed character.
Tie to genre and prior cost; include a simple logline.
Keep synopsis 3-5 sentences.

Respond in JSON:
{
  "new_adventure": "short synopsis",
  "logline": "one-liner",
  "foil_or_ally": "who challenges or supports the growth"
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
