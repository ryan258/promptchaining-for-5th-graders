#!/usr/bin/env python3
"""
🤝 Negotiation Strategy Builder (adult mode)

Analyze leverage, BATNAs, anchors, objections, and counter-scripts for a negotiation scenario.

Usage:
    python tools/business/negotiation_strategy_builder.py "Scenario description"
    python tools/business/negotiation_strategy_builder.py "Scenario" --context "Role, constraints, numbers"
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


def negotiation_strategy_builder(scenario: str, additional_context: str = ""):
    print("🤝 Negotiation Strategy Builder")
    print(f"Scenario: {scenario}")
    if additional_context:
        print(f"Context: {additional_context}")
    print()

    user_profile = load_user_context(project_root)
    tone = user_profile.get("writing_style", {}).get("tone", "Professional and firm")

    client, model_names = build_models()
    model_info = (client, model_names[0])

    context_data = {
        "scenario": scenario,
        "additional_context": additional_context,
        "tone": tone,
    }

    result, context_filled_prompts, usage_stats = MinimalChainable.run(
        context=context_data,
        model=model_info,
        callable=prompt,
        prompts=[
            # Power analysis
            """Analyze leverage and hidden power dynamics.
Tone: {{tone}}

Scenario: {{scenario}}
Context: {{additional_context}}

Respond in JSON:
{
  "leverage_analysis": "description",
  "my_power": "high/medium/low",
  "their_power": "high/medium/low"
}""",
            # BATNAs
            """Define BATNAs (yours and theirs) and likely outcome if no deal is reached.

Analysis: {{output[-1].leverage_analysis}}

Respond in JSON:
{
  "my_batna": "description",
  "their_batna": "description"
}""",
            # Anchoring
            """Set the opening anchor and speaking order based on power and BATNAs.

Leverage: {{output[-2].leverage_analysis}}
BATNAs: {{output[-1].my_batna}} vs {{output[-1].their_batna}}

Respond in JSON:
{
  "speak_first": "yes/no",
  "opening_anchor": "proposal",
  "reasoning": "why this anchor"
}""",
            # Objections
            """Predict the top objections to the anchor.

Anchor: {{output[-1].opening_anchor}}

Respond in JSON:
{
  "objections": ["objection1", "objection2", "objection3"]
}""",
            # Counter-scripts
            """Write counter-scripts that pivot to value without unnecessary concessions.

Objections: {{output[-1].objections}}
Anchor: {{output[-2].opening_anchor}}

Respond in JSON:
{
  "scripts": [
    {"objection": "text", "response_script": "script"}
  ],
  "concession_guardrails": ["what not to give away"]
}"""
        ],
        return_usage=True,
    )

    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    output_dir = os.path.join(project_root, "output", "business", "negotiation_strategy_builder")
    os.makedirs(output_dir, exist_ok=True)

    output_path = os.path.join(output_dir, f"{timestamp}-negotiation_strategy.json")
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2)

    log_file = MinimalChainable.log_to_markdown("negotiation_strategy_builder", context_filled_prompts, result, usage_stats)

    print(f"✅ Saved JSON to: {output_path}")
    print(f"✅ Log saved to: {log_file}")


def main():
    scenario, context = get_input_from_args(
        description="Build a negotiation strategy with leverage, BATNA, anchoring, objections, and scripts"
    )
    negotiation_strategy_builder(scenario, context)


if __name__ == "__main__":
    main()
