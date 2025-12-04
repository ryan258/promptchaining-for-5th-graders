#!/usr/bin/env python3
"""
🏛️ Regulatory Capture Mapper (adult mode)

Map agencies/industries for capture risk: revolving doors, incentives, signals, and mitigation ideas.

Usage:
    python tools/policy/regulatory_capture_mapper.py "Agency/industry description"
    cat sector.txt | python tools/policy/regulatory_capture_mapper.py
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


def regulatory_capture_mapper(text: str):
    print("🏛️ Regulatory Capture Mapper")
    print(f"Target preview: {text[:200]}{'...' if len(text) > 200 else ''}\n")

    user_profile = load_user_context(project_root)
    tone = user_profile.get("writing_style", {}).get("tone", "Skeptical and direct")

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
            # Capture signals
            """You are an Antitrust Lawyer and Institutional Economist. Detect "Regulatory Capture" and "Rent-Seeking".

Identify mechanisms where the regulator serves the industry it regulates.
Tone: {{tone}}

Target:
{{text}}

Perspective Framework:
- Revolving Door: Are regulators future employees of the industry?
- Information Asymmetry: Does the regulator rely on industry data?

Constraints:
- Identify exactly 5 capture signals.
- "Signal": Name the mechanism (e.g., "Cultural Capture").
- "Evidence": Quote the snippet.

Respond in JSON:
{
  "capture_signals": [
    {"signal": "Signal Name", "evidence": "Quote snippet"}
  ]
}""",
            # Incentives and beneficiaries
            """Map the "Incentive Structure". Why is capture rational for these actors?

Signals: {{output[-1].capture_signals}}

Constraints:
- Beneficiaries: Exactly 3 actors.
- Incentives: Exactly 3 reasons (e.g., "Job security").

Respond in JSON:
{
  "beneficiaries": ["Actor 1", "Actor 2", "Actor 3"],
  "incentives": ["Incentive 1", "Incentive 2", "Incentive 3"]
}""",
            # Mitigations
            """You are a Governance Designer. Propose "Structural Reforms" to break the capture.

Constraints:
- Mitigations: Exactly 3 structural changes (e.g., "Cooling-off periods").
- Monitoring: Exactly 3 metrics to watch.

Respond in JSON:
{
  "mitigations": ["Reform 1 (e.g., 'Ban on stock trading')", "Reform 2"],
  "monitoring": ["Metric 1 (e.g., 'Waiver approval rate')", "Metric 2"]
}"""
        ],
        return_usage=True,
    )

    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    output_dir = os.path.join(project_root, "output", "policy", "regulatory_capture_mapper")
    os.makedirs(output_dir, exist_ok=True)

    output_path = os.path.join(output_dir, f"{timestamp}-regulatory_capture.json")
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2)

    log_file = MinimalChainable.log_to_markdown("regulatory_capture_mapper", context_filled_prompts, result, usage_stats)

    print(f"✅ Saved JSON to: {output_path}")
    print(f"✅ Log saved to: {log_file}")


def main():
    text, _ = get_input_from_args(
        description="Map regulatory capture signals and mitigations for an agency/industry",
        default_context_help="(unused)"
    )
    regulatory_capture_mapper(text)


if __name__ == "__main__":
    main()
