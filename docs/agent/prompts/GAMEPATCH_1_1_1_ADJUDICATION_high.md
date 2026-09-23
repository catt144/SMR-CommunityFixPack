# Adjudicate the 1.1.1 triage — full-body replacements first

One-off adjudication brief. The 1.1.1 game-patch triage landed as `c7266f0`
("Game patch: triage 1.1.1 and queue follow-up work"): one report, five filings
(F121–F125), two follow-up briefs, a checklist pair, and a `bodycheck.py` self-test
change. `d45655c` ("Record 1.1.1 retail audit legs") then folded in the owner's
completed retail A/B: it cleared the Open Pasture gate, upgraded F123 to a measured
pack-on result, removed the spent checklist leg, and renumbered the surviving limits
item to **ck207**. Neither commit has been adjudicated. This brief is that
adjudication, and `d45655c` is in its scope exactly as `c7266f0` is.

The owner has settled the ordering (2026-09-23): **full-body replacements are the
critical path and go first.** Phase A produces and commits a full-body priority report
and messages the orchestrator before Phase B touches anything else. Do not reorder the
phases, and do not fold Phase A's findings into a single combined report at the end —
the owner is waiting on Phase A to start work while Phase B is still running.

This brief was authored from `d45655c`. Start with `git log --oneline -3`, `git pull`,
and `git status --short`; if HEAD has moved, re-derive every line number and SHA below
before use. All cited line numbers are leads and must be re-derived with `rg -n` or
`grep -n`. Invoke `doc-editing` before record edits and `smr-bug-library` for any
status or evidence change. Apply `CLAUDE.md`, `docs/agent/WORKFLOW.md`, and
`docs/agent/FIX_POLICY.md`.

Both commits were produced by one seat and this audit must run on another: execution and
audit use different owner-selected seats, and no unattended result enters the record
unaudited. You are adjudicating another seat's work — judge it on the diff and the
archived source, never on its report's own summary of itself.

## Authority and outcome

This brief authorizes: reading, measuring, two new reports, and corrections to the
records those two commits wrote where a claim is wrong. It does **not** authorize
code changes, firing either follow-up brief, deleting modules, or launching the game.

End state: the owner knows, in rank order and with evidence, which full-body
replacement work to start first; and every load-bearing claim in `c7266f0` and
`d45655c` has been confirmed, corrected, or marked unproven.

## Phase A — the full-body priority report (blocking, lands first)

### The population

A **full-body replacement** is a module that redefines a shipped declaration outright
rather than delegating to a captured original. It is the critical class because when
the vendor repairs that declaration, our 1.1.0 copy silently reverts the repair — which
is exactly how three of the five new filings failed (F122, F124, F125).

Seed, an authored claim from the orchestrator session on 2026-09-23 — **re-derive it,
do not adopt it.** Method: for each `-- SRC:` pinned declaration in a module, test
whether the module redefines that declaration, and where it captures the original, test
whether the capture is actually *called*. A capture that is never called is a
replacement, not a wrapper.

Seed result: **12 full-body of 52 modules** (51 `Code/Fix_*.lua` + `90_SaveSanitizer`;
`00_Core.lua` is framework, not a module). Split 12 full-body · 17 delegating wrappers ·
22 guards/hooks/data/migrations.

| module | 1.1.1 verdict as landed | filing |
|---|---|---|
| `Fix_TrackSalvageWipe` | FIX | F124 |
| `Fix_VacuumWalks` | FIX | F125 |
| `Fix_DomeOverviewHighlight` | REMOVE | F122 |
| `Fix_TradeRocketFuelRefresh` | REMOVE | — |
| `Fix_TrainCargoDumping` | REMOVE | — |
| `Fix_WispRewards` | REMOVE | — |
| `Fix_LandscapeUnitFilter` | KEEP | — |
| `Fix_PayloadTemplateRefill` | KEEP | — |
| `Fix_RocketDroneChurn` | KEEP | — |
| `Fix_ShuttleTransportCache` | KEEP | — |
| `Fix_TrackConnectorPingPong` | KEEP | — |
| `Fix_TrackSalvageRefund` | KEEP | — |

Falsifying reads, both required:

1. The seed keys off `-- SRC:` pins, so a module that replaces a declaration it never
   pinned is invisible to it. `Fix_BuildingCodesPrefab` has no pins at all and is
   outside the test rather than cleared by it. Sweep the unpinned and
   wrapper-classified modules for an uncaptured redefinition; any module you add or
   remove from the twelve is a finding, reported by name.
2. A capture that is called on only some paths, or called but with its result
   discarded, is a partial replacement. Decide and record which side it falls on; do
   not let the binary hide it.

### What the report must decide

The report's job is **rank order with reasons**, not a catalogue. For each of the
twelve (as you re-derived them):

- Did 1.1.1 change the replaced declaration's body or signature? Name the archived
  1.1.1.405907 evidence.
- If yes, what does our copy revert — and is the reverted vendor work a repair players
  would notice, a save-state migration, or cosmetic?
- Blast radius if it ships wrong: silent and permanent (save corruption, mis-scoring),
  loud and visible, or inert.
- For the six KEEP rows: a KEEP verdict is a this-patch judgement, not a standing
  clearance. Say for each whether it is genuinely inert on 1.1.1 or merely not yet
  broken, because that is the difference between a closed row and standing exposure.

Then rank all action-bearing rows into the order the owner should start them, and say
plainly what goes first and why. Where two rows are coupled, rank them as one unit.

**A coupling to adjudicate, an authored claim from the orchestrator — check it, it may
be wrong.** `Fix_TrackSalvageWipe` and `Fix_BrokenTrackSalvage` both pin
`TrackGridElement:DemolishAndSplitTrack` at the same sha
(`Fix_TrackSalvageWipe.lua:90`, `Fix_BrokenTrackSalvage.lua:35`), and the former
replaces that body outright. If that holds, the REMOVE brief's premise for retiring
`Fix_BrokenTrackSalvage` — that 1.1.1 vanilla excludes and rehomes repair sites — is
only true in a shipping pack after F124's rebase, and F124's rebase restamps a pin the
other module also carries. Decide whether the two briefs can be fired independently, or
whether that pair must move as one unit, and say which brief should own it.

### Landing Phase A

Write `docs/agent/reports/FULL_BODY_PRIORITY_2026-09-23.md`. Give it a
`Must_Read_Header`, add its row to `docs/README.md` if the folder contract requires one,
run `python tools/doccheck.py --regen`, review the generated diffs, and finish on a
green `python tools/doccheck.py`. Commit exact paths only.

Then **message the orchestrator session `smr-bugfixpack-83`** with `SendMessage`. The
message must carry, in a few lines the owner can act on without opening the file:

- the committed SHA and the report path;
- how many full-body modules you found and how that differs from the seed of twelve,
  by name;
- the top-ranked item and the one-line reason it is first;
- the track-pair verdict: independent, or one unit;
- anything in Phase A that changes whether the two follow-up briefs can fire as written.

Do not wait for a reply. Continue straight into Phase B.

## Phase B — the rest of the adjudication

Judge `c7266f0` and `d45655c` on the diff and the archived 1.1.1.405907 tree, with
depth set by consequence:

- **The five filings.** Each `evidence:` field is a claim about archived source. Confirm
  or correct F121–F125 against that tree. A wrong filing is corrected in the entry under
  `smr-bug-library`, not merely noted.
- **The fifteen REMOVE premises.** Each names a native replacement. A disappearance or
  rename is not proof: trace the replacement body and its consumer. Two rows carry
  explicit gates. Open Pasture's is recorded as **cleared** by `d45655c` on the retail
  on-leg (the module declined because the entity mismatch is gone, retail log
  `Mars.exe-20260923-10.39.06-6aad2d75.log:135`) — test that clearance against the
  A/B's own stated limits below before accepting it. The trade-rocket gate is still
  open: decide whether `SavegameFixups.ZZZ_UpdateRefuelRequests` is genuinely
  *enrolled* for an upgrading 1.1.0 save rather than merely present, and whether that
  can be settled at the desk.
- **The retail A/B itself**, which `d45655c` folded into the record. Its own report
  states two limits: the on-leg carried Opt-In and Train Hub mods the off-leg did not,
  so it is **not a single-variable A/B**, and neither leg met the zero-error acceptance
  condition the spent checklist leg set. Those limits bound every claim drawn from that
  run — including the cleared Open Pasture gate and F123's measured pack-on result,
  whose pack-off leg short-circuited at "fix pack not loaded" rather than calling the
  vanilla function. Say plainly which retail-derived claims survive the limits, which
  need a focused re-run, and whether any record overstates what the legs showed.
- **The three FIX premises**, including whether F121's retained load-only half survives
  a whole-tree search for a shipped 1.1.1 migration clearing reason `789863173059`.
- **The thirty-four KEEP verdicts**, at surface level, with any full-body row among them
  already handled in Phase A. Escalate a specific row rather than deep-checking all.
- **The two follow-up briefs**, for premises Phase A or B falsified. A brief that can no
  longer fire as written is a finding; say precisely which clause fails.
- **The `bodycheck.py` self-test change** (`c7266f0`, 25 lines): the OK control was
  rewritten from asserting F46 is still shipped to a patch-stable regex control. Decide
  whether it still fails a tool that returns RED on everything — run
  `python tools/bodycheck.py --selftest` and a deliberately broken variant in a scratch
  copy. A control that cannot fail is worth nothing.
- **The report's unfinished row**: the opt-in outbox entry marked `<<PENDING-RUN>>`.
  Say what is owed and to whom; do not write the opt-in entry from here.
- **ck207** (the limits decision, renumbered by `d45655c`) as the owner will read it:
  does it state the 12-module / 1,000-declaration proposal with the evidence actually
  behind it, and is its "stop the deep sweep here" recommendation still sound now that
  the A/B has run and returned bounded results?

Write `docs/agent/reports/GAMEPATCH_1.1.1_ADJUDICATION_2026-09-23.md`: per area, the
verdict (confirmed / corrected / unproven), the evidence, and what the owner must decide.
Corrections to those records land in those records in the same change.

## Live work list

Put this list in the todo tool before the first write; keep one unfinished
commit-and-verify unit in progress, and add discoveries rather than hiding them.

- [ ] 1. Orient; re-derive the full-body population independently of the seed
- [ ] 2. Per-module 1.1.1 evidence and blast radius for every full-body row
- [ ] 3. Track-pair coupling decided; ranking settled
- [ ] 4. Phase A report written, doccheck green, exact paths committed
- [ ] 5. `SendMessage` to `smr-bugfixpack-83` sent — Phase A is not done until this lands
- [ ] 6. F121–F125 evidence confirmed or corrected in the entries
- [ ] 7. REMOVE premises, the cleared and open gates, FIX premises, KEEP surface pass
- [ ] 8. Briefs, retail A/B limits, bodycheck self-test, opt-in outbox, ck207
- [ ] 9. Phase B report committed; this prompt and its map row deleted

## Scope and stops

In scope: the paths touched by `c7266f0` and `d45655c`, the pack's module bodies as
evidence, the archived 1.1.0.403908 and 1.1.1.405907 trees, two new reports, and corrections to the
records those two commits wrote.

Out of scope: code changes to any module, firing either follow-up brief, deleting or
rebasing anything, release and store surfaces, shipped game files, and launching the
game. A wrong verdict is reported and corrected in the record; it is not repaired in
code from here.

Report instead of continuing only if: (1) a newer game build lands; (2) Phase A
falsifies the full-body framing itself, so the owner's ordering rests on a wrong
premise; or (3) a shared path has peer changes that cannot be integrated without
overwriting them.

## Claim limits

A source read is not `tested`; say SOURCE on build 1.1.1.405907, desk-MEASURED when a
named harness ran, and pending owner play until its checklist leg runs. A matching body
hash is not compatibility. A verdict agreeing with the seed is not confirmation unless
you re-derived it by your own route; say which route. A KEEP is a 1.1.1 judgement, not
a standing clearance for the next patch. The absence of a decoded caller does not prove
an engine route impossible.

## Lifecycle

One-off. When fired, delete this prompt and its row in
`docs/agent/prompts/README.md` in the Phase B result commit. The two reports and the
corrected entries are the durable record.
