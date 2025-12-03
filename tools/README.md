# 🧠 Cognitive Exoskeleton Tools

Production-ready tools that amplify output while conserving cognitive energy.

## Philosophy

These tools are designed for **low-energy usability**. If you can't use them on a bad day, they're not working.

### Design Principles

1. **Zero-config start**: Load user context automatically
2. **Resume-able**: Save state if interrupted
3. **Fast**: < 3 minutes for 80% of use cases
4. **Energy ROI positive**: Value out > effort in

---

## Content Tools

### 🌲 Evergreen Guide Architect

Transform topics or rough notes into structured, lasting guide outlines.

**Usage:**
```bash
# From topic
python tools/content/evergreen_guide.py "Progressive overload for MS patients"

# From notes
cat notes/training-thoughts.md | python tools/content/evergreen_guide.py

# With context
python tools/content/evergreen_guide.py "Topic" --context "Additional notes here"
```

**Output:**
- Markdown outline in `output/guides/`
- Analysis of user intent & pain points
- Competition differentiation strategy
- Key metaphors and research citations
- Evergreen audit (what stays timeless)
- Quality metrics and writing priorities

**Energy Cost**: Low (2-3 minutes)
**Energy Return**: High (saves hours of outlining)
**Net**: Strongly positive ✅

---

## Learning Tools

### 🧭 Concept Simplifier

Break complex topics into components, analogies, examples, and a concise explainer.

**Usage:**
```bash
python tools/learning/concept_simplifier.py "Diffusion models in AI"
python tools/learning/concept_simplifier.py "Topic" --context "Audience or constraints"
```

**Output:**
- JSON in `output/learning/concept_simplifier/`
- Components, analogies, examples, explainer, pitfalls, next steps
- Logs with token/cost estimates in `logs/`

---

## Research Tools

### 🕰️ Research Timeline (Knowledge Time Machine, adult mode)

Generate origin → evolution → current frontier timelines with citations and risks.

**Usage:**
```bash
python tools/research/timeline.py "CRISPR gene editing"
cat notes/topic.md | python tools/research/timeline.py --context "Specific angle"
```

**Output:**
- Markdown timeline in `output/research/`
- Origins, breakthroughs, current state, future speculation
- Risks/limitations and research gaps
- Logs with token/cost estimates in `logs/`

**Energy Cost**: Low (2-3 minutes)
**Energy Return**: High (research prep shortcut)
**Net**: Strongly positive ✅

---

## Development Tools

### 🏗️ Code Architecture Critic

Audit a code snippet for patterns/anti-patterns, smells, refactors, risks, and an improved architecture sketch.

**Usage:**
```bash
python tools/dev/code_architecture_critic.py "path/to/file.py"
python tools/dev/code_architecture_critic.py "inline code" --context "constraints or goals"
```

**Output:**
- JSON in `output/dev/code_architecture_critic/`
- Patterns/anti-patterns, smells, refactor plan, maintenance forecast, architecture sketch
- Logs with token/cost estimates in `logs/`

---

## Collaboration Tools

### 🤝 Common Ground Finder

Map opposing views to values, shared concerns, common goals, and bridge options.

**Usage:**
```bash
python tools/collaboration/common_ground_finder.py "View A" --context "View B"
```

**Output:**
- JSON in `output/collaboration/common_ground_finder/`
- Values, shared concerns, common goals, bridge ideas, conversation prompts
- Logs with token/cost estimates in `logs/`

---

## Brainstorming Tools

### 🕷️ Problem–Solution Spider

Clarify a problem, constraints, wild ideas, blended solutions, and a quick test scenario.

---

## Career Tools

### 🎯 Dream Job Reverse Engineer

Decode a job posting into hidden priorities, pain points, application strategy, resume bullets, and STAR stories.

**Usage:**
```bash
python tools/career/dream_job_reverse_engineer.py "path/to/job.txt"
python tools/career/dream_job_reverse_engineer.py "Job text" --context "Your profile/angle"
```

**Output:**
- JSON in `output/career/dream_job_reverse_engineer/`
- Hidden priorities, pain points, strategy, bullets, STAR outlines
- Logs with token/cost estimates in `logs/`

---

## Media Literacy Tools

### 🧹 Euphemism Decoder

Turn sanitized language into plain English, expose intent, and flag manipulation.

**Usage:**
```bash
python tools/media/euphemism_decoder.py "Quoted text"
cat speech.txt | python tools/media/euphemism_decoder.py
```

**Output:**
- JSON in `output/media/euphemism_decoder/`
- Euphemism mappings, plain-English rewrite, intent/beneficiaries
- Logs with token/cost estimates in `logs/`

### 🧭 Media Bias Triangulator

Generate polarized framings, surface omissions, and synthesize ground truth.

**Usage:**
```bash
python tools/media/media_bias_triangulator.py "Event description"
cat event.txt | python tools/media/media_bias_triangulator.py
```

**Output:**
- JSON in `output/media/media_bias_triangulator/`
- Biased headlines, omissions, ground truth synthesis
- Logs with token/cost estimates in `logs/`

---

## Social Dynamics Tools

### 🧠 Status Game Decoder

Parse social interactions for signals, hierarchy, and the real game being played.

**Usage:**
```bash
python tools/social/status_game_decoder.py "Describe the scene"
```

**Output:**
- JSON in `output/social/status_game_decoder/`
- Surface analysis, signals, hierarchy, real game, countermoves
- Logs with token/cost estimates in `logs/`

**Usage:**
```bash
python tools/brainstorm/problem_solution_spider.py "Problem statement"
python tools/brainstorm/problem_solution_spider.py "Problem" --context "Constraints/stakeholders"
```

**Output:**
- JSON in `output/brainstorm/problem_solution_spider/`
- Defined problem, constraints/resources, wild ideas, solution options, test scenario
- Logs with token/cost estimates in `logs/`

---

## Health Tools

### 🔬 Medical Consensus Parser
*Coming soon*

Parse research studies with built-in skepticism and synthesis.

### 📊 Symptom Correlator
*Coming soon*

Find patterns in health logs and propose experiments.

### ⚖️  Protocol Decision Matrix
*Coming soon*

Evaluate new interventions with risk-adjusted framework.

---

## Cognitive Tools

### 🎯 Advocacy Prep
*Coming soon*

Prepare for important conversations (doctor appointments, business calls).

### 🔓 Blocker Breaker
*Coming soon*

Break through when feeling stuck on projects.

---

## Setup

### 1. Configure User Profile

Edit `context/user_profile.json` with your preferences:
```json
{
  "writing_style": {
    "tone": "Your preferred tone",
    "avoid": ["Things to avoid"],
    "prefer": ["Things to emphasize"]
  },
  "health_context": {
    "condition": "Your situation",
    "priorities": ["Your health priorities"]
  }
}
```

### 2. Ensure API Access

Tools use the same `.env` setup as the main framework:
```bash
# Should already be configured if demos work
OPENROUTER_API_KEY=your_key_here
OPENROUTER_MODELS="openai/gpt-3.5-turbo,google/gemini-flash-1.5,google/gemini-pro-1.5"  # Optional: override model list for FusionChain
RUN_FUSION_CHAIN=0  # Optional: enable multi-model demo (uses more calls)
```

### 3. Run a Tool

```bash
python tools/content/evergreen_guide.py "Test topic"
python tools/research/timeline.py "Test topic"
```

---

## Output Structure

```
output/
├── guides/               # Guide outlines
│   └── 20241203-1430-topic.md
├── health/              # Health analysis
│   ├── research/
│   ├── experiments/
│   └── protocols/
└── prep/                # Conversation prep docs
    └── appointment-2024-12-03.md
```

---

## Energy Cost Reference

| Tool | Setup | Usage | Value | Net ROI |
|------|-------|-------|-------|---------|
| Evergreen Guide | 0min | 2min | 2hrs saved | +++ |
| Medical Consensus | 0min | 3min | Hours of research | +++ |
| Symptom Correlator | 5min* | 2min | Pattern insights | ++ |
| Advocacy Prep | 0min | 10min | Confidence++ | ++ |
| Blocker Breaker | 0min | 5min | Restart work | +++ |

*One-time setup to create log format

---

## Development Guidelines

### When Adding New Tools

1. **User Context**: Load `context/user_profile.json` automatically
2. **CLI-First**: Accept input via args or stdin
3. **Output Structure**: Save to appropriate `output/` subdirectory
4. **Error Handling**: Graceful degradation, partial value
5. **Energy Test**: Can you use it at 50% capacity?
6. **Cost Visibility**: Include usage stats in logs; summarize with `python tools/cost_report.py`

### Tool Template

```python
#!/usr/bin/env python3
"""
Tool Name

Brief description of what it does and why.

Usage:
    python tools/category/tool.py "input"
    cat file.txt | python tools/category/tool.py
"""

import sys
import os
import argparse
import json

# Standard project setup
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from chain import MinimalChainable
from main import build_models, prompt

def load_user_context():
    """Load user profile for context-aware generation"""
    # Standard implementation
    pass

def tool_main(input_data, additional_context=""):
    """Main tool logic"""
    # Load context
    user_profile = load_user_context()

    # Build chain
    # Execute
    # Save output
    # Print summary
    pass

def main():
    # CLI argument handling
    pass

if __name__ == "__main__":
    main()
```

---

## Feedback Loop

Track which tools you actually use:
- **Using weekly**: Keep and improve
- **Using monthly**: Good, maintain
- **Haven't used in 2 weeks**: Archive or delete

Better to have 3 great tools than 10 mediocre ones.

---

## Support

Issues: File in project root issue tracker
Questions: See main project README

---

**Tools that feel like extensions of your mind, not external systems to manage.**
