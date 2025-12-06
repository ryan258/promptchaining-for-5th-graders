"""
Adversarial Chains Demo
=======================

Demonstrates adversarial reasoning patterns that use conflict to reveal truth:
1. Red Team vs Blue Team
2. Dialectical Synthesis (Thesis → Antithesis → Synthesis)
3. Adversarial Socratic Dialogue

These patterns are impossible with single prompts - they require the back-and-forth
of prompt chaining to create genuine dialectical tension.
"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from adversarial_chains import (
    red_vs_blue,
    dialectical,
    adversarial_socratic,
    list_patterns
)
import json


def demo_red_vs_blue():
    """Demo: Red Team attacks, Blue Team defends."""
    print("\n" + "=" * 70)
    print("DEMO 1: RED TEAM vs BLUE TEAM")
    print("=" * 70)
    print("\nTopic: MS Treatment Strategies")
    print("Position: MS patients should prioritize high-efficacy DMTs from diagnosis")
    print("\nRed Team will attack this position...")
    print("Blue Team will defend...")
    print("Judge will evaluate the debate...")
    print()

    result, metadata = red_vs_blue(
        topic="Multiple Sclerosis treatment strategies",
        position_to_defend="MS patients should start high-efficacy DMTs immediately after diagnosis",
        rounds=2,  # 2 rounds for demo speed
        judge_criteria=[
            "Strength of evidence",
            "Logical coherence",
            "Practical considerations",
            "Patient welfare"
        ]
    )

    print("\n⚔️  DEBATE RESULTS:")
    print(f"\nOpening Position (Blue Team):")
    print(f"  {result['opening'].get('thesis', 'N/A')}")

    for round_data in result['rounds']:
        print(f"\n--- Round {round_data['round']} ---")
        print(f"\n🔴 Red Team Attack:")
        attacks = round_data['red_attack'].get('attacks', [])
        if attacks:
            print(f"  Strongest objection: {round_data['red_attack'].get('strongest_objection', 'N/A')}")

        print(f"\n🔵 Blue Team Defense:")
        counters = round_data['blue_defense'].get('counters', [])
        if counters:
            print(f"  Strengthened position: {round_data['blue_defense'].get('strengthened_position', 'N/A')}")

    print(f"\n⚖️  JUDGE'S VERDICT:")
    print(f"  Blue Team strength: {result['judgment'].get('blue_team_strength', 'N/A')}/10")
    print(f"  Red Team strength: {result['judgment'].get('red_team_strength', 'N/A')}/10")
    print(f"  Winner: {metadata['winner']}")
    print(f"  Verdict: {result['judgment'].get('verdict', 'N/A')}")
    print(f"\n  Nuanced conclusion: {result['judgment'].get('nuanced_conclusion', 'N/A')[:200]}...")

    print(f"\n✅ Red vs Blue debate completed in {metadata['rounds']} rounds")
    print(f"📊 Scores - Blue: {metadata['blue_score']}, Red: {metadata['red_score']}")


def demo_dialectical():
    """Demo: Thesis → Antithesis → Synthesis."""
    print("\n" + "=" * 70)
    print("DEMO 2: DIALECTICAL SYNTHESIS")
    print("=" * 70)
    print("\nThesis: MS patients should focus on symptom management")
    print("\nApplying Hegelian dialectic...")
    print("  Thesis → Antithesis → Synthesis")
    print()

    result, metadata = dialectical(
        thesis="MS patients should prioritize symptom management over disease modification",
        context="Approaches to MS treatment and patient quality of life",
        domain="Medical philosophy"
    )

    print("\n📖 DIALECTICAL PROGRESSION:")

    print(f"\n1️⃣ THESIS:")
    print(f"  Statement: {result['thesis'].get('thesis_statement', 'N/A')}")
    print(f"  Key assumptions: {result['thesis'].get('assumptions', [])[:2]}")
    print(f"  Implications: {result['thesis'].get('implications', 'N/A')[:150]}...")

    print(f"\n2️⃣ ANTITHESIS (What the thesis excludes):")
    print(f"  Statement: {result['antithesis'].get('antithesis_statement', 'N/A')}")
    print(f"  Thesis ignores: {result['antithesis'].get('what_thesis_ignores', [])[:2]}")
    print(f"  Who is marginalized: {result['antithesis'].get('who_is_marginalized', 'N/A')}")

    print(f"\n3️⃣ SYNTHESIS (Transcending the opposition):")
    print(f"  Statement: {result['synthesis'].get('synthesis_statement', 'N/A')}")
    print(f"  How it transcends: {result['synthesis'].get('how_it_transcends', 'N/A')[:200]}...")
    print(f"  Emergent insight: {result['synthesis'].get('emergent_insight', 'N/A')[:200]}...")

    print(f"\n🧪 EVALUATION:")
    print(f"  Resolves contradiction: {result['evaluation'].get('resolves_contradiction', 'N/A')}")
    print(f"  Synthesis quality: {metadata['synthesis_quality']}")
    print(f"  Avoids mere compromise: {result['evaluation'].get('avoids_compromise', 'N/A')[:150]}...")

    print(f"\n✅ Dialectical synthesis completed")
    print(f"💡 New understanding emerged that transcends both original positions")


def demo_adversarial_socratic():
    """Demo: Adversarial Socratic questioning."""
    print("\n" + "=" * 70)
    print("DEMO 3: ADVERSARIAL SOCRATIC DIALOGUE")
    print("=" * 70)
    print("\nClaim: AI assistants will solve the MS medication adherence problem")
    print("\nSubjecting claim to aggressive Socratic questioning...")
    print()

    result, metadata = adversarial_socratic(
        claim="AI assistants will solve the MS medication adherence problem",
        depth=3,  # 3 rounds for demo
        aggressive=True
    )

    print("\n⚡ ADVERSARIAL DIALOGUE:")

    print(f"\n📢 ORIGINAL CLAIM:")
    print(f"  {result['original_claim'].get('claim', 'N/A')}")
    print(f"  Initial confidence: {result['original_claim'].get('confidence', 'N/A')}")

    for round_data in result['rounds']:
        print(f"\n--- Round {round_data['round']} ---")

        print(f"\n❓ Adversarial Challenge:")
        print(f"  Target: {round_data['challenge'].get('target_weakness', 'N/A')}")
        print(f"  Question: {round_data['challenge'].get('question', 'N/A')}")

        print(f"\n🛡️  Defense:")
        print(f"  Type: {round_data['defense'].get('response_type', 'N/A')}")
        print(f"  Response: {round_data['defense'].get('response', 'N/A')[:200]}...")
        print(f"  Confidence now: {round_data['defense'].get('confidence_now', 'N/A')}")
        print(f"  Learned: {round_data['defense'].get('what_you_learned', 'N/A')[:150]}...")

    print(f"\n🏁 FINAL VERDICT:")
    print(f"  Claim survived: {metadata['survived']}")
    print(f"  Credibility impact: {metadata['credibility_impact']}")
    print(f"  Refined claim: {result['verdict'].get('refined_claim', 'N/A')}")
    print(f"  Remaining vulnerabilities: {result['verdict'].get('remaining_vulnerabilities', [])[:2]}")
    print(f"  Confidence verdict: {result['verdict'].get('confidence_verdict', 'N/A')[:200]}...")

    print(f"\n✅ Adversarial Socratic dialogue completed in {metadata['rounds']} rounds")


def demo_comparison():
    """Show the difference between cooperative and adversarial Socratic methods."""
    print("\n" + "=" * 70)
    print("BONUS: COOPERATIVE vs ADVERSARIAL SOCRATIC METHOD")
    print("=" * 70)
    print("\nKey Differences:")
    print("\nCOOPERATIVE (from natural_reasoning.py):")
    print("  • Teacher guides student to deeper understanding")
    print("  • Questions reveal nuances and refine thinking")
    print("  • Goal: Improve the student's reasoning")
    print("  • Tone: Supportive exploration")

    print("\nADVERSARIAL (from adversarial_chains.py):")
    print("  • Questioner tries to demolish the claim")
    print("  • Questions exploit weaknesses and contradictions")
    print("  • Goal: Stress-test the claim's validity")
    print("  • Tone: Aggressive intellectual combat")

    print("\nWhen to use each:")
    print("  • Cooperative → Learning, teaching, personal growth")
    print("  • Adversarial → Testing claims, finding flaws, intellectual rigor")


def run_all_demos():
    """Run all adversarial reasoning pattern demos."""
    print("\n" + "=" * 70)
    print("ADVERSARIAL CHAINS - COMPLETE DEMO")
    print("=" * 70)
    print("\nThese patterns use CONFLICT to reveal truth.")
    print("They're impossible with single prompts - they require the")
    print("back-and-forth dialectical tension that only chains enable.")

    # Show available patterns
    list_patterns()

    # Run each demo
    demos = [
        ("Red Team vs Blue Team", demo_red_vs_blue),
        ("Dialectical Synthesis", demo_dialectical),
        ("Adversarial Socratic", demo_adversarial_socratic),
        ("Comparison: Cooperative vs Adversarial", demo_comparison)
    ]

    for i, (name, demo_func) in enumerate(demos, 1):
        input(f"\n\n[Press Enter to run Demo {i}/{len(demos)}: {name}]")
        demo_func()

    print("\n" + "=" * 70)
    print("🎉 ALL ADVERSARIAL DEMOS COMPLETED!")
    print("=" * 70)
    print("\nWhat makes these patterns unique:")
    print("  ⚔️  Genuine dialectical tension (not possible in single prompts)")
    print("  🔥 Adversarial pressure reveals hidden weaknesses")
    print("  🧠 Produces nuanced understanding through conflict")
    print("  ⚡ Transcends binary thinking via synthesis")

    print("\nPerfect for:")
    print("  • Blog content on controversial topics")
    print("  • Ethical debates and policy analysis")
    print("  • Stress-testing business strategies")
    print("  • Philosophical exploration")
    print("  • Red-teaming ideas before implementation")

    print("\nLogs have been saved to the logs/ directory.")
    print("=" * 70)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Adversarial Chains Demo")
    parser.add_argument(
        "--demo",
        type=int,
        choices=[1, 2, 3, 4],
        help="Run specific demo (1=Red vs Blue, 2=Dialectical, 3=Adversarial Socratic, 4=All)"
    )

    args = parser.parse_args()

    if args.demo == 1:
        demo_red_vs_blue()
    elif args.demo == 2:
        demo_dialectical()
    elif args.demo == 3:
        demo_adversarial_socratic()
    else:
        run_all_demos()
