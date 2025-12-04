#!/usr/bin/env python3
"""
🕵️ Revealed Preference Detective (adult mode)

Contrast stated preferences with revealed behavior to infer real values and likely choices.

Usage:
    python tools/psychology/revealed_preference_detective.py "Stated pref" --context "Revealed behavior"
    echo "Stated" | python tools/psychology/revealed_preference_detective.py --context "Behavior"
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


def revealed_preference_detective(stated: str, revealed: str):
    print("🕵️ Revealed Preference Detective")
    print(f"Stated: {stated}")
    print(f"Revealed: {revealed}\n")

    user_profile = load_user_context(project_root)
    tone = user_profile.get("writing_style", {}).get("tone", "Blunt but fair")

    client, model_names = build_models()
    model_info = (client, model_names[0])

    context_data = {
        "stated": stated,
        "revealed": revealed,
        "tone": tone,
    }

    result, context_filled_prompts, usage_stats = MinimalChainable.run(
        context=context_data,
        model=model_info,
        callable=prompt,
        prompts=[
            # Contradiction
            """Identify contradictions between stated preference and revealed behavior.
Tone: {{tone}}

Stated: {{stated}}
Revealed: {{revealed}}

Keep contradiction to 2-3 sentences; severity = High/Med/Low.

Respond in JSON:
{
  "contradiction": "description",
  "severity": "High/Med/Low"
}""",
            # Value hierarchy
            """Infer the actual value hierarchy implied by behavior.
Provide top 3 values; include evidence snippet for each.

Contradiction: {{output[-1].contradiction}}

Respond in JSON:
{
  "actual_values": ["Value 1", "Value 2"],
  "evidence": "supporting signals or snippets"
}""",
            # Predict a choice
            """Predict a likely choice in a simple tradeoff scenario given these revealed values.
Keep reasoning to 2 sentences.

Stated: {{stated}}
Revealed values: {{output[-1].actual_values}}

Respond in JSON:
{
  "predicted_choice": "description",
  "reasoning": "why"
}"""
        ],
        return_usage=True,
    )

    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    output_dir = os.path.join(project_root, "output", "psychology", "revealed_preference_detective")
    os.makedirs(output_dir, exist_ok=True)

    output_path = os.path.join(output_dir, f"{timestamp}-revealed_preference.json")
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2)

    log_file = MinimalChainable.log_to_markdown("revealed_preference_detective", context_filled_prompts, result, usage_stats)

    print(f"✅ Saved JSON to: {output_path}")
    print(f"✅ Log saved to: {log_file}")


def main():
    stated, revealed = get_input_from_args(
        description="Contrast stated preferences with revealed behavior to infer true values",
        default_context_help="Revealed behavior"
    )
    revealed_preference_detective(stated, revealed)


if __name__ == "__main__":
    main()
