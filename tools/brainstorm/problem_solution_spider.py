#!/usr/bin/env python3
"""
🕷️ Problem–Solution Spider (adult mode)

Clarify a problem, constraints, wild ideas, blended solutions, and a quick test scenario.

Usage:
    python tools/brainstorm/problem_solution_spider.py "Problem statement"
    python tools/brainstorm/problem_solution_spider.py "Problem" --context "Constraints, stakeholders, goals"
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


def problem_solution_spider(problem: str, additional_context: str = ""):
    print("🕷️ Problem–Solution Spider")
    print(f"Problem: {problem}")
    if additional_context:
        print(f"Context/constraints: {additional_context}")
    print()

    user_profile = load_user_context(project_root)
    tone = user_profile.get("writing_style", {}).get("tone", "Direct")

    client, model_names = build_models()
    model_info = (client, model_names[0])

    context_data = {
        "problem": problem,
        "additional_context": additional_context,
        "tone": tone,
    }

    result, context_filled_prompts, usage_stats = MinimalChainable.run(
        context=context_data,
        model=model_info,
        callable=prompt,
        prompts=[
            # Define the problem crisply
            """Define the problem succinctly for an adult operator.
Include who is affected, what breaks, and why it matters.
Tone: {{tone}}
Context: {{additional_context}}

Problem: {{problem}}

Respond in JSON:
{
  "defined_problem": "crisp definition",
  "stakes": ["stake 1", "stake 2"]
}""",
            # Constraints and resources
            """List constraints and available resources for tackling the problem.
Be realistic; avoid generic answers.

Problem: {{output[-1].defined_problem}}
Context: {{additional_context}}

Respond in JSON:
{
  "constraints": ["constraint1", "constraint2"],
  "resources": ["resource1", "resource2"]
}""",
            # Wild ideas
            """Brainstorm 4-5 unconventional ideas to solve the problem within/around the constraints.
Signal feasibility at a glance.

Constraints: {{output[-1].constraints}}
Resources: {{output[-1].resources}}

Respond in JSON:
{
  "wild_ideas": [
    {"idea": "description", "feasibility": "low/med/high", "why_it_might_work": "reason"}
  ]
}""",
            # Combine and shape
            """Combine the best parts of the wild ideas into 1-2 pragmatic solution options.
Show why they are better than the originals.

Wild ideas: {{output[-1].wild_ideas}}

Respond in JSON:
{
  "solution_options": [
    {"option": "description", "edge_cases": ["case1"], "tradeoffs": ["tradeoff1"]}
  ]
}""",
            # Test scenario
            """Draft a quick test scenario to validate the leading option.
Include success/failure signals and next steps.

Solutions: {{output[-1].solution_options}}
Problem: {{output[-4].defined_problem}}

Respond in JSON:
{
  "test_scenario": "short scenario",
  "success_signals": ["signal1", "signal2"],
  "failure_signals": ["signal1", "signal2"],
  "next_steps": ["step1", "step2"]
}"""
        ],
        return_usage=True,
    )

    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    output_dir = os.path.join(project_root, "output", "brainstorm", "problem_solution_spider")
    os.makedirs(output_dir, exist_ok=True)

    output_path = os.path.join(output_dir, f"{timestamp}-problem_solution.json")
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2)

    log_file = MinimalChainable.log_to_markdown("problem_solution_spider", context_filled_prompts, result, usage_stats)

    print(f"✅ Saved JSON to: {output_path}")
    print(f"✅ Log saved to: {log_file}")


def main():
    problem, context = get_input_from_args(
        description="Map problems to constraints, wild ideas, blended solutions, and a quick test"
    )
    problem_solution_spider(problem, context)


if __name__ == "__main__":
    main()
