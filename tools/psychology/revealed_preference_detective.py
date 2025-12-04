#!/usr/bin/env python3
"""
🕵️ Revealed Preference Detective (adult mode)

Contrast stated preferences with revealed behavior to infer real values and likely choices.

Usage:
    python tools/psychology/revealed_preference_detective.py "Stated pref" --context "Revealed behavior"
    echo "Stated" | python tools/psychology/revealed_preference_detective.py --context "Behavior"
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


def revealed_preference_detective(stated: str, revealed: str):
    print("🕵️ Revealed Preference Detective")
    print(f"Stated: {stated}")
    print(f"Revealed: {revealed}\n")

    user_profile = load_user_context(project_root)
    tone = user_profile.get("writing_style", {}).get("tone", "Blunt but fair")

    client, model_names = build_models()
    model_info = (client, model_names[0])

    context_data = {
        "stated": stated,
        "revealed": revealed,
        "tone": tone,
    }

    result, context_filled_prompts, usage_stats = MinimalChainable.run(
        context=context_data,
        model=model_info,
        callable=prompt,
        prompts=[
            # Contradiction
            """You are a behavioral economist with 15+ years analyzing preference revelation patterns, specializing in identifying gaps between stated values and actual resource allocation (time, money, attention).

Analyze this preference-behavior mismatch:

**Stated Preference:** {{stated}}
**Revealed Behavior:** {{revealed}}

Use the preference revelation framework:

**Actions speak louder than words** - Where do they actually spend:
- Time (hours per week, repeated patterns)
- Money (budget allocation, recurring purchases)
- Attention (what they track, measure, optimize)
- Social capital (who they associate with, what they signal)

**Opportunity cost reveals priority** - What did they give up to do this?

**Example contradiction for "I value work-life balance":**
✅ GOOD: "Claims to value work-life balance but checks email at 11pm daily (revealed behavior from phone logs), schedules 7am calls (calendar data), and canceled 3 family dinners this month for client meetings (stated by partner). Actual priority: client satisfaction > family time > rest."
❌ BAD: "Says one thing but does another with work-life balance" (no specific evidence, no measurement, no opportunity cost)

Tone: {{tone}}

Respond in JSON:
{
  "contradiction": "Specific description with concrete evidence from behavior (max 50 words). Include measurements, frequencies, or counts where possible.",
  "severity": "High (directly opposed) / Med (competing priorities) / Low (context-dependent)",
  "opportunity_cost": "What they sacrificed to reveal this preference (max 20 words)"
}

Be ruthlessly specific. Cite actual behaviors, not generalizations.""",
            # Value hierarchy
            """You are an organizational psychologist expert in value systems and behavioral pattern analysis.

Based on the contradiction detected, reconstruct the person's TRUE value hierarchy (what they actually optimize for, not what they claim).

**Framework for inferring values:**

1. **Resource allocation** - Where do time/money/energy actually flow?
2. **Consistency test** - Which behaviors repeat across contexts?
3. **Tradeoff patterns** - When forced to choose, what wins?
4. **Stress behavior** - What do they prioritize when under pressure?

**Example value inference:**
✅ GOOD:
Value 1: "Status/reputation" - Evidence: Spends 2+ hours daily on LinkedIn self-promotion, name-drops in every meeting (15 times in last team call), hired expensive personal branding consultant ($8k)
Value 2: "Risk avoidance" - Evidence: Declined 3 higher-paying job offers to stay in comfortable role, always seeks consensus before decisions, avoids controversial projects
❌ BAD:
Value 1: "Career success" - Evidence: Works hard (too vague, no specifics)
Value 2: "Being liked" - Evidence: Friendly to people (describes behavior without revealing preference)

Contradiction detected: {{output[-1].contradiction}}
Opportunity cost: {{output[-1].opportunity_cost}}

Respond in JSON:
{
  "actual_values": [
    "Value 1 (1-4 words)",
    "Value 2 (1-4 words)",
    "Value 3 (1-4 words)"
  ],
  "evidence": "For each value, cite specific behaviors with measurements/frequencies/counts that reveal this priority. Use numbers wherever possible (times, dollars, percentages). Max 60 words total.",
  "stated_vs_revealed": "One-sentence summary of the core gap between claimed and actual priorities (max 25 words)"
}

Provide exactly 3 values in priority order. Be specific with evidence - include metrics.""",
            # Predict a choice
            """You are a decision science researcher specializing in behavioral prediction using revealed preference theory.

Given these revealed values, predict their ACTUAL choice in a future tradeoff scenario.

**Prediction framework:**

1. **Past predicts future** - Assume revealed values persist unless context changes dramatically
2. **Intensifying tradeoffs** - When stakes increase, revealed preferences become MORE obvious
3. **Social desirability gap** - They'll SAY the socially acceptable choice, DO the revealed preference

**Example prediction for someone who revealed "career status > family time":**
✅ GOOD: "When offered VP promotion requiring 60hr weeks + 40% travel, they'll accept despite promising spouse to reduce hours. Reasoning: They've already sacrificed family time 3x this year for smaller career gains (skipped kid's recital for optional conference, took weekend calls during vacation). Status/advancement wins in past tradeoffs, will win in future."
❌ BAD: "They'll probably choose work over family. Reasoning: That's what they usually do." (no specific scenario, vague pattern claim, no evidence cited)

Stated preference: {{stated}}
Revealed values: {{output[-1].actual_values}}
Evidence: {{output[-1].evidence}}

Create a SPECIFIC future tradeoff scenario based on their domain, then predict their actual choice.

Respond in JSON:
{
  "scenario": "Concrete future dilemma matching their context with specific details (2 clear options, max 30 words)",
  "predicted_choice": "Which option they'll actually choose and key details (max 25 words)",
  "stated_choice": "Which option they'd CLAIM to prefer publicly (max 20 words)",
  "reasoning": "Why revealed preferences predict this, citing specific past behavior patterns (2-3 sentences, max 50 words)"
}

Make the scenario realistic and testable. Root predictions in actual past behavior."""
        ],
        return_usage=True,
    )

    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    output_dir = os.path.join(project_root, "output", "psychology", "revealed_preference_detective")
    os.makedirs(output_dir, exist_ok=True)

    output_path = os.path.join(output_dir, f"{timestamp}-revealed_preference.json")
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2)

    log_file = MinimalChainable.log_to_markdown("revealed_preference_detective", context_filled_prompts, result, usage_stats)

    print(f"✅ Saved JSON to: {output_path}")
    print(f"✅ Log saved to: {log_file}")


def main():
    stated, revealed = get_input_from_args(
        description="Contrast stated preferences with revealed behavior to infer true values",
        default_context_help="Revealed behavior"
    )
    revealed_preference_detective(stated, revealed)


if __name__ == "__main__":
    main()
