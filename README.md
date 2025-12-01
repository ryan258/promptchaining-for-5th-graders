# Prompt Chaining Framework

A Python framework for building sequential LLM prompts that build on previous outputs. Useful for complex reasoning tasks that benefit from step-by-step processing.

## Overview

This project implements two main patterns:

1. **MinimalChainable**: Sequential prompt execution with context variables and output references
2. **FusionChain**: Parallel execution across multiple models with comparative evaluation

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

## Quick Start

### Setup
```bash
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
cp .env.example .env
# Add your OPENROUTER_API_KEY to .env
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

def longest_wins(responses):
    return max(enumerate(responses), key=lambda x: len(x[1]))[0]

result = FusionChain.run(
    context={"topic": "APIs"},
    models=[(client, name) for name in model_names],
    callable=prompt,
    evaluator=longest_wins,
    prompts=[...]
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
├── demos/                # Example implementations
│   ├── character_evolution_engine/
│   ├── common_ground_finder/
│   ├── concept_simplifier/
│   ├── emergence_simulator/
│   ├── historical_what_if_machine/
│   ├── knowledge_time_machine/
│   ├── problem_solution_spider/
│   └── subject_connector/
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

| Demo | Pattern | Use Case |
|------|---------|----------|
| character_evolution_engine | Iterative development | Character/narrative building |
| common_ground_finder | Convergent synthesis | Conflict resolution |
| concept_simplifier | Layered explanation | Teaching/learning |
| emergence_simulator | System analysis | Complex systems reasoning |
| knowledge_time_machine | Temporal analysis | Historical/future thinking |
| problem_solution_spider | Divergent→convergent | Creative problem solving |
| subject_connector | Cross-domain linking | Interdisciplinary thinking |

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

## Use Cases

- Multi-step reasoning tasks
- Content generation with refinement
- Research and analysis workflows
- Educational content creation
- Creative writing assistance
- Decision-making frameworks

## Technical Notes

- Uses ThreadPoolExecutor for parallel model execution
- Automatically parses JSON responses (including markdown code blocks)
- Handles both string and structured (JSON) outputs
- Model-agnostic: works with any OpenAI-compatible API

## License

Personal project - private repository

## Acknowledgments

Built with OpenRouter API for multi-model access.
