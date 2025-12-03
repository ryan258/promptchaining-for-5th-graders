#!/usr/bin/env python3
"""
⏳ Research Timeline Tool

Generates research-grade timelines tracing the origins, evolution, current state,
and future possibilities of any topic.

Usage:
    # Interactive mode
    python tools/research/timeline.py

    # Single topic
    python tools/research/timeline.py "CRISPR gene editing"

    # With context
    python tools/research/timeline.py "Topic" --context "Focus on ethical implications"
"""

import sys
import os
import argparse
import json
import tempfile
import subprocess
from datetime import datetime

# Add project root to sys.path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from chain import MinimalChainable
from main import build_models, prompt

def load_user_context():
    """Load user profile for context-aware generation"""
    context_path = os.path.join(project_root, 'context', 'user_profile.json')
    try:
        with open(context_path, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print("⚠️  No user profile found. Using defaults.")
        return {
            "research_interests": [],
            "expertise_level": "General"
        }

def research_timeline_tool(topic, additional_context=""):
    """Generate research-grade timeline for a topic"""

    print(f"⏳ Research Timeline Tool")
    print(f"Topic: {topic}\n")

    # Load user context
    user_profile = load_user_context()
    
    client, model_names = build_models()
    selected_model_name = model_names[0]
    model_info = (client, selected_model_name)

    # Enhanced context
    context_data = {
        "topic": topic,
        "additional_context": additional_context,
        "user_expertise": user_profile.get('expertise_level', 'General')
    }

    result, context_filled_prompts = MinimalChainable.run(
        context=context_data,
        model=model_info,
        callable=prompt,
        prompts=[
            # Prompt 1: Historical Origins (Deep Dive)
            """Analyze the historical origins of '{{topic}}'. 
            
            Look for:
            - Earliest theoretical underpinnings (even if obscure)
            - Contradicting theories or disputed attributions
            - Precursor technologies or concepts
            
            Respond in JSON: {
                "origins": [
                    {
                        "period": "Time period",
                        "event": "Event/Discovery",
                        "description": "Detailed description",
                        "significance": "Why this matters",
                        "uncertainty": "Any historical debate/uncertainty"
                    }
                ],
                "theoretical_roots": "Summary of early theoretical work"
            }""",

            # Prompt 2: Evolution & Breakthroughs
            """Trace the key evolution points of '{{topic}}' from its origins ({{output[-1].theoretical_roots}}).
            
            Focus on:
            - Major paradigm shifts
            - Critical breakthroughs (technical or conceptual)
            - "Winter" periods (stagnation) and what ended them
            
            Respond in JSON: {
                "evolution_points": [
                    {
                        "year": "Year/Era",
                        "breakthrough": "Name of breakthrough",
                        "impact": "Transformative effect",
                        "key_figures": ["Names"],
                        "citation_needed": "Topic needing citation"
                    }
                ]
            }""",

            # Prompt 3: Current State & Frontier
            """Analyze the current state of '{{topic}}' today.
            
            Identify:
            - State-of-the-art (SOTA) capabilities
            - Unresolved questions/Research gaps
            - Current limitations
            
            Respond in JSON: {
                "current_state_summary": "High-level summary",
                "sota_capabilities": ["Cap 1", "Cap 2"],
                "research_gaps": ["Gap 1", "Gap 2"],
                "limitations": ["Limitation 1", "Limitation 2"],
                "consensus_level": "High/Medium/Low (is there agreement on direction?)"
            }""",

            # Prompt 4: Future Trajectories & Risks
            """Project the future of '{{topic}}' (20 years).
            
            Speculate on:
            - Probable evolution (linear progress)
            - Wildcard scenarios (disruptive changes)
            - Systemic risks or ethical implications
            
            Respond in JSON: {
                "near_term_prediction": "Next 5 years",
                "long_term_speculation": "20 years out",
                "wildcards": ["Low probability, high impact event"],
                "risks": ["Risk 1", "Risk 2"]
            }"""
        ]
    )

    # Save output
    output_dir = os.path.join(project_root, 'output', 'research', 'timelines')
    os.makedirs(output_dir, exist_ok=True)

    # Generate filename
    safe_topic = "".join(c for c in topic if c.isalnum() or c in (' ', '-', '_')).strip()
    safe_topic = safe_topic.replace(' ', '-').lower()[:50]
    timestamp = datetime.now().strftime("%Y%m%d-%H%M")
    
    output_file = os.path.join(output_dir, f"{timestamp}-{safe_topic}.md")

    # Format as markdown
    markdown_output = format_as_markdown(topic, result)

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(markdown_output)

    print(f"\n✅ Timeline saved to: {output_file}")
    
    # Log
    log_file = MinimalChainable.log_to_markdown("research_timeline", context_filled_prompts, result)
    print(f"✅ Full chain log saved to: {log_file}")
    
    return output_file

def format_as_markdown(topic, chain_results):
    """Format chain results as research-grade markdown"""
    
    md = f"""# Research Timeline: {topic}
    
Generated: {datetime.now().strftime("%Y-%m-%d %H:%M")}

---

## 🏛️ Historical Origins

"""
    try:
        origins_data = chain_results[0]
        if origins_data.get('theoretical_roots'):
            md += f"**Theoretical Roots**: {origins_data['theoretical_roots']}\n\n"
        
        if origins_data.get('origins'):
            for item in origins_data['origins']:
                md += f"### {item.get('period', 'Unknown Period')}: {item.get('event', 'Event')}\n"
                md += f"{item.get('description', '')}\n\n"
                md += f"**Significance**: {item.get('significance', '')}\n"
                if item.get('uncertainty'):
                    md += f"> [!NOTE]\n> **Historical Uncertainty**: {item['uncertainty']}\n"
                md += "\n"
    except Exception as e:
        md += f"*Error parsing origins: {e}*\n"

    md += "## 🧬 Evolution & Breakthroughs\n\n"
    
    try:
        evo_data = chain_results[1]
        if evo_data.get('evolution_points'):
            for point in evo_data['evolution_points']:
                md += f"### {point.get('year', 'Year')}: {point.get('breakthrough', 'Breakthrough')}\n"
                md += f"{point.get('impact', '')}\n\n"
                if point.get('key_figures'):
                    md += f"**Key Figures**: {', '.join(point['key_figures'])}\n"
                if point.get('citation_needed'):
                    md += f"*[Citation needed: {point['citation_needed']}]*\n"
                md += "\n"
    except Exception as e:
        md += f"*Error parsing evolution: {e}*\n"

    md += "## 📍 Current State (SOTA)\n\n"
    
    try:
        current_data = chain_results[2]
        md += f"{current_data.get('current_state_summary', '')}\n\n"
        
        md += "**Capabilities**:\n"
        for cap in current_data.get('sota_capabilities', []):
            md += f"- {cap}\n"
        md += "\n"
        
        md += "**Research Gaps**:\n"
        for gap in current_data.get('research_gaps', []):
            md += f"- [ ] {gap}\n"
        md += "\n"
        
        md += f"**Consensus Level**: {current_data.get('consensus_level', 'Unknown')}\n"
    except Exception as e:
        md += f"*Error parsing current state: {e}*\n"

    md += "\n## 🔮 Future Trajectories\n\n"
    
    try:
        future_data = chain_results[3]
        md += f"**Near Term (5y)**: {future_data.get('near_term_prediction', '')}\n\n"
        md += f"**Long Term (20y)**: {future_data.get('long_term_speculation', '')}\n\n"
        
        if future_data.get('wildcards'):
            md += "**Wildcards**:\n"
            for card in future_data['wildcards']:
                md += f"- ⚠️ {card}\n"
        md += "\n"
        
        if future_data.get('risks'):
            md += "**Systemic Risks**:\n"
            for risk in future_data['risks']:
                md += f"- {risk}\n"
    except Exception as e:
        md += f"*Error parsing future: {e}*\n"

    return md

def open_in_editor():
    """Open a temporary file in the user's default editor"""
    editor = os.environ.get('EDITOR', 'vi')

    with tempfile.NamedTemporaryFile(mode='w+', suffix='.txt', delete=False) as tf:
        tf.write("# Enter your research topic below\n")
        tf.write("# Lines starting with # will be ignored\n\n")
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

def read_interactive_input():
    """Prompt user to paste multi-line content"""
    print("⏳ Research Timeline Tool - Interactive Mode")
    print("=" * 60)
    print("Enter your research topic.")
    print("Press Ctrl+D (or Ctrl+Z on Windows) when finished.")
    print("=" * 60)
    print()

    try:
        content = sys.stdin.read().strip()
        return content
    except KeyboardInterrupt:
        print("\n\n❌ Cancelled")
        sys.exit(0)

def main():
    parser = argparse.ArgumentParser(
        description="Generate research-grade timelines",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument('topic', nargs='?', help='Topic for the timeline')
    parser.add_argument('--context', default='', help='Additional context')
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
        print("❌ Error: No topic provided")
        sys.exit(1)

    research_timeline_tool(topic, args.context)

if __name__ == "__main__":
    main()
