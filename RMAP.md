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

## Current Priorities

1. **Knowledge time machine tool** - Prove the demo→tool pattern works
2. **Cognitive exoskeleton tools** (`tools/`) - Only build what directly helps output
3. **Fix annoying bugs** - As they come up
4. **Add features when blocked** - Only when current approach doesn't work

If it ain't broke, don't fix it.

---

**Keep it simple. Add complexity only when pain is real.**
