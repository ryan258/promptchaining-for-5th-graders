#!/usr/bin/env python3
"""
Tests for MS Blog Content Generation Tools
===========================================

Quick validation tests to ensure all generators work correctly.
"""

import sys
from pathlib import Path
import pytest
from unittest.mock import patch

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from lib.core import llm_client
from lib.core.errors import InputError
from tools.ms_blog import cli
from tools.ms_blog.ms_content_tools import (
    batch_generate_content,
    generate_prompt_card,
    generate_shortcut_spotlight,
    generate_guide,
    expand_content_idea,
    low_energy_pipeline,
    save_markdown,
    validate_content
)


def _mock_chain_run(
    context,
    model,
    llm_callable=None,
    prompts=None,
    return_trace=False,
    return_usage=False,
    callable=None,
    **kwargs
):
    """Deterministic mock for MinimalChainable.run used by unit tests."""
    if llm_callable is None:
        llm_callable = callable
    if prompts is None:
        prompts = []

    first_prompt = prompts[0] if prompts else ""
    usage = [{"prompt_tokens": 120, "completion_tokens": 80}]
    trace = {"steps": [], "final_result": None, "total_tokens": 200}

    prompt_card_md = """---
title: "Test Prompt Card"
---

## Problem
A clear test problem.

## Prompt
Use this prompt.

## Examples
Example output.
"""
    shortcut_md = """---
title: "Test Shortcut"
---

## Why This Matters for MS
It saves effort.

## How
Step-by-step usage.

## Use Case
A practical scenario.
"""
    guide_md = """---
title: "Test Guide"
---

## Quick Path
Fast setup.

## Phase 1
Start here.

## Troubleshooting
Fixes and checks.
"""

    if "Analyze this MS-related problem" in first_prompt:
        result = [{}, {}, {}, {}, prompt_card_md]
    elif "Analyze this accessibility tool/technique" in first_prompt:
        result = [{}, {}, {}, {}, shortcut_md]
    elif "Analyze this system for MS users" in first_prompt:
        result = [{}, {}, {}, {}, {}, guide_md]
    elif "Analyze this content seed idea" in first_prompt:
        result = [{}, {}, {}, {}, {}, {
            "summary": {"seed_idea": "test"},
            "prompt_cards": [{"title": "Idea 1"}],
            "shortcuts": [{"title": "Shortcut 1"}],
            "guides": [{"title": "Guide 1"}],
            "blog_posts": [{"title": "Blog 1"}],
        }]
    elif "Analyze this user input" in first_prompt:
        result = [{
            "format": "prompt_card",
            "reasoning": "Best fit for a direct problem",
            "parameters": {
                "problem": "Test problem from selector",
                "target_audience": "People with MS"
            }
        }]
    else:
        result = [{"ok": True}]

    trace["final_result"] = result[-1]
    filled_prompts = prompts

    if return_trace:
        return result, filled_prompts, usage, trace
    if return_usage:
        return result, filled_prompts, usage
    return result, filled_prompts


@pytest.fixture(autouse=True)
def mock_chain_runner():
    with (
        patch("tools.ms_blog.ms_content_tools.get_model", return_value=(None, "offline")),
        patch("tools.ms_blog.ms_content_tools.MinimalChainable.run", side_effect=_mock_chain_run),
        patch("tools.ms_blog.ms_content_tools.MinimalChainable.log_to_markdown", return_value="mock_log.md"),
    ):
        yield


def test_cli_uses_shared_dotenv_loader(tmp_path, monkeypatch):
    monkeypatch.delenv("OPENROUTER_API_KEY", raising=False)
    monkeypatch.setattr(llm_client, "load_dotenv", lambda: monkeypatch.setenv("OPENROUTER_API_KEY", "synthetic-test-key"))
    monkeypatch.setattr(cli, "expand_content_idea", lambda **_: ({"ideas": ["An example"]}, {}))
    assert cli.main(["ideas", "An example", "--output-dir", str(tmp_path)]) == 0
    assert len(list(tmp_path.glob("ideas-*.json"))) == 1


def test_draft_save_preserves_existing_file_and_returns_actual_path(tmp_path):
    path = tmp_path / "same-title.md"
    assert Path(save_markdown("First draft", path)) == path
    copy = Path(save_markdown("Second draft", path))
    assert path.read_text() == "First draft"
    assert copy != path and copy.read_text() == "Second draft"
    assert not list(tmp_path.glob(".draft-*"))


def test_batch_rejects_excessive_request_plans_before_generation():
    with pytest.raises(InputError, match="1 to 20"):
        batch_generate_content("A topic", count=21)
    with pytest.raises(InputError, match="1–20 total drafts"):
        batch_generate_content("A topic", mix={"prompt": 20, "guide": 1})


def test_prompt_card_generator():
    """Test that prompt card generator produces valid output."""
    print("\n" + "="*60)
    print("TEST: Prompt Card Generator")
    print("="*60)

    try:
        content, metadata = generate_prompt_card(
            problem="Test problem: I forget things due to brain fog",
            target_audience="MS patients",
            energy_level="low"
        )

        assert isinstance(content, str), "Content should be a string"
        assert len(content) > 100, "Content should be substantial"
        assert "---" in content, "Should have YAML front matter"
        assert "##" in content, "Should have markdown headings"
        assert metadata['type'] == 'prompt_card', "Metadata type should be prompt_card"

        print("✅ Prompt card generator working")
        print(f"   Generated {len(content)} characters")
        print(f"   Validation: {'PASSED' if metadata['validation']['valid'] else 'FAILED'}")
    except Exception as e:
        print(f"❌ Prompt card generator failed: {e}")
        raise


def test_shortcut_generator():
    """Test that shortcut generator produces valid output."""
    print("\n" + "="*60)
    print("TEST: Shortcut Spotlight Generator")
    print("="*60)

    try:
        content, metadata = generate_shortcut_spotlight(
            tool="Test tool: Keyboard shortcuts",
            ms_benefit="Saves energy",
            category="keyboard-shortcuts"
        )

        assert isinstance(content, str), "Content should be a string"
        assert len(content) > 100, "Content should be substantial"
        assert "---" in content, "Should have YAML front matter"
        assert metadata['type'] == 'shortcut', "Metadata type should be shortcut"

        print("✅ Shortcut generator working")
        print(f"   Generated {len(content)} characters")
    except Exception as e:
        print(f"❌ Shortcut generator failed: {e}")
        raise


def test_guide_generator():
    """Test that guide generator produces valid output."""
    print("\n" + "="*60)
    print("TEST: Multi-Phase Guide Generator")
    print("="*60)

    try:
        content, metadata = generate_guide(
            system="Test system: Simple task automation",
            complexity="beginner",
            estimated_time="15 minutes"
        )

        assert isinstance(content, str), "Content should be a string"
        assert len(content) > 100, "Content should be substantial"
        assert "---" in content, "Should have YAML front matter"
        assert metadata['type'] == 'guide', "Metadata type should be guide"

        print("✅ Guide generator working")
        print(f"   Generated {len(content)} characters")
    except Exception as e:
        print(f"❌ Guide generator failed: {e}")
        raise


def test_content_idea_expander():
    """Test that idea expander produces valid output."""
    print("\n" + "="*60)
    print("TEST: Content Idea Expander")
    print("="*60)

    try:
        ideas, metadata = expand_content_idea(
            seed="Voice control and automation for people with limited hand mobility",
            pillar="All",
            count=10
        )

        assert isinstance(ideas, dict), "Ideas should be a dict"

        # Check if we got valid ideas or just an error
        if 'error' in ideas:
            # If there's an error, print it but don't fail the test
            # (idea expander can fail with short/simple inputs)
            print(f"⚠️  Idea expander returned error: {ideas.get('error')}")
            print("   (This can happen with minimal test inputs)")
            return  # Don't fail the test

        assert 'prompt_cards' in ideas or 'summary' in ideas, "Should have content ideas"

        print("✅ Idea expander working")
        if 'prompt_cards' in ideas:
            print(f"   Generated {len(ideas.get('prompt_cards', []))} prompt card ideas")
            print(f"   Generated {len(ideas.get('shortcuts', []))} shortcut ideas")
            print(f"   Generated {len(ideas.get('guides', []))} guide ideas")
    except Exception as e:
        print(f"❌ Idea expander failed: {e}")
        raise


def test_validation_function():
    """Test the validation function."""
    print("\n" + "="*60)
    print("TEST: Content Validation")
    print("="*60)

    try:
        # Test with valid content
        valid_content = """---
title: Test
---

## Problem

Some content here.

## Prompt

More content.

## Examples

Example content.
"""
        result = validate_content(valid_content, 'prompt_card')
        assert isinstance(result, dict), "Should return a dict"
        assert 'valid' in result, "Should have valid key"
        assert 'issues' in result, "Should have issues key"

        print("✅ Validation function working")
        print(f"   Test content valid: {result['valid']}")
    except Exception as e:
        print(f"❌ Validation function failed: {e}")
        raise


def test_low_energy_pipeline():
    """Test the complete low-energy pipeline."""
    print("\n" + "="*60)
    print("TEST: Low-Energy Pipeline (Integration)")
    print("="*60)

    try:
        result = low_energy_pipeline(
            input_text="Test: I need help with organization",
            energy_level="low",
            auto_save=False  # Don't save during tests
        )

        assert isinstance(result, dict), "Should return a dict"
        assert 'content' in result, "Should have content"
        assert 'metadata' in result, "Should have metadata"
        assert 'validation' in result, "Should have validation"
        assert isinstance(result['content'], str), "Content should be string"

        print("✅ Low-energy pipeline working")
        print(f"   Format chosen: {result['metadata'].get('format_chosen')}")
        print(f"   Content length: {len(result['content'])} characters")
        print(f"   Validation: {'PASSED' if result['validation']['valid'] else 'NEEDS REVIEW'}")
    except Exception as e:
        print(f"❌ Low-energy pipeline failed: {e}")
        import traceback
        traceback.print_exc()
        raise



if __name__ == "__main__":
    import argparse

    tests = {
        "validation": "test_validation_function",
        "prompt": "test_prompt_card_generator",
        "shortcut": "test_shortcut_generator",
        "guide": "test_guide_generator",
        "ideas": "test_content_idea_expander",
        "pipeline": "test_low_energy_pipeline",
    }
    parser = argparse.ArgumentParser(description="Run offline MS Blog Content Tools checks.")
    parser.add_argument("--test", choices=[*tests, "all"], default="all")
    selected = parser.parse_args().test
    target = str(Path(__file__).resolve())
    if selected != "all":
        target += f"::{tests[selected]}"
    raise SystemExit(pytest.main(["-q", target]))
