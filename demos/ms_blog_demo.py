#!/usr/bin/env python3
"""
MS Blog Content Generator - Interactive Demo
==============================================

This demo shows the Low-Energy Content Pipeline in action.

Three demonstration scenarios:
1. Auto-detect format and generate content (low energy)
2. Generate a specific prompt card (medium energy)
3. Expand a seed idea into multiple content pieces (brainstorming)

Run this to see how the pipeline works end-to-end.
"""

import sys
import os
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from tools.ms_blog.ms_content_tools import (
    low_energy_pipeline,
    generate_prompt_card,
    generate_shortcut_spotlight,
    generate_guide,
    expand_content_idea
)


def demo_1_low_energy_pipeline():
    """
    Demo 1: The complete low-energy pipeline

    Just describe a problem and let the system decide what to build.
    Perfect for low-energy days when you can't think through format decisions.
    """
    print("\n" + "="*70)
    print("DEMO 1: LOW-ENERGY PIPELINE (Auto-detect format)")
    print("="*70)
    print("\nScenario: You're having a foggy day and just want to create content")
    print("Input: A simple problem description")
    print("\nLet's generate content for: 'I keep forgetting to take my medication'\n")

    result = low_energy_pipeline(
        input_text="I keep forgetting to take my medication",
        energy_level="low",
        auto_save=True
    )

    print("\n📄 Generated content preview (first 500 chars):")
    print("-" * 70)
    print(result['content'][:500] + "...")
    print("-" * 70)

    return result


def demo_2_prompt_card_generation():
    """
    Demo 2: Generate a specific prompt card

    When you know you want a prompt card, use the focused generator.
    """
    print("\n" + "="*70)
    print("DEMO 2: PROMPT CARD GENERATOR (Focused generation)")
    print("="*70)
    print("\nScenario: You specifically want to create a prompt card")
    print("Problem: MS brain fog makes daily planning overwhelming\n")

    content, metadata = generate_prompt_card(
        problem="I get overwhelmed planning my day with MS brain fog",
        target_audience="People with MS experiencing cognitive challenges",
        energy_level="medium"
    )

    print(f"\n✅ Generated prompt card")
    print(f"📊 Validation: {'PASSED' if metadata['validation']['valid'] else 'NEEDS REVIEW'}")
    print(f"🔢 Tokens used: {metadata['token_usage']}")

    if metadata['validation']['warnings']:
        print(f"⚠️  Warnings: {metadata['validation']['warnings']}")

    print("\n📄 Content preview (first 800 chars):")
    print("-" * 70)
    print(content[:800] + "...")
    print("-" * 70)

    # Save it
    output_path = os.path.join(project_root, "output", "ms_blog", "daily-planning-prompt.md")
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, 'w') as f:
        f.write(content)
    print(f"\n💾 Saved to: {output_path}")

    return content, metadata


def demo_3_shortcut_generation():
    """
    Demo 3: Generate a shortcut spotlight

    Showcase an accessibility tool or technique.
    """
    print("\n" + "="*70)
    print("DEMO 3: SHORTCUT SPOTLIGHT GENERATOR")
    print("="*70)
    print("\nScenario: You want to write about an accessibility tool")
    print("Tool: Voice typing in Google Docs\n")

    content, metadata = generate_shortcut_spotlight(
        tool="Voice typing in Google Docs",
        ms_benefit="Reduces hand fatigue and typing strain, helps when fine motor control is difficult",
        category="automation"
    )

    print(f"\n✅ Generated shortcut spotlight")
    print(f"📊 Validation: {'PASSED' if metadata['validation']['valid'] else 'NEEDS REVIEW'}")

    print("\n📄 Content preview (first 600 chars):")
    print("-" * 70)
    print(content[:600] + "...")
    print("-" * 70)

    # Save it
    output_path = os.path.join(project_root, "output", "ms_blog", "voice-typing-shortcut.md")
    with open(output_path, 'w') as f:
        f.write(content)
    print(f"\n💾 Saved to: {output_path}")

    return content, metadata


def demo_4_guide_generation():
    """
    Demo 4: Generate a multi-phase guide

    Create a comprehensive system setup guide.
    """
    print("\n" + "="*70)
    print("DEMO 4: MULTI-PHASE GUIDE GENERATOR")
    print("="*70)
    print("\nScenario: You want to create a comprehensive setup guide")
    print("System: Setting up AI assistant for MS symptom tracking\n")

    content, metadata = generate_guide(
        system="Setting up an AI assistant to track and analyze MS symptoms",
        complexity="beginner",
        estimated_time="30-45 minutes"
    )

    print(f"\n✅ Generated multi-phase guide")
    print(f"📊 Validation: {'PASSED' if metadata['validation']['valid'] else 'NEEDS REVIEW'}")

    print("\n📄 Content preview (first 700 chars):")
    print("-" * 70)
    print(content[:700] + "...")
    print("-" * 70)

    # Save it
    output_path = os.path.join(project_root, "output", "ms_blog", "ai-symptom-tracking-guide.md")
    with open(output_path, 'w') as f:
        f.write(content)
    print(f"\n💾 Saved to: {output_path}")

    return content, metadata


def demo_5_content_idea_expansion():
    """
    Demo 5: Expand a seed idea into multiple content pieces

    Great for brainstorming and content planning.
    """
    print("\n" + "="*70)
    print("DEMO 5: CONTENT IDEA EXPANDER (Brainstorming)")
    print("="*70)
    print("\nScenario: You have a rough idea and want to explore it")
    print("Seed: Voice control for when hands don't cooperate\n")

    ideas, metadata = expand_content_idea(
        seed="Voice control for when hands don't cooperate",
        pillar="All",
        count=10
    )

    print("\n✅ Generated content ideas")
    print(f"\n📋 Summary:")
    if 'summary' in ideas:
        print(f"  • Total ideas: {ideas['summary'].get('total_ideas', 'N/A')}")
        print(f"  • Top priority: {ideas['summary'].get('top_priority', 'N/A')}")

    print(f"\n💡 Prompt card ideas: {len(ideas.get('prompt_cards', []))}")
    if ideas.get('prompt_cards'):
        for i, idea in enumerate(ideas['prompt_cards'][:2], 1):
            print(f"  {i}. {idea.get('title', 'N/A')} (Priority: {idea.get('priority_score', 'N/A')}/10)")

    print(f"\n⚡ Shortcut ideas: {len(ideas.get('shortcuts', []))}")
    if ideas.get('shortcuts'):
        for i, idea in enumerate(ideas['shortcuts'][:2], 1):
            print(f"  {i}. {idea.get('title', 'N/A')} (Priority: {idea.get('priority_score', 'N/A')}/10)")

    print(f"\n📚 Guide ideas: {len(ideas.get('guides', []))}")
    if ideas.get('guides'):
        for i, idea in enumerate(ideas['guides'], 1):
            print(f"  {i}. {idea.get('title', 'N/A')} (Priority: {idea.get('priority_score', 'N/A')}/10)")

    # Save the ideas
    import json
    output_path = os.path.join(project_root, "output", "ms_blog", "content-ideas-voice-control.json")
    with open(output_path, 'w') as f:
        json.dump(ideas, f, indent=2)
    print(f"\n💾 Saved ideas to: {output_path}")

    return ideas, metadata


def interactive_menu():
    """
    Interactive menu for running demos.
    """
    print("\n" + "="*70)
    print("MS BLOG CONTENT GENERATOR - DEMO SUITE")
    print("="*70)
    print("\nChoose a demo to run:")
    print("\n1. Low-Energy Pipeline (auto-detect format)")
    print("2. Prompt Card Generator")
    print("3. Shortcut Spotlight Generator")
    print("4. Multi-Phase Guide Generator")
    print("5. Content Idea Expander (brainstorming)")
    print("6. Run ALL demos")
    print("0. Exit")

    choice = input("\nEnter your choice (0-6): ").strip()

    if choice == "1":
        demo_1_low_energy_pipeline()
    elif choice == "2":
        demo_2_prompt_card_generation()
    elif choice == "3":
        demo_3_shortcut_generation()
    elif choice == "4":
        demo_4_guide_generation()
    elif choice == "5":
        demo_5_content_idea_expansion()
    elif choice == "6":
        print("\n🚀 Running all demos...\n")
        demo_1_low_energy_pipeline()
        demo_2_prompt_card_generation()
        demo_3_shortcut_generation()
        demo_4_guide_generation()
        demo_5_content_idea_expansion()
        print("\n✅ All demos complete!")
    elif choice == "0":
        print("\n👋 Goodbye!")
        return
    else:
        print("\n❌ Invalid choice. Please try again.")
        return interactive_menu()

    # Ask if they want to run another
    print("\n" + "-"*70)
    again = input("\nRun another demo? (y/n): ").strip().lower()
    if again == 'y':
        interactive_menu()
    else:
        print("\n👋 Thanks for trying the MS Blog Content Generator!")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="MS Blog Content Generator Demo")
    parser.add_argument(
        "--demo",
        type=int,
        choices=[1, 2, 3, 4, 5, 6],
        help="Run specific demo (1-6) or all demos (6)"
    )
    parser.add_argument(
        "--interactive",
        action="store_true",
        help="Run interactive menu"
    )

    args = parser.parse_args()

    if args.demo:
        if args.demo == 1:
            demo_1_low_energy_pipeline()
        elif args.demo == 2:
            demo_2_prompt_card_generation()
        elif args.demo == 3:
            demo_3_shortcut_generation()
        elif args.demo == 4:
            demo_4_guide_generation()
        elif args.demo == 5:
            demo_5_content_idea_expansion()
        elif args.demo == 6:
            demo_1_low_energy_pipeline()
            demo_2_prompt_card_generation()
            demo_3_shortcut_generation()
            demo_4_guide_generation()
            demo_5_content_idea_expansion()
    elif args.interactive:
        interactive_menu()
    else:
        # Default: run interactive menu
        interactive_menu()

    print("\n" + "="*70)
    print("DEMO COMPLETE")
    print("="*70)
    print("\n📁 All generated content saved to: output/ms_blog/")
    print("📊 Logs saved to: logs/")
    print("\n💡 Next steps:")
    print("  • Review generated content")
    print("  • Test the prompts and instructions")
    print("  • Customize as needed")
    print("  • Copy to your Hugo blog when ready")
    print("\n" + "="*70)
