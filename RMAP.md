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

## Current Priorities

1. **Cognitive exoskeleton tools** (`tools/`) - These directly help output
2. **Fix annoying bugs** - As they come up
3. **Add features when blocked** - Only when current approach doesn't work

If it ain't broke, don't fix it.

---

**Keep it simple. Add complexity only when pain is real.**
