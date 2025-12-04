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
            """You are a Geopolitical Intelligence Analyst. Map the "Conflict Ecosystem" to identify who is fighting and who is paying.

Distinguish between "Proxies" (fighting on behalf of others) and "Sponsors" (providing resources).
Tone: {{tone}}

Conflict:
{{conflict}}

Perspective Framework:
- Principal-Agent Problem: Do the proxies have different goals than their sponsors?
- Plausible Deniability: How are sponsors hiding their involvement?

Constraints:
- Identify exactly 6 key actors.
- "Role": Must be specific (e.g., "State Sponsor", "Non-State Proxy").
- "Objective": What is their specific end-game? (Max 10 words).

Respond in JSON:
{
  "actors": [
    {"actor": "Name", "role": "Role", "objective": "Specific goal"}
  ]
}""",
            # Escalation paths
            """You are a Crisis Simulation Expert. Model the "Escalation Ladder" to predict how this gets worse.

Focus on "Flashpoints"—events that force a response.
Constraints:
- Identify exactly 3 escalation paths.
- "Trigger": A specific event (e.g., "Sinking of a naval vessel").
- "Risk": Low, Medium, High.

Respond in JSON:
{
  "escalation_paths": [
    {"trigger": "Specific event", "path": "Sequence of retaliation", "risk": "High"}
  ]
}""",
            # Off-ramps and constraints
            """You are a Diplomatic Strategist. Identify "Off-Ramps" and "Stabilizers".

How do we de-escalate without either side losing face?
Constraints:
- Off-ramps: Exactly 3 diplomatic options.
- Constraints: Exactly 3 limiting factors (e.g., "Economic exhaustion").
- Monitoring Signals: Exactly 3 indicators to watch.

Respond in JSON:
{
  "off_ramps": ["Option 1 (e.g., 'Ceasefire for hostage exchange')", "Option 2"],
  "constraints": ["Constraint 1", "Constraint 2"],
  "monitoring_signals": ["Signal 1 (e.g., 'Troop withdrawal')", "Signal 2"]
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
