#!/usr/bin/env python3
"""
🛰️ Proxy War Analyst (adult mode)

Identify proxies, sponsors, objectives, escalation paths, and off-ramps in a conflict.

Usage:
    python tools/geopolitics/proxy_war_analyst.py "Conflict description"
    cat conflict.txt | python tools/geopolitics/proxy_war_analyst.py
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


def proxy_war_analyst(conflict: str):
    print("🛰️ Proxy War Analyst")
    print(f"Conflict: {conflict[:200]}{'...' if len(conflict) > 200 else ''}\n")

    user_profile = load_user_context(project_root)
    tone = user_profile.get("writing_style", {}).get("tone", "Analytical and sober")

    client, model_names = build_models()
    model_info = (client, model_names[0])

    context_data = {
        "conflict": conflict,
        "tone": tone,
    }

    result, context_filled_prompts, usage_stats = MinimalChainable.run(
        context=context_data,
        model=model_info,
        callable=prompt,
        prompts=[
            # Proxies and sponsors
            """List likely proxies and sponsors, and what each side wants.
Tone: {{tone}}

Conflict:
{{conflict}}

Limit to top 6 actors. Be explicit on role (proxy/sponsor/primary).

Respond in JSON:
{
  "actors": [
    {"actor": "name", "role": "proxy/sponsor/primary", "objective": "goal"}
  ]
}""",
            # Escalation paths
            """Map plausible escalation paths and triggers.
Provide 2-3 paths; each with trigger and short sequence.

Respond in JSON:
{
  "escalation_paths": [
    {"trigger": "event", "path": "steps", "risk": "Low/Med/High"}
  ]
}""",
            # Off-ramps and constraints
            """Identify off-ramps, constraints, and leverage points to reduce risk.
Provide 2-3 off-ramps and 2-3 monitoring signals.

Respond in JSON:
{
  "off_ramps": ["option1", "option2"],
  "constraints": ["constraint1", "constraint2"],
  "monitoring_signals": ["signal1", "signal2"]
}"""
        ],
        return_usage=True,
    )

    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    output_dir = os.path.join(project_root, "output", "geopolitics", "proxy_war_analyst")
    os.makedirs(output_dir, exist_ok=True)

    output_path = os.path.join(output_dir, f"{timestamp}-proxy_war.json")
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2)

    log_file = MinimalChainable.log_to_markdown("proxy_war_analyst", context_filled_prompts, result, usage_stats)

    print(f"✅ Saved JSON to: {output_path}")
    print(f"✅ Log saved to: {log_file}")


def main():
    conflict, _ = get_input_from_args(
        description="Analyze a proxy war: actors, objectives, escalation, and off-ramps",
        default_context_help="(unused)"
    )
    proxy_war_analyst(conflict)


if __name__ == "__main__":
    main()
