# Prompt Chaining Framework

> **Build AI systems that think in steps, not shots.**

A Python framework for creating sequential LLM workflows where each step builds on previous discoveries. Turn complex reasoning tasks that would fail as single prompts into reliable, emergent multi-step processes.

[![Tests](https://img.shields.io/badge/tests-passing-brightgreen)]() [![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)]() [![License: Private](https://img.shields.io/badge/license-Private-red.svg)]()

---

## 🎯 What Is This?

This framework lets you chain multiple LLM prompts together where **each step can reference outputs from previous steps**. This unlocks reasoning patterns impossible with single prompts.

**Quick Example:**

```python
from chain import MinimalChainable
from main import build_models, prompt

client, models = build_models()

result, _, _, _ = MinimalChainable.run(
    context={"topic": "Neural Networks"},
    model=(client, models[0]),
    callable=prompt,
    return_trace=True,
    prompts=[
        "Break down {{topic}} into 3-5 core components",
        "For each component in {{output[-1]}}, create a simple analogy",
        "Using {{output[-2]}} and {{output[-1]}}, write a 5th-grade explanation",
    ]
)

print(result[-1])  # Final explanation built from previous insights
```

**Why This Works:**
- Step 1 identifies the essential pieces
- Step 2 creates analogies for those *specific* pieces
- Step 3 synthesizes insights from both previous steps

This sequential reasoning **cannot work as a single prompt** because later steps depend on discoveries from earlier ones.

---

## 📚 Table of Contents

- [Why Prompt Chaining?](#-why-prompt-chaining)
- [Quick Start](#-quick-start)
- [Core Capabilities](#-core-capabilities)
- [Advanced Features](#-advanced-features)
- [Framework Enhancements](#-framework-enhancements)
- [Built-In Tools](#-built-in-tools)
- [Project Structure](#-project-structure)
- [Examples & Demos](#-examples--demos)
- [Documentation](#-documentation)
- [Contributing](#-contributing)

---

## 💡 Why Prompt Chaining?

### The Problem with Single Prompts

Single prompts are limited by:
- **Working memory constraints** - Can't hold complex analysis + synthesis simultaneously
- **No iteration** - Can't refine based on intermediate results
- **No emergent insights** - Can't discover connections that require multi-step reasoning

### What Chaining Unlocks

✨ **Emergent Insights** - Later steps reveal connections impossible to specify upfront
🔄 **Self-Refinement** - Critique and improve intermediate outputs
🎯 **Progressive Depth** - Start broad, zoom into specifics, then synthesize
🧬 **Complex Reasoning** - Break down problems that overwhelm single-shot thinking
🔀 **Multi-Perspective** - Analyze from different angles, then integrate
💡 **Discovery-Driven** - Each step builds on *what was actually discovered*, not just *what you planned*

### Real Example: The Concept Simplifier

This tool **cannot work as a single prompt**:

```
1. Decompose → Identify core components
2. Analogize → Create metaphors for THOSE components
3. Exemplify → Build examples using THOSE analogies
4. Synthesize → Combine everything into coherent explanation
```

Each step depends on *discoveries* from previous steps. You can't write the analogies until you know the components. You can't synthesize until you have both.

**The chain IS the insight.**

---

## 🚀 Quick Start

### Installation

```bash
# Clone and setup
python3 -m venv venv
source venv/bin/activate  # or: venv\Scripts\activate on Windows

# Install dependencies
pip install -r requirements.txt

# Configure API key
cp .env.example .env
# Edit .env and add your OpenRouter API key
```

### Run Your First Chain

```bash
# Try the concept simplifier
python tools/learning/concept_simplifier.py "Quantum Computing"

# Try the subject connector
python tools/learning/subject_connector.py "Poetry" --context "Machine Learning"

# Generate MS blog content
python tools/ms_blog/ms_content_tools.py "I forget my medication" --energy low
```

### Web UI (Optional)

```bash
# Start backend
python server/main.py

# In another terminal, start frontend
cd web && npm install && npm run dev

# Open http://localhost:5173
```

The web UI shows beautiful step-by-step chain visualization with token usage tracking.

---

## ⚙️ Core Capabilities

### 1. Sequential Chaining (MinimalChainable)

Run prompts in sequence, each building on previous outputs:

```python
from chain import MinimalChainable
from main import build_models, prompt

client, models = build_models()
model = (client, models[0])

result, prompts, usage, trace = MinimalChainable.run(
    context={"topic": "Recursion"},
    model=model,
    callable=prompt,
    return_trace=True,
    prompts=[
        "Define {{topic}} in one sentence",
        "Give 2 examples of {{output[-1]}}",
        "Explain why {{output[-2]}} is powerful in programming"
    ]
)

# result is a list of outputs from each step
# result[-1] is the final output
```

**Features:**
- `{{variable}}` - Context substitution
- `{{output[-1]}}` - Reference previous output
- `{{output[-1].field}}` - Extract JSON fields
- Automatic logging to `logs/`
- Full execution traces

### 2. Parallel Comparison (FusionChain)

Run the same chain across multiple models and compare results:

```python
from chain import FusionChain

def evaluator(responses):
    # Your custom scoring logic
    scores = [len(r) for r in responses]
    max_score = max(scores)
    normalized = [s/max_score for s in scores]
    best = responses[scores.index(max_score)]
    return best, normalized

result = FusionChain.run(
    context={"topic": "AI Safety"},
    models=[(client, name) for name in model_names],
    callable=prompt,
    evaluator=evaluator,
    get_model_name=lambda m: m[1],
    prompts=[...]
)

print(f"Best response: {result.top_response}")
print(f"Model scores: {result.performance_scores}")
```

### 3. Artifact System (Persistent Knowledge)

Save and reuse outputs across chains:

```python
from artifact_store import ArtifactStore

store = ArtifactStore()

# Chains automatically store outputs
result, _, _, _ = MinimalChainable.run(
    context={"topic": "Machine Learning"},
    model=model,
    callable=prompt,
    artifact_store=store,
    topic="machine_learning",
    prompts=[...]
)

# Later, reference those artifacts in new chains
prompts = [
    "Using {{artifact:machine_learning:components}}, explain supervised learning"
]
```

**Artifacts enable:**
- Cross-chain knowledge sharing
- Building on previous work
- Avoiding redundant analysis
- Progressive knowledge accumulation

### 4. Chain Composition (ChainComposer)

Build complex multi-chain workflows programmatically:

```python
from chain_composer import ChainComposer, ChainStep

composer = ChainComposer()

# Define a multi-chain workflow
steps = [
    ChainStep(
        name="Analyze concept",
        prompts=["Break down {{topic}} into components"],
        creates_artifact="components"
    ),
    ChainStep(
        name="Create curriculum",
        prompts=["Design a learning path for {{artifact:components}}"],
        depends_on=["components"]
    )
]

result = composer.compose(
    steps=steps,
    context={"topic": "Neural Networks"},
    model=model
)
```

### 5. Meta-Chain Generator (Self-Improving)

The system can design its own chains:

```python
from meta_chain_generator import MetaChainGenerator

generator = MetaChainGenerator()

# Describe what you want, get a chain that does it
chain = generator.design_chain(
    task="Analyze a business idea for feasibility",
    cognitive_moves=["decompose", "critique", "synthesize"],
    depth=4
)

# Run the generated chain
result = chain.execute(
    context={"idea": "AI-powered meal planning app"}
)
```

The meta-chain analyzes your task and generates optimal prompt sequences automatically.

---

## 🧠 Framework Enhancements

Three powerful extensions that unlock new reasoning capabilities:

### 1. Natural Reasoning Patterns ⭐⭐⭐⭐

**Module:** `natural_reasoning.py`

Formalize expert reasoning patterns as reusable chain templates:

- **Scientific Method** - Test hypotheses through observation, prediction, experiment, analysis
- **Socratic Dialogue** - Examine beliefs through systematic questioning
- **Design Thinking** - Human-centered problem solving (Empathize → Define → Ideate → Prototype → Test)
- **Judicial Reasoning** - Analyze cases using facts, principles, precedent, judgment
- **Root Cause Analysis (5 Whys)** - Dig beneath symptoms to find systemic causes

```python
from natural_reasoning import scientific_method, design_thinking

# Apply scientific method to a hypothesis
result, metadata = scientific_method(
    hypothesis="Regular exercise improves MS fatigue management",
    evidence_sources=["Study 1", "Study 2"]
)
print(result['conclusion']['verdict'])  # "Supported" / "Refuted" / "Inconclusive"

# Use design thinking for user-centered problem solving
solution, metadata = design_thinking(
    problem="MS patients struggle to track symptoms",
    constraints=["Low energy", "Brain fog"]
)
print(solution['prototype']['how_it_works'])
```

**Use for:** Teaching how experts think, applying proven patterns to any domain, creating "How experts think about X" blog content.

### 2. Adversarial Chains ⭐⭐⭐⭐⭐

**Module:** `adversarial_chains.py`

Use conflict and opposition to reveal truth (impossible with single prompts!):

- **Red Team vs Blue Team** - Adversarial debate with one side attacking, one defending, judge evaluating
- **Dialectical Synthesis** - Hegelian dialectic: Thesis → Antithesis → Synthesis
- **Adversarial Socratic** - Aggressive questioning to stress-test claims

```python
from adversarial_chains import red_vs_blue, dialectical

# Run adversarial debate
debate, metadata = red_vs_blue(
    topic="MS treatment strategies",
    position_to_defend="Aggressive DMTs should be prioritized",
    rounds=3
)
print(f"Winner: {metadata['winner']}")
print(debate['judgment']['verdict'])

# Find synthesis that transcends opposition
result, metadata = dialectical(
    thesis="Prioritize symptom management",
    domain="MS treatment philosophy"
)
print(result['synthesis']['synthesis_statement'])  # Transcendent position
```

**Use for:** Testing ideas rigorously, exploring controversial topics, red-teaming strategies, transcending binary thinking.

### 3. Emergence Measurement ⭐⭐⭐⭐

**Module:** `emergence_measurement.py`

Scientifically prove chains unlock insights impossible from single prompts:

```python
from emergence_measurement import measure_emergence, batch_measure

# Compare chain vs mega-prompt
comparison, metadata = measure_emergence(
    topic="Neural Networks",
    chain_function=concept_simplifier
)
print(f"Winner: {comparison['winner']}")  # "Chain" / "Baseline" / "Tie"

# Batch test for statistical significance
aggregate, results = batch_measure(
    topics=["Topic 1", "Topic 2", "Topic 3", "Topic 4", "Topic 5"],
    chain_function=concept_simplifier
)
print(aggregate['results']['chain_win_rate'])  # e.g., "73.3%"
print(aggregate['statistical_significance'])
```

**Measures across 5 dimensions:**
- Novelty (unique insights)
- Depth (sophistication)
- Coherence (logical flow)
- Pedagogical (understandability)
- Actionability (practical use)

**Use for:** Validating your chains work better, publishing research findings, convincing stakeholders with data.

**📖 Full Documentation:** See [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) for complete guide, examples, and API reference.

**🎬 Demos:**
```bash
python demos/natural_reasoning_demo.py
python demos/adversarial_chains_demo.py
python demos/emergence_measurement_demo.py
```

---

## 🛠️ Built-In Tools

The framework includes production-ready tools demonstrating best practices:

### Learning Tools

**📚 Concept Simplifier**
```bash
python tools/learning/concept_simplifier.py "Blockchain"
```
4-step chain: Decompose → Analogize → Exemplify → Synthesize

**🔗 Subject Connector**
```bash
python tools/learning/subject_connector.py "Philosophy" --context "Software Engineering"
```
4-step chain: Analyze each → Find connections → Evaluate → Design project

### MS Blog Content Generator

**🎯 Low-Energy Content Pipeline**
```bash
python tools/ms_blog/ms_content_tools.py "I struggle with daily planning" --energy low
```

Automatically generates Hugo-compatible markdown for:
- ✅ Prompt cards (AI prompts solving MS-related problems)
- ✅ Shortcut spotlights (Accessibility tool tutorials)
- ✅ Multi-phase guides (Complete system setups)
- ✅ Content ideas (Brainstorming from seed concepts)

**Features:**
- Auto-detects best format for your input
- Generates complete YAML front matter
- Includes examples, variations, troubleshooting
- Validates content quality
- Provides review checklist
- Saves to Hugo content directory

**Try the interactive demo:**
```bash
python demos/ms_blog_demo.py --interactive
```

See [tools/ms_blog/README.md](tools/ms_blog/README.md) for full documentation.

---

## 🔬 Advanced Features

### Execution Traces

Get complete visibility into chain execution:

```python
result, prompts, usage, trace = MinimalChainable.run(
    return_trace=True,
    prompts=[...]
)

# trace contains:
{
    "steps": [
        {
            "step_number": 1,
            "role": "Educator",
            "prompt": "...",
            "response": "...",
            "tokens": {"prompt": 50, "completion": 200}
        }
    ],
    "final_result": {...},
    "total_tokens": 500
}
```

### Automatic Logging

All chains automatically log to `logs/` with:
- Timestamped filename
- All prompts and responses
- Token usage per step
- Total execution time
- Markdown formatted for readability

### Cognitive Move Patterns

The framework recognizes common reasoning patterns:

- **decompose** - Break complex things into parts
- **analogize** - Create metaphors and comparisons
- **exemplify** - Generate concrete examples
- **synthesize** - Combine insights into coherent whole
- **critique** - Evaluate and find flaws
- **abstract** - Generalize from specifics
- **apply** - Take theory to practice
- **connect** - Find relationships between ideas

These can be composed into powerful chains.

### Recipe System

Save and reuse chain patterns:

```python
# Create a recipe
recipe = {
    "name": "Concept Comparison",
    "steps": [
        {"name": "Analyze A", "prompts": [...]},
        {"name": "Analyze B", "prompts": [...]},
        {"name": "Compare", "prompts": [...]}
    ]
}

# Use the recipe with different inputs
result = run_recipe(recipe, context={"A": "Python", "B": "JavaScript"})
```

---

## 📁 Project Structure

```
.
├── 📄 README.md                          # You are here
│
├── 🔧 Source Code
│   ├── src/core/                         # Core framework
│   │   ├── chain.py                      # MinimalChainable, FusionChain
│   │   ├── main.py                       # Model setup and utilities
│   │   ├── artifact_store.py             # Persistent knowledge system
│   │   ├── chain_composer.py             # Multi-chain workflows
│   │   └── meta_chain_generator.py       # Self-improving chain design
│   │
│   ├── src/enhancements/                 # Framework enhancements
│   │   ├── natural_reasoning.py          # 5 expert reasoning patterns
│   │   ├── adversarial_chains.py         # Dialectical reasoning
│   │   └── emergence_measurement.py      # Scientific validation
│   │
│   └── src/utils/                        # Utility modules
│       ├── artifact_browser.py           # Artifact inspector
│       └── demo_utils.py                 # Demo helpers
│
├── 🧪 Tests
│   ├── tests/test_chain.py               # Core chain tests
│   ├── tests/test_artifacts.py           # Artifact system tests
│   ├── tests/test_chain_composer.py      # Composer tests
│   └── tests/test_meta_chain.py          # Meta-chain tests
│
├── 📚 Documentation
│   ├── docs/QUICKSTART.md                # 5-minute getting started
│   ├── docs/ARCHITECTURE.md              # System design & features
│   ├── docs/TESTING.md                   # Testing guide
│   ├── docs/DEMOS.md                     # Demo scripts
│   └── docs/IDEAS.md                     # Future enhancements
│
├── 🛠️ Built-In Tools
│   ├── tools/learning/
│   │   ├── concept_simplifier.py         # Educational chain example
│   │   └── subject_connector.py          # Connection-finding example
│   │
│   ├── tools/ms_blog/
│   │   ├── ms_content_tools.py           # MS blog content generator
│   │   ├── cli.py                        # Command-line interface
│   │   └── README.md                     # Full documentation
│   │
│   └── tools/tool_utils.py               # Shared utilities
│
├── 🎬 Demos
│   ├── demos/natural_reasoning_demo.py   # Expert reasoning patterns
│   ├── demos/adversarial_chains_demo.py  # Dialectical reasoning
│   ├── demos/emergence_measurement_demo.py # Validation framework
│   ├── demos/meta_chain_demo.py          # Self-improving chains
│   └── demos/ms_blog_demo.py             # MS blog tool showcase
│
├── 🎨 Web Interface
│   ├── server/main.py                    # FastAPI backend
│   ├── web/                              # React frontend
│   │   └── src/components/patterns/      # Reasoning UI patterns
│
├── 📊 Runtime Data
│   ├── output/                           # Generated content
│   ├── logs/                             # Execution logs
│   └── artifacts/                        # Saved artifacts
│
├── 🔧 Scripts
│   └── scripts/                          # Utility scripts
│
└── ⚙️ Configuration
    ├── .env.example                      # API key template
    ├── context/user_profile.json         # User preferences
    └── requirements.txt                  # Python dependencies
```

---

## 🎯 Examples & Demos

### Example 1: Educational Chain

Break down complex topics into 5th-grade explanations:

```bash
python tools/learning/concept_simplifier.py "Neural Networks"
```

**Output:**
- Core components identified
- Analogies for each component
- Concrete examples
- Full synthesis

### Example 2: Connection Finding

Discover unexpected links between subjects:

```bash
python tools/learning/subject_connector.py "Music Theory" --context "Data Science"
```

**Output:**
- Analysis of each field
- Surprising connections
- Why they matter
- Project idea leveraging both

### Example 3: Content Generation

Generate blog content on low-energy days:

```bash
python tools/ms_blog/ms_content_tools.py "I can't focus due to brain fog" --energy low
```

**Output:**
- Auto-detects best format (prompt card/shortcut/guide)
- Generates complete Hugo markdown
- Includes examples and troubleshooting
- Ready to publish

### Example 4: Multi-Chain Workflow

Build a complete learning curriculum:

```bash
python demos/curriculum_builder_demo.py
```

**Output:**
- Topic analysis
- Learning path design
- Exercises for each step
- Assessment criteria

### Example 5: Self-Improving System

Let the system design its own chains:

```bash
python demos/meta_chain_demo.py
```

**Output:**
- Analyzes your task
- Designs optimal chain
- Generates prompts
- Executes and refines

---

## 📖 Documentation

| Document | Description |
|----------|-------------|
| [QUICKSTART.md](docs/QUICKSTART.md) | Get up and running in 5 minutes |
| [ARCHITECTURE.md](docs/ARCHITECTURE.md) | System design, core features, and technical specs |
| [TESTING.md](docs/TESTING.md) | Guide to testing frameworks and verification |
| [DEMOS.md](docs/DEMOS.md) | Demo scripts and walkthroughs (Full & Quick) |
| [IDEAS.md](docs/IDEAS.md) | Future features and roadmap |
| [WHATS_NEW.md](docs/WHATS_NEW.md) | Recent updates and changes |


### Key Concepts

| Concept | Explanation |
|---------|-------------|
| **Context** | Variables passed to prompts: `{{variable}}` |
| **Output References** | Access previous steps: `{{output[-1]}}` |
| **Chain** | Sequence of prompts where each builds on previous |
| **Artifact** | Saved output reusable across chains |
| **Trace** | Complete execution history with tokens |
| **Cognitive Move** | Reasoning pattern (decompose, synthesize, etc.) |

---

## 🧪 Testing

```bash
# Test core framework
python chain_test.py

# Test chain composer
python test_chain_composer.py

# Test artifact system
python test_artifacts.py

# Test meta-chain generator
python test_meta_chain.py

# Test MS blog tools
python tools/ms_blog/test_ms_tools.py

# Run all demos
./verify_demos.sh
```

**Current Status:** ✅ All tests passing (6/6 MS tools, 100% core framework)

---

## 🎨 Use Cases

### ✅ Already Built

- **Education** - Break down complex topics into simple explanations
- **Content Creation** - Generate blog posts, guides, and tutorials
- **Concept Exploration** - Find unexpected connections between ideas
- **Curriculum Design** - Build complete learning paths
- **Meta-Learning** - System designs its own chains

### 🚧 Coming Soon

- **Code Analysis** - Understand complex codebases through chains
- **Decision Support** - Multi-perspective analysis of choices
- **Research Synthesis** - Combine findings from multiple sources
- **Adversarial Reasoning** - Red team / Blue team debates
- **Design Thinking** - Structured problem-solving workflows

See [IDEAS.md](IDEAS.md) for the full roadmap.

---

## 💰 Cost Management

- OpenRouter provides access to 100+ models
- Start with free/cheap models (gemini-flash-1.5)
- Execution traces show token usage per step
- Set billing alerts in OpenRouter dashboard
- Typical chain costs: $0.001 - $0.05

**Example costs:**
- Concept Simplifier: ~500-1000 tokens (~$0.002)
- MS Blog Generator: ~2000-4000 tokens (~$0.01)
- Meta-Chain: ~1000-2000 tokens (~$0.005)

---

## 🤝 Contributing

This is a personal learning project, but feedback and ideas are welcome!

**Ways to contribute:**
- 🐛 Report bugs in GitHub Issues
- 💡 Suggest features in IDEAS.md
- 📚 Improve documentation
- 🔧 Build new tools using the framework
- 🧪 Add test cases

---

## ⚠️ Ethical Note

This framework enables powerful analytical tools. Some patterns reveal uncomfortable truths about persuasion, manipulation, and strategic deception.

**Understanding ≠ Endorsing**

These patterns exist whether you acknowledge them or not. This knowledge is for:
- ✅ **Defense** - See through manipulation
- ✅ **Awareness** - Make better decisions
- ✅ **Education** - Understand how systems work

Not for:
- ❌ **Offense** - Deploy manipulative tactics
- ❌ **Deception** - Mislead others
- ❌ **Harm** - Cause damage

Use responsibly.

---

## 🔗 Links

- [OpenRouter API](https://openrouter.ai/) - Multi-model LLM access
- [Anthropic Claude](https://www.anthropic.com/) - Recommended model
- [FastAPI](https://fastapi.tiangolo.com/) - Backend framework
- [React](https://react.dev/) - Frontend framework

---

## 📜 License

Personal learning project - Private repository

---

## 🙏 Acknowledgments

- **OpenRouter** - For making 100+ models accessible
- **Anthropic** - For Claude, the best reasoning model
- **The LLM Community** - For advancing the field

---

## 🚀 Quick Command Reference

```bash
# Setup
python3 -m venv venv && source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env  # Then add your API key

# Try Built-In Tools
python tools/learning/concept_simplifier.py "Your Topic"
python tools/learning/subject_connector.py "Subject A" --context "Subject B"
python tools/ms_blog/ms_content_tools.py "Your problem" --energy low

# Run Demos
python demos/ms_blog_demo.py --interactive
python demos/meta_chain_demo.py
python demos/curriculum_builder_demo.py

# Test Everything
python chain_test.py
python tools/ms_blog/test_ms_tools.py
./verify_demos.sh

# Web UI
python server/main.py  # Backend
cd web && npm run dev  # Frontend (in another terminal)
```

---

<div align="center">

**[Get Started](#-quick-start)** • **[Documentation](#-documentation)** • **[Examples](#-examples--demos)** • **[Advanced Features](#-advanced-features)**

Built with ❤️ by passionate learners, for passionate learners.

**See what prompt chaining can unlock.**

</div>
