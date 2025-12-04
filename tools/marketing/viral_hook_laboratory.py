#!/usr/bin/env python3
"""
🧪 Viral Hook Laboratory (adult mode)

Generate and stress-test viral hooks: angles, headlines, risks, and ethics.

Usage:
    python tools/marketing/viral_hook_laboratory.py "Product/message"
    python tools/marketing/viral_hook_laboratory.py "Topic" --context "Audience, channel"
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


def viral_hook_laboratory(topic: str, additional_context: str = ""):
    print("🧪 Viral Hook Laboratory")
    print(f"Topic: {topic}")
    if additional_context:
        print(f"Context: {additional_context}")
    print()

    user_profile = load_user_context(project_root)
    tone = user_profile.get("writing_style", {}).get("tone", "Crisp and high-signal")

    client, model_names = build_models()
    model_info = (client, model_names[0])

    context_data = {
        "topic": topic,
        "additional_context": additional_context,
        "tone": tone,
    }

    result, context_filled_prompts, usage_stats = MinimalChainable.run(
        context=context_data,
        model=model_info,
        callable=prompt,
        prompts=[
            # Hooks
            """You are a Growth Hacker and Viral Engineer. Generate high-conversion hooks using "Curiosity Gaps" and "Pattern Interrupts".

Avoid clickbait (over-promising); focus on "High-Signal" intrigue.
Tone: {{tone}}
Context: {{additional_context}}

Perspective Framework:
- Contrarian: "Why everyone is wrong about X."
- Data-Driven: "The one metric that matters."
- Story: "How I lost everything and gained it back."

Constraints:
- Generate exactly 5 viral hooks.
- "Angle": The psychological lever used (e.g., "FOMO", "Status").
- "Headline": Max 12 words.

Respond in JSON:
{
  "hooks": [
    {"angle": "Angle used", "headline": "The actual headline"}
  ]
}""",
            # Risks and ethics
            """You are a Brand Safety Officer and Ethics Compliance Officer. Stress-test these hooks for "Reputational Risk".

Which hooks are "Engagement Bait" that will destroy trust long-term?
Hooks: {{output[-1].hooks}}

Constraints:
- Analyze exactly 3 hooks (the most risky ones).
- "Risk": Specific backlash scenario (e.g., "Audience feels tricked").
- "Ethics": Is this manipulative or just persuasive?

Respond in JSON:
{
  "risk_analysis": [
    {"hook": "Ref to headline", "risk": "Specific backlash risk", "ethics": "Ethical verdict (Pass/Fail)"}
  ]
}""",
            # Top picks
            """You are a Chief Marketing Officer. Select the "Winning Campaign" that balances Virality and Brand Equity.

We want attention, but not at the cost of trust.
Hooks: {{output[-2].hooks}}
Risks: {{output[-1].risk_analysis}}

Constraints:
- Select exactly 2 top hooks.
- "Guardrails": Specific instructions to the content team to keep it safe (e.g., "Must cite data source").

Respond in JSON:
{
  "top_hooks": [
    {"hook": "Winning headline", "why": "Why it wins", "guardrails": ["Guardrail 1"]}
  ]
}"""
        ],
        return_usage=True,
    )

    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    output_dir = os.path.join(project_root, "output", "marketing", "viral_hook_laboratory")
    os.makedirs(output_dir, exist_ok=True)

    output_path = os.path.join(output_dir, f"{timestamp}-viral_hooks.json")
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2)

    log_file = MinimalChainable.log_to_markdown("viral_hook_laboratory", context_filled_prompts, result, usage_stats)

    print(f"✅ Saved JSON to: {output_path}")
    print(f"✅ Log saved to: {log_file}")


def main():
    topic, context = get_input_from_args(
        description="Generate and stress-test viral hooks with risk/ethics guardrails"
    )
    viral_hook_laboratory(topic, context)


if __name__ == "__main__":
    main()
