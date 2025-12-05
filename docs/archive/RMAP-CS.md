# 🧠 Cognitive Exoskeleton Roadmap

> **From playground to prosthetic** - Building tools that amplify output while conserving cognitive energy

**Mission**: Transform this framework into a production engine that serves three core needs:
1. **Content creation** for ryanleej.com (deep, evergreen, useful)
2. **Health sovereignty** (managing MS with data and clear reasoning)
3. **Cognitive leverage** (reducing executive function load)

---

## Design Principles

### 1. Energy Conservation First
- **No cognitive tax**: Tools should require less mental energy than doing it manually
- **Sensible defaults**: Should work without configuration
- **Resume-ability**: Save progress, pick up where you left off
- **Graceful degradation**: If the AI fails, still get partial value

### 2. Context Awareness
- **User profile**: Load personal context (writing style, health history, preferences)
- **Project memory**: Remember previous outputs to avoid repetition
- **Learning**: Adapt to feedback over time

### 3. Production Quality
- **CLI-first**: Pipe text in, get text out
- **Fast**: No unnecessary API calls
- **Reliable**: Handle failures gracefully
- **Observable**: Know what it's doing and why

---

## Phase 1: The Content Engine (Weeks 1-2)

### 🎯 Goal: Ship 2x more useful content with 50% less cognitive load

### Tool 1: Evergreen Guide Architect ✅ Priority 1
**Source**: Refactor `demos/viral_hook_laboratory`
**Path**: `tools/evergreen_guide.py`

**What it does**:
```bash
# Start from a topic
python tools/evergreen_guide.py "Progressive overload for MS patients"

# Or from existing notes
cat notes/training-thoughts.md | python tools/evergreen_guide.py
```

**Chain Design**:
```
1. Topic Analysis
   Input: Topic or rough notes
   Output: {
     "user_intent": "What problems are they trying to solve?",
     "search_patterns": ["search query 1", "query 2"],
     "pain_points": ["I don't know where to start", "Afraid of injury"]
   }

2. Competition Steel-Man
   Input: Topic + User Intent
   Output: {
     "existing_content_gaps": ["Most guides ignore fatigue management"],
     "what_they_do_well": ["Clear progression steps"],
     "differentiation_angle": "Focus on energy management and adaptation"
   }

3. Structure Generation
   Input: All previous outputs
   Output: {
     "outline": {
       "sections": [...],
       "key_metaphors": ["Progressive overload as a ramp, not stairs"],
       "research_needed": ["Fatigue studies in MS", "Detraining rates"]
     },
     "skimmability_score": 8.5,
     "evergreen_score": 9.0
   }

4. The Evergreen Audit
   Input: Outline
   Output: {
     "time_sensitive_claims": ["flagged for review"],
     "universal_principles": ["highlighted for emphasis"],
     "update_triggers": ["When new MS treatment options emerge"]
   }
```

**Output Format**: Markdown outline ready for writing

**Success Metric**: Can generate a useful outline in < 2 minutes

---

### Tool 2: Analogy Engine ✅ Priority 2
**Source**: Refactor `demos/concept_simplifier`
**Path**: `tools/analogy_engine.py`

**What it does**:
```bash
# Generate metaphors for complex concepts
python tools/analogy_engine.py "How oligoclonal bands indicate MS"
```

**Chain Design**:
```
1. Identify Abstraction Layer
   Input: Technical concept
   Output: "Core mechanism: Pattern recognition in immune response"

2. Generate 5 Distinct Metaphors
   - Biological: "Like finding the same graffiti tag at multiple crime scenes"
   - Mechanical: "Factory producing defective products in batches"
   - Software: "Same bug appearing across multiple test runs"
   - Everyday: "Recognizing your neighbor's handwriting on different notes"
   - Visual: "Unique fingerprints showing up in multiple places"

3. Stress Test Each Metaphor
   Input: Metaphors
   Output: {
     "accuracy_score": 8/10,
     "potential_confusion": "Factory metaphor might imply intentional production",
     "best_for_audience": "Software metaphor for technical readers"
   }
```

**Output**: Ranked metaphors with usage guidance

---

### Tool 3: Content Repurposer ✅ Priority 3
**Path**: `tools/content_repurposer.py`

**What it does**:
```bash
# Turn one guide into multiple formats
python tools/content_repurposer.py guides/progressive-overload.md
```

**Output Structure**:
```
output/
├── newsletter_segment.md       # 200-300 words, conversational
├── linkedin_post.md           # Professional, 150 words
├── twitter_thread.txt         # 5-7 tweets
├── personal_reflection.md     # Raw, vulnerable, 100 words
└── talking_points.md         # For podcasts/conversations
```

**Chain Design**:
```
1. Extract Core Insights
   Output: ["Key point 1", "Key point 2", "Key point 3"]

2. Adapt to Format
   For each format:
   - Match tone (newsletter: conversational, LinkedIn: professional)
   - Match length
   - Match platform norms

3. Cross-Link
   Add "Read the full guide: [link]" where appropriate
```

---

## Phase 2: Health Sovereignty & Research (Weeks 3-4)

### 🎯 Goal: Make better health decisions with less mental overhead

### Tool 4: Medical Consensus Parser ✅ Priority 1
**Source**: Refactor `demos/media_bias_triangulator`
**Path**: `tools/medical_consensus.py`

**What it does**:
```bash
# Parse a new study or health claim
python tools/medical_consensus.py --url "https://study-link.com"
# Or from text
cat clipboard.txt | python tools/medical_consensus.py
```

**Chain Design**:
```
1. The Skeptic's View
   Output: {
     "sample_size": 45,
     "sample_size_adequate": false,
     "funding_source": "Supplement company",
     "conflicts_of_interest": ["Authors have patents on compound"],
     "limitations": ["Short duration", "Self-reported outcomes"],
     "p_hacking_risk": "Medium"
   }

2. The Believer's View
   Output: {
     "mechanism_of_action": "Anti-inflammatory via COX-2 pathway",
     "mechanism_plausible": true,
     "anecdotal_support": "Strong community reports",
     "biological_rationale": "Well-understood pathway",
     "potential_magnitude": "Moderate effect size"
   }

3. The Synthesis
   Output: {
     "confidence_level": "Low-Medium",
     "safe_bet_interpretation": "Plausible mechanism, weak evidence",
     "action_recommendation": "Consider if other interventions have failed",
     "monitoring_needed": ["Track baseline", "Watch for side effects"],
     "decision_framework": {
       "try_if": ["Low cost", "Low risk", "Other options exhausted"],
       "skip_if": ["High cost", "Known interactions", "Better options available"]
     }
   }
```

**Output**: Risk-adjusted summary saved to `health/research/[topic].md`

---

### Tool 5: Symptom Correlator ✅ Priority 2
**Source**: Refactor `demos/historical_what_if_machine`
**Path**: `tools/symptom_correlator.py`

**What it does**:
```bash
# Analyze your health logs
python tools/symptom_correlator.py health/logs/2024-12.json
```

**Expected Input Format** (`health/logs/2024-12.json`):
```json
{
  "entries": [
    {
      "date": "2024-12-01",
      "sleep_hours": 7.5,
      "sleep_quality": 8,
      "energy_level": 7,
      "brain_fog": 2,
      "diet_notes": "High protein, avoided sugar",
      "stress_level": 4,
      "exercise": "20min walk",
      "symptoms": []
    }
  ]
}
```

**Chain Design**:
```
1. Pattern Recognition
   Input: 30 days of logs
   Output: {
     "strong_correlations": [
       {
         "factor": "sleep < 7 hours",
         "symptom": "brain fog next day",
         "correlation": 0.82,
         "lag": "1 day"
       }
     ],
     "weak_signals": [...],
     "noise": [...]
   }

2. Propose Experiments
   Output: {
     "experiment_1": {
       "hypothesis": "Increasing sleep to 8 hours reduces brain fog",
       "test_protocol": "2 weeks of 8+ hour sleep",
       "metrics_to_track": ["Brain fog score", "Energy level"],
       "expected_change": "20-30% reduction in fog days"
     }
   }

3. Risk Assessment
   For each experiment:
   - "What if it doesn't work?" (Cost of trying)
   - "What if it does work?" (Benefit)
   - "What's the worst case?" (Safety check)
```

**Output**: Experiment proposals saved to `health/experiments/[date].md`

---

### Tool 6: Protocol Decision Matrix ✅ Priority 3
**Path**: `tools/protocol_decision.py`

**What it does**:
```bash
# Evaluate a new intervention
python tools/protocol_decision.py "Low-dose naltrexone for MS"
```

**Chain Design**:
```
1. Cost/Benefit Analysis
   Output: {
     "financial_cost": "$30-50/month",
     "time_cost": "Daily pill, minimal",
     "cognitive_load": "Low (once daily)",
     "potential_benefit": "20-40% report symptom improvement",
     "timeline_to_effect": "2-3 months"
   }

2. Second-Order Effects Check
   Output: {
     "known_side_effects": ["Sleep disturbance (10%)", "Vivid dreams (15%)"],
     "interaction_risks": ["None with current meds"],
     "monitoring_needed": ["Sleep quality", "Dream intensity"],
     "reversibility": "High (stop anytime)"
   }

3. Implementation Friction Score
   Output: {
     "friction_score": 2/10,
     "friction_sources": ["Need to remember daily pill"],
     "mitigation_strategies": ["Set phone reminder", "Use pill organizer"],
     "sustainability": "High - simple protocol"
   }

4. Decision Recommendation
   Output: {
     "recommendation": "Worth trying",
     "reasoning": "Low risk, moderate potential, minimal friction",
     "trial_duration": "3 months",
     "success_criteria": ["Reduced fatigue", "Better cognitive clarity"],
     "stop_criteria": ["Sleep disruption", "No benefit after 3 months"]
   }
```

**Output**: Decision document saved to `health/protocols/[intervention].md`

---

## Phase 3: Professional & Cognitive Leverage (Weeks 5-6)

### 🎯 Goal: Reduce executive function load by 40%

### Tool 7: Advocacy Prep ✅ Priority 1
**Source**: Refactor `demos/negotiation_strategy_builder`
**Path**: `tools/advocacy_prep.py`

**What it does**:
```bash
# Prepare for important conversations
python tools/advocacy_prep.py "Doctor appointment - requesting MRI"
```

**Chain Design**:
```
1. Goal Definition
   Output: {
     "primary_goal": "Get MRI approved",
     "fallback_goals": ["Schedule follow-up", "Get symptom validation"],
     "must_avoid": ["Being dismissed", "Leaving without clear next step"]
   }

2. Anticipate Objections
   Output: {
     "likely_objections": [
       "Too soon since last MRI",
       "Symptoms could be stress",
       "Insurance won't cover"
     ],
     "responses": {
       "too_soon": "New symptom onset (date), different from previous pattern",
       "stress": "Tracked symptoms for 6 weeks, pattern is consistent"
     }
   }

3. Script "Polite Persistence"
   Output: {
     "opening": "I appreciate your time. I've been tracking new symptoms...",
     "escalation_phrases": [
       "I understand your concern, and I'd like to share why this feels different...",
       "What would need to be true for you to approve the MRI?",
       "Can we document my request in case symptoms worsen?"
     ],
     "closing": "What are our next steps if symptoms continue?"
   }

4. Must-Have Outcomes
   Output: {
     "minimum_success": "Documented symptom discussion + follow-up scheduled",
     "ideal_success": "MRI ordered",
     "walk_away_trigger": "If doctor dismisses without examination"
   }
```

**Output**: Conversation guide saved to `prep/[appointment-type]-[date].md`

---

### Tool 8: Blocker Breaker ✅ Priority 2
**Source**: Refactor `demos/problem_solution_spider`
**Path**: `tools/blocker_breaker.py`

**What it does**:
```bash
# When you feel stuck
python tools/blocker_breaker.py
# Prompts you through questions, then generates strategies
```

**Interactive Prompts**:
```
1. "Describe the stuck feeling in one sentence"
   → "I know I should write this guide, but I keep opening tabs instead"

2. "What's the smallest atomic blocker?"
   → "I don't have a clear outline"

3. "What would success look like in the next 2 hours?"
   → "A solid outline that I actually believe in"
```

**Chain Design**:
```
1. Decompose the Stuckness
   Input: Your answers above
   Output: {
     "root_cause": "Decision paralysis on structure",
     "surface_behavior": "Procrastination via research",
     "emotional_component": "Perfectionism + fear of wasted effort"
   }

2. Three Unblocking Strategies
   Output: {
     "the_easy_way": {
       "action": "Use existing outline from similar guide",
       "time": "15 minutes",
       "energy": "Low",
       "drawback": "Might not be perfect fit"
     },
     "the_money_way": {
       "action": "Pay editor to create outline from your notes",
       "cost": "$50-100",
       "time": "24 hours",
       "drawback": "Dependency, cost"
     },
     "the_nuclear_way": {
       "action": "Publish messy outline publicly, commit to deadline",
       "time": "30 minutes + social pressure",
       "energy": "High upfront, reduces ongoing friction",
       "drawback": "Public commitment risk"
     }
   }

3. Recommendation
   Output: "Try the Easy Way first (15 min). If still stuck, go Nuclear."
```

**Output**: Action plan saved to `blockers/[date]-[project].md`

---

## Phase 4: Technical Infrastructure (Week 7)

### Reorganization

```bash
# Current structure
promptchaining-for-5th-graders/
├── demos/              # Educational, keep for learning
├── chain.py           # Core framework
└── main.py            # Model setup

# New structure
promptchaining-for-5th-graders/
├── demos/              # Keep for learning/examples
├── tools/              # Production utilities ✅ NEW
│   ├── content/       # Content creation tools
│   ├── health/        # Health sovereignty tools
│   └── cognitive/     # Cognitive support tools
├── context/           # Personal context ✅ NEW
│   ├── user_profile.json
│   ├── writing_style.json
│   └── health_history.json
├── output/            # Tool outputs ✅ NEW
│   ├── guides/
│   ├── health/
│   └── prep/
├── core/              # Framework (renamed from root)
│   ├── chain.py
│   ├── models.py
│   └── config.py
└── cli/               # Command-line interface ✅ NEW
    └── toolbox.py     # Unified CLI
```

### User Profile Context

**File**: `context/user_profile.json`

```json
{
  "identity": {
    "name": "Ryan Johnson",
    "site": "ryanleej.com",
    "focus": "Health optimization, MS management, systems thinking"
  },
  "writing_style": {
    "tone": "Direct, practical, evidence-based",
    "avoid": ["Hype", "Unsubstantiated claims", "Medical advice"],
    "prefer": ["Personal experience", "Data", "Clear reasoning"],
    "metaphor_style": "Software and systems analogies",
    "reading_level": "Educated general audience"
  },
  "health_context": {
    "condition": "Multiple Sclerosis",
    "priorities": ["Energy management", "Cognitive clarity", "Long-term trajectory"],
    "sensitivities": ["Fatigue from heat", "Cognitive load", "Decision fatigue"],
    "current_protocols": ["Listed in protocols/current.md"]
  },
  "constraints": {
    "cognitive_budget": "Limited executive function - tools must be effortless",
    "time_budget": "Batch work in high-energy windows",
    "risk_tolerance": "Medium - willing to experiment with low-risk interventions"
  }
}
```

### CLI Integration

**File**: `cli/toolbox.py`

```python
#!/usr/bin/env python3
"""
Unified CLI for all cognitive exoskeleton tools
"""

import click
from tools.content import evergreen_guide, analogy_engine, content_repurposer
from tools.health import medical_consensus, symptom_correlator, protocol_decision
from tools.cognitive import advocacy_prep, blocker_breaker

@click.group()
def cli():
    """🧠 Cognitive Exoskeleton - Tools that amplify your output"""
    pass

# Content tools
@cli.command()
@click.argument('topic')
def guide(topic):
    """Generate evergreen guide outline"""
    evergreen_guide.run(topic)

@cli.command()
@click.argument('concept')
def metaphor(concept):
    """Generate metaphors for complex concepts"""
    analogy_engine.run(concept)

# Health tools
@cli.command()
@click.option('--url', help='Study URL')
@click.option('--text', help='Study text')
def research(url, text):
    """Parse medical research with skepticism and synthesis"""
    medical_consensus.run(url or text)

@cli.command()
@click.argument('log_file')
def correlate(log_file):
    """Find patterns in health logs"""
    symptom_correlator.run(log_file)

# Cognitive tools
@cli.command()
@click.argument('situation')
def prep(situation):
    """Prepare for important conversations"""
    advocacy_prep.run(situation)

@cli.command()
def unblock():
    """Break through when feeling stuck"""
    blocker_breaker.run()

if __name__ == '__main__':
    cli()
```

**Usage**:
```bash
# Install as command
pip install -e .

# Use anywhere
toolbox guide "Progressive overload for MS"
toolbox research --url "https://study-link.com"
toolbox unblock
```

---

## Success Metrics

### Content Engine
- ✅ **Speed**: Guide outline in < 2 minutes
- ✅ **Quality**: Published guides get > 100 reads/month
- ✅ **Volume**: 2x content output (4 guides/month → 8 guides/month)
- ✅ **Energy**: 50% less cognitive load (self-reported)

### Health Sovereignty
- ✅ **Confidence**: Make protocol decisions in < 30 minutes
- ✅ **Signal**: Identify 1-2 meaningful correlations per quarter
- ✅ **Outcomes**: Measurable improvement in tracked metrics
- ✅ **Safety**: Zero adverse events from rushed decisions

### Cognitive Leverage
- ✅ **Prep time**: Doctor/business prep in < 15 minutes
- ✅ **Unblocking**: Resume work within 30 minutes of feeling stuck
- ✅ **Meetings**: 90%+ achieve primary goal (vs 60% baseline)
- ✅ **Decision quality**: Reduce decision regret by 50%

---

## Implementation Philosophy

### Start Small, Compound Value
```
Week 1: One tool working (Evergreen Guide)
Week 2: Use it 3x, refine based on feedback
Week 3: Add second tool, but keep using first
Week 4: Now you have 2 tools in rotation
```

### Optimize for "Would I Use This Today?"
If a tool requires 10 minutes of configuration, you won't use it on a low-energy day. Every tool must be:
- **Zero-config** to start
- **Context-aware** (loads user profile automatically)
- **Resumable** (save state if interrupted)
- **Fast** (< 3 minutes for 80% of use cases)

### Measure Energy ROI
For each tool, track:
- **Energy in**: Cognitive load to use
- **Energy out**: Value generated
- **Net**: Out - In (must be positive)

If a tool has negative energy ROI, it's not a tool - it's a burden.

---

## Next Session: Build Tool #1

**Goal**: Ship `tools/evergreen_guide.py` and test it on one real topic

**Checklist**:
- [ ] Copy `demos/viral_hook_laboratory` → `tools/evergreen_guide.py`
- [ ] Modify prompts to focus on depth, utility, longevity
- [ ] Add CLI argument handling (`argparse`)
- [ ] Test on: "Progressive overload for MS patients"
- [ ] Refine based on output quality
- [ ] Document usage in `tools/README.md`
- [ ] Create `context/user_profile.json` with your preferences

**Time Budget**: 2 hours max

---

## Long-Term Vision (6 Months)

**The Cognitive Exoskeleton in Practice**:

```bash
# Morning routine
$ toolbox correlate health/logs/2024-12.json
→ "Strong signal: Sleep < 7hrs → Brain fog (0.82 correlation)"
→ Generates experiment proposal

# Content creation
$ toolbox guide "Symptom tracking for chronic illness"
→ Full outline in 90 seconds
→ Ready to write

# Research review
$ cat new-study.txt | toolbox research
→ Risk-adjusted summary
→ Action recommendation

# Before important meeting
$ toolbox prep "Neurologist appointment - discussing new symptom"
→ Conversation script
→ Objection responses
→ Must-have outcomes

# When stuck
$ toolbox unblock
→ "Try the easy way: Use outline from last guide"
→ Back to work in 10 minutes
```

**Impact**:
- **Content**: 8 high-quality guides/month, minimal stress
- **Health**: Clear decision framework, tracked experiments, measurable progress
- **Cognitive**: Spend energy on creation, not overhead

**The North Star**:
Tools that feel like extensions of your mind, not external systems you have to manage.

---

## Notes for Future Self

**On Bad Days**:
- These tools should work especially well when you're at 50% capacity
- If you can't use a tool on a bad day, it needs redesign
- "Good enough" output at low energy > perfect output that requires peak energy

**On Tool Abandonment**:
- If you stop using a tool after 2 weeks, it failed
- Better to have 3 great tools than 10 mediocre ones
- Delete ruthlessly, keep only what compounds

**On Evolution**:
- Tools will change as your needs change
- That's fine - they're prosthetics, not monuments
- Focus on energy ROI, always

---

**From learning project to life infrastructure.**
**From curiosity to capability.**
**From playground to prosthetic.**
