#!/usr/bin/env python3
"""
🌾 Astroturf Detector (adult mode)

Assess whether a campaign/text shows signs of astroturfing: origin, coordination, tells, and confidence.

Usage:
    python tools/media/astroturf_detector.py "Thread/post text"
    cat thread.txt | python tools/media/astroturf_detector.py
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


def astroturf_detector(text: str):
    print("🌾 Astroturf Detector")
    print(f"Input preview: {text[:160]}{'...' if len(text) > 160 else ''}\n")

    user_profile = load_user_context(project_root)
    tone = user_profile.get("writing_style", {}).get("tone", "Skeptical and precise")

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
            # Signals and coordination
            """Identify signals of astroturfing/coordination in the text.
Tone: {{tone}}

Text:
{{text}}

Provide top 5 signals max; include snippet evidence.

Respond in JSON:
{
  "signals": [
    {"pattern": "tell", "evidence": "snippet"}
  ],
  "claimed_origin": "stated origin if any"
}""",
            # Likely origin and motives
            """Hypothesize likely originators, funding sources, and motives based on patterns.
Keep lists to top 3; include confidence (Low/Med/High).

Signals: {{output[-1].signals}}

Respond in JSON:
{
  "likely_origin": ["actor1", "actor2"],
  "motives": ["motive1", "motive2"],
  "confidence": "Low/Med/High"
}""",
            # Confidence and alternatives
            """Provide confidence and alternative explanations to avoid false positives.

Origins: {{output[-1].likely_origin}}

Respond in JSON:
{
  "confidence": "Low/Med/High",
  "alternative_explanations": ["alt1", "alt2"]
}""",
            # Concise verdict
            """Give a concise verdict and what to watch for next.
Limit verdict to 2 sentences; provide 2-3 watch-next signals.

Respond in JSON:
{
  "verdict": "short verdict",
  "watch_next": ["signal1", "signal2"]
}"""
        ],
        return_usage=True,
    )

    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    output_dir = os.path.join(project_root, "output", "media", "astroturf_detector")
    os.makedirs(output_dir, exist_ok=True)

    output_path = os.path.join(output_dir, f"{timestamp}-astroturf.json")
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2)

    log_file = MinimalChainable.log_to_markdown("astroturf_detector", context_filled_prompts, result, usage_stats)

    print(f"✅ Saved JSON to: {output_path}")
    print(f"✅ Log saved to: {log_file}")


def main():
    text, _ = get_input_from_args(
        description="Detect astroturf/coordination signals in a campaign or post",
        default_context_help="(unused)"
    )
    astroturf_detector(text)


if __name__ == "__main__":
    main()
