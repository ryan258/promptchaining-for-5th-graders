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
from datetime import datetime

# Setup project root and import shared tools
try:
    from tools.tool_utils import setup_project_root, load_user_context, get_input_from_args
except ImportError:
    # Fallback if running directly from tools/research/
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
    from tools.tool_utils import setup_project_root, load_user_context, get_input_from_args

project_root = setup_project_root(__file__)

from chain import MinimalChainable
from main import build_models, prompt

def research_timeline_tool(topic, additional_context=""):
    """Generate research-grade timeline for a topic"""

    print(f"⏳ Research Timeline Tool")
    print(f"Topic: {topic}\n")

    # Load user context
    user_profile = load_user_context(project_root)
    
    client, model_names = build_models()
    selected_model_name = model_names[0]
    model_info = (client, selected_model_name)

    # Enhanced context
    context_data = {
        "topic": topic,
        "additional_context": additional_context,
        "user_expertise": user_profile.get('expertise_level', 'General')
    }

    result, context_filled_prompts, usage_stats = MinimalChainable.run(
        context=context_data,
        model=model_info,
        callable=prompt,
        prompts=[
            # Prompt 1: Historical Origins (Deep Dive)
            """Analyze the historical origins of '{{topic}}' (aim for 3-5 entries; if fewer, explain why).
            
            Prioritize:
            - Earliest documented theory/concept (even if obscure)
            - One disputed attribution (if any)
            - One precursor technology/concept
            
            Keep each description to 2-3 sentences max.
            
            Respond in JSON: {
                "origins": [
                    {
                        "period": "e.g., '1600s' or '300 BCE'",
                        "event": "Event/Discovery (<=8 words)",
                        "description": "2-3 sentences",
                        "significance": "1 sentence",
                        "uncertainty": "1 sentence or 'None'"
                    }
                ],
                "theoretical_roots": "3-4 sentence summary; if <3 origins, explain scarcity here"
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
            """Project the future of '{{topic}}' over 20 years with exactly three scenarios:
            - Best-case (optimistic but realistic)
            - Worst-case (risks/limits magnified)
            - Wildcard (low-probability, high-impact; e.g., regulatory shock, enabling tech leap)
            
            Respond in JSON: {
                "future_scenarios": [
                    {
                        "scenario_name": "Best-case/Worst-case/Wildcard",
                        "description": "3-5 sentences",
                        "risks": ["Risk 1", "Risk 2"],
                        "ethics": ["Ethical concern 1"],
                        "mitigations": ["Mitigation 1"]
                    }
                ]
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
    log_file = MinimalChainable.log_to_markdown("research_timeline", context_filled_prompts, result, usage_stats)
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

def main():
    topic, context = get_input_from_args(
        description="Generate research-grade timelines"
    )
    research_timeline_tool(topic, context)

if __name__ == "__main__":
    main()
