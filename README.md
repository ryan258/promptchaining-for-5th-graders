# Prompt Chaining Framework

A Python framework for building sequential LLM prompts that build on previous outputs. Designed for complex reasoning tasks that benefit from step-by-step processing.

> **New to this project?** Start with [HAPPY-PATH.md](HAPPY-PATH.md) for a beginner-friendly guide!

## Overview

This project implements prompt chaining patterns for AI model interactions:

1. **MinimalChainable**: Sequential prompt execution with context variables and output references
2. **FusionChain**: Parallel execution across multiple models with comparative evaluation
3. **Automatic Logging**: Timestamped markdown logs of all runs for history tracking
4. **Production-Ready Tools**: 33 specialized tools for professional-grade AI-powered analysis across multiple domains

## Core Features

### Variable Substitution
```python
context = {"topic": "quantum mechanics"}
prompt = "Explain {{topic}} simply"
# Becomes: "Explain quantum mechanics simply"
```

### Output References
```python
prompts = [
    "List 3 facts about {{topic}}",
    "Based on {{output[-1]}}, explain the most interesting one",
    "Connect {{output[-1]}} to real-world applications"
]
```

### JSON Field Access
```python
# If output[-1] = {"title": "AI", "summary": "..."}
"Write an article about {{output[-1].title}}"
```

### Automatic Logging
All demo runs automatically create timestamped markdown logs in `/logs`:
```
logs/2025-12-02_14-30-15_concept_simplifier.md
```

### Basic Usage
```python
from chain import MinimalChainable
from main import build_models, prompt

client, model_names = build_models()
model_info = (client, model_names[0])

outputs, prompts = MinimalChainable.run(
    context={"topic": "recursion"},
    model=model_info,
    callable=prompt,
    prompts=[
        "Define {{topic}} in one sentence",
        "Give a simple example of {{output[-1]}}",
        "Explain why {{output[-2]}} matters in programming"
    ]
)
```

### Multi-Model Comparison
```python
from chain import FusionChain

def evaluator(responses):
    """Pick the longest response"""
    scores = [len(r) for r in responses]
    max_score = max(scores)
    normalized = [s/max_score for s in scores]
    top_response = responses[scores.index(max_score)]
    return top_response, normalized

# FusionChain.run() executes models in parallel
result = FusionChain.run(
    context={"topic": "APIs"},
    models=[(client, name) for name in model_names],
    callable=prompt,
    evaluator=evaluator,
    get_model_name=lambda m: m[1],
    prompts=[
        "Explain {{topic}} in simple terms",
        "Give a real-world example of {{output[-1]}}"
    ]
)

print(result.top_response)
print(result.performance_scores)
```

## Project Structure

```
.
├── chain.py                  # Core chaining framework (MinimalChainable, FusionChain)
├── main.py                   # Model configuration and utilities
├── tools/                    # 33 production-ready specialized tools
│   ├── brainstorm/          # Problem-solving tools
│   ├── business/            # Negotiation and business strategy
│   ├── career/              # Job search and career navigation
│   ├── collaboration/       # Bridging disagreements
│   ├── content/             # Content creation and planning
│   ├── culture/             # Corporate dynamics analysis
│   ├── dev/                 # Code analysis and architecture
│   ├── geopolitics/         # International relations analysis
│   ├── history/             # Historical analysis and counterfactuals
│   ├── learning/            # Education and concept explanation
│   ├── marketing/           # Marketing strategy and virality
│   ├── media/               # Media literacy and bias detection
│   ├── policy/              # Policy analysis and regulatory scrutiny
│   ├── politics/            # Political analysis and promise tracking
│   ├── psychology/          # Behavioral analysis and consistency testing
│   ├── research/            # Research timelines and emergence patterns
│   ├── social/              # Social dynamics and status games
│   ├── strategy/            # Strategic analysis and scenario planning
│   └── writing/             # Creative writing and character development
├── demos/                   # Example demonstrations (legacy)
├── output/                  # Generated analysis and reports
├── logs/                    # Execution logs with token usage
└── context/                 # User profile configuration
```

See [tools/README.md](tools/README.md) for comprehensive tool documentation.

## Why Prompt Chaining?

**Single Prompts**: Limited to what AI can think through in one step

**Prompt Chains**:
- ✨ Build complexity through iteration
- 🔄 Self-critique and refinement loops
- 🧬 Emergent insights impossible from single prompts
- 🎯 Progressive abstraction from specific to universal
- 🔀 Multiple perspectives synthesized
- 💡 Later steps couldn't exist without earlier discoveries

**Example**: The Negotiation Strategy Builder CANNOT work as a single prompt because:
1. First must analyze power dynamics and leverage
2. Then identify BATNAs (Best Alternative To Negotiated Agreement)
3. Then set strategic anchors based on power analysis
4. Then predict objections based on counterparty interests
5. Only then craft counter-scripts that maintain frame control

The chain IS the strategy. Each step depends on insights from previous steps.

## Ethical Note

Some tools (especially those analyzing power dynamics, manipulation, and strategic deception) reveal uncomfortable truths.

**Understanding ≠ Endorsing**

These patterns exist whether you acknowledge them or not. Knowledge is for defense (see through BS) and awareness (make better decisions), not offense (deploy BS).

## Getting Started

1. Follow [GETTING_STARTED.md](GETTING_STARTED.md) for installation
2. Explore [tools/README.md](tools/README.md) for the full tool catalog
3. Check [HAPPY-PATH.md](HAPPY-PATH.md) for beginner-friendly examples

## License

Personal learning project - private repository

## Acknowledgments

Built with OpenRouter API for multi-model access.

---

**33 production-ready tools. See what prompt chaining can unlock.**
