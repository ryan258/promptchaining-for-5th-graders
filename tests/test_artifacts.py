#!/usr/bin/env python3
"""
Quick test to verify artifact system works correctly.
"""

import os
import sys
import json
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# Test basic artifact store functionality
from src.core.artifact_store import ArtifactStore, resolve_artifact_references


def test_artifact_store_basic():
    """Test basic save/retrieve operations."""
    print("Testing basic artifact store operations...")

    # Create a test store in /tmp
    store = ArtifactStore(base_dir="/tmp/test_artifacts")

    # Save some artifacts
    store.save(
        topic="Machine Learning",
        step_name="components",
        data={"components": ["Data", "Algorithm", "Training"]}
    )

    store.save(
        topic="Machine Learning",
        step_name="analogies",
        data={"analogies": ["Like teaching a child"]}
    )

    store.save(
        topic="Quantum Physics",
        step_name="components",
        data={"components": ["Superposition", "Entanglement"]}
    )

    # Test retrieval
    ml_components = store.get("Machine Learning", "components")
    assert ml_components == {"components": ["Data", "Algorithm", "Training"]}
    print("✅ Save/retrieve works")

    # Test query patterns
    all_ml = store.query("machine_learning:*")
    assert len(all_ml) == 2
    print("✅ Query patterns work")

    all_components = store.query("*:components")
    assert len(all_components) == 2
    print("✅ Wildcard queries work")

    # Test topics listing
    topics = store.list_topics()
    assert "machine_learning" in topics
    assert "quantum_physics" in topics
    print("✅ Topic listing works")

    # Test visualization
    viz = store.visualize()
    assert "machine_learning" in viz
    print("✅ Visualization works")

    print()


def test_artifact_references():
    """Test artifact reference resolution in prompts."""
    print("Testing artifact reference resolution...")

    store = ArtifactStore(base_dir="/tmp/test_artifacts")

    store.save(
        topic="AI",
        step_name="summary",
        data="Artificial Intelligence is machine learning"
    )

    store.save(
        topic="AI",
        step_name="details",
        data={"key": "value", "number": 42}
    )

    # Test simple reference
    prompt1 = "Explain this: {{artifact:ai:summary}}"
    resolved1, used1 = resolve_artifact_references(prompt1, store)
    assert "Artificial Intelligence is machine learning" in resolved1
    assert "ai:summary" in used1
    print("✅ Simple artifact reference works")

    # Test JSON artifact reference
    prompt2 = "Use this data: {{artifact:ai:details}}"
    resolved2, used2 = resolve_artifact_references(prompt2, store)
    assert '"key": "value"' in resolved2 or "'key': 'value'" in resolved2
    print("✅ JSON artifact reference works")

    # Test non-existent artifact
    prompt3 = "Find {{artifact:nonexistent:missing}}"
    resolved3, used3 = resolve_artifact_references(prompt3, store)
    assert "NOT FOUND" in resolved3
    print("✅ Missing artifact handling works")

    # Test multiple references
    prompt4 = "Compare {{artifact:ai:summary}} with {{artifact:ai:details}}"
    resolved4, used4 = resolve_artifact_references(prompt4, store)
    assert len(used4) == 2
    print("✅ Multiple artifact references work")

    print()


def test_persistence():
    """Test that artifacts persist to disk and reload."""
    print("Testing artifact persistence...")

    # Create store and save data
    store1 = ArtifactStore(base_dir="/tmp/test_artifacts_persist")
    store1.save(
        topic="Test Topic",
        step_name="test_step",
        data={"persisted": True}
    )

    # Create a NEW store pointing to same directory
    store2 = ArtifactStore(base_dir="/tmp/test_artifacts_persist")

    # Should auto-load from disk
    loaded = store2.get("Test Topic", "test_step")
    assert loaded == {"persisted": True}
    print("✅ Artifacts persist to disk and reload correctly")

    print()


def test_metadata():
    """Test metadata tracking."""
    print("Testing metadata...")

    store = ArtifactStore(base_dir="/tmp/test_artifacts_meta")
    store.save(
        topic="Test",
        step_name="meta_test",
        data="data",
        metadata={"custom_field": "custom_value"}
    )

    meta = store.get_metadata("Test", "meta_test")
    assert meta["custom_field"] == "custom_value"
    assert "created_at" in meta
    print("✅ Metadata tracking works")

    print()


if __name__ == "__main__":
    print("=" * 70)
    print("🧪 ARTIFACT SYSTEM TEST SUITE")
    print("=" * 70)
    print()

    try:
        test_artifact_store_basic()
        test_artifact_references()
        test_persistence()
        test_metadata()

        print("=" * 70)
        print("✅ ALL TESTS PASSED!")
        print("=" * 70)
        print()
        print("The artifact system is ready to use.")
        print()
        print("Next steps:")
        print("  1. Run: python tools/learning/concept_simplifier.py 'Machine Learning'")
        print("  2. Check artifacts/ directory for saved knowledge")
        print("  3. Run: python demos/artifact_composition_demo.py")
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
