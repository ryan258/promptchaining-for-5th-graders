#!/usr/bin/env python3
"""
🧭 Ideological Consistency Test (adult mode)

Surface contradictions between stated beliefs, derived implications, and likely behavior.

Usage:
    python tools/psychology/ideological_consistency_test.py "Stated beliefs text"
    cat beliefs.txt | python tools/psychology/ideological_consistency_test.py
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


def ideological_consistency_test(beliefs: str):
    print("🧭 Ideological Consistency Test")
    print(f"Beliefs preview: {beliefs[:160]}{'...' if len(beliefs) > 160 else ''}\n")

    user_profile = load_user_context(project_root)
    tone = user_profile.get("writing_style", {}).get("tone", "Direct")

    client, model_names = build_models()
    model_info = (client, model_names[0])

    context_data = {
        "beliefs": beliefs,
        "tone": tone,
    }

    result, context_filled_prompts, usage_stats = MinimalChainable.run(
        context=context_data,
        model=model_info,
        callable=prompt,
        prompts=[
            # Core claims and premises
            """You are a philosopher specializing in argument analysis and logical structure, with expertise in distinguishing explicit claims from implicit premises.

Extract the core claims (what they explicitly argue) and the hidden premises (unstated assumptions required for their argument to work).

**Analysis framework:**

1. **Explicit claims** - What conclusions do they state directly?
2. **Hidden premises** - What must be true for their claims to follow? Look for:
   - Unstated factual assumptions (e.g., "X causes Y" without evidence)
   - Value judgments (e.g., "Y is bad" without defining "bad")
   - Logical leaps (e.g., A→B→C where B→C is assumed, not proven)
3. **Normative vs descriptive** - Are they claiming "is" (fact) or "ought" (value)?

**Example for text "We should abolish homework because Finland doesn't have much homework and they're successful":**

✅ GOOD:
Claims:
- "Schools should abolish homework" (normative, explicit)
- "Finland has minimal homework" (descriptive, explicit)
- "Finland has a successful education system" (descriptive, explicit)

Premises (unstated):
- "Finland's success is caused by low homework, not other factors" (causal assumption)
- "What works in Finland will work in other countries" (transferability assumption)
- "Academic outcomes are the primary measure of success" (value assumption)

❌ BAD:
Claims: ["Homework is bad", "Finland is good"]
Premises: ["Schools should copy Finland"]
(Not distinguishing claim types, mixing claims with premises, too vague)

Tone: {{tone}}

Text to analyze:
{{beliefs}}

Respond in JSON:
{
  "claims": [
    "Claim 1 (max 25 words, specify if normative 'should' or descriptive 'is')",
    "Claim 2 (max 25 words)",
    "Claim 3 (max 25 words)"
  ],
  "premises": [
    "Hidden premise 1 (max 30 words, state what they MUST believe for their argument to work)",
    "Hidden premise 2 (max 30 words)",
    "Hidden premise 3 (max 30 words)"
  ]
}

Provide exactly 3-5 claims and exactly 3-5 premises. Be surgical - extract only core arguments, not supporting details.""",
            # Internal contradictions
            """You are a logician expert in identifying internal contradictions, motivated reasoning, and logical inconsistencies in belief systems.

Analyze the extracted claims and premises for contradictions using this framework:

**Types of contradictions:**

1. **Direct logical conflict** - A claims X, B claims ¬X
2. **Pragmatic contradiction** - Claim requires premise P, but another claim denies P
3. **Value hierarchy conflict** - Prioritizes X over Y in case 1, Y over X in case 2
4. **Scope creep** - Universal claim in one place, qualified claim elsewhere

**Example for beliefs claiming both "Free speech is absolute" and "Hate speech should be banned":**
✅ GOOD:
Between: ["Free speech is absolute (no exceptions)", "Hate speech laws are justified"]
Why: "Absolute means no exceptions, but hate speech laws ARE an exception. Either speech has limits (not absolute) or hate speech is protected (no bans). Cannot hold both unless 'absolute' is redefined."
Severity: High (directly contradictory)

❌ BAD:
Between: ["Free speech", "Hate speech laws"]
Why: "They contradict"
(Too vague, doesn't explain the logical conflict or define terms)

Claims: {{output[-1].claims}}
Premises: {{output[-1].premises}}

Respond in JSON:
{
  "contradictions": [
    {
      "between": ["Specific claim/premise 1 (10-15 words)", "Specific claim/premise 2 (10-15 words)"],
      "why": "Explain the logical conflict, showing why both cannot be true simultaneously (max 50 words)",
      "type": "Direct conflict / Pragmatic / Value hierarchy / Scope creep"
    }
  ],
  "severity": "High (makes argument incoherent) / Med (tension but resolvable) / Low (depends on interpretation)"
}

Provide exactly 2-4 contradictions. Focus on structural conflicts, not nitpicking word choice.""",
            # Behavioral implications
            """You are a behavioral scientist specializing in belief-action consistency and cognitive dissonance prediction.

Given the stated beliefs AND the contradictions detected, predict how they'll actually behave when faced with tradeoffs.

**Prediction framework:**

1. **Cognitive dissonance resolution** - When contradictions surface, people typically:
   - Modify behavior to match stated belief (rare, requires social pressure)
   - Rationalize contradiction away ("this case is different")
   - Avoid situations that expose contradiction

2. **Revealed preference test** - When forced to choose between contradictory beliefs, which wins?
   - First-stated beliefs often lose to later ones
   - Abstract principles lose to concrete self-interest
   - "Should" beliefs lose to "is" beliefs under pressure

**Example for someone believing "Climate change requires urgent action" but also "Economic growth is essential":**
✅ GOOD:
Likely behaviors:
- "When voting, will support climate policies that don't increase personal costs (carbon tax on corporations yes, gas tax no) - abstract principle yields to concrete self-interest"
- "Will buy SUV despite climate concern if family needs justify it - immediate utility beats future risk"
- "Will advocate loudly for climate action while maintaining high-consumption lifestyle - social signaling costs less than behavior change"

If consistent: "Would support carbon taxes even if personally costly, downsize home/vehicle to reduce emissions, prioritize climate over GDP growth in all tradeoffs"

❌ BAD:
Likely behaviors: ["Will be inconsistent", "Won't change much", "Talks more than acts"]
If consistent: ["Would actually care about climate"]
(Vague, no specific scenarios, no reasoning about contradiction resolution)

Claims: {{output[-1].claims}}
Contradictions: {{output[-1].contradictions}}

Respond in JSON:
{
  "likely_behaviors": [
    "Specific behavior prediction with scenario and reasoning (max 40 words each)"
  ],
  "if_consistent": [
    "Specific behavior they'd show if contradictions were resolved toward internally consistent worldview (max 40 words each)"
  ]
}

Provide exactly 3-4 likely behaviors and exactly 2-3 consistent behaviors. Make predictions testable and specific.""",
            # Questions to self-test
            """You are an epistemologist who designs probing questions to test belief consistency and uncover hidden assumptions.

Create questions that expose the contradictions and reading prompts that challenge the weakest premises.

**Question design principles:**

1. **Force explicit tradeoffs** - "If you had to choose between X and Y, which?" (reveals value hierarchy)
2. **Test universality** - "Does this apply to [edge case]?" (tests if principle is truly universal)
3. **Demand evidence** - "What would prove this wrong?" (tests falsifiability)
4. **Surface assumptions** - "What must be true for this to work?" (makes implicit explicit)

**Example for contradictory beliefs about meritocracy:**
✅ GOOD:
Self-test questions:
- "If two candidates have identical test scores but one had tutors/prep courses and one didn't, does the score measure 'merit'? If yes, define merit. If no, how do you measure it?"
- "Name 3 specific ways you'd know if your success was due to your effort vs. your starting advantages. What % luck vs. skill?"
- "Would you trade your current socioeconomic position with a random person from birth? If not, what does that reveal about whether outcomes reflect merit?"

Reading prompts:
- "Meritocracy trap (Daniel Markovits) - argues meritocracy harms even winners"
- "Luck egalitarianism vs. social determinism in outcomes - philosophy of distributive justice"
- "Natural experiments: lottery winners, inherited wealth studies - what happens to effort/outcomes?"

❌ BAD:
Self-test questions: ["Do you really believe in meritocracy?", "What is merit?", "Think about fairness"]
Reading prompts: ["Books on meritocracy", "Economic inequality", "Philosophy"]
(Questions don't force tradeoffs, reading prompts too vague to be actionable)

Contradictions detected: {{output[-1].contradictions}}
Claims and premises: {{output[-1].claims}}, {{output[-1].premises}}

Respond in JSON:
{
  "self_test_questions": [
    "Question that forces a tradeoff, tests an edge case, or demands evidence (max 45 words, should make contradiction uncomfortable)"
  ],
  "reading_prompts": [
    "Specific book/paper/topic with 1-sentence description of why it challenges their premises (max 35 words total)"
  ]
}

Provide exactly 4-5 self-test questions and exactly 4-5 reading prompts. Questions should be genuinely difficult to answer without revealing inconsistency."""
        ],
        return_usage=True,
    )

    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    output_dir = os.path.join(project_root, "output", "psychology", "ideological_consistency_test")
    os.makedirs(output_dir, exist_ok=True)

    output_path = os.path.join(output_dir, f"{timestamp}-ideological_consistency.json")
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2)

    log_file = MinimalChainable.log_to_markdown("ideological_consistency_test", context_filled_prompts, result, usage_stats)

    print(f"✅ Saved JSON to: {output_path}")
    print(f"✅ Log saved to: {log_file}")


def main():
    beliefs, _ = get_input_from_args(
        description="Surface contradictions and implications in stated beliefs",
        default_context_help="(unused)"
    )
    ideological_consistency_test(beliefs)


if __name__ == "__main__":
    main()
