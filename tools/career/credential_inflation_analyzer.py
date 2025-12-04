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
            """You are a Labor Economist and HR Systems Auditor. Detect "Degree Inflation" and "Credential Creep" where requirements exceed actual job functions.

Analyze the text for "Gatekeeping Mechanisms"—arbitrary barriers that filter out qualified talent without degrees.
Tone: {{tone}}

Text:
{{text}}

Perspective Framework:
- Signal vs. Noise: Does the degree predict performance, or just social class?
- Skill Gap: Is the requirement a lazy proxy for a specific skill (e.g., "CS Degree" vs. "Can code Python")?

Constraints:
- Identify exactly 3-5 inflation signals.
- "Why suspect": Must explain the disconnect between the role's output and the input requirement.
- Max 2 sentences per signal.

Respond in JSON:
{
  "inflation_signals": [
    {"requirement": "Specific text (e.g., 'Masters Degree required for Entry Level')", "why_suspect": "Explanation of why this is likely inflation (e.g., 'Role is administrative; degree is a proxy for conscientiousness, not skill.')"}
  ]
}""",
            # Skill-based equivalents
            """You are a Competency-Based Hiring Strategist. Translate academic credentials into verifiable "Proofs of Work".

For each inflation signal, propose a "Direct Skill Substitute" that proves ability better than the credential.
Focus on "Portfolio over Pedigree".

Signals: {{output[-1].inflation_signals}}

Example:
- Requirement: "MBA"
- Skill: "Financial Modeling & Strategic Planning"
- Proof: "Track record of managing $50k+ P&L or successful launch of a new business unit."

Constraints:
- Provide exactly 1 skill substitute per signal.
- "Proof" must be something a candidate can show, not just say.
- Max 20 words per field.

Respond in JSON:
{
  "skill_substitutes": [
    {"requirement": "Ref from previous step", "skills": ["Specific skill name"], "proofs": ["Specific portfolio item or test result"]}
  ]
}""",
            # Impact and advice
            """You are a Career Mobility Coach for non-traditional talent. Summarize the market impact and give tactical advice.

Impacts: Who gets left behind? (e.g., "Excludes 60% of workforce", "Ignores self-taught developers").
Advice: How to bypass the filter? (e.g., "Network directly", "Build a specific project").

Constraints:
- Impacts: Exactly 3 bullet points.
- Advice: Exactly 3 actionable steps.
- No generic advice like "Keep learning". Be specific.

Respond in JSON:
{
  "impacts": ["Specific impact 1", "Specific impact 2", "Specific impact 3"],
  "advice": ["Actionable step 1", "Actionable step 2", "Actionable step 3"]
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
