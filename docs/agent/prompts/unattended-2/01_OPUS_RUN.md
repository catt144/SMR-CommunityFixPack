# Chain prompt 1 — build the decided batch, verify it all in one launch

**Read `README.md` in this folder first — binding chain rules apply.**
Unattended; the owner has gone to bed — route, never wait. Start with
`git log --oneline -10` + `git pull`. Todo list up front, updated per item.

**Read path (before any edit):** `agent/bugs/F48.md` (the 2026-08-11 SHIP
block AND the 2026-08-05 PT-37 evidence block) · `C43.md` (the option-2
block) · `F100.md` (the reason-string block) · `F35.md` (fixture contents) ·
the checklist's PT-35 section · `WORKFLOW.md` "Co-runs" harness rules +
R4/R7 · `FIX_POLICY.md` · facts EF-014/047/048/049 · the existing
`Code/Fix_SaveSanitizer.lua` and TestKit `Code/00_TestCore.lua` +
`50_Probes_Wave5.lua` · batch-2's parked instrument sources
(`git show 7110384:docs/agent/prompts/corun-batch-2/99_CB2Legs.lua.txt` — the
PT35 reader and the SAVE/LOAD primitives) and batch-1's
(`git show 530df63:docs/agent/prompts/corun-batch-1/99_CB1Legs.lua.txt` — the
PT-37 case-A connection reader). **Resurrect instruments; do not rewrite.**

## Job 1 — the three builds (game closed; parse sweep after each)

**1a · F48 — the corrected pass into the sanitizer.** Re-derive from the
entry: the shipped fixup calls
`ProcessTrackElements(ResolveMap(track, track.elements))` — paren misplaced,
`Station.lua:1346` — and no-ops; the correction is
`ProcessTrackElements(ResolveMap(track), track.elements)`. Src-verify the
site and the callee signature FIRST (Src path: README rule 13; F48's F99-era
evidence proved the corrected call runs safely on live tracks — 280 elements,
never emptied the list). Implement per FIX_POLICY's cheapest applicable
technique as a sanitizer pass; the F86-era heal-family conventions apply
(one-shot, logged by name, idempotent — a second run repairs nothing and
says so). ⚠️ The pass must print a per-repair count line (R7 needs an effect
reading, and PT-35's do-no-harm reads must be able to see a ZERO on clean
saves).

**1b · C43 — restrict `set_global` (TestKit only).** `00_TestCore.lua`:
`set_global` may REPLACE an existing global but never create one; on a
missing target it returns a sentinel the caller can read. The two Wave-5
probes stubbing `IsNearDome` / `AddAreaRubble` print
`SKIP <stub target undeclared on this build>` when that happens, instead of
PASSing over a stub the engine rejected. **Also count** (grep, record on the
entry) how many OTHER probes call `set_global` — the entry's noted gap — and
whether any other caller can hit the undeclared case.

**1c · F100 — the reason string.** The first-pass deactivation line for
`Opt_NoHomeless` states the recorded truth (authoring-error self-check, class
not built on first pass per EF-001, module applies cleanly on pass two) —
NOT a "game update changed the mixin?" guess. Touch only the string(s); the
`Require` target and self-check semantics stay exactly as they are.

## Job 2 — the launch: one process verifies everything

Stage a COPY of `PT35FIXTURE.savegame.sav` (game closed, `Copy-Item`, note
MD5) — the fixture itself is never written. ARM gate, launch, load the copy
by filename. Then, banked incrementally (a card per item the moment it
completes):

1. **Fixture confirm** (stop condition 3 if it fails): FrictionlessComposites
   `researched` truthy, `discovered` truthy (⛔ numbers, not booleans —
   EF-048), 1 `WindTurbine_Large`, the Remote Medic upgrade present on the
   Hospital.
2. **F100 read** — the boot log carries the NEW line and `81/81 active`.
3. **PT-35 leg A, turbine half** — the sanitizer's do-no-harm reads with a
   REAL subject at last: every heal-family read (incl. `RepairTurbineBuff`
   over population=1 and `RepairLeakedUpgradeModifiers` over the applied
   Remote Medic) before and after **save + reload ×2** (R4). The entry's own
   claim is the acceptance: **the read-back numbers do not change across
   loads and no heal line fires on a healthy fixture.** APPLICABLE=true this
   time — say so; that is the whole point of the fixture.
4. **F48 acceptance** — build the case-A state deliberately on this staged
   copy (the batch-1 route: a witnessed `CheatBreakElement` break + repair,
   or the stale-connection producer PT-37 used — re-derive from F48.md's
   2026-08-05 block; the reader is the parked CB1 connection-count
   instrument). Readings required, each with its R4 round trip: (a) the
   SHIPPED pass repairs the staged state — connection count moves to the
   clean-chain value and STAYS there across save+reload; (b) on the
   already-clean fixture the pass reports ZERO repairs (do-no-harm); (c) the
   pass's own log line prints its count (R7). ⛔ If (a) or (b) fails →
   stop condition 1: revert, record, route.
5. **C43 acceptance** — full `SMRTest.RunAll()`: ZERO `[LUA ERROR]` lines
   from TestKit code in the final archived log, the two probes report SKIP
   (not PASS) wherever the target is genuinely undeclared, and every other
   probe's verdict is UNCHANGED from the last suite baseline (any flip is a
   finding, not a shrug).

⛔ Every save witnessed by on-disk bytes + load-back (EF-049). ⛔ Absence
claims (zero errors, zero heal lines) are read from the FINAL archived log
after process exit (EF-047), never mid-session. Whole-log review before
recording: every unexplained line reported with its age; grep for
`TrackElement.lua:805` (F99 passive watch) and `invalid pos with no holder`
(C45 — a second occurrence outside a bombardment window is exactly what its
entry is waiting for).

## Job 3 — record and hand off

Entries carry their results (F48 → `fixed` ONLY if 4a-4c all held, with the
readings verbatim; C43/F100 status per honest outcome; F35/PT-35 checklist
line + entry; each card names FORCED vs ORGANIC — everything here is
forced/staged, no `tested` anywhere). SESSION_LOG record newest-first; STATE
updated (cap 60); checklist PT-35 line updated. Close-out: probes deleted in
the recording commit, `PROBE SWEEP:` line, both trees clean, **save-dir
listing** (staged copies gone; `PT35FIXTURE` + `TEST2H TRAIN` present and
byte-verified), logs archived `git add -f` + `cmp`-verified, doccheck GREEN,
push. Append the outbox to `02_FABLE_AUDIT.md` "Notes from upstream" —
run conditions, every card verbatim, the ledger of your own misses (0 of them
the game's fault is the expected shape; say what actually happened) — and
delete this file in the same commit.

## Stop conditions

README's chain-wide list. An honestly-recorded partial beats a rushed
complete: any item that cannot meet its acceptance is recorded as exactly
what it is and routed.
