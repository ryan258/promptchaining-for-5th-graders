#!/usr/bin/env python3
"""
⌛ Historical What-If Machine (adult mode)

Explore counterfactual scenarios: branching point, plausible ripple effects, and confidence.

Usage:
    python tools/history/historical_what_if_machine.py "What if Rome never fell?"
    python tools/history/historical_what_if_machine.py "Scenario" --context "Constraints or lens"
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


def historical_what_if_machine(counterfactual: str, additional_context: str = ""):
    print("⌛ Historical What-If Machine")
    print(f"Scenario: {counterfactual}")
    if additional_context:
        print(f"Context: {additional_context}")
    print()

    user_profile = load_user_context(project_root)
    tone = user_profile.get("writing_style", {}).get("tone", "Analytical and cautious")

    client, model_names = build_models()
    model_info = (client, model_names[0])

    context_data = {
        "scenario": counterfactual,
        "additional_context": additional_context,
        "tone": tone,
    }

    result, context_filled_prompts, usage_stats = MinimalChainable.run(
        context=context_data,
        model=model_info,
        callable=prompt,
        prompts=[
            # Branching point and assumptions
            """State the branching point and key assumptions explicitly.
Tone: {{tone}}

Scenario: {{scenario}}
Context: {{additional_context}}

Respond in JSON:
{
  "branch_point": "event",
  "assumptions": ["assumption1", "assumption2"]
}""",
            # Near-term ripple effects
            """Map near-term ripple effects (0-10 years) with plausibility.

Branch: {{output[-1].branch_point}}
Assumptions: {{output[-1].assumptions}}

Respond in JSON:
{
  "near_term_effects": [
    {"effect": "description", "plausibility": "Low/Med/High"}
  ]
}""",
            # Longer-term trajectory
            """Project longer-term trajectory (10-50 years) with confidence and key dependencies.

Respond in JSON:
{
  "long_term_effects": [
    {"effect": "description", "confidence": "Low/Med/High", "dependencies": ["dep1"]}
  ]
}""",
            # Caveats and research hooks
            """List caveats, unknowns, and sources/lines of research to validate or refine the scenario.

Respond in JSON:
{
  "caveats": ["caveat1", "caveat2"],
  "research_hooks": ["hook1", "hook2"]
}"""
        ],
        return_usage=True,
    )

    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    output_dir = os.path.join(project_root, "output", "history", "historical_what_if_machine")
    os.makedirs(output_dir, exist_ok=True)

    output_path = os.path.join(output_dir, f"{timestamp}-historical_what_if.json")
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2)

    log_file = MinimalChainable.log_to_markdown("historical_what_if_machine", context_filled_prompts, result, usage_stats)

    print(f"✅ Saved JSON to: {output_path}")
    print(f"✅ Log saved to: {log_file}")


def main():
    scenario, context = get_input_from_args(
        description="Explore historical counterfactuals with explicit assumptions and ripple effects"
    )
    historical_what_if_machine(scenario, context)


if __name__ == "__main__":
    main()
