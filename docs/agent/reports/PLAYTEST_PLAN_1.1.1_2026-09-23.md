# 1.1.1 playtest plan — triaged for exposure, not coverage

## Must_Read_Header
<!-- RULES -->
Rule: Ship-blocking is phases 1–3 only; phase 4 is post-ship unless a phase 1–3 result implicates it. [A3: pass]
Rule: Run the unattended legs single-variable — the pack is the only difference between them. [A3: pass]
<!-- /RULES -->

Audience: the owner, at the controls. Ordered so the build can ship after phase 3.

## Why this is triaged rather than exhaustive

Every hour of testing is an hour thousands of users run the **current** build on game
1.1.1, and that build is not inert. It ships full-body replacements that cannot stand
themselves down:

| shipping now | harm while we test |
|---|---|
| `Fix_TrackSalvageWipe` (F124) | Overwrites 1.1.1's repair-site rehome and `repair_cgs` rebuild. **Silent and permanent in the save** — no error, no report, damage accumulates. |
| `Fix_GeneForging` (F123) | Double-pays the technology. Measured in retail: returns 100 against a live parameter of 50. Wrong gameplay every birth. |
| `Fix_VacuumWalks` (F125) | Overwrites the multi-leg migration state machine. Silent. |
| `Fix_DomeOverviewHighlight` (F122) | Marks an empty dome red. Loud, cosmetic. |
| `Fix_FounderTraitNotification` (F126) | Builds an unknown notification id from the base class. |

So delay is not neutral, and the plan is sized to **de-risk shipping**, not to reach full
coverage. Coverage continues after release.

## The risk asymmetry that shapes it

Sixteen retirements sound like more risk than three rebases. They are not:

- **A deletion reverts to vendor code**, which the vendor ships and tests. Its realistic
  failure is a dangling reference — a load error, a lost registration, an orphaned probe
  — and that is caught wholesale by one clean boot, not by testing sixteen behaviours
  one at a time.
- **A rebase is new code** written this session against a body that moved. That is where
  a regression would actually come from.

Hands-on time therefore goes to the rebases and to save compatibility. The retirements
ride on the boot census and their desk controls.

## Phase 0 · Unattended — costs you nothing but the launch

Two autorun legs, then walk away. Each performs the boot census, `DispatchReach` and
`SMRTest.RunAll()` across the current 83 probes, then quits itself.

```powershell
& "C:\Program Files (x86)\Steam\steam.exe" -applaunch 3215050 -smrautorun
```

**Run it single-variable this time.** The 2026-09-23 A/B could not be read cleanly
because the on-leg also carried the Opt-In pack and the Train Hub dev mod while the
off-leg did not. Keep TestKit on for both legs and change **only** the fix pack between
them; disable every other mod for both.

Let each leg quit itself before touching anything, then scan each finished log with
`python tools/logscan.py <log>`.

What this settles, with no attention from you: all sixteen retirements load clean, no
module is orphaned or double-registered, the module census reads 36, and the probe suite
runs. If this is clean, the retirements are done being a ship risk.

## Two different "old saves" — do not conflate them

Phases 1 and 4 move on different axes, and only one of them is ship-blocking.

| axis | what varies | where |
|---|---|---|
| **Pack version** | a save written with the old 52-module pack, loaded with the new 36-module pack, **both on game 1.1.1** | Phase 1, ship-blocking |
| **Game version** | a save written on game **1.1.0**, loaded on 1.1.1 — what F121's provenance condition keys on | Phase 4, post-ship |

**A 1.1.0 save does load on 1.1.1.** The only revision gate refuses a save whose
`required_lua_revision` *exceeds* the running game's (`CommonLua/Savegame.lua:228-230`,
`:970`), and `config.SavegameRequiredLuaRevision` is **402200 on both builds**
(`Lua/Config/config.lua:179`, identical in the archived 1.1.0.403908 and 1.1.1.405907
trees). 1.1.1 did not raise the bar, so the block is forward-only: a 1.1.1 save will not
open on 1.1.0, but the reverse is fine.

⚠️ **But each pre-1.1.1 save is a one-shot fixture.** Loading it converts it — the save
metadata is rewritten with the current revision on the next write
(`CommonLua/Savegame.lua:775`), which is the very thing F121's provenance condition
keys on (`Code/Fix_CloggedBuildingRelease.lua:97-98`, `lua_revision < 405907`).
**Copy the file before loading it**, or the fixture is spent and cannot be re-run.

Measured by the audit seat on 2026-09-23, reading five of the owner's saves as bytes:
1.1.1 saves carry `lua_revision 405907` with `orig_lua_revision 403908`; the 09-17
`C95*` saves carry `403908`. So the pre-1.1.1 fixtures in `saves/game/` are real and the
discriminator is live — candidates run 09-11 to 09-20, including `F119stuck` and the
`C95*` set.

## Phase 1 · The one test that cannot be skipped — ~10 minutes

**Load a save made with the old pack under the new pack.** Every existing user performs
this the moment they update, automatically, without choosing to. Sixteen modules have
just disappeared from under their saves. It is the highest-blast-radius path in the
release and it has never been exercised.

`saves/game/` holds fixtures written with the old pack on game 1.1.1, including
`Autosave Sol 493` (today, 12:35) and `Autosave Sol 31(2)` (today, 11:42). These are the
pack-axis fixtures; they are already 1.1.1 and do not need copying for this phase.

Load it, let it run a few sols, and watch for errors and for track or routing state that
looks wrong. Then do the reverse — save with the repaired pack, remove the pack, restart
fully and load — which is what a user who unsubscribes will do.

## Phase 2 · The two rebases — the irreducible hands-on work

This is new code and the only place a real regression is likely.

**Track salvage (F124).** Curved and short track salvage with a **live repair site
spanning the split** — the vendor semantics the rebase had to preserve. Check survivors,
refunds and shells. This one matters most: its failure mode is silent and lands in the
save.

**Vacuum migration (F125).** A direct final leg and an intermediate leg, with breathable
and no-passage controls. Check reservations and shuttle/train continuation, and cancel
a migration mid-route.

## Phase 3 · Sixty-second confirmations

Each is a single observation. Do them in whatever game state phase 2 leaves you in.

- **F123** — call the chance function with only Gene Forging researched. It must return
  the live parameter (50), not 100. One console line, and it is the defect with measured
  retail evidence against the current build.
- **F122** — open an empty dome's overview. The zero average must not be red.
- **F126** — no founder-trait notification appears where the removed one used to.

**After phase 3 the build can ship.**

## Phase 4 · Post-ship, or earlier only if implicated

**F121, the legacy clogged migration.** It is *inactive on 1.1.1* — the retail on-leg
logged it declining — so it cannot harm a current player. It only acts when loading a
save written before 1.1.1 that carries a stuck building. Testing it properly needs a
pre-1.1.1 fixture with that exact state, which is slow to construct and narrow in reach.
**Copy any candidate fixture before loading it** (see "Two different old saves"): the
first load spends it, and this is the one phase where that matters.

Its builder made the departure with the largest unexamined surface: a saved-provenance
condition resting on `CommonLua/Savegame.lua:775` rewriting the saved revision, with **no
save file inspected**. The audit seat inspected five on 2026-09-23 and the condition
holds. `orig_lua_revision` is **not** a usable alternative key: it records the colony's
origin, not the event's, so a fresh `BuildingClogged` firing on 1.1.1 inside a colony
started on 1.1.0 writes the same saved fields as a genuinely stranded one, and keying on
origin would release it and cut the vendor's one-hour disable short. `lua_revision <
405907` is the widest safe reach.

Its real-world reach is narrower than that suggests, which is the other reason this is
post-ship: **with the pack present at the first 1.1.1 load, a stranded building is healed
on that load, before the rewrite.** The under-heal only bites a player who updated, saved
once *without* the pack, and noticed afterwards.

Also here: the thirteen benign retirements' individual behaviours, which revert to
vendor code and have their desk controls.

## What would stop the ship

Phase 0 showing a load error, a module census other than 36, or a probe regression.
Phase 1 showing errors or wrong state on an old-pack save. Phase 2 showing lost vendor
semantics — survivors, refunds, `repair_cgs` or routing wrong. Anything else is a
finding to file, not a hold.

## Claim limits

Passing these phases supports "no regression observed on the paths played", not "tested".
The unattended legs are desk-MEASURED on their own configuration. Nothing here inspects
a save file's stored fields, so F121's provenance condition stays unproven either way.
