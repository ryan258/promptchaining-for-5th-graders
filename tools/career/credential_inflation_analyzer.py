#!/usr/bin/env python3
"""
🎓 Credential Inflation Analyzer (adult mode)

Analyze credential creep in a role/industry, detect gatekeeping, and propose skill-based alternatives.

Usage:
    python tools/career/credential_inflation_analyzer.py "Job/role description"
    cat role.txt | python tools/career/credential_inflation_analyzer.py
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


def credential_inflation_analyzer(text: str):
    print("🎓 Credential Inflation Analyzer")
    print(f"Role preview: {text[:200]}{'...' if len(text) > 200 else ''}\n")

    user_profile = load_user_context(project_root)
    tone = user_profile.get("writing_style", {}).get("tone", "Blunt and pragmatic")

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
            # Identify inflation signals
            """Identify signs of credential inflation or unnecessary gatekeeping.
Tone: {{tone}}

Text:
{{text}}

Give 3-5 signals max; include why each is suspect.

Respond in JSON:
{
  "inflation_signals": [
    {"requirement": "what", "why_suspect": "reason (1 sentence)"}
  ]
}""",
            # Skill-based equivalents
            """Map skills or proofs-of-work that would substitute for inflated credentials.
Provide 1-2 substitutes per signal; keep concise.

Signals: {{output[-1].inflation_signals}}

Respond in JSON:
{
  "skill_substitutes": [
    {"requirement": "ref", "skills": ["skill1"], "proofs": ["portfolio/test"]}
  ]
}""",
            # Impact and advice
            """Summarize impact on candidates and practical advice to navigate or counter credential creep.
Impacts: 2-3 bullets. Advice: 3-5 bullets, specific actions.

Respond in JSON:
{
  "impacts": ["impact1", "impact2"],
  "advice": ["step1", "step2"]
}"""
        ],
        return_usage=True,
    )

    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    output_dir = os.path.join(project_root, "output", "career", "credential_inflation_analyzer")
    os.makedirs(output_dir, exist_ok=True)

    output_path = os.path.join(output_dir, f"{timestamp}-credential_inflation.json")
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2)

    log_file = MinimalChainable.log_to_markdown("credential_inflation_analyzer", context_filled_prompts, result, usage_stats)

    print(f"✅ Saved JSON to: {output_path}")
    print(f"✅ Log saved to: {log_file}")


def main():
    text, _ = get_input_from_args(
        description="Analyze credential inflation and propose skill-based alternatives",
        default_context_help="(unused)"
    )
    credential_inflation_analyzer(text)


if __name__ == "__main__":
    main()
