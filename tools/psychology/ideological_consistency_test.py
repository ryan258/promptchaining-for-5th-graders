#!/usr/bin/env python3
"""
🧭 Ideological Consistency Test (adult mode)

Surface contradictions between stated beliefs, derived implications, and likely behavior.

Usage:
    python tools/psychology/ideological_consistency_test.py "Stated beliefs text"
    cat beliefs.txt | python tools/psychology/ideological_consistency_test.py
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


def ideological_consistency_test(beliefs: str):
    print("🧭 Ideological Consistency Test")
    print(f"Beliefs preview: {beliefs[:160]}{'...' if len(beliefs) > 160 else ''}\n")

    user_profile = load_user_context(project_root)
    tone = user_profile.get("writing_style", {}).get("tone", "Direct")

    client, model_names = build_models()
    model_info = (client, model_names[0])

    context_data = {
        "beliefs": beliefs,
        "tone": tone,
    }

    result, context_filled_prompts, usage_stats = MinimalChainable.run(
        context=context_data,
        model=model_info,
        callable=prompt,
        prompts=[
            # Core claims and premises
            """Extract core claims and implied premises from the beliefs.
Tone: {{tone}}

Text:
{{beliefs}}

Respond in JSON:
{
  "claims": ["claim1", "claim2"],
  "premises": ["premise1", "premise2"]
}""",
            # Internal contradictions
            """Identify internal contradictions or tensions between claims/premises.

Claims: {{output[-1].claims}}
Premises: {{output[-1].premises}}

Respond in JSON:
{
  "contradictions": [
    {"between": ["claim/premise"], "why": "conflict"}
  ],
  "severity": "Low/Med/High"
}""",
            # Behavioral implications
            """Predict behavior choices implied by the stated beliefs vs the contradictions.

Respond in JSON:
{
  "likely_behaviors": ["behavior1", "behavior2"],
  "if_consistent": ["behavior if they resolved contradictions"]
}""",
            # Questions to self-test
            """Provide questions/prompts to self-test consistency or refine the worldview.

Respond in JSON:
{
  "self_test_questions": ["question1", "question2"],
  "reading_prompts": ["topic1", "topic2"]
}"""
        ],
        return_usage=True,
    )

    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    output_dir = os.path.join(project_root, "output", "psychology", "ideological_consistency_test")
    os.makedirs(output_dir, exist_ok=True)

    output_path = os.path.join(output_dir, f"{timestamp}-ideological_consistency.json")
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2)

    log_file = MinimalChainable.log_to_markdown("ideological_consistency_test", context_filled_prompts, result, usage_stats)

    print(f"✅ Saved JSON to: {output_path}")
    print(f"✅ Log saved to: {log_file}")


def main():
    beliefs, _ = get_input_from_args(
        description="Surface contradictions and implications in stated beliefs",
        default_context_help="(unused)"
    )
    ideological_consistency_test(beliefs)


if __name__ == "__main__":
    main()
