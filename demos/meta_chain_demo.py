#!/usr/bin/env python3
"""
🧠 Meta-Chain Generator Demo

Shows chains that design other chains automatically.

This is the pinnacle of the framework:
- Layer 1: Prompts
- Layer 2: Chains
- Layer 3: Artifacts
- Layer 4: Tools
- Layer 5: Compositions
- Layer 6: Meta-Chains ← THIS DEMO

The system analyzes your goal and automatically designs
the optimal chain to achieve it.
"""

import os
import sys
import json

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from meta_chain_generator import MetaChainGenerator, quick_generate


def demo_1_explain_through_analogies():
    """
    Demo 1: Automatically design a chain to explain through analogies.
    """
    print("=" * 70)
    print("🧠 META-CHAIN DEMO #1: Explain Through Analogies")
    print("=" * 70)
    print()
    print("Goal: Teach recursion through powerful analogies")
    print()
    print("The meta-chain will:")
    print("  1. Analyze what's needed")
    print("  2. Design the optimal cognitive sequence")
    print("  3. Generate specific prompts")
    print("  4. Execute the designed chain")
    print()
    input("Press Enter to start...")
    print()

    # Let the meta-chain design and execute
    design, outputs = quick_generate(
        "Teach recursion through powerful analogies",
        topic="recursion"
    )

    print()
    print("=" * 70)
    print("📊 DESIGNED CHAIN")
    print("=" * 70)
    print()
    print(design.visualize())
    print()

    print("=" * 70)
    print("🎯 FINAL OUTPUT")
    print("=" * 70)
    print()
    if outputs:
        final_output = outputs[-1]
        if isinstance(final_output, dict):
            print(json.dumps(final_output, indent=2))
        else:
            print(final_output)
    print()


def demo_2_compare_concepts():
    """
    Demo 2: Automatically design a chain to compare concepts.
    """
    print("=" * 70)
    print("🧠 META-CHAIN DEMO #2: Compare Concepts")
    print("=" * 70)
    print()
    print("Goal: Compare machine learning to human learning")
    print()
    input("Press Enter to start...")
    print()

    generator = MetaChainGenerator()

    # Just design (don't execute yet)
    design = generator.design_chain(
        goal="Compare machine learning to human learning",
        context={"concept_a": "machine learning", "concept_b": "human learning"}
    )

    print()
    print("=" * 70)
    print("📋 DESIGNED CHAIN (Design Only)")
    print("=" * 70)
    print()
    print(design.visualize())
    print()
    print("Cognitive Moves Sequence:")
    for i, move in enumerate(design.cognitive_moves, 1):
        print(f"  {i}. {move}")
    print()
    print("Prompts:")
    for i, prompt in enumerate(design.prompts, 1):
        print(f"\n--- Prompt {i} ---")
        print(prompt[:200] + "..." if len(prompt) > 200 else prompt)
    print()

    choice = input("Execute this designed chain? (y/n): ").strip().lower()
    if choice == 'y':
        print()
        outputs, prompts, usage = generator.execute_chain(design)

        print()
        print("=" * 70)
        print("🎯 EXECUTION RESULT")
        print("=" * 70)
        print()
        if outputs:
            final = outputs[-1]
            if isinstance(final, dict):
                print(json.dumps(final, indent=2))
            else:
                print(final)
        print()


def demo_3_custom_goal():
    """
    Demo 3: User provides their own goal.
    """
    print("=" * 70)
    print("🧠 META-CHAIN DEMO #3: Your Custom Goal")
    print("=" * 70)
    print()
    print("Describe what you want to learn or understand.")
    print()
    print("Examples:")
    print("  - 'Explain blockchain through historical analogies'")
    print("  - 'Break down quantum mechanics into teachable parts'")
    print("  - 'Compare functional and object-oriented programming'")
    print("  - 'Trace how AI ethics has evolved'")
    print()

    goal = input("Your goal: ").strip()

    if not goal:
        print("No goal provided. Exiting.")
        return

    print()
    print(f"Designing chain for: {goal}")
    print()

    generator = MetaChainGenerator()
    design = generator.design_chain(goal)

    print()
    print("=" * 70)
    print("📋 YOUR CUSTOM CHAIN")
    print("=" * 70)
    print()
    print(design.visualize())
    print()

    choice = input("Execute this chain? (y/n): ").strip().lower()
    if choice == 'y':
        print()
        outputs, prompts, usage = generator.execute_chain(design)

        print()
        print("=" * 70)
        print("🎯 RESULT")
        print("=" * 70)
        print()
        for i, output in enumerate(outputs, 1):
            print(f"\n--- Step {i} Output ---")
            if isinstance(output, dict):
                print(json.dumps(output, indent=2))
            else:
                print(output)
        print()


def demo_4_constrained_design():
    """
    Demo 4: Design with constraints.
    """
    print("=" * 70)
    print("🧠 META-CHAIN DEMO #4: Constrained Design")
    print("=" * 70)
    print()
    print("Goal: Explain neural networks")
    print("Constraint: Must use only 2 cognitive moves")
    print()
    input("Press Enter to start...")
    print()

    generator = MetaChainGenerator()

    design = generator.design_chain(
        goal="Explain neural networks to a beginner",
        context={"topic": "neural networks"},
        constraints=["Maximum 2 cognitive moves", "Must include analogies"]
    )

    print()
    print("=" * 70)
    print("📋 CONSTRAINED CHAIN")
    print("=" * 70)
    print()
    print(design.visualize())
    print()
    print(f"Constraint satisfied: {len(design.cognitive_moves)} moves")
    print()


def demo_5_meta_reflection():
    """
    Demo 5: Meta-chain reflects on its own design.
    """
    print("=" * 70)
    print("🧠 META-CHAIN DEMO #5: Meta-Reflection")
    print("=" * 70)
    print()
    print("The meta-chain designs a chain, then critiques its own design.")
    print()
    input("Press Enter to start...")
    print()

    generator = MetaChainGenerator()

    # Design a chain
    design1 = generator.design_chain(
        goal="Teach calculus basics",
        context={"topic": "calculus"}
    )

    print()
    print("=" * 70)
    print("📋 INITIAL DESIGN")
    print("=" * 70)
    print()
    print(design1.visualize())
    print()

    # Now ask the meta-chain to critique its own design
    print("Now asking meta-chain to critique its own design...")
    print()

    design2 = generator.design_chain(
        goal=f"Improve this chain design: {design1.cognitive_moves}",
        context={
            "original_design": json.dumps(design1.to_dict()),
            "goal": "Teach calculus basics"
        }
    )

    print()
    print("=" * 70)
    print("📋 IMPROVED DESIGN")
    print("=" * 70)
    print()
    print(design2.visualize())
    print()
    print("Comparison:")
    print(f"  Original: {design1.cognitive_moves}")
    print(f"  Improved: {design2.cognitive_moves}")
    print()


if __name__ == "__main__":
    print()
    print("🧠 META-CHAIN GENERATOR DEMOS")
    print()
    print("This shows chains that design other chains.")
    print()
    print("Choose a demo:")
    print("  1. Explain through analogies (full execution)")
    print("  2. Compare concepts (design + optional execution)")
    print("  3. Your custom goal (design + optional execution)")
    print("  4. Constrained design (design only)")
    print("  5. Meta-reflection (meta-chain critiques itself)")
    print()

    choice = input("Enter 1-5: ").strip()

    print()

    if choice == "1":
        demo_1_explain_through_analogies()
    elif choice == "2":
        demo_2_compare_concepts()
    elif choice == "3":
        demo_3_custom_goal()
    elif choice == "4":
        demo_4_constrained_design()
    elif choice == "5":
        demo_5_meta_reflection()
    else:
        print("Invalid choice. Exiting.")

    print()
    print("=" * 70)
    print("✅ META-CHAIN DEMO COMPLETE")
    print("=" * 70)
    print()
    print("What just happened:")
    print("  • The meta-chain ANALYZED your goal")
    print("  • It SELECTED optimal cognitive moves")
    print("  • It GENERATED specific prompts")
    print("  • It EXECUTED the designed chain (optional)")
    print()
    print("This is Layer 6: Chains that design chains.")
    print("The system is now self-improving.")
    print()
