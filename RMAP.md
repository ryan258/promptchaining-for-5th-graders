# Prompt Chain Framework - Roadmap

> **Personal tool evolution**

Things I might build if they become useful. No timeline, no promises.

---

## Current State (v0.3)

**What works:**
- Sequential chains with context passing
- Parallel model comparison
- JSON response parsing
- Basic logging to markdown
- 31 working demo chains

**What's good enough:**
- Cost tracking (shows up in logs)
- Error handling (try/except, keep going)
- Variable substitution (`{{var}}` and `{{output[-1]}}`)
- Usage capture per prompt + markdown log with token/cost estimate
- FusionChain opt-in via `RUN_FUSION_CHAIN` to avoid surprise spend

---

## Immediate Next Steps (keep it light)

- [x] Harden prompt helper defaults everywhere (explicit `max_tokens`, deterministic temp when desired) — audit any stragglers beyond `main.prompt`
- [x] Wrap FusionChain ordering bugfix with a quick regression test (model name/output alignment) so it doesn't regress
- [x] Refresh `tools/README.md` with current tool list + `OPENROUTER_MODELS` env override and Fusion opt-in flag
- [ ] Finish cost report rollup from logs (simple aggregator script)
- [ ] Keep logs/outputs under control (prune or rotate; local only so just a reminder)

---

## If Needed Later

### Performance
- [ ] **Async execution** - If chains get slow
- [ ] **Response caching** - If hitting same prompts repeatedly
- [ ] **Streaming responses** - If want to see output as it generates

### Reliability
- [ ] **Retry logic** - If API calls fail too often
- [ ] **Better error messages** - If debugging becomes annoying
- [ ] **Resume from checkpoint** - If long chains fail midway

### Usability
- [ ] **Better logging** - If current logs aren't useful enough
- [ ] **Cost limits** - If accidentally burning money
- [ ] **Chain templates** - If making similar chains repeatedly

### Tools
See `RMAP-CS.md` for cognitive exoskeleton tool roadmap.

---

## Probably Won't Build

- Docker/Kubernetes deployment
- Multi-tenancy
- Enterprise auth (OAuth, SAML)
- Distributed tracing
- Prometheus metrics
- GraphQL API
- Load balancing
- Any "scale" features

This is for local dev, not production services.

---

## Next: Demo → Tool Conversion Pattern

### Exemplar: Knowledge Time Machine → Research Timeline Tool

**Source**: `demos/knowledge_time_machine/main.py`
**Target**: `tools/research/timeline.py`

**Why this one first:**
- Already traces concept evolution (origins → current → future)
- Clear transformation path from kid-friendly to research-grade
- Good template for converting other demos

**Conversion Plan:**

1. **Strip kid explanations** - Remove comment cruft
2. **Add CLI + multi-line input** - Same pattern as evergreen_guide
3. **Adult-focused prompts**:
   - Historical origins → Include contradicting theories, uncertain attributions
   - Evolution points → Breakthrough moments with impact assessment
   - Current state → Frontier research, unresolved questions
   - Future → Expert speculation + risks/limitations
4. **Output format**: Research-grade markdown
   - Proper citations format
   - Uncertainty indicators
   - Research gaps highlighted
5. **Context loading** - Pull user profile preferences

**Expected Usage:**
```bash
python tools/research/timeline.py "CRISPR gene editing"
# or
python tools/research/timeline.py --editor
```

**Success criteria:**
- Would actually use for research/writing prep
- Output quality matches cognitive exoskeleton standards
- < 3 min runtime

**After this works:**
Use as template for converting other demos → tools when needed.

---

## Exemplar Readiness (steelman check)

- **Research timeline** (`tools/research/timeline.py`): adult prompts, context loading, structured markdown + JSON logging, usage/cost captured. Good enough to copy for other research tools.
- **Evergreen guide** (`tools/content/evergreen_guide.py`): adult prompts, context-aware tone, structured outline + audit + log with usage. Good template for content tools.
- **FusionChain demo** (`main.py`): kept as opt-in showcase; retains max token/usage capture. Use as pattern only when multi-model competition is necessary (rare).

Verdict: Exemplars are sufficiently steelmanned for local use; no enterprise hardening needed. Reuse patterns, avoid overbuilding.

---

## Things to Consider Before Mass Conversion

### 1. Code Duplication
~100 lines of identical code in tools (load_user_context, open_in_editor, etc).
**Action**: Create `tools/tool_utils.py` to extract shared code.

### 2. Tool Discovery
31+ tools will be hard to navigate.
**Action**: Keep `tools/README.md` updated or add a simple listing script.

### 3. Output Organization
`output/` directory could get messy.
**Action**: Use consistent naming `output/{category}/{tool_name}/`.

### 4. Cost Tracking
Need aggregate view of spending.
**Action**: Implement `tools/cost_report.py`.

### 5. User Profile Complexity
Different tools need different contexts.
**Action**: Consider `context/profiles/` for specific needs later.

### 6. Quality Checking
Not all demos are useful tools.
**Action**: Triage demos before converting (Must-have vs Nice-to-have).

### 7. Batch Operations
Chaining tools together.
**Action**: YAGNI for now.

### 8. Documentation Drift
`tools/README.md` will get stale.
**Action**: Commit to updating it (discipline tax).

---

## Recommendations (Priority Order)

- [x] Cost-tracked logging to markdown
- [x] Basic error handling
- [x] Environment variable configuration
- [x] Refactor `tools/tool_utils.py` for DRY
- [x] Create `tools/cost_report.py` utility
- [ ] Tool triage - Which demos are worth converting? (~30 min)

---

## Current Priorities

1. **Knowledge time machine tool** - Prove the demo→tool pattern works
2. **Cognitive exoskeleton tools** (`tools/`) - Only build what directly helps output
3. **Fix annoying bugs** - As they come up
4. **Add features when blocked** - Only when current approach doesn't work

If it ain't broke, don't fix it.

---

**Keep it simple. Add complexity only when pain is real.**

---

## Tool Triage Status

| Demo Name | Status | Notes |
|-----------|--------|-------|
| `astroturf_detector` | Maybe | Useful for media analysis |
| `bill_pork_barrel_finder` | Skip | Too specific |
| `campaign_promise_tracker` | Skip | Too specific |
| `character_evolution_engine` | Done | Tool: `tools/writing/character_evolution_engine.py` |
| `coalition_fracture_simulator` | Maybe | Advanced analysis |
| `code_architecture_critic` | Done | Tool: `tools/dev/code_architecture_critic.py` |
| `common_ground_finder` | Done | Tool: `tools/collaboration/common_ground_finder.py` |
| `concept_simplifier` | Done | Tool: `tools/learning/concept_simplifier.py` |
| `consensus_manufacturing_detective` | Maybe | Media analysis |
| `corporate_theater_director` | Skip | Satire |
| `credential_inflation_analyzer` | Skip | Niche |
| `crisis_opportunity_scanner` | Done | Tool: `tools/strategy/crisis_opportunity_scanner.py` |
| `diplomatic_subtext_decoder` | Done | Tool: `tools/strategy/diplomatic_subtext_decoder.py` |
| `dream_job_reverse_engineer` | Done | Tool: `tools/career/dream_job_reverse_engineer.py` |
| `emergence_simulator` | Maybe | Abstract |
| `euphemism_decoder` | Done | Tool: `tools/media/euphemism_decoder.py` |
| `goodharts_law_predictor` | Done | Tool: `tools/strategy/goodharts_law_predictor.py` |
| `historical_what_if_machine` | Skip | Entertainment |
| `ideological_consistency_test` | Maybe | Self-reflection |
| `knowledge_time_machine` | Done | `research/timeline.py` |
| `media_bias_triangulator` | Done | Tool: `tools/media/media_bias_triangulator.py` |
| `meeting_dynamics_forensics` | Done | Tool: `tools/career/meeting_dynamics_forensics.py` |
| `narrative_warfare_analyst` | Maybe | Advanced |
| `negotiation_strategy_builder` | Done | Tool: `tools/business/negotiation_strategy_builder.py` |
| `platform_lock_in_forensics` | Skip | Niche |
| `problem_solution_spider` | Done | Tool: `tools/brainstorm/problem_solution_spider.py` |
| `proxy_war_analyst` | Skip | Niche |
| `regulatory_capture_mapper` | Skip | Niche |
| `revealed_preference_detective` | Done | Tool: `tools/psychology/revealed_preference_detective.py` |
| `status_game_decoder` | Done | Tool: `tools/social/status_game_decoder.py` |
| `subject_connector` | Done | Tool: `tools/learning/subject_connector.py` |
| `viral_hook_laboratory` | Skip | Marketing (maybe) |
