# 🔗 Artifact System - Knowledge That Persists

## What Just Happened?

You now have a **knowledge accumulation system** where every chain step creates reusable artifacts that future chains can reference.

This transforms your framework from:
- ❌ Ephemeral chain execution (results disappear after each run)

To:
- ✅ **Persistent knowledge graphs** (every run adds to a growing library)
- ✅ **Chain composition** (chains can build on other chains' work)
- ✅ **Zero-cost reuse** (reference previous insights without re-running)

## Core Concept

**Before:**
```python
# Run concept_simplifier("Machine Learning")
# Results: some JSON in logs/
# Next run: starts from scratch
```

**After:**
```python
# Run concept_simplifier("Machine Learning")
# Creates artifacts:
#   - artifacts/machine_learning/expert_educator.json
#   - artifacts/machine_learning/master_communicator.json
#   - artifacts/machine_learning/learning_designer.json
#   - artifacts/machine_learning/skilled_technical_writer.json

# Now ANY future chain can do:
"Compare {{artifact:machine_learning:expert_educator}} to {{artifact:neural_networks:expert_educator}}"

# No API calls needed - artifacts are local!
```

## What Was Built

### 1. `artifact_store.py` - The Foundation

A persistent knowledge store with:

**Save artifacts:**
```python
artifact_store.save(
    topic="Machine Learning",
    step_name="components",
    data={"components": [...]}
)
```

**Query artifacts:**
```python
# Get specific artifact
artifact_store.get("Machine Learning", "components")

# Query patterns
artifact_store.query("machine_learning:*")  # All ML artifacts
artifact_store.query("*:components")         # All components
artifact_store.query("*:*")                  # Everything

# List topics
artifact_store.list_topics()  # ["machine_learning", "quantum_physics", ...]
```

**Visualize knowledge:**
```python
print(artifact_store.visualize())
# 📚 Artifact Store
#
# 📖 machine_learning
#   └─ expert_educator (created: 2025-12-05 15:30)
#   └─ master_communicator (created: 2025-12-05 15:31)
```

### 2. Enhanced `chain.py`

**New parameters for `MinimalChainable.run()`:**
```python
result = MinimalChainable.run(
    context={...},
    model=model_info,
    callable=prompt,
    prompts=[...],
    artifact_store=artifact_store,  # ← NEW: Enable artifacts
    topic="Machine Learning"         # ← NEW: What to name artifacts
)
```

**Automatic artifact saving:**
- Every step automatically saves its output as an artifact
- Artifact names are extracted from prompt roles (e.g., "You are an expert educator" → `expert_educator`)
- Metadata tracks: timestamp, which prompt created it, which artifacts it used

**Artifact references in prompts:**
```python
prompts = [
    "Explain {{topic}}",
    "Use this prior knowledge: {{artifact:machine_learning:components}}"
]
```

The system automatically:
1. Finds `{{artifact:topic:step}}` patterns
2. Loads the artifact from disk
3. Replaces with the actual data
4. Tracks which artifacts were used

### 3. Updated `concept_simplifier.py`

Now automatically creates artifacts:
```bash
python tools/learning/concept_simplifier.py "Machine Learning"

# Creates artifacts/:
#   machine_learning/expert_educator.json
#   machine_learning/master_communicator.json
#   machine_learning/learning_designer.json
#   machine_learning/skilled_technical_writer.json
```

### 4. Demo: `demos/artifact_composition_demo.py`

Shows the "holy shit" moment:
1. Analyze "Neural Networks" → creates artifacts
2. Analyze "Human Brain" → creates artifacts
3. **NEW CHAIN** synthesizes both using `{{artifact:...}}` references

No re-computation. Pure composition.

## How to Use

### Try It Now

**1. Test the system:**
```bash
python test_artifacts.py
# Should see: ✅ ALL TESTS PASSED!
```

**2. Create your first artifacts:**
```bash
python tools/learning/concept_simplifier.py "Machine Learning"

# Look at artifacts/ directory:
ls artifacts/machine_learning/
# expert_educator.json
# master_communicator.json
# ...
```

**3. See artifact composition:**
```bash
python demos/artifact_composition_demo.py

# Analyzes "Neural Networks" and "Human Brain"
# Then synthesizes them WITHOUT re-running the analysis
```

### Using Artifacts in Your Own Chains

**Pattern 1: Enable artifact storage**
```python
from artifact_store import ArtifactStore

artifact_store = ArtifactStore()  # Creates artifacts/ directory

result = MinimalChainable.run(
    context={"topic": "Quantum Mechanics"},
    model=model_info,
    callable=prompt,
    artifact_store=artifact_store,
    topic="Quantum Mechanics",
    prompts=[...]
)

# Artifacts are auto-saved!
```

**Pattern 2: Reference artifacts in prompts**
```python
prompts = [
    # First, create base knowledge
    "Explain {{topic}} in simple terms",

    # Then build on it
    "Using {{output[-1]}}, create examples",

    # Then pull in external knowledge
    "Compare to what we know about Machine Learning: {{artifact:machine_learning:expert_educator}}",

    # Synthesize everything
    "Based on {{output[-1]}} and {{artifact:machine_learning:master_communicator}}, create a unified explanation"
]
```

**Pattern 3: Query the artifact library**
```python
artifact_store = ArtifactStore()

# What topics do we have?
topics = artifact_store.list_topics()
print(topics)  # ["machine_learning", "neural_networks", "quantum_mechanics"]

# What did we learn about ML?
ml_artifacts = artifact_store.query("machine_learning:*")
for key, data in ml_artifacts.items():
    print(f"{key}: {data}")

# Get all "components" across topics
all_components = artifact_store.query("*:components")
```

**Pattern 4: Chain composition**
```python
# This is the "chains of chains" pattern

artifact_store = ArtifactStore()

# Step 1: Run chain A
result_a = MinimalChainable.run(
    context={"topic": "Topic A"},
    artifact_store=artifact_store,
    topic="Topic A",
    prompts=[...]
)

# Step 2: Run chain B
result_b = MinimalChainable.run(
    context={"topic": "Topic B"},
    artifact_store=artifact_store,
    topic="Topic B",
    prompts=[...]
)

# Step 3: Synthesize using artifacts from both
synthesis = MinimalChainable.run(
    context={"topic_a": "Topic A", "topic_b": "Topic B"},
    artifact_store=artifact_store,
    topic="Synthesis",
    prompts=[
        "Compare {{artifact:topic_a:step_1}} to {{artifact:topic_b:step_1}}",
        "Synthesize insights from both"
    ]
)
```

## File Structure

```
artifacts/
  machine_learning/
    expert_educator.json       # Step 1 output
    expert_educator.meta.json  # Metadata
    master_communicator.json   # Step 2 output
    master_communicator.meta.json
  neural_networks/
    expert_educator.json
    ...
```

**Data files (`.json`)**: The actual artifact content

**Meta files (`.meta.json`)**: When created, by what tool, which artifacts it used

## What This Unlocks

### 1. **Knowledge Accumulation**
Every chain run adds to a growing library. After running concept_simplifier on 20 topics, you have a **reusable knowledge base** of:
- 20 × component breakdowns
- 20 × analogy sets
- 20 × example collections

### 2. **Zero-Cost Composition**
```python
# Build a curriculum by composing existing artifacts
curriculum_chain = [
    "Start with: {{artifact:basics:summary}}",
    "Add depth: {{artifact:intermediate:deep_dive}}",
    "Connect to: {{artifact:advanced:applications}}",
    "Synthesize everything"
]

# No API calls for steps 1-3! Pure artifact retrieval.
```

### 3. **Meta-Learning Ready**
You can now build chains that:
- **Analyze artifacts**: "What patterns appear across all {{artifact:*:components}}?"
- **Improve artifacts**: "Critique {{artifact:topic:step}} and create a better version"
- **Generate chains**: "Based on {{artifact:successful_topics:*}}, design a chain for new topic"

### 4. **Comparison & Analysis**
```python
"Compare these pedagogical approaches:
- {{artifact:topic_a:analogies}}
- {{artifact:topic_b:analogies}}
- {{artifact:topic_c:analogies}}

Which analogy style is most effective?"
```

### 5. **Curriculum Design**
```python
# Automatically compose a learning path
learning_path = [
    ("Prerequisites", "{{artifact:basics:components}}"),
    ("Core Concepts", "{{artifact:intermediate:components}}"),
    ("Applications", "{{artifact:advanced:examples}}"),
    ("Synthesis", "Create project using all three levels")
]
```

## Next Steps

### Immediate (Tonight)
- ✅ Test: `python test_artifacts.py`
- ✅ Try: `python tools/learning/concept_simplifier.py "Your Topic"`
- ✅ Explore: Browse `artifacts/` directory
- ✅ Demo: `python demos/artifact_composition_demo.py`

### This Weekend
1. **Update subject_connector** to use artifacts
2. **Build artifact browser CLI** (`python artifact_browser.py`)
3. **Create curriculum_builder.py** - chain that orchestrates multiple tools

### Next Week
1. **Meta-chain generator** - chain that designs chains by analyzing artifacts
2. **Web UI integration** - show artifacts in the visualization
3. **Artifact quality scoring** - rate and improve artifacts

## Technical Details

**Storage format:** JSON files in `artifacts/` directory

**Key normalization:** "Machine Learning" → `machine_learning`

**Auto-loading:** ArtifactStore loads all existing artifacts on init

**Thread-safe:** Not yet (add locking if needed for parallel chains)

**Max size:** No limits (consider chunking for large artifacts)

**Versioning:** Not yet (all saves overwrite - add versioning if needed)

## Philosophy

This isn't just "caching chain results."

This is **knowledge as infrastructure**.

Every chain run:
1. Consumes artifacts (prior knowledge)
2. Produces artifacts (new knowledge)
3. Enriches the ecosystem (growing library)

Over time, your artifact store becomes:
- A **textbook** (curated explanations of concepts)
- A **workshop** (tools for building new chains)
- A **laboratory** (data for meta-learning experiments)

**The chain IS the insight. The artifacts ARE the knowledge.**

---

Welcome to persistent prompt chaining.
