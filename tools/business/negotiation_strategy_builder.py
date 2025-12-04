#!/usr/bin/env python3
"""
🤝 Negotiation Strategy Builder (adult mode)

Analyze leverage, BATNAs, anchors, objections, and counter-scripts for a negotiation scenario.

Usage:
    python tools/business/negotiation_strategy_builder.py "Scenario description"
    python tools/business/negotiation_strategy_builder.py "Scenario" --context "Role, constraints, numbers"
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


def negotiation_strategy_builder(scenario: str, additional_context: str = ""):
    print("🤝 Negotiation Strategy Builder")
    print(f"Scenario: {scenario}")
    if additional_context:
        print(f"Context: {additional_context}")
    print()

    user_profile = load_user_context(project_root)
    tone = user_profile.get("writing_style", {}).get("tone", "Professional and firm")

    client, model_names = build_models()
    model_info = (client, model_names[0])

    context_data = {
        "scenario": scenario,
        "additional_context": additional_context,
        "tone": tone,
    }

    result, context_filled_prompts, usage_stats = MinimalChainable.run(
        context=context_data,
        model=model_info,
        callable=prompt,
        prompts=[
            # Power analysis
            """You are a negotiation strategist with 20+ years experience in high-stakes business negotiations, specializing in power asymmetry analysis and BATNA development (trained in Harvard Negotiation Project methodology, Getting to Yes framework).

Analyze the power dynamics using a systematic leverage assessment:

**Power analysis framework:**

1. **Alternatives** - Who has better options if this deal fails? (BATNA strength)
2. **Urgency** - Who faces time pressure? (Deadline = weakness, patience = power)
3. **Information** - Who knows more about the other's constraints? (Transparency = vulnerability)
4. **Resources** - Who can absorb a failed deal? (Capital, runway, dependencies)
5. **Replaceability** - How easily can each side find alternatives? (Unique value = power)

**Leverage indicators:**
- High power: Multiple good alternatives, no urgency, information advantage, resourced, hard to replace
- Low power: Few alternatives, deadline pressure, information disadvantage, resource-constrained, easily replaced

**Example for "Negotiating salary for senior engineer role, competing offer at $180K, this company offering $150K":**
✅ GOOD:
Leverage analysis: "YOU have strong leverage: (1) Competing offer is verified alternative at +20% ($180K vs $150K), (2) Employer has 3-month vacancy cost (~$60K in delayed projects), you can wait, (3) You know their initial offer, they don't know your floor, (4) Senior engineers are scarce (12% vacancy rate in domain), they're replaceable employer in hot market. Power gap: 2-3 tiers in your favor."
My power: High (quantified BATNA, time flexibility, rare skillset)
Their power: Medium-Low (vacancy costs, talent scarcity, but unlimited capital/not urgent)

❌ BAD:
Leverage analysis: "They need engineers, you have options"
My power: High
Their power: Low
(No specifics, no measurements, no analysis of relative strength, no mechanism)

Tone: {{tone}}

Scenario: {{scenario}}
Additional context: {{additional_context}}

Respond in JSON:
{
  "leverage_analysis": "Systematic assessment of 5 power factors (alternatives, urgency, info, resources, replaceability) with specific evidence and measurements where possible (max 80 words)",
  "my_power": "High/Medium/Low (with 1-2 key factors justifying this rating, max 20 words)",
  "their_power": "High/Medium/Low (with 1-2 key factors justifying this rating, max 20 words)",
  "power_gap": "Estimate relative power in your favor or theirs (e.g., '2 tiers in your favor', 'roughly even', '1 tier in their favor')"
}

Be specific with numbers, timelines, market conditions. Avoid vague assessments.""",
            # BATNAs
            """You are a BATNA analyst expert in defining walkaway alternatives and reservation prices.

Define the Best Alternative To Negotiated Agreement for both sides - this is their real power.

**BATNA definition framework:**

1. **Be specific** - Not "find another job" but "Accept XYZ Corp offer at $180K, start in 2 weeks"
2. **Include costs** - Time, money, opportunity cost of switching to BATNA
3. **Rate quality** - Strong BATNA (nearly as good as desired deal), Weak BATNA (much worse), No BATNA (desperate)
4. **BATNA ≠ wishful thinking** - Must be realistic, available NOW, not hypothetical

**Example for salary negotiation with competing offer:**
✅ GOOD:
My BATNA: "Accept competing offer from TechCo at $180K base + $30K equity (4yr vest), role is 85% match to skills vs 95% here, start date in 2 weeks. Quality: Strong - only 10% worse fit, higher comp. Cost: Minimal, offer in hand."
Their BATNA: "Continue 3-month search (avg $60K in delayed projects per month = $180K total cost), hire junior for $120K (saves $30K/year but adds 6-month ramp = net negative), or use contractor at $120/hr (~$250K/year). Quality: Weak - all options worse than paying you $180K. Cost: High - time and productivity."

❌ BAD:
My BATNA: "Get another job"
Their BATNA: "Hire someone else"
(Not specific, no numbers, no quality assessment, no costs, not actionable)

Power analysis: {{output[-1].leverage_analysis}}

Respond in JSON:
{
  "my_batna": "Specific alternative with numbers, timing, quality assessment (how good vs desired deal, %), and costs (max 50 words)",
  "their_batna": "Specific alternative with numbers, timing, quality assessment (how good vs desired deal, %), and costs (max 50 words)",
  "batna_gap": "Whose BATNA is stronger and by how much? This determines who has more power (max 30 words)",
  "reservation_price": "Your walkaway number/terms based on BATNA (e.g., 'Won't accept below $175K', 'Must have 20% equity', max 20 words)"
}

BATNAs must be concrete enough to actually execute. Include specific numbers and timelines.""",
            # Anchoring
            """You are a behavioral negotiation expert specializing in anchoring effects and strategic first offers (research on extremity, credibility, and adjustment psychology).

Set the opening anchor using power/BATNA analysis to determine who should speak first and what number to open with.

**Anchoring strategy framework:**

1. **Who speaks first?**
   - Speak FIRST if: You have strong power, know market value, want to set frame
   - Let THEM speak first if: You're uncertain on value, they have more info, you want to learn their range

2. **How aggressive?**
   - Aggressive anchor (20-30% beyond target): Use if high power, competitive market, need negotiating room
   - Moderate anchor (10-15% beyond target): Use if balanced power, ongoing relationship matters
   - Conservative anchor (5-10% beyond target): Use if weak power, risk they walk away

3. **Justification matters** - Anchor with rationale is stronger than anchor alone
   - Bad: "I want $200K"
   - Good: "I want $200K based on market rate for senior engineers with 10 years ($185K avg) + competing offer at $180K + my domain expertise"

**Example for strong BATNA scenario (competing offer $180K, target $190-200K):**
✅ GOOD:
Speak first: Yes (you have strong BATNA, sets high anchor)
Opening anchor: "$210K base salary with standard equity package. Here's why: Market rate for senior engineers in this domain is $185K (Glassdoor data), my competing offer is $180K, and I bring specialized ML infrastructure expertise you're currently lacking (saves 6mo+ ramp time = $90K+ value). I'm anchoring high because my BATNA is strong and I want room to negotiate down to $195-200K range."
Reasoning: "Aggressive anchor (25% above competing offer) is justified by strong power position (verified BATNA, their urgency). Opens space to 'concede' to $195K while staying above target. Rationale cites objective data (market, offer, value-add) making anchor credible not arbitrary."

❌ BAD:
Speak first: Yes
Opening anchor: "$200K"
Reasoning: "That's what I want"
(No justification, no strategy for concessions, doesn't tie to BATNA or power analysis)

Leverage: {{output[-2].leverage_analysis}}
BATNAs: {{output[-1].my_batna}} vs {{output[-1].their_batna}}
BATNA gap: {{output[-1].batna_gap}}

Respond in JSON:
{
  "speak_first": "Yes/No (with brief reasoning based on power/info asymmetry, max 20 words)",
  "opening_anchor": "Specific proposal with numbers/terms and built-in rationale (max 60 words)",
  "aggressiveness": "Aggressive (20-30% beyond target) / Moderate (10-15%) / Conservative (5-10%) with justification based on power",
  "target_outcome": "Your realistic goal after negotiation, given power dynamics (max 25 words)",
  "walk_away_point": "Your reservation price/terms based on BATNA (max 20 words)"
}

Anchor must be defensible with data, market rates, or objective value. Include the reasoning IN the anchor statement.""",
            # Objections
            """You are a sales and negotiation psychologist expert in objection patterns and resistance analysis.

Predict their strongest objections to your anchor - think like a skeptical counterpart trying to push back.

**Objection prediction framework:**

1. **Budget objection** - "Too expensive / over our range / can't afford it"
2. **Comparison objection** - "Others cost less / market rate is lower / internal equity issues"
3. **Value objection** - "Not worth it / unproven / risky / we can do it cheaper internally"
4. **Process objection** - "Need approval / not in budget cycle / have to check with others"
5. **Alternative objection** - "We have other candidates / can wait / can use contractors"

**Objection quality - Make them sharp:**
- Weak: "That's too high" (vague)
- Strong: "Our budget for this role is $170K and internal equity means we can't go above that without adjusting 5 other salaries"

**Example for $210K anchor when their initial offer was $150K:**
✅ GOOD:
Objections: [
  "Budget: Our approved range for senior roles is $150-170K max. Going to $210K requires VP approval and sets precedent that breaks internal equity - we'd have to adjust 3 current engineers' salaries upward.",
  "Market comparison: Our data shows market rate for senior engineers is $165K median in this region. Your ask is 27% above market, even accounting for experience.",
  "Alternative: We have two other strong candidates interviewing at $155-165K range. If you're unwilling to negotiate down significantly, we'll move forward with them rather than break our comp structure."
]

❌ BAD:
Objections: ["Too expensive", "Others are cheaper", "We can't do that"]
(Too vague, no specifics, no reasoning, not sharp enough to prepare against)

Anchor: {{output[-1].opening_anchor}}
Target: {{output[-1].target_outcome}}
Their BATNA: {{output[-2].their_batna}}

Respond in JSON:
{
  "objections": [
    "Specific objection with reasoning, numbers, or constraints (max 40 words each)"
  ]
}

Provide exactly 3-4 objections in order of likely severity. Make them as strong as possible - imagine their best negotiator making the case.""",
            # Counter-scripts
            """You are a persuasion expert specializing in objection handling, value reframing, and maintaining frame control in negotiations.

Write counter-scripts for each objection that:
1. Acknowledge without apologizing
2. Reframe to value, not cost
3. Use evidence/data
4. Avoid premature concessions

**Counter-script framework:**

1. **Acknowledge + reframe** - "I understand budget constraints [acknowledge]. Let's look at value delivered [reframe]."
2. **Cite objective data** - Market rates, competitive offers, ROI calculations, cost of delay
3. **Maintain frame** - Don't accept their frame (cost), shift to your frame (value)
4. **Concede strategically** - Only concede if they concede, never unilateral, never on first ask

**Example counter-scripts for "$210K is above our $150-170K range" objection:**
✅ GOOD:
Response script: "I appreciate the budget parameters. Here's the value equation: You've had this role open 3 months at ~$60K/month in delayed projects ($180K sunk cost). Hiring me at $210K vs. continuing search for 2 more months to find $170K candidate costs you $120K in additional delays + 6mo ramp time for less experienced candidate. My competing offer at $180K + domain expertise means I deliver ROI in month 1. Where's the flexibility in your range given this math?"

Alternative if they push back: "What if we structure it as $195K base + performance bonus tied to shipping the ML pipeline in Q1? That keeps base closer to your range while rewarding the speed-to-value you need."

❌ BAD:
Response script: "Okay, I can go lower. How about $190K?"
(Immediate concession, no value defense, gives up negotiating position, doesn't address their objection)

Objections: {{output[-1].objections}}
Anchor: {{output[-2].opening_anchor}}
Target: {{output[-2].target_outcome}}

Respond in JSON:
{
  "scripts": [
    {
      "objection": "Quote the objection (abbreviated, max 20 words)",
      "response_script": "Counter-script using acknowledge+reframe+evidence+strategic concession if needed (max 70 words)",
      "fallback_script": "Alternative response if they reject first counter, with potential tactical concession (max 50 words)"
    }
  ],
  "concession_guardrails": [
    "Specific things NOT to concede or give away without getting something back (max 25 words each)"
  ],
  "negotiation_choreography": "Suggested sequence: which concessions in what order IF needed, what to demand in return (max 50 words)"
}

Provide scripts for 3-4 objections. Each script should maintain your power position while showing flexibility on structure, not just price. Include 3-4 concession guardrails."""
        ],
        return_usage=True,
    )

    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    output_dir = os.path.join(project_root, "output", "business", "negotiation_strategy_builder")
    os.makedirs(output_dir, exist_ok=True)

    output_path = os.path.join(output_dir, f"{timestamp}-negotiation_strategy.json")
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2)

    log_file = MinimalChainable.log_to_markdown("negotiation_strategy_builder", context_filled_prompts, result, usage_stats)

    print(f"✅ Saved JSON to: {output_path}")
    print(f"✅ Log saved to: {log_file}")


def main():
    scenario, context = get_input_from_args(
        description="Build a negotiation strategy with leverage, BATNA, anchoring, objections, and scripts"
    )
    negotiation_strategy_builder(scenario, context)


if __name__ == "__main__":
    main()
