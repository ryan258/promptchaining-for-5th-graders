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
            """You are a Media Critic and Propaganda Analyst. Deconstruct the "Manufacturing of Consent" (Chomsky).

Identify "Framing Devices" and "Thought-Terminating Clichés".
Tone: {{tone}}

Text:
{{text}}

Perspective Framework:
- Agenda Setting: What are they forcing us to think *about*?
- Priming: How are they pre-loading our emotional response?

Constraints:
- Identify exactly 3 frames.
- "Repetition": List exactly 3 phrases repeated for effect.
- "Emotional Hooks": List exactly 3 specific emotions targeted (e.g., "Fear of missing out").

Respond in JSON:
{
  "frames": ["Frame 1 (e.g., 'The War on Terror')", "Frame 2"],
  "repetition": ["Phrase 1", "Phrase 2"],
  "emotional_hooks": ["Hook 1", "Hook 2"]
}""",
            # Omissions and skew
            """Analyze the "Negative Space"—what is deliberately left out?

Focus on "Selective Omission" and "Context Collapse".
Frames: {{output[-1].frames}}

Constraints:
- Identify exactly 3 key omissions.
- "Skew": One sentence summary of the bias direction.
- "Missing Evidence": What specific data point would disprove this?

Respond in JSON:
{
  "omissions": ["Omission 1 (e.g., 'Civilian casualty counts')", "Omission 2"],
  "skew": "The narrative skews heavily towards...",
  "missing_evidence": "Data point X is absent."
}""",
            # Beneficiaries and risks
            """Follow the Money/Power. Who benefits from this specific consensus?

Constraints:
- Beneficiaries: Exactly 3 actors (e.g., "Defense Contractors").
- Disadvantaged: Exactly 3 actors (e.g., "Privacy Advocates").

Respond in JSON:
{
  "beneficiaries": ["Actor 1", "Actor 2", "Actor 3"],
  "disadvantaged": ["Actor 1", "Actor 2", "Actor 3"]
}""",
            # Counter-framing
            """You are a Debate Coach. Construct "Subversive Questions" to break the frame.

How do we shift the "Overton Window"?
Constraints:
- Counter-frames: Exactly 3 alternative ways to view this.
- Fact Checks: Exactly 3 specific claims to verify.

Respond in JSON:
{
  "counter_frames": ["Question 1 (e.g., 'Why are we framing this as a security issue instead of a health issue?')", "Question 2"],
  "fact_checks": ["Claim 1", "Claim 2", "Claim 3"]
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
