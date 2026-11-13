# MS Blog Content Generation Tools

Automated content generation for MS-focused blog with minimal cognitive load.

## Overview

The **Low-Energy Content Pipeline** turns an idea into a draft and a short review checklist for the author.

## Boundaries

These CLI tools are separate from the resumable workbench. Each model step is attempted once and requires an explicit action after failure. Generated scenarios are illustrative; personal experience, measured time/energy savings, medical benefits, sources and setup details require actual evidence or a [verify] marker. Structural validation checks sections and length, not truth or publication readiness.

Prompt-card `energy_level` changes the actual final-draft constraint: low requests under 600 words and at most three essential setup actions; medium under 900 words and at most five; high under 1,200 words with optional worked detail. These are model instructions, not measured energy outcomes or enforced word counts.

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
# - Possible effort reduction, without invented measurements
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
**Draft workflow** - One command from idea to a saved draft for review.

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

### Command Line Interface (CLI)

The new CLI makes it easy to generate content from your terminal.

```bash
# View all commands
python tools/ms_blog/cli.py --help

# Run the interactive menu (easiest way to start)
python tools/ms_blog/cli.py

# Run the low-energy pipeline
python tools/ms_blog/cli.py pipeline "I need help organizing my day" --energy low

# Generate a batch of content (New!)
python tools/ms_blog/cli.py batch "Fatigue Management" --count 5

# Generate a content calendar (New!)
python tools/ms_blog/cli.py calendar "Cognitive Health" --duration "1 month"

# Generate specific formats
python tools/ms_blog/cli.py prompt "Brain fog planning"
python tools/ms_blog/cli.py shortcut "Voice typing" --benefit "Saves energy"
python tools/ms_blog/cli.py guide "Symptom tracking system"
```

### Run Tests

```bash
.venv/bin/python -m pytest -q tools/ms_blog/test_ms_tools.py
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

To keep drafts in a separate review directory:
```python
result = low_energy_pipeline(
    input_text="...",
    output_dir="/path/to/local/draft-review"
)
```

## Energy Levels

Content adapts to your energy level:

- **Low**: Minimal detail, focus on essentials, shorter examples
- **Medium**: Balanced detail, standard examples, good explanations
- **High**: Comprehensive detail, multiple examples, thorough explanations

## Review the draft

The default `output/ms_blog/` directory is ignored by Git. If a draft filename already exists, the tool writes a new file and reports the actual path. Structural checks flag missing sections and short drafts for revision. Check factual claims, source details, setup instructions, metadata, and whether the examples suit the intended reader. Use your review experience to decide whether a particular workflow saves effort.

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
# Review and verify before considering publication.
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
2. **Run the offline MS tool checks**: `.venv/bin/python -m pytest -q tools/ms_blog/test_ms_tools.py`
3. **Generate real content**: Use the CLI or Python API
4. **Review the draft**: Check claims, use the prompts, and verify the setup instructions.

## Move a reviewed draft to Hugo

Keep generated files in the draft directory while you review the writing and front matter. Move the selected reviewed draft into the appropriate Hugo content folder and preview it in the site’s normal local workflow. Follow the site's publication process when the draft is ready.

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
