#!/usr/bin/env python3
"""
🎭 Corporate Theater Director (adult mode)

Decode performative corporate rituals, scripts, and incentives; propose honest alternatives.

Usage:
    python tools/culture/corporate_theater_director.py "Describe the ritual/town hall/email"
    cat memo.txt | python tools/culture/corporate_theater_director.py
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


def corporate_theater_director(text: str):
    print("🎭 Corporate Theater Director")
    print(f"Ritual preview: {text[:200]}{'...' if len(text) > 200 else ''}\n")

    user_profile = load_user_context(project_root)
    tone = user_profile.get("writing_style", {}).get("tone", "Wry but constructive")

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
            # Decode the theater
            """You are an Organizational Anthropologist and Semiotics Expert. Decode the "Corporate Theater" to reveal the hidden signals.

Analyze the text for "Performative Utterances"—statements that do nothing but signal virtue or compliance.
Tone: {{tone}}

Text:
{{text}}

Perspective Framework:
- Signaling Theory: Costly signals (real) vs. Cheap talk (fake).
- Mimetic Desire: Are they copying a competitor or trend?

Constraints:
- Identify exactly 3-5 performative moves.
- "Signal": What virtue is being signaled? (e.g., "We are innovative").
- "Audience": Who is this really for? (e.g., "Investors", "Regulators", "Employees").

Respond in JSON:
{
  "performative_moves": [
    {"move": "Quote snippet", "signal": "The hidden message", "audience": "Target audience"}
  ],
  "audience_reaction": "The cynical internal monologue of the average employee (max 2 sentences)."
}""",
            # Incentives and reality
            """You are a Game Theorist mapping the "Principal-Agent Problem". Why is this theater necessary?

What "Inconvenient Truth" is being obscured by the performance?
Moves: {{output[-1].performative_moves}}

Constraints:
- List exactly 3 incentives driving the behavior.
- "Obscured Reality": The brutal truth they cannot say out loud (max 1 sentence).

Respond in JSON:
{
  "incentives": ["Incentive 1 (e.g., 'Stock price stability')", "Incentive 2"],
  "obscured_reality": "The unvarnished truth."
}""",
            # Honest alternative
            """You are a Radical Candor Communications Coach. Rewrite the message to build trust through vulnerability.

The goal is "Psychological Safety"—admitting the hard truth so people can actually work on it.

Constraints:
- Maximum 4 sentences.
- Must include one "Vulnerable Admission" (e.g., "We messed up").
- Must be actionable.

Respond in JSON:
{
  "honest_script": "The rewritten, honest version.",
  "likely_effect": "Why this would increase trust (max 1 sentence)."
}"""
        ],
        return_usage=True,
    )

    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    output_dir = os.path.join(project_root, "output", "culture", "corporate_theater_director")
    os.makedirs(output_dir, exist_ok=True)

    output_path = os.path.join(output_dir, f"{timestamp}-corporate_theater.json")
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2)

    log_file = MinimalChainable.log_to_markdown("corporate_theater_director", context_filled_prompts, result, usage_stats)

    print(f"✅ Saved JSON to: {output_path}")
    print(f"✅ Log saved to: {log_file}")


def main():
    text, _ = get_input_from_args(
        description="Decode corporate theater and draft an honest alternative",
        default_context_help="(unused)"
    )
    corporate_theater_director(text)


if __name__ == "__main__":
    main()
