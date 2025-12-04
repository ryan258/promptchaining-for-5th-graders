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
            """You are a CTO and Antitrust Expert. Audit this platform for "Vendor Lock-in" and "Moats".

Identify technical, legal, and economic barriers to exit.
Tone: {{tone}}

Platform/use case: {{platform}}
Context: {{additional_context}}

Perspective Framework:
- The "California Hotel" Principle: You can check out any time you like, but you can never leave.
- Data Gravity: Applications move to where the data resides.

Constraints:
- Mechanisms: Exactly 3 distinct lock-in types.
- Evidence: Specific features or terms (e.g., "Egress fees").
- Severity: Low, Medium, High.

Respond in JSON:
{
  "lock_in_mechanisms": [
    {"type": "Data / API / Pricing / Ecosystem", "evidence": "Description of the trap", "severity": "High"}
  ]
}""",
            # Incentives and switching costs
            """Calculate the "Switching Cost" equation. Why is staying easier than leaving?

Mechanisms: {{output[-1].lock_in_mechanisms}}

Constraints:
- Costs: Exactly 3 concrete friction points (Time, Money, Risk).
- Incentives: Why the vendor wants you trapped (e.g., "Upsell path").

Respond in JSON:
{
  "switching_costs": ["Cost 1 (e.g., 'Rewriting all SQL queries')", "Cost 2"],
  "vendor_incentives": ["Incentive 1", "Incentive 2"]
}""",
            # Exit strategies
            """Design an "Escape Hatch". How do we maintain optionality?

Constraints:
- Mitigations: Exactly 2 strategic moves (e.g., "Use open standards").
- Signals: Exactly 2 warning signs to watch for.

Respond in JSON:
{
  "mitigations": ["Mitigation 1 (e.g., 'Build an abstraction layer')", "Mitigation 2"],
  "early_warning_signals": ["Signal 1 (e.g., 'Proprietary API extensions')", "Signal 2"]
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
