# 🧠 Cognitive Exoskeleton Tools

Production-ready tools that amplify output while conserving cognitive energy.

## Philosophy

These tools are designed for **low-energy usability**. If you can't use them on a bad day, they're not working.

### Design Principles

1. **Zero-config start**: Load user context automatically
2. **Resume-able**: Save state if interrupted
3. **Fast**: < 3 minutes for 80% of use cases
4. **Energy ROI positive**: Value out > effort in

---

## Content Tools

### 🌲 Evergreen Guide Architect

Transform topics or rough notes into structured, lasting guide outlines.

**Usage:**
```bash
# From topic
python tools/content/evergreen_guide.py "Progressive overload for MS patients"

# From notes
cat notes/training-thoughts.md | python tools/content/evergreen_guide.py

# With context
python tools/content/evergreen_guide.py "Topic" --context "Additional notes here"
```

**Output:**
- Markdown outline in `output/guides/`
- Analysis of user intent & pain points
- Competition differentiation strategy
- Key metaphors and research citations
- Evergreen audit (what stays timeless)
- Quality metrics and writing priorities

**Energy Cost**: Low (2-3 minutes)
**Energy Return**: High (saves hours of outlining)
**Net**: Strongly positive ✅

---

## Learning Tools

### 🧭 Concept Simplifier

Break complex topics into components, analogies, examples, and a concise explainer.

**Usage:**
```bash
python tools/learning/concept_simplifier.py "Diffusion models in AI"
python tools/learning/concept_simplifier.py "Topic" --context "Audience or constraints"
```

**Output:**
- JSON in `output/learning/concept_simplifier/`
- Components, analogies, examples, explainer, pitfalls, next steps
- Logs with token/cost estimates in `logs/`

### 🔗 Subject Connector

Find surprising links between two subjects, why they matter, and design a project that uses both.

**Usage:**
```bash
python tools/learning/subject_connector.py "Subject A" --context "Subject B"
```

**Output:**
- JSON in `output/learning/subject_connector/`
- Connections, importance, project idea with expected outputs
- Logs with token/cost estimates in `logs/`

---

## Research Tools

### 🕰️ Research Timeline (Knowledge Time Machine, adult mode)

Generate origin → evolution → current frontier timelines with citations and risks.

**Usage:**
```bash
python tools/research/timeline.py "CRISPR gene editing"
cat notes/topic.md | python tools/research/timeline.py --context "Specific angle"
```

**Output:**
- Markdown timeline in `output/research/`
- Origins, breakthroughs, current state, future speculation
- Risks/limitations and research gaps
- Logs with token/cost estimates in `logs/`

**Energy Cost**: Low (2-3 minutes)
**Energy Return**: High (research prep shortcut)
**Net**: Strongly positive ✅

---

## Development Tools

### 🏗️ Code Architecture Critic

Audit a code snippet for patterns/anti-patterns, smells, refactors, risks, and an improved architecture sketch.

**Usage:**
```bash
python tools/dev/code_architecture_critic.py "path/to/file.py"
python tools/dev/code_architecture_critic.py "inline code" --context "constraints or goals"
```

**Output:**
- JSON in `output/dev/code_architecture_critic/`
- Patterns/anti-patterns, smells, refactor plan, maintenance forecast, architecture sketch
- Logs with token/cost estimates in `logs/`

---

## Collaboration Tools

### 🤝 Common Ground Finder

Map opposing views to values, shared concerns, common goals, and bridge options.

**Usage:**
```bash
python tools/collaboration/common_ground_finder.py "View A" --context "View B"
```

**Output:**
- JSON in `output/collaboration/common_ground_finder/`
- Values, shared concerns, common goals, bridge ideas, conversation prompts
- Logs with token/cost estimates in `logs/`

---

## Brainstorming Tools

### 🕷️ Problem–Solution Spider

Clarify a problem, constraints, wild ideas, blended solutions, and a quick test scenario.

**Output:**
- JSON in `output/brainstorm/problem_solution_spider/`
- Defined problem, constraints/resources, wild ideas, solution options, test scenario
- Logs with token/cost estimates in `logs/`

---

## Career Tools

### 🎯 Dream Job Reverse Engineer

Decode a job posting into hidden priorities, pain points, application strategy, resume bullets, and STAR stories.

**Usage:**
```bash
python tools/career/dream_job_reverse_engineer.py "path/to/job.txt"
python tools/career/dream_job_reverse_engineer.py "Job text" --context "Your profile/angle"
```

**Output:**
- JSON in `output/career/dream_job_reverse_engineer/`
- Hidden priorities, pain points, strategy, bullets, STAR outlines
- Logs with token/cost estimates in `logs/`

### 🔎 Meeting Dynamics Forensics

Analyze meeting transcripts for interruptions, deference, and the real power hierarchy.

**Usage:**
```bash
python tools/career/meeting_dynamics_forensics.py "Transcript text"
cat meeting.txt | python tools/career/meeting_dynamics_forensics.py
```

**Output:**
- JSON in `output/career/meeting_dynamics_forensics/`
- Interruptions, deference markers, inferred hierarchy, red flags
- Logs with token/cost estimates in `logs/`

---

## Media Literacy Tools

### 🧹 Euphemism Decoder

Turn sanitized language into plain English, expose intent, and flag manipulation.

**Usage:**
```bash
python tools/media/euphemism_decoder.py "Quoted text"
cat speech.txt | python tools/media/euphemism_decoder.py
```

**Output:**
- JSON in `output/media/euphemism_decoder/`
- Euphemism mappings, plain-English rewrite, intent/beneficiaries
- Logs with token/cost estimates in `logs/`

### 🧭 Media Bias Triangulator

Generate polarized framings, surface omissions, and synthesize ground truth.

**Usage:**
```bash
python tools/media/media_bias_triangulator.py "Event description"
cat event.txt | python tools/media/media_bias_triangulator.py
```

**Output:**
- JSON in `output/media/media_bias_triangulator/`
- Biased headlines, omissions, ground truth synthesis
- Logs with token/cost estimates in `logs/`

### 🌾 Astroturf Detector

Assess whether messaging shows signs of astroturfing/coordination.

**Usage:**
```bash
python tools/media/astroturf_detector.py "Thread/post text"
```

**Output:**
- JSON in `output/media/astroturf_detector/`
- Signals, likely origin/motives, confidence, verdict/watch-next
- Logs with token/cost estimates in `logs/`

### 🧠 Consensus Manufacturing Detective

Spot framing/repetition/omissions used to manufacture consensus and who benefits.

**Usage:**
```bash
python tools/media/consensus_manufacturing_detective.py "Campaign text"
```

**Output:**
- JSON in `output/media/consensus_manufacturing_detective/`
- Frames, omissions, beneficiaries, counter-frames
- Logs with token/cost estimates in `logs/`

### 🛡️ Narrative Warfare Analyst

Analyze competing narratives, techniques, escalation risks, and counters.

**Usage:**
```bash
python tools/media/narrative_warfare_analyst.py "Narrative summary or quotes"
```

**Output:**
- JSON in `output/media/narrative_warfare_analyst/`
- Narratives, techniques, counters, monitoring signals
- Logs with token/cost estimates in `logs/`

---

## Social Dynamics Tools

### 🧠 Status Game Decoder

Parse social interactions for signals, hierarchy, and the real game being played.

**Usage:**
```bash
python tools/social/status_game_decoder.py "Describe the scene"
```

**Output:**
- JSON in `output/social/status_game_decoder/`
- Surface analysis, signals, hierarchy, real game, countermoves
- Logs with token/cost estimates in `logs/`

---

## Strategy Tools

### ⚡ Crisis Opportunity Scanner

Spot agenda-driven moves during a crisis: actors, overreach solutions, and the bypass mechanism.

**Usage:**
```bash
python tools/strategy/crisis_opportunity_scanner.py "Describe the crisis"
```

**Output:**
- JSON in `output/strategy/crisis_opportunity_scanner/`
- Actors, overreach solutions, bypass mechanism, guardrails
- Logs with token/cost estimates in `logs/`

### 📈 Goodhart's Law Predictor

Stress-test a metric for gaming strategies, unintended consequences, and long-term distortion.

**Usage:**
```bash
python tools/strategy/goodharts_law_predictor.py "Metric description"
```

**Output:**
- JSON in `output/strategy/goodharts_law_predictor/`
- Gaming strategies, unintended consequences, long-term distortion, mitigations
- Logs with token/cost estimates in `logs/`

### 🕊️ Diplomatic Subtext Decoder

Translate diplomatese into real intent, predict responses, and surface political purpose.

**Usage:**
```bash
python tools/strategy/diplomatic_subtext_decoder.py "Statement text"
```

**Output:**
- JSON in `output/strategy/diplomatic_subtext_decoder/`
- Plain translation, action level, predicted response, political purpose
- Logs with token/cost estimates in `logs/`

---

## Business Tools

### 🤝 Negotiation Strategy Builder

Analyze leverage, BATNAs, anchors, objections, and counter-scripts for a negotiation scenario.

**Usage:**
```bash
python tools/business/negotiation_strategy_builder.py "Scenario description"
python tools/business/negotiation_strategy_builder.py "Scenario" --context "Role, constraints, numbers"
```

**Output:**
- JSON in `output/business/negotiation_strategy_builder/`
- Leverage/BATNA, anchor, objections, scripts, guardrails
- Logs with token/cost estimates in `logs/`

---

## Psychology Tools

### 🕵️ Revealed Preference Detective

Contrast stated preferences with revealed behavior to infer real values and likely choices.

**Usage:**
```bash
python tools/psychology/revealed_preference_detective.py "Stated pref" --context "Revealed behavior"
```

**Output:**
- JSON in `output/psychology/revealed_preference_detective/`
- Contradiction severity, actual value hierarchy, predicted choice
- Logs with token/cost estimates in `logs/`

---

## Writing Tools

### 🎭 Character Evolution Engine

Generate a character arc (trait, flaw, crucible challenge, growth, new adventure).

**Usage:**
```bash
python tools/writing/character_evolution_engine.py "Character type" --context "Genre, tone, constraints"
```

**Output:**
- JSON in `output/writing/character_evolution_engine/`
- Character baseline, flaw, challenge, growth, new adventure hook
- Logs with token/cost estimates in `logs/`

---

## Psychology Tools

### 🕵️ Revealed Preference Detective

Contrast stated preferences with revealed behavior to infer real values and likely choices.

**Usage:**
```bash
python tools/psychology/revealed_preference_detective.py "Stated pref" --context "Revealed behavior"
```

**Output:**
- JSON in `output/psychology/revealed_preference_detective/`
- Contradiction severity, actual value hierarchy, predicted choice
- Logs with token/cost estimates in `logs/`

**Usage:**
```bash
python tools/brainstorm/problem_solution_spider.py "Problem statement"
python tools/brainstorm/problem_solution_spider.py "Problem" --context "Constraints/stakeholders"
```

**Output:**
- JSON in `output/brainstorm/problem_solution_spider/`
- Defined problem, constraints/resources, wild ideas, solution options, test scenario
- Logs with token/cost estimates in `logs/`

---

## Health Tools

### 🔬 Medical Consensus Parser
*Coming soon*

Parse research studies with built-in skepticism and synthesis.

---

## New Additions (Policy, Politics, Strategy, Geo, Marketing)

### 📋 Campaign Promise Tracker
- Usage: `python tools/politics/campaign_promise_tracker.py "Speech/manifesto text"`
- Output: `output/politics/campaign_promise_tracker/` — promises, feasibility/blockers, verification hooks

### 🐖 Bill Pork Barrel Finder
- Usage: `python tools/policy/bill_pork_barrel_finder.py "Bill text or summary"`
- Output: `output/policy/bill_pork_barrel_finder/` — pork items, beneficiaries/payers, red flags

### 🏛️ Regulatory Capture Mapper
- Usage: `python tools/policy/regulatory_capture_mapper.py "Agency/industry description"`
- Output: `output/policy/regulatory_capture_mapper/` — capture signals, incentives, mitigations

### 🔒 Platform Lock-in Forensics
- Usage: `python tools/strategy/platform_lock_in_forensics.py "Platform description"`
- Output: `output/strategy/platform_lock_in_forensics/` — lock-in mechanisms, switching costs, mitigations

### 🧩 Coalition Fracture Simulator
- Usage: `python tools/strategy/coalition_fracture_simulator.py "Describe the coalition"`
- Output: `output/strategy/coalition_fracture_simulator/` — fault lines, triggers, scenarios, mitigations

### 🛰️ Proxy War Analyst
- Usage: `python tools/geopolitics/proxy_war_analyst.py "Conflict description"`
- Output: `output/geopolitics/proxy_war_analyst/` — actors/objectives, escalation paths, off-ramps

### 🌌 Emergence Simulator
- Usage: `python tools/research/emergence_simulator.py "System description"`
- Output: `output/research/emergence_simulator/` — agents/rules, emergent behaviors, experiments

### 📈 Goodhart's Law Predictor
- Usage: `python tools/strategy/goodharts_law_predictor.py "Metric description"`
- Output: `output/strategy/goodharts_law_predictor/` — gaming strategies, unintended outcomes, mitigations

### 🧪 Viral Hook Laboratory
- Usage: `python tools/marketing/viral_hook_laboratory.py "Product/message"`
- Output: `output/marketing/viral_hook_laboratory/` — hooks, risk/ethics analysis, guardrails

### 🌾 Astroturf Detector
- Usage: `python tools/media/astroturf_detector.py "Thread/post text"`
- Output: `output/media/astroturf_detector/` — signals, likely origin/motives, verdict

### 🧠 Consensus Manufacturing Detective
- Usage: `python tools/media/consensus_manufacturing_detective.py "Campaign text"`
- Output: `output/media/consensus_manufacturing_detective/` — frames, omissions, beneficiaries, counter-frames

### 🛡️ Narrative Warfare Analyst
- Usage: `python tools/media/narrative_warfare_analyst.py "Narrative summary or quotes"`
- Output: `output/media/narrative_warfare_analyst/` — narratives, techniques, counters, monitoring

### 🎭 Corporate Theater Director
- Usage: `python tools/culture/corporate_theater_director.py "Describe the ritual/town hall/email"`
- Output: `output/culture/corporate_theater_director/` — performative moves, incentives, honest alternative

### 🎓 Credential Inflation Analyzer
- Usage: `python tools/career/credential_inflation_analyzer.py "Job/role description"`
- Output: `output/career/credential_inflation_analyzer/` — inflation signals, skill substitutes, advice

### 🧭 Ideological Consistency Test
- Usage: `python tools/psychology/ideological_consistency_test.py "Stated beliefs text"`
- Output: `output/psychology/ideological_consistency_test/` — claims/premises, contradictions, behaviors, self-test

### 🧠 Subject Connector
- Usage: `python tools/learning/subject_connector.py "Subject A" --context "Subject B"`
- Output: `output/learning/subject_connector/` — connections, importance, project idea

### 🎭 Character Evolution Engine
- Usage: `python tools/writing/character_evolution_engine.py "Character type" --context "Genre, tone, constraints"`
- Output: `output/writing/character_evolution_engine/` — arc with flaw, challenge, growth, new adventure

### 🧪 Historical What-If Machine
- Usage: `python tools/history/historical_what_if_machine.py "What if..." --context "Lens/constraints"`
- Output: `output/history/historical_what_if_machine/` — branch point, ripple effects, caveats/hooks

### 📊 Symptom Correlator
*Coming soon*

Find patterns in health logs and propose experiments.

### ⚖️  Protocol Decision Matrix
*Coming soon*

Evaluate new interventions with risk-adjusted framework.

---

## Cognitive Tools

### 🎯 Advocacy Prep
*Coming soon*

Prepare for important conversations (doctor appointments, business calls).

### 🔓 Blocker Breaker
*Coming soon*

Break through when feeling stuck on projects.

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
  "health_context": {
    "condition": "Your situation",
    "priorities": ["Your health priorities"]
  }
}
```

### 2. Ensure API Access

Tools use the same `.env` setup as the main framework:
```bash
# Should already be configured if demos work
OPENROUTER_API_KEY=your_key_here
OPENROUTER_MODELS="openai/gpt-3.5-turbo,google/gemini-flash-1.5,google/gemini-pro-1.5"  # Optional: override model list for FusionChain
RUN_FUSION_CHAIN=0  # Optional: enable multi-model demo (uses more calls)
```

### 3. Run a Tool

```bash
python tools/content/evergreen_guide.py "Test topic"
python tools/research/timeline.py "Test topic"
```

---

## Output Structure

```
output/
├── guides/               # Guide outlines
│   └── 20241203-1430-topic.md
├── health/              # Health analysis
│   ├── research/
│   ├── experiments/
│   └── protocols/
└── prep/                # Conversation prep docs
    └── appointment-2024-12-03.md
```

---

## Energy Cost Reference

| Tool | Setup | Usage | Value | Net ROI |
|------|-------|-------|-------|---------|
| Evergreen Guide | 0min | 2min | 2hrs saved | +++ |
| Medical Consensus | 0min | 3min | Hours of research | +++ |
| Symptom Correlator | 5min* | 2min | Pattern insights | ++ |
| Advocacy Prep | 0min | 10min | Confidence++ | ++ |
| Blocker Breaker | 0min | 5min | Restart work | +++ |

*One-time setup to create log format

---

## Development Guidelines

### When Adding New Tools

1. **User Context**: Load `context/user_profile.json` automatically
2. **CLI-First**: Accept input via args or stdin
3. **Output Structure**: Save to appropriate `output/` subdirectory
4. **Error Handling**: Graceful degradation, partial value
5. **Energy Test**: Can you use it at 50% capacity?
6. **Cost Visibility**: Include usage stats in logs; summarize with `python tools/cost_report.py`

### Tool Template

```python
#!/usr/bin/env python3
"""
Tool Name

Brief description of what it does and why.

Usage:
    python tools/category/tool.py "input"
    cat file.txt | python tools/category/tool.py
"""

import sys
import os
import argparse
import json

# Standard project setup
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from chain import MinimalChainable
from main import build_models, prompt

def load_user_context():
    """Load user profile for context-aware generation"""
    # Standard implementation
    pass

def tool_main(input_data, additional_context=""):
    """Main tool logic"""
    # Load context
    user_profile = load_user_context()

    # Build chain
    # Execute
    # Save output
    # Print summary
    pass

def main():
    # CLI argument handling
    pass

if __name__ == "__main__":
    main()
```

---

## Feedback Loop

Track which tools you actually use:
- **Using weekly**: Keep and improve
- **Using monthly**: Good, maintain
- **Haven't used in 2 weeks**: Archive or delete

Better to have 3 great tools than 10 mediocre ones.

---

## Support

Issues: File in project root issue tracker
Questions: See main project README

---

**Tools that feel like extensions of your mind, not external systems to manage.**
