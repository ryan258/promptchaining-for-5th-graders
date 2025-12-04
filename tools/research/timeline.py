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
            # Prompt 1: Historical Origins with research-grade rigor
            """You are a research historian specializing in the history of science and technology.

Analyze the historical origins of '{{topic}}' with academic rigor.

Provide 3-5 key origins, prioritizing:
1. Earliest documented theory or concept (even if obscure)
2. Major disputed attribution or controversy (if exists)
3. Most important precursor technology or breakthrough
4. Foundational work that enabled this field

For EACH origin:
- Period: Specific date range (e.g., "1820s", "300 BCE - 100 CE")
- Event: Name in under 10 words
- Description: 2-3 sentences maximum explaining what happened
- Significance: 1 sentence on why this mattered
- Uncertainty: Note debates, disputed claims, or "None known"

Example for "Artificial Intelligence - Origins":
{
  "period": "1943",
  "event": "McCulloch-Pitts Neural Model",
  "description": "Warren McCulloch and Walter Pitts published the first mathematical model of an artificial neuron, showing how simple connected units could compute logical functions. This provided the theoretical foundation that neurons could be modeled mathematically.",
  "significance": "Established that brain-like computation could be formalized with logic and math, not just biology.",
  "uncertainty": "Debate exists whether this was 'true' AI research or just computational theory."
}

Respond in JSON:
{
  "origins": [
    {
      "period": "Date or era",
      "event": "Event name (max 10 words)",
      "description": "2-3 sentences (max 80 words)",
      "significance": "1 sentence (max 25 words)",
      "uncertainty": "1 sentence or 'None known'"
    }
  ],
  "theoretical_roots": "3-4 sentence summary of the intellectual foundations (max 100 words)"
}

If fewer than 3 significant origins exist, explain why in "theoretical_roots". Provide 3-5 origins total.""",

            # Prompt 2: Evolution with paradigm shifts and stagnation periods
            """You are a science historian tracking the evolution of technological and scientific fields.

Trace the key evolution of '{{topic}}' from its theoretical roots:
{{output[-1].theoretical_roots}}

Provide 4-7 major evolution points, focusing on:
1. **Paradigm shifts** - Fundamental changes in approach or thinking
2. **Critical breakthroughs** - Discoveries that unlocked new possibilities
3. **Stagnation periods** ("AI winters", "dead ends") - When progress stalled and why it resumed
4. **Enabling technologies** - External developments that accelerated the field

Example of a "Winter Period" for "Artificial Intelligence":
{
  "year": "1974-1980",
  "breakthrough": "First AI Winter",
  "impact": "Funding dried up after early AI promises failed to materialize. Research slowed dramatically as practical applications proved elusive.",
  "key_figures": ["Lighthill Report (UK)", "DARPA funding cuts (US)"],
  "citation_needed": "Exact funding reduction percentages"
}

For EACH evolution point:
- Year: Specific year or era (e.g., "1997", "Early 2000s")
- Breakthrough: Name (max 12 words). Use negative framing for setbacks ("Second AI Winter", "Dot-com Crash Impact")
- Impact: 2-3 sentences on transformative effects (max 60 words)
- Key figures: 2-5 names (people, papers, or institutions)
- Citation needed: Specific claim that needs verification, or "None"

Respond in JSON:
{
  "evolution_points": [
    {
      "year": "Year or era",
      "breakthrough": "Name (max 12 words)",
      "impact": "2-3 sentences (max 60 words)",
      "key_figures": ["Name 1", "Name 2"],
      "citation_needed": "Specific claim needing verification or 'None'"
    }
  ]
}

Provide 4-7 evolution points chronologically. Include at least one setback/stagnation if applicable.""",

            # Prompt 3: Current state with SOTA and research frontiers
            """You are a research analyst providing a state-of-the-field assessment of '{{topic}}'.

Analyze the current state (as of 2024-2025) with precision.

Provide:
1. **High-level summary** (3-4 sentences): Where does the field stand today?
2. **SOTA capabilities** (4-6 items): What can we do NOW that we couldn't 5 years ago?
3. **Research gaps** (3-5 items): What major questions remain unsolved?
4. **Current limitations** (3-5 items): What are the hard blockers?
5. **Consensus level**: How much agreement exists on the path forward?

Example SOTA capability for "Gene Editing":
✅ GOOD: "Prime editing allows precise DNA changes without double-strand breaks, achieving ~90% efficiency in some cell types (2024)"
❌ BAD: "Gene editing is really advanced now" (too vague)

Example research gap:
✅ GOOD: "No reliable method for in vivo editing of neuronal cells in adult humans without viral vectors"
❌ BAD: "Brain editing is hard" (not specific)

Respond in JSON:
{
  "current_state_summary": "3-4 sentence overview (max 100 words)",
  "sota_capabilities": [
    "Specific capability 1 with metric/date if possible (max 30 words)",
    "Specific capability 2...",
    "(provide 4-6 total)"
  ],
  "research_gaps": [
    "Specific unsolved problem 1 (max 25 words)",
    "Specific unsolved problem 2...",
    "(provide 3-5 total)"
  ],
  "limitations": [
    "Specific limitation 1 (max 25 words)",
    "Specific limitation 2...",
    "(provide 3-5 total)"
  ],
  "consensus_level": "High/Medium/Low - [1 sentence explaining why]"
}

Be specific. Include years/dates where possible. Avoid vague statements.""",

            # Prompt 4: Future trajectories with scenarios
            """You are a technology forecaster analyzing possible futures for '{{topic}}'.

Project plausible trajectories over the next 20 years (2025-2045).

Provide:
1. **Near-term (5 years)**: Likely developments based on current trends
2. **Long-term (20 years)**: Speculative but plausible scenarios
3. **Wildcards** (2-4 items): Low-probability, high-impact disruptions
4. **Risks** (3-5 items): Systemic dangers or failure modes

Example "Wildcard" for "Quantum Computing":
✅ GOOD: "Room-temperature superconductors discovered, eliminating cooling requirements and enabling desktop quantum computers"
❌ BAD: "Quantum computers get better" (not a wildcard, just trend)

Example "Risk" for "AI Systems":
✅ GOOD: "Automated systems become too complex to audit, leading to undetectable bias in critical decisions (hiring, loans, parole)"
❌ BAD: "AI might be dangerous" (too vague)

Respond in JSON:
{
  "near_term_prediction": "2-3 sentence projection for next 5 years (max 75 words)",
  "long_term_speculation": "3-4 sentence scenario for 20 years (max 100 words)",
  "wildcards": [
    "Low-probability, high-impact event 1 (max 30 words)",
    "Wildcard 2...",
    "(provide 2-4 total)"
  ],
  "risks": [
    "Specific systemic risk 1 (max 30 words)",
    "Risk 2...",
    "(provide 3-5 total)"
  ]
}

Wildcards should be surprising but not science fiction. Risks should be systemic/structural, not obvious."""
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
