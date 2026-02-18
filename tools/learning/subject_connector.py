#!/usr/bin/env python3
"""
🔗 Subject Connector (adult mode)

Find surprising links between two subjects, why they matter, and propose a project that uses both.

Usage:
    python tools/learning/subject_connector.py "Subject A" --context "Subject B"
    echo "History" | python tools/learning/subject_connector.py --context "Mathematics"
"""

import os
from typing import Optional

try:
    from tools.tool_utils import setup_project_root, load_user_context, get_input_from_args, save_chain_output
except ImportError:
    import sys
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
    from tools.tool_utils import setup_project_root, load_user_context, get_input_from_args, save_chain_output

project_root = setup_project_root(__file__)

from lib.core.chain import MinimalChainable
from lib.core.artifact_store import ArtifactStore
from lib.core.llm_client import build_models, prompt


def subject_connector(subject_a: str, subject_b: str, artifact_store: Optional[ArtifactStore] = None):
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

    artifact_store = artifact_store or ArtifactStore()

    result, context_filled_prompts, usage_stats, execution_trace = MinimalChainable.run(
        context=context_data,
        model=model_info,
        llm_callable=prompt,
        return_trace=True,
        artifact_store=artifact_store,
        topic=f"{subject_a}_vs_{subject_b}",

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
        )

    output_dir = os.path.join(project_root, "output", "learning", "subject_connector")
    save_chain_output(project_root, output_dir, "subject_connector", f"{subject_a}_vs_{subject_b}", execution_trace, result, context_filled_prompts, usage_stats, artifact_store)


def main():
    subject_a, subject_b = get_input_from_args(
        description="Connect two subjects with surprising links and a project idea",
        default_context_help="Second subject"
    )
    subject_connector(subject_a, subject_b)


if __name__ == "__main__":
    main()
