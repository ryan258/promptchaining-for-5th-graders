# Getting Started

## Prerequisites

- Python 3.8+
- OpenRouter API key (free tier available)

## Installation

### 1. Clone and setup virtual environment
```bash
python -m venv venv
source venv/bin/activate  # Mac/Linux
# or
venv\Scripts\activate     # Windows
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure API key
```bash
cp .env.example .env
```

Edit `.env` and add your OpenRouter API key:
```
OPENROUTER_API_KEY=sk-or-v1-...
```

Get a key at [openrouter.ai/keys](https://openrouter.ai/keys)

### 4. Verify setup
```bash
python main.py
```

Expected output:
- Setup verification message
- Example prompt chain execution
- Generated outputs saved to timestamped files

## First Steps

### Run a demo
```bash
cd demos/concept_simplifier
python main.py
```

### Modify a demo
Edit the demo's `main.py`:
- Change the `context` variables
- Modify the `prompts` list
- Try different models from `model_names`

### Create your own chain

```python
from chain import MinimalChainable
from main import build_models, prompt

client, model_names = build_models()
model_info = (client, model_names[0])

outputs, prompts = MinimalChainable.run(
    context={"input": "your data here"},
    model=model_info,
    callable=prompt,
    prompts=[
        "Analyze {{input}}",
        "Based on {{output[-1]}}, suggest improvements",
        "Prioritize {{output[-1]}} by impact"
    ]
)

for i, output in enumerate(outputs):
    print(f"\nStep {i+1}:\n{output}")
```

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

**Empty model_names list**
- Check `build_models()` return value
- Verify OpenRouter API is accessible

## Next Steps

1. Run all demos to see different patterns
2. Check `IDEAS.md` for project inspiration
3. Read `chain.py` to understand the implementation
4. Experiment with custom evaluator functions
5. Try multi-model comparison with FusionChain

## Key Concepts

**Context variables**: `{{variable}}` gets replaced from context dict

**Output references**: `{{output[-1]}}` = last output, `{{output[-2]}}` = second-to-last

**JSON field access**: `{{output[-1].field_name}}` extracts fields from JSON responses

**Model info tuple**: `(client, model_name)` required for prompt function

## Cost Management

- OpenRouter shows per-request costs
- Start with free/cheap models (gemini-flash-1.5)
- Set up billing alerts in OpenRouter dashboard
- Use caching during development to avoid repeated calls

## Development Tips

- Save outputs to files for later review
- Use print statements to debug context substitution
- Test with mock callables before hitting real APIs
- Start with short chains, then expand

---

That's it! You're ready to start building prompt chains.
