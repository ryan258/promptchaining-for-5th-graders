# Reference Tool Implementations

This directory contains reference implementations demonstrating best practices for building prompt chaining tools.

## Philosophy

These tools are designed for **low-energy usability**. If you can't use them on a bad day, they're not working.

### Design Principles

1. **Zero-config start**: Load user context automatically from `context/user_profile.json`
2. **CLI-first**: Accept input via args or stdin
3. **Fast**: < 3 minutes for 80% of use cases
4. **Energy ROI positive**: Value out > effort in
5. **Professional output**: Structured JSON + markdown with comprehensive analysis
6. **Execution traces**: Full chain visualization data for web UI

## Reference Tools

### 🧭 Concept Simplifier
Break complex topics into components, analogies, examples, and a concise explainer.

**Usage:**
```bash
python tools/learning/concept_simplifier.py "Diffusion models in AI"
python tools/learning/concept_simplifier.py "Topic" --context "Audience or constraints"
```

**Output:** JSON in `output/learning/concept_simplifier/`
- Components with significance
- Analogies with breakdown points
- Concrete examples with self-check questions
- Synthesized explainer
- Common pitfalls and next steps

**Chain structure (4 steps):**
1. Expert educator → Decompose concept into components
2. Analogy specialist → Create memorable analogies for each
3. Learning designer → Build concrete examples with self-checks
4. Technical writer → Synthesize cohesive explainer

**Why it demonstrates best practices:**
- Persona-driven prompts (expert roles)
- Progressive refinement (each step builds on last)
- Structured JSON output
- Execution trace for web UI visualization
- Context-aware (user profile integration)

---

### 🔗 Subject Connector
Find surprising links between two subjects, why they matter, and design a project that uses both.

**Usage:**
```bash
python tools/learning/subject_connector.py "History" --context "Physics"
python tools/learning/subject_connector.py "Subject A" --context "Subject B"
```

**Output:** JSON in `output/learning/subject_connector/`
- Unexpected connections between subjects
- Why connections matter (practical significance)
- Project idea with expected outputs

**Chain structure (4 steps):**
1. Domain analyst → Analyze each subject independently
2. Connection finder → Identify unexpected links
3. Significance evaluator → Explain why connections matter
4. Project designer → Design practical application

**Why it demonstrates best practices:**
- Multi-subject integration
- Divergent → convergent thinking pattern
- Practical output (actionable project)
- Demonstrates {{output[-1]}} references clearly

---

## Common Patterns

Both reference tools follow this structure:

```python
from tools.tool_utils import setup_project_root, load_user_context, get_input_from_args
from chain import MinimalChainable
from main import build_models, prompt

def my_tool(topic: str, additional_context: str = ""):
    # 1. Load user preferences
    user_profile = load_user_context(project_root)

    # 2. Build models
    client, model_names = build_models()
    model_info = (client, model_names[0])

    # 3. Run chain with execution trace
    result, prompts, usage, trace = MinimalChainable.run(
        context={"topic": topic, ...},
        model=model_info,
        callable=prompt,
        return_trace=True,  # ← Important for web UI!
        prompts=[...]
    )

    # 4. Save execution trace (not raw results)
    with open(output_path, "w") as f:
        json.dump(trace, f, indent=2)

    # 5. Save logs
    MinimalChainable.log_to_markdown("my_tool", prompts, result, usage)
```

## Key Features

### Execution Traces (NEW!)

All tools now return execution traces:
```json
{
  "steps": [
    {
      "step_number": 1,
      "role": "Expert Educator",
      "prompt": "Filled-in prompt...",
      "response": {...},
      "tokens": 125
    }
  ],
  "final_result": {...},
  "total_tokens": 500
}
```

This enables the web UI's beautiful chain visualization where users can:
- See prompts with variables already filled in
- See responses formatted for readability
- Track token usage per step
- Understand the AI's reasoning flow

### Tool Utilities

`tool_utils.py` provides shared functionality:
- `setup_project_root()` - Path configuration
- `load_user_context()` - User profile loading
- `get_input_from_args()` - CLI argument parsing
- `open_in_editor()` - Editor integration
- `read_interactive_input()` - Multi-line input handling

## Building Your Own Tool

1. **Copy a reference implementation** as your starting point
2. **Design your prompt chain** - What sequence of steps leads to the insight?
3. **Define clear personas** - "You are a [expert role]..."
4. **Use structured output** - JSON with clear field names
5. **Test with web UI** - Does the chain visualization make sense?
6. **Enable `return_trace=True`** - Always!

## Full Tool Catalog

The complete catalog of 33 production tools has been moved to a separate repository for easier management and plugin-based architecture.

These 2 reference implementations demonstrate all the patterns used across the full catalog.

## Energy Cost vs Return

**Concept Simplifier:**
- Energy cost: Low (2-3 minutes)
- Energy return: High (deep understanding shortcut)
- Net: Strongly positive ✅

**Subject Connector:**
- Energy cost: Low (2-3 minutes)
- Energy return: Medium-High (creative insights, project ideas)
- Net: Positive ✅

## What Makes a Good Prompt Chain?

1. **Each step is necessary** - Can't skip without losing insight
2. **Later steps impossible without earlier ones** - True dependency
3. **Progressive refinement** - Each step adds precision/depth
4. **Clear personas** - Each step has a distinct expert role
5. **Structured output** - Parseable, reusable data
6. **Execution trace** - Transparent reasoning for users

## Testing Your Tool

```bash
# Test CLI
python tools/learning/your_tool.py "Test input" --context "Extra context"

# Test with web UI
# 1. Start backend: python3 server/main.py
# 2. Start frontend: cd web && npm run dev
# 3. Select your tool in the UI
```

---

For more information, see the main [README.md](../README.md) in the project root.
