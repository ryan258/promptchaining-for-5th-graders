"""
Measurement of Emergence
=========================

Scientifically measure whether prompt chains unlock insights impossible from
single mega-prompts.

This module runs systematic comparisons:
- Chain approach vs Single mega-prompt
- Measure: Novelty, Depth, Coherence, Pedagogical effectiveness
- Statistical analysis across multiple topics
- Generate evidence-based validation

This answers the fundamental question: "Do chains really work better?"
"""

import os
import sys
import json
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple, Callable
from datetime import datetime

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from chain import MinimalChainable
from main import build_models, prompt


# ============================================================================
# BASE CONFIGURATION
# ============================================================================

def get_model():
    """Get the default model for measurements."""
    client, model_names = build_models()
    return (client, model_names[0])


# ============================================================================
# CORE COMPARISON FRAMEWORK
# ============================================================================

def measure_emergence(
    topic: str,
    chain_function: Callable,
    baseline_prompt: Optional[str] = None,
    **chain_kwargs
) -> Tuple[Dict[str, Any], Dict[str, Any]]:
    """
    Compare a chain approach vs single mega-prompt on a topic.

    This is the core measurement function that runs both approaches and
    compares their outputs across multiple dimensions.

    Args:
        topic: The topic to explore (e.g., "Quantum Computing")
        chain_function: The chain function to test (e.g., concept_simplifier)
        baseline_prompt: Optional custom baseline prompt (auto-generated if None)
        **chain_kwargs: Arguments to pass to the chain function

    Returns:
        Tuple of (comparison dict, metadata dict)
    """
    model_info = get_model()

    print(f"\n{'='*70}")
    print(f"MEASURING EMERGENCE: {topic}")
    print(f"{'='*70}")

    # Step 1: Run the chain
    print("\n🔗 Running chain approach...")
    chain_start = datetime.now()

    try:
        chain_result, chain_meta = chain_function(topic, **chain_kwargs)
        chain_output = json.dumps(chain_result, indent=2) if isinstance(chain_result, dict) else str(chain_result)
    except Exception as e:
        print(f"Error running chain: {e}")
        chain_output = f"Chain failed: {e}"
        chain_meta = {}

    chain_time = (datetime.now() - chain_start).total_seconds()
    chain_tokens = chain_meta.get('total_tokens', 0)

    print(f"  ✅ Chain completed in {chain_time:.1f}s, {chain_tokens} tokens")

    # Step 2: Generate baseline mega-prompt
    if baseline_prompt is None:
        baseline_prompt = _generate_baseline_prompt(topic, chain_function.__name__)

    print(f"\n📄 Running baseline mega-prompt...")
    baseline_start = datetime.now()

    baseline_result, _, baseline_usage, _ = MinimalChainable.run(
        context={},
        model=model_info,
        callable=prompt,
        return_trace=True,
        prompts=[baseline_prompt]
    )

    baseline_output = baseline_result[0]
    baseline_time = (datetime.now() - baseline_start).total_seconds()
    baseline_tokens = sum(baseline_usage)

    print(f"  ✅ Baseline completed in {baseline_time:.1f}s, {baseline_tokens} tokens")

    # Step 3: Measure both outputs
    print(f"\n📊 Measuring outputs...")

    scores = _measure_outputs(
        topic=topic,
        chain_output=chain_output,
        baseline_output=baseline_output,
        model_info=model_info
    )

    # Step 4: Compile results
    comparison = {
        "topic": topic,
        "chain_approach": chain_function.__name__,
        "outputs": {
            "chain": chain_output[:1000] + "..." if len(chain_output) > 1000 else chain_output,
            "baseline": baseline_output[:1000] + "..." if len(str(baseline_output)) > 1000 else baseline_output
        },
        "scores": scores,
        "performance": {
            "chain": {
                "time_seconds": chain_time,
                "tokens": chain_tokens,
                "tokens_per_second": chain_tokens / chain_time if chain_time > 0 else 0
            },
            "baseline": {
                "time_seconds": baseline_time,
                "tokens": baseline_tokens,
                "tokens_per_second": baseline_tokens / baseline_time if baseline_time > 0 else 0
            }
        },
        "winner": _determine_winner(scores),
        "analysis": _analyze_results(scores)
    }

    metadata = {
        "topic": topic,
        "chain_function": chain_function.__name__,
        "timestamp": datetime.now().isoformat(),
        "chain_tokens": chain_tokens,
        "baseline_tokens": baseline_tokens,
        "winner": comparison["winner"]
    }

    return comparison, metadata


def _generate_baseline_prompt(topic: str, chain_name: str) -> str:
    """Generate a mega-prompt that asks for everything the chain does."""

    # Map chain names to their comprehensive requirements
    prompts = {
        "concept_simplifier": f"""You are an expert educator. Teach {topic} to a 5th grader.

Provide:
1. Break down the core components
2. Create powerful analogies for each component
3. Generate concrete examples
4. Synthesize everything into a clear explanation

Make it comprehensive, clear, and accessible.""",

        "subject_connector": f"""You are an expert at finding connections between subjects.

Analyze the deep structural connections between the subjects in: {topic}

Provide:
1. Deep analysis of each subject
2. Structural patterns and principles
3. Surprising connections between them
4. A practical project that leverages both

Be thorough and insightful.""",

        "scientific_method": f"""Apply the scientific method to evaluate this hypothesis: {topic}

Provide:
1. Observations that led to this hypothesis
2. Testable predictions
3. Experimental design
4. Analysis of expected results
5. Conclusion with confidence level

Be rigorous and scientific.""",

        "design_thinking": f"""Apply design thinking to solve: {topic}

Provide:
1. Empathy (understand the user)
2. Define (frame the problem)
3. Ideate (generate solutions)
4. Prototype (detailed design)
5. Test (evaluate the solution)

Be comprehensive and user-centered.""",

        "default": f"""Provide a comprehensive, insightful analysis of: {topic}

Be thorough, nuanced, and detailed. Cover all important aspects."""
    }

    return prompts.get(chain_name, prompts["default"])


def _measure_outputs(
    topic: str,
    chain_output: str,
    baseline_output: str,
    model_info: Tuple
) -> Dict[str, Any]:
    """
    Use AI to measure outputs across multiple dimensions.

    Dimensions:
    - Novelty: Unique insights not obvious from the topic
    - Depth: Level of detail and sophistication
    - Coherence: Logical flow and structure
    - Pedagogical: Would a learner understand?
    - Token efficiency: Insights per token
    """

    measurement_prompt = f"""You are evaluating two approaches to explaining a topic.

Topic: {topic}

APPROACH A (Chain):
{chain_output[:2000]}

APPROACH B (Baseline):
{str(baseline_output)[:2000]}

Evaluate both approaches across these dimensions (score 1-10):

1. NOVELTY: Unique insights that aren't obvious from the topic alone
   - Does it reveal non-obvious connections?
   - Does it create new understanding?

2. DEPTH: Level of detail and sophistication
   - How thorough is the analysis?
   - Does it go beyond surface-level?

3. COHERENCE: Logical flow and structure
   - Is it well-organized?
   - Does each part build on the previous?

4. PEDAGOGICAL EFFECTIVENESS: Would a learner understand?
   - Is it clear and accessible?
   - Are examples/analogies helpful?

5. ACTIONABILITY: Can someone DO something with this?
   - Are there concrete takeaways?
   - Is it practical?

Return as JSON:
{{
  "scores": {{
    "approach_a": {{
      "novelty": 1-10,
      "depth": 1-10,
      "coherence": 1-10,
      "pedagogical": 1-10,
      "actionability": 1-10
    }},
    "approach_b": {{
      "novelty": 1-10,
      "depth": 1-10,
      "coherence": 1-10,
      "pedagogical": 1-10,
      "actionability": 1-10
    }}
  }},
  "qualitative": {{
    "approach_a_strengths": ["strength 1", "strength 2", ...],
    "approach_a_weaknesses": ["weakness 1", ...],
    "approach_b_strengths": ["strength 1", ...],
    "approach_b_weaknesses": ["weakness 1", ...],
    "most_novel_insight_a": "The most unique insight from A",
    "most_novel_insight_b": "The most unique insight from B",
    "which_would_you_learn_from": "A/B/Both equally"
  }},
  "summary": "Which approach is better and why (2-3 sentences)"
}}"""

    result, _, _, _ = MinimalChainable.run(
        context={},
        model=model_info,
        callable=prompt,
        return_trace=False,
        prompts=[measurement_prompt]
    )

    scores = result[0] if isinstance(result[0], dict) else {}

    return scores


def _determine_winner(scores: Dict[str, Any]) -> str:
    """Determine which approach won based on scores."""
    if not scores or 'scores' not in scores:
        return "Inconclusive"

    a_scores = scores.get('scores', {}).get('approach_a', {})
    b_scores = scores.get('scores', {}).get('approach_b', {})

    a_total = sum(a_scores.values()) if a_scores else 0
    b_total = sum(b_scores.values()) if b_scores else 0

    if a_total > b_total + 3:  # Chain wins by clear margin
        return "Chain"
    elif b_total > a_total + 3:  # Baseline wins
        return "Baseline"
    else:
        return "Tie"


def _analyze_results(scores: Dict[str, Any]) -> str:
    """Generate analysis of the comparison."""
    if not scores or 'scores' not in scores:
        return "Unable to analyze - insufficient data"

    a_scores = scores.get('scores', {}).get('approach_a', {})
    b_scores = scores.get('scores', {}).get('approach_b', {})

    # Find where chain excelled
    chain_advantages = []
    for dimension, score in a_scores.items():
        if score > b_scores.get(dimension, 0) + 1:
            chain_advantages.append(f"{dimension} (+{score - b_scores.get(dimension, 0)})")

    baseline_advantages = []
    for dimension, score in b_scores.items():
        if score > a_scores.get(dimension, 0) + 1:
            baseline_advantages.append(f"{dimension} (+{score - a_scores.get(dimension, 0)})")

    analysis = f"Chain excels at: {', '.join(chain_advantages) if chain_advantages else 'none'}. "
    analysis += f"Baseline excels at: {', '.join(baseline_advantages) if baseline_advantages else 'none'}. "
    analysis += f"{scores.get('qualitative', {}).get('summary', '')}"

    return analysis


# ============================================================================
# BATCH MEASUREMENT ACROSS TOPICS
# ============================================================================

def batch_measure(
    topics: List[str],
    chain_function: Callable,
    **chain_kwargs
) -> Tuple[Dict[str, Any], List[Dict[str, Any]]]:
    """
    Run emergence measurement across multiple topics.

    This provides statistical significance by testing the chain approach
    on diverse topics.

    Args:
        topics: List of topics to test
        chain_function: The chain function to evaluate
        **chain_kwargs: Arguments to pass to chain function

    Returns:
        Tuple of (aggregate results, individual results list)
    """
    print(f"\n{'='*70}")
    print(f"BATCH EMERGENCE MEASUREMENT")
    print(f"Testing {chain_function.__name__} across {len(topics)} topics")
    print(f"{'='*70}")

    individual_results = []
    chain_wins = 0
    baseline_wins = 0
    ties = 0

    for i, topic in enumerate(topics, 1):
        print(f"\n[{i}/{len(topics)}] Testing: {topic}")
        comparison, metadata = measure_emergence(topic, chain_function, **chain_kwargs)

        individual_results.append({
            "topic": topic,
            "comparison": comparison,
            "metadata": metadata
        })

        if comparison["winner"] == "Chain":
            chain_wins += 1
        elif comparison["winner"] == "Baseline":
            baseline_wins += 1
        else:
            ties += 1

        print(f"  Result: {comparison['winner']} wins")

    # Aggregate statistics
    total = len(topics)
    chain_win_rate = (chain_wins / total) * 100 if total > 0 else 0

    aggregate = {
        "chain_function": chain_function.__name__,
        "topics_tested": total,
        "results": {
            "chain_wins": chain_wins,
            "baseline_wins": baseline_wins,
            "ties": ties,
            "chain_win_rate": f"{chain_win_rate:.1f}%"
        },
        "average_scores": _calculate_average_scores(individual_results),
        "conclusion": _generate_conclusion(chain_wins, baseline_wins, ties, total),
        "statistical_significance": _assess_significance(chain_wins, baseline_wins, total)
    }

    return aggregate, individual_results


def _calculate_average_scores(results: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Calculate average scores across all topics."""
    chain_scores = {'novelty': [], 'depth': [], 'coherence': [], 'pedagogical': [], 'actionability': []}
    baseline_scores = {'novelty': [], 'depth': [], 'coherence': [], 'pedagogical': [], 'actionability': []}

    for result in results:
        scores = result['comparison'].get('scores', {}).get('scores', {})
        a_scores = scores.get('approach_a', {})
        b_scores = scores.get('approach_b', {})

        for dimension in chain_scores.keys():
            if dimension in a_scores:
                chain_scores[dimension].append(a_scores[dimension])
            if dimension in b_scores:
                baseline_scores[dimension].append(b_scores[dimension])

    averages = {
        "chain": {dim: sum(vals) / len(vals) if vals else 0 for dim, vals in chain_scores.items()},
        "baseline": {dim: sum(vals) / len(vals) if vals else 0 for dim, vals in baseline_scores.items()}
    }

    return averages


def _generate_conclusion(chain_wins: int, baseline_wins: int, ties: int, total: int) -> str:
    """Generate conclusion from results."""
    if chain_wins > baseline_wins + ties:
        strength = "strong" if chain_wins > total * 0.7 else "moderate"
        return f"Chain approach shows {strength} superiority, winning {chain_wins}/{total} comparisons."
    elif baseline_wins > chain_wins + ties:
        return f"Baseline approach performs better, winning {baseline_wins}/{total} comparisons."
    else:
        return f"Results are mixed ({chain_wins} chain, {baseline_wins} baseline, {ties} ties). Further testing needed."


def _assess_significance(chain_wins: int, baseline_wins: int, total: int) -> str:
    """Assess statistical significance (simplified)."""
    if total < 5:
        return "Sample size too small for statistical significance"

    win_rate = chain_wins / total
    if win_rate >= 0.7:
        return "High confidence - chain consistently outperforms"
    elif win_rate >= 0.6:
        return "Moderate confidence - chain shows advantage"
    elif win_rate >= 0.5:
        return "Low confidence - results are close"
    else:
        return "Chain does not show advantage over baseline"


# ============================================================================
# REPORT GENERATION
# ============================================================================

def generate_report(
    aggregate: Dict[str, Any],
    individual_results: List[Dict[str, Any]],
    output_path: str = "output/emergence_report.md"
) -> str:
    """Generate a markdown report of the measurement results."""

    report = f"""# Emergence Measurement Report

**Chain Function:** {aggregate['chain_function']}
**Topics Tested:** {aggregate['topics_tested']}
**Date:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

---

## Executive Summary

{aggregate['conclusion']}

**Statistical Significance:** {aggregate['statistical_significance']}

---

## Overall Results

| Metric | Chain | Baseline | Winner |
|--------|-------|----------|--------|
| Wins | {aggregate['results']['chain_wins']} | {aggregate['results']['baseline_wins']} | {'Chain' if aggregate['results']['chain_wins'] > aggregate['results']['baseline_wins'] else 'Baseline'} |
| Win Rate | {aggregate['results']['chain_win_rate']} | {100 - float(aggregate['results']['chain_win_rate'].rstrip('%')):.1f}% | - |
| Ties | {aggregate['results']['ties']} | {aggregate['results']['ties']} | - |

---

## Average Scores by Dimension

"""

    avg_scores = aggregate['average_scores']
    for dimension in ['novelty', 'depth', 'coherence', 'pedagogical', 'actionability']:
        chain_score = avg_scores['chain'].get(dimension, 0)
        baseline_score = avg_scores['baseline'].get(dimension, 0)
        report += f"**{dimension.capitalize()}:** Chain {chain_score:.1f}/10 vs Baseline {baseline_score:.1f}/10\n"

    report += "\n---\n\n## Individual Topic Results\n\n"

    for result in individual_results:
        topic = result['topic']
        winner = result['comparison']['winner']
        report += f"### {topic}\n\n"
        report += f"**Winner:** {winner}\n\n"
        report += f"{result['comparison']['analysis']}\n\n"

    report += "\n---\n\n## Conclusion\n\n"
    report += aggregate['conclusion'] + "\n\n"
    report += f"Statistical confidence: {aggregate['statistical_significance']}\n"

    # Save report
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, 'w') as f:
        f.write(report)

    return output_path


# ============================================================================
# CONVENIENCE FUNCTIONS
# ============================================================================

def quick_test(topic: str, chain_function: Callable, **kwargs) -> None:
    """Quick test: measure one topic and print results."""
    comparison, metadata = measure_emergence(topic, chain_function, **kwargs)

    print(f"\n{'='*70}")
    print("QUICK TEST RESULTS")
    print(f"{'='*70}")
    print(f"\nTopic: {topic}")
    print(f"Winner: {comparison['winner']}")
    print(f"\nAnalysis: {comparison['analysis']}")
    print(f"\nScores:")

    scores = comparison['scores'].get('scores', {})
    a_scores = scores.get('approach_a', {})
    b_scores = scores.get('approach_b', {})

    for dim in ['novelty', 'depth', 'coherence', 'pedagogical', 'actionability']:
        print(f"  {dim.capitalize():15s}: Chain {a_scores.get(dim, 0)}/10  |  Baseline {b_scores.get(dim, 0)}/10")


if __name__ == "__main__":
    print("\nEmergence Measurement Tool")
    print("===========================")
    print("\nThis module scientifically measures whether prompt chains")
    print("unlock insights impossible from single mega-prompts.")
    print("\nRun demos/emergence_measurement_demo.py to see it in action!")
