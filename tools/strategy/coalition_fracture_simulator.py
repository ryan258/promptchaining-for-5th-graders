#!/usr/bin/env python3
"""
🧩 Coalition Fracture Simulator (adult mode)

Explore how a coalition could fracture: fault lines, triggers, incentives, and mitigation moves.

Usage:
    python tools/strategy/coalition_fracture_simulator.py "Describe the coalition"
    cat coalition.txt | python tools/strategy/coalition_fracture_simulator.py
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


def coalition_fracture_simulator(description: str):
    print("🧩 Coalition Fracture Simulator")
    print(f"Coalition: {description[:160]}{'...' if len(description) > 160 else ''}\n")

    user_profile = load_user_context(project_root)
    tone = user_profile.get("writing_style", {}).get("tone", "Analytical and direct")

    client, model_names = build_models()
    model_info = (client, model_names[0])

    context_data = {
        "coalition": description,
        "tone": tone,
    }

    result, context_filled_prompts, usage_stats = MinimalChainable.run(
        context=context_data,
        model=model_info,
        callable=prompt,
        prompts=[
            # Fault lines
            """You are a conflict analyst. Identify key factions and fault lines in the coalition.
Tone: {{tone}}

Coalition:
{{coalition}}

Limit to 3-5 fault lines; include severity.

Respond in JSON:
{
  "factions": ["faction1", "faction2"],
  "fault_lines": [
    {"line": "issue/tension", "who": ["actors"], "severity": "Low/Med/High"}
  ]
}""",
            # Triggers and incentives
            """List plausible triggers that would open the fault lines and the incentives to break ranks.
Provide 3 triggers max; include likelihood.

Fault lines: {{output[-1].fault_lines}}

Respond in JSON:
{
  "triggers": [
    {"trigger": "event", "affected_factions": ["who"], "likelihood": "Low/Med/High"}
  ],
  "defection_incentives": ["incentive1", "incentive2"]
}""",
            # Fracture scenarios
            """Simulate 1-2 fracture scenarios and short-term outcomes.
Keep sequences concise (3 steps max).

Triggers: {{output[-1].triggers}}

Respond in JSON:
{
  "scenarios": [
    {"name": "scenario", "sequence": ["step1", "step2"], "outcome": "result"}
  ]
}""",
            # Mitigations
            """Propose mitigation or cohesion moves to reduce fracture risk.
Give 2-3 moves and 2-3 monitoring signals.

Fault lines: {{output[-3].fault_lines}}
Triggers: {{output[-2].triggers}}

Respond in JSON:
{
  "mitigations": ["move1", "move2"],
  "monitoring_signals": ["signal1", "signal2"]
}"""
        ],
        return_usage=True,
    )

    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    output_dir = os.path.join(project_root, "output", "strategy", "coalition_fracture_simulator")
    os.makedirs(output_dir, exist_ok=True)

    output_path = os.path.join(output_dir, f"{timestamp}-coalition_fracture.json")
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2)

    log_file = MinimalChainable.log_to_markdown("coalition_fracture_simulator", context_filled_prompts, result, usage_stats)

    print(f"✅ Saved JSON to: {output_path}")
    print(f"✅ Log saved to: {log_file}")


def main():
    description, _ = get_input_from_args(
        description="Simulate coalition fracture: fault lines, triggers, scenarios, mitigations",
        default_context_help="(unused)"
    )
    coalition_fracture_simulator(description)


if __name__ == "__main__":
    main()
