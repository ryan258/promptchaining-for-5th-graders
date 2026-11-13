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

from lib.enhancements.natural_reasoning import (
    scientific_method,
    socratic_dialogue,
    design_thinking,
    judicial_reasoning,
    five_whys,
    list_patterns
)
import json


def demo_scientific_method():
    """Draft a test plan using observations from a fictional intake log."""
    print("\n" + "=" * 70)
    print("DEMO 1: SCIENTIFIC METHOD")
    print("=" * 70)
    print("\nHypothesis: A structured intake form reduces follow-up for missing details.")
    print("\nThe model will propose tests for the fictional observations.\n")

    result, metadata = scientific_method(
        hypothesis="A structured intake form reduces follow-up for missing details",
        context="Fictional sample: 14 of 40 email requests and 5 of 20 form requests required follow-up. Teams chose their own channel. The log omits request type and urgency.",
    )

    print("\n📊 RESULTS:")
    print(f"Model assessment: {metadata['verdict']}")
    print(f"\nObservations: {json.dumps(result['observations'], indent=2)}")
    print(f"\nConclusion: {json.dumps(result['conclusion'], indent=2)}")
    print(f"\n✅ Scientific method completed in {metadata['steps_completed']} steps")
    print(f"📝 Detailed log saved to logs/")


def demo_socratic_dialogue():
    """Demo: Use Socratic method to examine a belief."""
    print("\n" + "=" * 70)
    print("DEMO 2: SOCRATIC DIALOGUE")
    print("=" * 70)
    print("\nBelief: A meeting is the fastest way to unblock work.")
    print("\nEngaging Socratic dialogue...\n")

    result, metadata = socratic_dialogue(
        belief="A meeting is always the fastest way to unblock work",
        teacher_persona="A facilitator asking for concrete examples and exceptions",
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
    print("\nProblem: People returning to drafts forget which file is current.")
    print("\nApplying design thinking methodology...\n")

    result, metadata = design_thinking(
        problem="Someone returning to a draft forgets which file is current",
        target_user="A writer who uses dictation and takes breaks throughout a session",
        constraints=["Use the existing folder", "Minimize typing", "Make the next action easy to find"]
    )

    print("\n🎨 DESIGN PROCESS:")
    print(f"\n1. EMPATHIZE: {json.dumps(result['empathize'].get('pain_points', []), indent=2)}")
    print(f"\n2. DEFINE: {result['define'].get('problem_statement', 'N/A')}")
    print(f"\n3. IDEATE: {len(result['ideate'].get('ideas', []))} ideas generated")
    print(f"   Top ideas: {result['ideate'].get('most_promising', [])}")
    print(f"\n4. PROTOTYPE: {result['prototype'].get('chosen_idea', 'N/A')}")
    print(f"   How it works: {result['prototype'].get('how_it_works', 'N/A')[:200]}...")
    print(f"\n5. PROPOSED TEST: {result['test'].get('overall_assessment', 'N/A')}")
    print(f"   Next iteration: {result['test'].get('next_iteration', 'N/A')}")
    print(f"\n✅ Design thinking completed")


def demo_judicial_reasoning():
    """Demo: Apply judicial reasoning to an ethical case."""
    print("\n" + "=" * 70)
    print("DEMO 4: JUDICIAL REASONING")
    print("=" * 70)
    print("\nFictional case: Does an incident handoff comply with an internal policy?")
    print("\nApplying judicial reasoning...\n")

    result, metadata = judicial_reasoning(
        case="An outgoing support engineer posts an active priority incident in the team channel and leaves without acknowledgement. Did the ownership transfer under the fictional policy?",
        relevant_principles=[
            "Fictional support policy: ownership transfers only when the incoming engineer acknowledges",
            "If no acknowledgement arrives after five minutes, page the duty manager",
        ],
    )

    print("\n⚖️  JUDICIAL ANALYSIS:")
    print(f"\nFacts: {json.dumps(result['facts'].get('undisputed_facts', []), indent=2)}")
    print(f"\nPrinciples: {json.dumps(result['principles'].get('principles', [])[:2], indent=2)}")
    print(f"\nArguments for Position A: {result['arguments'].get('position_A', {}).get('strongest_point', 'N/A')}")
    print(f"\nArguments for Position B: {result['arguments'].get('position_B', {}).get('strongest_point', 'N/A')}")
    print(f"\nMODEL'S PROPOSED INTERPRETATION: {result['ruling'].get('ruling', 'N/A')}")
    print(f"\nReasoning: {result['ruling'].get('core_reasoning', 'N/A')}")
    print(f"Confidence: {result['ruling'].get('confidence', 'N/A')}")
    print(f"\n✅ Judicial reasoning completed")


def demo_five_whys():
    """Draft possible causes and propose a way to investigate them."""
    print("\n" + "=" * 70)
    print("DEMO 5: ROOT CAUSE ANALYSIS (5 WHYS)")
    print("=" * 70)
    print("\nProblem: A reviewer opened an out-of-date draft.")
    print("\nGenerating possible explanations to check.\n")

    result, metadata = five_whys(
        problem="A reviewer opened an out-of-date draft",
        depth=5,
        context="Fictional observations: two drafts share almost the same filename. The handoff message links one of them. The cause is undetermined."
    )

    print("\n🔍 WHY CHAIN:")
    print(f"Problem: {result['problem'].get('problem_statement', 'N/A')}")

    for i, why in enumerate(result['whys'], 1):
        print(f"\nWhy #{i}: {why.get('question', 'N/A')}")
        print(f"  → {why.get('cause', 'N/A')}")

    print(f"\nPOSSIBLE CAUSE: {result['synthesis'].get('root_cause', 'N/A')}")
    print(f"\nModel's reasoning: {result['synthesis'].get('why_this_is_root', 'N/A')}")
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

    parser.add_argument("--live", action="store_true", help="Send the selected provider requests.")
    args = parser.parse_args()
    limits = {1: 5, 2: 8, 3: 5, 4: 5, 5: 7, 6: 30}
    if args.demo is None or not args.live:
        parser.error("Choose --demo and pass --live for provider requests. For offline examples use ./verify_demos.sh.")
    print(f"Up to {limits[args.demo]} provider requests. Provider charges apply.")

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
