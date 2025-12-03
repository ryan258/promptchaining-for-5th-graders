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
            """Generate 5 viral hook angles for {{topic}} tailored to audience/channel if given.
Tone: {{tone}}
Context: {{additional_context}}

Respond in JSON:
{
  "hooks": [
    {"angle": "idea", "headline": "headline"}
  ]
}""",
            # Risks and ethics
            """Assess risks/ethics for each hook (backlash, misinformation, manipulation).

Hooks: {{output[-1].hooks}}

Respond in JSON:
{
  "risk_analysis": [
    {"hook": "ref", "risk": "risk description", "ethics": "concern if any"}
  ]
}""",
            # Top picks
            """Select top 2 hooks balancing virality and acceptable risk; propose guardrails.

Hooks: {{output[-2].hooks}}
Risks: {{output[-1].risk_analysis}}

Respond in JSON:
{
  "top_hooks": [
    {"hook": "headline", "why": "reason", "guardrails": ["guardrail1"]}
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
