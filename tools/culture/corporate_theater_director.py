#!/usr/bin/env python3
"""
🎭 Corporate Theater Director (adult mode)

Decode performative corporate rituals, scripts, and incentives; propose honest alternatives.

Usage:
    python tools/culture/corporate_theater_director.py "Describe the ritual/town hall/email"
    cat memo.txt | python tools/culture/corporate_theater_director.py
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


def corporate_theater_director(text: str):
    print("🎭 Corporate Theater Director")
    print(f"Ritual preview: {text[:200]}{'...' if len(text) > 200 else ''}\n")

    user_profile = load_user_context(project_root)
    tone = user_profile.get("writing_style", {}).get("tone", "Wry but constructive")

    client, model_names = build_models()
    model_info = (client, model_names[0])

    context_data = {
        "text": text,
        "tone": tone,
    }

    result, context_filled_prompts, usage_stats = MinimalChainable.run(
        context=context_data,
        model=model_info,
        callable=prompt,
        prompts=[
            # Decode the theater
            """Decode the performative elements and intended signals in this corporate ritual/communication.
Tone: {{tone}}

Text:
{{text}}

Respond in JSON:
{
  "performative_moves": [
    {"move": "description", "signal": "what it's trying to signal"}
  ],
  "audience_reaction": "likely internal reaction"
}""",
            # Incentives and reality
            """Map the incentives driving the theater and what reality it obscures.

Moves: {{output[-1].performative_moves}}

Respond in JSON:
{
  "incentives": ["incentive1", "incentive2"],
  "obscured_reality": "what's not being said"
}""",
            # Honest alternative
            """Propose a more honest, concise alternative that keeps morale and trust higher.

Respond in JSON:
{
  "honest_script": "rewrite",
  "likely_effect": "impact on morale/trust"
}"""
        ],
        return_usage=True,
    )

    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    output_dir = os.path.join(project_root, "output", "culture", "corporate_theater_director")
    os.makedirs(output_dir, exist_ok=True)

    output_path = os.path.join(output_dir, f"{timestamp}-corporate_theater.json")
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2)

    log_file = MinimalChainable.log_to_markdown("corporate_theater_director", context_filled_prompts, result, usage_stats)

    print(f"✅ Saved JSON to: {output_path}")
    print(f"✅ Log saved to: {log_file}")


def main():
    text, _ = get_input_from_args(
        description="Decode corporate theater and draft an honest alternative",
        default_context_help="(unused)"
    )
    corporate_theater_director(text)


if __name__ == "__main__":
    main()
