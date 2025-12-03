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
```

### 3. Run a Tool

```bash
python tools/content/evergreen_guide.py "Test topic"
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
