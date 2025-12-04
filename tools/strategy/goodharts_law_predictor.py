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
            """Given the metric, predict how rational actors will game it for maximum reward/minimum effort.
Tone: {{tone}} | Context: {{additional_context}}

Metric: {{metric}}

Give 2-4 tactics; include one GOOD vs BAD example:
GOOD: "Report easy bugs to inflate counts; avoid hard fixes" (specific)
BAD: "Work harder" (not gaming)

Respond in JSON:
{
  "gaming_strategy": "description",
  "effort_level": "Low/Med/High"
}""",
            # Unintended consequences
            """If the gaming strategy spreads, what happens to the true objective?
Keep to 3-5 sentences; call out at least one negative externality explicitly.

Strategy: {{output[-1].gaming_strategy}}

Respond in JSON:
{
  "actual_outcome": "description",
  "quality_impact": "Positive/Negative/Unknown",
  "externalities": ["ext1", "ext2"]
}""",
            # Long-term distortion and culture
            """Simulate the long-term distortion: codebase/process/data quality/culture.
Limit to 2-3 key effects; note confidence if low.

Outcome: {{output[-1].actual_outcome}}

Respond in JSON:
{
  "long_term_effect": "description",
  "culture_shift": "description"
}""",
            # Mitigations
            """Suggest mitigations or counter-metrics to reduce gaming while keeping signal.
Provide 2-3 mitigations and 2-3 alternative signals; keep each to one sentence.

Metric: {{metric}}
Known gaming: {{output[-3].gaming_strategy}}
Outcomes: {{output[-1].long_term_effect}}

Respond in JSON:
{
  "mitigations": ["mitigation1", "mitigation2"],
  "better_signals": ["alternate metric1", "alternate metric2"]
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
