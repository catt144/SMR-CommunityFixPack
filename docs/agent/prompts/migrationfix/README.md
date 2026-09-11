# `migrationfix` — mini chain: build the migration audit's code actions, then audit both the build and the audit

Authored **2026-09-11** by `smr-bugfixpack-cb` at the owner's instruction. **Staleness anchor: HEAD was `33b9f8e`.**
Two links, self-consuming (each prompt `git rm`s itself in its own close-out commit). The owner starts link 01 by
hand; link 02 follows it.

| # | file | model | job |
|---|---|---|---|
| 01 | `01_BUILD_opus.md` | Opus | Repair F59 (against the verified dossier, which is the report **plus** the re-derivation that found a second harmful caller); build F60's retirement as the report proposes, with its replacement trace written as falsifiable claims. |
| 02 | `02_AUDIT_fable.md` | Fable | Terminal adversarial backward QA. Grades the build, **and** surface-sweeps Astra's eight module verdicts — a logic check, not a re-run of the deep dive. **Holds the upload gate.** |

## The ordering that makes this safe

**01 build → 02 audit → owner uploads.** Not build → upload → audit. The owner's instruction was "build it as
Astra wrote it and audit after", and that is only safe while the upload sits behind the audit: a refuted build
then costs a revert instead of a release. Link 01 is told in its own text that it is the executor and not the
certifier, and link 02 is told it is the gate.

## The one place "as is" was overridden, and why

Astra's report proposes an **expedition-home exclusion** for F59. That covers one of the two harmful callers and
does nothing for the other — the manual-assign over-capacity route, desk-controlled 8/8 in
`tools/desk_f59_interact.py`, reachable by an ordinary player action, on both game branches. Building the
report's shape as-is would have shipped a fix leaving the more reachable harm in place, so link 01 builds against
`bugs/F59.md`'s last two sections instead. **F60 is built as the report proposes**, with link 02 as its check.

## What is NOT in this chain

The audit reviews eight modules but proposes only **two** code actions. The five PARTIAL rows (F51, F52, F53,
F58, F73) and F54 change what we **claim** on the fix list and the store card, not `Code/` — that is
`prompts/perma/PUBLIC_SURFACE_SWEEP.md`, and link 02 sweeps those verdicts for soundness so the sweep has
something trustworthy to work from. **F80 is capture-before-mitigate** and is not built here.

No status word in this chain is a playtest grant: `tested-attended` is the sitting's. The four-click in-play
receipt for F59 is in checklist **151** and in link 01's foot.

---

## HANDOFF

*(Link 01 appends its close-out here — disagreements first, then what it built as falsifiable claims, then what
it skipped by name, then the commands a fresh session must re-read, then the one thing it is least sure of.
Link 02 reads this section before anything else.)*

**Not yet run.**
