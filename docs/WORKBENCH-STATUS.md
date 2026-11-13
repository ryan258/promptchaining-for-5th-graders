# Workbench status

The implemented local workflow is recipe → intention → saved run → reviewed steps → reusable output. The original framework remains available through Advanced. This status distinguishes implementation and offline checks from owner acceptance.

## Implemented

- Nine editable recipes, including three take-home projects, and a blank-chain editor. A four-step authored Moon example works offline.
- Six classroom challenges and three professional practice cases with authored answers and editable handoffs. [Classroom challenges](DEMOS.md#try-it-with-a-class) · [Professional practice](PROFESSIONAL-CASES.md)
- A saved offline dragon challenge lets students choose a job, see two earlier answers in the final prompt, and compare prepared answers for the two choices. [Dragon challenge walkthrough](DEMOS.md#build-the-next-prompt)
- Chain Lab offers four offline missions and a build-your-own option. Students write prompts, choose handoffs, save human answers, and remix a saved chain while keeping the original. [Chain Lab walkthrough](DEMOS.md#build-your-own-chain-in-chain-lab)
- Saved inputs, browser draft recovery, review pace, 1–8 named steps, keyboard shortcuts and ordinary dictation-compatible fields.
- SQLite checkpoints, one runtime owner, stale-tab checks, explicit starts/retries, pause after the active step, original-answer retention and interruption recovery.
- Paged run search, current and archived views, resume notes, checkpoint forks, and reusable recipe snapshots.
- Final-answer Markdown, inspection trace Markdown, single-run JSON, explicit final-artifact handoff, and additive workspace backups. Restore bounds the upload before parsing the archive.
- Live answer checkpoints include model settings per attempt and provider usage and provenance where available. A failed checkpoint can be retried as a local save without requesting another answer.
- In-app Guides sourced from the existing Markdown, with local section search, copyable blocks, downloads, and contextual help.
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

The November 11 harmony pass exercised the workbench, request boundary, Guides, portable framework, artifact library and MS draft tools in targeted offline test groups. The offline demo smoke check completed the Moon walkthrough, all three professional cases and a portable chain. The local setup diagnostic and syntax checks passed. [Verification commands](TESTING.md)

On October 25, 2026, the repair group passed **129 targeted offline tests** across the workbench, routes, Guides, provider client, chain engine, composer, meta-chain and enhancement modules. `./pc doctor`, shell and JavaScript syntax, local documentation links, and Git whitespace checks also passed for that snapshot. See [Testing](TESTING.md) for current scoped commands.

Historical pre-repair groups reported 54 workbench/framework checks and 44 Guides/route checks; those counts describe earlier snapshots rather than current whole-project acceptance.

Regression data is temporary. Library tests redirect default artifact storage so checks do not write to the owner's saved artifact library. Provider responses are substituted. See [Testing](TESTING.md) for scoped commands and [Architecture](ARCHITECTURE.md) for the contracts.

## Acceptance boundary

Ryan reserved full-suite checks, browser testing and commits. No live model requests, browser pass, screen-reader or voice-control acceptance, staging, commits, pushes, deployment or publication are part of this repair. Local setup checks do not establish current model availability, account credit or output quality.

Archives accept at most 128 JSON parts, 128 MB compressed and 256 MB expanded. Each JSON part accepts 10 MB and 2,000 recipes/runs. Browser drafts, `.env`, legacy artifacts and logs remain outside workspace backups. Per-file atomic artifact replacement is not a transaction across an entire legacy chain. Generated content requires human judgment.

## Review and policy evidence

The October review used the index at `65cfd55`. The November review opened the owner-supplied index at `675857d` for a bounded look at the request boundary and backup flow. Current worktree changes were verified through source and offline tests.

Shared human policy remains canonical. Generated GitNexus directives were removed from active agent guidance, and the six supplied skill copies were preserved outside active skills under `.claude/retired-gitnexus/`. The owner index was preserved. This is a local policy alignment, not a change to shared Cyborg policy or global integrations.

## Resume

Run `./pc`, then open `http://127.0.0.1:8000`. Try the authored example, inspect Guides, or return to a saved run. Use `./pc backup` for a new ZIP copy and `./pc restore FILE` for additive import. See [Saving and recovery](SAVING-EXPORT-AND-RECOVERY.md) for limits and fallback folder copies. Optional enhancements remain in [ROADMAP.md](../ROADMAP.md).
