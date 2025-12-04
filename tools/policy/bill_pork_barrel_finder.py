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
            """You are a Fiscal Hawk and Legislative Watchdog. Audit this bill for "Pork Barrel Spending" and "Poison Pill Riders".

Identify non-germane provisions added to buy votes.
Tone: {{tone}}

Bill:
{{bill}}

Perspective Framework:
- Earmarks: Directing funds to a specific entity without competition.
- Logrolling: "I'll vote for your pork if you vote for mine."

Constraints:
- Identify exactly 5 suspicious items.
- "Why Suspect": Explain the specific mechanism of waste (e.g., "No competitive bidding").
- "Hinted Sponsor": Who likely inserted this? (e.g., "Senator from [State]").

Respond in JSON:
{
  "pork_items": [
    {"section": "Section 123", "description": "Description of provision", "why_suspect": "Reason it's pork", "hinted_sponsor": "Likely sponsor"}
  ]
}""",
            # Beneficiaries and pay-fors
            """Follow the Money. Who wins and who pays?

Pork: {{output[-1].pork_items}}

Constraints:
- Beneficiaries: Specific companies, unions, or donors (not just "The public").
- Pay-fors: Who bears the cost? (e.g., "Taxpayers", "Future generations").

Respond in JSON:
{
  "beneficiaries": [
    {"item": "Ref to Section 123", "who_benefits": ["Specific Entity"], "who_pays": ["Specific Group"]}
  ]
}""",
            # Red flags and questions
            """You are a Citizen Journalist. What questions should we scream at the press briefing?

Constraints:
- Red Flags: Exactly 3 systemic issues.
- Questions: Exactly 3 "Gotcha" questions that demand a specific answer.

Respond in JSON:
{
  "red_flags": ["Flag 1 (e.g., 'Passed at midnight')", "Flag 2"],
  "questions": ["Question 1 (e.g., 'Why is this bridge funded from the education budget?')", "Question 2"]
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
