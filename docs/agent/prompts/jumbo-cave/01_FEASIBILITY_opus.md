# D·01 — feasibility and the seed hunt · UNATTENDED · owner cost ZERO

**Read `README.md` in this folder first — especially ⛔ THE LINE and the
⚖️ pre-registered discriminator. Both bind you.** Then `docs/agent/STATE.md`,
then this.

## 0 · Staleness check

```
git log --oneline -10
git pull
```
⛔ **This prompt is gated on chain A.** If `smrcf-verify/` is not yet consumed,
**STOP and say so** — job 3 there answers whether any of this is possible.

## 1 · 🗒 Live todo list from your first action.

## 2 · The jobs

### Job 1 — find the deposition density parameter
Waste rock is `Deposition` scatter placed at map generation. Find **where its
amount is authored** for the underground map: the `RandomMapPreset` used
(`"Underground"` unless the map data overrides it,
`RandomMapGenerator_Picard.lua:274`), the `MapData` instance, whatever
scatter/prefab rule places `WasteRockObstructor` entities.

Deliver: the exact field, its shipped value, its range, and **how a mod can set
it at generation time without touching game files**.

⛔ If the only way to change it is editing the installation, **STOP** — that is
forbidden, and the chain re-plans around walling a rock in with buildings
instead (a legitimate but weaker test that proves consequence, not trigger).

### Job 2 — prove or kill the seed search
Using chain A's answer about drivable generation:
- generate N maps across seeds, reading `UndergroundMap.City.labels.JumboCave`
  after each
- **measure and report the frequency** — how many seeds in how many carried a
  cave, and how long one generation costs

That frequency is a deliverable in its own right whatever else happens: it tells
the owner whether "wait for one organically" was ever a plan.

⛔ **Abort thresholds, written down before you start** (`CHAIN_METHOD` §5-D):
if one generation costs more than ~60 s, or 50 seeds yield no cave, **stop and
route to the owner** rather than grinding. Record the numbers either way.

### Job 3 — characterise the winner
For the first seed that yields a cave, record at shipped density: the cave's
position, the surrounding terrain passability, the `WasteRockObstructor` count
near it, and whether any of them already look enclosed. **This is the control
against which 02's elevated-density run is read.**

## 3 · Predictions before any run
Numbered, with falsifiers, committed and pushed BEFORE the first generation.
Include your honest prior on cave frequency — being wrong on the record is worth
more than not writing it down.

## 4 · Scope fence
**IN:** the density parameter, the seed sweep, the baseline characterisation.
**OUT:** ⛔ generating the staged colony (that is 02) · ⛔ any elevated density
run · ⛔ any fix code · ⛔ owner time · ⛔ touching the owner's saves.

## 5 · ⛔ What may not be claimed
- ⛔ **"The seed search works"** on a `type()` read alone — a callable function
  is not a completed generation.
- ⛔ **Any statement about the trigger.** This prompt establishes a venue.
  Nothing here can say whether geometry strands a rock.
- ⛔ **A cave frequency** from a sweep too small to carry it. Report n, not a
  rate dressed as a fact.
- ⛔ Provenance per row; the ROUTE sentence tagged separately from its citations.

## 6 · Close-out
One commit: findings appended to `02_STAGE`'s and `04_AUDIT`'s
`## Notes from upstream` · `C25` entry updated with the measured cave frequency
(that is a real finding about the game, whatever happens next) · logs archived
`git add -f` · manifest row struck · `git rm` this file · doccheck GREEN · commit
naming the grave · push.

⚠️ **If job 1 or job 2 aborted**, your close-out hands `04_AUDIT` the reduced
form: post-mortem, route the respec/abandon decision to the owner, and the
remaining prompts get deleted rather than run. **A recorded kill is the gate
working, not a failure.**

## Notes from upstream

*(Chain A's audit appends here. The coverage sweep's own handoff:)*
- `WasteRockObstructor` is `Deposition` scatter — `Decor.lua:97-98`,
  `_EntityData.generated.lua` `class_parent = "Deposition,WasteRockObstructor"`,
  `Landscaping.lua:404`. SOURCE, 2026-08-16, re-derive it.
- Underground map is generated with the surface from `UIColony.map_seed`
  (`RandomMapGenerator_Picard.lua:270-289`), not on unlock.
- `JumboCave` is a placed `BuildingTemplate`; the scenario *finds* one via
  `SA_PickRandomObject{ obj_label = "JumboCave" }`. Empty label ⇒ the storyline
  never starts.
