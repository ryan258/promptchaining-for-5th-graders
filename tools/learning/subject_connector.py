#!/usr/bin/env python3
"""
🔗 Subject Connector (adult mode)

Find surprising links between two subjects, why they matter, and propose a project that uses both.

Usage:
    python tools/learning/subject_connector.py "Subject A" --context "Subject B"
    echo "History" | python tools/learning/subject_connector.py --context "Mathematics"
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


def subject_connector(subject_a: str, subject_b: str):
    print("🔗 Subject Connector")
    print(f"Subject A: {subject_a}")
    print(f"Subject B: {subject_b}\n")

    user_profile = load_user_context(project_root)
    tone = user_profile.get("writing_style", {}).get("tone", "Clear and practical")

    client, model_names = build_models()
    model_info = (client, model_names[0])

    context_data = {
        "subject_A": subject_a,
        "subject_B": subject_b,
        "tone": tone,
    }

    result, context_filled_prompts, usage_stats = MinimalChainable.run(
        context=context_data,
        model=model_info,
        callable=prompt,
        prompts=[
            # Connections
            """You are a Polymath and Innovation Consultant. Find "Structural Isomorphisms" (shared underlying patterns) between {{subject_A}} and {{subject_B}}.

Avoid surface-level links. Look for deep structural similarities.
Tone: {{tone}}

Perspective Framework:
- Systems Theory: Do they share feedback loops or emergent properties?
- Evolution: Do they share selection pressures?

Constraints:
- List exactly 3 non-obvious connections.
- "Connection": Must describe the shared mechanism (max 15 words).

Respond in JSON:
{
  "connections": ["Connection 1 (e.g., 'Both use distributed consensus')", "Connection 2", "Connection 3"]
}""",
            # Why they matter
            """Explain the "Cross-Pollination Value". Why does knowing A help you understand B?

Connections: {{output[-1].connections}}

Constraints:
- Explain exactly 3 connections.
- "Importance": How does this insight solve a problem in the other field? (Max 1 sentence).

Respond in JSON:
{
  "explanations": [
    {"connection": "Ref to connection", "importance": "Insight value"}
  ]
}""",
            # Project idea
            """Design a "Synthesis Project" that proves mastery of both domains.

The project must be concrete and buildable.
Explanations: {{output[-1].explanations}}

Constraints:
- Title: Max 10 words.
- Description: Exactly 3 sentences.
- Outputs: Exactly 3 tangible artifacts (e.g., "Codebase", "Whitepaper", "Model").

Respond in JSON:
{
  "project_title": "Title",
  "project_description": "Description",
  "expected_outputs": ["Output 1", "Output 2", "Output 3"]
}"""
        ],
        return_usage=True,
    )

    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    output_dir = os.path.join(project_root, "output", "learning", "subject_connector")
    os.makedirs(output_dir, exist_ok=True)

    output_path = os.path.join(output_dir, f"{timestamp}-subject_connector.json")
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2)

    log_file = MinimalChainable.log_to_markdown("subject_connector", context_filled_prompts, result, usage_stats)

    print(f"✅ Saved JSON to: {output_path}")
    print(f"✅ Log saved to: {log_file}")


def main():
    subject_a, subject_b = get_input_from_args(
        description="Connect two subjects with surprising links and a project idea",
        default_context_help="Second subject"
    )
    subject_connector(subject_a, subject_b)


if __name__ == "__main__":
    main()
