#!/usr/bin/env python3
"""
Test suite for meta-chain generator.
"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from src.core.meta_chain_generator import (
    MetaChainGenerator,
    CognitiveMoveLibrary,
    CognitiveMove,
    quick_generate
)


def test_cognitive_move_library():
    """Test that cognitive move library has expected moves."""
    print("Testing cognitive move library...")

    moves = CognitiveMoveLibrary.get_all_moves()

    # Should have multiple moves
    assert len(moves) > 5, "Should have at least 5 cognitive moves"

    # Check some key moves exist
    move_names = [m.name for m in moves]
    assert "decompose" in move_names
    assert "analogize" in move_names
    assert "synthesize" in move_names
    assert "connect" in move_names

    # Each move should have required fields
    for move in moves:
        assert move.name, "Move should have name"
        assert move.description, "Move should have description"
        assert move.when_to_use, "Move should have when_to_use"
        assert move.prompt_template, "Move should have prompt_template"

    print(f"✅ Cognitive move library has {len(moves)} moves")
    print()


def test_get_specific_move():
    """Test retrieving specific cognitive moves."""
    print("Testing specific move retrieval...")

    decompose = CognitiveMoveLibrary.get_move("decompose")
    assert decompose is not None
    assert decompose.name == "decompose"

    analogize = CognitiveMoveLibrary.get_move("analogize")
    assert analogize is not None
    assert analogize.name == "analogize"

    # Non-existent move
    fake = CognitiveMoveLibrary.get_move("nonexistent")
    assert fake is None

    print("✅ Specific move retrieval works")
    print()


def test_prompt_generation():
    """Test that cognitive moves can generate prompts."""
    print("Testing prompt generation...")

    decompose = CognitiveMoveLibrary.get_move("decompose")

    # Generate a prompt with context
    context = {"topic": "Machine Learning"}
    generated_prompt = decompose.generate_prompt(context)

    assert "Machine Learning" in generated_prompt
    assert "{{topic}}" not in generated_prompt  # Should be replaced
    assert "Respond in JSON" in generated_prompt

    print("✅ Prompt generation works")
    print()


def test_chain_design():
    """Test that meta-chain can design a chain."""
    print("Testing chain design...")

    generator = MetaChainGenerator()

    # Design a chain (don't execute)
    design = generator.design_chain(
        goal="Explain recursion simply",
        context={"topic": "recursion"}
    )

    # Check design structure
    assert design.goal == "Explain recursion simply"
    assert len(design.cognitive_moves) > 0
    assert len(design.prompts) > 0
    assert len(design.prompts) == len(design.cognitive_moves)

    # Check prompts are generated
    for prompt in design.prompts:
        assert len(prompt) > 0
        assert isinstance(prompt, str)

    print(f"✅ Chain design generated {len(design.prompts)} prompts")
    print()


def test_design_visualization():
    """Test that design can be visualized."""
    print("Testing design visualization...")

    generator = MetaChainGenerator()

    design = generator.design_chain(
        goal="Test visualization",
        context={"topic": "test"}
    )

    viz = design.visualize()

    assert "Goal:" in viz
    assert "Cognitive Moves:" in viz
    assert "Total Steps:" in viz

    print("✅ Design visualization works")
    print()


def test_design_serialization():
    """Test that design can be serialized."""
    print("Testing design serialization...")

    generator = MetaChainGenerator()

    design = generator.design_chain(
        goal="Test serialization",
        context={"topic": "test"}
    )

    # To dict
    design_dict = design.to_dict()
    assert isinstance(design_dict, dict)
    assert "goal" in design_dict
    assert "cognitive_moves" in design_dict

    # To JSON
    design_json = design.to_json()
    assert isinstance(design_json, str)
    assert "goal" in design_json

    print("✅ Design serialization works")
    print()


if __name__ == "__main__":
    print("=" * 70)
    print("🧪 META-CHAIN GENERATOR TEST SUITE")
    print("=" * 70)
    print()

    try:
        test_cognitive_move_library()
        test_get_specific_move()
        test_prompt_generation()
        test_chain_design()
        test_design_visualization()
        test_design_serialization()

        print("=" * 70)
        print("✅ ALL META-CHAIN TESTS PASSED!")
        print("=" * 70)
        print()
        print("The meta-chain generator is ready.")
        print()
        print("Try running:")
        print("  python demos/meta_chain_demo.py")
        print()
        print("Or use it directly:")
        print("  from meta_chain_generator import quick_generate")
        print('  design, outputs = quick_generate("Your goal here")')
        print()

    except AssertionError as e:
        print()
        print("=" * 70)
        print("❌ TEST FAILED")
        print("=" * 70)
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
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
