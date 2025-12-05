#!/usr/bin/env python3
"""
Quick test of chain composer functionality.
"""

import sys
from chain_composer import ChainComposer, ChainStep, ChainRecipe
from artifact_store import ArtifactStore


def test_basic_composition():
    """Test basic chain composition."""
    print("Testing basic chain composition...")

    composer = ChainComposer()

    # Create a simple composition
    steps = [
        ChainStep(
            name="Test Chain",
            step_type="chain",
            topic="test_topic",
            prompts=[
                """You are a test assistant.

Say hello and introduce yourself.

Respond in JSON:
{
  "greeting": "Your greeting",
  "name": "Your name"
}"""
            ]
        )
    ]

    result = composer.compose(steps)

    assert len(result.steps_executed) == 1
    assert result.total_tokens > 0

    print("✅ Basic composition works")
    print()


def test_recipe_creation():
    """Test that recipes create valid steps."""
    print("Testing recipe creation...")

    # Test concept_comparison recipe
    steps = ChainRecipe.concept_comparison("Topic A", "Topic B")
    assert len(steps) == 4  # Analyze A, Analyze B, Connect, Synthesize
    assert steps[0].step_type == "tool"
    assert steps[-1].step_type == "synthesize"

    print("✅ Concept comparison recipe valid")

    # Test learning_curriculum recipe
    steps = ChainRecipe.learning_curriculum(["A", "B", "C"])
    assert len(steps) > 3  # At least 3 analyze + 2 connect + 1 synthesize
    assert steps[0].step_type == "tool"

    print("✅ Learning curriculum recipe valid")

    # Test progressive_depth recipe
    steps = ChainRecipe.progressive_depth("Test Topic")
    assert len(steps) >= 4  # At least 4 levels
    assert steps[0].step_type == "chain"

    print("✅ Progressive depth recipe valid")
    print()


def test_artifact_flow():
    """Test that artifacts flow between steps."""
    print("Testing artifact flow...")

    store = ArtifactStore(base_dir="/tmp/test_composer_artifacts")
    composer = ChainComposer(artifact_store=store)

    # Step 1: Create an artifact
    steps = [
        ChainStep(
            name="Create data",
            step_type="chain",
            topic="source_topic",
            prompts=[
                """Create a simple data structure.

Respond in JSON:
{
  "data": ["item1", "item2", "item3"]
}"""
            ]
        ),
        ChainStep(
            name="Use data",
            step_type="chain",
            topic="consumer_topic",
            prompts=[
                """You have access to this data: {{artifact:source_topic:step_1}}

Count how many items are in the data.

Respond in JSON:
{
  "count": <number>
}"""
            ]
        )
    ]

    result = composer.compose(steps)

    # Check that both steps executed
    assert len(result.steps_executed) == 2

    # Check that second step got the artifact
    consumer_artifact = store.get("consumer_topic", "step_1")
    assert consumer_artifact is not None

    print("✅ Artifacts flow between steps")
    print()


if __name__ == "__main__":
    print("=" * 70)
    print("🧪 CHAIN COMPOSER TEST SUITE")
    print("=" * 70)
    print()

    try:
        test_basic_composition()
        test_recipe_creation()
        test_artifact_flow()

        print("=" * 70)
        print("✅ ALL CHAIN COMPOSER TESTS PASSED!")
        print("=" * 70)
        print()
        print("Chain composer is ready to use.")
        print()
        print("Try running:")
        print("  python demos/curriculum_builder_demo.py")
        print()

    except AssertionError as e:
        print()
        print("=" * 70)
        print("❌ TEST FAILED")
        print("=" * 70)
        print(f"Error: {e}")
        sys.exit(1)

    except Exception as e:
        print()
        print("=" * 70)
        print("❌ UNEXPECTED ERROR")
        print("=" * 70)
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
