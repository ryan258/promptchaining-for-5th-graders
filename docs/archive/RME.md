# Prompt Chain Framework (v40s)

> **Simple LLM orchestration for local development**

A lightweight Python framework for building sequential and parallel prompt chains. Built for personal projects running locally.

## What It Does

- **Sequential Chaining**: Multi-step reasoning with context propagation
- **Parallel Execution**: Compare multiple models concurrently
- **Cost Tracking**: Know what you're spending on API calls
- **Simple Logging**: See what's happening

## Quick Start

```python
from chain import MinimalChainable
from main import build_models, prompt

# Initialize
client, model_names = build_models()
model_info = (client, model_names[0])

# Define and run chain
result, logs = MinimalChainable.run(
    context={"topic": "quantum computing"},
    model=model_info,
    callable=prompt,
    prompts=[
        "Summarize {{topic}} for a technical audience",
        "Identify the top 3 practical applications of {{output[-1]}}",
        "For each application, estimate market size and timeline: {{output[-1]}}"
    ]
)

# Results are saved to logs/ automatically
print(result)
```

## How It Works

```
Your Code
    ↓
Chain Executor
    ↓
Context Substitution ({{variables}})
    ↓
Model API Calls (OpenRouter)
    ↓
JSON Parsing & Output Chaining
    ↓
Logs & Results
```

## Project Structure

```
.
├── chain.py              # Core chaining logic
├── main.py              # Model client setup
├── demos/               # Example chains (31 demos)
├── tools/               # Cognitive exoskeleton tools
│   ├── content/        # Content creation tools
│   └── README.md       # Tool documentation
├── logs/               # Chain execution logs
└── output/             # Generated content
```

## Running Demos

```bash
# See all demos
ls demos/

# Run a demo
python demos/concept_simplifier/main.py

# Verify all demos work
./verify_demos.sh
```

## Making Your Own Chains

Check the demos for examples. Basic pattern:

1. Define context dict with your variables
2. Write prompts using `{{variable}}` and `{{output[-1]}}` syntax
3. Run with `MinimalChainable.run()`
4. Results auto-save to `logs/`

## Cost Tracking

Logs show:
- Tokens used per step
- Estimated cost per call
- Total cost for chain

Check `logs/` after each run.

## Cognitive Exoskeleton Tools

See `tools/README.md` for production tools built on this framework:
- Evergreen guide architect
- Content repurposer
- Medical research parser (coming)
- More tools as needed

---

**Simple chains for local AI work.**
