#!/usr/bin/env python3
"""
🎯 Dream Job Reverse Engineer (adult mode)

Decode a job posting for hidden priorities, pain points, application strategy, resume bullets, and STAR stories.

Usage:
    python tools/career/dream_job_reverse_engineer.py "path/to/job.txt"
    python tools/career/dream_job_reverse_engineer.py "Job text here" --context "Your profile, target angle"
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


def _load_text(input_str: str) -> str:
    if os.path.isfile(input_str):
        with open(input_str, "r", encoding="utf-8") as f:
            return f.read()
    return input_str


def dream_job_reverse_engineer(job_posting: str, additional_context: str = ""):
    print("🎯 Dream Job Reverse Engineer")

    posting = _load_text(job_posting)
    print(f"Posting length: {len(posting)} chars")
    if additional_context:
        print(f"Context: {additional_context}")
    print()

    user_profile = load_user_context(project_root)
    tone = user_profile.get("writing_style", {}).get("tone", "Confident and direct")
    career = user_profile.get("career_profile", {})

    client, model_names = build_models()
    model_info = (client, model_names[0])

    context_data = {
        "job_posting": posting,
        "tone": tone,
        "additional_context": additional_context,
        "target_role": career.get("target_role", ""),
        "notable_wins": ", ".join(career.get("wins", [])),
    }

    result, context_filled_prompts, usage_stats = MinimalChainable.run(
        context=context_data,
        model=model_info,
        callable=prompt,
        prompts=[
            # Decode hidden priorities
            """You are a senior hiring manager decoding a job posting.
Tone: {{tone}}
Additional context: {{additional_context}}
Target role (if provided): {{target_role}}

Posting:
{{job_posting}}

Respond in JSON:
{
  "hidden_priorities": ["priority1", "priority2"],
  "culture_vibe": "concise read of culture",
  "red_flags": ["flag1", "flag2"]
}""",
            # Manager pain points
            """List the specific pain points the hiring manager is trying to solve.
Priorities: {{output[-1].hidden_priorities}}
Culture: {{output[-1].culture_vibe}}

Respond in JSON:
{
  "manager_pain_points": ["pain1", "pain2", "pain3"]
}""",
            # Application strategy
            """Craft an application strategy that hooks to the pain points.
Include positioning theme and proof vectors.

Pain points: {{output[-1].manager_pain_points}}
Notable wins: {{notable_wins}}

Respond in JSON:
{
  "application_theme": "short theme",
  "strategy_angle": "1-2 sentence angle",
  "proof_targets": ["win or project to highlight"]
}""",
            # Resume bullets
            """Write 3 resume bullets aligned to the strategy.
Use strong verbs, quantified outcomes, and relevance to pain points.

Pain points: {{output[-2].manager_pain_points}}
Theme: {{output[-1].application_theme}}
Proof targets: {{output[-1].proof_targets}}

Respond in JSON:
{
  "resume_bullets": ["bullet1", "bullet2", "bullet3"]
}""",
            # STAR stories
            """Draft STAR mini-outlines to back up each bullet.
Keep them concise and ready to expand in interview prep.

Bullets: {{output[-1].resume_bullets}}

Respond in JSON:
{
  "interview_stories": [
    {"bullet": "bullet text", "star": {"situation": "S", "task": "T", "action": "A", "result": "R"}}
  ]
}"""
        ],
        return_usage=True,
    )

    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    output_dir = os.path.join(project_root, "output", "career", "dream_job_reverse_engineer")
    os.makedirs(output_dir, exist_ok=True)

    output_path = os.path.join(output_dir, f"{timestamp}-dream_job.json")
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2)

    log_file = MinimalChainable.log_to_markdown("dream_job_reverse_engineer", context_filled_prompts, result, usage_stats)

    print(f"✅ Saved JSON to: {output_path}")
    print(f"✅ Log saved to: {log_file}")


def main():
    posting, context = get_input_from_args(
        description="Reverse engineer a job posting into strategy, bullets, and STAR stories",
        default_context_help="Your profile, constraints, or angle"
    )
    dream_job_reverse_engineer(posting, context)


if __name__ == "__main__":
    main()
