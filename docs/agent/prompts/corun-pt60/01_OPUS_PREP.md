# Chain prompt 1 — prep (game closed; no owner time)

**Read `README.md` first — binding chain rules apply.** Staleness check, todo
list (live, one item per commit-and-verify unit). Everything you produce is
committed BEFORE the owner sits down; nothing lands in `Code/` until the
sitting (probe hygiene rule 5).

## Read path (files, not folders)

`archive/PLAYTEST_ARCHIVE.md` § "PT-60 — The chain-8b batch leg" (~line 3822,
the WHOLE section incl. "What this leg does NOT cover" and "Steps") ·
`agent/bugs/F90.md`–`F96.md` · the conversion commits (`git show 69c02b9` etc.,
README list) · `agent/bugs/F57.md` + `F29.md` (P9 and SequenceLatents routes) ·
`agent/WORKFLOW.md` "Co-runs" (all four harness-rule stacks) ·
`docs/PLAYTEST_HELP.md` (verified command table; loggers) ·
`agent/facts/EF-051.md` (the cloud-ON hold) · indexes for anything further.

## Jobs

**Job 1 — re-derive the prediction set for today's build; the 08-02 content
is the record, your numbers are the annotation.** For each of P1–P9 (archive
section): keep the prediction verbatim, attach today's expected reading with
provenance, and name the exact instrument line that will read it. Musts:

* P1: expected registered/active counts read from `metadata.lua` + the
  ListFixes convention — never from defaults (that was P1's own 08-02 miss).
  Today's baseline: 81 registered / 74 default-active; active depends on the
  owner's opt-in toggles — predict the registered half, READ the active half.
* P2/P3: confirm the five new modules and the seven converted modules still
  exist under the archived names (vs `Code/`); note F29 items 1+3 share
  `SequenceLatents`.
* P4/P5: probe total today is 87 with **eight retail `[install]` SKIPs** —
  enumerate which of the seven new probes RUN on retail and which SKIP, from
  the TestKit source, so the sitting predicts verdicts only for runnable ones.
* P8: verify the three heal lines' CURRENT wording against module source
  (`TrackSalvageWipe` shell heal, `SaintBlessing` re-base,
  `AstrogeologistExtractors` bonus heal) — the sitting greps the archived log
  for these exact strings. ⚠️ Distinguish boot-time preset heals (fire every
  launch) from save-state heals (fire on the pre-batch save's first load);
  the corun-pt15 log (`docs/archive/cp15sitting_…15.09.30.log` L176-L182)
  shows the boot-time class firing on an unrelated save — a P8 read that
  counts those as save heals is wrong.
* P9: re-derive the exact console read for `SMRFixPack_rocket_fuel_key`
  absence from `DroneControl` (from `8f58f30` + Src), pre-flighted for thread
  context (`*r` if it sleeps/yields — batch-2 rule 1).

**Job 2 — fixture.** Verify `USA Sol 302.savegame.sav` on disk (record MD5 +
LastWriteTime in the notes — it is protected file #4 from this moment). Stage
`CP60STAGE.savegame.sav` via `Copy-Item`, verify MD5-identical. ⚠️ The
lineage claim (owner campaign, pack on, written pre-batch) is CONFIRMED AT THE
GATE by reads (map, sol, module count), never assumed. Note for the record:
a `Copy-Item` byte-copy has the same metadata shape as a Cloud restore
(EF-051) — and the cloud is ON, so say which files you created and when.

**Job 3 — instruments.** Resurrect corun-pt15's harness
(`git show f289b11:docs/agent/prompts/corun-pt15/97_CP15Common.lua.txt` and
`…/98_CP15Sitting.lua.txt`), adapt to `CP60`, park as
`97_CP60Common.lua.txt` + `98_CP60Sitting.lua.txt` + `CP60_ARM.ps1.txt` in
THIS folder. Keep: the gate that STOPS, `CP60.Load/SaveNamed` with the EF-050
verbatim-savename guard, `CP60.Note`, CLOCK lines, forced/organic labels.
Add: a `CP60.Fixes()` wrapper that relays `SMRFixPack.ListFixes()` through the
log, a `CP60.Suite()` wrapper for `*r SMRTest.RunAll()` likewise, and a
`CP60.P9()` read. Drop the mystery/trap legs. ⛔ Resolution cross-check
(used-vs-defined, one command) is part of the ARM script; the ARM GATE reads
`metadata.lua` and the probe files back OFF DISK and refuses to launch
unarmed. ⚠️ Loggers are cleared by every restart — the brief's first-action
list includes `SMRTest.Log.<name>(true)` re-arming if any logger is wanted.

**Job 4 — the sitting brief (append as prompt 2's `## Notes from upstream`).**
Measure-moments list with the owner's cost per moment; the priority queue
(decider first): ①load lands the P8 heal lines at zero owner cost → ②Fixes +
Suite vs the annotated predictions → ③save/reload + P9 → ④owner's 15–20 min
ordinary play (P6/P7) with riders opportunistic. Every owner-typed line
pre-flighted for thread context; the load mechanism is a named console line
(`CP60.Load("CP60STAGE.savegame.sav")` — staged copies are indistinguishable
in the in-game list). Name the rider preconditions the gate will read (trains
working? elevator built? passages trafficked?) so nothing is promised blind.
State the honest attended estimate: **~40–60 min** including console driving
(the 15–20 min of play is the floor, not the total — batch-1 rule 4).

**Job 5 — close.** The checklist PT-60 QUEUED banner exists (authoring
session, 2026-08-12) — update it only if prep changed the plan. doccheck
GREEN, commit (`PROBE SWEEP:` line), push, delete this file in the same
commit.

## Stop conditions

- Fixture fails job 2 → fall back to `USA Sol 298`; both failing → stop,
  route to the owner, leave the chain intact.
- A prediction cannot be annotated without guessing → mark it DEGRADED with
  what is missing; the sitting reads what it can and the audit rules.

## ⛔ What you may not claim

- Nothing is "verified" by prep. You produce expectations and instruments.
- No count is written from defaults or memory — read the build.
