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
├── chain.py              # Core framework (MinimalChainable, FusionChain)
├── main.py               # OpenRouter API client + examples
├── chain_test.py         # Unit tests
├── HAPPY-PATH.md         # Beginner-friendly getting started guide
├── GETTING_STARTED.md    # Technical setup guide
├── ROADMAP.md            # Project roadmap and demo ideas (40+ concepts!)
├── demos/                # 18 example implementations
│   ├── Educational Foundations (8 demos)
│   │   ├── character_evolution_engine/    ✅ with logging
│   │   ├── common_ground_finder/
│   │   ├── concept_simplifier/            ✅ with logging
│   │   ├── emergence_simulator/           ✅ with logging
│   │   ├── historical_what_if_machine/
│   │   ├── knowledge_time_machine/        ✅ with logging
│   │   ├── problem_solution_spider/       ✅ with logging
│   │   └── subject_connector/             ✅ with logging
│   │
│   └── Metagame X-Ray Vision (10 demos) 🔥
│       ├── consensus_manufacturing_detective/  ✅ NEW
│       ├── corporate_theater_director/         ✅ NEW
│       ├── credential_inflation_analyzer/      ✅ NEW
│       ├── goodharts_law_predictor/            ✅ NEW
│       ├── meeting_dynamics_forensics/         ✅ NEW
│       ├── narrative_warfare_analyst/          ✅ NEW
│       ├── platform_lock_in_forensics/         ✅ NEW
│       ├── regulatory_capture_mapper/          ✅ NEW
│       ├── revealed_preference_detective/      ✅ NEW
│       └── status_game_decoder/                ✅ NEW
│
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

### Educational Foundations (8 demos)

Classic prompt chaining patterns for learning and exploration:

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

### Metagame X-Ray Vision (10 demos) 🔥

**NEW**: Demos that reveal the hidden games beneath surface games. These expose uncomfortable truths about how systems actually work vs. how they claim to work.

> "The game about the game. Understanding metagames is the ultimate strategic edge."

| Demo | Reveals | Example Insight |
|------|---------|-----------------|
| **status_game_decoder** | Social power dynamics | "They're debating ideas" → Actually battling for who defines "smart" |
| **credential_inflation_analyzer** | Signaling arms races | Bachelor's (2000) → Master's (2010) → PhD (2025) for same job |
| **corporate_theater_director** | Stated vs actual values | "We value innovation" → Actually punish all failures |
| **meeting_dynamics_forensics** | Real power structures | Org chart vs interruption patterns = who has actual power |
| **revealed_preference_detective** | True values via behavior | "I care about privacy" → Uses services that sell data |
| **regulatory_capture_mapper** | Who regulations really serve | "Consumer protection" → Barriers to entry for competition |
| **platform_lock_in_forensics** | Strategic traps | Free tier → network effects → price increase (you're trapped) |
| **goodharts_law_predictor** | Metric gaming | "Lines of code" metric → Verbose code, lower productivity |
| **narrative_warfare_analyst** | Frame control battles | "Tax relief" vs "Tax cuts for rich" = same policy, frame war |
| **consensus_manufacturing_detective** | How "truth" gets created | "Everyone knows X" = platforms repeated it until it seemed true |

**What makes metagame demos different:**
- 🎭 Surface game vs actual game analysis
- 💡 Incentive forensics - what's rewarded reveals what's valued
- 🔍 Pattern recognition across domains
- 🎯 Predictive power from understanding real games
- ⚡ Uncomfortable truths that make you slightly queasy (means they're working)

**Metagame Principles Taught:**
1. Revealed Preferences > Stated Preferences
2. Incentives > Intentions
3. Frame Control = Game Control
4. Exceptions Reveal Rules (who can break them = who has power)
5. Metrics Shape Reality (Goodhart's Law)
6. The Real Game is Meta

See [ROADMAP.md](ROADMAP.md) for 20+ more exceptional demo concepts!

### Running Demos
```bash
# Run the main proof-of-concept
python main.py

# Run a classic demo
python demos/concept_simplifier/main.py

# Run a metagame demo (reveals uncomfortable truths)
python demos/revealed_preference_detective/main.py
python demos/status_game_decoder/main.py

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

**Truth-seeking**: Metagame demos reveal uncomfortable realities about power and strategy.

## Use Cases

### Classic Applications
- Multi-step reasoning tasks
- Content generation with refinement
- Research and analysis workflows
- Educational content creation
- Creative writing assistance
- Decision-making frameworks
- Experiment tracking and logging

### Metagame Analysis (NEW)
- Decode hidden power dynamics in organizations
- Understand incentive structures vs stated values
- Predict how metrics will be gamed
- Analyze narrative framing battles
- Identify platform lock-in traps
- Map regulatory capture patterns
- Develop immunity to manipulation

## Technical Notes

- Uses ThreadPoolExecutor for parallel model execution in FusionChain
- Automatically parses JSON responses (including markdown code blocks)
- Handles both string and structured (JSON) outputs
- Model-agnostic: works with any OpenAI-compatible API
- Graceful error handling for file operations
- UTF-8 encoding for all file outputs

## Recent Updates

### December 2024 - Metagame X-Ray Vision
- ✅ Added 10 metagame analysis demos that reveal hidden strategic layers
- ✅ Status Game Decoder, Revealed Preference Detective, Goodhart's Law Predictor, and more
- ✅ Each demo exposes gap between stated game and actual game
- ✅ Teaches critical thinking about power, incentives, and manipulation

### November 2024 - Logging & Documentation
- ✅ Added automatic markdown logging to all demos
- ✅ Simplified FusionChain to parallel-only execution
- ✅ Added HAPPY-PATH.md beginner guide
- ✅ Improved error handling in logging
- ✅ Migrated from Google Gemini to OpenRouter API

See [ROADMAP.md](ROADMAP.md) for 20+ exceptional demo concepts and future plans.

## Documentation

- **[HAPPY-PATH.md](HAPPY-PATH.md)** - Beginner-friendly getting started guide
- **[GETTING_STARTED.md](GETTING_STARTED.md)** - Technical setup and concepts
- **[ROADMAP.md](ROADMAP.md)** - Project roadmap with 40+ demo concepts
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
