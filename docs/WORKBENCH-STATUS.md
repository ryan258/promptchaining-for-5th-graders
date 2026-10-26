# Workbench status — October 25, 2026

The implemented local workflow is recipe → intention → saved run → reviewed steps → reusable output. The original framework remains available through Advanced. This status distinguishes implementation and offline checks from owner acceptance.

## Implemented

- Six editable recipes, a blank-chain editor and a four-step authored Moon example requiring no model requests.
- Saved inputs, browser draft recovery, review pace, 1–8 named steps, keyboard shortcuts and ordinary dictation-compatible fields.
- SQLite checkpoints, one runtime owner, stale-tab checks, explicit starts/retries, pause after the active step, original-answer retention and interruption recovery.
- Run search, reuse, Markdown and single-run JSON export, explicit final-artifact handoff, and additive workspace backups.
- Twenty in-app Guides sourced from the existing Markdown, with local search, section links, copyable blocks, downloads and contextual help.
- Loopback startup through `./pc`, vendored HTMX, local fonts, escaped text, origin checks, focus and reduced-motion rules.

## Harmony repairs

- Advanced provider/subprocess work is delegated to `lib/advanced.py` through worker threads; setup failures use recoverable errors and raw provider payloads are omitted.
- Artifact files publish atomically, unreadable records are skipped without changing the source, and FusionChain gives parallel models separate namespaces.
- Every framework/workbench step makes one attempt. No nested transport or JSON-format retries remain. Depth/rounds accept 1–5; forms show request counts.
- Five Whys, Red vs Blue and meta fallback handoffs carry the intended prior answer. Framework substitution is one pass, including literal-placeholder quoting for design lessons.
- Default workspace backups are ZIP archives with importable JSON parts, checksums and complete-file validation before an additive transaction. Legacy JSON remains supported within its size/record limits; export enforces those limits as well.
- Composer totals and traces are independent per operation; unavailable tool usage is labelled incomplete. Costs are explicit estimates or unknown.
- Failed comparisons stop before later phases and are excluded from wins/ties. Scores are validated; excerpt limits and the absence of statistical testing are explicit.
- Legacy prompts separate observed evidence from hypotheses and illustrative scenarios. The prompt-card energy setting changes generation constraints.

## Local verification

The final repair group passed **129 targeted offline tests** across the repair regressions, workbench, routes, Guides, provider client, chain engine, composer, meta-chain and enhancement modules. `./pc doctor` passed without provider requests; shell and JavaScript syntax, local documentation links and Git whitespace checks passed. See [Testing](TESTING.md) for the exact scoped command.

Historical pre-repair groups reported 54 workbench/framework checks and 44 Guides/route checks; those counts describe earlier snapshots rather than current whole-project acceptance.

Regression data is temporary. Library tests redirect default artifact storage so checks do not write to the owner's saved artifact library. Provider responses are substituted. See [Testing](TESTING.md) for scoped commands and [Architecture](ARCHITECTURE.md) for the contracts.

## Acceptance boundary

Ryan reserved full-suite checks, browser testing and commits. No live model requests, browser pass, screen-reader or voice-control acceptance, staging, commits, pushes, deployment or publication are part of this repair. Local setup checks do not establish current model availability, account credit or output quality.

Archives accept at most 128 JSON parts, 128 MB compressed and 256 MB expanded. Each JSON part accepts 10 MB and 2,000 recipes/runs. Browser drafts, `.env`, legacy artifacts and logs remain outside workspace backups. Per-file atomic artifact replacement is not a transaction across an entire legacy chain. Generated content requires human judgment.

## Review and policy evidence

The owner supplied an index at commit `65cfd55`; pre-edit impact analysis identified broad logging, design and content-generator dependencies. Graph gaps in dynamic route and runner calls were checked directly. That index becomes stale as this repair changes source; it does not establish final graph clearance. No new analysis/reindex was run.

Shared human policy remains canonical. Generated GitNexus directives were removed from active agent guidance, and the six supplied skill copies were preserved outside active skills under `.claude/retired-gitnexus/`. The owner index was preserved. This is a local policy alignment, not a change to shared Cyborg policy or global integrations.

## Resume

Run `./pc`, then open `http://127.0.0.1:8000`. Try the authored example, inspect Guides, or return to a saved run. Use `./pc backup` for a new ZIP copy and `./pc restore FILE` for additive import. See [Saving and recovery](SAVING-EXPORT-AND-RECOVERY.md) for limits and fallback folder copies. Optional enhancements remain in [ROADMAP.md](../ROADMAP.md).
