#!/usr/bin/env python3
"""
🧠 Consensus Manufacturing Detective (adult mode)

Analyze messaging to see how consensus is being manufactured: framing, repetition, omission, and beneficiaries.

Usage:
    python tools/media/consensus_manufacturing_detective.py "Message/campaign text"
    cat campaign.txt | python tools/media/consensus_manufacturing_detective.py
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


def consensus_manufacturing_detective(text: str):
    print("🧠 Consensus Manufacturing Detective")
    print(f"Input preview: {text[:160]}{'...' if len(text) > 160 else ''}\n")

    user_profile = load_user_context(project_root)
    tone = user_profile.get("writing_style", {}).get("tone", "Critical but precise")

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
            # Framing and repetition
            """Identify framing devices, repeated slogans, and emotional levers used to manufacture consensus.
Tone: {{tone}}

Text:
{{text}}

Respond in JSON:
{
  "frames": ["frame1", "frame2"],
  "repetition": ["phrase1", "phrase2"],
  "emotional_hooks": ["hook1", "hook2"]
}""",
            # Omissions and skew
            """Surface key omissions or asymmetries (who/what is minimized or excluded).

Frames: {{output[-1].frames}}

Respond in JSON:
{
  "omissions": ["omission1", "omission2"],
  "skew": "short description"
}""",
            # Beneficiaries and risks
            """Who benefits from this framing, and who is disadvantaged?

Respond in JSON:
{
  "beneficiaries": ["actor1", "actor2"],
  "disadvantaged": ["actor1", "actor2"]
}""",
            # Counter-framing
            """Offer counter-frames or questions to test the narrative.

Respond in JSON:
{
  "counter_frames": ["question1", "question2"],
  "fact_checks": ["claim to verify"]
}"""
        ],
        return_usage=True,
    )

    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    output_dir = os.path.join(project_root, "output", "media", "consensus_manufacturing_detective")
    os.makedirs(output_dir, exist_ok=True)

    output_path = os.path.join(output_dir, f"{timestamp}-consensus_detective.json")
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2)

    log_file = MinimalChainable.log_to_markdown("consensus_manufacturing_detective", context_filled_prompts, result, usage_stats)

    print(f"✅ Saved JSON to: {output_path}")
    print(f"✅ Log saved to: {log_file}")


def main():
    text, _ = get_input_from_args(
        description="Detect consensus manufacturing techniques in messaging",
        default_context_help="(unused)"
    )
    consensus_manufacturing_detective(text)


if __name__ == "__main__":
    main()
