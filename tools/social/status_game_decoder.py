#!/usr/bin/env python3
"""
🧠 Status Game Decoder (adult mode)

Parse social interactions for signals, hierarchy, and the real game being played.

Usage:
    python tools/social/status_game_decoder.py "Describe the scene"
    cat situation.txt | python tools/social/status_game_decoder.py
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


def status_game_decoder(situation: str):
    print("🧠 Status Game Decoder")
    print(f"Situation: {situation[:160]}{'...' if len(situation) > 160 else ''}\n")

    user_profile = load_user_context(project_root)
    tone = user_profile.get("writing_style", {}).get("tone", "Observant and concise")

    client, model_names = build_models()
    model_info = (client, model_names[0])

    context_data = {
        "situation": situation,
        "tone": tone,
    }

    result, context_filled_prompts, usage_stats = MinimalChainable.run(
        context=context_data,
        model=model_info,
        callable=prompt,
        prompts=[
            # Surface analysis
            """You are an Evolutionary Psychologist and Sociologist. Decode the "Micro-Sociology" of this interaction.

Analyze the "Dramaturgy" (Goffman)—the performance of self.
Tone: {{tone}}

Situation:
{{situation}}

Perspective Framework:
- Face Work: How are they protecting their own/others' dignity?
- Politeness Theory: Positive face (need to be liked) vs Negative face (need for autonomy).

Constraints:
- Observations: Exactly 3 key dynamics.
- "Polite Person": Who is adhering to norms?
- "Rude Person": Who is violating norms?

Respond in JSON:
{
  "surface_analysis": "Description of the social friction",
  "polite_person": "Name (e.g., 'The Host')",
  "rude_person": "Name (e.g., 'The Interrupter')"
}""",
            # Status signals
            """Decode the "Signaling Game". Who is high status, and how do you know?

Look for "Costly Signals" and "Countersignaling".
Constraints:
- Identify exactly 5 signals.
- "Signal Type": Use specific terms (e.g., "Dominance Display", "Virtue Signaling").
- "Evidence": Quote the behavior.

Respond in JSON:
{
  "signals": [
    {"person": "Person A", "signal_type": "Countersignaling", "description": "Wearing a hoodie to a board meeting"}
  ]
}""",
            # Hierarchy mapping
            """Map the "Pecking Order". Who is the Alpha?

Signals: {{output[-1].signals}}

Constraints:
- Hierarchy: Rank exactly the top 3 players.
- Reasoning: Based on "Resource Control" or "Social Proof".

Respond in JSON:
{
  "hierarchy": ["1. Person X (Alpha)", "2. Person Y (Beta)", "3. Person Z (Omega)"],
  "reasoning": "Person X controls the attention economy of the room."
}""",
            # Real game
            """What is the "Meta-Game"? What are they *really* fighting over?

Situation: {{situation}}
Hierarchy: {{output[-1].hierarchy}}

Constraints:
- "Real Game": Name it (e.g., "The Victimhood Olympics").
- Rules: Exactly 3 implicit rules.
- Winner: Who wins this specific game?

Respond in JSON:
{
  "real_game": "Name of the hidden game",
  "rules": ["Rule 1 (e.g., 'Whoever cries first wins')", "Rule 2"],
  "winner": "Person Y",
  "countermoves": ["Strategy to flip the board (e.g., 'Refuse to validate the frame')"]
}"""
        ],
        return_usage=True,
    )

    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    output_dir = os.path.join(project_root, "output", "social", "status_game_decoder")
    os.makedirs(output_dir, exist_ok=True)

    output_path = os.path.join(output_dir, f"{timestamp}-status_game.json")
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2)

    log_file = MinimalChainable.log_to_markdown("status_game_decoder", context_filled_prompts, result, usage_stats)

    print(f"✅ Saved JSON to: {output_path}")
    print(f"✅ Log saved to: {log_file}")


def main():
    situation, _ = get_input_from_args(
        description="Decode status games in a social situation",
        default_context_help="(unused)"
    )
    status_game_decoder(situation)


if __name__ == "__main__":
    main()
