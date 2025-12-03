#!/usr/bin/env python3
"""
🌌 Emergence Simulator (adult mode)

Explore how simple rules/agents produce emergent behavior: rules, interactions, simulations, and observations.

Usage:
    python tools/research/emergence_simulator.py "System description"
    python tools/research/emergence_simulator.py "Boids flocking" --context "Constraints or levers"
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


def emergence_simulator(system: str, additional_context: str = ""):
    print("🌌 Emergence Simulator")
    print(f"System: {system}")
    if additional_context:
        print(f"Context: {additional_context}")
    print()

    user_profile = load_user_context(project_root)
    tone = user_profile.get("writing_style", {}).get("tone", "Analytical and curious")

    client, model_names = build_models()
    model_info = (client, model_names[0])

    context_data = {
        "system": system,
        "additional_context": additional_context,
        "tone": tone,
    }

    result, context_filled_prompts, usage_stats = MinimalChainable.run(
        context=context_data,
        model=model_info,
        callable=prompt,
        prompts=[
            # Define agents and rules
            """Define agent types and simple rules/interactions for the system.
Tone: {{tone}}

System: {{system}}
Context: {{additional_context}}

Respond in JSON:
{
  "agents": ["agent1", "agent2"],
  "rules": ["rule1", "rule2"],
  "environment": "constraints"
}""",
            # Interaction loop
            """Describe an interaction loop (tick) and likely short-term patterns.

Rules: {{output[-1].rules}}

Respond in JSON:
{
  "loop": "step description",
  "short_term_patterns": ["pattern1", "pattern2"]
}""",
            # Emergent behaviors
            """Hypothesize emergent behaviors over time and conditions that amplify/suppress them.

Patterns: {{output[-1].short_term_patterns}}

Respond in JSON:
{
  "emergent_behaviors": [
    {"behavior": "description", "amplifiers": ["amp1"], "dampers": ["damp1"]}
  ]
}""",
            # Experiments
            """Propose simple experiments to probe or steer emergence.

Emergent behaviors: {{output[-1].emergent_behaviors}}

Respond in JSON:
{
  "experiments": [
    {"experiment": "what to change", "measure": "what to observe"}
  ],
  "risks": ["risk1", "risk2"]
}"""
        ],
        return_usage=True,
    )

    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    output_dir = os.path.join(project_root, "output", "research", "emergence_simulator")
    os.makedirs(output_dir, exist_ok=True)

    output_path = os.path.join(output_dir, f"{timestamp}-emergence_simulator.json")
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2)

    log_file = MinimalChainable.log_to_markdown("emergence_simulator", context_filled_prompts, result, usage_stats)

    print(f"✅ Saved JSON to: {output_path}")
    print(f"✅ Log saved to: {log_file}")


def main():
    system, context = get_input_from_args(
        description="Probe emergent behavior from simple rules and propose experiments"
    )
    emergence_simulator(system, context)


if __name__ == "__main__":
    main()
