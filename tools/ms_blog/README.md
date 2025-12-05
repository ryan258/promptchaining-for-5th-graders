# MS Blog Content Generation Tools

Automated content generation for MS-focused blog with minimal cognitive load.

## Overview

This module provides a **Low-Energy Content Pipeline** that generates publication-ready content for MS blog topics. Perfect for days when brain fog makes writing difficult.

## Features

### 1. Prompt Card Generator
Generate complete AI prompt cards that solve MS-related problems.

```python
from tools.ms_blog.ms_content_tools import generate_prompt_card

content, metadata = generate_prompt_card(
    problem="I get overwhelmed planning my day with MS brain fog",
    target_audience="People with MS and brain fog",
    energy_level="low"
)

# Generates:
# - YAML front matter with tags and SEO
# - Problem statement
# - Readiness checklist
# - The actual prompt (copy-paste ready)
# - 2-3 concrete examples
# - 3 variations (quick/detailed/alternative)
# - Troubleshooting section
# - Related resources
```

### 2. Shortcut Spotlight Generator
Generate accessibility-focused tool tutorials.

```python
from tools.ms_blog.ms_content_tools import generate_shortcut_spotlight

content, metadata = generate_shortcut_spotlight(
    tool="Voice typing in Google Docs",
    ms_benefit="Reduces hand fatigue and typing strain",
    category="automation"  # or "keyboard-shortcuts" or "system-instructions"
)

# Generates:
# - Why it matters for MS
# - Step-by-step setup
# - Keyboard shortcuts table
# - 3-4 practical use cases
# - Before/After comparison
# - Energy savings estimate
# - Troubleshooting section
```

### 3. Multi-Phase Guide Generator
Create comprehensive system setup guides.

```python
from tools.ms_blog.ms_content_tools import generate_guide

content, metadata = generate_guide(
    system="Setting up an AI assistant for MS brain fog",
    complexity="beginner",  # affects number of phases
    estimated_time="30-45 minutes"
)

# Generates:
# - Quick Path (30-second version for low-energy)
# - Detailed phases (3-5 steps based on complexity)
# - Complete Prompt Kit section
# - Before/After narrative
# - Troubleshooting checklist
# - Related resources
# - Full Hugo-compatible markdown
```

### 4. Content Idea Expander
Generate multiple content ideas from a seed concept.

```python
from tools.ms_blog.ms_content_tools import expand_content_idea

ideas, metadata = expand_content_idea(
    seed="Voice control for when hands don't cooperate",
    pillar="All",  # or "Prompts"/"Shortcuts"/"Guides"/"Blog"
    count=10
)

# Generates:
# - 5 prompt card ideas
# - 3 shortcut spotlight ideas
# - 2 multi-phase guide ideas
# - 1 blog post idea
# - SEO keywords for each
# - JTBD tags
# - Difficulty ratings
# - Priority scores (1-10)
```

### 5. Low-Energy Pipeline ⭐
**THE COMPLETE SYSTEM** - One command from idea to publishable content.

```python
from tools.ms_blog.ms_content_tools import low_energy_pipeline

result = low_energy_pipeline(
    input_text="I keep forgetting to take my medication",
    energy_level="low",  # adapts complexity to your energy
    auto_save=True
)

# System automatically:
# 1. Analyzes the problem
# 2. Chooses best format (prompt/shortcut/guide)
# 3. Generates complete content
# 4. Creates Hugo-compatible markdown
# 5. Saves to correct directory
# 6. Validates content
# 7. Provides review checklist

# Returns:
# {
#   'content': '...',           # Full markdown
#   'metadata': {...},          # Generation details
#   'file_path': '...',         # Where it was saved
#   'validation': {...},        # Quality checks
#   'review_checklist': [...]   # What to review before publishing
# }
```

## Quick Start

### Command Line Interface

```bash
# Use the low-energy pipeline
python tools/ms_blog/ms_content_tools.py "I need help organizing my day" --energy low

# Generate specific format
python tools/ms_blog/ms_content_tools.py "Voice typing" --format shortcut --energy medium

# Don't auto-save (just preview)
python tools/ms_blog/ms_content_tools.py "Medication tracking" --no-save
```

### Run the Demo

```bash
# Interactive demo menu
python demos/ms_blog_demo.py --interactive

# Run specific demo
python demos/ms_blog_demo.py --demo 1  # Low-energy pipeline
python demos/ms_blog_demo.py --demo 2  # Prompt card
python demos/ms_blog_demo.py --demo 3  # Shortcut
python demos/ms_blog_demo.py --demo 4  # Guide
python demos/ms_blog_demo.py --demo 5  # Idea expander

# Run all demos
python demos/ms_blog_demo.py --demo 6
```

### Run Tests

```bash
# Run all tests
python tools/ms_blog/test_ms_tools.py

# Run specific test
python tools/ms_blog/test_ms_tools.py --test prompt
python tools/ms_blog/test_ms_tools.py --test pipeline
```

## How It Works

### Prompt Chaining for Quality

Each generator uses **multi-step prompt chaining** to create emergent insights:

**Prompt Card Generation (5 steps):**
1. **Analyze** - Deep analysis of MS-specific problem
2. **Design** - Create solution prompt accounting for cognitive load
3. **Exemplify** - Generate concrete, relatable examples
4. **Vary** - Create variations for different energy levels
5. **Synthesize** - Combine into complete Hugo markdown

**Why chains vs single prompt:**
- Each step builds on discoveries from previous steps
- Deeper analysis than possible in one shot
- More nuanced, practical output
- Better structure and organization
- Automatic quality improvements through iteration

### Content Validation

All generated content is automatically validated:

```python
validation = {
    'valid': bool,           # Overall pass/fail
    'issues': [...],         # Critical problems
    'warnings': [...]        # Recommendations
}
```

Checks include:
- Minimum length requirements
- Required sections for content type
- YAML front matter presence
- Markdown structure
- Accessibility considerations

### Hugo Integration

Content is generated Hugo-compatible with:
- YAML front matter (title, description, tags, etc.)
- JTBD tags (Do/Decide/Write/Understand)
- SEO meta descriptions
- Difficulty ratings
- Energy cost estimates
- Proper date formatting

## File Structure

```
tools/ms_blog/
├── __init__.py
├── ms_content_tools.py      # Main module (all generators)
├── test_ms_tools.py         # Test suite
└── README.md                # This file

demos/
└── ms_blog_demo.py          # Interactive demo

output/ms_blog/              # Generated content saved here
└── *.md                     # Hugo-compatible markdown files
```

## Output Location

By default, content is saved to:
```
output/ms_blog/[filename].md
```

You can customize the output directory:
```python
result = low_energy_pipeline(
    input_text="...",
    output_dir="/path/to/hugo/content/prompts"
)
```

## Energy Levels

Content adapts to your energy level:

- **Low**: Minimal detail, focus on essentials, shorter examples
- **Medium**: Balanced detail, standard examples, good explanations
- **High**: Comprehensive detail, multiple examples, thorough explanations

## Success Metrics

**Efficiency:**
- Time to publish: **2-4 hours → 15-30 minutes**
- Cognitive load: **High focus → Works on foggy days**
- Consistency: **100% adherence to standards**

**Output:**
- Content velocity: **2-3x current pace**
- Quality: Matches or exceeds manual exemplars
- SEO: All proper tags/meta automatically

## Examples

### Example 1: Quick Content on Low Energy Day

```python
# You're having a foggy day, just type a problem
result = low_energy_pipeline(
    "I can't remember what I worked on yesterday",
    energy_level="low"
)

# ✅ Created: daily-work-log-prompt.md
# Format: Prompt Card (auto-detected)
# Ready to publish with minimal review
```

### Example 2: Brainstorm Content Ideas

```python
# You have a rough topic, need ideas
ideas, meta = expand_content_idea(
    "AI assistants for medication management"
)

# Generated:
# - 5 prompt cards (pill reminders, dose tracking, etc.)
# - 3 shortcuts (calendar automation, voice commands, etc.)
# - 2 guides (complete medication system, etc.)
# - 1 blog post (listicle of medication tools)
# All ranked by priority
```

### Example 3: Generate Specific Content Type

```python
# You know you want a guide
content, meta = generate_guide(
    system="Daily symptom tracking with AI",
    complexity="beginner",
    estimated_time="20 minutes"
)

# Complete multi-phase guide with:
# - Quick Path for low-energy days
# - 3 detailed phases
# - AI prompt kit
# - Troubleshooting checklist
```

## Customization

### Adjust Complexity

```python
# For different complexity levels
generate_guide(
    system="...",
    complexity="beginner"     # 3 phases
    # complexity="intermediate"  # 4 phases
    # complexity="advanced"      # 5 phases
)
```

### Target Specific Audience

```python
generate_prompt_card(
    problem="...",
    target_audience="MS patients with severe mobility challenges"
)
```

### Choose Content Category

```python
generate_shortcut_spotlight(
    tool="...",
    category="keyboard-shortcuts"  # or "automation" or "system-instructions"
)
```

## Next Steps

1. **Try the demo**: `python demos/ms_blog_demo.py --interactive`
2. **Run tests**: `python tools/ms_blog/test_ms_tools.py`
3. **Generate real content**: Use the CLI or Python API
4. **Review and publish**: Check the review checklist, test prompts, publish

## Integration with Hugo Blog

To use with your actual Hugo blog:

```python
# Point to your Hugo content directory
result = low_energy_pipeline(
    input_text="...",
    output_dir="/path/to/your/hugo/blog/content/prompts"
)

# Then in your blog directory:
# hugo server  # Preview
# git add .
# git commit -m "Add new prompt card"
# git push
```

## Architecture

The Low-Energy Pipeline uses the framework's **prompt chaining capabilities**:

```
User Input
    ↓
Format Selector (meta-chain decides prompt/shortcut/guide)
    ↓
Appropriate Generator (4-6 step chain)
    ↓
Validation & Quality Checks
    ↓
Hugo-Compatible Markdown
    ↓
Auto-Save + Review Checklist
```

Each generator is a **MinimalChainable** execution that:
1. Decomposes the problem
2. Designs the solution
3. Generates examples
4. Creates variations/extensions
5. Synthesizes into final markdown

## Troubleshooting

**"Module not found"**
- Make sure you're running from project root
- Check that `tools/ms_blog/__init__.py` exists

**"Content validation failed"**
- Check the validation.issues for specific problems
- Review the generated content manually
- Adjust inputs and regenerate if needed

**"Token usage too high"**
- Use energy_level="low" for shorter output
- Choose simpler complexity levels
- Use specific generators instead of pipeline for more control

## Future Enhancements

Potential additions:
- Batch content generator (month of content at once)
- Content refresher (update old posts)
- SEO optimizer
- Related content linker
- Multi-language support
- Voice input integration

---

**Built with the Prompt Chaining Framework**
- Leverages MinimalChainable for sequential reasoning
- Uses meta-chains for format selection
- Automatic artifact logging
- Full execution traces in logs/
