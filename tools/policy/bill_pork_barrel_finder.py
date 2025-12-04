#!/usr/bin/env python3
"""
🐖 Bill Pork Barrel Finder (adult mode)

Scan a bill text or summary for pork, riders, beneficiaries, and red flags.

Usage:
    python tools/policy/bill_pork_barrel_finder.py "Bill text or summary"
    cat bill.txt | python tools/policy/bill_pork_barrel_finder.py
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


def bill_pork_barrel_finder(bill_text: str):
    print("🐖 Bill Pork Barrel Finder")
    print(f"Bill preview: {bill_text[:200]}{'...' if len(bill_text) > 200 else ''}\n")

    user_profile = load_user_context(project_root)
    tone = user_profile.get("writing_style", {}).get("tone", "Skeptical and concise")

    client, model_names = build_models()
    model_info = (client, model_names[0])

    context_data = {
        "bill": bill_text,
        "tone": tone,
    }

    result, context_filled_prompts, usage_stats = MinimalChainable.run(
        context=context_data,
        model=model_info,
        callable=prompt,
        prompts=[
            # Identify pork/riders
            """You are a legislative analyst. Identify likely pork/riders/unrelated provisions in the bill.
Tone: {{tone}}

Bill:
{{bill}}

Provide 3-7 items max; include why each is suspect and who pushed it if hinted.

Respond in JSON:
{
  "pork_items": [
    {"section": "identifier if any", "description": "what it does", "why_suspect": "reason", "hinted_sponsor": "if known/guess"}
  ]
}""",
            # Beneficiaries and pay-fors
            """List likely beneficiaries and pay-fors for each pork item.
Keep to top 3 per item.

Pork: {{output[-1].pork_items}}

Respond in JSON:
{
  "beneficiaries": [
    {"item": "ref", "who_benefits": ["actor"], "who_pays": ["actor"]}
  ]
}""",
            # Red flags and questions
            """Provide red flags and questions to ask before passage.
Give 3-5 red flags and 3-5 concise questions.

Respond in JSON:
{
  "red_flags": ["flag1", "flag2"],
  "questions": ["question1", "question2"]
}"""
        ],
        return_usage=True,
    )

    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    output_dir = os.path.join(project_root, "output", "policy", "bill_pork_barrel_finder")
    os.makedirs(output_dir, exist_ok=True)

    output_path = os.path.join(output_dir, f"{timestamp}-bill_pork_barrel.json")
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2)

    log_file = MinimalChainable.log_to_markdown("bill_pork_barrel_finder", context_filled_prompts, result, usage_stats)

    print(f"✅ Saved JSON to: {output_path}")
    print(f"✅ Log saved to: {log_file}")


def main():
    bill_text, _ = get_input_from_args(
        description="Find pork/riders/beneficiaries in a bill text or summary",
        default_context_help="(unused)"
    )
    bill_pork_barrel_finder(bill_text)


if __name__ == "__main__":
    main()
