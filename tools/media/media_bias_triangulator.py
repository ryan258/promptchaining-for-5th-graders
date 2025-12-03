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
            """Generate headlines for the event from multiple bias lenses.
Tone: {{tone}}

Event:
{{event}}

Respond in JSON:
{
  "headline_left": "text",
  "headline_right": "text",
  "headline_center": "text"
}""",
            # Omissions per framing
            """For each headline, note the likely omissions or minimized facts.

Headlines: {{output[-1]}}

Respond in JSON:
{
  "omission_left": "text",
  "omission_right": "text",
  "omission_center": "text"
}""",
            # Ground truth synthesis
            """Synthesize a ground-truth summary including material facts and uncertainty.
Avoid emotional framing; include what is unknown or contested.

Event: {{event}}
Headlines: {{output[-2]}}
Omissions: {{output[-1]}}

Respond in JSON:
{
  "ground_truth": "text",
  "bias_rating": "High/Med/Low",
  "unknowns": ["unknown 1", "unknown 2"]
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
