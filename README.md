# Prompt Chaining Framework

A Python framework for building sequential LLM prompts that build on previous outputs. Designed for complex reasoning tasks that benefit from step-by-step processing.

## Overview

This project implements prompt chaining patterns for AI model interactions:

- **MinimalChainable**: Sequential prompt execution with context variables and output references
- **FusionChain**: Parallel execution across multiple models with comparative evaluation
- **Web UI**: Interactive interface with beautiful chain execution visualization
- **Reference Tools**: Two complete examples (concept_simplifier, subject_connector) demonstrating best practices

## Why Prompt Chaining?

**Single Prompts**: Limited to what AI can think through in one step

**Prompt Chains**:
- ✨ Build complexity through iteration
- 🔄 Self-critique and refinement loops
- 🧬 Emergent insights impossible from single prompts
- 🎯 Progressive abstraction from specific to universal
- 🔀 Multiple perspectives synthesized
- 💡 Later steps couldn't exist without earlier discoveries

**Examples**:

The **Concept Simplifier** CANNOT work as a single prompt because:
1. First must decompose the concept into core components
2. Then create targeted analogies for each component
3. Then build concrete examples with self-checks
4. Only then synthesize everything into a cohesive explainer

The **Subject Connector** CANNOT work as a single prompt because:
1. First must analyze each subject independently
2. Then identify unexpected connections between them
3. Then evaluate why those connections matter
4. Only then design a project that leverages both

The chain IS the insight. Each step depends on discoveries from previous steps.

## Quick Start

### Prerequisites

- Python 3.8+
- Node.js 18+ (for web UI)
- OpenRouter API key ([get one free](https://openrouter.ai/keys))

### Installation

1. **Clone and setup virtual environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # Mac/Linux
   # or
   venv\Scripts\activate     # Windows
   ```

2. **Install Python dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure API key**
   ```bash
   cp .env.example .env
   ```

   Edit `.env` and add your OpenRouter API key:
   ```
   OPENROUTER_API_KEY=sk-or-v1-...
   ```

4. **Verify setup**
   ```bash
   python main.py
   ```

### Running the Web UI

1. **Install frontend dependencies**
   ```bash
   cd web
   npm install
   ```

2. **Start the backend server** (in one terminal)
   ```bash
   python3 server/main.py
   ```

3. **Start the frontend dev server** (in another terminal)
   ```bash
   cd web
   npm run dev
   ```

4. **Open browser**
   ```
   http://localhost:5173
   ```

The web UI provides:
- Interactive tool execution
- Beautiful step-by-step chain visualization
- No more cryptic `{{output[-1]}}` placeholders
- See exactly what each step receives and produces
- Token usage tracking per step

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

### Execution Traces (NEW!)
```python
result, prompts, usage, trace = MinimalChainable.run(
    context={"topic": "recursion"},
    model=model_info,
    callable=prompt,
    return_trace=True,  # Get full execution trace
    prompts=[...]
)

# trace contains:
# - steps: [{step_number, role, prompt, response, tokens}, ...]
# - final_result: {...}
# - total_tokens: 500
```

### Automatic Logging
All runs automatically create timestamped markdown logs in `/logs`:
```
logs/2025-12-05_14-30-15_concept_simplifier.md
```

## Basic Usage

### Simple Chain

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

for i, output in enumerate(outputs):
    print(f"\nStep {i+1}:\n{output}")
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

### Building Your Own Tool

Use the reference implementations as templates:

```bash
# Example 1: 4-step educational chain
cat tools/learning/concept_simplifier.py

# Example 2: 4-step connection-finding chain
cat tools/learning/subject_connector.py
```

Key pattern:
```python
from tools.tool_utils import setup_project_root, load_user_context, get_input_from_args
from chain import MinimalChainable
from main import build_models, prompt

def my_tool(topic: str, additional_context: str = ""):
    # Load user preferences
    user_profile = load_user_context(project_root)

    # Build models
    client, model_names = build_models()
    model_info = (client, model_names[0])

    # Run chain with execution trace
    result, prompts, usage, trace = MinimalChainable.run(
        context={"topic": topic, ...},
        model=model_info,
        callable=prompt,
        return_trace=True,
        prompts=[
            "Your first prompt...",
            "Your second prompt using {{output[-1]}}...",
            # ... more prompts
        ]
    )

    # Save results
    with open(output_path, "w") as f:
        json.dump(trace, f, indent=2)

    # Save logs
    MinimalChainable.log_to_markdown("my_tool", prompts, result, usage)
```

## Project Structure

```
.
├── chain.py                  # Core framework (MinimalChainable, FusionChain)
├── main.py                   # Model configuration and utilities
├── server/                   # FastAPI backend for web UI
│   └── main.py
├── web/                      # React frontend
│   ├── src/
│   │   ├── components/
│   │   │   ├── ChainViewer.jsx      # Step-by-step visualization
│   │   │   ├── ResultViewer.jsx     # Results display
│   │   │   ├── ToolSelector.jsx     # Tool picker
│   │   │   └── InputForm.jsx        # Input form
│   │   ├── App.jsx
│   │   └── index.css
│   └── package.json
├── tools/                    # Tool implementations
│   ├── learning/
│   │   ├── concept_simplifier.py    # Reference: Educational chain
│   │   └── subject_connector.py     # Reference: Connection-finding chain
│   └── tool_utils.py         # Shared utilities
├── output/                   # Generated outputs
├── logs/                     # Execution logs
└── context/                  # User profile configuration
```

## Key Concepts

**Context Variables**: `{{variable}}` gets replaced from context dict

**Output References**: `{{output[-1]}}` = last output, `{{output[-2]}}` = second-to-last

**JSON Field Access**: `{{output[-1].field_name}}` extracts fields from JSON responses

**Model Info Tuple**: `(client, model_name)` required for prompt function

**Execution Traces**: Enable with `return_trace=True` for full step-by-step visibility

## Troubleshooting

**"Connection error"**
- Check internet connection
- Verify API key is correct in `.env`
- Try a different model (some may have rate limits)

**"Module not found"**
- Ensure virtual environment is activated
- Run `pip install -r requirements.txt` again

**"API key not found"**
- Check `.env` file exists in project root
- Verify `OPENROUTER_API_KEY` is set correctly
- No quotes needed around the key value

**Web UI not loading**
- Ensure both backend (`python3 server/main.py`) and frontend (`npm run dev`) are running
- Check that ports 8000 (backend) and 5173 (frontend) are available

## Cost Management

- OpenRouter shows per-request costs
- Start with free/cheap models (gemini-flash-1.5)
- Set up billing alerts in OpenRouter dashboard
- Execution traces show token usage per step

## Ethical Note

This framework enables powerful analytical tools. Some reveal uncomfortable truths about power dynamics, manipulation, and strategic deception.

**Understanding ≠ Endorsing**

These patterns exist whether you acknowledge them or not. Knowledge is for defense (see through BS) and awareness (make better decisions), not offense (deploy BS).

## What's Next?

1. **Try the reference tools**:
   - `python tools/learning/concept_simplifier.py "Machine Learning"`
   - `python tools/learning/subject_connector.py "History" --context "Physics"`
2. **Use the web UI**: Visualize how chains work step-by-step
3. **Build your own tool**: Use the reference implementations as templates
4. **Explore FusionChain**: Compare multiple models in parallel
5. **Check IDEAS.md**: See future enhancements and contribute

## License

Personal learning project - private repository

## Acknowledgments

Built with OpenRouter API for multi-model access.

---

**See what prompt chaining can unlock.**
