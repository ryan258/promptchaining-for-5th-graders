#!/usr/bin/env python3
"""
🌲 Evergreen Guide Architect

Transforms topics or rough notes into structured, useful, lasting guide outlines.
Optimizes for utility and longevity over virality.

Usage:
    # Interactive mode - paste multi-line content, press Ctrl+D when done
    python tools/content/evergreen_guide.py

    # Editor mode - opens in $EDITOR (vim, nano, etc.)
    python tools/content/evergreen_guide.py --editor

    # Single-line topic
    python tools/content/evergreen_guide.py "Topic name"

    # From piped input
    cat notes.txt | python tools/content/evergreen_guide.py

    # With additional context
    python tools/content/evergreen_guide.py "Topic" --context "Additional context"
"""

import sys
import os
from datetime import datetime

# Setup project root and import shared tools
try:
    from tools.tool_utils import setup_project_root, load_user_context, get_input_from_args
except ImportError:
    # Fallback if running directly from tools/content/
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
    from tools.tool_utils import setup_project_root, load_user_context, get_input_from_args

project_root = setup_project_root(__file__)

from chain import MinimalChainable
from main import build_models, prompt

def evergreen_guide_architect(topic, additional_context=""):
    """Generate evergreen guide outline optimized for depth and longevity"""

    print(f"🌲 Evergreen Guide Architect")
    print(f"📝 Topic: {topic}\n")

    # Load user context
    user_profile = load_user_context(project_root)
    writing_style = user_profile.get('writing_style', {})
    tone = writing_style.get('tone', 'Practical')

    client, model_names = build_models()
    selected_model_name = model_names[0]
    model_info = (client, selected_model_name)

    # Enhanced context with user preferences
    context_data = {
        "topic": topic,
        "additional_notes": additional_context,
        "tone": tone,
        "avoid": ", ".join(writing_style.get('avoid', [])),
        "prefer": ", ".join(writing_style.get('prefer', []))
    }

    result, context_filled_prompts, usage_stats = MinimalChainable.run(
        context=context_data,
        model=model_info,
        callable=prompt,
        prompts=[
            # Prompt 1: User Intent & Pain Points Analysis
            """You are a content strategist (10 years in SEO + user research). Analyze '{{topic}}' strictly through reader intent.

Provide 3-5 pain points and search patterns for three modes:
- Beginner panic (first time searching)
- Stuck/frustrated practitioner (mid-way, hitting blockers)
- Optimizer/refiner (improving an existing approach)

Show one GOOD vs BAD intent example:
GOOD: "I keep breaking form on rep #6; how do I stop that?" (specific, stakes)
BAD: "Tell me about fitness" (too broad)

Respond in JSON (keep lists 3-5 items each):
{
  "user_intent": "Primary problem they're solving",
  "search_patterns": ["query 1", "query 2", "query 3"],
  "pain_points": ["pain point 1", "pain point 2", "pain point 3"],
  "knowledge_gaps": ["gap 1", "gap 2"],
  "audience_segments": [
    {"segment": "Beginner panic", "needs": "2-3 needs"},
    {"segment": "Stuck practitioner", "needs": "2-3 needs"},
    {"segment": "Optimizer", "needs": "2-3 needs"}
  ]
}""",

            # Prompt 2: Competition Steel-Man & Differentiation
            """You are comparing against the top 3 guides on '{{topic}}'.
Steel-man them (assume competence). Then find gaps.

Example of steel-man strength: "Great walkthrough with screenshots for setup"
Example of gap: "No troubleshooting section; assumes ideal path"

Respond in JSON (keep 3-5 items max per list):
{
  "what_exists": {
    "strengths": ["What good guides do well"],
    "weaknesses": ["Common gaps or superficial treatments"],
    "overused_angles": ["Tired approaches"]
  },
  "differentiation_opportunity": "How we can add unique value",
  "unique_perspective": "Our specific angle or insight",
  "why_readers_would_bookmark": "Specific utility this guide provides"
}""",

            # Prompt 3: Structure for Utility & Skimmability
            """Create a structured outline for '{{topic}}' optimized for:
1. Utility (value even if they read only 20%)
2. Skimmability (headings that convey meaning; bullets 7 words max)
3. Depth (go beyond listicles)
4. Actionability (clear next steps)

Writing tone: {{tone}}
Avoid: {{avoid}}
Prefer: {{prefer}}

Use size budgets:
- Title options: 3
- Metaphors: max 3, memorable and specific
- Key points per section: 2-4
- Takeaways: 3-5

Include one GOOD vs BAD example of a skimmable heading:
GOOD: "Diagnose slow queries in 5 minutes"
BAD: "Performance tips"

Respond in JSON: {
  "title_options": ["title 1", "title 2", "title 3"],
  "subtitle": "One-line value proposition",
  "outline": [
    {
      "section": "Section Title",
      "why_it_matters": "Purpose of this section",
      "subsections": ["Subsection 1", "Subsection 2"],
      "key_points": ["Point 1", "Point 2"],
      "metaphor_opportunity": "Where to use analogy",
      "research_needed": ["Citation 1", "Citation 2"]
    }
  ],
  "key_metaphors": [
    {
      "concept": "What needs explanation",
      "metaphor": "Analogy to use",
      "why_it_works": "Makes X relatable"
    }
  ],
  "practical_takeaways": ["Actionable insight 1", "Actionable insight 2"],
  "skimmability_score": 0-10,
  "estimated_depth_level": "Intermediate/Advanced/etc"
}""",

            # Prompt 4: The Evergreen Audit
            """Review the outline for '{{topic}}' through the lens of longevity. Label claims as Evergreen vs Time-sensitive.

Examples:
❌ Time-sensitive to flag: "In 2024, React 18 is best-in-class"
✅ Evergreen to keep: "Readable code beats premature optimization"

For each time-sensitive item, include the exact quote + why it will age + mitigation.

Respond in JSON:
{
  "evergreen_score": 0-10,
  "time_sensitive_claims": [
    {
      "claim": "Exact quote",
      "why_it_will_age": "Specific reason",
      "mitigation": "How to reframe or date",
      "update_trigger": "Event that requires revision"
    }
  ],
  "universal_principles": [
    "Principle 1 that won't change",
    "Principle 2 that won't change"
  ],
  "update_schedule_recommendation": "Review every X months",
  "longevity_improvements": [
    "Suggestion 1 to make more timeless",
    "Suggestion 2"
  ]
}""",

            # Prompt 5: Final Polish & Meta-Quality Check
            """Final quality check for the '{{topic}}' guide outline.

Use these criteria:
- Utility: real problems solved, not trivia
- Clarity: skimmable headings with meaning
- Depth: beyond listicles; includes trade-offs
- Actionability: clear next steps
- Longevity: principles over tactics

Provide one GOOD vs BAD call-to-action example:
GOOD: "Run this 10-minute diagnostic to find your bottleneck"
BAD: "Check performance regularly"

Respond in JSON:
{
  "overall_quality_score": 0-10,
  "would_bookmark": true/false,
  "strengths": ["Strength 1", "Strength 2"],
  "gaps_to_address": ["Gap 1", "Gap 2"],
  "writing_priorities": [
    "What to emphasize when writing",
    "What to de-emphasize"
  ],
  "success_metrics": {
    "good": "Reader completes one action",
    "great": "Reader bookmarks for future reference",
    "exceptional": "Reader shares with others"
  },
  "estimated_word_count": "2000-2500 words",
  "estimated_reading_time": "10-12 minutes"
}"""
        ],
        return_usage=True,
    )

    # Save output
    output_dir = os.path.join(project_root, 'output', 'guides')
    os.makedirs(output_dir, exist_ok=True)

    # Generate filename from topic
    safe_topic = "".join(c for c in topic if c.isalnum() or c in (' ', '-', '_')).strip()
    safe_topic = safe_topic.replace(' ', '-').lower()[:50]
    timestamp = datetime.now().strftime("%Y%m%d-%H%M")

    output_file = os.path.join(output_dir, f"{timestamp}-{safe_topic}.md")

    # Format as markdown
    markdown_output = format_as_markdown(topic, result)

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(markdown_output)

    print(f"\n✅ Guide outline saved to: {output_file}")

    # Also log to standard logging
    log_file = MinimalChainable.log_to_markdown("evergreen_guide", context_filled_prompts, result, usage_stats)
    print(f"✅ Full chain log saved to: {log_file}")

    # Print summary to console
    print("\n" + "="*60)
    print("📊 SUMMARY")
    print("="*60)

    try:
        final_check = result[-1]
        print(f"\n🎯 Overall Quality Score: {final_check.get('overall_quality_score', 'N/A')}/10")
        print(f"📚 Estimated Length: {final_check.get('estimated_word_count', 'N/A')}")
        print(f"⏱️  Reading Time: {final_check.get('estimated_reading_time', 'N/A')}")
        print(f"🔖 Bookmark-worthy: {'Yes' if final_check.get('would_bookmark') else 'No'}")

        if final_check.get('strengths'):
            print(f"\n💪 Strengths:")
            for strength in final_check['strengths']:
                print(f"   • {strength}")

        if final_check.get('gaps_to_address'):
            print(f"\n⚠️  Gaps to Address:")
            for gap in final_check['gaps_to_address']:
                print(f"   • {gap}")
    except (IndexError, KeyError, TypeError) as e:
        print(f"\n⚠️  Could not parse summary: {e}")

    print("\n" + "="*60)
    print(f"✨ Ready to write! Open: {output_file}")
    print("="*60)

    return output_file

def format_as_markdown(topic, chain_results):
    """Format chain results as readable markdown outline"""

    md = f"""# Evergreen Guide Outline: {topic}

Generated: {datetime.now().strftime("%Y-%m-%d %H:%M")}

---

## 📊 Analysis Summary

### User Intent & Pain Points
"""

    try:
        analysis = chain_results[0]
        md += f"\n**Primary Intent**: {analysis.get('user_intent', 'N/A')}\n\n"

        if analysis.get('pain_points'):
            md += "**Pain Points**:\n"
            for pain in analysis['pain_points']:
                md += f"- {pain}\n"

        if analysis.get('search_patterns'):
            md += "\n**Common Searches**:\n"
            for search in analysis['search_patterns']:
                md += f"- \"{search}\"\n"
    except (IndexError, KeyError, TypeError):
        md += "*Analysis data unavailable*\n"

    md += "\n---\n\n## 🎯 Differentiation Strategy\n\n"

    try:
        diff = chain_results[1]
        md += f"**Unique Angle**: {diff.get('unique_perspective', 'N/A')}\n\n"
        md += f"**Why Readers Will Bookmark**: {diff.get('why_readers_would_bookmark', 'N/A')}\n"
    except (IndexError, KeyError, TypeError):
        md += "*Differentiation data unavailable*\n"

    md += "\n---\n\n## 📝 Content Outline\n\n"

    try:
        structure = chain_results[2]

        if structure.get('title_options'):
            md += "**Title Options**:\n"
            for i, title in enumerate(structure['title_options'], 1):
                md += f"{i}. {title}\n"
            md += "\n"

        if structure.get('subtitle'):
            md += f"**Subtitle**: {structure['subtitle']}\n\n"

        if structure.get('outline'):
            md += "### Structure\n\n"
            for section in structure['outline']:
                md += f"#### {section.get('section', 'Section')}\n\n"
                md += f"*Purpose*: {section.get('why_it_matters', 'N/A')}\n\n"

                if section.get('subsections'):
                    md += "**Subsections**:\n"
                    for sub in section['subsections']:
                        md += f"- {sub}\n"
                    md += "\n"

                if section.get('key_points'):
                    md += "**Key Points**:\n"
                    for point in section['key_points']:
                        md += f"- {point}\n"
                    md += "\n"

                if section.get('research_needed'):
                    md += "**Research Needed**:\n"
                    for research in section['research_needed']:
                        md += f"- [ ] {research}\n"
                    md += "\n"

                md += "---\n\n"

        if structure.get('key_metaphors'):
            md += "### 🎨 Key Metaphors\n\n"
            for metaphor in structure['key_metaphors']:
                md += f"**{metaphor.get('concept', 'Concept')}**\n"
                md += f"- Metaphor: {metaphor.get('metaphor', 'N/A')}\n"
                md += f"- Why it works: {metaphor.get('why_it_works', 'N/A')}\n\n"
    except (IndexError, KeyError, TypeError):
        md += "*Structure data unavailable*\n"

    md += "\n---\n\n## ♻️  Evergreen Audit\n\n"

    try:
        audit = chain_results[3]
        md += f"**Evergreen Score**: {audit.get('evergreen_score', 'N/A')}/10\n\n"

        if audit.get('universal_principles'):
            md += "**Timeless Principles**:\n"
            for principle in audit['universal_principles']:
                md += f"- {principle}\n"
            md += "\n"

        if audit.get('time_sensitive_claims'):
            md += "**Time-Sensitive Elements** (flag for updates):\n"
            for claim in audit['time_sensitive_claims']:
                md += f"- {claim.get('claim', 'Claim')}\n"
                md += f"  - Mitigation: {claim.get('mitigation', 'N/A')}\n"
                md += f"  - Update trigger: {claim.get('update_trigger', 'N/A')}\n"
            md += "\n"

        md += f"**Recommended Review Schedule**: {audit.get('update_schedule_recommendation', 'Annually')}\n"
    except (IndexError, KeyError, TypeError):
        md += "*Audit data unavailable*\n"

    md += "\n---\n\n## ✅ Quality Metrics\n\n"

    try:
        quality = chain_results[4]
        md += f"**Overall Score**: {quality.get('overall_quality_score', 'N/A')}/10\n"
        md += f"**Bookmark-Worthy**: {'✅ Yes' if quality.get('would_bookmark') else '❌ No'}\n\n"

        if quality.get('strengths'):
            md += "**Strengths**:\n"
            for strength in quality['strengths']:
                md += f"- {strength}\n"
            md += "\n"

        if quality.get('writing_priorities'):
            md += "**Writing Priorities**:\n"
            for priority in quality['writing_priorities']:
                md += f"- {priority}\n"
            md += "\n"

        md += f"**Target Length**: {quality.get('estimated_word_count', 'N/A')}\n"
        md += f"**Reading Time**: {quality.get('estimated_reading_time', 'N/A')}\n"
    except (IndexError, KeyError, TypeError):
        md += "*Quality data unavailable*\n"

    md += "\n---\n\n## 🚀 Next Steps\n\n"
    md += "1. Review outline and adjust structure as needed\n"
    md += "2. Complete research citations marked above\n"
    md += "3. Write first draft following the priorities\n"
    md += "4. Test metaphors with target audience\n"
    md += "5. Schedule evergreen audit review\n"

    return md

def main():
    topic, context = get_input_from_args(
        description="Generate evergreen guide outlines optimized for depth and longevity"
    )
    evergreen_guide_architect(topic, context)

if __name__ == "__main__":
    main()
