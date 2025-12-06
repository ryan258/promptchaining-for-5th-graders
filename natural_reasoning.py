"""
Natural Reasoning Patterns
===========================

Formalize real-world reasoning structures as reusable chain patterns.

This module implements expert reasoning patterns that have been refined over
centuries of human thought:
- Scientific Method
- Socratic Dialogue
- Design Thinking
- Judicial Reasoning
- Root Cause Analysis (5 Whys)

These patterns can be applied to any domain, making the framework a pedagogical
tool that teaches how experts think about complex problems.
"""

import os
import sys
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from chain import MinimalChainable
from main import build_models, prompt


# ============================================================================
# BASE CONFIGURATION
# ============================================================================

def get_model():
    """Get the default model for reasoning patterns."""
    client, model_names = build_models()
    return (client, model_names[0])


# ============================================================================
# PATTERN 1: SCIENTIFIC METHOD
# ============================================================================

def scientific_method(
    hypothesis: str,
    context: str = "",
    evidence_sources: Optional[List[str]] = None
) -> Tuple[Dict[str, Any], Dict[str, Any]]:
    """
    Apply the scientific method to evaluate a hypothesis.

    The scientific method is humanity's most reliable tool for understanding
    the world. This pattern systematically tests ideas through:
    - Observation
    - Hypothesis formation
    - Prediction
    - Experimentation (thought experiment if needed)
    - Analysis
    - Conclusion

    Args:
        hypothesis: The hypothesis to test (e.g., "MS fatigue is worsened by dehydration")
        context: Additional context or domain knowledge
        evidence_sources: Optional list of evidence to consider

    Returns:
        Tuple of (results dict, metadata dict)
    """
    model_info = get_model()
    evidence_str = "\n".join(evidence_sources) if evidence_sources else "No specific evidence provided - use general knowledge"

    prompts = [
        # Step 1: Observation
        f"""You are a scientist applying the scientific method.

Hypothesis to test: {hypothesis}
Context: {context}
Available evidence: {evidence_str}

STEP 1: OBSERVATION
What observations led to this hypothesis? What phenomena are we trying to explain?

Provide:
1. Key observations that prompted this hypothesis
2. What we already know about the domain
3. What patterns or anomalies need explanation

Return as JSON:
{{
  "observations": ["observation 1", "observation 2", ...],
  "existing_knowledge": "What we already know",
  "phenomena_to_explain": "What patterns need explanation"
}}""",

        # Step 2: Predictions
        f"""You are a scientist. Based on the hypothesis and observations, make testable predictions.

Hypothesis: {hypothesis}
Observations: {{{{output[-1].observations}}}}

STEP 2: PREDICTIONS
If the hypothesis is true, what specific, measurable outcomes would we expect?

Provide:
1. Specific predictions that follow from the hypothesis
2. What we would observe if hypothesis is TRUE
3. What we would observe if hypothesis is FALSE
4. How we could measure/test this

Return as JSON:
{{
  "if_true": ["prediction 1", "prediction 2", ...],
  "if_false": ["alternative outcome 1", ...],
  "measurables": ["metric 1", "metric 2", ...],
  "test_method": "How we could test this"
}}""",

        # Step 3: Thought Experiment / Analysis
        f"""You are a scientist designing an experiment to test the hypothesis.

Hypothesis: {hypothesis}
Predictions if true: {{{{output[-1].if_true}}}}
Test method: {{{{output[-1].test_method}}}}

STEP 3: EXPERIMENTAL DESIGN
Design a rigorous experiment (or thought experiment) to test the hypothesis.

Provide:
1. Experimental design (what would we measure, how, when)
2. Control variables (what must stay constant)
3. Independent variable (what we change)
4. Dependent variable (what we measure)
5. Potential confounds (what could skew results)

Return as JSON:
{{
  "experimental_design": "Detailed description",
  "control_variables": ["var 1", "var 2", ...],
  "independent_variable": "What we manipulate",
  "dependent_variable": "What we measure",
  "potential_confounds": ["confound 1", ...]
}}""",

        # Step 4: Analysis
        f"""You are a scientist analyzing experimental results.

Hypothesis: {hypothesis}
Experimental design: {{{{output[-1].experimental_design}}}}
Predictions: {{{{output[-2].if_true}}}}

STEP 4: ANALYSIS
Analyze what the experiment would likely show, given current knowledge.

Provide:
1. Expected results based on existing evidence
2. How strongly results support/refute hypothesis
3. Alternative explanations for results
4. Limitations of the experiment

Return as JSON:
{{
  "expected_results": "What we'd likely observe",
  "strength_of_evidence": "Strong/Moderate/Weak support or refutation",
  "alternative_explanations": ["explanation 1", ...],
  "limitations": ["limitation 1", ...]
}}""",

        # Step 5: Conclusion
        f"""You are a scientist drawing conclusions from the scientific investigation.

Hypothesis: {hypothesis}
Analysis: {{{{output[-1]}}}}
Evidence strength: {{{{output[-1].strength_of_evidence}}}}

STEP 5: CONCLUSION
Draw a rigorous scientific conclusion and identify next steps.

Provide:
1. Verdict on hypothesis (Supported / Refuted / Inconclusive)
2. Confidence level and reasoning
3. Implications if hypothesis is correct
4. Next research questions
5. Practical applications

Return as JSON:
{{
  "verdict": "Supported/Refuted/Inconclusive",
  "confidence": "High/Medium/Low",
  "reasoning": "Why we reached this conclusion",
  "implications": "What this means if true",
  "next_questions": ["question 1", ...],
  "practical_applications": "How this could be used"
}}"""
    ]

    result, filled_prompts, usage, trace = MinimalChainable.run(
        context={},
        model=model_info,
        callable=prompt,
        return_trace=True,
        prompts=prompts
    )

    # Log the scientific method process
    MinimalChainable.log_to_markdown(
        "scientific_method",
        filled_prompts,
        result,
        usage
    )

    metadata = {
        "pattern": "scientific_method",
        "hypothesis": hypothesis,
        "steps_completed": len(result),
        "total_tokens": sum(usage),
        "verdict": result[-1].get("verdict", "Unknown") if isinstance(result[-1], dict) else "Unknown"
    }

    return {
        "observations": result[0],
        "predictions": result[1],
        "experimental_design": result[2],
        "analysis": result[3],
        "conclusion": result[4]
    }, metadata


# ============================================================================
# PATTERN 2: SOCRATIC DIALOGUE
# ============================================================================

def socratic_dialogue(
    belief: str,
    teacher_persona: str = "Philosopher",
    depth: int = 5
) -> Tuple[Dict[str, Any], Dict[str, Any]]:
    """
    Apply Socratic method to examine and refine a belief.

    The Socratic method uses systematic questioning to uncover assumptions,
    find contradictions, and refine understanding. Named after Socrates, who
    taught by asking questions rather than lecturing.

    Args:
        belief: The belief or claim to examine
        teacher_persona: Who is asking the questions (affects questioning style)
        depth: Number of question-answer rounds (default 5)

    Returns:
        Tuple of (dialogue dict, metadata dict)
    """
    model_info = get_model()

    # Build the dialogue chain
    prompts = []

    # Initial belief statement
    prompts.append(f"""You are a student stating your belief for Socratic examination.

Belief to examine: {belief}

State your belief clearly and explain why you hold it. What are your initial reasons and assumptions?

Return as JSON:
{{
  "belief_statement": "Clear statement of the belief",
  "initial_reasoning": "Why you believe this",
  "key_assumptions": ["assumption 1", "assumption 2", ...]
}}""")

    # Generate question-answer pairs
    for round_num in range(1, depth + 1):
        # Teacher asks probing question
        prompts.append(f"""You are a {teacher_persona} using the Socratic method.

Student's current understanding: {{{{output[-1]}}}}

ROUND {round_num}: Ask a probing question that challenges assumptions or reveals contradictions.

Your question should:
- Challenge a specific assumption
- Reveal potential contradictions
- Explore edge cases
- Deepen understanding

Return as JSON:
{{
  "question": "The probing question",
  "target": "What assumption/claim this targets",
  "purpose": "What you hope to reveal"
}}""")

        # Student responds and refines
        prompts.append(f"""You are a student responding to Socratic questioning.

Question from teacher: {{{{output[-1].question}}}}
Your previous understanding: {{{{output[-2]}}}}

ROUND {round_num}: Answer the question honestly and refine your understanding.

Consider:
- Does the question reveal a flaw in your reasoning?
- Do you need to revise your belief?
- What new nuances do you now see?

Return as JSON:
{{
  "answer": "Your response to the question",
  "revision": "How your understanding has changed (if at all)",
  "new_insight": "What you now realize"
}}""")

    # Final synthesis
    prompts.append(f"""You are a student synthesizing insights from Socratic dialogue.

Original belief: {belief}
Rounds of questioning: {depth}
Final understanding: {{{{output[-1]}}}}

SYNTHESIS: How has your understanding evolved?

Provide:
1. Refined belief (how it's changed)
2. Key insights gained
3. Assumptions you now question
4. Remaining uncertainties
5. Stronger or weaker confidence?

Return as JSON:
{{
  "original_belief": "{belief}",
  "refined_belief": "Your updated understanding",
  "key_insights": ["insight 1", "insight 2", ...],
  "questioned_assumptions": ["assumption 1", ...],
  "uncertainties": ["what you're still unsure about", ...],
  "confidence_change": "Stronger/Weaker/Same",
  "reasoning_quality": "How much more rigorous is your thinking now?"
}}""")

    result, filled_prompts, usage, trace = MinimalChainable.run(
        context={},
        model=model_info,
        callable=prompt,
        return_trace=True,
        prompts=prompts
    )

    # Log the dialogue
    MinimalChainable.log_to_markdown(
        "socratic_dialogue",
        filled_prompts,
        result,
        usage
    )

    # Structure the dialogue for easy reading
    dialogue = {
        "initial_belief": result[0],
        "rounds": [],
        "synthesis": result[-1]
    }

    # Extract question-answer pairs
    for i in range(1, len(result) - 1, 2):
        if i + 1 < len(result) - 1:
            dialogue["rounds"].append({
                "round": (i + 1) // 2,
                "question": result[i],
                "answer": result[i + 1]
            })

    metadata = {
        "pattern": "socratic_dialogue",
        "belief": belief,
        "rounds": depth,
        "total_tokens": sum(usage),
        "belief_changed": result[-1].get("confidence_change", "Unknown") if isinstance(result[-1], dict) else "Unknown"
    }

    return dialogue, metadata


# ============================================================================
# PATTERN 3: DESIGN THINKING
# ============================================================================

def design_thinking(
    problem: str,
    target_user: str = "End user",
    constraints: Optional[List[str]] = None
) -> Tuple[Dict[str, Any], Dict[str, Any]]:
    """
    Apply design thinking methodology to solve a problem.

    Design thinking is a human-centered approach to innovation that puts
    empathy and iteration at the core. Developed at Stanford d.school and
    IDEO, it's used to create user-centered solutions.

    Five phases: Empathize → Define → Ideate → Prototype → Test

    Args:
        problem: The problem to solve (e.g., "MS patients forget medications")
        target_user: Who we're designing for
        constraints: Design constraints (e.g., ["Low tech literacy", "Brain fog"])

    Returns:
        Tuple of (design dict, metadata dict)
    """
    model_info = get_model()
    constraints_str = ", ".join(constraints) if constraints else "No specific constraints"

    prompts = [
        # Phase 1: Empathize
        f"""You are a design thinker in the EMPATHIZE phase.

Problem space: {problem}
Target user: {target_user}
Constraints: {constraints_str}

EMPATHIZE: Deeply understand the user's needs, pain points, and context.

Explore:
1. Who is the user? (demographics, abilities, context)
2. What are their pain points related to this problem?
3. What are their goals and motivations?
4. What's their environment/context?
5. What have they tried before?

Return as JSON:
{{
  "user_profile": {{
    "description": "Who they are",
    "abilities": ["ability 1", ...],
    "limitations": ["limitation 1", ...]
  }},
  "pain_points": ["pain 1", "pain 2", ...],
  "goals": ["goal 1", ...],
  "context": "Their environment and circumstances",
  "current_attempts": "What they've tried and why it failed"
}}""",

        # Phase 2: Define
        f"""You are a design thinker in the DEFINE phase.

User insights: {{{{output[-1]}}}}
Original problem: {problem}

DEFINE: Frame the problem from the user's perspective.

Create a clear problem statement:
"[User] needs a way to [need] because [insight]"

Provide:
1. Point-of-view problem statement
2. Core user need (not solution)
3. Key insights from empathy phase
4. Success criteria (how we'll know it works)

Return as JSON:
{{
  "problem_statement": "[User] needs a way to [need] because [insight]",
  "core_need": "The fundamental user need",
  "key_insights": ["insight 1", "insight 2", ...],
  "success_criteria": ["criterion 1", "criterion 2", ...]
}}""",

        # Phase 3: Ideate
        f"""You are a design thinker in the IDEATE phase.

Problem statement: {{{{output[-1].problem_statement}}}}
Constraints: {constraints_str}

IDEATE: Generate diverse solution ideas without judgment.

Brainstorm 8-10 solutions ranging from:
- Obvious/conventional
- Creative/unconventional
- Wild/provocative

For each idea, note what's interesting about it.

Return as JSON:
{{
  "ideas": [
    {{
      "idea": "Solution description",
      "type": "conventional/creative/wild",
      "interesting_because": "What makes this worth exploring"
    }},
    ...
  ],
  "most_promising": ["idea 1", "idea 2", "idea 3"],
  "why_promising": "Why these stood out"
}}""",

        # Phase 4: Prototype
        f"""You are a design thinker in the PROTOTYPE phase.

Top ideas: {{{{output[-1].most_promising}}}}
Problem statement: {{{{output[-2].problem_statement}}}}
Constraints: {constraints_str}

PROTOTYPE: Design a concrete, detailed solution.

Choose the most promising idea and create a detailed prototype:
1. How does it work? (step-by-step)
2. What does the user experience?
3. What makes it better than alternatives?
4. How does it address constraints?

Return as JSON:
{{
  "chosen_idea": "Which idea you're prototyping",
  "how_it_works": "Detailed step-by-step description",
  "user_experience": "What the user sees/does/feels",
  "key_features": ["feature 1", "feature 2", ...],
  "addresses_constraints": {{
    "constraint_1": "how we handle it",
    ...
  }},
  "differentiators": "Why this is better than alternatives"
}}""",

        # Phase 5: Test
        f"""You are a design thinker in the TEST phase.

Prototype: {{{{output[-1]}}}}
Success criteria: {{{{output[-3].success_criteria}}}}
User pain points: {{{{output[-4].pain_points}}}}

TEST: Evaluate the prototype against user needs.

Test the design:
1. Does it meet success criteria?
2. Does it solve the pain points?
3. What could go wrong?
4. How would you improve it?
5. What would you test with real users?

Return as JSON:
{{
  "meets_criteria": {{
    "criterion_1": "Yes/No/Partial - explanation",
    ...
  }},
  "solves_pain_points": ["pain point 1: how well it's solved", ...],
  "potential_issues": ["issue 1", "issue 2", ...],
  "improvements": ["improvement 1", ...],
  "user_testing_plan": "What to test with real users",
  "overall_assessment": "Strong/Moderate/Weak solution",
  "next_iteration": "What to refine in next version"
}}"""
    ]

    result, filled_prompts, usage, trace = MinimalChainable.run(
        context={},
        model=model_info,
        callable=prompt,
        return_trace=True,
        prompts=prompts
    )

    # Log the process
    MinimalChainable.log_to_markdown(
        "design_thinking",
        filled_prompts,
        result,
        usage
    )

    metadata = {
        "pattern": "design_thinking",
        "problem": problem,
        "target_user": target_user,
        "total_tokens": sum(usage),
        "assessment": result[-1].get("overall_assessment", "Unknown") if isinstance(result[-1], dict) else "Unknown"
    }

    return {
        "empathize": result[0],
        "define": result[1],
        "ideate": result[2],
        "prototype": result[3],
        "test": result[4]
    }, metadata


# ============================================================================
# PATTERN 4: JUDICIAL REASONING
# ============================================================================

def judicial_reasoning(
    case: str,
    relevant_principles: Optional[List[str]] = None,
    precedents: Optional[List[str]] = None
) -> Tuple[Dict[str, Any], Dict[str, Any]]:
    """
    Apply judicial reasoning to analyze a case and reach a decision.

    Judicial reasoning is how courts analyze cases using:
    - Facts of the case
    - Applicable legal/ethical principles
    - Precedent analysis
    - Balancing competing interests
    - Reasoned judgment

    This pattern is excellent for ethical dilemmas, policy decisions, and
    any situation requiring careful weighing of principles.

    Args:
        case: The case to decide (e.g., "Should insurance cover off-label MS treatments?")
        relevant_principles: Applicable principles (e.g., ["beneficence", "justice"])
        precedents: Relevant precedents or similar cases

    Returns:
        Tuple of (judgment dict, metadata dict)
    """
    model_info = get_model()
    principles_str = "\n".join(relevant_principles) if relevant_principles else "Identify relevant principles"
    precedents_str = "\n".join(precedents) if precedents else "No specific precedents provided"

    prompts = [
        # Step 1: Facts of the case
        f"""You are a judge analyzing a case.

Case: {case}

STEP 1: FACTS OF THE CASE
Establish the facts clearly and objectively.

Provide:
1. Key facts (what is undisputed)
2. Disputed facts (what's in question)
3. Relevant context
4. Stakeholders and their interests

Return as JSON:
{{
  "undisputed_facts": ["fact 1", "fact 2", ...],
  "disputed_facts": ["question 1", ...],
  "context": "Relevant background",
  "stakeholders": [
    {{
      "party": "Stakeholder name",
      "interests": "What they want and why"
    }},
    ...
  ]
}}""",

        # Step 2: Applicable principles
        f"""You are a judge identifying applicable principles.

Case: {case}
Facts: {{{{output[-1]}}}}
Suggested principles: {principles_str}

STEP 2: APPLICABLE PRINCIPLES
What principles, rules, or values apply to this case?

Identify:
1. Legal/ethical principles that govern this domain
2. How each principle applies to this case
3. Potential conflicts between principles

Return as JSON:
{{
  "principles": [
    {{
      "principle": "Principle name",
      "description": "What it means",
      "applies_how": "How it relates to this case"
    }},
    ...
  ],
  "conflicts": "Where principles might conflict"
}}""",

        # Step 3: Precedent analysis
        f"""You are a judge analyzing precedents.

Case: {case}
Facts: {{{{output[-2]}}}}
Principles: {{{{output[-1]}}}}
Known precedents: {precedents_str}

STEP 3: PRECEDENT ANALYSIS
How have similar cases been decided?

Analyze:
1. Relevant precedents (real or hypothetical)
2. How this case is similar/different
3. What precedents suggest about this case

Return as JSON:
{{
  "precedents": [
    {{
      "case_name": "Prior case",
      "decision": "How it was decided",
      "similarity": "How it's similar to current case",
      "difference": "How it differs",
      "relevance": "What it suggests for this case"
    }},
    ...
  ],
  "precedent_guidance": "What precedents suggest we should do"
}}""",

        # Step 4: Arguments
        f"""You are a judge considering arguments from both sides.

Case: {case}
Facts: {{{{output[-3]}}}}
Principles: {{{{output[-2]}}}}

STEP 4: ARGUMENTS
Present the strongest arguments for both sides.

Provide:
1. Arguments in favor of [one position]
2. Arguments against [that position]
3. Strength assessment of each argument

Return as JSON:
{{
  "position_A": {{
    "position": "Description of position A",
    "arguments": ["argument 1", "argument 2", ...],
    "strongest_point": "Most compelling argument",
    "weaknesses": ["weakness 1", ...]
  }},
  "position_B": {{
    "position": "Description of position B",
    "arguments": ["argument 1", ...],
    "strongest_point": "Most compelling argument",
    "weaknesses": ["weakness 1", ...]
  }}
}}""",

        # Step 5: Ruling and reasoning
        f"""You are a judge issuing a ruling.

Case: {case}
Facts: {{{{output[-4]}}}}
Principles: {{{{output[-3]}}}}
Arguments: {{{{output[-1]}}}}

STEP 5: RULING AND REASONING
Issue your decision with clear reasoning.

Provide:
1. The ruling (decision)
2. Reasoning (why you decided this way)
3. How you weighed competing interests
4. Dissenting considerations (what argues against your decision)
5. Implications of this ruling

Return as JSON:
{{
  "ruling": "The decision",
  "core_reasoning": "Primary reason for this decision",
  "balancing": "How you weighed competing interests",
  "supporting_factors": ["factor 1", "factor 2", ...],
  "dissenting_considerations": "Arguments against this ruling",
  "implications": "What this means going forward",
  "confidence": "High/Medium/Low",
  "limitations": "Scope or limits of this ruling"
}}"""
    ]

    result, filled_prompts, usage, trace = MinimalChainable.run(
        context={},
        model=model_info,
        callable=prompt,
        return_trace=True,
        prompts=prompts
    )

    # Log the judgment
    MinimalChainable.log_to_markdown(
        "judicial_reasoning",
        filled_prompts,
        result,
        usage
    )

    metadata = {
        "pattern": "judicial_reasoning",
        "case": case,
        "total_tokens": sum(usage),
        "ruling": result[-1].get("ruling", "Unknown") if isinstance(result[-1], dict) else "Unknown"
    }

    return {
        "facts": result[0],
        "principles": result[1],
        "precedents": result[2],
        "arguments": result[3],
        "ruling": result[4]
    }, metadata


# ============================================================================
# PATTERN 5: ROOT CAUSE ANALYSIS (5 WHYS)
# ============================================================================

def five_whys(
    problem: str,
    depth: int = 5,
    context: str = ""
) -> Tuple[Dict[str, Any], Dict[str, Any]]:
    """
    Apply root cause analysis using the "5 Whys" technique.

    The 5 Whys technique, developed by Sakichi Toyoda (Toyota), digs beneath
    surface symptoms to find root causes. By asking "why" repeatedly, you move
    from symptoms to systemic issues.

    Classic example:
    - Problem: Car won't start
    - Why? Battery is dead
    - Why? Alternator not working
    - Why? Belt is broken
    - Why? Belt was old and not replaced
    - Why? No preventive maintenance schedule → ROOT CAUSE

    Args:
        problem: The problem to analyze (e.g., "I missed my medication dose")
        depth: How many "why" levels to explore (default 5)
        context: Additional context about the situation

    Returns:
        Tuple of (analysis dict, metadata dict)
    """
    model_info = get_model()

    prompts = [
        # Initial problem statement
        f"""You are analyzing a problem using the 5 Whys technique.

Problem: {problem}
Context: {context}

STATE THE PROBLEM: Clearly describe the problem as a specific, observable event.

Return as JSON:
{{
  "problem_statement": "Clear, specific statement of what went wrong",
  "observable_symptoms": ["symptom 1", "symptom 2", ...],
  "impact": "Why this problem matters"
}}"""
    ]

    # Generate the "Why?" chain
    for why_num in range(1, depth + 1):
        prompts.append(f"""You are conducting root cause analysis.

{"Problem: " + problem if why_num == 1 else "Previous cause: {output[-1].cause}"}

WHY #{why_num}: Why did {"this problem occur" if why_num == 1 else "this cause happen"}?

Identify the immediate cause at this level. Go deeper than surface explanations.

Return as JSON:
{{
  "why_number": {why_num},
  "question": "The specific 'why' question asked",
  "cause": "The immediate cause at this level",
  "evidence": "What suggests this is the cause",
  "is_root_cause": {"true" if why_num == depth else "false"}
}}""")

    # Synthesis and solution
    prompts.append(f"""You are synthesizing root cause analysis.

Original problem: {problem}
Root cause (Why #{depth}): {{{{output[-1].cause}}}}

SYNTHESIS: Connect the chain and propose systemic fixes.

Provide:
1. The full causal chain
2. The root cause
3. Why this is the root (not just another symptom)
4. Systemic solutions that address the root
5. Quick fixes that address symptoms
6. Prevention strategy

Return as JSON:
{{
  "causal_chain": ["Problem → Why 1 → Why 2 → ... → Root cause"],
  "root_cause": "The fundamental issue",
  "why_this_is_root": "Why this is systemic, not symptomatic",
  "systemic_solutions": ["solution 1", "solution 2", ...],
  "quick_fixes": ["temporary fix 1", ...],
  "prevention": "How to prevent recurrence",
  "effort_vs_impact": "Assessment of solution difficulty vs impact"
}}""")

    result, filled_prompts, usage, trace = MinimalChainable.run(
        context={},
        model=model_info,
        callable=prompt,
        return_trace=True,
        prompts=prompts
    )

    # Log the analysis
    MinimalChainable.log_to_markdown(
        "five_whys",
        filled_prompts,
        result,
        usage
    )

    # Structure the why chain
    why_chain = {
        "problem": result[0],
        "whys": result[1:-1],
        "synthesis": result[-1]
    }

    metadata = {
        "pattern": "five_whys",
        "problem": problem,
        "depth": depth,
        "total_tokens": sum(usage),
        "root_cause": result[-1].get("root_cause", "Unknown") if isinstance(result[-1], dict) else "Unknown"
    }

    return why_chain, metadata


# ============================================================================
# CONVENIENCE: PATTERN REGISTRY
# ============================================================================

REASONING_PATTERNS = {
    "scientific_method": {
        "function": scientific_method,
        "description": "Test hypotheses using observation, prediction, experiment, analysis, conclusion",
        "use_when": "Evaluating claims, testing ideas, scientific inquiry",
        "example": 'scientific_method("MS fatigue is worsened by dehydration")'
    },
    "socratic_dialogue": {
        "function": socratic_dialogue,
        "description": "Question assumptions and refine beliefs through systematic inquiry",
        "use_when": "Examining beliefs, finding contradictions, deepening understanding",
        "example": 'socratic_dialogue("AI will replace doctors", depth=5)'
    },
    "design_thinking": {
        "function": design_thinking,
        "description": "Human-centered problem solving: empathize, define, ideate, prototype, test",
        "use_when": "Designing solutions, innovation, user-centered problems",
        "example": 'design_thinking("MS patients forget medications")'
    },
    "judicial_reasoning": {
        "function": judicial_reasoning,
        "description": "Analyze cases using facts, principles, precedent, and balanced judgment",
        "use_when": "Ethical dilemmas, policy decisions, weighing competing interests",
        "example": 'judicial_reasoning("Should insurance cover off-label MS treatments?")'
    },
    "five_whys": {
        "function": five_whys,
        "description": "Find root causes by asking 'why' repeatedly",
        "use_when": "Solving recurring problems, finding systemic issues",
        "example": 'five_whys("I missed my medication dose", depth=5)'
    }
}


def list_patterns():
    """List all available reasoning patterns."""
    print("\n" + "=" * 70)
    print("NATURAL REASONING PATTERNS")
    print("=" * 70)
    for name, info in REASONING_PATTERNS.items():
        print(f"\n{name.upper()}")
        print(f"  Description: {info['description']}")
        print(f"  Use when: {info['use_when']}")
        print(f"  Example: {info['example']}")
    print("\n" + "=" * 70)


if __name__ == "__main__":
    # Demo mode: show all patterns
    list_patterns()

    print("\nRun demos/natural_reasoning_demo.py to see these patterns in action!")
