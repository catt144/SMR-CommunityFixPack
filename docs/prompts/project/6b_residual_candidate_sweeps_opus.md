# Chain 6b — the residual candidate sweeps (pre-cleared; game-free reading)

**One-off; delete this file in your final commit. Read `README.md` in this
folder first — including the owner blanket pre-clearance block, which is why
this prompt exists at all (it was an open "sweep now or leave?" question and
the owner answered it in advance).** Game-free; READ-ONLY on the game dir;
no `Code/` changes. Runs after prompt 6 (its verdicts may overlap yours).

**Staleness check: `git log --oneline -10` + `git pull`.**

## Jobs (todo list first; one sweep per item; every sweep ends in a BUGS
entry update — verdicts, not vibes)

1. **C18 — XenoExtraction label coverage.** The audit marked this an INTENT
   QUESTION (description matches the four shipped effects; no promise
   broken). Answer the one checkable fact: does `AutomaticMetalsExtractor`
   (and the Micro-G extractors) carry labels a player would reasonably
   expect the tech's named buildings to cover? Expected outcome per the §4
   bar: likely a clean DECLINE (no tell) — the pre-clearance covers
   recording that close as `wontfix — intent` without a fresh ask.
2. **C19 — `AreDomesConnectedWithPassage` distance term.** Sweep who
   consumes the predicate in Relaunched and whether the long-walk-through-
   network class survives F52's fix; state the interaction with F52/F53
   explicitly. Verdict: F-row package for prompt 7, or close with grounds.
3. **C20 — Philosopher's Stone paused sector count.** Trace the
   `registers._sectors_scanned` update path; determine whether the
   pause-stall is live in Relaunched from source, and if source can't
   settle it, write the ONE console observation for the campaign checklist.
4. **C21 — St. Elmo sinkholes vs meteors.** Check the meteor damage path
   against `SinkholeBase` (no `indestructible` set, `Fireflies.lua:116`);
   soft-lock class. Verdict or checklist observation, as with C20.
5. **C25 — Jumbo Cave waste-rock wedge.** Source has the wedge chain
   verified; what's unproven is the trigger (unreachable rock). Define the
   minimal in-game check for the campaign, and check whether the 1.0.4-1.0.7
   patch notes ever touched Jumbo Cave reinforcements.
6. **C26-C30 — the five SkiRich OG-era candidates** (perpetual maintenance,
   Signal Booster extender radius, Transport Optimization on RC Transports,
   children-only buildings, supply-pod pins). For each: find the mechanism
   in Relaunched Src, verdict VERIFIED-STILL-BROKEN / FIXED-IN-RELAUNCHED /
   CANNOT-DETERMINE with file:line. These are the highest already-patched
   risk in the ledger (the owner's standing challenge) — the Blank Slate
   precedent says expect at least one to be fixed.
7. **F82 trace.** The entry has the legacy `g_SplitSupplyGridPositions`
   thread started; finish the trace (what clears the notification, on what
   cadence) and either file the mechanism or write the timed observation
   precisely for the campaign.
8. **F80 source-audit.** The entry's suspected mechanism
   (`ForEachStationAlongTrack` enumeration direction) is source-checkable:
   audit it, and sharpen the settling observation the checklist carries
   into something a single sitting can PASS/FAIL.

## Scope fence

**In:** the sweeps + records + checklist-observation wording. **Out:** any
fix (promotions go to prompt 7's packages); C-entries not named here;
anything new → file + route.

## Stop conditions

- A sweep contradicts a recorded verdict → correct the record prominently.
- Context pressure → self-split (`6c_…_opus.md`) — eight sweeps is a lot;
  split by default at the halfway mark if the first four ran long.

## What may not be claimed

No verdict without file:line read this session. "Fixed in Relaunched" only
from current Src, never from patch notes alone. CANNOT DETERMINE is a
first-class result.

## On completion

Outbox → `7_audit_candidate_decisions_opus.md` (promoted packages) and the
checklist observations to the checklist itself (that edit is in-scope
here). Delete this file, commit, push.

## Notes from upstream

### From prompt 6 (2026-08-01) — four sweeps run; three things touch your jobs

**None of my four is yours to redo.** Results: C32 **DOWNGRADED** (no route in
current Src), C04 **CONFIRMED and promoted → F90**, F35 scope **re-confirmed
from source**, fredware #11 **a real gap → filed C35, deliberately not
promoted**. Full trails on the BUGS entries and `BUG_LIST_AUDIT.md` §10.

**Three carry into your sweeps:**

1. **⚠️ Your job 6 (C26-C30) inherits my strongest method warning.** C32 looked
   real for one reason only: a third-party fix existed and evidently *fires* in
   the wild. It fires on **destroyed-but-unrebuilt buildings**, because
   `Building:OnDestroyed` is empty while `ShiftsBuilding:OnDestroyed`
   de-labels — a benign asymmetry, not the defect. **"His fix does something"
   is not evidence that the thing it does was needed.** For each SkiRich
   candidate, find what the fix's *predicate* actually matches in Src before
   grading it. This is the same failure the audit's own §9 F04 bullet warns
   about, one level up, and it cost that entry its GOLD.
2. **Your job 6 also inherits a live 1.0.7-fixed precedent with a shape worth
   copying.** C32's owner challenge split cleanly into **"1.0.7 killed the
   trigger, not the mechanism"** — asteroids never expire now
   (`Lua\Asteroids.lua:1, :208, :331-348` with `ReleaseAsteroid`'s whole body
   commented out, and `SavegameFixups.AsteroidsNeverExpire` :493-500
   retro-fixing old saves), while the workshift tick is untouched. When you hit
   "fixed in Relaunched?", **answer trigger and mechanism separately** — a
   removed trigger is not a repaired mechanism, and grading them as one thing
   is how a candidate gets wrongly closed.
3. **Your job 2 (C19, dome passages) and job 7 (F82, split supply grids) both
   sit next to something I proved: grid fragments and label containers span
   maps, and `UICity` follows the map the player is looking at**
   (`Lua\_init.lua:12-14`). `SupplyGridFragment` **is** a `MultiMapSupplyGrid`
   (`Lua\SupplyGrid.lua:337-338`), merged across the elevator
   (`Lua\Buildings\Elevator.lua:402-440`), and registered on **both** cities'
   lists (`SupplyGrid.lua:463-477`). If either sweep reads a city label or a
   grid list, say **which** city and **which** map, or the reading means
   nothing. F82's "split grid rejoined" question in particular may have a
   cross-map face — I did not look, and it is yours if it appears.

**Nothing else of mine overlaps you.** C35 is a lander/cargo-ramp lead with a
named settling observation; it is not in your list and should not be adopted
into it.

**Tooling you may want:** the six archived FPKs re-extract in one shot with
`python tools/flpk_extract.py "C:\Dev\workshop_fpk_archive" <outdir>` (all six
unpacked cleanly this session; fredware's is the only multi-file one).
