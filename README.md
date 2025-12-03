# Prompt Chaining Framework

A Python framework for building sequential LLM prompts that build on previous outputs. Designed for complex reasoning tasks that benefit from step-by-step processing.

> **New to this project?** Start with [HAPPY-PATH.md](HAPPY-PATH.md) for a beginner-friendly guide!

## Overview

This project implements prompt chaining patterns for AI model interactions:

1. **MinimalChainable**: Sequential prompt execution with context variables and output references
2. **FusionChain**: Parallel execution across multiple models with comparative evaluation
3. **Automatic Logging**: Timestamped markdown logs of all runs for history tracking

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
├── chain.py              # Core framework (MinimalChainable, FusionChain)
├── main.py               # OpenRouter API client + examples
├── chain_test.py         # Unit tests
├── HAPPY-PATH.md         # Beginner-friendly getting started guide
├── GETTING_STARTED.md    # Technical setup guide
├── ROADMAP.md            # Project roadmap and priorities
├── demos/                # Example implementations
│   ├── character_evolution_engine/    ✅ with logging
│   ├── common_ground_finder/
│   ├── concept_simplifier/            ✅ with logging
│   ├── emergence_simulator/           ✅ with logging
│   ├── historical_what_if_machine/
│   ├── knowledge_time_machine/        ✅ with logging
│   ├── problem_solution_spider/       ✅ with logging
│   └── subject_connector/             ✅ with logging
├── logs/                 # Auto-generated timestamped logs
└── requirements.txt
```

## API Integration

Uses OpenRouter for access to multiple LLM providers:
- OpenAI (GPT-3.5, GPT-4)
- Google (Gemini Flash, Gemini Pro)
- Anthropic (Claude)
- Meta (Llama)
- And 100+ others

Get an API key at [openrouter.ai/keys](https://openrouter.ai/keys)

## Demos

Each demo shows a different prompt chaining pattern:

| Demo | Pattern | Use Case | Logging |
|------|---------|----------|---------|
| character_evolution_engine | Iterative development | Character/narrative building | ✅ |
| common_ground_finder | Convergent synthesis | Conflict resolution | - |
| concept_simplifier | Layered explanation | Teaching/learning | ✅ |
| emergence_simulator | System analysis | Complex systems reasoning | ✅ |
| historical_what_if_machine | Counterfactual reasoning | Alternative history | - |
| knowledge_time_machine | Temporal analysis | Historical/future thinking | ✅ |
| problem_solution_spider | Divergent→convergent | Creative problem solving | ✅ |
| subject_connector | Cross-domain linking | Interdisciplinary thinking | ✅ |

### Running Demos
```bash
# Run the main proof-of-concept
python main.py

# Run a specific demo
python demos/concept_simplifier/main.py

# Check the outputs
cat demos/concept_simplifier/concept_simplifier_results.txt
cat logs/2025-12-02_*_concept_simplifier.md
```

## Output Files

Demos generate two types of output:

**In demo directory** (e.g., `demos/concept_simplifier/`):
- `*_prompts.txt` - The actual prompts sent to AI
- `*_results.txt` - The AI responses

**In `/logs` directory**:
- `YYYY-MM-DD_HH-MM-SS_demoname.md` - Timestamped markdown logs with full run history

## Testing

```bash
pytest chain_test.py
```

Tests use mock callables to avoid API costs during development.

## Design Philosophy

**Minimal**: Small, focused abstractions. No unnecessary framework complexity.

**Composable**: Chain outputs can feed into new chains. Models can be swapped easily.

**Transparent**: All prompts and outputs are returned for inspection and debugging.

**Cost-aware**: Designed for experimentation without accidental API spend.

**Educational**: Code is heavily commented to explain concepts to learners.

## Use Cases

- Multi-step reasoning tasks
- Content generation with refinement
- Research and analysis workflows
- Educational content creation
- Creative writing assistance
- Decision-making frameworks
- Experiment tracking and logging

## Technical Notes

- Uses ThreadPoolExecutor for parallel model execution in FusionChain
- Automatically parses JSON responses (including markdown code blocks)
- Handles both string and structured (JSON) outputs
- Model-agnostic: works with any OpenAI-compatible API
- Graceful error handling for file operations
- UTF-8 encoding for all file outputs

## Recent Updates

- ✅ Added automatic markdown logging to all demos
- ✅ Simplified FusionChain to parallel-only execution
- ✅ Added HAPPY-PATH.md beginner guide
- ✅ Improved error handling in logging
- ✅ Migrated from Google Gemini to OpenRouter API

See [ROADMAP.md](ROADMAP.md) for upcoming features.

## Documentation

- **[HAPPY-PATH.md](HAPPY-PATH.md)** - Beginner-friendly getting started guide
- **[GETTING_STARTED.md](GETTING_STARTED.md)** - Technical setup and concepts
- **[ROADMAP.md](ROADMAP.md)** - Project roadmap and learning goals

## License

Personal learning project - private repository

## Acknowledgments

Built with OpenRouter API for multi-model access.
