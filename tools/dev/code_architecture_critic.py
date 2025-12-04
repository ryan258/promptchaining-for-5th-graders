#!/usr/bin/env python3
"""
🏗️ Code Architecture Critic (adult mode)

Audit a code snippet for patterns/anti-patterns, smells, refactors, risks, and an improved architecture sketch.

Usage:
    python tools/dev/code_architecture_critic.py "path/to/file.py"
    python tools/dev/code_architecture_critic.py "inline code here"
    python tools/dev/code_architecture_critic.py "code" --context "constraints, tech stack, goals"
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


def _load_code(input_str: str) -> str:
    if os.path.isfile(input_str):
        with open(input_str, "r", encoding="utf-8") as f:
            return f.read()
    return input_str


def code_architecture_critic(code_input: str, additional_context: str = ""):
    print("🏗️ Code Architecture Critic")

    code = _load_code(code_input)
    print(f"Analyzing snippet length: {len(code)} chars")
    if additional_context:
        print(f"Context: {additional_context}")
    print()

    user_profile = load_user_context(project_root)
    tone = user_profile.get("writing_style", {}).get("tone", "Pragmatic")
    priorities = user_profile.get("dev_priorities", [])

    client, model_names = build_models()
    model_info = (client, model_names[0])

    context_data = {
        "code": code,
        "tone": tone,
        "additional_context": additional_context,
        "priorities": ", ".join(priorities) if priorities else "",
    }

    result, context_filled_prompts, usage_stats = MinimalChainable.run(
        context=context_data,
        model=model_info,
        callable=prompt,
        prompts=[
            # Identify patterns / anti-patterns
            """You are an experienced software architect.

Analyze the following code for patterns and anti-patterns. Keep it concise and actionable.
Tone: {{tone}}
Priorities: {{priorities}}
Additional context: {{additional_context}}

Code:
{{code}}

Provide 3-7 patterns/anti-patterns total; keep each to one sentence.

Respond in JSON:
{
  "patterns": ["pattern 1", "pattern 2"],
  "anti_patterns": ["anti-pattern 1", "anti-pattern 2"],
  "tech_debt_risks": ["risk 1", "risk 2"]
}""",
            # Code smells / hotspots
            """Detail concrete code smells and hotspots based on the anti-patterns and risks.

Anti-patterns: {{output[-1].anti_patterns}}
Tech debt risks: {{output[-1].tech_debt_risks}}

Provide top 5 smells; include where + impact.

Respond in JSON:
{
  "code_smells": [
    {"smell": "name", "where": "file/area", "impact": "short impact", "risk_window": "now/soon/later"}
  ],
  "gaps": ["missing tests/types/logging/etc"]
}""",
            # Refactor plan
            """Propose a pragmatic refactor plan for the code.
Include sequencing, safety nets, and quick wins.

Code smells: {{output[-1].code_smells}}
Gaps: {{output[-1].gaps}}

Limit quick_wins to 3; refactor_plan steps to 5; safety_nets to 3.

Respond in JSON:
{
  "quick_wins": ["step 1", "step 2"],
  "refactor_plan": [
    {"step": "description", "why": "value", "risk": "low/med/high"}
  ],
  "safety_nets": ["tests or checks to add"]
}""",
            # Consequence of doing nothing
            """If we do nothing, what breaks and when?
Be specific about failure modes and maintenance pain.

Refactor plan: {{output[-1].refactor_plan}}

Respond in JSON:
{
  "maintenance_forecast": [
    {"horizon": "short/medium/long", "pain": "description", "who_feels_it": "team/users"}
  ]
}""",
            # Improved architecture sketch
            """Describe an improved architecture for this code.
Prefer a minimal, testable, dependency-light shape.

Use Mermaid if natural; otherwise clear text.

Respond in JSON:
{
  "architecture": "mermaid_or_text",
  "principles": ["principle 1", "principle 2"],
  "review_checklist": ["check 1", "check 2"]
}"""
        ],
        return_usage=True,
    )

    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    output_dir = os.path.join(project_root, "output", "dev", "code_architecture_critic")
    os.makedirs(output_dir, exist_ok=True)

    output_path = os.path.join(output_dir, f"{timestamp}-architecture_critic.json")
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2)

    log_file = MinimalChainable.log_to_markdown("code_architecture_critic", context_filled_prompts, result, usage_stats)

    print(f"✅ Saved JSON to: {output_path}")
    print(f"✅ Log saved to: {log_file}")


def main():
    topic, context = get_input_from_args(
        description="Audit a code snippet for patterns/anti-patterns, smells, refactors, and architecture improvements"
    )
    code_architecture_critic(topic, context)


if __name__ == "__main__":
    main()
