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
            """Extract the main competing narratives, target audiences, and objectives.
Tone: {{tone}}

Text:
{{narratives}}

Respond in JSON:
{
  "narratives": [
    {"label": "A", "message": "summary", "target": "who", "objective": "goal"}
  ]
}""",
            # Escalation and techniques
            """Identify escalation moves and techniques used (fear, appeal to authority, doubt seeding, etc).

Respond in JSON:
{
  "techniques": [
    {"narrative": "A", "technique": "type", "example": "snippet"}
  ],
  "escalation_risks": ["risk1", "risk2"]
}""",
            # Counters
            """Offer counter-messaging ideas or inoculation prompts to reduce the impact of the narratives.

Respond in JSON:
{
  "counter_moves": [
    {"narrative": "A", "counter": "idea"}
  ],
  "inoculation_prompts": ["prompt1", "prompt2"]
}""",
            # Monitoring
            """Suggest monitoring signals to track narrative shifts over time.

Respond in JSON:
{
  "monitoring_signals": ["signal1", "signal2"]
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
