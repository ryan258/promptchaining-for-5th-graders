#!/usr/bin/env python3
"""
🔍 Artifact Browser - Explore Your Knowledge Library

Browse all artifacts created by prompt chains.
"""

import json
import sys
from artifact_store import ArtifactStore


def print_separator():
    print("=" * 70)


def browse_artifacts():
    """Interactive artifact browser."""
    store = ArtifactStore()

    print_separator()
    print("🔍 ARTIFACT BROWSER")
    print_separator()
    print()

    topics = store.list_topics()

    if not topics:
        print("📚 No artifacts found yet.")
        print()
        print("Create some by running:")
        print("  python tools/learning/concept_simplifier.py 'Your Topic'")
        print()
        return

    # Show overview
    print(store.visualize())

    # Interactive mode
    if len(sys.argv) > 1:
        # Command-line mode: artifact_browser.py <topic>
        topic = sys.argv[1]
        show_topic_artifacts(store, topic)
    else:
        # Interactive mode
        print("Commands:")
        print("  <topic>  - Show artifacts for a topic")
        print("  list     - List all topics")
        print("  query    - Search with patterns")
        print("  quit     - Exit")
        print()

        while True:
            try:
                cmd = input("🔍 > ").strip()

                if cmd in ["quit", "exit", "q"]:
                    break

                elif cmd == "list":
                    topics = store.list_topics()
                    print()
                    print("📚 Topics:")
                    for topic in topics:
                        steps = store.list_steps_for_topic(topic)
                        print(f"  • {topic} ({len(steps)} artifacts)")
                    print()

                elif cmd.startswith("query "):
                    pattern = cmd[6:].strip()
                    results = store.query(pattern)
                    print()
                    print(f"🔎 Results for '{pattern}':")
                    if results:
                        for key in results.keys():
                            print(f"  • {key}")
                    else:
                        print("  (no matches)")
                    print()

                elif cmd:
                    show_topic_artifacts(store, cmd)

            except KeyboardInterrupt:
                print()
                break

    print()
    print("👋 Done browsing!")


def show_topic_artifacts(store, topic):
    """Show all artifacts for a topic."""
    print()
    print_separator()
    print(f"📖 {topic.upper()}")
    print_separator()
    print()

    steps = store.list_steps_for_topic(topic)

    if not steps:
        print(f"No artifacts found for '{topic}'")
        print()
        print("Available topics:")
        for t in store.list_topics():
            print(f"  • {t}")
        print()
        return

    for step in steps:
        artifact = store.get(topic, step)
        metadata = store.get_metadata(topic, step)

        print(f"🔗 {step}")
        print(f"   Created: {metadata.get('created_at', 'unknown')[:19]}")

        if metadata.get('artifacts_used'):
            print(f"   Uses: {', '.join(metadata['artifacts_used'])}")

        print()

        # Pretty-print the artifact
        if isinstance(artifact, (dict, list)):
            print(json.dumps(artifact, indent=2, ensure_ascii=False))
        else:
            print(artifact)

        print()
        print("-" * 70)
        print()


def export_topic(topic):
    """Export all artifacts for a topic to a single JSON file."""
    store = ArtifactStore()

    steps = store.list_steps_for_topic(topic)
    if not steps:
        print(f"❌ No artifacts found for '{topic}'")
        return

    export_data = {
        "topic": topic,
        "artifacts": {}
    }

    for step in steps:
        artifact = store.get(topic, step)
        metadata = store.get_metadata(topic, step)
        export_data["artifacts"][step] = {
            "data": artifact,
            "metadata": metadata
        }

    output_file = f"{topic}_export.json"
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(export_data, f, indent=2, ensure_ascii=False)

    print(f"✅ Exported to {output_file}")


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--export":
        if len(sys.argv) < 3:
            print("Usage: python artifact_browser.py --export <topic>")
        else:
            export_topic(sys.argv[2])
    else:
        browse_artifacts()
