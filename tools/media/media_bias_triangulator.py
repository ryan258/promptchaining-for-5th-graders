#!/usr/bin/env python3
"""
🧭 Media Bias Triangulator (adult mode)

Generate polarized framings, surface omissions, and synthesize ground truth.

Usage:
    python tools/media/media_bias_triangulator.py "Event description"
    cat event.txt | python tools/media/media_bias_triangulator.py
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


def media_bias_triangulator(event: str):
    print("🧭 Media Bias Triangulator")
    print(f"Event: {event[:160]}{'...' if len(event) > 160 else ''}\n")

    user_profile = load_user_context(project_root)
    tone = user_profile.get("writing_style", {}).get("tone", "Neutral and skeptical")

    client, model_names = build_models()
    model_info = (client, model_names[0])

    context_data = {
        "event": event,
        "tone": tone,
    }

    result, context_filled_prompts, usage_stats = MinimalChainable.run(
        context=context_data,
        model=model_info,
        callable=prompt,
        prompts=[
            # Biased framings
            """You are a Media Bias Researcher and Political Scientist. Simulate how different "Echo Chambers" will frame this event.

Tone: {{tone}}

Event:
{{event}}

Perspective Framework:
- Progressive Lens: Focus on systemic inequality, corporate power, and social justice.
- Conservative Lens: Focus on tradition, individual responsibility, and national security.
- Centrist/Establishment Lens: Focus on stability, institutions, and bipartisan compromise.

Constraints:
- Generate exactly 3 headlines.
- Length: Max 12 words per headline.
- Style: Mimic the specific vocabulary of each tribe (e.g., "Woke mob" vs "Systemic racism").

Respond in JSON:
{
  "headline_left": "Headline from a Progressive outlet",
  "headline_right": "Headline from a Conservative outlet",
  "headline_center": "Headline from a Mainstream/Corporate outlet"
}""",
            # Omissions per framing
            """Analyze the "Blind Spots". What does each lens *refuse* to see?

Headlines: {{output[-1]}}

Constraints:
- Identify exactly 1 major omission per lens.
- "Omission": A specific fact or context that undermines their narrative.
- Max 1 sentence per omission.

Respond in JSON:
{
  "omission_left": "What the Left ignores",
  "omission_right": "What the Right ignores",
  "omission_center": "What the Center ignores"
}""",
            # Ground truth synthesis
            """You are an Epistemologist and Neutral Arbiter. Triangulate the "Ground Truth" from the noise.

Synthesize the facts that all sides agree on, and clearly state what is disputed.
Event: {{event}}
Headlines: {{output[-2]}}
Omissions: {{output[-1]}}

Constraints:
- Ground Truth: Max 5 sentences. Must be purely factual.
- Bias Rating: Low, Medium, High (for the overall media ecosystem's handling of this).
- Unknowns: Exactly 2 key facts that are currently unknowable.

Respond in JSON:
{
  "ground_truth": "The synthesized factual summary.",
  "bias_rating": "High",
  "unknowns": ["Unknown 1", "Unknown 2"]
}"""
        ],
        return_usage=True,
    )

    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    output_dir = os.path.join(project_root, "output", "media", "media_bias_triangulator")
    os.makedirs(output_dir, exist_ok=True)

    output_path = os.path.join(output_dir, f"{timestamp}-media_bias.json")
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2)

    log_file = MinimalChainable.log_to_markdown("media_bias_triangulator", context_filled_prompts, result, usage_stats)

    print(f"✅ Saved JSON to: {output_path}")
    print(f"✅ Log saved to: {log_file}")


def main():
    event, _ = get_input_from_args(
        description="Triangulate media bias and synthesize ground truth for an event",
        default_context_help="(unused)"
    )
    media_bias_triangulator(event)


if __name__ == "__main__":
    main()
