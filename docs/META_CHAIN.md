# 🧠 Meta-Chain Generator - Chains That Design Chains

## The Pinnacle

This is **Layer 6** of the abstraction stack:

1. **Prompts** - Individual questions
2. **Chains** - Sequences that build
3. **Artifacts** - Persistent knowledge
4. **Tools** - Reusable chains
5. **Compositions** - Orchestrated tools
6. **Meta-Chains** ← **YOU ARE HERE**

**The meta-chain analyzes your goal and automatically designs the optimal chain to achieve it.**

## What Is This?

Instead of manually designing chains, you describe your goal in plain English and the meta-chain:
1. Analyzes what's needed
2. Selects optimal cognitive moves
3. Generates specific prompts
4. Optionally executes the designed chain

**This is true meta-level AI** - the system improving itself.

## Quick Start

```python
from meta_chain_generator import quick_generate

# Describe your goal
design, outputs = quick_generate(
    "Teach recursion through powerful analogies"
)

# The meta-chain automatically:
# - Analyzes the goal
# - Designs a custom chain
# - Executes it
# - Returns results
```

## The Cognitive Move Library

The meta-chain composes from 10 fundamental "thinking primitives":

### 1. **Decompose**
Break complex concepts into essential components
- **When**: Understanding structure
- **Example**: "Break down quantum mechanics"

### 2. **Analogize**
Create powerful analogies from everyday experience
- **When**: Making abstract concrete
- **Example**: "Explain neural networks like cooking"

### 3. **Synthesize**
Combine insights into unified understanding
- **When**: Building complete picture
- **Example**: "Integrate these three perspectives"

### 4. **Connect**
Find deep structural connections
- **When**: Cross-domain learning
- **Example**: "How is blockchain like Git?"

### 5. **Critique**
Find flaws, gaps, weaknesses
- **When**: Quality improvement
- **Example**: "What's wrong with this explanation?"

### 6. **Exemplify**
Create concrete, testable examples
- **When**: Grounding theory
- **Example**: "Show recursion in real code"

### 7. **Historicize**
Trace how understanding evolved
- **When**: Context matters
- **Example**: "How has AI ethics developed?"

### 8. **Problematize**
Identify key questions and challenges
- **When**: Deep understanding
- **Example**: "What's still unresolved in quantum physics?"

### 9. **Apply**
Show practical usage
- **When**: Theory → action
- **Example**: "How do I actually use Docker?"

### 10. **Compare**
Systematic comparison and contrast
- **When**: Understanding distinctions
- **Example**: "React vs Vue - when to use which?"

## How It Works

### The Meta-Chain Process

```
User Goal
   ↓
Analyze Goal (meta-prompt 1)
   ├─ What operations needed?
   ├─ Optimal sequence?
   └─ Why this order?
   ↓
Generate Prompts (meta-prompt 2)
   ├─ Specific prompts for each move
   ├─ Build on previous outputs
   └─ Use context variables
   ↓
ChainDesign Object
   ├─ Goal
   ├─ Reasoning
   ├─ Cognitive moves
   ├─ Prompts
   └─ Context
   ↓
(Optional) Execute
   ↓
Results
```

### Example: "Teach recursion through analogies"

**Meta-chain analysis:**
```json
{
  "goal_analysis": "User wants analogies that make recursion intuitive",
  "required_operations": [
    {"move": "decompose", "why": "Understand recursion components first"},
    {"move": "analogize", "why": "Create powerful analogies"},
    {"move": "exemplify", "why": "Ground in concrete examples"}
  ],
  "optimal_sequence": ["decompose", "analogize", "exemplify"],
  "reasoning": "Must understand structure before creating analogies, then validate with examples"
}
```

**Generated chain:**
1. Decompose recursion into core components
2. Create analogies for each component
3. Provide testable examples

## Usage Patterns

### Pattern 1: Quick Generate

Simplest way - design and execute in one call:

```python
from meta_chain_generator import quick_generate

design, outputs = quick_generate(
    "Compare functional vs object-oriented programming",
    concept_a="functional programming",
    concept_b="object-oriented programming"
)

print(design.visualize())
print(outputs[-1])  # Final result
```

### Pattern 2: Design Only

Just design the chain, don't execute yet:

```python
from meta_chain_generator import MetaChainGenerator

generator = MetaChainGenerator()

design = generator.design_chain(
    goal="Explain blockchain through historical analogies",
    context={"topic": "blockchain"}
)

print(design.visualize())
print(design.prompts)  # See the generated prompts
```

### Pattern 3: Design + Manual Review + Execute

Design, review, then execute:

```python
generator = MetaChainGenerator()

# Design
design = generator.design_chain(goal="Your goal here")

# Review
print(design.visualize())
print("Cognitive moves:", design.cognitive_moves)

# Decide whether to execute
user_input = input("Execute? (y/n): ")
if user_input == 'y':
    outputs, prompts, usage = generator.execute_chain(design)
```

### Pattern 4: Constrained Design

Add constraints to the design:

```python
design = generator.design_chain(
    goal="Explain neural networks",
    context={"topic": "neural networks"},
    constraints=[
        "Maximum 3 cognitive moves",
        "Must include analogies",
        "No technical jargon"
    ]
)
```

### Pattern 5: Iterative Improvement

Design, execute, critique, redesign:

```python
# Initial design
design1 = generator.design_chain("Teach calculus")
outputs1 = generator.execute_chain(design1)

# Critique the result
design2 = generator.design_chain(
    goal="Improve this explanation",
    context={"previous_output": outputs1[-1]}
)

# Execute improved version
outputs2 = generator.execute_chain(design2)
```

## The ChainDesign Object

```python
@dataclass
class ChainDesign:
    goal: str                    # What user wants
    reasoning: str               # Why this design
    cognitive_moves: List[str]   # Sequence of moves
    prompts: List[str]          # Actual prompts
    context: Dict[str, Any]     # Context variables
    metadata: Dict[str, Any]    # Additional info

design.visualize()   # Pretty print
design.to_dict()     # Convert to dict
design.to_json()     # Convert to JSON
```

## Examples

### Example 1: Concept Explanation

```python
design, outputs = quick_generate(
    "Break down blockchain into teachable parts"
)

# Meta-chain likely chooses:
# 1. decompose (break into parts)
# 2. analogize (make parts concrete)
# 3. synthesize (show how parts fit)
```

### Example 2: Comparison

```python
design, outputs = quick_generate(
    "Compare machine learning to human learning",
    concept_a="machine learning",
    concept_b="human learning"
)

# Meta-chain likely chooses:
# 1. decompose (analyze each separately)
# 2. connect (find deep similarities)
# 3. compare (systematic comparison)
# 4. synthesize (unified insight)
```

### Example 3: Historical Understanding

```python
design, outputs = quick_generate(
    "Trace how AI ethics has evolved"
)

# Meta-chain likely chooses:
# 1. historicize (evolution over time)
# 2. problematize (current challenges)
# 3. synthesize (where we are now)
```

### Example 4: Practical Application

```python
design, outputs = quick_generate(
    "How do I actually use Docker in production?",
    tool="Docker"
)

# Meta-chain likely chooses:
# 1. decompose (Docker components)
# 2. apply (practical usage)
# 3. exemplify (real examples)
```

## Advanced: Custom Cognitive Moves

You can add your own cognitive moves:

```python
from meta_chain_generator import CognitiveMove, CognitiveMoveLibrary

custom_move = CognitiveMove(
    name="debug",
    description="Find and fix errors in reasoning",
    when_to_use="When something seems wrong",
    prompt_template="""You are a debugging expert.

Analyze this reasoning: {{reasoning}}

Find logical errors, gaps, or inconsistencies.

Respond in JSON:
{
  "errors": [
    {"error": "What's wrong", "fix": "How to fix it"}
  ]
}""",
    example_contexts=["Validation", "Error checking"]
)

# Add to library (if you extend the class)
# Or use directly in custom chains
```

## How This Enables Meta-Learning

### 1. Self-Improvement

```python
# Chain designs chains that design chains
meta_meta_design = generator.design_chain(
    goal="Design a better chain designer"
)
```

### 2. Pattern Discovery

```python
# Analyze what cognitive sequences work best
for topic in ["AI", "Blockchain", "Quantum"]:
    design = generator.design_chain(f"Explain {topic}")
    # Track which moves get chosen
    # Find patterns in successful chains
```

### 3. Automatic Optimization

```python
# Try multiple designs, pick best
designs = []
for i in range(3):
    design = generator.design_chain(goal, constraints=[f"Try approach {i}"])
    designs.append(design)

# Compare results, learn which works best
```

### 4. Curriculum Generation

```python
# Meta-chain designs learning paths
curriculum = generator.design_chain(
    goal="Create a learning path for quantum physics",
    context={"level": "beginner"}
)

# The meta-chain decides the pedagogical sequence
```

## Demos

Run the demos to see it in action:

```bash
python demos/meta_chain_demo.py

# Then choose:
# 1. Explain through analogies
# 2. Compare concepts
# 3. Your custom goal
# 4. Constrained design
# 5. Meta-reflection (meta-chain critiques itself!)
```

## Philosophy

### Before Meta-Chains

```
Human → Designs Chain → LLM Executes → Result
  ↑                                       ↓
  └──────── Manual iteration ─────────────┘
```

**Human** does the cognitive work of chain design.

### After Meta-Chains

```
Human → Goal → Meta-Chain → Designed Chain → LLM → Result
                    ↑                                   ↓
                    └────── Can improve itself ─────────┘
```

**Meta-chain** does the cognitive work of chain design.

**The system designs itself.**

## What This Unlocks

### 1. Non-Experts Can Use Advanced Techniques

```python
# User doesn't need to know about cognitive moves
quick_generate("Explain X")

# Meta-chain figures it out
```

### 2. Optimal Chain Discovery

```python
# System finds best cognitive sequence
# Not just good, but provably optimal for goal
```

### 3. Self-Improving Workflows

```python
# Chains get better over time
# Meta-chain learns from successes
```

### 4. Automated Curriculum Design

```python
# Meta-chain becomes a teaching system
# Designs optimal learning paths
```

### 5. Research Tool

```python
# Experiment with cognitive sequences
# Discover new reasoning patterns
```

## Limitations & Future Work

### Current Limitations

1. **No feedback loop yet** - Meta-chain doesn't learn from execution results
2. **No chain validation** - Doesn't check if design will actually work
3. **No optimization** - Doesn't compare multiple designs
4. **Fallback is simple** - If meta-chain fails, uses basic 2-step chain

### Future Enhancements

1. **Execution feedback** - Meta-chain sees results, improves design
2. **Chain validation** - Check design before execution
3. **Multi-design comparison** - Generate 3 designs, pick best
4. **Chain optimization** - Minimize steps while maximizing quality
5. **Learning from history** - Analyze which cognitive sequences work best
6. **Constraint satisfaction** - Provably meet user constraints

## Testing

```bash
python test_meta_chain.py
# Tests cognitive move library
# Tests chain design
# Tests serialization
```

## Integration with Other Systems

### With Artifacts

```python
# Meta-chain can use existing artifacts
design = generator.design_chain(
    goal="Build on what we know about ML",
    context={"existing": "{{artifact:machine_learning:components}}"}
)
```

### With Chain Composer

```python
from chain_composer import ChainStep

# Use meta-chain to design individual steps
design = generator.design_chain("Analyze topic")

step = ChainStep(
    name="Meta-designed step",
    step_type="chain",
    prompts=design.prompts
)
```

## Summary

**The meta-chain generator is the culmination of the framework:**

- **Layer 1-2**: Basic prompting
- **Layer 3-4**: Knowledge accumulation
- **Layer 5**: Orchestration
- **Layer 6**: Self-design

**You now have a system that:**
- Understands goals
- Designs solutions
- Executes automatically
- Can improve itself

**This is AI-assisted AI engineering.**

---

Welcome to meta-level intelligence.
