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
            # Prompt 1: User Intent Analysis with real search psychology
            """You are a content strategist with 10+ years in audience research and search intent analysis.

Analyze '{{topic}}' by thinking through what brings people to search for this information.

Consider THREE specific user modes:

**Mode 1: Discovery/Panic** (just realized they need this)
- What problem just surfaced? (broke something, got feedback, saw competitor doing it)
- What's their emotional state? (confused, overwhelmed, urgent need)
- What false assumptions do they hold?

**Mode 2: Stuck/Frustrated** (tried something, hit a wall)
- What specific step are they failing at?
- What worked in theory but failed in practice?
- What error messages or symptoms are they seeing?

**Mode 3: Optimization** (doing it now, seeking mastery)
- What separates "good enough" from "great"?
- What edge cases or tradeoffs matter?
- What tribal knowledge isn't in the docs?

Example pain point for "Database Indexing":
✅ GOOD: "Query was fast in dev (1000 rows) but times out in production (10M rows). Don't know if it's indexing, query structure, or both."
❌ BAD: "Databases are slow" (too vague, no context)

Example search query:
✅ GOOD: "postgres index not being used explain analyze"
❌ BAD: "how to use database" (too generic)

Respond in JSON:
{
  "user_intent": "The core problem in 1-2 sentences with emotional context (max 50 words)",
  "search_patterns": [
    "Actual frustrated search query 1 (something real users would type)",
    "Query 2 (different angle)...",
    "(provide exactly 5 search patterns covering all 3 user modes)"
  ],
  "pain_points": [
    "Specific pain point 1 with context (max 35 words)",
    "Pain point 2...",
    "(provide exactly 5 pain points, at least one per user mode)"
  ],
  "knowledge_gaps": [
    "Specific gap 1 (max 25 words)",
    "Gap 2...",
    "(provide exactly 4 gaps)"
  ],
  "audience_segments": [
    {"segment": "Discovery/Panic", "needs": "What they need to move forward (max 35 words)"},
    {"segment": "Stuck/Frustrated", "needs": "What will unstick them (max 35 words)"},
    {"segment": "Optimization", "needs": "What will level them up (max 35 words)"}
  ]
}

Be ruthlessly specific. Use real scenarios with context, not abstract statements.""",

            # Prompt 2: Competitive Analysis with steel-manning
            """You are a content analyst evaluating the top existing guides on '{{topic}}'.

Use the "steel-man" technique: Assume the best existing content was created by competent people solving real problems. What did they get RIGHT? Only then identify gaps.

For existing content, analyze:
1. **Strengths**: What do good guides do well? Be specific.
2. **Weaknesses**: Where do they fall short? Not malice, but gaps.
3. **Overused angles**: What approaches are tired/saturated?

Then identify differentiation:
- What unique value can we add?
- What perspective is missing?
- Why would someone bookmark THIS guide vs existing ones?

Example strength for "Git Tutorials":
✅ GOOD: "Interactive visualizations showing how branches diverge and merge make concepts tangible"
❌ BAD: "Good explanations" (too vague)

Example gap:
✅ GOOD: "Tutorials assume linear progression but never cover recovering from common mistakes (wrong branch, committed secrets, rebased published history)"
❌ BAD: "Not detailed enough" (not actionable)

Example differentiation:
✅ GOOD: "We'll provide a 'troubleshooting decision tree' for the 10 most common mistakes, linking to recovery steps"
❌ BAD: "We'll be better" (empty promise)

Respond in JSON:
{
  "what_exists": {
    "strengths": [
      "Specific strength 1 with example (max 30 words)",
      "Strength 2...",
      "(provide exactly 3-4 strengths)"
    ],
    "weaknesses": [
      "Specific gap 1 with impact (max 30 words)",
      "Gap 2...",
      "(provide exactly 3-4 gaps)"
    ],
    "overused_angles": [
      "Tired approach 1 (max 20 words)",
      "Approach 2...",
      "(provide exactly 2-3)"
    ]
  },
  "differentiation_opportunity": "How we add unique value in 2-3 sentences (max 60 words)",
  "unique_perspective": "Our specific angle or insight in 1 sentence (max 25 words)",
  "why_readers_would_bookmark": "Concrete utility (max 30 words) - be specific about what action/outcome they get"
}

Be specific. Explain WHY something is valuable, not just that it is.""",

            # Prompt 3: Structure with skimmability and utility
            """You are an information architect specializing in educational content.

Create a structured outline for '{{topic}}' optimized for FOUR goals:

1. **Utility** - Reader gets value even if they only read 20%
2. **Skimmability** - Headings convey meaning, not just topics
3. **Depth** - Goes beyond surface-level listicles
4. **Actionability** - Every section answers "what should I do?"

Writing constraints:
- Tone: {{tone}}
- Avoid: {{avoid}}
- Prefer: {{prefer}}

Key insights from previous analysis:
- User intent: {{output[-2].user_intent}}
- Differentiation: {{output[-1].differentiation_opportunity}}

Output size budgets:
- Title options: exactly 3
- Sections: 4-6 major sections
- Subsections per section: 2-4
- Key points per section: 2-4
- Metaphors: 2-3 total (only for complex concepts)
- Practical takeaways: 4-6

Example of skimmable heading:
✅ GOOD: "Diagnose slow queries in under 10 minutes (3-step checklist)"
❌ BAD: "Performance" (no value promised)

Example of metaphor:
✅ GOOD:
- Concept: "Database indexes"
- Metaphor: "Like a book index - you jump to the right page instead of reading cover to cover"
- Why it works: "Everyone knows book indexes, maps unfamiliar tech to familiar tool"

❌ BAD:
- Metaphor: "Indexes are like magic" (not concrete)

Respond in JSON:
{
  "title_options": [
    "Title 1 (promise outcome or solve problem)",
    "Title 2 (alternative angle)...",
    "(exactly 3 options)"
  ],
  "subtitle": "One-line value proposition answering 'what will I gain?' (max 15 words)",
  "outline": [
    {
      "section": "Section heading (promises outcome, max 10 words)",
      "why_it_matters": "What problem this solves (1 sentence, max 25 words)",
      "subsections": ["Subsection 1", "Subsection 2"],
      "key_points": ["Specific point 1", "Point 2"],
      "metaphor_opportunity": "Where to use analogy if concept is abstract, or 'None'",
      "research_needed": ["Citation 1", "Citation 2", "or 'None'"]
    },
    "(provide 4-6 major sections)"
  ],
  "key_metaphors": [
    {
      "concept": "Abstract concept needing explanation",
      "metaphor": "Concrete analogy (2-3 sentences)",
      "why_it_works": "Why this makes it clearer (1 sentence)"
    },
    "(provide 2-3 metaphors only for genuinely complex concepts)"
  ],
  "practical_takeaways": [
    "Actionable takeaway 1 (verb-led, max 15 words)",
    "Takeaway 2...",
    "(provide 4-6)"
  ],
  "skimmability_score": "7-10 (rate how well headings convey value)",
  "estimated_depth_level": "Beginner/Intermediate/Advanced"
}

Every heading should promise an outcome or answer a question. No generic topic headings.""",

            # Prompt 4: Evergreen Audit with time-sensitivity assessment
            """You are a content strategist evaluating '{{topic}}' for longevity (will this be useful in 5 years?).

Review the outline from the previous step and categorize every claim as:
- **Evergreen**: Principle-based, won't change (fundamental truths, human behavior, physics)
- **Time-sensitive**: Will age (versions, current tools, statistics, "best practices" that shift)

For time-sensitive elements, provide mitigation strategies.

Examples:

❌ **Time-sensitive** (needs flagging):
"In 2024, React 18 is the best frontend framework"
- Why it ages: Framework popularity shifts every 2-3 years
- Mitigation: "As of 2024, React dominates (60% market share), but framework choices evolve. Focus on: [timeless principle about component architecture]"
- Update trigger: "Major new framework gains >20% adoption"

✅ **Evergreen** (keep as-is):
"Readable code is more valuable than clever code"
- This is a principle that won't change with technology

Another example:

❌ **Time-sensitive**:
"ChatGPT costs $20/month for Pro"
- Mitigation: Add date and link: "Pricing as of Jan 2025 (latest pricing)" with update trigger

✅ **Evergreen**:
"LLMs have context length limitations that affect conversation design"
- True regardless of specific models or token counts

Respond in JSON:
{
  "evergreen_score": "7-10 (how much of the guide is principle-based?)",
  "time_sensitive_claims": [
    {
      "claim": "Exact quote from outline that will age",
      "why_it_will_age": "Specific reason (tech changes/stats update/version releases) (max 25 words)",
      "mitigation": "How to reframe as principle OR how to date it properly (max 40 words)",
      "update_trigger": "Specific event requiring revision (max 15 words)"
    },
    "(provide 3-6 time-sensitive claims from the outline)"
  ],
  "universal_principles": [
    "Timeless principle 1 that won't change in 10 years",
    "Principle 2...",
    "(provide 4-6 universal principles to emphasize)"
  ],
  "update_schedule_recommendation": "Review every [X] months - explain why this cadence",
  "longevity_improvements": [
    "Specific suggestion 1 to make more timeless (max 25 words)",
    "Suggestion 2...",
    "(provide 3-4 improvements)"
  ]
}

Quote actual claims from the outline. Be specific about what will age and why.""",

            # Prompt 5: Final quality check with clear success criteria
            """You are a senior editor evaluating whether '{{topic}}' outline is publish-ready.

Apply these FIVE quality criteria rigorously:

1. **Utility**: Does this solve real problems (not just educate)?
2. **Clarity**: Can a skimmer understand value without reading everything?
3. **Depth**: Does this go beyond surface-level advice? Are tradeoffs discussed?
4. **Actionability**: Can the reader DO something specific after reading?
5. **Longevity**: Will this be useful in 3-5 years?

Use the "Would I bookmark this?" test:
- If I Google this topic again in 6 months, would I come back to THIS guide?
- What would make me choose this over competitors?
- Is there a specific problem this solves better than anything else?

Example of actionability:
✅ GOOD: "Run this 10-minute diagnostic: (1) Check query execution plan, (2) Identify sequential scans, (3) Add indexes for top 3 slowest queries"
❌ BAD: "Improve your database performance" (no concrete steps)

Example of depth:
✅ GOOD: "Caching speeds reads but complicates invalidation. Use it when read:write ratio > 10:1. If lower, optimize queries first."
❌ BAD: "Caching is good for performance" (no tradeoff discussed)

Respond in JSON:
{
  "overall_quality_score": "7-10 with brief justification",
  "would_bookmark": "true/false with 1-sentence reason why or why not",
  "strengths": [
    "Specific strength 1 (max 25 words)",
    "Strength 2...",
    "(provide exactly 3-4)"
  ],
  "gaps_to_address": [
    "Specific gap 1 with suggested fix (max 30 words)",
    "Gap 2...",
    "(provide exactly 2-4 gaps)"
  ],
  "writing_priorities": [
    "Specific thing to emphasize when writing (max 20 words)",
    "Specific thing to de-emphasize or cut (max 20 words)",
    "(provide exactly 3-4 priorities)"
  ],
  "success_metrics": {
    "good": "Concrete outcome for 'good' (reader does X)",
    "great": "Concrete outcome for 'great' (reader achieves Y)",
    "exceptional": "Concrete outcome for 'exceptional' (reader enables Z)"
  },
  "estimated_word_count": "Range (e.g., 2000-2500 words) based on outline depth",
  "estimated_reading_time": "X-Y minutes"
}

Be honest. If it's not bookmark-worthy, explain what's missing specifically."""
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
