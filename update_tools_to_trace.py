#!/usr/bin/env python3
"""
Script to update all tools to use execution trace format.
This makes them compatible with the web UI's chain visualization.
"""

import os
import re

TOOLS_DIR = "tools"

# Files to skip (already updated or utility files)
SKIP_FILES = {
    "tool_utils.py",
    "cost_report.py",
    "concept_simplifier.py",  # Already updated
    "__init__.py",
    "__pycache__"
}

def update_tool_file(filepath):
    """Update a single tool file to use execution trace format."""

    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    original_content = content
    changes_made = []

    # Pattern 1: Update the return values from MinimalChainable.run()
    # From: result, context_filled_prompts, usage_stats = MinimalChainable.run(
    # To: result, context_filled_prompts, usage_stats, execution_trace = MinimalChainable.run(
    pattern1 = r'(\s+)(result, context_filled_prompts, usage_stats)\s*=\s*MinimalChainable\.run\('
    if re.search(pattern1, content):
        content = re.sub(
            pattern1,
            r'\1result, context_filled_prompts, usage_stats, execution_trace = MinimalChainable.run(',
            content
        )
        changes_made.append("Updated MinimalChainable.run() return values")

    # Pattern 2: Add return_trace=True parameter
    # Need to add it before the prompts parameter
    # From: prompts=[
    # To: return_trace=True,\n        prompts=[
    pattern2 = r'(\s+)(prompts=\[)'
    if re.search(pattern2, content) and 'return_trace=True' not in content:
        content = re.sub(
            pattern2,
            r'\1return_trace=True,\n\1\2',
            content,
            count=1  # Only replace the first occurrence
        )
        changes_made.append("Added return_trace=True parameter")

    # Pattern 3: Update what gets saved
    # From: json.dump(result, f, indent=2)
    # To: json.dump(execution_trace, f, indent=2)
    pattern3 = r'json\.dump\(result,\s*f,\s*indent=2\)'
    if re.search(pattern3, content):
        content = re.sub(pattern3, 'json.dump(execution_trace, f, indent=2)', content)
        changes_made.append("Updated json.dump to save execution_trace")

    # Pattern 4: Update comment about saving
    # From: # Save the results
    # To: # Save the execution trace (includes full chain visualization data)
    pattern4 = r'#\s*Save the results?'
    if re.search(pattern4, content):
        content = re.sub(
            pattern4,
            '# Save the execution trace (includes full chain visualization data)',
            content
        )
        changes_made.append("Updated save comment")

    # Pattern 5: Remove return_usage=True if it exists (replaced by return_trace)
    pattern5 = r',?\s*return_usage=True,?\s*'
    if re.search(pattern5, content):
        # Only remove if we're adding return_trace
        if 'return_trace=True' in content:
            content = re.sub(pattern5, ',\n        ', content)
            changes_made.append("Removed return_usage=True (replaced by return_trace)")

    if content != original_content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return True, changes_made

    return False, []

def main():
    """Update all tool files."""
    total_files = 0
    updated_files = 0

    print("🔄 Updating tools to use execution trace format...\n")

    for root, dirs, files in os.walk(TOOLS_DIR):
        for filename in files:
            if not filename.endswith('.py'):
                continue

            if filename in SKIP_FILES:
                continue

            filepath = os.path.join(root, filename)
            total_files += 1

            success, changes = update_tool_file(filepath)

            if success:
                updated_files += 1
                print(f"✅ {filepath}")
                for change in changes:
                    print(f"   - {change}")
            else:
                print(f"⏭️  {filepath} (no changes needed)")

    print(f"\n📊 Summary:")
    print(f"   Total files processed: {total_files}")
    print(f"   Files updated: {updated_files}")
    print(f"   Files unchanged: {total_files - updated_files}")

    if updated_files > 0:
        print(f"\n✨ All tools now use execution trace format!")
        print(f"   They're ready for the web UI chain visualization.")
    else:
        print(f"\n✨ All tools already using execution trace format!")

if __name__ == "__main__":
    main()
