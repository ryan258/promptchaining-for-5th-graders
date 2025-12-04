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
            """You are a Complexity Theorist and Agent-Based Modeler. Design a "Generative System" to simulate this phenomenon.

Define the "Micro-Foundations" (simple rules) that create macro-complexity.
Tone: {{tone}}

System: {{system}}
Context: {{additional_context}}

Perspective Framework:
- Boids Algorithm: Separation, Alignment, Cohesion.
- Game Theory: Payoff matrices for interaction.

Constraints:
- Agents: Exactly 2 distinct types.
- Rules: Exactly 3 interaction rules (If X, then Y).
- Environment: One key constraint (e.g., "Limited resources").

Respond in JSON:
{
  "agents": ["Agent Type A", "Agent Type B"],
  "rules": ["Rule 1 (e.g., 'If neighbor is close, move away')", "Rule 2", "Rule 3"],
  "environment": "Description of the boundary condition"
}""",
            # Interaction loop
            """Simulate the "Feedback Loop". What happens in one "Tick"?

Rules: {{output[-1].rules}}

Constraints:
- Loop: Step-by-step execution order (Max 3 steps).
- Patterns: Exactly 2 short-term results (e.g., "Oscillation").

Respond in JSON:
{
  "loop": "Step 1 -> Step 2 -> Step 3",
  "short_term_patterns": ["Pattern 1", "Pattern 2"]
}""",
            # Emergent behaviors
            """Predict the "Macro-State". What properties emerge that are not in the rules?

Look for "Phase Transitions" and "Self-Organization".
Patterns: {{output[-1].short_term_patterns}}

Constraints:
- Behaviors: Exactly 2 emergent properties.
- Amplifiers: One factor that speeds this up.
- Dampers: One factor that slows it down.

Respond in JSON:
{
  "emergent_behaviors": [
    {"behavior": "Description of macro-phenomenon", "amplifiers": ["Factor A"], "dampers": ["Factor B"]}
  ]
}""",
            # Experiments
            """Design "Perturbation Experiments". How do we break or steer the system?

Emergent behaviors: {{output[-1].emergent_behaviors}}

Constraints:
- Experiments: Exactly 2 interventions.
- Measure: Specific metric to track.
- Risks: Exactly 2 unintended consequences (e.g., "System collapse").

Respond in JSON:
{
  "experiments": [
    {"experiment": "Change parameter X to Y", "measure": "Track variable Z"}
  ],
  "risks": ["Risk 1", "Risk 2"]
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
