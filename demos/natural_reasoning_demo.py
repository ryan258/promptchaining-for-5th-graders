"""
Natural Reasoning Patterns Demo
================================

Demonstrates the 5 expert reasoning patterns:
1. Scientific Method
2. Socratic Dialogue
3. Design Thinking
4. Judicial Reasoning
5. Root Cause Analysis (5 Whys)

Each pattern formalizes centuries of human expertise in reasoning.
"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from natural_reasoning import (
    scientific_method,
    socratic_dialogue,
    design_thinking,
    judicial_reasoning,
    five_whys,
    list_patterns
)
import json


def demo_scientific_method():
    """Demo: Apply scientific method to an MS-related hypothesis."""
    print("\n" + "=" * 70)
    print("DEMO 1: SCIENTIFIC METHOD")
    print("=" * 70)
    print("\nHypothesis: Regular exercise improves MS fatigue management")
    print("\nApplying the scientific method...\n")

    result, metadata = scientific_method(
        hypothesis="Regular exercise improves MS fatigue management",
        context="Multiple sclerosis patients often experience chronic fatigue",
        evidence_sources=[
            "Studies show exercise improves mitochondrial function",
            "MS patients report both fatigue and exercise intolerance",
            "Some MS patients report feeling better after exercise"
        ]
    )

    print("\n📊 RESULTS:")
    print(f"Verdict: {metadata['verdict']}")
    print(f"\nObservations: {json.dumps(result['observations'], indent=2)}")
    print(f"\nConclusion: {json.dumps(result['conclusion'], indent=2)}")
    print(f"\n✅ Scientific method completed in {metadata['steps_completed']} steps")
    print(f"📝 Detailed log saved to logs/")


def demo_socratic_dialogue():
    """Demo: Use Socratic method to examine a belief."""
    print("\n" + "=" * 70)
    print("DEMO 2: SOCRATIC DIALOGUE")
    print("=" * 70)
    print("\nBelief: People with MS should always use high-efficacy DMTs")
    print("\nEngaging Socratic dialogue...\n")

    result, metadata = socratic_dialogue(
        belief="People with MS should always use high-efficacy DMTs",
        teacher_persona="Neurologist",
        depth=3  # 3 rounds of questioning
    )

    print("\n💬 DIALOGUE:")
    print(f"Original belief: {result['initial_belief'].get('belief_statement', 'N/A')}")

    for round_data in result['rounds']:
        print(f"\n--- Round {round_data['round']} ---")
        print(f"Teacher: {round_data['question'].get('question', 'N/A')}")
        print(f"Student: {round_data['answer'].get('answer', 'N/A')}")
        print(f"Insight: {round_data['answer'].get('new_insight', 'N/A')}")

    print(f"\n🎯 SYNTHESIS:")
    print(f"Refined belief: {result['synthesis'].get('refined_belief', 'N/A')}")
    print(f"Confidence changed: {metadata['belief_changed']}")
    print(f"\n✅ Socratic dialogue completed in {metadata['rounds']} rounds")


def demo_design_thinking():
    """Demo: Apply design thinking to solve a problem."""
    print("\n" + "=" * 70)
    print("DEMO 3: DESIGN THINKING")
    print("=" * 70)
    print("\nProblem: MS patients struggle to track daily symptoms")
    print("\nApplying design thinking methodology...\n")

    result, metadata = design_thinking(
        problem="MS patients struggle to track daily symptoms",
        target_user="Person with MS experiencing brain fog",
        constraints=["Low energy", "Cognitive limitations", "Variable symptoms"]
    )

    print("\n🎨 DESIGN PROCESS:")
    print(f"\n1. EMPATHIZE: {json.dumps(result['empathize'].get('pain_points', []), indent=2)}")
    print(f"\n2. DEFINE: {result['define'].get('problem_statement', 'N/A')}")
    print(f"\n3. IDEATE: {len(result['ideate'].get('ideas', []))} ideas generated")
    print(f"   Top ideas: {result['ideate'].get('most_promising', [])}")
    print(f"\n4. PROTOTYPE: {result['prototype'].get('chosen_idea', 'N/A')}")
    print(f"   How it works: {result['prototype'].get('how_it_works', 'N/A')[:200]}...")
    print(f"\n5. TEST: {result['test'].get('overall_assessment', 'N/A')} solution")
    print(f"   Next iteration: {result['test'].get('next_iteration', 'N/A')}")
    print(f"\n✅ Design thinking completed")


def demo_judicial_reasoning():
    """Demo: Apply judicial reasoning to an ethical case."""
    print("\n" + "=" * 70)
    print("DEMO 4: JUDICIAL REASONING")
    print("=" * 70)
    print("\nCase: Should employers be required to accommodate MS-related fatigue?")
    print("\nApplying judicial reasoning...\n")

    result, metadata = judicial_reasoning(
        case="Should employers be required to accommodate MS-related fatigue with flexible schedules?",
        relevant_principles=[
            "ADA (Americans with Disabilities Act)",
            "Reasonable accommodation",
            "Undue hardship standard",
            "Equal opportunity"
        ],
        precedents=[
            "ADA requires accommodation unless it causes undue hardship",
            "Flexible schedules have been upheld as reasonable accommodations"
        ]
    )

    print("\n⚖️  JUDICIAL ANALYSIS:")
    print(f"\nFacts: {json.dumps(result['facts'].get('undisputed_facts', []), indent=2)}")
    print(f"\nPrinciples: {json.dumps(result['principles'].get('principles', [])[:2], indent=2)}")
    print(f"\nArguments for Position A: {result['arguments'].get('position_A', {}).get('strongest_point', 'N/A')}")
    print(f"\nArguments for Position B: {result['arguments'].get('position_B', {}).get('strongest_point', 'N/A')}")
    print(f"\n📜 RULING: {result['ruling'].get('ruling', 'N/A')}")
    print(f"\nReasoning: {result['ruling'].get('core_reasoning', 'N/A')}")
    print(f"Confidence: {result['ruling'].get('confidence', 'N/A')}")
    print(f"\n✅ Judicial reasoning completed")


def demo_five_whys():
    """Demo: Use 5 Whys to find root cause."""
    print("\n" + "=" * 70)
    print("DEMO 5: ROOT CAUSE ANALYSIS (5 WHYS)")
    print("=" * 70)
    print("\nProblem: I missed my medication dose today")
    print("\nDigging to find root cause...\n")

    result, metadata = five_whys(
        problem="I missed my medication dose today",
        depth=5,
        context="Person with MS taking daily disease-modifying therapy"
    )

    print("\n🔍 WHY CHAIN:")
    print(f"Problem: {result['problem'].get('problem_statement', 'N/A')}")

    for i, why in enumerate(result['whys'], 1):
        print(f"\nWhy #{i}: {why.get('question', 'N/A')}")
        print(f"  → {why.get('cause', 'N/A')}")

    print(f"\n🎯 ROOT CAUSE: {result['synthesis'].get('root_cause', 'N/A')}")
    print(f"\nWhy this is the root: {result['synthesis'].get('why_this_is_root', 'N/A')}")
    print(f"\n💡 SYSTEMIC SOLUTIONS:")
    for solution in result['synthesis'].get('systemic_solutions', []):
        print(f"  • {solution}")
    print(f"\n✅ Root cause analysis completed at depth {metadata['depth']}")


def run_all_demos():
    """Run all natural reasoning pattern demos."""
    print("\n" + "=" * 70)
    print("NATURAL REASONING PATTERNS - COMPLETE DEMO")
    print("=" * 70)
    print("\nThis demo shows 5 expert reasoning patterns that formalize")
    print("centuries of human expertise in systematic thinking.")
    print("\nEach pattern can be applied to any domain to unlock deeper insights.")

    # Show available patterns
    list_patterns()

    # Run each demo
    demos = [
        demo_scientific_method,
        demo_socratic_dialogue,
        demo_design_thinking,
        demo_judicial_reasoning,
        demo_five_whys
    ]

    for i, demo_func in enumerate(demos, 1):
        input(f"\n\n[Press Enter to run Demo {i}/{len(demos)}]")
        demo_func()

    print("\n" + "=" * 70)
    print("🎉 ALL DEMOS COMPLETED!")
    print("=" * 70)
    print("\nThese reasoning patterns can now be used for:")
    print("  • Blog content on complex topics")
    print("  • Problem-solving and decision-making")
    print("  • Teaching how experts think")
    print("  • Exploring controversial or nuanced issues")
    print("\nLogs have been saved to the logs/ directory.")
    print("=" * 70)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Natural Reasoning Patterns Demo")
    parser.add_argument(
        "--demo",
        type=int,
        choices=[1, 2, 3, 4, 5, 6],
        help="Run specific demo (1=Scientific, 2=Socratic, 3=Design, 4=Judicial, 5=Five Whys, 6=All)"
    )

    args = parser.parse_args()

    if args.demo == 1:
        demo_scientific_method()
    elif args.demo == 2:
        demo_socratic_dialogue()
    elif args.demo == 3:
        demo_design_thinking()
    elif args.demo == 4:
        demo_judicial_reasoning()
    elif args.demo == 5:
        demo_five_whys()
    else:
        run_all_demos()
