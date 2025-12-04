#!/usr/bin/env python3
"""
🤝 Common Ground Finder (adult mode)

Map opposing views to underlying values, shared concerns, common goals, and bridge options.

Usage:
    python tools/collaboration/common_ground_finder.py "View A statement" --context "View B statement"
    echo "View A" | python tools/collaboration/common_ground_finder.py --context "View B"
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


def common_ground_finder(view_a: str, view_b: str):
    print("🤝 Common Ground Finder")
    print(f"View A: {view_a}")
    print(f"View B: {view_b}\n")

    user_profile = load_user_context(project_root)
    tone = user_profile.get("writing_style", {}).get("tone", "Calm and precise")

    client, model_names = build_models()
    model_info = (client, model_names[0])

    context_data = {
        "view_A": view_a,
        "view_B": view_b,
        "tone": tone,
    }

    result, context_filled_prompts, usage_stats = MinimalChainable.run(
        context=context_data,
        model=model_info,
        callable=prompt,
        prompts=[
            # Values behind each view
            """You are a facilitator mediating two sides. Extract underlying values and motivations for each view.
Tone: {{tone}}

View A: {{view_A}}
View B: {{view_B}}

Provide 3-5 values per side; include one unstated fear.

Respond in JSON:
{
  "view_A_values": ["value1", "value2"],
  "view_B_values": ["value1", "value2"],
  "unstated_fears": ["fear1", "fear2"]
}""",
            # Shared concerns
            """Identify shared concerns or risks that both sides legitimately care about.

Values: A={{output[-1].view_A_values}}, B={{output[-1].view_B_values}}

Provide 3-5 concerns; include evidence both care.

Respond in JSON:
{
  "shared_concerns": ["concern1", "concern2"],
  "evidence_both_care": ["short evidence for each"]
}""",
            # Common goals
            """Derive common goals that are downstream of the shared concerns.

Shared concerns: {{output[-1].shared_concerns}}

Respond in JSON:
{
  "common_goals": ["goal1", "goal2"],
  "goal_tensions": ["where goals could conflict"]
}""",
            # Bridge options
            """Propose bridge-building moves that respect both sides' values and fears.
Keep them specific and testable; avoid platitudes.

Views: {{view_A}} vs {{view_B}}
Values: A={{output[-3].view_A_values}}, B={{output[-3].view_B_values}}
Shared concerns: {{output[-2].shared_concerns}}
Common goals: {{output[-1].common_goals}}

Provide 3-5 bridge ideas and 3-5 conversation prompts.

Respond in JSON:
{
  "bridge_ideas": [
    {"move": "action", "why_it_works": "reason", "risk": "what could backfire"}
  ],
  "conversation_prompts": ["question or prompt to surface alignment"]
}"""
        ],
        return_usage=True,
    )

    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    output_dir = os.path.join(project_root, "output", "collaboration", "common_ground_finder")
    os.makedirs(output_dir, exist_ok=True)

    output_path = os.path.join(output_dir, f"{timestamp}-common_ground.json")
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2)

    log_file = MinimalChainable.log_to_markdown("common_ground_finder", context_filled_prompts, result, usage_stats)

    print(f"✅ Saved JSON to: {output_path}")
    print(f"✅ Log saved to: {log_file}")


def main():
    view_a, view_b = get_input_from_args(
        description="Find common ground between two opposing views (topic=A, --context=B)",
        default_context_help="Second viewpoint"
    )
    common_ground_finder(view_a, view_b)


if __name__ == "__main__":
    main()
