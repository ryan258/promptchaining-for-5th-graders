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
            """You are a Political Strategist and Game Theorist. Analyze the stability of this "Minimum Winning Coalition".

Identify "Wedge Issues" and "Misaligned Incentives".
Tone: {{tone}}

Coalition:
{{coalition}}

Perspective Framework:
- Ideological vs Transactional: Are they bound by belief or profit?
- The "Junior Partner" Dilemma: Is the smaller faction being exploited?

Constraints:
- Factions: Exactly 2-3 key players.
- Fault Lines: Exactly 3 structural weaknesses.
- Severity: Low, Medium, High.

Respond in JSON:
{
  "factions": ["Faction A", "Faction B"],
  "fault_lines": [
    {"line": "Description of tension", "who": ["Faction A", "Faction B"], "severity": "High"}
  ]
}""",
            # Triggers and incentives
            """What "Exogenous Shocks" could break this alliance?

Fault lines: {{output[-1].fault_lines}}

Constraints:
- Triggers: Exactly 3 specific events (e.g., "Budget vote").
- Incentives: Why defect? (e.g., "Prisoner's Dilemma payoff").

Respond in JSON:
{
  "triggers": [
    {"trigger": "Event description", "affected_factions": ["Faction A"], "likelihood": "Medium"}
  ],
  "defection_incentives": ["Incentive 1", "Incentive 2"]
}""",
            # Fracture scenarios
            """Simulate the "Endgame". How does the collapse happen?

Triggers: {{output[-1].triggers}}

Constraints:
- Scenarios: Exactly 2 distinct paths to failure.
- Sequence: Exactly 3 steps per scenario.

Respond in JSON:
{
  "scenarios": [
    {"name": "Scenario Name (e.g., 'The Betrayal')", "sequence": ["Step 1", "Step 2", "Step 3"], "outcome": "Final state"}
  ]
}""",
            # Mitigations
            """You are a Diplomat and Crisis Manager. How do we hold the center?

Constraints:
- Mitigations: Exactly 3 moves to restore trust.
- Monitoring: Exactly 3 early warning signals.

Respond in JSON:
{
  "mitigations": ["Move 1 (e.g., 'Power-sharing agreement')", "Move 2"],
  "monitoring_signals": ["Signal 1 (e.g., 'Leak frequency')", "Signal 2"]
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
