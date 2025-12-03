#!/usr/bin/env python3
"""
⚡ Crisis Opportunity Scanner (adult mode)

Spot agenda-driven moves during a crisis: actors, overreach solutions, and the power bypass.

Usage:
    python tools/strategy/crisis_opportunity_scanner.py "Describe the crisis"
    cat crisis.txt | python tools/strategy/crisis_opportunity_scanner.py
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


def crisis_opportunity_scanner(crisis: str):
    print("⚡ Crisis Opportunity Scanner")
    print(f"Crisis: {crisis[:160]}{'...' if len(crisis) > 160 else ''}\n")

    user_profile = load_user_context(project_root)
    tone = user_profile.get("writing_style", {}).get("tone", "Skeptical and concise")

    client, model_names = build_models()
    model_info = (client, model_names[0])

    context_data = {
        "crisis": crisis,
        "tone": tone,
    }

    result, context_filled_prompts, usage_stats = MinimalChainable.run(
        context=context_data,
        model=model_info,
        callable=prompt,
        prompts=[
            # Actors
            """Identify actors ready to exploit this crisis to advance pre-existing agendas.
Tone: {{tone}}

Text:
{{crisis}}

Respond in JSON:
{
  "actors": [
    {"group": "who", "agenda": "what they want", "playbook": "typical moves"}
  ]
}""",
            # Overreach solutions
            """List likely overreach solutions pitched as fixes but serving the agendas.

Actors: {{output[-1].actors}}

Respond in JSON:
{
  "proposed_solutions": [
    {"solution": "description", "hidden_agenda": "what it enables", "winners": ["who"], "losers": ["who"]}
  ]
}""",
            # Crisis bypass
            """Explain how the crisis is used to bypass normal scrutiny and what the long-tail impacts are.

Solutions: {{output[-1].proposed_solutions}}

Respond in JSON:
{
  "bypass_mechanism": "emergency powers/fear/etc",
  "long_term_impacts": ["impact1", "impact2"],
  "guardrails": ["mitigation1", "mitigation2"]
}"""
        ],
        return_usage=True,
    )

    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    output_dir = os.path.join(project_root, "output", "strategy", "crisis_opportunity_scanner")
    os.makedirs(output_dir, exist_ok=True)

    output_path = os.path.join(output_dir, f"{timestamp}-crisis_opportunity.json")
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2)

    log_file = MinimalChainable.log_to_markdown("crisis_opportunity_scanner", context_filled_prompts, result, usage_stats)

    print(f"✅ Saved JSON to: {output_path}")
    print(f"✅ Log saved to: {log_file}")


def main():
    crisis, _ = get_input_from_args(
        description="Scan a crisis for agenda-driven actors and overreach solutions",
        default_context_help="(unused)"
    )
    crisis_opportunity_scanner(crisis)


if __name__ == "__main__":
    main()
