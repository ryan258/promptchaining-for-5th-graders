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
            """You are a Disinformation Analyst and Forensic Linguist. Detect "Inauthentic Coordinated Behavior" (Astroturfing).

Look for "Scripted Language", "Temporal Anomalies", and "Persona Inconsistencies".
Tone: {{tone}}

Text:
{{text}}

Perspective Framework:
- Linguistic Fingerprinting: Are different accounts using the same unique phrases?
- Sentiment Analysis: Is the outrage/praise disproportionate to the event?

Constraints:
- Identify exactly 5 specific signals.
- "Pattern": Name the technique (e.g., "Copypasta", "Strawman Army").
- "Evidence": Quote the exact text snippet.

Respond in JSON:
{
  "signals": [
    {"pattern": "Pattern Name", "evidence": "Quote from text"}
  ],
  "claimed_origin": "Who they claim to be (e.g., 'Concerned Parents')"
}""",
            # Likely origin and motives
            """Hypothesize the "Dark Money" or "State Actor" behind this. Who benefits?

Signals: {{output[-1].signals}}

Constraints:
- List exactly 3 likely origins.
- "Confidence": Low, Medium, High.
- "Motives": Cui Bono? (Who benefits?).

Respond in JSON:
{
  "likely_origin": ["Actor 1 (e.g., 'Competitor X')", "Actor 2"],
  "motives": ["Motive 1", "Motive 2"],
  "confidence": "High"
}""",
            # Confidence and alternatives
            """You are a Skeptical Peer Reviewer. Play "Devil's Advocate".

Could this be organic viral behavior?
Origins: {{output[-1].likely_origin}}

Constraints:
- Confidence: Re-evaluate based on alternative explanations.
- Alternatives: Exactly 2 innocent explanations.

Respond in JSON:
{
  "confidence": "Medium",
  "alternative_explanations": ["Alternative 1 (e.g., 'Genuine viral outrage')", "Alternative 2"]
}""",
            # Concise verdict
            """Issue a final "Forensic Verdict". Is this Astroturf or Grassroots?

Limit verdict to 2 sentences.
Constraints:
- Verdict: Definitive statement.
- Watch Next: Exactly 3 specific things to monitor to confirm.

Respond in JSON:
{
  "verdict": "This is likely a coordinated campaign by...",
  "watch_next": ["Signal 1", "Signal 2", "Signal 3"]
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
