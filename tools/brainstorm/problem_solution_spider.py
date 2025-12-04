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
            """You are a Senior Product Manager and Crisis Fixer. Your goal is to define the problem with absolute clarity for an executive audience.

Analyze the input to identify the core dysfunction, the specific victims, and the business/operational impact.
Tone: {{tone}}
Context: {{additional_context}}

Problem: {{problem}}

Perspective Framework:
- Who: The specific user or system segment affected.
- What: The precise mechanism of failure.
- Why: The quantifiable cost or risk (time, money, reputation).

Constraints:
- Maximum 3 sentences.
- No jargon unless strictly necessary.
- Focus on root cause, not symptoms.

Respond in JSON:
{
  "defined_problem": "A single, punchy definition of the core issue.",
  "stakes": ["Specific consequence 1 (e.g., 'Losing $5k/day')", "Specific consequence 2"]
}""",
            # Constraints and resources
            """You are a Logistics & Operations Strategist. Map the battlefield constraints and available arsenal.

Identify the hard limits (budget, time, physics, policy) and the usable assets (people, tools, data, leverage).
Avoid generic answers like "time" or "money"—be specific (e.g., "Must launch by Q3", "$50k budget cap").

Problem: {{output[-1].defined_problem}}
Context: {{additional_context}}

Constraints:
- List exactly 3-5 hard constraints.
- List exactly 3-5 usable resources.
- Each item must be under 10 words.

Respond in JSON:
{
  "constraints": ["Hard constraint 1", "Hard constraint 2", "Hard constraint 3"],
  "resources": ["Resource 1", "Resource 2", "Resource 3"]
}""",
            # Wild ideas
            """You are a Radical Innovation Consultant. Generate unconventional, high-leverage solutions that bypass standard bottlenecks.

Use the "Lateral Thinking" framework:
- Inversion: What if we did the opposite?
- Exaggeration: What if we had infinite resources?
- Substitution: What if we replaced the core mechanism?

Constraints: {{output[-1].constraints}}
Resources: {{output[-1].resources}}

Example GOOD Idea: "Automate the entire intake via SMS bot to bypass the broken web portal."
Example BAD Idea: "Fix the website." (Too obvious/conventional)

Constraints:
- Generate exactly 5 wild ideas.
- Each idea must be feasible within physics, even if politically difficult.
- "Feasibility" score: Low, Medium, High.

Respond in JSON:
{
  "wild_ideas": [
    {"idea": "Description of the wild idea", "feasibility": "High", "why_it_might_work": "Specific mechanism of action"}
  ]
}""",
            # Combine and shape
            """You are a Pragmatic Systems Architect. Synthesize the wild ideas into viable, robust solution options.

Combine the most promising elements of the wild ideas into 1-2 coherent strategies.
Focus on "Pareto Efficiency"—80% of the benefit for 20% of the effort.

Wild ideas: {{output[-1].wild_ideas}}

Constraints:
- Create exactly 2 distinct solution options.
- "Edge cases" must be specific failure modes (e.g., "User loses internet connection").
- "Tradeoffs" must be real costs (e.g., "Higher latency", "Requires manual review").

Respond in JSON:
{
  "solution_options": [
    {"option": "Name and description of the solution", "edge_cases": ["Edge case 1"], "tradeoffs": ["Tradeoff 1"]}
  ]
}""",
            # Test scenario
            """You are a QA Lead and Experiment Designer. Design a "Smoke Test" to validate the best solution option immediately.

Create a test that requires minimal build time but yields high signal.
Focus on "Falsifiability"—how can we prove this fails quickly?

Solutions: {{output[-1].solution_options}}
Problem: {{output[-4].defined_problem}}

Constraints:
- Scenario must be testable in < 24 hours.
- Maximum 4 sentences for the scenario.
- List exactly 3 success signals and 3 failure signals.

Respond in JSON:
{
  "test_scenario": "Step-by-step description of the quick test.",
  "success_signals": ["Signal 1 (e.g., 'Conversion > 5%')", "Signal 2"],
  "failure_signals": ["Signal 1 (e.g., 'Server crash')", "Signal 2"],
  "next_steps": ["Immediate next action 1", "Immediate next action 2"]
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
