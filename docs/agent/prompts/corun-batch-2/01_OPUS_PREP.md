# Chain prompt 1 — prep: cross-check the record, resurrect the instruments, confirm the fixtures, write an honest brief

**Read `README.md` in this folder first — binding chain rules apply.**
Unattended. Start with `git log --oneline -10` + `git pull`. Todo list up
front. You write the sitting's brief into `02_OPUS_SITTING.md` "Notes from
upstream", commit, and delete this file in the same commit.

**Read path**: this folder's README · `docs/agent/STATE.md` ·
`WORKFLOW.md` "Co-runs" (ALL of it — the 2026-08-05 attended rules are yours
to satisfy) · entries `F26`, `F99`, `F48` (2026-08-05 block), `C42`, `F21`,
`F85`-related checklist riders, `D07` (trigger E), `F35`/PT-35 · checklist
sections PT-47, PT-53, PT-35, popup riders · the batch-1 close record
(`SESSION_LOG.md` 2026-08-05) and its parked sources in git at `530df63`.

## Jobs

**Job 1 — ⛔ ARCHIVE CROSS-CHECK FIRST (the S7 repair, now a binding rule).**
For EVERY entry and PT this chain briefs (F26/PT-47, D07/PT-53, F35/PT-35,
C42, F21, F99, the popup riders): verify the entry's status against
`PLAYTEST_ARCHIVE.md` and the checklist BEFORE writing a brief line. Batch-1
shipped a false SKIP because D07's entry was 5 days stale against the archive
and nobody checked. A contradiction found → correct the entry visibly (chain
rule 5) and brief from the corrected state.

**Job 2 — resurrect the instruments; do not rewrite.** Batch-1's parked
sources carry the pre-flight fixes and die-hard lessons:
`git show 530df63:docs/agent/prompts/corun-batch-1/97_CB1Common.lua.txt`
(likewise `98_…`, `99_…`, `CB1_ARM.ps1.txt`). Park them HERE as `.lua.txt` /
`.ps1.txt` (⚠️ the `.ps1` needs a BOM — S3; and scripted rewrites use
`[System.IO.File]` + `UTF8Encoding($false)`, never bare
`Get-Content`/`Set-Content`). Then ADAPT for this payload:
- Drop the batch-1 legs that already ran (leg 1/PT-37, leg 3/PT-42, leg 4
  pickers) — dead instrument code is context burned in the sitting.
- **Leg-2/PT-47 instruments survive with their S1 fix** (the watcher that
  walks every city, not `MainMap`) — verify the fix is present, then verify
  RESOLUTION (used-vs-defined names, one command) and parse, both gates.
- **NEW instruments this chain needs — each obeys the mid-chain instrument
  rule (a named liveness witness, printed `pcall`, type-checked inputs, a
  settling window on anything that could read a transient):**
  - C42: a traversal-witness poller (`passage.elements[*].units` non-empty at
    speed, bounded tries, witness printed) + the within-session `C42STALE`
    read gated on that witness.
  - Leg Q: a break-witness reader per element (`broken` truthy / repair site /
    `repair_cgs` — el.broken is a TABLE, not a boolean), a
    two-or-more-DISTINCT-tracks confirm before the completion, and a `:805`
    watch line.
  - Leg P: nothing beyond the log watch — say so rather than tooling for
    tooling's sake.
  - Leg S/T: the SAVE primitive is PROVEN (envelope) — reuse the batch-1 save
    helper lines as parked.
- **Subject-finder per moment (the S2 repair):** every owner moment in the
  brief names the instrument that FINDS its subject (which popup, which
  turbine spot class, which track elements for leg Q, where the Mod-Manager
  row is), and you CONFIRM each subject exists on the staged copy during the
  confirm cycle. A moment whose subject cannot be found by an instrument does
  not go in the brief — it routes.

**Job 3 — the F21 reader gap (bounded).** Batch-1 read `spent_time=nil` on
every sampled train. From Src, determine where the platform-wait penalty
actually lives on this build (field, object, or superseded by the Tier-2
rewrite — `F21.md` + `Fix_TrainWaitTime`'s own code are the map). Solved →
one read line in the brief; not solved within a bounded effort → the brief
says `SKIP <reader gap, where you looked>` and the rider keeps it. Do not
let this job eat the session — it is the cheapest item here.

**Job 4 — confirm cycle on a staged copy** (game closed → `Copy-Item` →
ARM GATE → launch → reads only → close): every fixture read (popup
availability, track counts for leg Q, PT-47's target area, Mod Manager
reachability is NOT confirmable from console — say so and leave it a hands
moment), zero mutations, log archived `git add -f`. Every zero states its
sampled condition.

**Job 5 — write the brief into `02_OPUS_SITTING.md` "Notes from upstream":**
run order per the README's simplest-first rule; measure-moments list with
per-moment minutes AND the console-driving overhead stated separately
(S6 rule — the owner types every line; the estimate that ignores this is the
estimate batch-1 broke); predictions numbered and falsifiable, each with its
falsifier named; SKIP lines with their live-confirmed reasons; card skeletons;
your own ledger (numbered, so the audit can diff it against batch-1's 8).

## ⛔ What you may not claim

- Not that a parked instrument works because it parses — resolution AND parse
  gates, and the sitting still treats first executions as first executions.
- Not that `StartBombard`'s recipe is good — Src-verify again on THIS tree,
  and the sitting runs it under `pcall` with the result printed regardless.
- Not any minutes estimate that excludes console driving.
- Nothing about F99 reachability — leg Q samples a cell, forced both halves.

## Stop conditions

- A fixture confirm fails → `SKIP <reason>` in the brief, sitting runs the
  rest; two or more core legs dead → route to the owner before scheduling.
- Context runs short → self-split at a clean commit boundary (rule 4); the
  brief's written state is the handoff.

## Notes from upstream

*(Empty — this is the first prompt. The chain author's only note: the owner
asked for this chain on 2026-08-05 and the ordering rule in the README is
their design input, verbatim.)*
