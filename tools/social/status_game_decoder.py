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
            """Analyze the surface interaction: who is polite, who is rude, what's happening on the face of it.
Tone: {{tone}}

Situation:
{{situation}}

Respond in JSON:
{
  "surface_analysis": "description",
  "polite_person": "Name/label",
  "rude_person": "Name/label"
}""",
            # Status signals
            """Identify status signals:
- countersignaling
- signaling wealth/experience
- signaling busy importance
- signaling intellectual dominance

Respond in JSON:
{
  "signals": [
    {"person": "label", "signal_type": "type", "description": "short"}
  ]
}""",
            # Hierarchy mapping
            """Map the dominance/status hierarchy and reasoning.

Signals: {{output[-1].signals}}

Respond in JSON:
{
  "hierarchy": ["1. Person X", "2. Person Y"],
  "reasoning": "why"
}""",
            # Real game
            """What is the real status game being played? Name it, list rules, and predict the winner.

Situation: {{situation}}
Signals: {{output[-2].signals}}
Hierarchy: {{output[-1].hierarchy}}

Respond in JSON:
{
  "real_game": "name",
  "rules": ["rule1", "rule2"],
  "winner": "Name/label",
  "countermoves": ["how to avoid/redirect if needed"]
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
