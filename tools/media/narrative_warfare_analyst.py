#!/usr/bin/env python3
"""
🛡️ Narrative Warfare Analyst (adult mode)

Analyze competing narratives, their objectives, escalation moves, and counters.

Usage:
    python tools/media/narrative_warfare_analyst.py "Narrative summary or quotes"
    cat narratives.txt | python tools/media/narrative_warfare_analyst.py
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


def narrative_warfare_analyst(narratives: str):
    print("🛡️ Narrative Warfare Analyst")
    print(f"Narratives preview: {narratives[:160]}{'...' if len(narratives) > 160 else ''}\n")

    user_profile = load_user_context(project_root)
    tone = user_profile.get("writing_style", {}).get("tone", "Analytical and succinct")

    client, model_names = build_models()
    model_info = (client, model_names[0])

    context_data = {
        "narratives": narratives,
        "tone": tone,
    }

    result, context_filled_prompts, usage_stats = MinimalChainable.run(
        context=context_data,
        model=model_info,
        callable=prompt,
        prompts=[
            # Map competing narratives
            """You are an Information Warfare Specialist and PsyOps Analyst. Map the "Battle of Narratives".

Identify the "Strategic Narratives" deployed by each side.
Tone: {{tone}}

Text:
{{narratives}}

Perspective Framework:
- Hero/Villain/Victim: Who plays what role in each story?
- Casus Belli: What is the justification for conflict?

Constraints:
- Identify exactly 3 competing narratives.
- "Target Audience": Be specific (e.g., "Disaffected youth").
- "Objective": What action do they want the target to take? (Max 10 words).

Respond in JSON:
{
  "narratives": [
    {"label": "Narrative A (e.g., 'Freedom Fighter')", "message": "Core message summary", "target": "Target demographic", "objective": "Specific goal"}
  ]
}""",
            # Escalation and techniques
            """Analyze the "Escalation Ladder". How are they raising the stakes?

Identify "Cognitive Hacks" (e.g., Fearmongering, Gaslighting).
Constraints:
- Identify exactly 3 specific techniques.
- "Technique": Name the PsyOp tactic.
- "Example": Quote the snippet.

Respond in JSON:
{
  "techniques": [
    {"narrative": "Ref to Narrative A", "technique": "Technique Name", "example": "Quote snippet"}
  ],
  "escalation_risks": ["Risk 1 (e.g., 'Violence in the streets')", "Risk 2"]
}""",
            # Counters
            """You are a Counter-Narrative Strategist. How do we "Inoculate" the audience?

Propose "Pre-bunking" or "Reframing" strategies.
Constraints:
- Counter-moves: Exactly 3 specific counters.
- Inoculation: Exactly 2 questions to plant doubt.

Respond in JSON:
{
  "counter_moves": [
    {"narrative": "Ref to Narrative A", "counter": "Specific counter-message"}
  ],
  "inoculation_prompts": ["Question 1 (e.g., 'Who benefits if you believe this?')", "Question 2"]
}""",
            # Monitoring
            """Establish "Early Warning Indicators". What signals a shift in the information war?

Constraints:
- Identify exactly 3 specific signals to watch.
- Must be observable (e.g., "Hashtag volume spikes").

Respond in JSON:
{
  "monitoring_signals": ["Signal 1", "Signal 2", "Signal 3"]
}"""
        ],
        return_usage=True,
    )

    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    output_dir = os.path.join(project_root, "output", "media", "narrative_warfare_analyst")
    os.makedirs(output_dir, exist_ok=True)

    output_path = os.path.join(output_dir, f"{timestamp}-narrative_warfare.json")
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2)

    log_file = MinimalChainable.log_to_markdown("narrative_warfare_analyst", context_filled_prompts, result, usage_stats)

    print(f"✅ Saved JSON to: {output_path}")
    print(f"✅ Log saved to: {log_file}")


def main():
    text, _ = get_input_from_args(
        description="Analyze competing narratives, techniques, and counters",
        default_context_help="(unused)"
    )
    narrative_warfare_analyst(text)


if __name__ == "__main__":
    main()
