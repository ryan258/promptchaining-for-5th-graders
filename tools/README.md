# 🧠 Cognitive Exoskeleton Tools

Production-ready tools that amplify cognitive output while conserving energy. All 33 tools use advanced prompt engineering with expert personas, structured frameworks, concrete examples, and well-defined constraints.

## Philosophy

These tools are designed for **low-energy usability**. If you can't use them on a bad day, they're not working.

### Design Principles

1. **Zero-config start**: Load user context automatically from `context/user_profile.json`
2. **CLI-first**: Accept input via args or stdin
3. **Fast**: < 3 minutes for 80% of use cases
4. **Energy ROI positive**: Value out > effort in
5. **Professional output**: Structured JSON + markdown with comprehensive analysis

---

## Tool Catalog

### 📚 Learning Tools

#### 🧭 Concept Simplifier
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

**Prompts:** Expert educator → analogy specialist → learning designer → technical writer

---

#### 🔗 Subject Connector
Find surprising links between two subjects, why they matter, and design a project that uses both.

**Usage:**
```bash
python tools/learning/subject_connector.py "Subject A" --context "Subject B"
```

**Output:** JSON in `output/learning/subject_connector/`
- Unexpected connections
- Why connections matter
- Project idea with expected outputs

---

### 🔬 Research Tools

#### 🕰️ Research Timeline (Knowledge Time Machine)
Generate comprehensive timelines: origins → evolution → current state → future trajectories.

**Usage:**
```bash
python tools/research/timeline.py "CRISPR gene editing"
cat notes/topic.md | python tools/research/timeline.py --context "Specific angle"
```

**Output:** Markdown in `output/research/timelines/`
- Historical origins with uncertainty notes
- Evolution points (breakthroughs and setbacks)
- Current SOTA (State of the Art) capabilities
- Research gaps and limitations
- Future scenarios and wildcards

**Prompts:** Research historian → science historian → field analyst → technology forecaster

**Energy Cost**: Low (2-3 minutes)
**Energy Return**: High (research prep shortcut)
**Net**: Strongly positive ✅

---

#### 🌌 Emergence Simulator
Analyze systems for emergent behaviors from simple agent interactions.

**Usage:**
```bash
python tools/research/emergence_simulator.py "System description"
```

**Output:** JSON in `output/research/emergence_simulator/`
- Agent types and interaction rules
- Emergent behaviors and mechanisms
- Validation experiments

---

### 🎨 Content Tools

#### 🌲 Evergreen Guide Architect
Transform topics or rough notes into structured, lasting guide outlines.

**Usage:**
```bash
python tools/content/evergreen_guide.py "Progressive overload for MS patients"
cat notes/training-thoughts.md | python tools/content/evergreen_guide.py
python tools/content/evergreen_guide.py "Topic" --context "Additional notes"
```

**Output:** Markdown in `output/guides/`
- User intent & pain point analysis
- Competition differentiation strategy
- Key metaphors and research citations
- Evergreen audit (timeless vs. timely elements)
- Quality metrics and writing priorities

**Prompts:** Content strategist → research analyst → metaphor specialist → quality auditor

**Energy Cost**: Low (2-3 minutes)
**Energy Return**: High (saves hours of outlining)
**Net**: Strongly positive ✅

---

### 💼 Career Tools

#### 🎯 Dream Job Reverse Engineer
Decode job postings into hidden priorities, manager pain points, and application strategy.

**Usage:**
```bash
python tools/career/dream_job_reverse_engineer.py "path/to/job.txt"
python tools/career/dream_job_reverse_engineer.py "Job text" --context "Your profile/angle"
```

**Output:** JSON in `output/career/dream_job_reverse_engineer/`
- Hidden priorities and culture vibe from language analysis
- Manager pain points (what broke, what's blocking them)
- Skills and proof-of-work mappings
- Resume bullets tailored to pain points
- STAR story outlines

**Prompts:** Recruiter → organizational psychologist → career strategist → storytelling coach

---

#### 🔎 Meeting Dynamics Forensics
Analyze meeting transcripts for interruptions, deference patterns, and the real power hierarchy.

**Usage:**
```bash
python tools/career/meeting_dynamics_forensics.py "Transcript text"
cat meeting.txt | python tools/career/meeting_dynamics_forensics.py
```

**Output:** JSON in `output/career/meeting_dynamics_forensics/`
- Interruption patterns (who interrupts whom)
- Deference markers (language, turn-taking)
- Inferred hierarchy vs. stated org chart
- Red flags and recommendations

---

#### 🎓 Credential Inflation Analyzer
Detect degree inflation and gatekeeping in job requirements.

**Usage:**
```bash
python tools/career/credential_inflation_analyzer.py "Job/role description"
```

**Output:** JSON in `output/career/credential_inflation_analyzer/`
- Inflation signals (why requirements are suspect)
- Skill-based substitutes and proofs
- Impacts and practical advice

---

### 🤝 Business Tools

#### 🤝 Negotiation Strategy Builder
Analyze leverage, BATNAs, set anchors, predict objections, and craft counter-scripts.

**Usage:**
```bash
python tools/business/negotiation_strategy_builder.py "Scenario description"
python tools/business/negotiation_strategy_builder.py "Scenario" --context "Role, constraints, numbers"
```

**Output:** JSON in `output/business/negotiation_strategy_builder/`
- Power analysis (leverage, BATNA strength)
- BATNA definition (yours and theirs)
- Opening anchor strategy with reasoning
- Predicted objections (3-4 sharp ones)
- Counter-scripts with fallback options
- Concession guardrails

**Prompts:** Negotiation strategist → BATNA analyst → anchoring expert → objection psychologist → persuasion expert

**Energy Cost**: Low
**Energy Return**: Very High (negotiation prep worth thousands)
**Net**: Extremely positive ✅

---

### 💻 Development Tools

#### 🏗️ Code Architecture Critic
Audit code for patterns/anti-patterns, smells, refactoring opportunities, and architecture improvements.

**Usage:**
```bash
python tools/dev/code_architecture_critic.py "path/to/file.py"
python tools/dev/code_architecture_critic.py "inline code" --context "constraints or goals"
```

**Output:** JSON in `output/dev/code_architecture_critic/`
- Patterns and anti-patterns
- Code smells with severity
- Refactoring roadmap
- Maintenance forecast (technical debt trajectory)
- Improved architecture sketch

---

### 🤝 Collaboration Tools

#### 🤝 Common Ground Finder
Map opposing views to shared values, concerns, and bridge options.

**Usage:**
```bash
python tools/collaboration/common_ground_finder.py "View A" --context "View B"
```

**Output:** JSON in `output/collaboration/common_ground_finder/`
- Core values from each side
- Shared concerns despite different solutions
- Common goals
- Bridge ideas (satisfies both)
- Conversation prompts

---

### 🧠 Brainstorming Tools

#### 🕷️ Problem–Solution Spider
Clarify problems, generate wild ideas, blend solutions, and design quick validation tests.

**Usage:**
```bash
python tools/brainstorm/problem_solution_spider.py "Problem statement"
python tools/brainstorm/problem_solution_spider.py "Problem" --context "Constraints/stakeholders"
```

**Output:** JSON in `output/brainstorm/problem_solution_spider/`
- Crisply defined problem with stakes
- Constraints and resources
- Wild ideas with feasibility
- Blended solution options
- Quick test scenario with success/failure signals

**Prompts:** Product manager → operations strategist → innovation consultant → systems architect → QA/experiment designer

---

### 📰 Media Literacy Tools

#### 🧹 Euphemism Decoder
Translate sanitized language into plain English and expose intent.

**Usage:**
```bash
python tools/media/euphemism_decoder.py "Quoted text"
cat speech.txt | python tools/media/euphemism_decoder.py
```

**Output:** JSON in `output/media/euphemism_decoder/`
- Euphemism mappings to plain English
- Full rewrite without spin
- Intent analysis and beneficiaries

---

#### 🧭 Media Bias Triangulator
Generate polarized framings, surface omissions, and synthesize ground truth.

**Usage:**
```bash
python tools/media/media_bias_triangulator.py "Event description"
cat event.txt | python tools/media/media_bias_triangulator.py
```

**Output:** JSON in `output/media/media_bias_triangulator/`
- Biased headlines (left and right framings)
- Omissions from each perspective
- Ground truth synthesis

---

#### 🌾 Astroturf Detector
Assess whether messaging shows signs of astroturfing or organic coordination.

**Usage:**
```bash
python tools/media/astroturf_detector.py "Thread/post text"
```

**Output:** JSON in `output/media/astroturf_detector/`
- Coordination signals
- Likely origin and motives
- Confidence assessment
- Verdict and monitoring guidance

---

#### 🧠 Consensus Manufacturing Detective
Spot framing, repetition, and omissions used to manufacture consensus.

**Usage:**
```bash
python tools/media/consensus_manufacturing_detective.py "Campaign text"
```

**Output:** JSON in `output/media/consensus_manufacturing_detective/`
- Framing techniques
- Key omissions
- Beneficiaries
- Counter-frames

---

#### 🛡️ Narrative Warfare Analyst
Analyze competing narratives, propaganda techniques, and escalation risks.

**Usage:**
```bash
python tools/media/narrative_warfare_analyst.py "Narrative summary or quotes"
```

**Output:** JSON in `output/media/narrative_warfare_analyst/`
- Competing narratives
- Techniques used
- Counter-narratives
- Monitoring signals for escalation

---

### 🧠 Psychology Tools

#### 🧭 Ideological Consistency Test
Surface contradictions between stated beliefs, derived implications, and likely behavior.

**Usage:**
```bash
python tools/psychology/ideological_consistency_test.py "Stated beliefs text"
cat beliefs.txt | python tools/psychology/ideological_consistency_test.py
```

**Output:** JSON in `output/psychology/ideological_consistency_test/`
- Core claims and hidden premises
- Internal contradictions with severity ratings
- Predicted behaviors vs. consistent behaviors
- Self-test questions and reading prompts

**Prompts:** Philosopher → logician → behavioral scientist → epistemologist

---

#### 🕵️ Revealed Preference Detective
Contrast stated preferences with revealed behavior to infer real values.

**Usage:**
```bash
python tools/psychology/revealed_preference_detective.py "Stated pref" --context "Revealed behavior"
```

**Output:** JSON in `output/psychology/revealed_preference_detective/`
- Contradiction severity
- Actual value hierarchy (revealed)
- Predicted choice in forced tradeoff

---

### 🧠 Social Dynamics Tools

#### 🧠 Status Game Decoder
Parse social interactions for signals, hierarchy, and the real game being played.

**Usage:**
```bash
python tools/social/status_game_decoder.py "Describe the scene"
```

**Output:** JSON in `output/social/status_game_decoder/`
- Surface analysis
- Status signals (subtle and overt)
- Inferred hierarchy
- Real game being played
- Countermoves

---

### 🎯 Strategy Tools

#### ⚡ Crisis Opportunity Scanner
Spot agenda-driven moves during crises: actors, overreach solutions, bypass mechanisms.

**Usage:**
```bash
python tools/strategy/crisis_opportunity_scanner.py "Describe the crisis"
```

**Output:** JSON in `output/strategy/crisis_opportunity_scanner/`
- Key actors and their agendas
- Overreach solutions (proposals exceeding crisis scope)
- Bypass mechanism (resistance strategy)
- Guardrails and red lines

---

#### 📈 Goodhart's Law Predictor
Stress-test metrics for gaming strategies, unintended consequences, and long-term distortion.

**Usage:**
```bash
python tools/strategy/goodharts_law_predictor.py "Metric description"
```

**Output:** JSON in `output/strategy/goodharts_law_predictor/`
- Gaming strategies (how to cheat the metric)
- Unintended consequences
- Long-term distortion
- Mitigations

---

#### 🕊️ Diplomatic Subtext Decoder
Translate diplomatic language into real intent, predict responses, surface political purpose.

**Usage:**
```bash
python tools/strategy/diplomatic_subtext_decoder.py "Statement text"
```

**Output:** JSON in `output/strategy/diplomatic_subtext_decoder/`
- Plain translation
- Action level (escalation vs. de-escalation)
- Predicted response
- Political purpose

---

#### 🔒 Platform Lock-in Forensics
Analyze platform lock-in mechanisms, switching costs, and escape routes.

**Usage:**
```bash
python tools/strategy/platform_lock_in_forensics.py "Platform description"
```

**Output:** JSON in `output/strategy/platform_lock_in_forensics/`
- Lock-in mechanisms
- Switching costs (time, money, data)
- Mitigations and escape routes

---

#### 🧩 Coalition Fracture Simulator
Identify fault lines in coalitions, fracture triggers, and mitigation strategies.

**Usage:**
```bash
python tools/strategy/coalition_fracture_simulator.py "Describe the coalition"
```

**Output:** JSON in `output/strategy/coalition_fracture_simulator/`
- Fault lines (value conflicts, power imbalances)
- Fracture triggers
- Scenarios (how it breaks)
- Mitigations

---

### 🌍 Geopolitics Tools

#### 🛰️ Proxy War Analyst
Analyze proxy conflicts: actors, objectives, escalation paths, off-ramps.

**Usage:**
```bash
python tools/geopolitics/proxy_war_analyst.py "Conflict description"
```

**Output:** JSON in `output/geopolitics/proxy_war_analyst/`
- Actors and objectives (sponsors + proxies)
- Escalation paths
- Off-ramps and peace conditions

---

### 🏛️ Policy & Politics Tools

#### 🐖 Bill Pork Barrel Finder
Identify pork barrel items, beneficiaries, and funding mechanisms in legislation.

**Usage:**
```bash
python tools/policy/bill_pork_barrel_finder.py "Bill text or summary"
```

**Output:** JSON in `output/policy/bill_pork_barrel_finder/`
- Pork items (suspicious spending)
- Beneficiaries and payers
- Red flags and justifications

---

#### 🏛️ Regulatory Capture Mapper
Detect regulatory capture signals and revolving door dynamics.

**Usage:**
```bash
python tools/policy/regulatory_capture_mapper.py "Agency/industry description"
```

**Output:** JSON in `output/policy/regulatory_capture_mapper/`
- Capture signals
- Incentives and mechanisms
- Mitigations

---

#### 📋 Campaign Promise Tracker
Track campaign promises, assess feasibility, identify blockers.

**Usage:**
```bash
python tools/politics/campaign_promise_tracker.py "Speech/manifesto text"
```

**Output:** JSON in `output/politics/campaign_promise_tracker/`
- Promises extracted
- Feasibility assessment
- Blockers (political, legal, budgetary)
- Verification hooks

---

### 🎭 Culture Tools

#### 🎭 Corporate Theater Director
Decode performative corporate rituals and propose honest alternatives.

**Usage:**
```bash
python tools/culture/corporate_theater_director.py "Describe the ritual/town hall/email"
```

**Output:** JSON in `output/culture/corporate_theater_director/`
- Performative moves
- Real incentives
- Honest alternative (what they should actually say/do)

---

### 📈 Marketing Tools

#### 🧪 Viral Hook Laboratory
Generate viral hooks with risk/ethics analysis.

**Usage:**
```bash
python tools/marketing/viral_hook_laboratory.py "Product/message"
```

**Output:** JSON in `output/marketing/viral_hook_laboratory/`
- Viral hook candidates
- Psychological mechanisms
- Risk analysis (ethical concerns)
- Guardrails

---

### 📚 History Tools

#### 🧪 Historical What-If Machine
Analyze historical counterfactuals with ripple effects and plausibility.

**Usage:**
```bash
python tools/history/historical_what_if_machine.py "What if..." --context "Lens/constraints"
```

**Output:** JSON in `output/history/historical_what_if_machine/`
- Branch point analysis
- Immediate and long-term ripple effects
- Plausibility assessment
- Caveats and research hooks

---

### ✍️ Writing Tools

#### 🎭 Character Evolution Engine
Generate character arcs: trait, flaw, crucible challenge, growth, new adventure.

**Usage:**
```bash
python tools/writing/character_evolution_engine.py "Character type" --context "Genre, tone, constraints"
```

**Output:** JSON in `output/writing/character_evolution_engine/`
- Character baseline (trait + strength)
- Flaw and consequences
- Crucible challenge
- Growth moment
- New adventure hook

---

## Setup

### 1. Configure User Profile

Edit `context/user_profile.json` with your preferences:
```json
{
  "writing_style": {
    "tone": "Your preferred tone",
    "avoid": ["Things to avoid"],
    "prefer": ["Things to emphasize"]
  },
  "learning_profile": {
    "audience": "Your target audience",
    "depth": "Preferred depth level"
  },
  "expertise_level": "General/Intermediate/Expert"
}
```

### 2. Ensure API Access

Tools use the same `.env` setup as the main framework:
```bash
OPENROUTER_API_KEY=sk-or-v1-your_key_here
```

Get a key at [openrouter.ai/keys](https://openrouter.ai/keys)

### 3. Run a Tool

```bash
python tools/content/evergreen_guide.py "Test topic"
python tools/learning/concept_simplifier.py "Quantum mechanics"
python tools/business/negotiation_strategy_builder.py "Salary negotiation scenario"
```

---

## Output Structure

```
output/
├── guides/                          # Evergreen guide outlines
├── learning/
│   ├── concept_simplifier/          # Topic breakdowns
│   └── subject_connector/           # Subject connections
├── research/
│   ├── timelines/                   # Research timelines
│   └── emergence_simulator/         # Emergence analyses
├── career/
│   ├── dream_job_reverse_engineer/  # Job analysis
│   ├── meeting_dynamics_forensics/  # Meeting analyses
│   └── credential_inflation_analyzer/ # Credential analysis
├── business/
│   └── negotiation_strategy_builder/ # Negotiation strategies
├── dev/
│   └── code_architecture_critic/    # Code audits
├── collaboration/
│   └── common_ground_finder/        # Disagreement bridges
├── brainstorm/
│   └── problem_solution_spider/     # Problem-solving
├── media/                           # Media literacy analyses
├── psychology/                      # Behavioral analyses
├── social/                          # Social dynamics
├── strategy/                        # Strategic analyses
├── geopolitics/                     # Geopolitical analyses
├── policy/                          # Policy analyses
├── politics/                        # Political analyses
├── culture/                         # Cultural analyses
├── marketing/                       # Marketing strategies
├── history/                         # Historical analyses
└── writing/                         # Creative writing
```

Logs are saved to `logs/` with token usage and cost estimates.

---

## Energy Cost Reference

| Tool Category | Setup | Usage | Value | Net ROI |
|---------------|-------|-------|-------|---------|
| Content (Evergreen Guide) | 0min | 2min | 2hrs saved | +++ |
| Career (Dream Job) | 0min | 2min | Interview advantage | +++ |
| Business (Negotiation) | 0min | 3min | Worth $1000s | +++ |
| Research (Timeline) | 0min | 2min | Hours of research | +++ |
| Learning (Concept Simplifier) | 0min | 2min | Deep understanding | +++ |
| Strategy (Crisis Scanner) | 0min | 2min | Pattern recognition | ++ |
| Media (Bias Triangulator) | 0min | 2min | Media literacy | ++ |

All tools are **Energy ROI Positive**: value delivered exceeds effort required.

---

## Cost Tracking

View token usage and costs:
```bash
python tools/cost_report.py
```

This analyzes all logs and shows:
- Per-tool usage statistics
- Total tokens consumed
- Estimated costs
- Most/least expensive tools

---

## Development Guidelines

### When Adding New Tools

1. **User Context**: Load `context/user_profile.json` automatically
2. **CLI-First**: Accept input via args or stdin
3. **Output Structure**: Save to appropriate `output/` subdirectory
4. **Error Handling**: Graceful degradation, partial value
5. **Energy Test**: Can you use it at 50% capacity?
6. **Cost Visibility**: Include usage stats in logs
7. **Prompt Engineering**: Use expert personas, frameworks, examples, constraints

### Tool Template

See existing tools for patterns. All tools should:
- Have clear docstrings with usage examples
- Use `tool_utils.py` for common functionality
- Save JSON output with timestamps
- Create markdown logs via `MinimalChainable.log_to_markdown()`
- Print clear success messages with output paths

---

## Feedback Loop

Track which tools you actually use:
- **Using weekly**: Keep and improve
- **Using monthly**: Good, maintain
- **Haven't used in 2 weeks**: Archive or delete

Better to have 5 great tools than 20 mediocre ones.

---

## Prompt Engineering Quality

All 33 tools now feature:
- **Expert personas**: Specific roles with 15-20+ years experience
- **Structured frameworks**: Step-by-step analytical approaches
- **Concrete examples**: ✅ GOOD / ❌ BAD patterns for every prompt
- **Well-defined constraints**: Explicit word counts, item counts, format requirements
- **Educational approach**: Prompts explain methodologies, not just ask for output

This results in professional-grade output quality with consistent structure.

---

**Tools that feel like extensions of your mind, not external systems to manage.**
