#!/usr/bin/env python3
"""
MS Blog Tools CLI
=================

Command-line interface for the MS Blog Content Generation Tools.

Usage:
    python tools/ms_blog/cli.py [command] [options]

Commands:
    pipeline    Run the low-energy pipeline (auto-detect format)
    prompt      Generate a prompt card
    shortcut    Generate a shortcut spotlight
    guide       Generate a multi-phase guide
    ideas       Expand content ideas
    batch       Generate a batch of content
    calendar    Generate a content calendar
    
    (No args)   Run interactive menu
"""

import argparse
import sys
import os
import json
import re
from datetime import datetime
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from lib.core.errors import user_error
from lib.core.llm_client import has_api_key
from tools.ms_blog.ms_content_tools import (
    low_energy_pipeline,
    generate_prompt_card,
    generate_shortcut_spotlight,
    generate_guide,
    expand_content_idea,
    batch_generate_content,
    generate_content_calendar,
    save_draft,
    save_markdown,
    sanitize_filename
)

def main(argv=None):
    parser = argparse.ArgumentParser(description="MS Blog Content Generator")
    subparsers = parser.add_subparsers(dest="command", help="Command to run")

    # --- Pipeline Command ---
    pipeline_parser = subparsers.add_parser("pipeline", help="Run low-energy pipeline")
    pipeline_parser.add_argument("input", help="Problem description or topic")
    pipeline_parser.add_argument("--energy", choices=["low", "medium", "high"], default="medium", help="Energy level")
    pipeline_parser.add_argument("--output-dir", help="Directory to save output")
    pipeline_parser.add_argument("--no-save", action="store_true", help="Don't auto-save")

    # --- Prompt Card Command ---
    prompt_parser = subparsers.add_parser("prompt", help="Generate prompt card")
    prompt_parser.add_argument("problem", help="Problem to solve")
    prompt_parser.add_argument("--audience", default="People with MS", help="Target audience")
    prompt_parser.add_argument("--energy", choices=["low", "medium", "high"], default="medium")
    prompt_parser.add_argument("--output-dir", help="Directory to save output")

    # --- Shortcut Command ---
    shortcut_parser = subparsers.add_parser("shortcut", help="Generate shortcut spotlight")
    shortcut_parser.add_argument("tool", help="Tool or technique name")
    shortcut_parser.add_argument("--benefit", required=True, help="MS benefit")
    shortcut_parser.add_argument("--category", default="automation", help="Category")
    shortcut_parser.add_argument("--output-dir", help="Directory to save output")

    # --- Guide Command ---
    guide_parser = subparsers.add_parser("guide", help="Generate multi-phase guide")
    guide_parser.add_argument("system", help="System to build")
    guide_parser.add_argument("--complexity", choices=["beginner", "intermediate", "advanced"], default="beginner")
    guide_parser.add_argument("--time", default="30 mins", help="Estimated time")
    guide_parser.add_argument("--output-dir", help="Directory to save output")

    # --- Ideas Command ---
    ideas_parser = subparsers.add_parser("ideas", help="Generate content ideas")
    ideas_parser.add_argument("seed", help="Seed idea")
    ideas_parser.add_argument("--count", type=int, default=10, help="Number of ideas")
    ideas_parser.add_argument("--output-dir", help="Directory to save output")

    # --- Batch Command ---
    batch_parser = subparsers.add_parser("batch", help="Generate batch of content")
    batch_parser.add_argument("topic", help="Topic area")
    batch_parser.add_argument("--count", type=int, default=5, help="Total items")
    batch_parser.add_argument("--output-dir", help="Directory to save output")

    # --- Calendar Command ---
    calendar_parser = subparsers.add_parser("calendar", help="Generate content calendar")
    calendar_parser.add_argument("topic", help="Main theme")
    calendar_parser.add_argument("--duration", default="1 month", help="Duration")
    calendar_parser.add_argument("--frequency", default="3x/week", help="Frequency")
    calendar_parser.add_argument("--output-dir", help="Directory to save output")

    args = parser.parse_args(argv)

    # Default output directory
    default_output_dir = os.path.join(project_root, "output", "ms_blog")

    # Validate API Key
    if args.command and not has_api_key():
        print("Add an OpenRouter key to .env before generating drafts.", file=sys.stderr)
        return 1

    try:
        run_command(args, default_output_dir)
    except OSError:
        print("Could not save the draft. Check the chosen output directory and available disk space.", file=sys.stderr)
        return 1
    except Exception as exc:
        print(user_error(exc), file=sys.stderr)
        return 1
    return 0


def run_command(args, default_output_dir):
    if args.command == "pipeline":
        print(f"🚀 Running pipeline for: {args.input}")
        result = low_energy_pipeline(
            input_text=args.input,
            energy_level=args.energy,
            output_dir=args.output_dir or default_output_dir,
            auto_save=not args.no_save
        )
        if args.no_save:
            print(result["content"])

    elif args.command == "prompt":
        print(f"🚀 Generating prompt card for: {args.problem}")
        content, meta = generate_prompt_card(
            problem=args.problem,
            target_audience=args.audience,
            energy_level=args.energy
        )
        _save_and_report(content, args.output_dir or default_output_dir, "prompt-card", meta["validation"])

    elif args.command == "shortcut":
        print(f"🚀 Generating shortcut for: {args.tool}")
        content, meta = generate_shortcut_spotlight(
            tool=args.tool,
            ms_benefit=args.benefit,
            category=args.category
        )
        _save_and_report(content, args.output_dir or default_output_dir, "shortcut", meta["validation"])

    elif args.command == "guide":
        print(f"🚀 Generating guide for: {args.system}")
        content, meta = generate_guide(
            system=args.system,
            complexity=args.complexity,
            estimated_time=args.time
        )
        _save_and_report(content, args.output_dir or default_output_dir, "guide", meta["validation"])

    elif args.command == "ideas":
        print(f"🚀 Generating ideas for: {args.seed}")
        ideas, meta = expand_content_idea(
            seed=args.seed,
            count=args.count
        )
        _save_json_and_report(ideas, args.output_dir or default_output_dir, "ideas")

    elif args.command == "batch":
        print(f"🚀 Batch generating for: {args.topic}")
        batch_generate_content(
            topic_area=args.topic,
            count=args.count,
            output_dir=args.output_dir or default_output_dir
        )

    elif args.command == "calendar":
        print(f"🚀 Generating calendar for: {args.topic}")
        calendar = generate_content_calendar(
            topic=args.topic,
            duration=args.duration,
            frequency=args.frequency
        )
        _save_json_and_report(calendar, args.output_dir or default_output_dir, "calendar")

    else:
        # Interactive mode
        run_interactive_menu(default_output_dir)

def _save_and_report(content, output_dir, prefix, validation):
    title_match = re.search(r'^title:\s*["\']?([^"\'\n]+)', content, re.MULTILINE)
    filename = sanitize_filename(title_match.group(1) if title_match else "", prefix=prefix)
    path = save_markdown(content, os.path.join(output_dir, filename))
    print(f"\nSaved draft for review: {path}")
    for note in validation["issues"] + validation["warnings"]:
        print(f"Review: {note}")

def _save_json_and_report(data, output_dir, prefix):
    filename = f"{prefix}-{datetime.now().strftime('%Y%m%d-%H%M%S')}.json"
    path = save_draft(json.dumps(data, indent=2, ensure_ascii=False), os.path.join(output_dir, filename))
    print(f"\nSaved draft for review: {path}")

def run_interactive_menu(output_dir):
    print("\n" + "="*60)
    print("MS BLOG TOOLS - INTERACTIVE MODE")
    print("="*60)
    print("1. Low-Energy Pipeline (Auto-detect)")
    print("2. Generate Prompt Card")
    print("3. Generate Shortcut Spotlight")
    print("4. Generate Multi-Phase Guide")
    print("5. Generate Content Ideas")
    print("6. Batch Generation")
    print("7. Generate Content Calendar")
    print("0. Exit")
    
    choice = input("\nSelect option: ").strip()
    
    if choice == "1":
        topic = input("Enter problem/topic: ")
        low_energy_pipeline(topic, auto_save=True, output_dir=output_dir)
    elif choice == "2":
        problem = input("Enter problem: ")
        content, metadata = generate_prompt_card(problem)
        _save_and_report(content, output_dir, "prompt", metadata["validation"])
    elif choice == "3":
        tool = input("Enter tool name: ")
        benefit = input("Enter MS benefit: ")
        content, metadata = generate_shortcut_spotlight(tool, benefit)
        _save_and_report(content, output_dir, "shortcut", metadata["validation"])
    elif choice == "4":
        system = input("Enter system name: ")
        content, metadata = generate_guide(system)
        _save_and_report(content, output_dir, "guide", metadata["validation"])
    elif choice == "5":
        seed = input("Enter seed idea: ")
        ideas, _ = expand_content_idea(seed)
        _save_json_and_report(ideas, output_dir, "ideas")
    elif choice == "6":
        topic = input("Enter topic area: ")
        batch_generate_content(topic, output_dir=output_dir)
    elif choice == "7":
        topic = input("Enter topic: ")
        cal = generate_content_calendar(topic)
        _save_json_and_report(cal, output_dir, "calendar")
    elif choice == "0":
        return
    else:
        print("Invalid choice")
        run_interactive_menu(output_dir)

if __name__ == "__main__":
    raise SystemExit(main())
