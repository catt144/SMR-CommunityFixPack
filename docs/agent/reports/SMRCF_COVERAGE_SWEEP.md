# Coverage sweep — `smr-community-fixes`, the seven leads · 2026-08-16

**One-line result: seven leads adjudicated, four filed (`C49`–`C52`), one
rejected outright, two closed as already-covered with one of them materially
upgraded. Zero fix code written. Zero changes under `Code/`.**

Consumes and replaces `agent/prompts/COVERAGE_SWEEP_SMRCF.md`, deleted in the
same commit (`git show <sha>:docs/agent/prompts/COVERAGE_SWEEP_SMRCF.md`).

## What this was

The owner asked for the pack to be *"fully fledged, one mod fix all"*. A
title-to-title comparison on 2026-08-16 put `fredware`'s **SMR Community Fixes**
(Paradox Mods 153410) at 15 modules, eight overlapping our corpus and seven not.
Those seven were the subject. The method was the owner's own framing:

> *"The only thing I am proposing is we look at his fixes, compare it to game
> code, and determine ourselves if it's a bug we missed."*

**Their mod is a list of claims about Paradox's code; we adjudicated each claim
against Paradox's code.** Every verdict below was derived at
`<game>\ModTools\Src` by symbol — never from a citation inherited from their
repo, our own records, or the brief — per the standing rule that a route can be
wrong while every cited line is right.

**Setup.** Reference clone at `C:\Dev\_ref\smr-community-fixes`
(⛔ outside our repos, never a submodule, never referenced from a shipped doc).
⛔ **Their mod was NOT installed or enabled on the rig** — a third mod would
have invalidated the `STATE.md` gate baselines. Their module count matched the
portal listing exactly: 15 `Code\smrcf_*.lua` plus one framework file, no hidden
extras.

## The scoreboard

| # | Their module | Verdict | Where it lives now |
|---|---|---|---|
| 7 | Restore Soil Overlay | **FILED — real, LATENT** | [`C49`](../bugs/C49.md) |
| 9 | Restore SpaceY Description | **FILED — real, reachable** | [`C50`](../bugs/C50.md) |
| 13 | Restore Localized UI Text | **FILED — real, MEASURED against shipped data** | [`C51`](../bugs/C51.md) |
| 4 | Repair Mod Manager Browser | **FILED — real, their mechanism refuted, ours found** | [`C52`](../bugs/C52.md) |
| 15 | Restore Clustered Lights | **REJECTED — not adjudicable from Lua** | this page, below |
| 10 | Restore Jumbo Cave Reinforcements | **already covered, nothing new** | `C25` (addendum) |
| 12 | Restore Asteroid Lander Cargo Safety | **already covered, MATERIALLY UPGRADED** | `C35` (addendum) |

Two engine facts came out of it: [`EF-063`](../facts/EF-063.md) (how to prove
whether a string is actually translated) and [`EF-064`](../facts/EF-064.md)
(`ProtectedPropertyObject` protects nothing in retail).

## The four filings, in one line each

- **`C49`** — `GetOverlayGrid`'s map guard is mis-grouped so the `soil_solid`
  branch escapes it (`GameOverlays.lua:106`), and three sibling functions in the
  same file prove the pair was meant to be symmetric. **But `soil_solid` has
  zero setters outside its own toggle pair, and that pair has zero callers in
  all of Src** ⇒ `P3`/LATENT/tier U. Third time in this project that a
  mechanism in source turned out not to be a player experience.
- **`C50`** — SpaceY grants `Consts.CommandCenterMaxDrones +20` and its
  description never mentions it. The control is a whole-tree preset sweep: 16
  sponsors, 6 carry an `Effect_ModifyLabel`, **5 of 6 describe every modifier
  they carry** — three of them with the exact number — and SpaceY is the only
  miss. ⚠️ The obvious remedy is a trap: replacing the shipped, translated
  string with a new literal regresses eight languages (`EF-039`).
- **`C51`** — the strongest of the seven and the only one **measured against
  shipped binary data**. The terraforming heading is a raw Lua literal with no
  id at all while `914616772802` carries **TERRAFORMING-GESAMTFORTSCHRITT** in
  `Local\German.fpk`; the *Back to Earth* button uses two ids no pack contains
  while the identical English text ships under two ids that every pack does.
  Two controls (7-of-7 siblings enrolled; 9 raw literals against 633 `T()`)
  rule out "that is just how XDefs work". Repair shape here is loss-free.
- **`C52`** — mod screenshots and thumbnails. Their stated mechanism is
  **refuted by our own `EF-008`**; the real cause is a `local mod_prefix` read
  outside the block that declares it (`ParadoxMods.lua:222` vs `:257`) with the
  developers' own `-- todo: this is not working` sitting directly above it, plus
  a second defect — a thumbnail cache keyed on mod id + version with no
  revalidation, which is release-relevant to us.

## The rejection — #15 Restore Clustered Lights

**Rejected, with the reason, and the reason is not that the symptom is
imaginary.**

Their claim: night lights are staggered over game time, so at compressed game
time they reach the renderer in one burst and trip an engine assertion, quoted
in their own module as
`s_pLightsData->m_LightsIndexData.empty() == s_pLightsData->m_ClusterLights.empty()`.

What we found:

1. **The assertion is not in Lua.** Whole-tree grep over `ModTools\Src`: zero
   hits for `cluster` in any light context, zero for a clustered-light limit,
   zero for that assertion text. It is engine-side C++ — the same class as the
   `Dome_Entrance` pathfinding data on `F55`: **data Lua cannot read, therefore
   a claim Lua cannot adjudicate.** The brief's own instruction covers this
   case: if a lead cannot be reached from vanilla alone, that is the finding.
2. **The Lua side is not self-contradictory.** `NightLightsOn(map, total_delay)`
   (`Lua/NightLightObjects.lua:332-385`) branches explicitly on
   `total_delay == 0`: instant refreshes run `TurnOnRandomized` synchronously
   (`:380-381`), delayed ones run it on a **game-time** thread that sleeps
   between attachments (`:383`, `CreateNightLightThread` at `:305-307`,
   `TurnOnRandomized` at `:309-330`). The caller picks the delay deliberately —
   `OnMsg.LightmodelChange` passes `time == 0 and time or NightLightObjectsTotalDelay`
   (`:253`), with a shipped comment on the third branch naming the instant case
   *"night->night instant refresh, e.g. after save/load"* (`:257`). A game-time
   stagger compressing at high game speed is what a game-time thread **is**.
   There is no dead branch, no unset field, no contradicted intent — nothing for
   `FIX_POLICY` §4 to bite on.
3. **Their remedy is a behaviour change, and arguably in the wrong direction.**
   Forcing `total_delay = 0` makes every eligible light enter in **one** Lua
   update — a bigger single burst, not a smaller one. Their reasoning (that one
   atomic update avoids an inconsistent intermediate state) is plausible and
   unverifiable from Lua.
4. **They have not proven it either.** Their own spec: *"remains default-off
   Beta until the controlled in-game reproduction passes"*, and their module
   header says it *"has not been proven to stop the assertion in a controlled
   in-game test."*

⇒ **No entry.** Filing a `C` row here would record an engine claim we cannot
verify, cannot falsify, and would not act on. If the assertion is ever seen in
one of our own logs with the pack off, that is the moment to revisit — and the
observation would come from a log line, not from source.

## The two already-covered leads

**#10 Jumbo Cave (`C25`).** Their module was read in full. It delegates to the
captured vanilla approach and acts **only after that approach has already
failed** — a reaction to the trigger, not evidence of it, which is precisely the
limit `C25` recorded on 2026-08-01. `beta`/default-off, so they have not
demonstrated the trigger either. **Nothing new; the unrun rider stands.**

**#12 Asteroid Lander (`C35`) — this one paid.** Their module names
`ForceInterruptIncomingDrones()` as the mechanism, which is *not* what our
2026-08-01 trace followed. Re-derived by symbol, **they are right and our entry
was reading the wrong override**: a lander is a `UniversalRocketBase`, whose
`UpdateCargoResourceRequests` (`UniversalRocket.lua:1679-1686`) calls
`ForceInterruptIncomingDrones()` *before* delegating — so confirming a payload
edit actively interrupts drones rather than merely disconnecting command
centres. **And `InterruptDrones` carries the developers' own
`assert(drone.command ~= "Embark")` immediately before `drone:SetCommand("Reset")`
(`_TaskRequest.lua:305-306`)** — with nothing in the filter excluding a drone on
the ramp, and `EF-008` guaranteeing the assert does not stop the `Reset`. The
sibling takeoff path guards the same call with
`while self:IsCargoRampInUse() do … Sleep(1000) end` (`RocketBase.lua:762-768`).
⇒ `C35` moves from *"a located mechanism with an unproven harm"* to *"a
self-contradiction in the strong sense, harm still unwitnessed"*. ⛔ Not
promoted, no fix proposed; the live repro named on the entry is still what would
settle it.

## Corrections made to our own records while here

- **`EF-039`'s live control was already discharged and the fact file still said
  it was queued.** The body carried *"a 30-second live control is queued … Do
  not build a text fix on this reading before that runs"*, while
  `PLAYTEST_ARCHIVE.md:4507-4508` records `ModLog(type(T(8821,"ZZZ")))` printing
  **`userdata`** on 2026-08-02, log `Mars.exe-20260802-20.28.19`. A live hold
  that is actually discharged is worse than no note, because it stops work that
  is allowed. Struck and replaced with the reading.
- **`C35`'s mechanism trace** — see above.

## What was NOT done, deliberately

- ⛔ **No fix code.** Zero changes under `Code/`. The pack's file, module and
  probe counts are untouched; no suite re-measure was needed or run.
- ⛔ **Their mod was never installed.** Every reading is from the clone and from
  `ModTools\Src`.
- ⛔ **Nothing was observed in game.** All four filings are SOURCE-verified;
  `C51` additionally reads shipped binary language data, which is stronger than
  source but is still not a screenshot. Each entry says so in its own words.
- ⛔ **No priority above `P3` was assigned** except `C52`, left at `?` because
  ranking a broken mod-browser feature against gameplay defects is an owner
  judgement, not ours.

## The thing the owner has to decide

**Five to seven modules is not a tidy-up.** The ship line is FROZEN pre-release
(owner ruling 2026-08-12) and the only remaining step is ④ upload. Each new
module costs a source verification, an entry, a probe, a save-safety pass
(`FIX_POLICY` §3a), a suite re-measure, and card + site + `metadata.lua` updates.

⇒ **Recommendation: investigate now (done — this page), build after launch.**
"One mod fixes all" survives as the trajectory without holding the release, and
each filed lead can be un-parked one at a time the way every other family in
this project is. **Mirrored to `PLAYTEST_CHECKLIST.md` item 34 — the decision is
the owner's and nothing here presumes it.**

⚖️ **And a gate for whoever builds first:** per the house rule, heavy
investigation gets an adversarial fresh-context read before implementation. This
leg is investigation. **A QA pass over the batch is owed before any filed lead
becomes code**, and it is not this leg's job.

## The reference clone

`C:\Dev\_ref\smr-community-fixes` was **left in place**, not deleted — it is
cheap, it is outside every repo we version, and the next person to touch
`C49`–`C52` will want it. It is not ours to maintain: do not commit it, do not
add it as a submodule, and do not let its path appear in any shipped document.
