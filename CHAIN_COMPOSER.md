# 🎼 Chain Composer - Orchestrate Chains of Chains

## What Is This?

The Chain Composer lets you **orchestrate multiple chains together** to build complex workflows that would be impossible with single chains.

Think of it like:
- **Single prompt**: Ask one question
- **Prompt chain**: Ask a sequence of questions that build on each other
- **Chain composition**: Run multiple different chains and synthesize their results

## The Magic

**You can now do this:**

```python
from chain_composer import ChainRecipe, quick_compose

# Automatically: analyze 3 topics, find connections, build curriculum
result = quick_compose(
    "learning_curriculum",
    topics=["Python Basics", "Data Structures", "Algorithms"]
)

# This orchestrates ~7 chains automatically!
```

## What Was Built

### 1. `chain_composer.py` - The Orchestration Engine

**Core Classes:**

**`ChainStep`** - A single step in a composition
```python
# Run a tool
ChainStep(
    name="Analyze ML",
    step_type="tool",
    tool_name="concept_simplifier",
    tool_args={"topic": "Machine Learning"}
)

# Run a custom chain
ChainStep(
    name="Synthesize",
    step_type="chain",
    topic="synthesis",
    prompts=[
        "Analyze {{artifact:topic_a:components}}",
        "Compare to {{artifact:topic_b:components}}"
    ]
)

# Synthesize artifacts
ChainStep(
    name="Find patterns",
    step_type="synthesize",
    artifact_pattern="*:components"  # All components
)
```

**`ChainComposer`** - Orchestrates steps
```python
composer = ChainComposer()

steps = [
    ChainStep(...),
    ChainStep(...),
    ChainStep(...)
]

result = composer.compose(steps)
# Returns: CompositionResult with execution details
```

**`ChainRecipe`** - Pre-built composition patterns
```python
# Recipe 1: Compare two concepts
steps = ChainRecipe.concept_comparison("AI", "Human Brain")

# Recipe 2: Build learning curriculum
steps = ChainRecipe.learning_curriculum(["Topic A", "Topic B", "Topic C"])

# Recipe 3: Progressive depth explanations
steps = ChainRecipe.progressive_depth("Quantum Mechanics")
```

### 2. Three Built-In Recipes

**Recipe #1: Concept Comparison**
```python
ChainRecipe.concept_comparison(topic_a, topic_b)
```

Automatically:
1. Run `concept_simplifier` on topic A
2. Run `concept_simplifier` on topic B
3. Run `subject_connector` to find connections
4. Synthesize all artifacts into insights

**Recipe #2: Learning Curriculum**
```python
ChainRecipe.learning_curriculum(["Python", "Data Structures", "Algorithms"])
```

Automatically:
1. Run `concept_simplifier` on each topic
2. Run `subject_connector` between adjacent topics
3. Synthesize into a 4-week curriculum with:
   - Weekly learning objectives
   - Key concepts
   - Practice exercises
   - Progression plan

**Recipe #3: Progressive Depth**
```python
ChainRecipe.progressive_depth("Recursion")
```

Automatically:
1. Explain for 5th grader
2. Explain for high school student
3. Explain for college student
4. Explain for expert
5. Analyze the pedagogical progression

### 3. Demos

**`demos/curriculum_builder_demo.py`** - Shows all three recipes

Run with:
```bash
python demos/curriculum_builder_demo.py

# Then choose:
# 1 = Full curriculum builder
# 2 = Quick comparison
# 3 = Progressive depth
```

**`test_chain_composer.py`** - Test suite ✅ ALL TESTS PASSED

## How to Use

### Pattern 1: Use a Recipe

**Easiest way:**
```python
from chain_composer import quick_compose

# One line to compare concepts
result = quick_compose(
    "concept_comparison",
    topic_a="Neural Networks",
    topic_b="Human Brain"
)

print(result.visualize())
```

**Or manually:**
```python
from chain_composer import ChainComposer, ChainRecipe

composer = ChainComposer()
steps = ChainRecipe.concept_comparison("AI", "Brain")
result = composer.compose(steps)
```

### Pattern 2: Build Custom Compositions

```python
from chain_composer import ChainComposer, ChainStep

composer = ChainComposer()

steps = [
    # Step 1: Analyze first topic
    ChainStep(
        name="Analyze Python",
        step_type="tool",
        tool_name="concept_simplifier",
        tool_args={"topic": "Python"}
    ),

    # Step 2: Analyze second topic
    ChainStep(
        name="Analyze JavaScript",
        step_type="tool",
        tool_name="concept_simplifier",
        tool_args={"topic": "JavaScript"}
    ),

    # Step 3: Custom synthesis
    ChainStep(
        name="Compare programming paradigms",
        step_type="chain",
        topic="language_comparison",
        prompts=[
            """Compare Python and JavaScript:

Python: {{artifact:python:expert_educator}}
JavaScript: {{artifact:javascript:expert_educator}}

What are the fundamental differences in philosophy?

Respond in JSON:
{
  "philosophical_differences": ["...", "..."],
  "use_case_guidance": "When to use which",
  "learning_path": "Which to learn first and why"
}"""
        ]
    )
]

result = composer.compose(steps)
```

### Pattern 3: Orchestrate Existing Artifacts

```python
# You already have artifacts from previous runs
# Now synthesize them without re-running

composer = ChainComposer()

steps = [
    ChainStep(
        name="Meta-analysis",
        step_type="synthesize",
        artifact_pattern="*:components",  # All component analyses
        topic="meta_analysis"
    )
]

result = composer.compose(steps)

# This analyzes ALL component breakdowns across ALL topics
# Finding meta-patterns in how you break down concepts
```

### Pattern 4: Build Workflows

```python
# Complex workflow: Research → Synthesize → Design
steps = [
    # Research phase
    ChainStep(name="Research A", step_type="tool", ...),
    ChainStep(name="Research B", step_type="tool", ...),
    ChainStep(name="Research C", step_type="tool", ...),

    # Synthesis phase
    ChainStep(name="Find connections", step_type="tool", ...),
    ChainStep(name="Identify gaps", step_type="chain", ...),

    # Design phase
    ChainStep(name="Propose solution", step_type="chain", ...),
    ChainStep(name="Generate curriculum", step_type="chain", ...)
]

result = composer.compose(steps)
```

## What This Unlocks

### 1. **Automatic Curriculum Generation**

```python
topics = ["Linear Algebra", "Calculus", "Statistics", "Machine Learning"]
result = quick_compose("learning_curriculum", topics=topics)

# Automatically creates:
# - Analysis of each topic
# - Connections between them
# - 4-week curriculum
# - Learning objectives
# - Practice exercises
```

### 2. **Multi-Concept Analysis**

```python
# Analyze 5 concepts and find emergent patterns
for topic in ["Concept A", "B", "C", "D", "E"]:
    composer.compose([
        ChainStep(name=f"Analyze {topic}", step_type="tool", ...)
    ])

# Then synthesize
composer.compose([
    ChainStep(
        name="Find meta-patterns",
        step_type="synthesize",
        artifact_pattern="*:components"
    )
])
```

### 3. **Pedagogical Experiments**

```python
# Test different explanation strategies
strategies = ["analogy-first", "example-first", "definition-first"]

for strategy in strategies:
    composer.compose([
        ChainStep(
            name=f"Explain using {strategy}",
            step_type="chain",
            topic=f"quantum_{strategy}",
            prompts=[f"Explain quantum mechanics using {strategy} approach"]
        )
    ])

# Then compare effectiveness
composer.compose([
    ChainStep(
        name="Compare strategies",
        step_type="chain",
        prompts=["Which explanation strategy worked best? ..."]
    )
])
```

### 4. **Knowledge Graph Building**

```python
# Systematically build knowledge graph
domains = ["Math", "Physics", "CS", "Biology"]

# Analyze each
for domain in domains:
    composer.compose([ChainStep(...)])

# Find connections
for i, domain_a in enumerate(domains):
    for domain_b in domains[i+1:]:
        composer.compose([
            ChainStep(
                name=f"Connect {domain_a} & {domain_b}",
                step_type="tool",
                tool_name="subject_connector",
                tool_args={"subject_a": domain_a, "subject_b": domain_b}
            )
        ])

# Now you have a complete knowledge graph!
```

## Step Types

### 1. Tool Steps

Run existing tools (concept_simplifier, subject_connector):

```python
ChainStep(
    name="Analyze topic",
    step_type="tool",
    tool_name="concept_simplifier",
    tool_args={"topic": "Machine Learning"}
)
```

### 2. Chain Steps

Run custom prompt chains:

```python
ChainStep(
    name="Custom analysis",
    step_type="chain",
    topic="my_topic",
    prompts=[
        "First prompt...",
        "Second prompt using {{output[-1]}}...",
        "Third prompt using {{artifact:other_topic:step}}"
    ]
)
```

### 3. Synthesize Steps

Analyze multiple artifacts:

```python
ChainStep(
    name="Find patterns",
    step_type="synthesize",
    artifact_pattern="*:components",  # All components
    topic="synthesis"
)
```

The synthesize step automatically:
- Queries artifacts matching the pattern
- Builds a prompt referencing all of them
- Extracts emergent patterns

## Composition Results

```python
result = composer.compose(steps)

# What you get:
result.steps_executed       # List of what happened
result.final_artifacts      # All artifacts created
result.execution_trace      # Detailed trace
result.total_tokens         # Token usage
result.visualize()          # Pretty summary
```

## Advanced: Creating Your Own Recipes

```python
class ChainRecipe:
    @staticmethod
    def my_custom_recipe(param1, param2):
        """Your recipe description."""
        return [
            ChainStep(...),
            ChainStep(...),
            ChainStep(...)
        ]

# Then use it:
steps = ChainRecipe.my_custom_recipe("foo", "bar")
result = composer.compose(steps)
```

## Examples

### Example 1: Quick Comparison

```bash
python -c "
from chain_composer import quick_compose
result = quick_compose('concept_comparison', topic_a='Lists', topic_b='Dictionaries')
"
```

### Example 2: Build Curriculum

```bash
python demos/curriculum_builder_demo.py
# Choose option 1
```

### Example 3: Progressive Depth

```bash
python -c "
from chain_composer import ChainRecipe, ChainComposer
composer = ChainComposer()
steps = ChainRecipe.progressive_depth('Recursion')
result = composer.compose(steps)
"
```

### Example 4: Custom Workflow

```python
from chain_composer import ChainComposer, ChainStep

composer = ChainComposer()

# Build a "concept evolution" workflow
steps = [
    # Historical analysis
    ChainStep(
        name="Historical context",
        step_type="chain",
        topic="evolution_history",
        prompts=["How has our understanding of {{topic}} evolved?"]
    ),

    # Current understanding
    ChainStep(
        name="Current state",
        step_type="tool",
        tool_name="concept_simplifier",
        tool_args={"topic": "Machine Learning"}
    ),

    # Future predictions
    ChainStep(
        name="Future trajectory",
        step_type="chain",
        topic="evolution_future",
        prompts=[
            """Based on:
History: {{artifact:evolution_history:step_1}}
Current: {{artifact:machine_learning:expert_educator}}

Where is this field heading?"""
        ]
    )
]

result = composer.compose(steps)
```

## Philosophy

**Before Chain Composer:**
- Tools run in isolation
- Results disappear
- Manual orchestration

**After Chain Composer:**
- Tools compose automatically
- Results accumulate
- Recipes encode workflows

This is **meta-level prompt engineering**:
- Not just chaining prompts
- Not just reusing artifacts
- **Orchestrating tools that orchestrate prompts that create artifacts**

Layers of abstraction:
1. **Prompts** - individual questions
2. **Chains** - sequences of prompts
3. **Tools** - reusable chains
4. **Compositions** - orchestrations of tools
5. **Recipes** - reusable compositions

You're now at **layer 5**.

## What's Next

### Weekend
- Run the demos
- Build your own recipes
- Experiment with compositions

### Next Week
- **Meta-chain generator** (the chain that designs chains)
- **Composition optimizer** (find optimal step ordering)
- **Web UI integration** (visualize compositions)

---

**You can now orchestrate complexity at scale.**

The foundation is complete. Every chain run adds to your knowledge base. Every composition creates new insights. The system grows smarter with use.

Welcome to meta-level AI orchestration.
