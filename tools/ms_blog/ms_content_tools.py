"""
MS Blog Content Generation Tools
==================================

Low-Energy Content Pipeline for generating MS-focused content with minimal cognitive load.

This module provides automated content generation for:
- Prompt Cards: AI prompts solving MS-related problems
- Shortcut Spotlights: Accessibility-focused tool tutorials
- Multi-Phase Guides: Comprehensive system setup guides
- Content Ideas: Brainstorming and topic expansion

All generators use prompt chaining for emergent insights and high-quality output.
"""

import os
import sys
import json
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime
from pathlib import Path

# Add project root to path for imports
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from src.core.chain import MinimalChainable
from src.core.main import build_models, prompt
from tools.tool_utils import load_user_context


# ============================================================================
# BASE UTILITIES
# ============================================================================

def get_model():
    """Get the default model for content generation."""
    client, model_names = build_models()
    # Use a capable model for content generation
    return (client, model_names[0])


def save_markdown(content: str, output_path: str) -> str:
    """Save generated markdown content to file."""
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, 'w') as f:
        f.write(content)
    return output_path


def sanitize_filename(title: str, prefix: str = "untitled") -> str:
    """
    Convert title to safe filename with fallback for invalid titles.

    Args:
        title: The title to sanitize
        prefix: Prefix to use if title contains only special characters

    Returns:
        Safe filename ending in .md
    """
    safe_title = "".join(c for c in title if c.isalnum() or c in (' ', '-', '_')).rstrip()
    if safe_title:
        return f"{safe_title.lower().replace(' ', '-')}.md"
    # Fallback for titles with only special characters
    return f"{prefix}-{datetime.now().strftime('%Y%m%d-%H%M%S')}.md"


def validate_content(content: str, content_type: str) -> Dict[str, Any]:
    """
    Validate generated content meets quality standards.

    Returns:
        Dict with validation results: {
            'valid': bool,
            'issues': List[str],
            'warnings': List[str]
        }
    """
    issues = []
    warnings = []

    # Check for minimum length
    if len(content) < 500:
        issues.append(f"Content too short ({len(content)} chars, minimum 500)")

    # Check for required sections based on type
    if content_type == "prompt_card":
        required = ["##", "Problem", "Prompt", "Examples"]
        for req in required:
            if req not in content:
                issues.append(f"Missing required section: {req}")

    elif content_type == "shortcut":
        required = ["##", "Why", "How", "Use Case"]
        for req in required:
            if req not in content:
                warnings.append(f"Recommended section missing: {req}")

    elif content_type == "guide":
        required = ["##", "Quick Path", "Phase", "Troubleshooting"]
        for req in required:
            if req not in content:
                warnings.append(f"Recommended section missing: {req}")

    # Check for front matter (YAML)
    if not content.startswith("---"):
        warnings.append("No YAML front matter detected")

    return {
        'valid': len(issues) == 0,
        'issues': issues,
        'warnings': warnings
    }


# ============================================================================
# PROMPT CARD GENERATOR
# ============================================================================

def generate_prompt_card(
    problem: str,
    target_audience: str = "People with MS experiencing cognitive challenges",
    energy_level: str = "medium",
    additional_context: str = ""
) -> Tuple[str, Dict[str, Any]]:
    """
    Generate a complete prompt card for MS-related problem.

    Args:
        problem: The MS-related problem to solve (e.g., "I get overwhelmed planning my day")
        target_audience: Who this prompt is for
        energy_level: "low", "medium", or "high" - affects detail level
        additional_context: Extra context or constraints

    Returns:
        Tuple of (markdown_content, metadata)
    """
    model_info = get_model()

    # Design the prompt chain for generating a prompt card
    prompts = [
        # Step 1: Analyze the problem deeply
        f"""Analyze this MS-related problem: "{problem}"

Target audience: {target_audience}
Additional context: {additional_context}

Provide a structured analysis:
1. Core challenge: What's the root issue?
2. MS-specific considerations: How does MS make this harder? (brain fog, fatigue, mobility, etc.)
3. Cognitive load factors: What mental demands does this problem create?
4. Success criteria: What would a good solution achieve?

Format as JSON with keys: core_challenge, ms_factors, cognitive_load, success_criteria""",

        # Step 2: Design the solution prompt
        f"""Based on this analysis:
{{{{output[-1]}}}}

Design an AI prompt that solves this problem. The prompt should:
- Be clear and easy to use (minimal cognitive load)
- Account for MS-specific challenges
- Produce actionable, practical output
- Work well with AI assistants like ChatGPT or Claude

Format as JSON with keys:
- prompt_title: A clear, descriptive title
- prompt_text: The actual prompt to use
- why_it_works: Brief explanation of the approach
- accessibility_notes: How this helps with MS challenges""",

        # Step 3: Generate concrete examples
        f"""Using this prompt design:
{{{{output[-1]}}}}

And the original problem context:
{{{{output[-2]}}}}

Generate 2-3 concrete examples showing the prompt in action.
Each example should include:
- Input scenario: A specific situation
- How to use the prompt: What to fill in
- Expected output: What the AI will generate

Format as JSON with key 'examples' containing a list of example objects.""",

        # Step 4: Create variations and troubleshooting
        f"""Based on the prompt design:
{{{{output[-2]}}}}

Create:
1. Three variations of the prompt for different needs:
   - Quick version (low energy days)
   - Detailed version (when you need more)
   - Alternative approach (different angle)

2. Troubleshooting guide:
   - Common issues users might face
   - How to adjust the prompt
   - When to use which variation

Format as JSON with keys: variations (list), troubleshooting (list of objects with 'issue' and 'solution')""",

        # Step 5: Synthesize into complete markdown
        f"""Synthesize all previous outputs into a complete Hugo-compatible prompt card.

Analysis: {{{{output[-4]}}}}
Prompt Design: {{{{output[-3]}}}}
Examples: {{{{output[-2]}}}}
Variations & Troubleshooting: {{{{output[-1]}}}}

Original problem: "{problem}"
Target audience: {target_audience}

Generate a complete markdown document with:

1. YAML front matter:
---
title: "[Clear, SEO-friendly title]"
description: "[1-2 sentence meta description]"
date: {datetime.now().strftime('%Y-%m-%d')}
tags: ["prompts", "ms-tools", "[relevant-tag]"]
jtbd: "[Do/Decide/Write/Understand]"
difficulty: "[beginner/intermediate/advanced]"
energy_cost: "[low/medium/high]"
---

2. Problem Statement section (## The Problem)
3. Readiness checklist (## Before You Start)
4. The Prompt section (## The Prompt) with clear copy-paste formatting
5. Examples section (## Examples) with 2-3 real scenarios
6. Variations section (## Variations) with all three versions
7. Troubleshooting section (## Troubleshooting)
8. Related Resources section (## Related Resources)

Use accordion formatting where helpful for long sections.
Ensure accessibility: clear headings, simple language, good structure.
Focus on reducing cognitive load in presentation.

Return ONLY the complete markdown, ready to save as a .md file."""
    ]

    # Run the chain
    result, filled_prompts, usage, trace = MinimalChainable.run(
        context={},
        model=model_info,
        callable=prompt,
        return_trace=True,
        prompts=prompts
    )

    # Get the final output (result is a list of all outputs from each step)
    final_content = result[-1]

    # Extract metadata from the generation process
    metadata = {
        'type': 'prompt_card',
        'problem': problem,
        'target_audience': target_audience,
        'energy_level': energy_level,
        'generated_at': datetime.now().isoformat(),
        'token_usage': usage,
        'validation': validate_content(final_content, 'prompt_card')
    }

    # Log the generation
    MinimalChainable.log_to_markdown(
        "prompt_card_generator",
        filled_prompts,
        result,
        usage
    )

    return final_content, metadata


# ============================================================================
# SHORTCUT SPOTLIGHT GENERATOR
# ============================================================================

def generate_shortcut_spotlight(
    tool: str,
    ms_benefit: str,
    category: str = "automation",  # or "keyboard-shortcuts" or "system-instructions"
    additional_context: str = ""
) -> Tuple[str, Dict[str, Any]]:
    """
    Generate a complete shortcut spotlight article.

    Args:
        tool: The tool, feature, or technique to showcase
        ms_benefit: How this helps with MS symptoms
        category: Type of shortcut (automation/keyboard-shortcuts/system-instructions)
        additional_context: Extra details or constraints

    Returns:
        Tuple of (markdown_content, metadata)
    """
    model_info = get_model()

    prompts = [
        # Step 1: Research and understand the tool
        f"""Analyze this accessibility tool/technique: "{tool}"

Category: {category}
MS Benefit: {ms_benefit}
Additional context: {additional_context}

Provide:
1. What it is: Clear explanation of the tool/technique
2. Accessibility angle: Why it matters for MS (fatigue, mobility, cognitive load)
3. Energy savings: How much effort/energy does this save?
4. Who benefits most: Which MS symptoms does this address?

Format as JSON.""",

        # Step 2: Create step-by-step setup instructions
        f"""Based on this tool analysis:
{{{{output[-1]}}}}

Create detailed but clear setup instructions. Remember, users may have:
- Brain fog (need very clear steps)
- Fatigue (keep steps minimal)
- Mobility challenges (keyboard-focused when possible)

Generate:
1. Prerequisites: What they need before starting
2. Setup steps: Numbered, clear, one action per step
3. Verification: How to test it's working
4. Quick troubleshooting: Top 3 issues and fixes

Format as JSON with keys: prerequisites, setup_steps, verification, troubleshooting""",

        # Step 3: Generate practical use cases
        f"""Using the tool info and setup:
Tool: {{{{output[-2]}}}}
Setup: {{{{output[-1]}}}}

Generate 3-4 practical use cases showing when/how to use this.
Each use case should:
- Start with a relatable scenario
- Show the before (without this tool)
- Show the after (with this tool)
- Highlight the energy/effort saved

Format as JSON with key 'use_cases' as a list.""",

        # Step 4: Create comparison and recommendations
        f"""Based on all the info:
Tool analysis: {{{{output[-3]}}}}
Setup: {{{{output[-2]}}}}
Use cases: {{{{output[-1]}}}}

Create:
1. Before/After comparison: Quick visual of the improvement
2. Energy savings estimate: "Saves X minutes/Y mental energy per day"
3. Related shortcuts: 2-3 similar tools/techniques
4. Next steps: What to learn after mastering this

Format as JSON.""",

        # Step 5: Synthesize into markdown
        f"""Synthesize into a complete Hugo-compatible shortcut article.

Tool analysis: {{{{output[-4]}}}}
Setup instructions: {{{{output[-3]}}}}
Use cases: {{{{output[-2]}}}}
Comparison & recommendations: {{{{output[-1]}}}}

Original tool: "{tool}"
Category: {category}
MS Benefit: {ms_benefit}

Generate complete markdown with:

1. YAML front matter:
---
title: "[Tool Name]: [Clear Benefit]"
description: "[SEO-friendly description]"
date: {datetime.now().strftime('%Y-%m-%d')}
tags: ["shortcuts", "{category}", "accessibility"]
difficulty: "[beginner/intermediate/advanced]"
energy_cost: "[low/medium/high]"
time_to_setup: "[5min/15min/30min]"
---

2. Why It Matters (## Why This Matters for MS)
3. Quick Start (## Quick Start) - minimal steps for low-energy days
4. Detailed Setup (## Setup Guide) with step-by-step
5. Use Cases (## When to Use This) with 3-4 scenarios
6. Keyboard Shortcuts table (if applicable)
7. Troubleshooting (## Troubleshooting)
8. Before/After comparison
9. Related Resources

Use clear headings, simple language, and accessible formatting.
Include energy savings prominently.

Return ONLY the markdown."""
    ]

    result, filled_prompts, usage, trace = MinimalChainable.run(
        context={},
        model=model_info,
        callable=prompt,
        return_trace=True,
        prompts=prompts
    )

    # Get the final output (result is a list of all outputs from each step)
    final_content = result[-1]

    metadata = {
        'type': 'shortcut',
        'tool': tool,
        'category': category,
        'ms_benefit': ms_benefit,
        'generated_at': datetime.now().isoformat(),
        'token_usage': usage,
        'validation': validate_content(final_content, 'shortcut')
    }

    MinimalChainable.log_to_markdown(
        "shortcut_generator",
        filled_prompts,
        result,
        usage
    )

    return final_content, metadata


# ============================================================================
# MULTI-PHASE GUIDE GENERATOR
# ============================================================================

def generate_guide(
    system: str,
    complexity: str = "beginner",  # beginner/intermediate/advanced
    estimated_time: str = "30-45 minutes",
    additional_context: str = ""
) -> Tuple[str, Dict[str, Any]]:
    """
    Generate a complete multi-phase guide.

    Args:
        system: The system or workflow to teach
        complexity: Determines number of phases and detail level
        estimated_time: How long setup takes
        additional_context: Extra details

    Returns:
        Tuple of (markdown_content, metadata)
    """
    model_info = get_model()

    # Adjust number of phases based on complexity
    num_phases = {"beginner": 3, "intermediate": 4, "advanced": 5}[complexity]

    prompts = [
        # Step 1: Decompose the system
        f"""Analyze this system for MS users: "{system}"

Complexity: {complexity}
Estimated time: {estimated_time}
Context: {additional_context}

Break down this system into {num_phases} clear phases.
Each phase should:
- Have a clear goal
- Build on previous phases
- Be achievable on a moderate-energy day
- Include MS-friendly adaptations

Also identify:
- Prerequisites: What they need before starting
- Common failure points: Where people get stuck
- Success indicators: How to know it's working

Format as JSON with keys: phases (list), prerequisites, failure_points, success_indicators""",

        # Step 2: Create Quick Path (30-second version)
        f"""Based on this system breakdown:
{{{{output[-1]}}}}

Create an ultra-condensed "Quick Path" version for very low-energy days.
This should be:
- Absolute minimum steps to get something working
- 30 seconds to 2 minutes to read
- Skips explanations, just actions
- Good enough to start, even if not perfect

Format as JSON with key 'quick_path' containing the compressed steps.""",

        # Step 3: Expand each phase with details
        f"""Using the phase breakdown:
{{{{output[-2]}}}}

For each of the {num_phases} phases, create detailed content:
- Phase name and goal
- Step-by-step instructions (numbered)
- Why this matters (brief motivation)
- Common mistakes and how to avoid them
- Checkpoint: How to verify this phase is complete

Format as JSON with key 'detailed_phases' as a list of phase objects.""",

        # Step 4: Create Complete Prompt Kit
        f"""Based on the system:
{{{{output[-3]}}}}

Create a "Complete Prompt Kit" - a collection of AI prompts that help with this system.
Include prompts for:
- Planning/getting started
- Troubleshooting problems
- Customizing the system
- Maintaining it long-term

Each prompt should be copy-paste ready.

Format as JSON with key 'prompt_kit' as a list of prompt objects (title, prompt_text, when_to_use).""",

        # Step 5: Generate before/after and troubleshooting
        f"""Using all the information:
System: {{{{output[-4]}}}}
Phases: {{{{output[-2]}}}}
Prompts: {{{{output[-1]}}}}

Create:
1. Before/After narrative: Story of life before vs after this system
2. Troubleshooting checklist: Top 5-7 issues with solutions
3. Related resources: What to learn next, related guides/prompts
4. Adaptation tips: How to adjust for bad symptom days

Format as JSON.""",

        # Step 6: Synthesize into complete guide
        f"""Synthesize everything into a complete multi-phase guide.

System breakdown: {{{{output[-5]}}}}
Quick Path: {{{{output[-4]}}}}
Detailed phases: {{{{output[-3]}}}}
Prompt Kit: {{{{output[-2]}}}}
Before/After & troubleshooting: {{{{output[-1]}}}}

Original system: "{system}"
Complexity: {complexity}
Time: {estimated_time}

Generate complete markdown with:

1. YAML front matter:
---
title: "[System Name]: Complete Setup Guide"
description: "[SEO description]"
date: {datetime.now().strftime('%Y-%m-%d')}
tags: ["guides", "setup", "[relevant-tags]"]
jtbd: "[primary job to be done]"
difficulty: "{complexity}"
estimated_time: "{estimated_time}"
energy_cost: "medium"
---

2. Introduction (## What This Guide Does)
3. Before You Start (## Prerequisites)
4. Quick Path (## Quick Path: 30-Second Version) in accordion
5. The Full Guide (## The Complete Guide)
   - Phase 1: [Name]
   - Phase 2: [Name]
   - ... (all {num_phases} phases)
6. Complete Prompt Kit (## AI Prompts for This System)
7. Before & After (## How This Changes Things)
8. Troubleshooting (## Troubleshooting Checklist)
9. Related Resources (## What's Next)

Use accordions for long sections.
Clear headings, accessible formatting.
Emphasize what changes for low-energy days.

Return ONLY the markdown."""
    ]

    result, filled_prompts, usage, trace = MinimalChainable.run(
        context={},
        model=model_info,
        callable=prompt,
        return_trace=True,
        prompts=prompts
    )

    # Get the final output (result is a list of all outputs from each step)
    final_content = result[-1]

    metadata = {
        'type': 'guide',
        'system': system,
        'complexity': complexity,
        'estimated_time': estimated_time,
        'generated_at': datetime.now().isoformat(),
        'token_usage': usage,
        'validation': validate_content(final_content, 'guide')
    }

    MinimalChainable.log_to_markdown(
        "guide_generator",
        filled_prompts,
        result,
        usage
    )

    return final_content, metadata


# ============================================================================
# CONTENT IDEA EXPANDER
# ============================================================================

def expand_content_idea(
    seed: str,
    pillar: str = "All",  # Prompts/Shortcuts/Guides/Blog/All
    count: int = 10
) -> Tuple[Dict[str, List[Dict]], Dict[str, Any]]:
    """
    Generate multiple content ideas from a seed concept.

    Args:
        seed: The rough idea or problem area
        pillar: Which content type to focus on (or "All")
        count: Total number of ideas to generate

    Returns:
        Tuple of (ideas_dict, metadata)
        ideas_dict has keys: prompt_cards, shortcuts, guides, blog_posts
    """
    model_info = get_model()

    prompts = [
        # Step 1: Analyze the seed idea
        f"""Analyze this content seed idea: "{seed}"

Content pillar focus: {pillar}

Understand:
1. Core topic: What's the main subject?
2. MS relevance: How does this relate to MS challenges?
3. Potential angles: What different perspectives could we take?
4. User needs: What jobs-to-be-done does this address?
5. Search intent: What would people search for?

Format as JSON.""",

        # Step 2: Generate prompt card ideas
        f"""Based on this analysis:
{{{{output[-1]}}}}

Seed: "{seed}"

Generate 5 prompt card ideas. Each should:
- Solve a specific MS-related problem
- Be distinct from the others
- Have clear practical value
- Address different JTBD (Do/Decide/Write/Understand)

For each idea include:
- Title: Clear, benefit-focused
- Description: 1-2 sentences
- Problem it solves: The specific pain point
- JTBD tag: Which job-to-be-done
- Difficulty: beginner/intermediate/advanced
- Energy cost: low/medium/high
- SEO keywords: 2-3 search terms
- Priority score: 1-10 based on impact/effort

Format as JSON with key 'prompt_cards' as list.""",

        # Step 3: Generate shortcut spotlight ideas
        f"""Using the analysis:
{{{{output[-2]}}}}

Seed: "{seed}"

Generate 3 shortcut spotlight ideas - tools/techniques/automations.
Focus on accessibility wins and energy savings.

For each idea include:
- Title: Tool/technique name + benefit
- Description: What it does
- Category: automation/keyboard-shortcuts/system-instructions
- MS benefit: Which symptoms it helps with
- Setup time: Quick estimate
- Difficulty: beginner/intermediate/advanced
- Energy savings: Qualitative estimate
- SEO keywords: 2-3 terms
- Priority score: 1-10

Format as JSON with key 'shortcuts' as list.""",

        # Step 4: Generate guide ideas
        f"""Using the analysis:
{{{{output[-3]}}}}

Seed: "{seed}"

Generate 2 multi-phase guide ideas - comprehensive system setups.
These should be more involved than shortcuts but high-value.

For each idea include:
- Title: Clear, goal-focused
- Description: What you'll learn/build
- System overview: Brief explanation
- Complexity: beginner/intermediate/advanced
- Estimated time: Setup duration
- Prerequisites: What you need first
- Value proposition: Why spend the time
- SEO keywords: 2-3 terms
- Priority score: 1-10

Format as JSON with key 'guides' as list.""",

        # Step 5: Generate blog post idea
        f"""Using the analysis and all generated ideas:
Analysis: {{{{output[-4]}}}}
Prompt cards: {{{{output[-3]}}}}
Shortcuts: {{{{output[-2]}}}}
Guides: {{{{output[-1]}}}}

Seed: "{seed}"

Generate 1 blog post idea that could tie these together or explore the topic differently.
Format: Listicle, how-to, or thought leadership

Include:
- Title: Engaging, SEO-friendly
- Description: What it covers
- Format: Listicle/How-to/Opinion/Case-study
- Angle: Unique perspective
- Outline: 3-5 main sections
- SEO keywords: 3-5 terms
- Priority score: 1-10

Format as JSON with key 'blog_post'.""",

        # Step 6: Synthesize and prioritize
        f"""Compile all ideas with priority rankings:

Analysis: {{{{output[-5]}}}}
Prompt cards: {{{{output[-4]}}}}
Shortcuts: {{{{output[-3]}}}}
Guides: {{{{output[-2]}}}}
Blog post: {{{{output[-1]}}}}

Create final JSON output with:
{{
  "summary": {{
    "seed_idea": "{seed}",
    "total_ideas": {count},
    "top_priority": "...",  // Highest scoring idea overall
    "quick_wins": [...]  // 3 easiest/highest impact ideas
  }},
  "prompt_cards": [...],  // All 5 ideas
  "shortcuts": [...],  // All 3 ideas
  "guides": [...],  // All 2 ideas
  "blog_posts": [...],  // The 1 idea
  "gaps_identified": [...]  // What's missing from current coverage
}}

Return ONLY valid JSON."""
    ]

    result, filled_prompts, usage, trace = MinimalChainable.run(
        context={},
        model=model_info,
        callable=prompt,
        return_trace=True,
        prompts=prompts
    )

    # Get the final output (result is a list of all outputs from each step)
    final_output = result[-1] if result else None

    # Parse the JSON result (handle both string and dict responses)
    if isinstance(final_output, dict):
        # Already parsed
        ideas = final_output
    elif isinstance(final_output, str) and final_output:
        try:
            ideas = json.loads(final_output)
        except json.JSONDecodeError:
            # Try to extract JSON from markdown
            import re
            json_match = re.search(r'```json\s*(\{.*?\})\s*```', final_output, re.DOTALL)
            if json_match:
                ideas = json.loads(json_match.group(1))
            else:
                ideas = {"error": "Failed to parse JSON", "raw": final_output}
    else:
        # Empty or invalid response
        ideas = {"error": "Empty or invalid response", "type": str(type(final_output))}

    metadata = {
        'type': 'content_ideas',
        'seed': seed,
        'pillar': pillar,
        'count': count,
        'generated_at': datetime.now().isoformat(),
        'token_usage': usage
    }

    MinimalChainable.log_to_markdown(
        "content_idea_expander",
        filled_prompts,
        result,
        usage
    )

    return ideas, metadata


# ============================================================================
# BATCH CONTENT GENERATOR
# ============================================================================

# Default batch distribution percentages
BATCH_MIX_PROMPT = 0.5
BATCH_MIX_SHORTCUT = 0.3
BATCH_MIX_GUIDE = 0.2

def batch_generate_content(
    topic_area: str,
    count: int = 5,
    mix: Dict[str, int] = None,
    energy_level: str = "medium",
    output_dir: str = None
) -> Dict[str, Any]:
    """
    Generate multiple pieces of content in a batch.

    Args:
        topic_area: General topic (e.g., "Fatigue Management")
        count: Total items to generate (if mix not provided)
        mix: Dict of type -> count (e.g., {"prompt": 3, "shortcut": 2})
        energy_level: Energy level for generation
        output_dir: Directory to save content

    Returns:
        Summary of generated content
    """
    print(f"🚀 Starting batch generation for: {topic_area}")
    
    # Default mix if not provided
    if not mix:
        n_prompts = int(count * BATCH_MIX_PROMPT)
        n_shortcuts = int(count * BATCH_MIX_SHORTCUT)
        # Ensure at least one of each if count allows, otherwise fill remainder with guides
        remaining = count - n_prompts - n_shortcuts
        n_guides = max(0, remaining)
        
        mix = {
            "prompt": n_prompts,
            "shortcut": n_shortcuts,
            "guide": n_guides
        }

    results = {
        "generated": [],
        "errors": [],
        "summary": {"topic": topic_area, "total": 0}
    }

    # Step 1: Generate ideas first to ensure coherence
    print("  🧠 Brainstorming batch ideas...")
    # Generate extra ideas to ensure we have enough valid ones
    ideas, _ = expand_content_idea(topic_area, count=sum(mix.values()) + 3)
    
    # Process each type
    for content_type, num in mix.items():
        if num <= 0:
            continue
            
        print(f"  Processing {num} {content_type}(s)...")
        
        # Get relevant ideas safely
        type_key_map = {
            "prompt": "prompt_cards",
            "shortcut": "shortcuts",
            "guide": "guides"
        }
        type_key = type_key_map.get(content_type, f"{content_type}s")
        available_ideas = ideas.get(type_key, [])
        
        if not isinstance(available_ideas, list):
            available_ideas = []

        # Warn if insufficient ideas
        actual_count = min(num, len(available_ideas))
        if actual_count < num:
            print(f"    ⚠️  Warning: Only {actual_count} {content_type} ideas available (requested {num})")

        for i in range(actual_count):
            idea = available_ideas[i]
            # Handle potential missing keys or malformed idea objects
            if not isinstance(idea, dict):
                continue
                
            title = idea.get('title', 'Untitled')
            print(f"    - Generating: {title}")
            
            try:
                content = None
                metadata = None
                
                if content_type == "prompt":
                    content, metadata = generate_prompt_card(
                        problem=idea.get('problem', title),
                        energy_level=energy_level
                    )
                elif content_type == "shortcut":
                    content, metadata = generate_shortcut_spotlight(
                        tool=title,
                        ms_benefit=idea.get('ms_benefit', "Helps with MS symptoms"),
                        category=idea.get('category', "automation")
                    )
                elif content_type == "guide":
                    content, metadata = generate_guide(
                        system=title,
                        complexity=idea.get('difficulty', 'beginner'),
                        estimated_time="30 mins"
                    )
                
                if content and output_dir:
                    # Use shared sanitization utility
                    filename = sanitize_filename(title, prefix=content_type)
                    save_path = os.path.join(output_dir, filename)
                    save_markdown(content, save_path)
                    metadata['saved_to'] = save_path
                
                results["generated"].append({
                    "title": title,
                    "type": content_type,
                    "metadata": metadata
                })
                
            except Exception as e:
                print(f"    ❌ Error: {e}")
                results["errors"].append({"title": title, "error": str(e)})

    results["summary"]["total"] = len(results["generated"])
    print(f"✅ Batch complete! Generated {results['summary']['total']} items.")
    
    return results


# ============================================================================
# CONTENT CALENDAR GENERATOR
# ============================================================================

def generate_content_calendar(
    topic: str,
    duration: str = "1 month",
    frequency: str = "3x/week",
    start_date: str = None
) -> Dict[str, Any]:
    """
    Generate a content calendar.

    Args:
        topic: Main theme
        duration: How long (e.g., "1 month")
        frequency: Posting frequency
        start_date: YYYY-MM-DD string

    Returns:
        Calendar plan
    """
    model_info = get_model()
    start_date = start_date or datetime.now().strftime('%Y-%m-%d')

    prompts = [
        f"""You are a content strategist for an MS blog.
        
Create a content calendar.
Topic: {topic}
Duration: {duration}
Frequency: {frequency}
Start Date: {start_date}

Content types available:
- Prompt Cards (quick wins)
- Shortcut Spotlights (tools)
- Multi-Phase Guides (deep dives)

Design a schedule that balances:
- Energy levels (mix of simple and complex)
- Topic variety
- User journey (building skills over time)

Respond in JSON:
{{
  "strategy": "Brief strategy explanation",
  "schedule": [
    {{
      "week": 1,
      "theme": "Week's theme",
      "posts": [
        {{
          "day": "Monday",
          "date": "YYYY-MM-DD",
          "type": "prompt|shortcut|guide",
          "title": "Post title",
          "goal": "What this achieves"
        }}
      ]
    }}
  ]
}}"""
    ]

    result, _, usage, _ = MinimalChainable.run(
        context={},
        model=model_info,
        callable=prompt,
        return_trace=True,
        prompts=prompts
    )

    calendar = result[-1]
    
    # Log it
    MinimalChainable.log_to_markdown(
        "calendar_generator",
        prompts,
        result,
        usage
    )

    return calendar


# ============================================================================
# SEO OPTIMIZER
# ============================================================================

def optimize_content_seo(content: str, keywords: List[str] = None) -> str:
    """
    Optimize existing markdown content for SEO.
    
    Args:
        content: The markdown content to optimize
        keywords: List of target keywords (optional)
        
    Returns:
        Optimized markdown content
    """
    model_info = get_model()
    keywords_str = ", ".join(keywords) if keywords else "relevant MS and accessibility keywords"

    # Handle long content
    content_preview = content[:3000]
    truncation_note = ""
    if len(content) > 3000:
        print(f"⚠️  Warning: Content is {len(content)} chars, optimizing first 3000 chars only")
        truncation_note = "\n\n[NOTE: Content truncated to 3000 chars. Optimize what's shown and return only the optimized portion.]"

    prompts = [
        f"""You are an SEO expert. Optimize this markdown content.

Target Keywords: {keywords_str}

Content:
{content_preview}{truncation_note}

Tasks:
1. Improve title for CTR and keywords (keep it under 60 chars)
2. Refine meta description in front matter (under 160 chars)
3. Ensure headings are hierarchical (H1, H2, H3) and keyword-rich
4. Add alt text suggestions to any image placeholders
5. Improve readability (short paragraphs, bullet points)
6. Ensure 'tags' in front matter are relevant

Constraint: Do NOT change the core meaning, helpfulness, or tone. Keep it accessible.

Return the optimized markdown content. Do not include explanations or commentary."""
    ]

    result, filled_prompts, usage, _ = MinimalChainable.run(
        context={},
        model=model_info,
        callable=prompt,
        return_trace=True,
        prompts=prompts
    )
    
    optimized_content = result[-1]
    
    # Log the optimization
    MinimalChainable.log_to_markdown(
        "seo_optimizer",
        filled_prompts,
        result,
        usage
    )

    return optimized_content


# ============================================================================
# LOW-ENERGY PIPELINE - THE COMPLETE SYSTEM
# ============================================================================

def low_energy_pipeline(
    input_text: str,
    energy_level: str = "low",  # low/medium/high
    output_dir: Optional[str] = None,
    auto_save: bool = True
) -> Dict[str, Any]:
    """
    THE COMPLETE SYSTEM: From idea to publishable content.

    This is the game-changer for low-energy days. Just describe your problem
    and get publication-ready content.

    Args:
        input_text: Describe the problem or topic
        energy_level: Your current energy (affects complexity)
        output_dir: Where to save (defaults to output/ms_blog)
        auto_save: Whether to save files automatically

    Returns:
        Dict with:
            - content: The generated markdown
            - metadata: All generation details
            - file_path: Where it was saved (if auto_save)
            - validation: Validation results
            - review_checklist: What to check before publishing
    """
    model_info = get_model()

    if output_dir is None:
        output_dir = os.path.join(project_root, "output", "ms_blog")

    # Step 1: Analyze input and choose format
    format_selector_prompts = [
        f"""Analyze this user input: "{input_text}"

User's current energy level: {energy_level}

Determine:
1. What type of content would best address this?
   - Prompt card: Solves a specific problem with an AI prompt
   - Shortcut: Shows how to use a tool/technique
   - Guide: Teaches a complete system setup
   - Blog post: Explores a topic/shares insights

2. Why that format fits best
3. Key parameters to use for generation
4. Difficulty level appropriate for their energy

Return JSON with:
{{
  "format": "prompt_card|shortcut|guide|blog",
  "reasoning": "...",
  "parameters": {{
    // Format-specific params
  }},
  "difficulty": "beginner|intermediate|advanced",
  "estimated_effort": "low|medium|high"
}}"""
    ]

    format_result, _, _, _ = MinimalChainable.run(
        context={},
        model=model_info,
        callable=prompt,
        return_trace=True,
        prompts=format_selector_prompts
    )

    # Get the final output (format_result is a list of all outputs from each step)
    format_decision = format_result[-1]

    # Parse format decision (handle both string and dict responses)
    if isinstance(format_decision, dict):
        # Already parsed
        decision = format_decision
    elif isinstance(format_decision, str):
        try:
            decision = json.loads(format_decision)
        except:
            # Try to extract JSON from markdown
            import re
            json_match = re.search(r'```json\s*(\{.*?\})\s*```', format_decision, re.DOTALL)
            if json_match:
                decision = json.loads(json_match.group(1))
            else:
                decision = {"format": "prompt_card", "reasoning": "default", "parameters": {}}
    else:
        # Fallback
        decision = {"format": "prompt_card", "reasoning": "default", "parameters": {}}

    chosen_format = decision.get('format', 'prompt_card')
    params = decision.get('parameters', {})

    # Step 2: Generate content using appropriate generator
    print(f"\n🎯 Generating {chosen_format} content...")
    print(f"📊 Energy level: {energy_level}")
    print(f"🤔 Reasoning: {decision.get('reasoning', 'N/A')}\n")

    if chosen_format == "prompt_card":
        content, metadata = generate_prompt_card(
            problem=params.get('problem', input_text),
            target_audience=params.get('target_audience', "People with MS"),
            energy_level=energy_level,
            additional_context=params.get('context', '')
        )

    elif chosen_format == "shortcut":
        content, metadata = generate_shortcut_spotlight(
            tool=params.get('tool', input_text),
            ms_benefit=params.get('ms_benefit', "Reduces cognitive load and saves energy"),
            category=params.get('category', 'automation'),
            additional_context=params.get('context', '')
        )

    elif chosen_format == "guide":
        content, metadata = generate_guide(
            system=params.get('system', input_text),
            complexity=params.get('complexity', 'beginner'),
            estimated_time=params.get('estimated_time', '30-45 minutes'),
            additional_context=params.get('context', '')
        )

    else:  # blog or fallback
        # For blog posts, use a simplified version of guide generator
        content, metadata = generate_guide(
            system=input_text,
            complexity='beginner',
            estimated_time='15-30 minutes'
        )

    # Step 3: Validate content
    validation = validate_content(content, chosen_format)

    # Step 4: Save if requested
    file_path = None
    if auto_save:
        # Generate filename from title or input
        import re
        # Try to extract title from front matter
        title_match = re.search(r'title:\s*["\']?([^"\'\n]+)["\']?', content)
        if title_match:
            filename = title_match.group(1).lower()
            filename = re.sub(r'[^\w\s-]', '', filename)
            filename = re.sub(r'[-\s]+', '-', filename)
        else:
            filename = re.sub(r'[^\w\s-]', '', input_text[:50].lower())
            filename = re.sub(r'[-\s]+', '-', filename)

        file_path = os.path.join(output_dir, f"{filename}.md")
        save_markdown(content, file_path)
        print(f"✅ Saved to: {file_path}")

    # Step 5: Generate review checklist
    review_checklist = [
        "☐ Read through content for accuracy",
        "☐ Check all examples are relevant and helpful",
        "☐ Verify tone matches MS blog style",
        "☐ Test any prompts or instructions",
        "☐ Review front matter tags and metadata",
        "☐ Check for typos and formatting issues",
        "☐ Ensure accessibility (headings, structure)",
    ]

    if validation['issues']:
        review_checklist.insert(0, f"⚠️  Fix validation issues: {', '.join(validation['issues'])}")

    if validation['warnings']:
        review_checklist.append(f"⚡ Consider warnings: {', '.join(validation['warnings'])}")

    # Compile final result
    result = {
        'content': content,
        'metadata': {
            **metadata,
            'format_chosen': chosen_format,
            'format_reasoning': decision.get('reasoning'),
            'energy_level': energy_level,
        },
        'file_path': file_path,
        'validation': validation,
        'review_checklist': review_checklist,
        'next_steps': [
            f"Review content at: {file_path}" if file_path else "Review generated content",
            "Test any prompts or instructions",
            "Preview with Hugo: hugo server",
            "Commit to git when ready"
        ]
    }

    # Print summary
    print("\n" + "="*60)
    print("🎉 CONTENT GENERATED!")
    print("="*60)
    print(f"\n📝 Format: {chosen_format}")
    print(f"✅ Validation: {'PASSED' if validation['valid'] else 'NEEDS REVIEW'}")
    if file_path:
        print(f"📁 Saved to: {file_path}")

    print("\n📋 REVIEW CHECKLIST:")
    for item in review_checklist:
        print(f"  {item}")

    print("\n🚀 NEXT STEPS:")
    for step in result['next_steps']:
        print(f"  • {step}")

    print("\n" + "="*60)

    return result


if __name__ == "__main__":
    # CLI interface for quick testing
    import argparse

    parser = argparse.ArgumentParser(description="MS Blog Content Generator")
    parser.add_argument("input", help="Describe the problem or topic")
    parser.add_argument("--energy", choices=["low", "medium", "high"], default="medium")
    parser.add_argument("--format", choices=["auto", "prompt", "shortcut", "guide"], default="auto")
    parser.add_argument("--no-save", action="store_true", help="Don't save to file")

    args = parser.parse_args()

    if args.format == "auto":
        # Use the pipeline
        result = low_energy_pipeline(
            input_text=args.input,
            energy_level=args.energy,
            auto_save=not args.no_save
        )
    else:
        # Use specific generator
        if args.format == "prompt":
            content, metadata = generate_prompt_card(
                problem=args.input,
                energy_level=args.energy
            )
        elif args.format == "shortcut":
            content, metadata = generate_shortcut_spotlight(
                tool=args.input
            )
        elif args.format == "guide":
            content, metadata = generate_guide(
                system=args.input
            )

        print(content)

        if not args.no_save:
            output_path = os.path.join(project_root, "output", "ms_blog", "content.md")
            save_markdown(content, output_path)
            print(f"\n✅ Saved to: {output_path}")
