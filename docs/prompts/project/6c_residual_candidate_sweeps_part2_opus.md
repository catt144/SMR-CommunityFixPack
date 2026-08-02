# Chain 6c — residual candidate sweeps, part 2 (pre-cleared; game-free reading)

**Continuation of `6b_residual_candidate_sweeps_opus.md`, which SELF-SPLIT
2026-08-02 under README rule 3 after finishing five of its eight sweeps.
One-off; delete this file in your final commit. Read `README.md` in this
folder first — including the owner blanket pre-clearance block, which is why
this work needs no ask.** Game-free; READ-ONLY on the game dir; no `Code/`
changes.

**Staleness check: `git log --oneline -10` + `git pull`.**

## What 6b already finished — do NOT redo any of it

| 6b job | Result |
|---|---|
| **C18** XenoExtraction | ✅ **CLOSED `wontfix — intent`.** Labels are exact-string with no inheritance; the tech names its four buildings and pays exactly those four |
| **C38** *(new, filed by that sweep)* | **VERIFIED** — Astrogeologist promises unqualified "Extractor production +10%" and pays 10 of 12 buildable extractors. **Routed to prompt 7**, not built |
| **C19** dome passages | ✅ **CLOSED — declined.** Relaunched put the distance term at the consumer (`Dome.lua:256-259`, 1200m). Taking ChoGGi's OG shape would have **degraded F53** |
| **C20** Philosopher's Stone | **Mechanism located** (the `Msg("SectorScanned")` emitter is a game-time thread that opens with `Sleep(10)`); deferred-vs-lost is **CANNOT DETERMINE** → checklist rider written, stays `cand` |
| **C21** St. Elmo sinkholes | **Destruction route VERIFIED**, soft-lock **located not proven** → **promoted to prompt 7** |
| **C25** Jumbo Cave | Patch question answered from source (**1.0.6 replaced the whole scenario and left this wedge byte-identical**); minimal check written as a checklist rider |

## Jobs (todo list first; one sweep per item; every sweep ends in a BUGS entry update — verdicts, not vibes)

1. **C26-C30 — the five SkiRich OG-era candidates** (perpetual maintenance,
   Signal Booster extender radius, Transport Optimization on RC Transports,
   children-only buildings, supply-pod pins). For each: find the mechanism in
   Relaunched Src, verdict VERIFIED-STILL-BROKEN / FIXED-IN-RELAUNCHED /
   CANNOT-DETERMINE with file:line. These are the highest already-patched risk
   in the ledger (the owner's standing challenge) — the Blank Slate precedent
   says expect at least one to be fixed. **This is five sweeps, not one; give
   it its own todo item per candidate.**
2. **F82 trace.** The entry has the legacy `g_SplitSupplyGridPositions` thread
   started; finish the trace (what clears the notification, on what cadence)
   and either file the mechanism or write the timed observation precisely for
   the campaign.
3. **F80 source-audit.** The entry's suspected mechanism
   (`ForEachStationAlongTrack` enumeration direction) is source-checkable:
   audit it, and sharpen the settling observation the checklist carries into
   something a single sitting can PASS/FAIL.

## Scope fence

**In:** the three sweeps + records + checklist-observation wording. **Out:**
any fix (promotions go to prompt 7's packages); C-entries not named here;
anything new → file + route.

## Stop conditions

- A sweep contradicts a recorded verdict → correct the record prominently.
- Context pressure → self-split again (`6d_…_opus.md`) at a clean commit
  boundary. Job 1 alone is five candidates; do not start it with a thin
  context.

## What may not be claimed

No verdict without file:line read this session. "Fixed in Relaunched" only
from current Src, never from patch notes alone. CANNOT DETERMINE is a
first-class result.

## On completion

Outbox → `7_audit_candidate_decisions_opus.md` (promoted packages) and the
checklist observations to the checklist itself (that edit is in-scope here).
Delete this file, update the README chain table, commit, push.

## Notes from upstream

### ⭐ From 6b (2026-08-02) — the strongest lead it hands you, and it is for job 1

**Three of your five SkiRich candidates smell like ONE class we now have three
confirmed members of, and 6b established the mechanism you would need.**

C18's sweep proved how labels work here, and the rule is narrow and total:
**a building registers under `self.class`, `self.object_class` (only when it
differs), `default_label`, `label1..label5`, and its build-menu categories —
and NOTHING ELSE. No parent class ever contributes a label**
(`Lua\Buildings\Building.lua:370-425`, `:427-444`; roster generator agrees at
`:641-661`). An `Effect_ModifyLabel` naming a label no building carries lands
on an empty set and is **silently** a no-op.

**Three entries already sit on exactly that failure:** **C22** (Saint trait
writes `"Religious"` where colonists are filed under `"TraitReligious"`),
**C38** (a ten-label enumeration missing two buildings), and C18's *non*-defect
(four labels, four named buildings, correctly scoped).

**So for C27 (Signal Boosters "never extend Drone Hub Extender radius") and
C28 (Transport Optimization "never applied to RC Transports"), the FIRST check
is not the tech's code — it is whether the tech's `Effect_ModifyLabel` names a
label the target actually carries.** SkiRich describes both as *"the missing
code"*, which is what a label miss looks like from outside. **C29
(children-only buildings admit all age groups)** may be the same shape one
level over — a filter naming a label/trait key that nothing is filed under.
Check `Data\TechPreset.lua` for the effect, then the target's
`.generated.lua` template for `object_class` / `label1..5`, then the class
name. That is a ten-minute test per candidate and it either finds the defect
outright or rules the whole class out.

⚠️ **This is a lead, not a finding. 6b did not look at C26-C30 at all.** If the
labels line up, the mechanism is somewhere else and you start from scratch.

### Two method facts 6b proved that apply to your jobs

1. **⭐ Check the obvious guess and RECORD that you ruled it out.** C21's
   assumed soft-lock was "meteors destroy the anomaly". It is false —
   `SubsurfaceAnomaly` is not a `Building` and matches none of the meteor
   query's classes — and writing that down is what stopped the next reader
   re-deriving it. Do the same for whatever the obvious mechanism is in each
   SkiRich candidate.
2. **⚠️ Save VINTAGE gates behaviour independently of build, and it is not
   rare.** `GameVar("UndergroundRework106", false)` is true only in saves
   *started* at or after 1.0.6 (`Lua\Buildings\UndergroundDome.lua:16-19`), and
   it switches the Jumbo Cave scenario (`Anomaly.lua:26-33`), elevator
   interaction (`Elevator.lua:830,:839`) and underground dome rules
   (`UndergroundDome.lua:41,:53`). **"Present in current Src" does not mean
   "reachable in this save."** If any SkiRich candidate lands near the
   underground, check for a vintage gate before grading it.

---

*The notes below were written for 6b and are carried forward verbatim because
they address jobs that are still open. Their "your job N" numbering refers to
6b's list — job 6 → your job 1, job 7 → your job 2, job 8 → your job 3.*

### From prompt 6 (2026-08-01)

1. **⚠️ Your job 1 (C26-C30) inherits prompt 6's strongest method warning.**
   C32 looked real for one reason only: a third-party fix existed and
   evidently *fires* in the wild. It fires on **destroyed-but-unrebuilt
   buildings**, because `Building:OnDestroyed` is empty while
   `ShiftsBuilding:OnDestroyed` de-labels — a benign asymmetry, not the
   defect. **"His fix does something" is not evidence that the thing it does
   was needed.** For each SkiRich candidate, find what the fix's *predicate*
   actually matches in Src before grading it. This is the same failure the
   audit's own §9 F04 bullet warns about, one level up, and it cost that entry
   its GOLD.
2. **Your job 1 also inherits a live 1.0.7-fixed precedent with a shape worth
   copying.** C32's owner challenge split cleanly into **"1.0.7 killed the
   trigger, not the mechanism"** — asteroids never expire now
   (`Lua\Asteroids.lua:1, :208, :331-348` with `ReleaseAsteroid`'s whole body
   commented out, and `SavegameFixups.AsteroidsNeverExpire` :493-500
   retro-fixing old saves), while the workshift tick is untouched. When you hit
   "fixed in Relaunched?", **answer trigger and mechanism separately** — a
   removed trigger is not a repaired mechanism, and grading them as one thing
   is how a candidate gets wrongly closed.
3. **Your job 2 (F82, split supply grids) sits next to something prompt 6
   proved: grid fragments and label containers span maps, and `UICity` follows
   the map the player is looking at** (`Lua\_init.lua:12-14`).
   `SupplyGridFragment` **is** a `MultiMapSupplyGrid`
   (`Lua\SupplyGrid.lua:337-338`), merged across the elevator
   (`Lua\Buildings\Elevator.lua:402-440`), and registered on **both** cities'
   lists (`SupplyGrid.lua:463-477`). If the sweep reads a city label or a grid
   list, say **which** city and **which** map, or the reading means nothing.
   F82's "split grid rejoined" question in particular may have a cross-map
   face — prompt 6 did not look, and it is yours if it appears.
   *(6b's C19 sweep, the other half of this note, is done and closed.)*

### Late addition, 2026-08-01 — your job 3 (F80) gained evidence

A Reddit thread the owner exported was read in full (`BUG_LIST_AUDIT.md`
**§10.5**, source **[S36]**). ⛔ **It is hotfix-1.0.3-era, four generations
before our pinned build — evidence of HARM, never of current presence. Carry
that sentence with any quote.**

- **Read the F80 entry before you start; it is materially different from when
  this prompt chain was written.** It now carries a witness cluster plus two
  constraining observations. The one that should shape your source audit:
  **Sorbicol reports the failure on a specific origin/destination PAIR while
  the rest of a healthy 3-line network works.** If the enumeration theory is
  right, that is what it should look like — so **audit for per-stop/per-pair
  asymmetry, not for a global break**. Also note the dominant public symptom is
  *"colonists ignore the train and walk, and die"*, not "colonists wait" —
  possibly the same defect before a ticket is ever issued. **Sharpening the
  settling observation to discriminate waits vs. walks would be worth more
  than sharpening it for the waiting case alone.**

### ⭐ One more move for your job 1, proven 2026-08-01: ask "is this DOWNSTREAM of something we already fix?" before asking "is this a new defect?"

**C36 was filed and closed within the hour by that question.** Two current
Reddit threads reported *"Inner Light is broken for some people"*. Rather than
sweep it as a new mystery defect, the check was whether an existing entry could
already produce it — and `Lua\Mysteries\Dream.lua:20-34` showed the mystery's
mirage loop skips `Dream()` for as long as `IsDisasterPredicted()` is true,
which is exactly the flag **F81(a)** strands permanently. Not a new defect: a
silent downstream casualty of one we already repair. **It even explained the
reporters' "for some people"** — you are affected iff a meteor storm completed
during your run.

**Why this matters for C26-C30 specifically.** Those are five author-witnessed
symptoms with no mechanism. Symptoms are what players can see; **one root defect
routinely presents as several unrelated-looking symptoms**, because players
cannot see causes (the same commenter gave two separate pieces of advice for
one bug). So for each candidate, before hunting a new mechanism, ask whether
any entry we already hold could produce that symptom — and check the
`REACHABILITY_AUDIT.md` "downstream victims" lists, which is where the Inner
Light connection had been sitting unread as an inference for days.

**Tooling you may want:** the six archived FPKs re-extract in one shot with
`python tools/flpk_extract.py "C:\Dev\workshop_fpk_archive" <outdir>` (all six
unpacked cleanly on 2026-08-01; fredware's is the only multi-file one).
