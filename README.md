# Prompt Chaining Framework

A Python framework for building sequential LLM prompts that build on previous outputs. Designed for complex reasoning tasks that benefit from step-by-step processing.

> **New to this project?** Start with [HAPPY-PATH.md](HAPPY-PATH.md) for a beginner-friendly guide!

## Overview

This project implements prompt chaining patterns for AI model interactions:

1. **MinimalChainable**: Sequential prompt execution with context variables and output references
2. **FusionChain**: Parallel execution across multiple models with comparative evaluation
3. **Automatic Logging**: Timestamped markdown logs of all runs for history tracking
4. **Metagame Analysis**: Demos that reveal hidden strategic layers and uncomfortable truths

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

## Quick Start

### Setup
```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows

# Install dependencies
pip install -r requirements.txt

# Configure API key
cp .env.example .env
# Add your OPENROUTER_API_KEY to .env
```

Get an API key at [openrouter.ai/keys](https://openrouter.ai/keys)

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
  - 20 Exceptional Use Cases (monetizable skills, cognitive amplification, pattern recognition, futures, creative synthesis)
  - 10 Metagame X-Ray Demos (reveal hidden strategic layers)
  - Implementation priorities and selection framework

## Why Prompt Chaining?

**Single Prompts**: Limited to what AI can think through in one step

**Prompt Chains**:
- ✨ Build complexity through iteration
- 🔄 Self-critique and refinement loops
- 🧬 Emergent insights impossible from single prompts
- 🎯 Progressive abstraction from specific to universal
- 🔀 Multiple perspectives synthesized
- 💡 Later steps couldn't exist without earlier discoveries

**Example**: Metagame demos CANNOT work as single prompts because:
1. First must map the surface game
2. Then identify contradictions (behavior vs stated rules)
3. Then reverse-engineer actual incentives
4. Only then reveal the real game

The chain IS the insight.

## Ethical Note

Some demos (especially metagame analysis) reveal uncomfortable truths about power, manipulation, and strategic deception.

**Understanding ≠ Endorsing**

These patterns exist whether you acknowledge them or not. Knowledge is for defense (see through BS) and awareness (make better decisions), not offense (deploy BS).

## License

Personal learning project - private repository

## Acknowledgments

Built with OpenRouter API for multi-model access.

---

**18 demos and counting. See what prompt chaining can unlock.**
