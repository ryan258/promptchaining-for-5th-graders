#!/usr/bin/env python3
"""
⚡ Crisis Opportunity Scanner (adult mode)

Spot agenda-driven moves during a crisis: actors, overreach solutions, and the power bypass.

Usage:
    python tools/strategy/crisis_opportunity_scanner.py "Describe the crisis"
    cat crisis.txt | python tools/strategy/crisis_opportunity_scanner.py
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


def crisis_opportunity_scanner(crisis: str):
    print("⚡ Crisis Opportunity Scanner")
    print(f"Crisis: {crisis[:160]}{'...' if len(crisis) > 160 else ''}\n")

    user_profile = load_user_context(project_root)
    tone = user_profile.get("writing_style", {}).get("tone", "Skeptical and concise")

    client, model_names = build_models()
    model_info = (client, model_names[0])

    context_data = {
        "crisis": crisis,
        "tone": tone,
    }

    result, context_filled_prompts, usage_stats = MinimalChainable.run(
        context=context_data,
        model=model_info,
        callable=prompt,
        prompts=[
            # Actors
            """You are a political strategist and policy analyst with 20+ years studying crisis exploitation patterns, specializing in identifying which interest groups use emergencies to advance pre-existing agendas (Rahm Emanuel's "never let a crisis go to waste" doctrine).

Identify actors positioned to exploit this crisis by asking:

**Actor identification framework:**

1. **Who had this policy ready?** - Look for proposals that appear too quickly (written before the crisis)
2. **Who shifts from cause to solution?** - They emphasize the crisis but pivot to their pet issue
3. **Who benefits from expanded authority?** - Follow the power/budget/mandate gains
4. **Who uses "we must act now"?** - Urgency rhetoric that discourages debate

**Example for 9/11 crisis:**
✅ GOOD:
Actors: [
  {
    "group": "National security hawks (DOD, intelligence agencies)",
    "agenda": "Expand surveillance powers, increase defense budget, reduce civil liberties oversight",
    "playbook": "Frame any opposition as 'soft on terror', use ticking time bomb scenarios, propose sunset clauses then extend indefinitely (PATRIOT Act renewed 4x)",
    "pre_crisis_position": "Had been seeking these powers since 1990s encryption debates"
  },
  {
    "group": "Foreign intervention advocates (neoconservatives)",
    "agenda": "Regime change in Middle East beyond Afghanistan (Iraq, Syria, Iran)",
    "playbook": "Link crisis to unrelated targets (Iraq WMD claims), use 'you're either with us or against us' framing, deploy 'mushroom cloud' fear",
    "pre_crisis_position": "PNAC documents from 1997 already advocated Iraq regime change"
  }
]

❌ BAD:
Actors: [
  {"group": "Government", "agenda": "More power", "playbook": "Pass laws"}
]
(Too vague, no specificity about which government actors, what power, what historical pattern)

Tone: {{tone}}

Crisis description:
{{crisis}}

Respond in JSON:
{
  "actors": [
    {
      "group": "Specific actor with institutional affiliation (max 15 words)",
      "agenda": "Concrete policy goals they'll pursue, with specifics (max 30 words)",
      "playbook": "Their typical tactics with historical examples or measurements (max 45 words)",
      "pre_crisis_position": "Evidence this agenda existed before crisis (max 25 words)"
    }
  ]
}

Provide exactly 4-6 actors. Focus on those with institutional power, not fringe groups. Be specific about tactics and cite historical patterns where possible.""",
            # Overreach solutions
            """You are a policy analyst expert in identifying mission creep, scope expansion, and Trojan horse legislation that exploits crisis fear to embed permanent changes beyond the crisis scope.

Analyze proposed solutions for overreach by testing:

**Overreach detection framework:**

1. **Scope test** - Does it address the stated crisis, or go broader?
2. **Duration test** - Temporary emergency or permanent power shift?
3. **Reversibility test** - Can it be easily undone when crisis ends?
4. **Proportionality test** - Do costs (liberty, money, precedent) match the threat?

**Example for 2008 financial crisis:**
✅ GOOD:
Proposed solutions: [
  {
    "solution": "TARP bailout ($700B to banks, minimal homeowner relief, executive comp limits removed)",
    "stated_rationale": "Prevent systemic collapse from toxic mortgages",
    "hidden_agenda": "Socialize losses while privatizing gains, establish 'too big to fail' doctrine, avoid structural banking reform",
    "scope_creep": "Expanded from mortgage-backed securities to auto companies, insurance (AIG), shifted from asset purchases to direct equity injections",
    "winners": ["Large banks (received funds + avoided prosecution)", "Executives (kept bonuses despite failures)"],
    "losers": ["Underwater homeowners (foreclosures continued)", "Small banks (no access to TARP)", "Moral hazard (risk-taking subsidized)"]
  }
]

❌ BAD:
Proposed solutions: [
  {"solution": "Bank bailout", "hidden_agenda": "Help rich people", "winners": ["Banks"], "losers": ["Everyone else"]}
]
(No specific amounts, mechanisms, scope creep analysis, or concrete impact measurement)

Actors identified: {{output[-1].actors}}

Respond in JSON:
{
  "proposed_solutions": [
    {
      "solution": "Specific policy with details: what changes, who it affects, scope/scale (max 35 words)",
      "stated_rationale": "Official justification for the policy (max 20 words)",
      "hidden_agenda": "Unstated goals it enables, with specific powers/precedents gained (max 35 words)",
      "scope_creep": "How it exceeds crisis scope or embeds permanent changes (max 30 words)",
      "winners": ["Specific groups with concrete gains (be precise, max 15 words each)"],
      "losers": ["Specific groups with concrete costs (be precise, max 15 words each)"]
    }
  ]
}

Provide exactly 3-5 solutions. Focus on major policy proposals with lasting impact, not minor adjustments.""",
            # Crisis bypass
            """You are a democratic governance expert specializing in emergency powers, constitutional crisis dynamics, and institutional erosion during states of exception (drawing on work of Clinton Rossiter, Bruce Ackerman).

Analyze how crisis bypasses normal democratic safeguards:

**Bypass mechanism framework:**

1. **Speed bypass** - "No time for debate" rushes bills past scrutiny (PATRIOT Act: 45 days from draft to law, most Congress didn't read it)
2. **Scope bypass** - "Existential threat" suspends normal limits (Lincoln suspending habeas corpus, FDR's Japanese internment)
3. **Accountability bypass** - "Need flexibility" avoids oversight (black sites, warrantless surveillance revealed years later)
4. **Precedent creep** - "Temporary" becomes permanent baseline (income tax "temporary" in 1913, still here; NSA programs continue post-threat)

**Long-term impact analysis:**
Ask: Does the expanded power sunset? Does anyone track if crisis justification is still valid? Can future actors use this precedent?

**Example for COVID-19 pandemic:**
✅ GOOD:
Bypass mechanism: "Public health emergency declarations (PHE) invoked at federal/state level, granting executives unilateral authority to: mandate closures without legislative approval (overriding property rights), restrict movement (stay-at-home orders), mandate medical interventions (vaccine passports). Normal administrative procedure (notice-and-comment, cost-benefit analysis) suspended. Debate framed as 'following science' vs 'killing grandma', chilling opposition."

Long-term impacts: [
  "Precedent that public health justifies suspending civil liberties without legislative vote - future pandemics (or redefined health crises: obesity, climate) could trigger same powers",
  "Expansion of executive emergency authority - 32 states still have active emergency powers 3+ years post-crisis, governors reluctant to relinquish",
  "Erosion of bodily autonomy norms - established that states can mandate medical procedures via employment pressure (OSHA mandates), opens door for future compelled health interventions"
]

Guardrails: [
  "Automatic sunset clauses (30-90 days) requiring legislative re-authorization for emergency powers to continue, with burden of proof that crisis persists",
  "Judicial fast-track review for emergency orders within 15 days, preventing years-long litigation while power remains active",
  "Mandatory cost-benefit analysis even during emergencies, published within 60 days, including civil liberties costs not just health benefits"
]

❌ BAD:
Bypass mechanism: "Emergency powers used to skip normal process"
Long-term impacts: ["Government has more power", "Less freedom"]
Guardrails: ["Better oversight", "Sunset clauses"]
(No specificity about which powers, what process bypassed, how much power, what freedom, what oversight mechanisms)

Solutions analyzed: {{output[-1].proposed_solutions}}

Respond in JSON:
{
  "bypass_mechanism": "Specific description of how crisis suspends normal checks/balances, with institutional details (max 70 words)",
  "urgency_rhetoric": "Key phrases used to shut down debate (quote actual language, max 30 words)",
  "long_term_impacts": [
    "Specific institutional/legal/norm erosion with mechanism for how it persists post-crisis (max 45 words each)"
  ],
  "guardrails": [
    "Specific procedural/institutional check with enforcement mechanism and timeline (max 40 words each)"
  ]
}

Provide exactly 3-4 long-term impacts and exactly 3-4 guardrails. Impacts should describe durable institutional changes, not temporary disruptions. Guardrails must be concrete and enforceable, not vague principles."""
        ],
        return_usage=True,
    )

    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    output_dir = os.path.join(project_root, "output", "strategy", "crisis_opportunity_scanner")
    os.makedirs(output_dir, exist_ok=True)

    output_path = os.path.join(output_dir, f"{timestamp}-crisis_opportunity.json")
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2)

    log_file = MinimalChainable.log_to_markdown("crisis_opportunity_scanner", context_filled_prompts, result, usage_stats)

    print(f"✅ Saved JSON to: {output_path}")
    print(f"✅ Log saved to: {log_file}")


def main():
    crisis, _ = get_input_from_args(
        description="Scan a crisis for agenda-driven actors and overreach solutions",
        default_context_help="(unused)"
    )
    crisis_opportunity_scanner(crisis)


if __name__ == "__main__":
    main()
