#!/usr/bin/env python3
"""
🧭 Concept Simplifier (adult mode)

Break complex topics into digestible parts with analogies, examples, and a short explainer.

Usage:
    python tools/learning/concept_simplifier.py "Diffusion models in AI"
    python tools/learning/concept_simplifier.py "Topic" --context "Audience, constraints, tone"
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


def concept_simplifier(topic: str, additional_context: str = ""):
    print("🧭 Concept Simplifier")
    print(f"Topic: {topic}")
    if additional_context:
        print(f"Context: {additional_context}")
    print()

    user_profile = load_user_context(project_root)
    tone = user_profile.get("writing_style", {}).get("tone", "Clear and direct")
    audience = user_profile.get("learning_profile", {}).get("audience", "Curious adult")

    client, model_names = build_models()
    model_info = (client, model_names[0])

    context_data = {
        "topic": topic,
        "tone": tone,
        "audience": audience,
        "additional_context": additional_context,
    }

    result, context_filled_prompts, usage_stats = MinimalChainable.run(
        context=context_data,
        model=model_info,
        callable=prompt,
        prompts=[
            # Decompose the concept
            """Decompose the concept '{{topic}}' for a {{audience}}.
Include 3-6 essential components (no trivia).
Keep phrasing concise but adult-ready.

Example pattern:
GOOD: name = "Data ingestion", why_it_matters = "Everything downstream fails if inputs are messy"
BAD: name = "All the things", why_it_matters = "It is important" (too vague)

Respond in JSON:
{
  "components": [
    {"name": "component", "why_it_matters": "short reason"},
    ...
  ]
}""",
            # Analogies per component
            """Create practical analogies for each component of '{{topic}}' to accelerate understanding.
Components: {{output[-1].components}}
Prefer analogies from everyday work/life; avoid cutesy.

Respond in JSON:
{
  "analogies": [
    {"component": "name", "analogy": "analogy", "when_it_breaks_down": "limit"}
  ]
}""",
            # Concrete examples/tests
            """Provide concrete examples or quick tests to validate understanding for each analogy.
Topic: {{topic}}
Analogies: {{output[-1].analogies}}

For each, include:
- example: 2-3 sentence concrete scenario showing the analogy in action
- check_yourself: single question starting with "Can you..." or "What would happen if..."

Respond in JSON:
{
  "examples": [
    {"component": "name", "example": "2-3 sentence scenario", "check_yourself": "question"}
  ]
}""",
            # Short explainer
            """Write a short explainer (6-10 sentences) for '{{topic}}' using components, analogies, and examples.
Audience: {{audience}}
Tone: {{tone}}
Additional context: {{additional_context}}

Weave in:
- Why the concept exists
- How the pieces interact
- A common pitfall to avoid

Respond in JSON:
{
  "explainer": "paragraphs",
  "pitfalls": ["pitfall 1", "pitfall 2"],
  "next_steps": ["what to read/try next"]
}"""
        ],
        return_usage=True,
    )

    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    output_dir = os.path.join(project_root, "output", "learning", "concept_simplifier")
    os.makedirs(output_dir, exist_ok=True)

    output_path = os.path.join(output_dir, f"{timestamp}-{topic[:50].replace(' ', '_')}.json")
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2)

    log_file = MinimalChainable.log_to_markdown("concept_simplifier", context_filled_prompts, result, usage_stats)

    print(f"✅ Saved JSON to: {output_path}")
    print(f"✅ Log saved to: {log_file}")


def main():
    topic, context = get_input_from_args(
        description="Break complex topics into digestible parts with analogies and a short explainer"
    )
    concept_simplifier(topic, context)


if __name__ == "__main__":
    main()
