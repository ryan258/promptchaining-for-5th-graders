# Prompt Chaining Roadmap

## Project Status

### Recently Completed ✅

**Political & Media Metagames** (Dec 2024)
- [x] Campaign Promise Tracker
- [x] Euphemism Decoder
- [x] Coalition Fracture Simulator
- [x] Media Bias Triangulator
- [x] Proxy War Analyst
- [x] Crisis Opportunity Scanner
- [x] Astroturf Detector
- [x] Diplomatic Subtext Decoder
- [x] Bill Pork Barrel Finder
- [x] Ideological Consistency Test

**Metagame X-Ray Vision** (Dec 2024)
- [x] Status Game Decoder
- [x] Credential Inflation Analyzer
- [x] Corporate Theater Director
- [x] Meeting Dynamics Forensics
- [x] Revealed Preference Detective
- [x] Regulatory Capture Mapper
- [x] Platform Lock-In Forensics
- [x] Goodhart's Law Predictor
- [x] Narrative Warfare Analyst
- [x] Consensus Manufacturing Detective

**Monetizable Skills** (Dec 2024)
- [x] Dream Job Reverse Engineer
- [x] Viral Hook Laboratory
- [x] Negotiation Strategy Builder
- [x] Code Architecture Critic

**OpenRouter API Migration** (Nov 2024)
- [x] Migrated from Google Gemini to OpenRouter API
- [x] Updated all 8 demos to use OpenRouter
- [x] Improved code quality with triple-quoted strings
- [x] Vendor-neutral documentation

**Benefits**: Access to 100+ AI models (GPT, Claude, Gemini, Llama, etc.) through one API

**Logging & Documentation** (Dec 2024)
- [x] Add automatic markdown logging to demos
- [x] Create timestamped logs in `/logs` directory
- [x] Create HAPPY-PATH.md beginner guide
- [x] Add error handling to log_to_markdown()
- [x] Simplify FusionChain to parallel-only execution
- [x] Add logging to all 32 demos

---

## Current Priorities

### High Priority

**Code Quality**
- [x] ~~Remove debug print statements (main.py line 16)~~ (verified removed)
- [ ] Add defensive programming (check empty model_names list)
- [ ] Improve error messages for edge cases
- [ ] Consider removing duplicate GETTING_STARTED.md vs HAPPY-PATH.md

**User Experience**
- [ ] Create demo selector CLI (interactive menu to choose which demo to run)
- [ ] Add progress indicators for long-running chains
- [ ] Better error handling and user feedback

**Documentation**
- [x] ~~Add troubleshooting guide for common issues~~ (in GETTING_STARTED.md)
- [ ] Document the FusionChain pattern more thoroughly
- [ ] Add examples of custom evaluator functions
- [ ] Update HAPPY-PATH.md to mention logs directory

### Medium Priority

**Robustness**
- [ ] Add retry logic for API failures (exponential backoff)
- [ ] Implement cost tracking/estimation
- [ ] Add configurable rate limiting

**Log Management**
- [ ] Add log cleanup utility (delete old logs)
- [ ] Document log retention strategy
- [ ] Consider max logs per demo (e.g., keep last 10)

**Testing**
- [ ] Integration tests with real API calls
- [ ] Unit tests for error handling scenarios
- [ ] Unit tests for log_to_markdown()
- [ ] GitHub Actions for CI/CD

### Low Priority

**Advanced Features**
- [ ] Prompt template library for common patterns
- [ ] Response caching system for development
- [ ] Support for streaming responses
- [ ] Web interface for visual chain building

---

## Learning Goals

### Core Concepts
- ✅ Prompt chaining and sequential reasoning
- ✅ Context management and variable substitution
- ✅ Multi-model comparison and evaluation
- ✅ API integration patterns
- ✅ Output logging and history tracking

### Technical Skills
- ✅ Python async/concurrency patterns (ThreadPoolExecutor)
- ✅ API client design
- ⏳ Error handling and retry logic (partial)
- ✅ Testing strategies (basic unit tests)
- ✅ File I/O and markdown generation

### System Design
- ✅ Breaking complex problems into steps
- ✅ Building composable abstractions
- ✅ Designing for extensibility
- ✅ Cost-aware architecture

---

## Demo Evolution

### Existing Demos (32)

#### Educational Foundations (8)
1. ✅ Character Evolution Engine - narrative development (with logging)
2. ✅ Common Ground Finder - conflict resolution (with logging)
3. ✅ Concept Simplifier - explanatory chains (with logging)
4. ✅ Emergence Simulator - complex systems (with logging)
5. ✅ Historical What-If Machine - counterfactual reasoning (with logging)
6. ✅ Knowledge Time Machine - temporal analysis (with logging)
7. ✅ Problem-Solution Spider - creative problem-solving (with logging)
8. ✅ Subject Connector - interdisciplinary thinking (with logging)

#### Monetizable Skills (4)
1. ✅ Dream Job Reverse Engineer
2. ✅ Viral Hook Laboratory
3. ✅ Negotiation Strategy Builder
4. ✅ Code Architecture Critic

#### Metagame X-Ray Vision (10)
1. ✅ Status Game Decoder
2. ✅ Credential Inflation Analyzer
3. ✅ Corporate Theater Director
4. ✅ Meeting Dynamics Forensics
5. ✅ Revealed Preference Detective
6. ✅ Regulatory Capture Mapper
7. ✅ Platform Lock-In Forensics
8. ✅ Goodhart's Law Predictor
9. ✅ Narrative Warfare Analyst
10. ✅ Consensus Manufacturing Detective

#### Political & Media Metagames (10)
1. ✅ Campaign Promise Tracker
2. ✅ Euphemism Decoder
3. ✅ Coalition Fracture Simulator
4. ✅ Media Bias Triangulator
5. ✅ Proxy War Analyst
6. ✅ Crisis Opportunity Scanner
7. ✅ Astroturf Detector
8. ✅ Diplomatic Subtext Decoder
9. ✅ Bill Pork Barrel Finder
10. ✅ Ideological Consistency Test

### Potential New Demos (Future Ideas)

> **What makes these exceptional**: Each demo leverages prompt chaining to achieve insights impossible with single prompts. They build complexity through iteration, self-critique, perspective shifting, and emergent reasoning.

#### 💰 Monetizable Skills (Direct Value Creation)

1. **Dream Job Reverse Engineer** - job posting → decode hidden priorities → identify decision makers' pain → craft application strategy → write tailored resume bullets → generate interview stories
   - *Why exceptional*: Treats job hunting as reverse engineering, not template filling
   - *Chaining power*: Each layer adds psychological insight the next builds on
   - *Value*: Could literally change someone's career trajectory

2. **Viral Hook Laboratory** - boring topic → emotional core → 10 angle variations → predict virality scores → combine best elements → A/B test versions
   - *Why exceptional*: Systematically deconstructs what makes content spread
   - *Chaining power*: Evolution through iteration, not random guessing
   - *Value*: Direct ROI for content creators and marketers

3. **Negotiation Strategy Builder** - situation → power analysis → BATNA identification → frame anchors → predict objections → counter-scripts → walk-away triggers
   - *Why exceptional*: Game theory applied to real conversations
   - *Chaining power*: Each step forces strategic thinking about the next
   - *Value*: Literally worth thousands in salary/deal negotiations

4. **Code Architecture Critic** - code sample → identify patterns → spot code smells → suggest refactors → predict maintenance costs → generate test cases → final architecture
   - *Why exceptional*: Builds understanding like a senior engineer reviewing junior code
   - *Chaining power*: Progressive abstraction from syntax to system design
   - *Value*: Teaches architecture thinking, not just coding

#### 🧠 Cognitive Amplification (Think Better, Not Just Faster)

5. **Assumption Excavator** - belief/claim → underlying assumptions → test each assumption → find weakest links → explore alternatives → rebuild belief
   - *Why exceptional*: Makes invisible thinking visible
   - *Chaining power*: Can't find deep assumptions without first finding surface ones
   - *Insight*: Most beliefs collapse when you dig deep enough

6. **Devil's Advocate Chain** - your position → strongest counterarguments → steel man opponent → find actual weak points → strengthen or pivot
   - *Why exceptional*: Forces intellectual honesty through adversarial thinking
   - *Chaining power*: Each critique informs the next layer of defense
   - *Growth*: Prevents echo chamber thinking

7. **Perspective Kaleidoscope** - situation → child's view → elder's view → alien's view → your enemy's view → synthesis → blind spots revealed
   - *Why exceptional*: Systematic perspective-taking reveals what you can't see
   - *Chaining power*: Each perspective unlocks different aspects of truth
   - *Insight*: Reality is multi-faceted; single perspectives are always incomplete

8. **Second-Order Consequence Explorer** - decision → immediate effects → ripple effects → long-tail consequences → unexpected interactions → risk/opportunity map
   - *Why exceptional*: Most people stop at first-order thinking
   - *Chaining power*: Can't see third-order effects until you map second-order
   - *Value*: Prevents disasters, reveals hidden opportunities

#### 🎯 Pattern Recognition & Synthesis

9. **Cross-Domain Pattern Mapper** - pattern in Domain A → abstract the mechanism → find parallel in Domain B → test mapping → generate novel insights → apply back to A
   - *Why exceptional*: How breakthroughs actually happen (borrowing from other fields)
   - *Chaining power*: Abstraction enables transfer, transfer enables innovation
   - *Example*: Evolution → algorithms → business strategy → personal growth

10. **Failure Autopsy Lab** - failed project → timeline of decisions → counterfactuals at each point → identify pivot moments → extract lessons → predict similar failures
    - *Why exceptional*: Treats failure as data, not shame
    - *Chaining power*: Sequential analysis reveals causation chains
    - *Value*: One avoided failure pays for itself

11. **Signal vs Noise Filter** - messy data/situation → identify signal patterns → map noise sources → extract core signal → predict future → confidence intervals
    - *Why exceptional*: Systematically separates meaning from randomness
    - *Chaining power*: Can't extract signal until you characterize noise
    - *Insight*: Most people react to noise thinking it's signal

12. **Wisdom Extraction Chain** - raw experience → concrete details → patterns across experiences → principles → edge cases → refined wisdom → teaching story
    - *Why exceptional*: Transforms experience into transferable knowledge
    - *Chaining power*: Abstraction ladder from specific to universal
    - *Value*: Makes tacit knowledge explicit

#### 🔮 Futures & Possibilities

13. **Scenario Branch Explorer** - current situation → key uncertainties → 4 extreme futures → paths to each → early warning signs → strategy for each scenario
    - *Why exceptional*: Structured uncertainty management, not prediction
    - *Chaining power*: Branches multiply, strategies adapt to branches
    - *Value*: Prepare for multiple futures, not just the expected one

14. **Innovation Gap Finder** - current state → ideal state → gaps → technologies needed → who's working on what → collaboration opportunities → your unique angle
    - *Why exceptional*: Maps the innovation landscape systematically
    - *Chaining power*: Each layer reveals where white space exists
    - *Value*: Find opportunities others miss

15. **Trend Collision Predictor** - Trend A → Trend B → interaction points → amplification effects → conflict points → emergent possibilities → investment thesis
    - *Why exceptional*: Breakthroughs happen at intersections
    - *Chaining power*: Can't predict collisions without mapping trajectories
    - *Profit*: See the future before the market does

16. **Backcasting from Utopia** - dream future → work backward → required milestones → blockers at each stage → solutions to blockers → actionable first step TODAY
    - *Why exceptional*: Inverts planning (future→present instead of present→future)
    - *Chaining power*: Each step backward reveals what must come before
    - *Value*: Makes impossible goals actionable

#### 🎨 Creative Synthesis

17. **Constraint-Driven Innovation** - problem → add absurd constraint → force solution → add second constraint → force adaptation → remove constraints → keep insights
    - *Why exceptional*: Constraints are features, not bugs, for creativity
    - *Chaining power*: Each constraint forces novel thinking paths
    - *Example*: Design a car (boring) → that's also a boat → that costs $100 → now what did we learn?

18. **Remix Machine** - Input A + Input B → find unexpected connections → mash up → evaluate strangeness × usefulness → iterate best mashup → polish
    - *Why exceptional*: Systematizes serendipity
    - *Chaining power*: Iterate on mashups, not just combine once
    - *Fun*: Picasso + quantum physics + cooking = ?

19. **Idea Evolution Chamber** - seed idea → mutate in 5 directions → select fittest → mutate winners → repeat 3 generations → compare to original
    - *Why exceptional*: Genetic algorithms for concepts
    - *Chaining power*: Evolution only works across generations
    - *Insight*: Best ideas often unrecognizable from starting point

20. **Paradox Resolver** - contradiction → reframe as paradox → both sides true? → find higher perspective → dissolve or embrace paradox → wisdom
    - *Why exceptional*: Most problems are paradoxes, not puzzles
    - *Chaining power*: Can't transcend without first understanding both poles
    - *Example*: "Be confident" + "Be humble" = ? (Leadership = context-switching)

---

### Why These Are ACTUALLY Exceptional

**Traditional demos**: Show the tool works
**These demos**: Show impossible-without-chaining insights

**What makes chaining essential here:**
- 🔄 **Iterative refinement** - Each step improves on the last
- 🔀 **Perspective multiplication** - See from angles impossible for one prompt
- 🧬 **Emergent complexity** - Later steps couldn't exist without earlier ones
- 🎯 **Progressive abstraction** - Climb from specific to universal
- 💡 **Self-critique loops** - The chain argues with itself
- 🌊 **Cascading insights** - Each discovery enables the next

### Selection Framework

Pick demos that:
1. **Couldn't work as one prompt** - The chain IS the insight
2. **Teach transferable thinking** - Not just outputs, but thought processes
3. **Produce "aha moments"** - Show something genuinely surprising
4. **Have commercial value** - People would pay for these insights
5. **Are intellectually beautiful** - Elegant in their reasoning

### Implementation Priority

**Start Here** (High value × Easy):
- Dream Job Reverse Engineer (immediate personal value)
- Assumption Excavator (profound yet simple)
- Second-Order Consequence Explorer (universally applicable)

**Build Next** (Teach advanced patterns):
- Cross-Domain Pattern Mapper (abstraction skills)
- Idea Evolution Chamber (iteration mechanics)
- Perspective Kaleidoscope (empathy + synthesis)

**Advanced** (Show full power):
- Scenario Branch Explorer (complex state management)
- Trend Collision Predictor (multi-variable synthesis)
- Paradox Resolver (meta-level thinking)

---

### Metagame X-Ray Demos (10 Demos That Reveal Hidden Strategic Layers)

> **What are metagames?** The game about the game. The unwritten rules, hidden incentives, and strategic patterns that govern how systems actually work vs. how they claim to work. These demos reveal uncomfortable truths.

#### 🎭 Social & Professional Metagames

1. **Status Game Decoder** - social situation → identify status signals → map dominance hierarchy → decode who's actually winning → reveal the real game being played
   - *X-Ray Vision*: "They're debating ideas" is surface game. Real game: "Who gets to define what counts as smart"
   - *Chaining Power*: Can't see the meta-game without first mapping the surface game
   - *Uncomfortable Truth*: Most "intellectual debates" are status battles in disguise
   - *Example*: Meeting where everyone agrees but nothing happens → reveals who has veto power nobody admits to

2. **Credential Inflation Analyzer** - requirement "10 years experience" → trace historical requirement → identify inflation rate → predict future → reveal the signaling arms race
   - *X-Ray Vision*: Job requirements aren't about skills, they're about filtering and signaling
   - *Chaining Power*: Historical analysis reveals the accelerating treadmill
   - *Uncomfortable Truth*: More education doesn't mean more skilled, just more competitive signaling
   - *Insight*: "Bachelor's required" (2000) → "Master's preferred" (2010) → "PhD or equivalent" (2025) for same job

3. **Corporate Theater Director** - stated company value → actual behavior → identify gap → decode real incentive structure → predict what actually gets rewarded
   - *X-Ray Vision*: "We value innovation" vs "We punish failure"
   - *Chaining Power*: Gap between stated and revealed preferences exposes the real game
   - *Uncomfortable Truth*: Company values are marketing; incentive structures are truth
   - *Example*: "Flat hierarchy" company where only CEO's friends get promoted

4. **Meeting Dynamics Forensics** - meeting transcript → identify who interrupts whom → map who defers to whom → reveal actual power structure → compare to org chart
   - *X-Ray Vision*: Org chart shows claimed structure; interruption patterns show real power
   - *Chaining Power*: Behavioral micro-patterns reveal macro power dynamics
   - *Uncomfortable Truth*: The person running the meeting isn't always the person with the power
   - *Pattern*: Person who can violate rules without consequence = actual authority

#### 💰 Economic & Market Metagames

5. **Revealed Preference Detective** - what people say they value → what they actually pay for → identify contradictions → decode real values → predict future behavior
   - *X-Ray Vision*: "I care about privacy" but uses free services that sell data
   - *Chaining Power*: Stated preferences lie; revealed preferences tell truth
   - *Uncomfortable Truth*: People don't know their own values; their purchases do
   - *Example*: "Support local businesses" but Amazon Prime delivery daily

6. **Regulatory Capture Mapper** - regulation text → identify who wrote it → trace lobbying money → find exceptions that matter → reveal who really wins
   - *X-Ray Vision*: Regulations that claim to protect consumers often protect incumbents
   - *Chaining Power*: Follow the exceptions to find the real beneficiaries
   - *Uncomfortable Truth*: Many regulations are barriers to entry disguised as consumer protection
   - *Pattern*: "Licensing for public safety" = "Preventing competition"

7. **Platform Lock-In Forensics** - user-friendly feature → identify switching cost → calculate lock-in value → predict extraction timeline → see the trap
   - *X-Ray Vision*: Free tier → network effects → proprietary format → price increase
   - *Chaining Power*: Each convenience feature is actually a moat deepener
   - *Uncomfortable Truth*: "For your convenience" often means "to trap you"
   - *Example*: Cloud photo storage → all photos there → can't switch → price increase

8. **Goodhart's Law Predictor** - new metric announced → predict how it will be gamed → identify unintended consequences → simulate optimization → show the distortion
   - *X-Ray Vision*: "When a measure becomes a target, it ceases to be a good measure"
   - *Chaining Power*: Can't predict gaming without first understanding the incentive structure
   - *Uncomfortable Truth*: Every metric creates its own distortion
   - *Example*: "Lines of code" metric → developers write verbose code → productivity decreases

#### 🧠 Information & Narrative Metagames

9. **Narrative Warfare Analyst** - competing narratives → identify frame battles → map who benefits from each frame → predict which wins → reveal the real conflict
   - *X-Ray Vision*: "Tax relief" vs "Tax cuts for the rich" - same policy, different frames, different winners
   - *Chaining Power*: The fight over framing determines the fight over policy
   - *Uncomfortable Truth*: He who controls the frame controls the game
   - *Example*: "Pro-life" vs "Pro-choice" - neither side accepts the other's frame because that concedes the game
**What makes these X-ray vision:**
- 🎭 **Surface vs Reality Gap** - Stated game vs actual game
- 💡 **Incentive Forensics** - What's rewarded reveals what's valued
- 🔍 **Pattern Recognition** - Same metagame across different domains
- 🎯 **Predictive Power** - Understanding metagames predicts behavior
- 🧠 **Mental Models** - Changes how you see power and strategy
- ⚡ **Uncomfortable Truths** - Real insights make you slightly queasy

### Metagame Principles These Demos Teach

1. **Revealed Preferences > Stated Preferences** - Watch what people do, not what they say
2. **Incentives > Intentions** - Good intentions without aligned incentives fail
3. **Second-Order Effects > First-Order** - The game after the game matters more
4. **Frame Control = Game Control** - Who defines terms wins before the debate starts
5. **Exceptions Reveal Rules** - Who can break rules shows who has power
6. **Metrics Shape Reality** - Measuring changes what's measured (Goodhart's Law)
7. **Friction = Moat** - Every inconvenience might be strategic lock-in
8. **Consensus is Manufactured** - "Everyone knows" is often "someone decided"
9. **Status Battles Masquerade** - Most conflicts are about status, not the stated topic
10. **The Real Game is Meta** - Understanding the game about the game is the ultimate edge

### Implementation Notes

**Ethical Considerations:**
- These demos reveal uncomfortable truths about power and manipulation
- Can be used for defense (see through BS) or offense (deploy BS)
- Include ethical framing: "Understanding ≠ Endorsing"
- Add disclaimer: "These patterns exist whether you acknowledge them or not"

**Educational Value:**
- Teaches critical thinking at the highest level
- Reveals systems thinking patterns
- Shows game theory in the wild
- Develops immunity to manipulation
- Builds strategic awareness

**Prompt Chain Pattern:**
Most metagame demos follow this structure:
1. Observe surface game
2. Identify contradictions/gaps
3. Map actual incentive structure
4. Reveal hidden strategic layer
5. Predict behavior from meta-understanding

**Why Chaining is Essential:**
You cannot see the metagame directly - you must:
1. First map the surface game
2. Then identify anomalies (why doesn't behavior match stated rules?)
3. Then reverse-engineer the actual incentive structure
4. Only then can you see the real game

Single prompt: "What's the real game here?" → superficial answer
Chain: Surface → Contradictions → Incentives → Real Game → profound insight

### Start Here:
- **Revealed Preference Detective** (easiest to implement, universally applicable)
- **Status Game Decoder** (immediate social value, teaches pattern recognition)
- **Goodhart's Law Predictor** (simple concept, powerful implications)

### Most Mind-Bending:
- **Narrative Warfare Analyst** (changes how you read news forever)
- **Consensus Manufacturing Detective** (questions "obvious truths")
- **Platform Lock-In Forensics** (reveals traps you're already in)

---

## Architecture Improvements

### Recently Completed ✅
- [x] Better logging system (markdown logs)
- [x] Standardized error handling in logging
- [x] Input validation in log_to_markdown

### Short Term
- [ ] Separate configuration from code (move model lists to config)
- [ ] Standardized error types (custom exceptions)
- [ ] Input validation utilities
- [ ] Cost estimation before running chains

### Long Term
- [ ] Plugin system for custom chain types
- [ ] Chain composition/nesting (chains calling chains)
- [ ] Persistent chain state (resume interrupted chains)
- [ ] Performance monitoring and metrics

---

## Quality of Life Improvements

### Done ✅
- [x] Beginner-friendly documentation (HAPPY-PATH.md)
- [x] Automatic output logging
- [x] Security warnings in documentation
- [x] Virtual environment setup guide

### Planned
- [ ] Interactive demo picker (menu-driven selection)
- [ ] One-command demo runner (`python run_demo.py --all`)
- [ ] Log viewer CLI (`python view_logs.py`)
- [ ] Cost calculator (`python estimate_cost.py`)
- [ ] Demo template generator for new chains

---

## Technical Debt

### Known Issues
- [ ] GETTING_STARTED.md and HAPPY-PATH.md have significant overlap
- [ ] Some demos missing comprehensive docstrings
- [ ] No integration tests with real API
- [ ] FusionChain evaluator signature could be more flexible
- [ ] No caching mechanism for development iterations

### Code Cleanup
- [ ] Remove commented-out code in main.py
- [ ] Standardize import ordering across files
- [ ] Add type hints to all functions
- [ ] Extract magic strings to constants
- [ ] Add docstrings to all demo files

---

## Notes

This is a personal learning project focused on:
- Understanding prompt engineering patterns
- Experimenting with AI model capabilities
- Building reusable abstractions for LLM interactions
- Developing systematic thinking skills
- Tracking and analyzing prompt chain experiments

The framework is intentionally minimal to keep the focus on core concepts rather than framework complexity.

### Philosophy
- **Start simple, iterate**: Basic features first, then enhance
- **Document everything**: Future-you will thank present-you
- **Fail gracefully**: Never crash on predictable errors
- **Track experiments**: Every run should be logged for learning
- **Cost-conscious**: Always know what API calls cost

---

## Version History

### v0.3 (Current) - December 2024
- Added markdown logging system
- Created HAPPY-PATH.md guide
- Simplified FusionChain architecture
- Enhanced error handling

### v0.2 - November 2024
- Migrated to OpenRouter API
- Added 8 demo implementations
- Improved documentation
- Added basic unit tests

### v0.1 - Initial
- Core MinimalChainable framework
- Basic FusionChain implementation
- Google Gemini integration
