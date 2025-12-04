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
            """You are a Conflict Resolution Specialist and Moral Psychologist. Deconstruct the opposing views into their "Moral Foundations" (Haidt's framework).

Identify the core values driving each side, not just their stated positions.
Tone: {{tone}}

View A: {{view_A}}
View B: {{view_B}}

Perspective Framework:
- Care/Harm
- Fairness/Cheating
- Loyalty/Betrayal
- Authority/Subversion
- Sanctity/Degradation
- Liberty/Oppression

Constraints:
- List exactly 3 core values per side.
- "Unstated Fear": What is the catastrophic outcome each side is trying to prevent? (Max 1 sentence).

Respond in JSON:
{
  "view_A_values": ["Value 1 (e.g., 'Sanctity of tradition')", "Value 2"],
  "view_B_values": ["Value 1 (e.g., 'Care for the vulnerable')", "Value 2"],
  "unstated_fears": ["View A fear: 'Chaos and loss of order'", "View B fear: 'Oppression and loss of rights'"]
}""",
            # Shared concerns
            """You are a Diplomatic Mediator. Identify the "Overlapping Magisteria"—the specific risks or outcomes that both sides genuinely want to avoid.

Focus on "Negative Agreement": What do they both hate?
Values: A={{output[-1].view_A_values}}, B={{output[-1].view_B_values}}

Constraints:
- List exactly 3 shared concerns.
- "Evidence": Must cite a specific overlap in their logic or values.
- Max 20 words per concern.

Respond in JSON:
{
  "shared_concerns": ["Shared Concern 1", "Shared Concern 2", "Shared Concern 3"],
  "evidence_both_care": ["Evidence for 1", "Evidence for 2", "Evidence for 3"]
}""",
            # Common goals
            """Synthesize "Superordinate Goals"—higher-level objectives that require cooperation to achieve.

These must be downstream of the shared concerns.
Shared concerns: {{output[-1].shared_concerns}}

Constraints:
- List exactly 2 common goals.
- "Goal Tensions": Where might the *methods* to achieve these goals conflict?

Respond in JSON:
{
  "common_goals": ["Goal 1 (e.g., 'Safe communities')", "Goal 2"],
  "goal_tensions": ["Tension 1 (e.g., 'Surveillance vs. Privacy')"]
}""",
            # Bridge options
            """You are a Game Theorist specializing in "Positive Sum" outcomes. Propose specific, low-risk moves to build trust.

Avoid "Compromise" (both lose); seek "Integration" (both win).

Views: {{view_A}} vs {{view_B}}
Values: A={{output[-3].view_A_values}}, B={{output[-3].view_B_values}}
Shared concerns: {{output[-2].shared_concerns}}
Common goals: {{output[-1].common_goals}}

Constraints:
- Bridge Ideas: Exactly 3 specific actions.
- Conversation Prompts: Exactly 3 questions to ask.
- "Risk": Must identify a specific backfire mode.

Respond in JSON:
{
  "bridge_ideas": [
    {"move": "Specific action", "why_it_works": "Mechanism of trust building", "risk": "Potential backfire"}
  ],
  "conversation_prompts": ["Question 1 (e.g., 'What is your worst case scenario?')", "Question 2", "Question 3"]
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
