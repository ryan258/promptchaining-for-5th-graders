## Framework Enhancements

**Three powerful additions that extend the prompt chaining framework's capabilities**

This document describes three major enhancements to the prompt chaining framework that unlock new reasoning capabilities and provide scientific validation.

---

## Table of Contents

1. [Natural Reasoning Patterns](#natural-reasoning-patterns)
2. [Adversarial Chains](#adversarial-chains)
3. [Emergence Measurement](#emergence-measurement)
4. [Quick Start Guide](#quick-start-guide)
5. [Use Cases & Examples](#use-cases--examples)

---

## Natural Reasoning Patterns

**Module:** `natural_reasoning.py`
**Purpose:** Formalize expert reasoning patterns as reusable chain templates

### What It Does

Implements 5 classic reasoning patterns that experts use:

#### 1. Scientific Method
Tests hypotheses through observation, prediction, experimentation, analysis, and conclusion.

```python
from natural_reasoning import scientific_method

result, metadata = scientific_method(
    hypothesis="Regular exercise improves MS fatigue management",
    context="MS patients often experience chronic fatigue",
    evidence_sources=[
        "Studies show exercise improves mitochondrial function",
        "MS patients report exercise intolerance"
    ]
)

# Returns structured analysis through scientific lens
print(result['conclusion']['verdict'])  # "Supported" / "Refuted" / "Inconclusive"
```

#### 2. Socratic Dialogue
Examines beliefs through systematic questioning to uncover assumptions and contradictions.

```python
from natural_reasoning import socratic_dialogue

dialogue, metadata = socratic_dialogue(
    belief="People with MS should always use high-efficacy DMTs",
    teacher_persona="Neurologist",
    depth=5  # 5 rounds of questioning
)

# Returns dialogue with refined understanding
print(dialogue['synthesis']['refined_belief'])
print(dialogue['synthesis']['key_insights'])
```

#### 3. Design Thinking
Human-centered problem solving: Empathize → Define → Ideate → Prototype → Test.

```python
from natural_reasoning import design_thinking

solution, metadata = design_thinking(
    problem="MS patients struggle to track daily symptoms",
    target_user="Person with MS experiencing brain fog",
    constraints=["Low energy", "Cognitive limitations"]
)

# Returns full design process
print(solution['prototype']['how_it_works'])
print(solution['test']['overall_assessment'])
```

#### 4. Judicial Reasoning
Analyzes cases using facts, principles, precedent, and balanced judgment.

```python
from natural_reasoning import judicial_reasoning

judgment, metadata = judicial_reasoning(
    case="Should employers accommodate MS-related fatigue?",
    relevant_principles=["ADA", "Reasonable accommodation"],
    precedents=["Flexible schedules have been upheld"]
)

# Returns structured legal/ethical analysis
print(judgment['ruling']['ruling'])
print(judgment['ruling']['core_reasoning'])
```

#### 5. Root Cause Analysis (5 Whys)
Digs beneath surface symptoms to find systemic root causes.

```python
from natural_reasoning import five_whys

analysis, metadata = five_whys(
    problem="I missed my medication dose today",
    depth=5,
    context="Person with MS taking daily DMT"
)

# Returns causal chain and systemic solutions
print(analysis['synthesis']['root_cause'])
print(analysis['synthesis']['systemic_solutions'])
```

### Why It Matters

- **Pedagogical value** - Teaches how experts think about problems
- **Reusable templates** - Apply proven patterns to any domain
- **Intellectual depth** - Connects framework to centuries of human reasoning
- **Blog content** - Generate "How experts think about X" articles

### Demo

```bash
python demos/natural_reasoning_demo.py

# Or run specific pattern:
python demos/natural_reasoning_demo.py --demo 1  # Scientific method
python demos/natural_reasoning_demo.py --demo 2  # Socratic dialogue
# ... etc
```

---

## Adversarial Chains

**Module:** `adversarial_chains.py`
**Purpose:** Use conflict and opposition to reveal truth through dialectical reasoning

### What It Does

Implements 3 adversarial patterns impossible with single prompts:

#### 1. Red Team vs Blue Team
One side attacks a position, the other defends, a judge evaluates.

```python
from adversarial_chains import red_vs_blue

debate, metadata = red_vs_blue(
    topic="MS treatment strategies",
    position_to_defend="MS patients should start high-efficacy DMTs immediately",
    rounds=3,
    judge_criteria=["Evidence strength", "Logic", "Patient welfare"]
)

# Returns full debate with judgment
print(f"Winner: {metadata['winner']}")
print(f"Blue score: {metadata['blue_score']}/10")
print(f"Red score: {metadata['red_score']}/10")
print(debate['judgment']['verdict'])
```

**Use when:**
- Testing ideas through adversarial pressure
- Finding weaknesses before implementation
- Red-teaming strategies or policies
- Exploring controversial topics

#### 2. Dialectical Synthesis
Hegelian dialectic: Thesis → Antithesis → Synthesis.

```python
from adversarial_chains import dialectical

result, metadata = dialectical(
    thesis="MS patients should prioritize symptom management",
    context="Treatment approaches and quality of life",
    domain="Medical philosophy"
)

# Returns thesis, antithesis, synthesis, and evaluation
print(result['synthesis']['synthesis_statement'])  # The transcendent position
print(result['synthesis']['emergent_insight'])      # New understanding
print(result['evaluation']['verdict'])              # Quality assessment
```

**Use when:**
- Resolving apparent contradictions
- Transcending binary thinking
- Finding nuanced positions
- Philosophical exploration

#### 3. Adversarial Socratic Dialogue
Aggressive questioning to stress-test claims.

```python
from adversarial_chains import adversarial_socratic

dialogue, metadata = adversarial_socratic(
    claim="AI will solve the MS medication adherence problem",
    depth=4,
    aggressive=True
)

# Returns rigorous stress test
print(f"Claim survived: {metadata['survived']}")  # "Yes" / "Partially" / "No"
print(f"Credibility: {metadata['credibility_impact']}")  # "Increased" / "Decreased"
print(dialogue['verdict']['refined_claim'])
print(dialogue['verdict']['remaining_vulnerabilities'])
```

**Use when:**
- Rigorously testing beliefs
- Finding every weakness in an argument
- Intellectual honesty and rigor
- Preparing for real-world critique

### Why It Matters

- **Unique capability** - Impossible with single prompts, requires back-and-forth
- **Reveals weaknesses** - Adversarial pressure finds flaws
- **Nuanced understanding** - Dialectic transcends simple pro/con
- **Visually compelling** - Debates are engaging to read

### Demo

```bash
python demos/adversarial_chains_demo.py

# Or specific pattern:
python demos/adversarial_chains_demo.py --demo 1  # Red vs Blue
python demos/adversarial_chains_demo.py --demo 2  # Dialectical
python demos/adversarial_chains_demo.py --demo 3  # Adversarial Socratic
```

---

## Emergence Measurement

**Module:** `emergence_measurement.py`
**Purpose:** Scientifically prove chains unlock insights impossible from single prompts

### What It Does

Provides rigorous framework for validating that chains produce better results:

#### Single Comparison

Compare a chain approach vs mega-prompt baseline on one topic.

```python
from emergence_measurement import measure_emergence
from tools.learning.concept_simplifier import concept_simplifier

comparison, metadata = measure_emergence(
    topic="Neural Networks",
    chain_function=concept_simplifier
)

# Returns detailed comparison
print(f"Winner: {comparison['winner']}")  # "Chain" / "Baseline" / "Tie"
print(comparison['analysis'])

# Scores across 5 dimensions (each 1-10):
scores = comparison['scores']['scores']
print(scores['approach_a']['novelty'])      # Chain novelty score
print(scores['approach_b']['depth'])        # Baseline depth score
```

**Dimensions measured:**
- **Novelty** - Unique insights not obvious from topic
- **Depth** - Level of detail and sophistication
- **Coherence** - Logical flow and structure
- **Pedagogical** - Would a learner understand?
- **Actionability** - Can someone DO something with this?

#### Batch Measurement

Test across multiple topics for statistical significance.

```python
from emergence_measurement import batch_measure

aggregate, individual_results = batch_measure(
    topics=["Quantum Computing", "Photosynthesis", "Blockchain"],
    chain_function=concept_simplifier
)

# Statistical validation
print(aggregate['results']['chain_win_rate'])        # e.g., "73.3%"
print(aggregate['statistical_significance'])         # Confidence assessment
print(aggregate['average_scores'])                   # Averages across topics
print(aggregate['conclusion'])                       # Summary verdict
```

#### Report Generation

Create publishable markdown reports.

```python
from emergence_measurement import generate_report

report_path = generate_report(aggregate, individual_results)
# Creates detailed report at output/emergence_report.md
```

### Why It Matters

- **Scientific validation** - Hard data proving chains work
- **Evidence-based** - Not just intuition, actual measurements
- **Identify patterns** - Learn which dimensions chains excel at
- **Publishable** - Generate reports to share findings
- **Convince skeptics** - Data beats anecdotes

### Demo

```bash
python demos/emergence_measurement_demo.py

# Or specific demo:
python demos/emergence_measurement_demo.py --demo 1  # Understanding metrics
python demos/emergence_measurement_demo.py --demo 2  # Single comparison
python demos/emergence_measurement_demo.py --demo 3  # Quick test
python demos/emergence_measurement_demo.py --demo 4  # Batch measurement
```

---

## Quick Start Guide

### Installation

All enhancements are already included in the framework. No additional dependencies needed.

### Basic Usage

```python
# 1. Pick a reasoning pattern
from natural_reasoning import scientific_method

# 2. Run it on your topic
result, metadata = scientific_method(
    hypothesis="Your hypothesis here",
    context="Additional context"
)

# 3. Get structured insights
print(result['conclusion'])
```

### Testing Your Own Chains

```python
from emergence_measurement import quick_test

# Validate your chain produces better results
quick_test(
    topic="Test Topic",
    chain_function=your_chain_function
)
```

---

## Use Cases & Examples

### For Blog Content

**Natural Reasoning → "How Experts Think" Series**
```python
# Generate blog post on judicial reasoning for ethical dilemmas
from natural_reasoning import judicial_reasoning

result, _ = judicial_reasoning(
    case="Should insurance cover off-label MS treatments?",
    relevant_principles=["Beneficence", "Justice", "Autonomy"]
)

# Use result as blog content showing expert reasoning process
```

**Adversarial Chains → Debate Articles**
```python
# Create engaging pro/con debate content
from adversarial_chains import red_vs_blue

debate, _ = red_vs_blue(
    topic="Aggressive vs conservative MS treatment",
    position_to_defend="Aggressive treatment is better",
    rounds=3
)

# Format as blog post with back-and-forth arguments
```

### For Decision Making

**Design Thinking → Product/Service Design**
```python
from natural_reasoning import design_thinking

solution, _ = design_thinking(
    problem="Users can't find relevant content",
    target_user="MS patients with cognitive limitations",
    constraints=["Low tech literacy", "Brain fog"]
)

# Get user-centered solution design
```

**Dialectical → Resolving Trade-offs**
```python
from adversarial_chains import dialectical

synthesis, _ = dialectical(
    thesis="Prioritize feature development",
    domain="Product strategy"
)

# Get nuanced position that transcends false dichotomies
```

### For Research & Validation

**Emergence Measurement → Validate Your Chains**
```python
from emergence_measurement import batch_measure

# Prove your chain approach works
aggregate, _ = batch_measure(
    topics=["Topic 1", "Topic 2", "Topic 3", "Topic 4", "Topic 5"],
    chain_function=your_custom_chain
)

# Generate statistical evidence
generate_report(aggregate, individual_results)
```

**Scientific Method → Hypothesis Testing**
```python
from natural_reasoning import scientific_method

result, _ = scientific_method(
    hypothesis="Feature X will increase engagement",
    evidence_sources=["User research", "A/B test data"]
)

# Get rigorous evaluation
```

### For Education

**Socratic Dialogue → Teaching Tool**
```python
from natural_reasoning import socratic_dialogue

dialogue, _ = socratic_dialogue(
    belief="Student's misconception here",
    teacher_persona="Patient teacher",
    depth=5
)

# Guide student to correct understanding
```

**Root Cause Analysis → Problem Solving**
```python
from natural_reasoning import five_whys

analysis, _ = five_whys(
    problem="Students aren't completing homework",
    depth=5
)

# Find systemic root cause, not just symptoms
```

---

## Pattern Selection Guide

**When to use Natural Reasoning Patterns:**
- ✅ Teaching/learning scenarios
- ✅ Applying established expert methods
- ✅ Structured problem-solving
- ✅ Building understanding step-by-step

**When to use Adversarial Chains:**
- ✅ Testing ideas rigorously
- ✅ Controversial or complex topics
- ✅ Finding weaknesses in arguments
- ✅ Transcending binary thinking
- ✅ Red-teaming strategies

**When to use Emergence Measurement:**
- ✅ Validating your chain designs
- ✅ Comparing approaches scientifically
- ✅ Publishing research findings
- ✅ Convincing stakeholders with data

---

## Contributing New Patterns

Want to add your own reasoning pattern?

### For Natural Reasoning:
1. Follow the pattern in `natural_reasoning.py`
2. Create clear prompts for each step
3. Return structured dict + metadata
4. Add to `REASONING_PATTERNS` registry
5. Write a demo

### For Adversarial Patterns:
1. Follow the pattern in `adversarial_chains.py`
2. Ensure genuine back-and-forth dialectic
3. Include evaluation/judgment step
4. Add to `ADVERSARIAL_PATTERNS` registry
5. Write a demo

---

## Performance Notes

**Token Usage:**
- Natural Reasoning: 500-2000 tokens per pattern
- Adversarial Chains: 1000-3000 tokens (more rounds = more tokens)
- Emergence Measurement: 1500-4000 tokens per comparison

**Timing:**
- Single pattern: 10-30 seconds
- Batch measurement (5 topics): 3-8 minutes
- Full adversarial debate (3 rounds): 1-2 minutes

**Cost Estimates:**
- Pattern execution: $0.002-0.010 per run
- Emergence measurement: $0.005-0.020 per comparison
- Batch measurement (5 topics): $0.025-0.100

---

## Troubleshooting

**Q: Pattern returns incomplete results**
- Check that your API key is set correctly
- Ensure model supports JSON output
- Try increasing `max_tokens` in main.py

**Q: Emergence measurement shows "Tie" for everything**
- Try different topics (some topics don't benefit from chaining)
- Check baseline prompt is appropriate
- Increase number of topics for statistical power

**Q: Adversarial chains aren't adversarial enough**
- Set `aggressive=True` in adversarial_socratic
- Increase rounds in red_vs_blue
- Check the judge criteria are appropriate

---

## Next Steps

1. **Try the demos** - Run each demo to see patterns in action
2. **Pick a use case** - Choose the pattern that fits your need
3. **Customize** - Adjust prompts and parameters for your domain
4. **Measure** - Use emergence_measurement to validate results
5. **Share** - Generate reports and publish findings

---

## License

These enhancements are part of the prompt chaining framework and share the same license.

## Citation

If you use these patterns in research or publications:

```
Prompt Chaining Framework Enhancements (2024)
Natural Reasoning Patterns, Adversarial Chains, and Emergence Measurement
https://github.com/yourusername/promptchaining-for-5th-graders
```

---

**Questions? Issues? Contributions?**

Open an issue or PR on GitHub!
