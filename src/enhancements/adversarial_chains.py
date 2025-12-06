"""
Adversarial Chains
==================

Build Red/Blue team dialectical reasoning and adversarial dialogue patterns.

This module implements competitive reasoning where multiple perspectives
clash to reveal truth through conflict:
- Red Team vs Blue Team debates
- Adversarial Socratic questioning
- Dialectical synthesis (Thesis → Antithesis → Synthesis)

These patterns are unique to prompt chaining - impossible with single prompts.
They unlock deep philosophical reasoning, ethics, and nuanced understanding.
"""

import os
import sys
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple, Callable

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from src.core.chain import MinimalChainable
from src.core.main import build_models, prompt


# ============================================================================
# BASE CONFIGURATION
# ============================================================================

def get_model():
    """Get the default model for adversarial reasoning."""
    client, model_names = build_models()
    return (client, model_names[0])


def _calculate_total_tokens(usage_list: List[Any]) -> int:
    """Helper to calculate total tokens from a list of usage stats."""
    total = 0
    for usage in usage_list:
        if isinstance(usage, dict):
            total += usage.get("total_tokens", 0)
            if "total_tokens" not in usage:
                total += usage.get("prompt_tokens", 0) + usage.get("completion_tokens", 0)
        else:
            # Handle object with attributes
            total += getattr(usage, "total_tokens", 0)
    return total

# ============================================================================
# PATTERN 1: RED TEAM vs BLUE TEAM
# ============================================================================

def red_vs_blue(
    topic: str,
    position_to_defend: str,
    rounds: int = 3,
    judge_criteria: Optional[List[str]] = None
) -> Tuple[Dict[str, Any], Dict[str, Any]]:
    """
    Run a Red Team vs Blue Team adversarial debate.

    Red Team attacks a position, trying to find flaws and weaknesses.
    Blue Team defends the position, countering attacks.
    Judge evaluates the strength of arguments.

    This pattern reveals weaknesses through adversarial pressure, similar to
    penetration testing for ideas.

    Args:
        topic: The domain or context
        position_to_defend: The claim Blue Team defends
        rounds: Number of attack-defense rounds (default 3)
        judge_criteria: What the judge evaluates (strength of logic, evidence, etc.)

    Returns:
        Tuple of (debate dict, metadata dict)

    Example:
        red_vs_blue(
            topic="MS treatment",
            position_to_defend="MS patients should prioritize aggressive DMTs early",
            rounds=3
        )
    """
    model_info = get_model()
    criteria_str = ", ".join(judge_criteria) if judge_criteria else "logical strength, evidence quality, practical considerations"

    prompts = []

    # Opening statements
    prompts.append(f"""You are BLUE TEAM in a Red vs Blue debate.

Topic: {topic}
Position to defend: {position_to_defend}

OPENING STATEMENT: Present your strongest case for this position.

Provide:
1. Core thesis (what you're arguing)
2. Key supporting arguments (3-5 main points)
3. Evidence or reasoning for each
4. Why this position is strong

Return as JSON:
{{
  "thesis": "Your core claim",
  "arguments": [
    {{
      "point": "Main argument",
      "reasoning": "Why this is true",
      "evidence": "Supporting evidence or logic"
    }},
    ...
  ],
  "conclusion": "Why this position is compelling"
}}""")

    # Rounds of attack and defense
    for round_num in range(1, rounds + 1):
        # Red Team attacks
        prompts.append(f"""You are RED TEAM in a Red vs Blue debate.

Topic: {topic}
Blue Team's position: {position_to_defend}
Blue Team's {"opening statement" if round_num == 1 else "last defense"}: {{{{output[-1]}}}}

ROUND {round_num} - RED TEAM ATTACK: Find and exploit weaknesses.

Your goal is to undermine Blue Team's position by:
1. Identifying flawed assumptions
2. Presenting counterexamples
3. Showing unintended consequences
4. Challenging evidence or logic
5. Revealing trade-offs they're ignoring

Return as JSON:
{{
  "round": {round_num},
  "attacks": [
    {{
      "target": "What you're attacking",
      "attack": "Your counterargument",
      "why_this_undermines": "How this weakens their position"
    }},
    ...
  ],
  "strongest_objection": "Your most damaging criticism",
  "alternative_view": "What you'd argue instead"
}}""")

        # Blue Team defends
        prompts.append(f"""You are BLUE TEAM in a Red vs Blue debate.

Topic: {topic}
Your position: {position_to_defend}
Red Team's attacks: {{{{output[-1]}}}}

ROUND {round_num} - BLUE TEAM DEFENSE: Counter the attacks and strengthen your position.

Respond to Red Team's objections:
1. Address each attack directly
2. Show why objections don't invalidate your position
3. Provide additional evidence or reasoning
4. Acknowledge valid points while maintaining your position
5. Strengthen weak areas they identified

Return as JSON:
{{
  "round": {round_num},
  "counters": [
    {{
      "to_attack": "The attack you're responding to",
      "counter": "Your response",
      "additional_evidence": "New support for your position"
    }},
    ...
  ],
  "concessions": "Valid points from Red Team (if any)",
  "strengthened_position": "How your argument is now stronger"
}}""")

    # Judge's evaluation
    prompts.append(f"""You are an impartial JUDGE evaluating a Red vs Blue debate.

Topic: {topic}
Position debated: {position_to_defend}
Rounds: {rounds}

Blue Team's opening: {{{{output[0]}}}}
Final round attacks: {{{{output[-2]}}}}
Final round defense: {{{{output[-1]}}}}

JUDGE'S EVALUATION: Assess both sides fairly.

Evaluate based on: {criteria_str}

Provide:
1. Strength of Blue Team's case (0-10)
2. Strength of Red Team's attacks (0-10)
3. Most compelling argument from each side
4. Weaknesses that remain in Blue Team's position
5. Whether Blue Team's position still stands
6. Nuanced verdict

Return as JSON:
{{
  "blue_team_strength": 0-10,
  "red_team_strength": 0-10,
  "blue_strongest": "Blue's best argument",
  "red_strongest": "Red's best attack",
  "remaining_weaknesses": ["weakness 1", ...],
  "verdict": "Does the position stand after adversarial testing?",
  "nuanced_conclusion": "A balanced assessment",
  "winner": "Blue/Red/Draw",
  "reasoning": "Why you scored it this way"
}}""")

    result, filled_prompts, usage, trace = MinimalChainable.run(
        context={},
        model=model_info,
        callable=prompt,
        return_trace=True,
        prompts=prompts
    )

    # Log the debate
    MinimalChainable.log_to_markdown(
        "red_vs_blue_debate",
        filled_prompts,
        result,
        usage
    )

    # Structure the debate
    debate = {
        "topic": topic,
        "position": position_to_defend,
        "opening": result[0],
        "rounds": [],
        "judgment": result[-1]
    }

    # Extract attack-defense pairs
    for i in range(1, len(result) - 1, 2):
        if i + 1 < len(result) - 1:
            debate["rounds"].append({
                "round": (i + 1) // 2,
                "red_attack": result[i],
                "blue_defense": result[i + 1]
            })

    metadata = {
        "pattern": "red_vs_blue",
        "topic": topic,
        "rounds": rounds,
        "total_tokens": _calculate_total_tokens(usage),
        "winner": result[-1].get("winner", "Unknown") if isinstance(result[-1], dict) else "Unknown",
        "blue_score": result[-1].get("blue_team_strength", 0) if isinstance(result[-1], dict) else 0,
        "red_score": result[-1].get("red_team_strength", 0) if isinstance(result[-1], dict) else 0
    }

    return debate, metadata


# ============================================================================
# PATTERN 2: DIALECTICAL SYNTHESIS
# ============================================================================

def dialectical(
    thesis: str,
    context: str = "",
    domain: str = ""
) -> Tuple[Dict[str, Any], Dict[str, Any]]:
    """
    Apply dialectical reasoning: Thesis → Antithesis → Synthesis.

    Hegelian dialectic resolves conflicts by finding a higher-order synthesis
    that transcends the thesis-antithesis opposition.

    This pattern is perfect for:
    - Resolving apparent contradictions
    - Finding nuanced positions
    - Transcending binary thinking

    Args:
        thesis: The initial position or claim
        context: Additional context about the domain
        domain: What area this applies to

    Returns:
        Tuple of (dialectic dict, metadata dict)

    Example:
        dialectical(
            thesis="MS patients should prioritize symptom management",
            context="Treatment approaches for multiple sclerosis",
            domain="Medical ethics"
        )
    """
    model_info = get_model()

    prompts = [
        # Step 1: Elaborate the thesis
        f"""You are a philosopher applying dialectical reasoning.

Thesis: {thesis}
Domain: {domain}
Context: {context}

STEP 1: THESIS
Fully develop the thesis position.

Provide:
1. Core claim
2. Supporting arguments
3. Underlying assumptions
4. Implications if accepted
5. Who benefits from this view

Return as JSON:
{{
  "thesis_statement": "Full articulation of the thesis",
  "core_arguments": ["argument 1", "argument 2", ...],
  "assumptions": ["assumption 1", ...],
  "implications": "What follows from accepting this",
  "beneficiaries": "Who this position serves"
}}""",

        # Step 2: Generate antithesis
        f"""You are a philosopher applying dialectical reasoning.

Thesis: {{{{output[-1].thesis_statement}}}}
Thesis assumptions: {{{{output[-1].assumptions}}}}

STEP 2: ANTITHESIS
Develop the antithesis - the opposing position that exposes limits of the thesis.

The antithesis is NOT just negation - it reveals what the thesis excludes,
suppresses, or fails to account for.

Provide:
1. The antithesis position
2. What the thesis ignores or excludes
3. Contradictions in the thesis
4. Who is marginalized by the thesis
5. Why the antithesis is necessary

Return as JSON:
{{
  "antithesis_statement": "The opposing position",
  "what_thesis_ignores": ["ignored factor 1", ...],
  "contradictions_in_thesis": ["contradiction 1", ...],
  "who_is_marginalized": "Whose interests the thesis neglects",
  "necessity": "Why this opposition is essential, not just contrary"
}}""",

        # Step 3: Find the synthesis
        f"""You are a philosopher applying dialectical reasoning.

Thesis: {{{{output[-2].thesis_statement}}}}
Antithesis: {{{{output[-1].antithesis_statement}}}}

STEP 3: SYNTHESIS
Find the higher-order synthesis that transcends the opposition.

The synthesis is NOT a compromise - it's a new position that:
- Preserves truth from both thesis and antithesis
- Resolves the contradiction at a higher level
- Creates new possibilities neither side saw

Provide:
1. The synthesis position
2. How it transcends the opposition
3. Truth preserved from thesis
4. Truth preserved from antithesis
5. What new insight emerges
6. Why this is superior to both

Return as JSON:
{{
  "synthesis_statement": "The transcendent position",
  "how_it_transcends": "How this goes beyond the opposition",
  "from_thesis": "Truth retained from thesis",
  "from_antithesis": "Truth retained from antithesis",
  "emergent_insight": "New understanding that neither side had",
  "superiority": "Why this is better than thesis or antithesis alone",
  "remaining_tensions": "Contradictions that persist (if any)"
}}""",

        # Step 4: Test the synthesis
        f"""You are a philosopher testing a dialectical synthesis.

Original thesis: {thesis}
Synthesis: {{{{output[-1].synthesis_statement}}}}

STEP 4: EVALUATION
Does the synthesis truly transcend the opposition, or is it just a compromise?

Test:
1. Does it resolve the core contradiction?
2. Does it create new possibilities?
3. Is it more adequate to reality than thesis alone?
4. Does it avoid simply averaging the positions?
5. What new contradictions might it contain (seeds of next dialectic)?

Return as JSON:
{{
  "resolves_contradiction": "Yes/No - explanation",
  "creates_new_possibilities": ["possibility 1", ...],
  "more_adequate": "Yes/No - how synthesis better captures reality",
  "avoids_compromise": "How this is transcendence, not averaging",
  "new_contradictions": "Seeds of the next dialectical movement",
  "verdict": "Strong/Moderate/Weak synthesis",
  "why": "Reasoning for verdict"
}}"""
    ]

    result, filled_prompts, usage, trace = MinimalChainable.run(
        context={},
        model=model_info,
        callable=prompt,
        return_trace=True,
        prompts=prompts
    )

    # Log the dialectic
    MinimalChainable.log_to_markdown(
        "dialectical_synthesis",
        filled_prompts,
        result,
        usage
    )

    metadata = {
        "pattern": "dialectical",
        "thesis": thesis,
        "total_tokens": _calculate_total_tokens(usage),
        "synthesis_quality": result[-1].get("verdict", "Unknown") if isinstance(result[-1], dict) else "Unknown"
    }

    return {
        "thesis": result[0],
        "antithesis": result[1],
        "synthesis": result[2],
        "evaluation": result[3]
    }, metadata


# ============================================================================
# PATTERN 3: ADVERSARIAL SOCRATIC DIALOGUE
# ============================================================================

def adversarial_socratic(
    claim: str,
    depth: int = 4,
    aggressive: bool = True
) -> Tuple[Dict[str, Any], Dict[str, Any]]:
    """
    Adversarial Socratic dialogue - aggressive questioning to stress-test claims.

    Unlike the cooperative Socratic dialogue in natural_reasoning.py, this
    version is combative. The questioner actively tries to demolish the claim.

    This reveals every weakness and forces the claimant to defend rigorously.

    Args:
        claim: The claim to stress-test
        depth: Number of adversarial rounds (default 4)
        aggressive: Whether to use aggressive questioning (default True)

    Returns:
        Tuple of (dialogue dict, metadata dict)

    Example:
        adversarial_socratic(
            claim="AI will solve the MS medication adherence problem",
            depth=4,
            aggressive=True
        )
    """
    model_info = get_model()
    style = "aggressively challenge and find every flaw" if aggressive else "probe gently"

    prompts = []

    # Initial claim
    prompts.append(f"""You are defending a claim against adversarial questioning.

Claim: {claim}

STATE YOUR CLAIM: Present it with your strongest initial defense.

Return as JSON:
{{
  "claim": "{claim}",
  "initial_defense": "Why you believe this claim is true",
  "key_premises": ["premise 1", "premise 2", ...],
  "confidence": "High/Medium/Low"
}}""")

    # Adversarial rounds
    for round_num in range(1, depth + 1):
        # Aggressive questioning
        prompts.append(f"""You are an adversarial questioner using the Socratic method.

Claim being tested: {claim}
Defender's current position: {{{{output[-1]}}}}

ROUND {round_num} - ADVERSARIAL QUESTION
Your goal: {style} in the claim.

Find:
- Hidden assumptions that might be false
- Contradictions
- Edge cases where the claim fails
- Alternative explanations
- Burden of proof issues

Ask a question that puts maximum pressure on the weakest point.

Return as JSON:
{{
  "round": {round_num},
  "target_weakness": "What vulnerability you're exploiting",
  "question": "Your challenging question",
  "why_this_matters": "Why this threatens the claim",
  "trap": "What you hope the defender will concede"
}}""")

        # Defender responds
        prompts.append(f"""You are defending your claim under adversarial questioning.

Original claim: {claim}
Adversarial question: {{{{output[-1].question}}}}

ROUND {round_num} - DEFENSE
Respond honestly. If the question reveals a flaw, acknowledge it.

Options:
1. Defend - show why your claim still stands
2. Refine - adjust your claim to account for the challenge
3. Concede - admit the flaw if it's fatal

Return as JSON:
{{
  "round": {round_num},
  "response_type": "Defend/Refine/Concede",
  "response": "Your answer to the question",
  "revised_claim": "Adjusted claim (if refined)",
  "confidence_now": "High/Medium/Low",
  "what_you_learned": "What this round revealed"
}}""")

    # Final verdict
    prompts.append(f"""You are evaluating an adversarially-tested claim.

Original claim: {claim}
Rounds of questioning: {depth}
Final position: {{{{output[-1]}}}}

VERDICT: Has the claim survived adversarial testing?

Assess:
1. Did the claim hold up, or did it need major revision?
2. What are the strongest objections that were raised?
3. What are the strongest defenses that survived?
4. Is the claim now more or less credible?
5. What are its clear limits?

Return as JSON:
{{
  "survived": "Yes/Partially/No",
  "strongest_objections": ["objection 1", ...],
  "strongest_defenses": ["defense 1", ...],
  "credibility": "Increased/Same/Decreased",
  "clear_limits": "Where the claim clearly doesn't apply",
  "refined_claim": "Best version of the claim after testing",
  "confidence_verdict": "Should we believe this claim?",
  "remaining_vulnerabilities": ["vulnerability 1", ...]
}}""")

    result, filled_prompts, usage, trace = MinimalChainable.run(
        context={},
        model=model_info,
        callable=prompt,
        return_trace=True,
        prompts=prompts
    )

    # Log the adversarial dialogue
    MinimalChainable.log_to_markdown(
        "adversarial_socratic",
        filled_prompts,
        result,
        usage
    )

    # Structure the dialogue
    dialogue = {
        "original_claim": result[0],
        "rounds": [],
        "verdict": result[-1]
    }

    # Extract question-answer pairs
    for i in range(1, len(result) - 1, 2):
        if i + 1 < len(result) - 1:
            dialogue["rounds"].append({
                "round": (i + 1) // 2,
                "challenge": result[i],
                "defense": result[i + 1]
            })

    metadata = {
        "pattern": "adversarial_socratic",
        "claim": claim,
        "rounds": depth,
        "total_tokens": _calculate_total_tokens(usage),
        "survived": result[-1].get("survived", "Unknown") if isinstance(result[-1], dict) else "Unknown",
        "credibility_impact": result[-1].get("credibility", "Unknown") if isinstance(result[-1], dict) else "Unknown"
    }

    return dialogue, metadata


# ============================================================================
# CONVENIENCE: PATTERN REGISTRY
# ============================================================================

ADVERSARIAL_PATTERNS = {
    "red_vs_blue": {
        "function": red_vs_blue,
        "description": "Red Team attacks position, Blue Team defends, Judge evaluates",
        "use_when": "Testing ideas through adversarial pressure, finding weaknesses",
        "example": 'red_vs_blue("MS treatment", "Aggressive DMTs should be prioritized", rounds=3)'
    },
    "dialectical": {
        "function": dialectical,
        "description": "Thesis → Antithesis → Synthesis (Hegelian dialectic)",
        "use_when": "Resolving contradictions, transcending binary thinking, finding nuance",
        "example": 'dialectical("Prioritize symptom management", domain="MS treatment")'
    },
    "adversarial_socratic": {
        "function": adversarial_socratic,
        "description": "Aggressive Socratic questioning to stress-test claims",
        "use_when": "Rigorously testing beliefs, finding vulnerabilities, intellectual honesty",
        "example": 'adversarial_socratic("AI will solve medication adherence", depth=4)'
    }
}


def list_patterns():
    """List all available adversarial patterns."""
    print("\n" + "=" * 70)
    print("ADVERSARIAL REASONING PATTERNS")
    print("=" * 70)
    print("\nThese patterns use conflict and opposition to reveal truth:")
    for name, info in ADVERSARIAL_PATTERNS.items():
        print(f"\n{name.upper()}")
        print(f"  Description: {info['description']}")
        print(f"  Use when: {info['use_when']}")
        print(f"  Example: {info['example']}")
    print("\n" + "=" * 70)


if __name__ == "__main__":
    # Demo mode: show all patterns
    list_patterns()

    print("\nRun demos/adversarial_chains_demo.py to see these patterns in action!")
