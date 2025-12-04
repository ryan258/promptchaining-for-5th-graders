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
            """You are a Policy Analyst and Accountability Watchdog. Audit this campaign text for "Hard Commitments".

Distinguish between "Puffery" (vague slogans) and "Actionable Promises".
Tone: {{tone}}

Text:
{{text}}

Perspective Framework:
- SMART Criteria: Specific, Measurable, Achievable, Relevant, Time-bound.
- The "Read My Lips" Test: Is this a clear pledge that can be broken?

Constraints:
- Identify exactly 5 concrete promises.
- "Promise": Quote the exact commitment.
- "Timeframe": If not stated, mark as "Indefinite".

Respond in JSON:
{
  "promises": [
    {"promise": "Quote of promise", "area": "Policy Area (e.g., 'Healthcare')", "timeframe": "By 2025 / First 100 Days"}
  ]
}""",
            # Feasibility and risks
            """Stress-test these promises. Are they legislative fantasy or executive reality?

Promises: {{output[-1].promises}}

Constraints:
- Feasibility: Low, Medium, High.
- "Blockers": Specific legislative or judicial hurdles (e.g., "Requires 60 votes in Senate").
- "Risks": Unintended consequences (Max 1 sentence).

Respond in JSON:
{
  "analysis": [
    {"promise": "Ref to promise", "feasibility": "Low", "blockers": ["Filibuster", "Court Challenge"], "risks": ["Inflationary pressure"]}
  ]
}""",
            # Verification hooks
            """Establish a "Truth-Tracking Protocol". How will we know if they failed?

Analysis: {{output[-1].analysis}}

Constraints:
- Metric: A specific number or binary outcome (e.g., "Unemployment rate < 4%").
- Milestones: Exactly 2 observable steps on the path.

Respond in JSON:
{
  "verification_hooks": [
    {"promise": "Ref to promise", "metric": "Specific KPI", "milestones": ["Bill introduced", "Signed into law"]}
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
