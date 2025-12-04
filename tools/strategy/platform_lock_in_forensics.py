#!/usr/bin/env python3
"""
🔒 Platform Lock-in Forensics (adult mode)

Analyze a platform/product for lock-in mechanisms, incentives, and exit strategies.

Usage:
    python tools/strategy/platform_lock_in_forensics.py "Platform description"
    python tools/strategy/platform_lock_in_forensics.py "Platform" --context "Use case/constraints"
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


def platform_lock_in_forensics(platform: str, additional_context: str = ""):
    print("🔒 Platform Lock-in Forensics")
    print(f"Platform: {platform}")
    if additional_context:
        print(f"Context: {additional_context}")
    print()

    user_profile = load_user_context(project_root)
    tone = user_profile.get("writing_style", {}).get("tone", "Technical and pragmatic")

    client, model_names = build_models()
    model_info = (client, model_names[0])

    context_data = {
        "platform": platform,
        "additional_context": additional_context,
        "tone": tone,
    }

    result, context_filled_prompts, usage_stats = MinimalChainable.run(
        context=context_data,
        model=model_info,
        callable=prompt,
        prompts=[
            # Lock-in mechanisms
            """Identify lock-in mechanisms (data moats, APIs, pricing, contracts, ecosystem).
Tone: {{tone}}

Platform/use case: {{platform}}
Context: {{additional_context}}

Provide 3-6 mechanisms; keep each specific.

Respond in JSON:
{
  "lock_in_mechanisms": [
    {"type": "data/api/pricing/etc", "evidence": "short"}
  ]
}""",
            # Incentives and switching costs
            """Map incentives for the vendor and switching costs for the customer.
Switching costs: list 3-5, concrete (time $, risk).

Mechanisms: {{output[-1].lock_in_mechanisms}}

Respond in JSON:
{
  "switching_costs": ["cost1", "cost2"],
  "vendor_incentives": ["incentive1", "incentive2"]
}""",
            # Exit strategies
            """Suggest exit or mitigation strategies (data portability, abstractions, contract terms).
Provide 3-5 mitigations; pair each with a monitoring signal.

Respond in JSON:
{
  "mitigations": ["mitigation1", "mitigation2"],
  "early_warning_signals": ["signal1", "signal2"]
}"""
        ],
        return_usage=True,
    )

    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    output_dir = os.path.join(project_root, "output", "strategy", "platform_lock_in_forensics")
    os.makedirs(output_dir, exist_ok=True)

    output_path = os.path.join(output_dir, f"{timestamp}-platform_lock_in.json")
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2)

    log_file = MinimalChainable.log_to_markdown("platform_lock_in_forensics", context_filled_prompts, result, usage_stats)

    print(f"✅ Saved JSON to: {output_path}")
    print(f"✅ Log saved to: {log_file}")


def main():
    platform, context = get_input_from_args(
        description="Analyze platform lock-in mechanisms and exit strategies"
    )
    platform_lock_in_forensics(platform, context)


if __name__ == "__main__":
    main()
