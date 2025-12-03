#!/usr/bin/env python3
"""
🕊️ Diplomatic Subtext Decoder (adult mode)

Translate diplomatese into real intent, predict response, and surface political purpose.

Usage:
    python tools/strategy/diplomatic_subtext_decoder.py "Statement"
    cat statement.txt | python tools/strategy/diplomatic_subtext_decoder.py
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


def diplomatic_subtext_decoder(statement: str):
    print("🕊️ Diplomatic Subtext Decoder")
    print(f"Statement: {statement[:160]}{'...' if len(statement) > 160 else ''}\n")

    user_profile = load_user_context(project_root)
    tone = user_profile.get("writing_style", {}).get("tone", "Realpolitik, concise")

    client, model_names = build_models()
    model_info = (client, model_names[0])

    context_data = {
        "statement": statement,
        "tone": tone,
    }

    result, context_filled_prompts, usage_stats = MinimalChainable.run(
        context=context_data,
        model=model_info,
        callable=prompt,
        prompts=[
            # Translate diplomatese
            """Translate the statement into plain Realpolitik English and rate action level.
Tone: {{tone}}

Statement:
{{statement}}

Respond in JSON:
{
  "translation": "plain text",
  "action_level": "Zero/Low/Medium/High",
  "blame_positioning": "how blame is distributed"
}""",
            # Predict response
            """Given the weak/strong language, predict the aggressor's next move and rationale.

Translation: {{output[-1].translation}}
Action level: {{output[-1].action_level}}

Respond in JSON:
{
  "prediction": "escalation/de-escalation/status-quo",
  "reasoning": "why"
}""",
            # Intent/purpose
            """Surface the political purpose of issuing this statement and who it is aimed at.

Respond in JSON:
{
  "political_purpose": "domestic/alliances/face-saving/etc",
  "intended_audience": ["group1", "group2"],
  "effectiveness": "Low/Med/High"
}"""
        ],
        return_usage=True,
    )

    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    output_dir = os.path.join(project_root, "output", "strategy", "diplomatic_subtext_decoder")
    os.makedirs(output_dir, exist_ok=True)

    output_path = os.path.join(output_dir, f"{timestamp}-diplomatic_decoder.json")
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2)

    log_file = MinimalChainable.log_to_markdown("diplomatic_subtext_decoder", context_filled_prompts, result, usage_stats)

    print(f"✅ Saved JSON to: {output_path}")
    print(f"✅ Log saved to: {log_file}")


def main():
    statement, _ = get_input_from_args(
        description="Decode diplomatic language for subtext, intent, and likely responses",
        default_context_help="(unused)"
    )
    diplomatic_subtext_decoder(statement)


if __name__ == "__main__":
    main()
