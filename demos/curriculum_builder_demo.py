#!/usr/bin/env python3
"""
📚 Curriculum Builder Demo

Shows the power of chain composition:
1. Analyze multiple related topics
2. Find connections between them
3. Build a complete learning curriculum

This demonstrates "chains of chains" - orchestrating complex workflows.
"""

import os
import sys
import json

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from chain_composer import ChainComposer, ChainStep, ChainRecipe


def curriculum_builder_demo():
    """
    Build a complete learning curriculum using chain composition.
    """
    print("=" * 70)
    print("📚 CURRICULUM BUILDER DEMO")
    print("=" * 70)
    print()
    print("This demo builds a complete learning curriculum by:")
    print("  1. Analyzing each topic individually")
    print("  2. Finding connections between topics")
    print("  3. Synthesizing into a structured learning path")
    print()
    print("This is IMPOSSIBLE with single prompts!")
    print()

    # Define the learning path
    topics = [
        "Python Basics",
        "Data Structures",
        "Algorithms"
    ]

    print(f"🎯 Goal: Build curriculum for {' → '.join(topics)}")
    print()
    input("Press Enter to start composition...")
    print()

    # Create composer
    composer = ChainComposer()

    # Use the learning_curriculum recipe
    steps = ChainRecipe.learning_curriculum(topics)

    print(f"📋 Composed {len(steps)} steps:")
    for i, step in enumerate(steps, 1):
        print(f"  {i}. {step.name}")
    print()
    input("Press Enter to execute...")
    print()

    # Execute the composition
    result = composer.compose(steps)

    # Show the final curriculum
    print()
    print("=" * 70)
    print("🎓 GENERATED CURRICULUM")
    print("=" * 70)
    print()

    # Get the curriculum artifact
    curriculum = composer.artifact_store.get("curriculum", "step_1")

    if curriculum and isinstance(curriculum, dict):
        weeks = curriculum.get("weeks", [])

        for week in weeks:
            print(f"📖 Week {week.get('week')}: {week.get('topic', 'N/A')}")
            print()

            objectives = week.get('objectives', [])
            if objectives:
                print("  Learning Objectives:")
                for obj in objectives:
                    print(f"    • {obj}")
                print()

            concepts = week.get('key_concepts', [])
            if concepts:
                print("  Key Concepts:")
                for concept in concepts:
                    print(f"    • {concept}")
                print()

            exercises = week.get('exercises', [])
            if exercises:
                print("  Practice Exercises:")
                for ex in exercises:
                    print(f"    • {ex}")
                print()

            print("-" * 70)
            print()
    else:
        print("Curriculum:")
        print(json.dumps(curriculum, indent=2) if curriculum else "Not available")
        print()

    # Show composition stats
    print("=" * 70)
    print("📊 COMPOSITION STATS")
    print("=" * 70)
    print()
    print(f"Total Steps Executed: {len(result.steps_executed)}")
    print(f"Total Artifacts Created: {len(result.final_artifacts)}")
    print(f"Total Tokens Used: {result.total_tokens}")
    print()

    print("Artifacts Created:")
    for key in sorted(result.final_artifacts.keys()):
        print(f"  • {key}")
    print()

    print("=" * 70)
    print("✅ CURRICULUM BUILDING COMPLETE")
    print("=" * 70)
    print()
    print("What just happened:")
    print("  1. Each topic was analyzed independently (concept_simplifier)")
    print("  2. Connections were found between adjacent topics (subject_connector)")
    print("  3. A custom chain synthesized everything into a curriculum")
    print()
    print("This is META-LEVEL composition:")
    print("  • Tools orchestrating tools")
    print("  • Artifacts flowing between chains")
    print("  • Complex workflows from simple building blocks")
    print()
    print(f"All artifacts saved to: {composer.artifact_store.base_dir}/")
    print()


def simple_comparison_demo():
    """
    Simpler demo: just compare two concepts.
    """
    print("=" * 70)
    print("⚡ QUICK COMPARISON DEMO")
    print("=" * 70)
    print()

    topic_a = "Lists"
    topic_b = "Dictionaries"

    print(f"Comparing: {topic_a} vs {topic_b}")
    print()

    composer = ChainComposer()

    # Use the concept_comparison recipe
    steps = ChainRecipe.concept_comparison(topic_a, topic_b)

    result = composer.compose(steps)

    print()
    print("=" * 70)
    print("✅ COMPARISON COMPLETE")
    print("=" * 70)
    print()
    print(result.visualize())


def progressive_depth_demo():
    """
    Demo: Explain topic at multiple levels.
    """
    print("=" * 70)
    print("📈 PROGRESSIVE DEPTH DEMO")
    print("=" * 70)
    print()

    topic = "Recursion"

    print(f"Explaining '{topic}' at 4 levels of depth")
    print()

    composer = ChainComposer()

    # Use the progressive_depth recipe
    steps = ChainRecipe.progressive_depth(topic)

    result = composer.compose(steps)

    print()
    print("=" * 70)
    print("🎓 MULTI-LEVEL EXPLANATIONS")
    print("=" * 70)
    print()

    # Show each level
    levels = ["5th_grader", "high_school_student", "college_student", "expert"]
    for level in levels:
        artifact = composer.artifact_store.get(f"{topic.lower()}_{level}", "step_1")
        if artifact:
            print(f"📚 {level.replace('_', ' ').title()}")
            print()
            if isinstance(artifact, dict):
                print(f"  {artifact.get('explanation', '')}")
                print()
                example = artifact.get('example')
                if example:
                    print(f"  Example: {example}")
                    print()
            print("-" * 70)
            print()

    # Show the progression analysis
    progression = composer.artifact_store.get(f"{topic.lower()}_progression", "step_1")
    if progression:
        print("🔬 Learning Science Analysis")
        print()
        if isinstance(progression, dict):
            print("Progression Patterns:")
            for pattern in progression.get('progression_patterns', []):
                print(f"  • {pattern}")
            print()

    print()
    print("=" * 70)
    print("✅ PROGRESSIVE DEPTH COMPLETE")
    print("=" * 70)


if __name__ == "__main__":
    # Choose which demo to run
    if len(sys.argv) > 1:
        demo_type = sys.argv[1]
    else:
        print("Choose demo:")
        print("  1. Full curriculum builder (3 topics → complete curriculum)")
        print("  2. Quick comparison (2 concepts)")
        print("  3. Progressive depth (1 topic, 4 levels)")
        print()
        choice = input("Enter 1, 2, or 3: ").strip()

        demo_type = {
            "1": "curriculum",
            "2": "comparison",
            "3": "depth"
        }.get(choice, "curriculum")

    print()

    if demo_type == "curriculum":
        curriculum_builder_demo()
    elif demo_type == "comparison":
        simple_comparison_demo()
    elif demo_type == "depth":
        progressive_depth_demo()
    else:
        print("Unknown demo type. Use: curriculum, comparison, or depth")
