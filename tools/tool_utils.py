"""
🛠️ Tool Utilities

Shared functions for cognitive exoskeleton tools to reduce code duplication.
"""

import sys
import os
import json
import tempfile
import subprocess
import argparse

def setup_project_root(current_file, depth=2):
    """
    Add project root to sys.path and return it.
    Call this at the very beginning of your script.
    depth: number of levels up to reach project root.
           Default is 2 (e.g. tools/category/script.py -> root)
    """
    path_parts = [os.path.dirname(current_file)] + ['..'] * depth
    project_root = os.path.abspath(os.path.join(*path_parts))
    if project_root not in sys.path:
        sys.path.insert(0, project_root)
    return project_root

def load_user_context(project_root):
    """Load user profile for context-aware generation"""
    context_path = os.path.join(project_root, 'context', 'user_profile.json')
    try:
        with open(context_path, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        # Return empty dict instead of printing warning to keep output clean
        # unless verbose logging is needed
        return {}

def open_in_editor(initial_content="# Enter your content below\n# Lines starting with # will be ignored\n\n"):
    """Open a temporary file in the user's default editor"""
    editor = os.environ.get('EDITOR', 'vi')

    with tempfile.NamedTemporaryFile(mode='w+', suffix='.txt', delete=False) as tf:
        tf.write(initial_content)
        temp_path = tf.name

    try:
        subprocess.run([editor, temp_path], check=True)

        with open(temp_path, 'r') as f:
            content = f.read()

        # Remove comment lines
        lines = [line for line in content.split('\n') if not line.strip().startswith('#')]
        return '\n'.join(lines).strip()
    finally:
        os.unlink(temp_path)

def read_interactive_input(prompt_title="Interactive Input", prompt_message="Enter your content."):
    """Prompt user to paste multi-line content"""
    print(f"{prompt_title}")
    print("=" * 60)
    print(f"{prompt_message}")
    print("Press Ctrl+D (or Ctrl+Z on Windows) when finished.")
    print("=" * 60)
    print()

    try:
        content = sys.stdin.read().strip()
        return content
    except KeyboardInterrupt:
        print("\n\n❌ Cancelled")
        sys.exit(0)

def get_input_from_args(description, default_context_help="Additional context"):
    """
    Standard CLI argument parsing.
    Returns (topic, context_string).
    """
    parser = argparse.ArgumentParser(
        description=description,
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument('topic', nargs='?', help='Main topic or input')
    parser.add_argument('--context', default='', help=default_context_help)
    parser.add_argument('--editor', action='store_true', help='Open editor for input')
    
    args = parser.parse_args()

    topic = None
    if args.editor:
        topic = open_in_editor()
    elif args.topic:
        topic = args.topic
    elif not sys.stdin.isatty():
        topic = sys.stdin.read().strip()
    else:
        topic = read_interactive_input()

    if not topic:
        print("❌ Error: No input provided")
        sys.exit(1)
        
    return topic, args.context

def save_chain_output(project_root, output_dir, tool_name, topic, execution_trace, result, context_filled_prompts, usage_stats, artifact_store=None):
    """
    Standard function to save chain outputs and logs.
    """
    from datetime import datetime
    try:
        from src.core.chain import MinimalChainable
    except ImportError:
        print("⚠️ Warning: Could not import MinimalChainable for logging")
        return None, None

    os.makedirs(output_dir, exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    
    # Save JSON trace
    # Simple sanitization
    safe_topic = "".join([c if c.isalnum() else "_" for c in topic[:50]])
    json_filename = f"{timestamp}-{safe_topic}.json"
    output_path = os.path.join(output_dir, json_filename)
    
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(execution_trace, f, indent=2)
        
    # Log to Markdown
    log_file = MinimalChainable.log_to_markdown(tool_name, context_filled_prompts, result, usage_stats)
    
    print(f"✅ Saved JSON to: {output_path}")
    print(f"✅ Log saved to: {log_file}")
    print()
    
    if artifact_store:
        print(artifact_store.visualize())
        
    return output_path, log_file

