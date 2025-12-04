#!/usr/bin/env python3
"""
📋 Campaign Promise Tracker (adult mode)

Extract, classify, and risk-check promises from campaign text; track plausibility and verification hooks.

Usage:
    python tools/politics/campaign_promise_tracker.py "Speech/manifesto text"
    cat promises.txt | python tools/politics/campaign_promise_tracker.py
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


def campaign_promise_tracker(text: str):
    print("📋 Campaign Promise Tracker")
    print(f"Input preview: {text[:200]}{'...' if len(text) > 200 else ''}\n")

    user_profile = load_user_context(project_root)
    tone = user_profile.get("writing_style", {}).get("tone", "Neutral and precise")

    client, model_names = build_models()
    model_info = (client, model_names[0])

    context_data = {
        "text": text,
        "tone": tone,
    }

    result, context_filled_prompts, usage_stats = MinimalChainable.run(
        context=context_data,
        model=model_info,
        callable=prompt,
        prompts=[
            # Extract promises
            """You are a campaign fact-auditor. Extract concrete promises/commitments from the text.
Tone: {{tone}}

Text:
{{text}}

Provide 3-7 promises max. Avoid vague slogans.

Respond in JSON:
{
  "promises": [
    {"promise": "what", "area": "policy area", "timeframe": "if stated"}
  ]
}""",
            # Feasibility and risks
            """Assess feasibility, blockers, and risks for each promise.
Keep each field 1 sentence max.

Promises: {{output[-1].promises}}

Respond in JSON:
{
  "analysis": [
    {"promise": "ref", "feasibility": "Low/Med/High", "blockers": ["blocker1"], "risks": ["risk1"]}
  ]
}""",
            # Verification hooks
            """Provide verification hooks and milestones to track delivery.
2-3 hooks per promise; milestones should be measurable.

Analysis: {{output[-1].analysis}}

Respond in JSON:
{
  "verification_hooks": [
    {"promise": "ref", "metric": "what to measure", "milestones": ["m1", "m2"]}
  ]
}"""
        ],
        return_usage=True,
    )

    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    output_dir = os.path.join(project_root, "output", "politics", "campaign_promise_tracker")
    os.makedirs(output_dir, exist_ok=True)

    output_path = os.path.join(output_dir, f"{timestamp}-campaign_promises.json")
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2)

    log_file = MinimalChainable.log_to_markdown("campaign_promise_tracker", context_filled_prompts, result, usage_stats)

    print(f"✅ Saved JSON to: {output_path}")
    print(f"✅ Log saved to: {log_file}")


def main():
    text, _ = get_input_from_args(
        description="Extract and analyze campaign promises with feasibility and tracking hooks",
        default_context_help="(unused)"
    )
    campaign_promise_tracker(text)


if __name__ == "__main__":
    main()
