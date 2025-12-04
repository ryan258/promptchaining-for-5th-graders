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
            """You are a Sociolinguist and Power Dynamics Expert. Map the "Conversational Floor" to reveal who actually dominates the room.

Analyze "Cooperative Overlaps" (enthusiastic agreement) vs. "Competitive Interruptions" (stealing the floor).
Tone: {{tone}}

Transcript:
{{transcript}}

Perspective Framework:
- Manterrupting/Bropropriating: Is credit being stolen in real-time?
- Filibustering: Who talks to prevent others from speaking?

Constraints:
- List exactly the top 5 interruption events.
- "Severity": Low (accidental), Medium (habitual), High (hostile).
- Max 15 words per event.

Respond in JSON:
{
  "interruptions": [
    {"interrupter": "Name", "victim": "Name", "type": "Competitive/Cooperative", "severity": "High"}
  ],
  "dominance_score": {"Name": 10 (Dominant), "Name": 1 (Silent)}
}""",
            # Deference markers
            """You are a Behavioral Psychologist specializing in Status Signals. Identify "Low Status" language markers.

Look for:
- Hedging: "I might be wrong, but..."
- Tag Questions: "It's a good plan, right?"
- Permission Seeking: "Is it okay if I..."

Transcript: {{transcript}}

Constraints:
- Identify exactly 3-5 deference markers.
- "Analysis": Explain *why* this signals submission in 1 sentence.

Respond in JSON:
{
  "deference_markers": [
    {"speaker": "Name", "phrase": "Exact quote snippet", "analysis": "Explanation of status signal"}
  ]
}""",
            # Real org chart
            """You are a Corporate Anthropologist. Infer the "Shadow Hierarchy" based on the behavioral data.

Who holds the "Veto Power"? Who do people look at when they finish speaking?
Distinguish between "Positional Authority" (Job Title) and "Relational Authority" (Influence).

Interruptions: {{output[-2].interruptions}}
Deference: {{output[-1].deference_markers}}

Constraints:
- Hierarchy: Top 5 influential people only.
- Red Flags: Specific toxic dynamics (e.g., "HiPPO decision making").
- Leverage Moves: How to gain influence in this specific group.

Respond in JSON:
{
  "real_hierarchy": ["1. Name (The real boss)", "2. Name (The influencer)", "3. Name"],
  "power_dynamic": "One sentence summary of the room's political structure.",
  "red_flags": ["Specific red flag 1", "Specific red flag 2"],
  "leverage_moves": ["Specific tactical move 1"]
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
