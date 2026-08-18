# L1 — the collision map: what our 75 modules patch, and where they meet

**Pre-launch sweep chain, link 1, lens L1 (structure & collision).**
Produced 2026-08-17. Configuration: **dev tree, source-derived only — nothing in
this document was run in a game.**

⭐ This is the artifact `00_CHAIN_SPEC.md` §3 says has never been produced here.
It is mechanical: every row below was emitted by a script over `Code/*.lua` and
the shipped `ModTools\Src` tree, not asserted. ⛔ Its verdicts are **static**;
where a question needed a running game, the row says *unmeasured* rather than
guessing.

---

## 0 · What was measured, and with what

| input | measured |
|---|---|
| our tree | 76 `Code/*.lua`, **197 patch-site rows**, **134 distinct symbols** after alias resolution |
| of those | **50 class-method patch targets**, **16 global replacements/definitions**, **21 `OnMsg` registrations** |
| game source | `ModTools\Src` — **4,446 `.lua` files**, **3,708 `DefineClass`**, 3,927 class names carrying parents or methods |
| engine tables | `AutoResolveMethods` — **58 members**, enumerated in full |

⚠️ **Alias resolution is the reason this map exists.** Modules capture targets as
file-locals (`local C = rawget(_G,"Colonist")`) and then write `function C:Idle`.
A plain grep reports `C:Idle`, which cannot be joined across files — so a naive
sweep sees **zero** same-symbol collisions and reports the pack clean. The first
pass of this very script did exactly that. Resolving the alias first is what
turned up the one real double-wrap in the pack.

---

## 1 · The three checks

- **C1 — shadowing.** We wrap `Parent:Method` at mod-load time, before class
  flattening, so every subclass inherits the wrapper — **unless that subclass
  declares its own `Method`**, in which case flattening keeps the subclass's copy
  and our repair silently does nothing there.
  **Route re-derived at Src:** `classes.lua:608` — `if src ~= classname then` …
  *"skip members set in our classdef"*. A class that declares a member itself
  never takes a parent's value for it.
- **C2 — chain collision.** Two of our modules patching the same method on two
  classes that are ancestor/descendant of one another, or on the same class.
- **C3 — shared class surface.** Two modules patching *different* methods on one
  inheritance chain. Informational; no fight by itself.

### The two engine facts C1/C2 turn on, both re-derived rather than inherited

1. **`OnMsg` is additive, and does not survive a Lua reload.**
   `cthreads.lua:64-72` — `OnMsg`'s `__newindex` **appends** to
   `message_to_staticfuncs[message]`. So eleven modules assigning
   `OnMsg.LoadGame` do not overwrite each other; all eleven run.
   ⭐ And `message_to_staticfuncs` is a plain **file-local**, *not* declared under
   `FirstLoad` — so `ReloadLua` rebuilds it empty and the handlers do **not**
   accumulate across reloads. That is the opposite of `SMRFixPack.order`, which
   *is* preserved across a reload and is exactly why it double-listed every
   module until `2f077e8`.
2. **`Done`, `Init` and `GameInit` are NOT auto-resolved.** The full
   `AutoResolveMethods` list is 58 entries; none of the three is among them. A
   subclass `Done` therefore genuinely replaces its parents' — it is not chained
   for you.

---

## 2 · C1 — every shadowing candidate, adjudicated

Eight of our 50 class-method targets have at least one subclass in Src declaring
the same method. Each is decided by one question: **does the subclass override
call the parent, or replace it outright?**

| # | our patch | subclasses declaring it | verdict |
|---|---|---|---|
| 1 | `Building:OnDemolish` — `Fix_TrainsToVoid.lua:41`, gated `IsKindOf(self,"Station")` | 10 (CrystalsBuilding, LanderRocketBase, LandingPadBase, MechanizedDepot, PassageBase, RocketBase, RocketExpeditionBase, TrackBase, TradePadBase, UniversalRocketBase) | ✅ **no gap.** None is on Station's ancestor chain. Only `Building` (`Building.lua:873`) and `Demolishable` (`Demolishable.lua:157`) declare `OnDemolish` there. The module header's claim re-derived and **holds**. |
| 2 | `Building:SetDome` — `Fix_GhostFarmOxygen.lua:36`, gated `IsKindOf(self,"FarmBase")` | 2 (`Residence`, `TrainingBuilding`) | ✅ **no gap.** Neither is a `FarmBase` ancestor; only `Building` (`Building.lua:673`) declares `SetDome` on that chain. |
| 3 | `CargoTransporterNew:UpdateCargoResourceRequests` — `Fix_RocketDroneChurn.lua:42` | `UniversalRocketBase` (`UniversalRocket.lua:1679`) | ✅ **no gap.** The override **calls the parent explicitly** — `CargoTransporterNew.UpdateCargoResourceRequests(self)`, `UniversalRocket.lua:1684`. Landers reach our patch. |
| 4 | `RCTransport:CanInteractWithObject` — `Fix_RocketInteractGuard.lua:120` | `RCConstructorBase`, `RCHarvester`, `RCTerraformer` | ✅ **no gap.** Every override tail-calls the parent: `RCHarvester.lua:127`, `RCConstructorBase.lua:353`, and `RCTerraformer.lua:237` → `RCConstructorBase` → `RCTransport`. |
| 5 | `RCTransport:InteractWithObject` — `Fix_RocketInteractGuard.lua:128` | same three | ✅ **no gap.** `RCHarvester.lua:139`, `RCConstructorBase.lua:372`, and `RCTerraformer.lua:242` calls `RCConstructorBase.InteractWithObject`, which calls `RCTransport`'s. |
| 6 | `MicroGHabitatAutoResolve:IsSuitable` — `Fix_ShelterReflex.lua:43` | `NaturalHabitatBase` (`NaturalHabitat.lua:33`) | ⛔ **REAL GAP — finding L1-F2.** See §4. |
| 7 | `TrackConnectedObjBase:Done` — `Fix_TrackConnectorPingPong.lua:190` | `Station` (`Station.lua:134`) | ⛔ **REAL GAP — finding L1-F3.** See §4. |
| 8 | `ElectricityStorage` / `WaterStorage` / `AirStorage` `:OnModifiableValueChanged` — `Fix_StorageRateModifiers.lua:53` | none | ✅ **no gap.** All three declare the method themselves (`ElectricityStorage.lua:47`, `LifeSupportStorage.lua:25`, `:131`); across their 2+4+4 descendants, **nothing** shadows it. |

⚠️ Row 8 was the artifact's one blind spot on the first pass — the targets come
from a runtime `TARGETS` loop, so the static map read the base as a loop
variable. The three class names are literals in the table and were resolved by
reading the module; the hole is closed, not waived.

## 3 · C2 / C3 — collisions between our own modules

**C2 — same method, one class or one chain: exactly one hit in the whole pack.**

```
Colonist:Idle   <- 2 modules
    Fix_ShelterReflex.lua:57-58    (loads first  -> INNER)
    Fix_ArrivalDeaths.lua:170-171  (loads second -> OUTER)
```

That is finding **L1-F1**; see §4.

**C3 — shared class surface, different methods: 16 pairs**, all on wide bases
(`Building` ↔ 10 subclasses, `City` ↔ `ResourceTracking`, `Train` ↔
`TransportStatistics`, `CargoTransporterNew` ↔ `UniversalRocketBase`, …). None is
a fight: different methods, and every one of our wrappers on these classes gates
itself to its own object kind before touching anything (`FIX_POLICY` §2's
foreign-object rule). Recorded for the next link, not actioned.

**Global replacements: 16 sites, 16 distinct symbols — no two modules replace the
same global.**

`CompleteMilestone` · `ExpandTrackFromElement` · `FindCaveInLocation` ·
`FindTransportationModeToCommunity` · `GetDisasterWarningTime` ·
`GetDustDevilsDescr` · `GetGridGlobalStorage` · `GetRareTraitChance` ·
`IsLRTransportAvailable` · `LandscapeForEachUnit` · `OverrideDisasterDescriptor` ·
`PlanetaryAsteroidVisitPossible` · `RainsDisasterActivation` · `SetLightTrapMode` ·
`TriggerCaveIn` · `WaitBombard`

**`OnMsg` registrations: 21, across 3 shared messages.** `LoadGame` ×11 ·
`PostLoadGame` ×7 · `NewDay` ×3. Additive (§1), so no registration fight.
⛔ **Not checked: whether two handlers on the same message touch the same state.**
Additivity was proven; non-interference was **not**. That is in the ledger's
*NOT reached* column.

## 3a · The other two exposure shapes (`02_LENS_NOTES.md` L1 names five)

Class method, global assignment and table slot are §2–§3. The remaining two:

**Preset field — 13 modules touch preset data; no two write the same field.**
10 route through `SMRFixPack.DataPatch`, 2 through `SMRFixPack.OnDataReady`.
The write targets:

| module | preset write |
|---|---|
| `Fix_DustSicknessDamage` | `TraitPresets.DustSickness.daily_update_func` (`:60`) |
| `Fix_SaintBlessing` | `p.modify_trait` on label-resolved trait presets (`:103`) |
| `Fix_FounderTraitNotification` | **reads only** (`:44`) |
| `Fix_DustSicknessBiorobots` | reads `colonist.traits`; no preset write |

⭐ **One shared preset group, and it is clean by construction.**
`Presets.MapSettings.DustDevils` is touched by **two** modules —
`Fix_DustDevilSpawnGate` and `Fix_DustDevilsDescrMap`. Neither mutates it:
SpawnGate builds a **copy** (`:199-247`) and returns that; DescrMap only reads it
(`:65-66`). The only same-preset pair in the pack does not collide.

**Own thread — 7 creation sites across 6 modules; no shared handle.**
`00_Core.lua:530` (the real-time pregame-menu dialog thread) ·
`Fix_BombardmentSpread:137` · `Fix_CrystalMysteryHang:71` ·
`Fix_ExtenderFlapChurn:90` · `Fix_MeteorStormWedge:138` ·
`Fix_MilestoneCrash:40` · `Fix_RainsDeadlock:195` ·
`Fix_TrackConnectorPingPong:174`. Only two park the handle anywhere
(`pending[hub]`, `data.activation_thread`) and both are module-private. No two
modules share a thread global, so there is no thread-ownership fight.

⭐ **A positive worth recording, because L8 will need it.**
`Fix_DustDevilSpawnGate`'s `set_installed` (`:250-258`) does **not** blindly
restore its captured original. It re-reads the live global and only swaps back
`if cur == wrapper` — so a later replacement by another module *or another mod*
is left alone instead of being clobbered. That is the correct shape for a
save/restore around a global, and it is the shape the rest of the pack should be
measured against under lens L8.

## 4 · Findings

Routes and evidence live here; the finding records themselves are in
`prompts/prelaunch-sweep/SWEEP_FINDINGS.md`.

### L1-F1 — `Colonist:Idle` is wrapped twice, and the order is load-bearing and unrecorded

`Fix_ShelterReflex` and `Fix_ArrivalDeaths` both wrap `Colonist:Idle`. Load order
is `metadata.lua`'s `code` list order — ours to set (`FIX_POLICY` §8) — and it
currently reads `Fix_ShelterReflex.lua` at **line 130**, `Fix_ArrivalDeaths.lua`
at **line 138**.

So ShelterReflex installs first and ArrivalDeaths wraps *it*: **ArrivalDeaths is
the outer wrapper.** That is the safe order, and it is safe by accident:

- ArrivalDeaths' wrapper only assigns `self.emigration_dome` /
  `self.emigration_elevator` and then **always** delegates
  (`Fix_ArrivalDeaths.lua:200`);
- ShelterReflex's wrapper can call `self:SetCommand("Rest")`, which by its own
  comment **"kills this thread; never returns"** (`Fix_ShelterReflex.lua:70`).

Swap the two `metadata.lua` lines and ShelterReflex becomes outer: for any
colonist meeting the shelter precondition, the F53b dome re-choice would be
skipped entirely — the arrival would keep an unreachable `emigration_dome`.

⛔ **Nothing records this.** Neither module header mentions the other; `FIX_POLICY`
§8 covers intra-mod order only as a `00_Core.lua`-must-be-first rule; and the
`metadata.lua` list carries no note. A future reordering — a rename, an
alphabetisation, a regenerated list — is silent.

⚠️ **Unmeasured:** whether one colonist can satisfy both preconditions at once.
ShelterReflex needs `outside_start`, a valid **working residence**, no
`transport_task`, not dying, ≥ half the oxygen budget outdoors, and a
non-breathable atmosphere; ArrivalDeaths needs `self.arriving` and an
`emigration_dome`. An arriving colonist holding a working residence is the
overlap, and **this link did not run a game**, so the overlap is neither shown
nor ruled out. The order dependency is real regardless of whether the overlap is.

### L1-F2 — F73(a) does not reach `NaturalistHabitat`

`Fix_ShelterReflex` replaces `MicroGHabitatAutoResolve:IsSuitable` so a momentary
life-support gap cannot evict a habitat's residents.

⭐ **This is the pack's only intersection with the engine's auto-resolve
machinery, and the fix works there for a reason nothing on record states.**
`AutoResolveMethods.IsSuitable = "and"` (`Building.lua:14`) — one of 58 such
members, and the **only** one among our 50 class-method targets.
`MicroGHabitatAutoResolve` is a bare mixin (`DefineClass("MicroGHabitatAutoResolve")`,
`MicroGHabitat.lua:1`) whose sole job is to contribute a term to that `and`.
Our write lands in `classdefs[...]` before flattening, and `GatherAutoResolved`
reads `classdefs[class][member]` (`classes.lua:107-119`), so the **patched** body
is the term combined into `MicroGHabitatBase`. ✅ `MicroGHabitat` is covered.

But `NaturalHabitatBase:IsSuitable` (`NaturalHabitat.lua:33`) declares the
identical **un-fixed** vanilla body —

```lua
function NaturalHabitatBase:IsSuitable(colonist)
    return self:GetScoreFor(colonist.traits) > 0
end
```

— and by `classes.lua:608` a class that declares a member itself skips its
parents' values **including the auto-resolve**. `NaturalistHabitat.__parents =
{ "NaturalHabitatBase" }`, so it inherits the shadowing copy.

⇒ Of `MicroGHabitatAutoResolve`'s 4 descendants: `MicroGHabitat` ✅ ·
`MicroGHabitatBase` ✅ · `NaturalistHabitat` ⛔ · `NaturalHabitatBase` ⛔.

⚠️ This is a **coverage** finding, not a defect in shipped code. Whether the same
harm is reachable on a Naturalist Habitat needs its own `FIX_POLICY` §4 intent +
reachability work; **no fix was written** (see §5).

### L1-F3 — F66's recovery reclaim does not run when a `Station` dies

`Fix_TrackConnectorPingPong` wraps `TrackConnectedObjBase:Done` so that when a
track-connected building dies, its neighbours are prompted to reclaim the hexes
it held (`SMRFixPack.TrackConnectorReclaim`).

`Station:Done` (`Station.lua:134-153`) declares its own body and **does not call
`TrackConnectedObjBase.Done`** — it ends at `RebuildTrainRoutes()`. Since `Done`
is not auto-resolved (§1), our wrapper is unreachable for a Station.

Of `TrackConnectedObjBase`'s 6 descendants:

| class | reclaim runs? |
|---|---|
| `StationBig` | ✅ |
| `StationSmall` | ✅ |
| `TrackTunnel` | ✅ |
| `TrackTunnelBase` | ✅ |
| `UniversalTunnel` | ✅ |
| `Station` | ⛔ shadowed |

⭐ **The primary F66 fix is unaffected.** It replaces
`TrackConnectedObjBase:CreateConnectorElements`, and the C1 scan found **no**
descendant declaring that method — so the ping-pong repair itself reaches
stations. Only the secondary recovery-gap reclaim is shadowed.

### L1-F4 — recorded fact, for `agent/facts/`

The three engine routes re-derived above (`OnMsg` additivity + its non-survival of
`ReloadLua`; `classes.lua:608` declare-wins; `Done`/`Init`/`GameInit` absent from
the 58-member `AutoResolveMethods`) are the facts every future wrapper decision in
this pack depends on, and none of them is currently written down.

## 5 · Why link 1 changed no code

`01_LINK.md` §4 permits link 1 to fix. Nothing here was fixed, deliberately:

- **No finding is launch-blocking.** L1-F1 is latent and currently in the safe
  order; L1-F2 and L1-F3 are coverage gaps in which the pack does *less* than it
  could, never something wrong.
- **L1-F2 and L1-F3 would be new fixes, not repairs.** `FIX_POLICY` §4 requires an
  `agent/bugs/` entry with file:line evidence, a positive intent statement and a
  recorded reachability tier before any of that ships. That is a build, and a
  build is not a sweep's to start on a release candidate.
- **L1-F1's cheapest honest remedy is a note, and every surface for the note is a
  shipped file** (`metadata.lua`, or the two module headers). Editing the tree
  under test to record a latent risk is a poor trade three days from a first
  launch; the finding is routed instead.

## 6 · What this map does NOT cover

⭐ The honest product. Each of these is in the ledger's *NOT reached* column.

1. **Preset-field coverage is by enumeration, not by proof.** §3a lists the write
   targets of the 13 preset-touching modules read one by one. ⛔ Unlike the class
   map, it is **not** backed by a mechanical extractor — a preset write hidden
   behind an indirection I did not read would not appear. Depth: medium.
2. **State interference between `OnMsg` handlers.** Additivity is proven; whether
   the 7 `PostLoadGame` handlers (or the 11 `LoadGame` ones) read and write
   overlapping state is **not** checked.
3. **Anything running.** Every verdict here is source-derived. Nothing was
   launched, and neither 2026-08-17 core fix has yet run in a game.
4. **The TestKit's own patches.** `Code/` only — and the TestKit mutates `_G`.
5. **Other mods.** Whether a foreign mod wrapping what we wrap breaks anything is
   lens **L8**, untouched.
6. **Aggregate save footprint, uninstall, and `90_SaveSanitizer`'s coverage of the
   current module set** — lens **L3**, untouched.
7. **Runtime cost of 75 modules together.** Not measured by anything, ever.

## 7 · Reproducing this

The extraction and analysis scripts are throwaway and were **not** committed —
`00_CHAIN_SPEC.md` §4 bars adding instruments to `Code/`, and a one-shot analysis
script over `Src` is not project tooling. The method, in full:

1. For each `Code/*.lua`, build the file's alias map from
   `local X = rawget(_G,"Y")`, `local X = g_Classes.Y`, `local X = Y`.
2. Extract patch sites: `function <base>[:.]<m>`, `<base>.<m> = …`,
   `SMRFixPack.SetGlobal("N"…)`, `_G["N"] = …`, `local orig… = <base>[:.]<m>`.
   Resolve `<base>` through the alias map; drop bookkeeping locals.
3. Walk `ModTools\Src` for `DefineClass.X = { __parents = {…} }` and
   `function C:M(`, building parent/child/declares graphs.
4. C1: for each patched `C:M`, list descendants of `C` declaring `M`.
   C2: for each method patched twice, test ancestry between the two classes.
   C3: same, across different methods.
5. For each C1 hit, read the subclass override and decide whether it calls the
   parent.
