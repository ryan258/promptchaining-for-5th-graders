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
            """You are a Principal Software Architect and Code Archaeologist. Audit the codebase for structural integrity and long-term viability.

Analyze the code for "Design Patterns" (Gang of Four) and "Anti-Patterns" (e.g., God Object, Shotgun Surgery).
Tone: {{tone}}
Priorities: {{priorities}}
Additional context: {{additional_context}}

Code:
{{code}}

Perspective Framework:
- SOLID Principles: Are they violated?
- DRY (Don't Repeat Yourself) vs. WET (Write Everything Twice): Is duplication accidental or intentional?
- Coupling vs. Cohesion: Is the code loosely coupled but highly cohesive?

Constraints:
- Identify exactly 3 patterns (Good) and 3 anti-patterns (Bad).
- "Tech Debt Risks": Must be specific failure scenarios (e.g., "Race condition in auth").
- Max 1 sentence per item.

Respond in JSON:
{
  "patterns": ["Pattern 1 (e.g., 'Factory Method used correctly')", "Pattern 2"],
  "anti_patterns": ["Anti-pattern 1 (e.g., 'Tight coupling in UI')", "Anti-pattern 2"],
  "tech_debt_risks": ["Risk 1", "Risk 2"]
}""",
            # Code smells / hotspots
            """You are a Code Quality Auditor. Locate specific "Code Smells" that indicate deeper rot.

Focus on "Hotspots"—areas with high complexity and high churn risk.
Anti-patterns: {{output[-1].anti_patterns}}
Tech Debt Risks: {{output[-1].tech_debt_risks}}

Constraints:
- Identify exactly 5 specific code smells.
- "Where": Line number range or function name.
- "Impact": Why this hurts maintainability (max 10 words).

Respond in JSON:
{
  "code_smells": [
    {"smell": "Name (e.g., 'Long Method')", "where": "Function/Area", "impact": "Hard to test", "risk_window": "Immediate/Near-term"}
  ],
  "gaps": ["Missing Unit Tests", "No Error Handling"]
}""",
            # Refactor plan
            """You are a Technical Lead planning a "Strangler Fig" migration or refactor. Create a pragmatic plan.

Prioritize "Quick Wins" (low effort, high impact) to build momentum.
Code smells: {{output[-1].code_smells}}
Gaps: {{output[-1].gaps}}

Constraints:
- Quick Wins: Exactly 3 steps.
- Refactor Plan: Exactly 5 sequential steps.
- Safety Nets: Exactly 3 protections (e.g., "Feature Flag").

Respond in JSON:
{
  "quick_wins": ["Step 1", "Step 2", "Step 3"],
  "refactor_plan": [
    {"step": "Actionable step", "why": "Value proposition", "risk": "Low/Med/High"}
  ],
  "safety_nets": ["Safety net 1", "Safety net 2", "Safety net 3"]
}""",
            # Consequence of doing nothing
            """You are a Reliability Engineer forecasting the "Cost of Inaction". What happens if we ignore this?

Be specific about "Failure Modes" and "Maintenance Drag".
Refactor plan: {{output[-1].refactor_plan}}

Constraints:
- Forecast: Short (1 month), Medium (6 months), Long (1 year).
- "Pain": Concrete symptoms (e.g., "On-call pages increase 50%").

Respond in JSON:
{
  "maintenance_forecast": [
    {"horizon": "Short Term", "pain": "Description of pain", "who_feels_it": "Dev Team"}
  ]
}""",
            # Improved architecture sketch
            """You are a Systems Designer. Propose the "Ideal State" architecture.

Focus on "Testability" and "Modularity".
Use Mermaid syntax for the diagram if possible, or clear text description.

Constraints:
- Principles: Exactly 3 guiding principles for the new design.
- Checklist: Exactly 3 criteria to approve the refactor.

Respond in JSON:
{
  "architecture": "Mermaid diagram code or text description",
  "principles": ["Principle 1 (e.g., 'Single Responsibility')", "Principle 2", "Principle 3"],
  "review_checklist": ["Check 1", "Check 2", "Check 3"]
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
