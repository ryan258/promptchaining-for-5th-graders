#!/usr/bin/env python3
"""
📈 Goodhart's Law Predictor (adult mode)

Stress-test a metric for gaming strategies, unintended consequences, and long-term distortion.

Usage:
    python tools/strategy/goodharts_law_predictor.py "Metric description"
    python tools/strategy/goodharts_law_predictor.py "Metric" --context "Org, incentives, constraints"
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


def goodharts_law_predictor(metric: str, additional_context: str = ""):
    print("📈 Goodhart's Law Predictor")
    print(f"Metric: {metric}")
    if additional_context:
        print(f"Context: {additional_context}")
    print()

    user_profile = load_user_context(project_root)
    tone = user_profile.get("writing_style", {}).get("tone", "Blunt and pragmatic")

    client, model_names = build_models()
    model_info = (client, model_names[0])

    context_data = {
        "metric": metric,
        "additional_context": additional_context,
        "tone": tone,
    }

    result, context_filled_prompts, usage_stats = MinimalChainable.run(
        context=context_data,
        model=model_info,
        callable=prompt,
        prompts=[
            # Gaming strategy
            """You are an Incentive Designer and Systems Theorist. Stress-test this metric for "Gaming" and "Goal Displacement".

Predict how rational actors will optimize for the metric at the expense of the goal.
Tone: {{tone}} | Context: {{additional_context}}

Metric: {{metric}}

Perspective Framework:
- Campbell's Law: "The more any quantitative social indicator is used for social decision-making, the more subject it will be to corruption pressures."
- Principal-Agent Problem: The agent (employee) has different incentives than the principal (employer).

Constraints:
- Tactics: Exactly 3 specific gaming strategies.
- "Effort Level": Low, Medium, High (how hard is it to cheat?).
- "Tactic": Description of the behavior (e.g., "Cherry-picking easy cases").

Respond in JSON:
{
  "gaming_strategy": "Description of the most likely gaming loop",
  "tactics": ["Tactic 1", "Tactic 2", "Tactic 3"],
  "effort_level": "Low"
}""",
            # Unintended consequences
            """Simulate the "Second-Order Effects". What breaks when everyone games the metric?

Strategy: {{output[-1].gaming_strategy}}

Constraints:
- "Actual Outcome": What happens to the real-world goal? (Max 1 sentence).
- "Externalities": Exactly 2 negative side effects (e.g., "Customer trust erodes").
- Quality Impact: Positive, Negative, Neutral.

Respond in JSON:
{
  "actual_outcome": "The metric goes up, but the goal collapses.",
  "quality_impact": "Negative",
  "externalities": ["Externality 1", "Externality 2"]
}""",
            # Long-term distortion and culture
            """Project the "Cultural Drift". How does this metric reshape the organization over 5 years?

Outcome: {{output[-1].actual_outcome}}

Constraints:
- "Long Term Effect": Structural damage (Max 1 sentence).
- "Culture Shift": How values change (e.g., "From craftsmanship to speed").

Respond in JSON:
{
  "long_term_effect": "The codebase becomes unmaintainable.",
  "culture_shift": "Mercenary culture where only measured tasks matter."
}""",
            # Mitigations
            """Design "Counter-Metrics" and "Guardrails". How do we align incentives?

Metric: {{metric}}
Known gaming: {{output[-3].gaming_strategy}}
Outcomes: {{output[-1].long_term_effect}}

Constraints:
- Mitigations: Exactly 2 structural fixes (e.g., "Pair metrics").
- Better Signals: Exactly 2 alternative ways to measure success.

Respond in JSON:
{
  "mitigations": ["Mitigation 1 (e.g., 'Measure latency AND error rate')", "Mitigation 2"],
  "better_signals": ["Signal 1", "Signal 2"]
}"""
        ],
        return_usage=True,
    )

    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    output_dir = os.path.join(project_root, "output", "strategy", "goodharts_law_predictor")
    os.makedirs(output_dir, exist_ok=True)

    output_path = os.path.join(output_dir, f"{timestamp}-goodharts_law.json")
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2)

    log_file = MinimalChainable.log_to_markdown("goodharts_law_predictor", context_filled_prompts, result, usage_stats)

    print(f"✅ Saved JSON to: {output_path}")
    print(f"✅ Log saved to: {log_file}")


def main():
    metric, context = get_input_from_args(
        description="Stress-test a metric for Goodhart effects and propose mitigations"
    )
    goodharts_law_predictor(metric, context)


if __name__ == "__main__":
    main()
