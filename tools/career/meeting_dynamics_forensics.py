#!/usr/bin/env python3
"""
🔎 Meeting Dynamics Forensics (adult mode)

Analyze transcripts for interruptions, deference, and real power hierarchy.

Usage:
    python tools/career/meeting_dynamics_forensics.py "Transcript text"
    cat meeting.txt | python tools/career/meeting_dynamics_forensics.py
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


def meeting_dynamics_forensics(transcript: str):
    print("🔎 Meeting Dynamics Forensics")
    print(f"Transcript preview: {transcript[:160]}{'...' if len(transcript) > 160 else ''}\n")

    user_profile = load_user_context(project_root)
    tone = user_profile.get("writing_style", {}).get("tone", "Direct and analytical")

    client, model_names = build_models()
    model_info = (client, model_names[0])

    context_data = {
        "transcript": transcript,
        "tone": tone,
    }

    result, context_filled_prompts, usage_stats = MinimalChainable.run(
        context=context_data,
        model=model_info,
        callable=prompt,
        prompts=[
            # Interruption patterns
            """You are a conversation analyst. Map interruption patterns and dominance signals in the meeting.
Tone: {{tone}}

Transcript:
{{transcript}}

Limit interruptions list to the top 5; include a severity or frequency note.

Respond in JSON:
{
  "interruptions": [{"interrupter": "Name", "victim": "Name"}],
  "dominance_score": {"Name": 10, "Name": 5}
}""",
            # Deference markers
            """Identify deference and submission markers (hedging, permission-seeking, orders as questions).
Provide 3-5 strongest examples. Include the exact phrase snippet.

Transcript: {{transcript}}

Respond in JSON:
{
  "deference_markers": [
    {"speaker": "Name", "phrase": "text", "analysis": "short (why it signals deference)"}
  ]
}""",
            # Real org chart
            """Infer the real power structure in the room and who holds veto power.
Keep hierarchy to top 5 only. Note one red flag and one leverage move.

Interruptions: {{output[-2].interruptions}}
Deference: {{output[-1].deference_markers}}

Respond in JSON:
{
  "real_hierarchy": ["1. Name", "2. Name"],
  "power_dynamic": "description",
  "red_flags": ["flag1", "flag2"],
  "leverage_moves": ["move1"]
}"""
        ],
        return_usage=True,
    )

    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    output_dir = os.path.join(project_root, "output", "career", "meeting_dynamics_forensics")
    os.makedirs(output_dir, exist_ok=True)

    output_path = os.path.join(output_dir, f"{timestamp}-meeting_forensics.json")
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2)

    log_file = MinimalChainable.log_to_markdown("meeting_dynamics_forensics", context_filled_prompts, result, usage_stats)

    print(f"✅ Saved JSON to: {output_path}")
    print(f"✅ Log saved to: {log_file}")


def main():
    transcript, _ = get_input_from_args(
        description="Analyze meeting dynamics for interruptions, deference, and real hierarchy",
        default_context_help="(unused)"
    )
    meeting_dynamics_forensics(transcript)


if __name__ == "__main__":
    main()
