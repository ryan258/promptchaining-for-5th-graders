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
            """You are a Counterfactual Historian and Chaos Theory Analyst. Identify the precise "Point of Divergence" (POD).

Avoid "Great Man Theory"—focus on structural forces and contingencies.
Tone: {{tone}}

Scenario: {{scenario}}
Context: {{additional_context}}

Perspective Framework:
- Butterfly Effect: Small changes, big consequences.
- Path Dependence: Once a path is chosen, it's hard to reverse.

Constraints:
- "Branch Point": The exact moment history changed (e.g., "Oct 14, 1066: Harold Godwinson survives Hastings").
- Assumptions: Exactly 3 structural changes required for this to happen.

Respond in JSON:
{
  "branch_point": "Specific event and date",
  "assumptions": ["Assumption 1 (e.g., 'Weather was different')", "Assumption 2"]
}""",
            # Near-term ripple effects
            """Map the "First-Order Effects" (0-10 years). What changes immediately?

Focus on "Plausibility"—what is the most likely immediate outcome?
Branch: {{output[-1].branch_point}}
Assumptions: {{output[-1].assumptions}}

Constraints:
- Identify exactly 3 near-term effects.
- "Plausibility": Low, Medium, High.
- Max 2 sentences per effect.

Respond in JSON:
{
  "near_term_effects": [
    {"effect": "Description of change", "plausibility": "High"}
  ]
}""",
            # Longer-term trajectory
            """Project the "Second-Order Effects" (10-50 years). How does the timeline diverge radically?

Focus on "Unintended Consequences".
Constraints:
- Identify exactly 3 long-term effects.
- "Confidence": Low, Medium, High.
- "Dependencies": What *else* must happen for this to be true?

Respond in JSON:
{
  "long_term_effects": [
    {"effect": "Description of radical divergence", "confidence": "Low", "dependencies": ["Dependency 1"]}
  ]
}""",
            # Caveats and research hooks
            """You are an Academic Reviewer. What are the flaws in this simulation?

Where is the "Determinism Trap"?
Constraints:
- Caveats: Exactly 3 reasons this might NOT happen.
- Research Hooks: Exactly 3 topics to study to validate this.

Respond in JSON:
{
  "caveats": ["Caveat 1 (e.g., 'Geography remains the same')", "Caveat 2"],
  "research_hooks": ["Topic 1 (e.g., 'Grain yields in 13th century France')", "Topic 2"]
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
