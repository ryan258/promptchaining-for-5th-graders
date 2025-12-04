#!/usr/bin/env python3
"""
🕊️ Diplomatic Subtext Decoder (adult mode)

Translate diplomatese into real intent, predict response, and surface political purpose.

Usage:
    python tools/strategy/diplomatic_subtext_decoder.py "Statement"
    cat statement.txt | python tools/strategy/diplomatic_subtext_decoder.py
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


def diplomatic_subtext_decoder(statement: str):
    print("🕊️ Diplomatic Subtext Decoder")
    print(f"Statement: {statement[:160]}{'...' if len(statement) > 160 else ''}\n")

    user_profile = load_user_context(project_root)
    tone = user_profile.get("writing_style", {}).get("tone", "Realpolitik, concise")

    client, model_names = build_models()
    model_info = (client, model_names[0])

    context_data = {
        "statement": statement,
        "tone": tone,
    }

    result, context_filled_prompts, usage_stats = MinimalChainable.run(
        context=context_data,
        model=model_info,
        callable=prompt,
        prompts=[
            # Translate diplomatese
            """You are a diplomatic analyst with 15+ years decoding international statements, specializing in translating euphemistic diplomatic language into actionable intelligence (expertise in signal theory, audience costs, and credible commitment problems in IR).

Translate this diplomatic statement into blunt, explicit language by decoding:

**Diplomatic euphemism decoder:**

1. **Passive voice = dodging responsibility** - "Mistakes were made" → "We screwed up but won't say who"
2. **Concern/monitoring = inaction** - "We are monitoring closely" → "We'll watch but do nothing"
3. **Condemn/deplore = words only** - "We condemn in strongest terms" → "We disapprove but won't act"
4. **Consequences = empty threat** - "There will be consequences" → "Vague threat with no commitment"
5. **All options on table = status quo** - "All options remain on table" → "Including the option to do nothing"
6. **Discussions ongoing = deadlock** - "Productive discussions continue" → "No agreement, buying time"

**Action level scale:**
- **Zero**: Pure posturing, no behavior change (statements, condemnations, monitoring)
- **Low**: Symbolic acts, easily reversed (recalls ambassador for "consultations", suspends meeting, strongly worded letter)
- **Medium**: Costly but reversible (sanctions, aid cuts, military exercises near border)
- **High**: Irreversible commitment (troop deployment, ultimatum with deadline, breaking diplomatic ties)

**Blame positioning**: Who's framed as responsible? Who's excused? (Active voice assigns blame, passive voice diffuses it)

**Example for "We are gravely concerned by recent developments and call on all parties to exercise restraint":**
✅ GOOD:
Translation: "We won't intervene militarily or impose meaningful costs. Both sides should stop, but we're not forcing either to comply. We're issuing this statement to be on the record as disapproving, but our actual policy is unchanged. Passive 'developments' language avoids naming aggressor."
Action level: Zero (statement only, no behavior change demanded, no enforcement)
Blame positioning: "Diluted across 'all parties' equally, even if one is aggressor. Passive 'developments' (not 'attacks' or 'invasion') avoids assigning responsibility. Maintains neutrality posture for domestic consumption."

❌ BAD:
Translation: "They're worried about the situation"
Action level: Low
Blame positioning: "Blames everyone"
(Doesn't decode euphemisms, no analysis of actual commitment level, misses strategic purpose)

Tone: {{tone}}

Statement to decode:
{{statement}}

Respond in JSON:
{
  "translation": "Explicit, blunt translation exposing what they WILL and WON'T do (3-5 sentences, max 80 words total)",
  "action_level": "Zero/Low/Medium/High (with brief justification, max 25 words)",
  "blame_positioning": "Who's blamed, who's excused, how language structure achieves this (max 40 words)",
  "key_omissions": "Critical things NOT said that reveal true policy (max 30 words)"
}

Be surgical about gaps between rhetoric and commitment. Quote specific euphemisms decoded.""",
            # Predict response
            """You are an international relations strategist expert in game theory, audience costs, and credible signaling in crisis bargaining.

Predict how the target actor will respond based on the signal's strength/weakness.

**Response prediction framework:**

1. **Weakness invites escalation** - If statement is all talk (Zero/Low action level), target interprets as green light
   - Low audience costs = easy to back down = not credible
   - Example: "Serious consequences" without specifics → Target escalates to probe limits

2. **Specificity signals resolve** - Vague threats are cheap talk; specific commitments with costs are credible
   - "Consequences" (vague) vs "50% tariff on your exports effective Monday" (specific, costly, credible)

3. **Deadline = commitment** - Open-ended warnings lack credibility; deadlines create audience costs
   - "Eventually there will be costs" vs "If troops not withdrawn by Friday, we invoke Article 5"

4. **Consistency test** - Does this match past behavior? If not, likely bluff
   - Actor who's never followed through on threats won't suddenly start

**Example for Zero action level statement:**
✅ GOOD:
Prediction: "Escalation - target proceeds with planned action (annex territory, pass law, arrest dissidents) because statement signals no enforcement. They may add token gesture (delay by 48hrs, release one prisoner) to claim 'responded to international pressure' but core action continues."
Reasoning: "Zero action level = pure talk, no costs imposed. Past pattern: issuer made similar statements 3x before (Crimea 2014, Hong Kong 2020, Belarus 2021) with no follow-through, establishing reputation for empty threats. Target's domestic audience costs for backing down exceed any international pressure, so they'll test limits. If they retreat from mere words, they look weak domestically."

❌ BAD:
Prediction: "Might escalate or might not"
Reasoning: "Depends on the situation"
(No specific prediction, no mechanism, no reference to credibility/costs)

Translation: {{output[-1].translation}}
Action level: {{output[-1].action_level}}
Blame positioning: {{output[-1].blame_positioning}}

Respond in JSON:
{
  "prediction": "Escalation / De-escalation / Status quo (with specific behavior target will likely take, max 40 words)",
  "confidence": "Low (30-50%) / Medium (50-75%) / High (75%+) with brief justification",
  "reasoning": "Why this response is most likely, citing credibility signals, audience costs, past precedent (max 60 words)",
  "wildcards": "Events that could change this prediction (max 30 words)"
}

Ground prediction in signaling theory and past behavior patterns, not wishful thinking.""",
            # Intent/purpose
            """You are a political communications analyst expert in strategic ambiguity, domestic-international audience tradeoffs, and face-saving mechanisms in diplomacy.

Identify the true purpose of this statement (hint: it's often NOT about changing the target's behavior).

**Purpose framework - Ask:**

1. **Domestic vs international audience?** - Is this for voters at home or for foreign actors?
   - Domestic: Shows strength, assigns blame, justifies inaction ("we condemned them, that's all we can do")
   - International: Signals intentions, coordinates allies, manages escalation

2. **Action or optics?** - Does issuer expect behavior change, or just want to be seen as responding?
   - Action: Specific demands, deadlines, enforcement mechanisms
   - Optics: Vague concern, "monitoring", calls for restraint (box-checking)

3. **Face-saving?** - Is this creating off-ramps for de-escalation without admitting defeat?
   - "Both sides should de-escalate" = giving aggressor excuse to freeze gains without calling it surrender

**Example for vague "concern" statement during ally's human rights violation:**
✅ GOOD:
Political purpose: "Domestic audience management - appear to uphold values (human rights) without endangering strategic relationship (military base access, trade). Statement signals to domestic critics 'we said something' while signaling to ally 'we won't actually do anything' via zero action level."

Intended audiences:
- "Primary: Domestic voters/human rights groups (66% of communication) - fulfill expectation of moral response, defuse pressure for sanctions"
- "Secondary: Ally government (25%) - private message is 'ignore this statement, relationship unchanged', public statement is cover"
- "Tertiary: International community (9%) - maintain human rights rhetoric credibility, minimal"

Effectiveness: "High for domestic (critics can't say they ignored it), High for ally (correctly reads it as theater), Low for actually changing behavior (Zero action level)"

Message discipline: "Carefully avoids naming violations specifically ('concerning reports' not 'torture'), avoids naming perpetrator directly, no deadline or consequences → maximally vague to avoid audience costs"

❌ BAD:
Political purpose: "Show they care"
Intended audiences: ["The public", "Other countries"]
Effectiveness: "Med"
(No analysis of competing audiences, missing domestic/international tradeoff, no mechanism explained)

Translation: {{output[-1].translation}}
Action level: {{output[-1].action_level}}
Predicted response: {{output[-1].prediction}}

Respond in JSON:
{
  "political_purpose": "Primary strategic goal and how this statement achieves it (max 40 words)",
  "intended_audiences": [
    "Specific audience 1 (domestic/ally/adversary/specific group) with % emphasis and desired takeaway (max 30 words each)"
  ],
  "effectiveness": "Low/Med/High for each purpose, with brief justification (max 35 words total)",
  "message_discipline": "What language choices reveal about constraints/priorities (what's avoided, what's emphasized) (max 35 words)"
}

Provide exactly 2-4 audiences in priority order. Effectiveness should assess against the ACTUAL purpose (often not the stated purpose)."""
        ],
        return_usage=True,
    )

    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    output_dir = os.path.join(project_root, "output", "strategy", "diplomatic_subtext_decoder")
    os.makedirs(output_dir, exist_ok=True)

    output_path = os.path.join(output_dir, f"{timestamp}-diplomatic_decoder.json")
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2)

    log_file = MinimalChainable.log_to_markdown("diplomatic_subtext_decoder", context_filled_prompts, result, usage_stats)

    print(f"✅ Saved JSON to: {output_path}")
    print(f"✅ Log saved to: {log_file}")


def main():
    statement, _ = get_input_from_args(
        description="Decode diplomatic language for subtext, intent, and likely responses",
        default_context_help="(unused)"
    )
    diplomatic_subtext_decoder(statement)


if __name__ == "__main__":
    main()
