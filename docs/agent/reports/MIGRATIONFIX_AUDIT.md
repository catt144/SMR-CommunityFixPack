# migrationfix — terminal audit (link 02, Fable), 2026-09-11

**Verdict: SHIP A. B was not built, so "A+B" was never on the table; the F60 trace holds at source and B can run in
the next cycle.** Written by `smr-bugfixpack-b7` against HEAD `3b41d9f`, shipped tree **1.1.0.403908**
(`bodycheck` 116 OK / 121 rows, so the live tree still matches every pin). Chain map: `prompts/migrationfix/README.md`
(consumed in this commit; its HANDOFF section is link 01's close-out and is reproduced nowhere else — read it from git,
`git show 3b41d9f:docs/agent/prompts/migrationfix/README.md`).

Scope as briefed: grade the build (primary), surface-sweep Astra's eight verdicts (secondary, a read-and-logic check,
not a re-run). Every claim below is my own read of the shipped body at the cited line, not an inheritance from
`bugs/F59.md`, the report, or link 01's close-out.

## 0 · What I ran (results are re-runnable, never quoted from a document)

| command | result |
|---|---|
| `python tools/desk_f59_expedition.py` | 18 of 18 |
| `python tools/desk_f59_interact.py` | 23 of 23 |
| `python tools/desk_probes_f67_f59.py` | 10 of 10 |
| `python tools/deskbench.py` | 16 harnesses, all HELD |
| `python tools/parsecheck.py` | 48 files, 0 errors |
| `python tools/bodycheck.py` / `--module FreedHousingNotice --all` | 116 OK of 121 rows (2 NO-MANIFEST, 1 NO-DEFECT, 4 SRC-NONE, all pre-existing) / 8 of 8 |
| `python tools/doccheck.py` | GREEN |

**⛔ The falsification the brief demanded, done with scratch copies rather than the harnesses' own `synchronous=True`
switch.** Three variants of `Code/Fix_FreedHousingNotice.lua`, each run through BOTH harnesses via a driver that
redirects only the "shipped" shape (the pre-repair shape still comes from git at `bb50f5d`):

| variant | what I reverted | interact | expedition | reading |
|---|---|---|---|---|
| A · inline | `CreateGameTimeThread(notify_freed_home, left)` → `notify_freed_home(left)` | **18/23** — the four A2 "REPAIRED" legs FAIL, overfill returns | **13/18** — the four A1 "REPAIRED" legs FAIL, hold lost | the deferral IS the repair |
| B · no `destroyed` | both `destroyed` tests removed | **20/23** — the three A3 legs FAIL, the non-resident is dragged in again | 18/18 (A3 is not an expedition shape) | the A3 guard is load-bearing and specific |
| C · silent | thread never scheduled | **20/23** — benefit legs FAIL ("infopanel kick DOES still offer the freed bed") | **15/18** — "ordinary departure is STILL notified" FAILS | the benefit legs have teeth; a silent removal cannot pass |

So every harm the build claims to fix has a leg that fails on the unrepaired shape, and the benefit has a leg that
fails on a removal. Driver and variants are in this session's scratchpad, not the repo (they are one-offs).

## 1 · Disagreements first — numbered, falsifiable

Each: verdict · `file:line` on 1.1.0.403908 · `SOURCE`/`INFERRED`. "Disagreement" includes places where I confirm a
claim the record holds only tentatively, because that changes what the next session may lean on.

1. **Link 01's caller enumeration is complete for the WHOLE tree, not just `Lua/`.** `CONFIRMED` · `SOURCE`. A grep
   of `Lua/`, `Data/`, `DLC/` and `CommonLua/` returns the same 11 call sites (`Data/TraitPreset.lua:772` is the one
   outside `Lua/`), one definition (`Colonist.lua:2898`), and the only override on the path is
   `NaturalHabitatBase:KickResident` (`NaturalHabitat.lua:5-8`), which link 01 had. No DLC touches
   `SetResidence`, `KickResident`, `CheckHomeForHomeless` or `GetFreeSpace`.
2. **`Residence.lua:265` is SAFE, recomputed.** `CONFIRMED` · `SOURCE`. The loop at `:257-268` runs only while
   `#reserved + #colonists > capacity - closed`; after `RemoveResident` inside `SetResidence` the sum is one lower,
   so `GetFreeSpace` (`:232-234`) is `Max(0, ≤0)` = 0 at every hook call and the pre-filter declines. Zero threads.
3. **A3's three entry paths are each closed, and the ordering claim holds.** `CONFIRMED` · `SOURCE`.
   `Building:Destroy` sets `self.destroyed = true` at `Building.lua:1560` and calls `OnDestroyed` at `:1576`;
   `Residence:Done:78` and `Building:Refabricate:1873` → `OnRefabricate:1870` → `DoneObject:1889` leave the object
   invalid before any thread can wake. `MicroGHabitatBase:OnDestroyed` (`MicroGHabitat.lua:43-52`) reaches the hook
   through `SetDome(false)` → `Colonist.lua:435` and is covered by the same two facts. The whole-tree list of
   `:OnDestroyed()` call sites has no fourth path onto a residence.
4. **The A1 leg has no yield between the slot freeing and the hold.** `CONFIRMED` · `SOURCE`. From `Colonist.lua:435`
   to `:5005`: the rest of `SetDome` (`:436-463`), the one `ColonistLeavesDome` handler (`StatusEffects.lua:50-55`),
   `ClearDetrimentalStatusEffects` (`:1000-1010`), `Unit:EnterTransporter` (`Unit.lua:1292-1306`), `Unit:Disappear`
   (`:1199-1225`) and `Colonist:OnDisappear:4992-5002` contain no `Sleep`/`Wait*`/`PlayState`. The deferred body
   therefore cannot run before `:5005` on a cooperative scheduler. (`OnDisappear:4995` is a no-op by then —
   `SetDome` already cleared `residence`, so `:2901` returns.)
5. **The widest input the new guard suppresses that the old one would have notified is a DESTROYED residence — and
   vanilla does not want that one.** `CONFIRMED` · `SOURCE`. Old guard (`bb50f5d`): `ui_working ∧ GetFreeSpace()>0`,
   evaluated inline. New: the same pre-filter plus `not destroyed`, then re-evaluated after the wake plus
   `parent_dome`. `parent_dome` drops nothing (`CheckHomeForHomeless:161` already yields `empty_table` without one).
   `destroyed` drops only rubble. The re-check after the wake can only decline when the bed is no longer free or the
   home was switched off in the gap, and in both cases there is nothing to offer (`SetUIWorking(true):173` notifies
   on its own when it comes back). I could not construct a reachable input where the repair withholds a bed vanilla
   would have wanted offered. **The benefit is intact.**
6. **`Sleep(0)` is not load-bearing for the ordering, only for the latency — and it is unmeasured.** `UNRESOLVED` ·
   `INFERRED`. The ordering rests on `CreateGameTimeThread` itself deferring (EF-029, MEASURED); `Sleep(0)` only
   decides how soon after that the body runs. It appears once in the shipped tree (`TutorialsNew.lua:2302`) and
   nothing in `CommonLua/LuaExportedDocs/Global/thread.lua:49-52` says what a zero sleep does. Stakes: if it wakes on
   the next tick, the benefit is "immediate"; if the engine treats 0 as a frame or more, the benefit is still hours
   ahead of `Clamp(#Colonist/300, 0, 12)` h. No harm shape depends on it. Link 01 named this as its least-sure point
   and I agree it is the right one; it is settled only by a boot.
7. **The `OnDestroyed` UNRESOLVED lead is STRONGER than the record says, and it is vanilla's.** `UNRESOLVED` ·
   `SOURCE` for the mechanism, `INFERRED` for the outcome. `Building:Destroy` (`Building.lua:1544-1625`) neither
   removes the building from any label nor clears `ui_working` (`:1570` clears `working`); `Residence:OnDestroyed:89`
   empties `colonists`, so `GetFreeSpace` reads the full capacity; `ChooseResidence` (`Residence.lua:437-467`) filters
   on `ui_working` and free space only, never `destroyed` (contrast `MicroGHabitatBase:ChooseResidence:164`, which
   does, and `Dome.lua:2557`, which filters `destroyed` for a different enumeration). ⇒ at source, vanilla's own
   homeless heavy update can assign a colonist INTO a destroyed residence, and `:86` does so mid-eviction. NOT
   sampled in play; a candidate C-entry, owner's call (ideas list).
8. **The report's F59 §1 line citations into our module are stale.** `CONFIRMED` · `SOURCE`. It cites
   `Fix_FreedHousingNotice.lua:66-79`; the wrapper now starts at `:266`. Cosmetic; the report is Astra's record and
   was deliberately not retrofitted (link 01 §3). Anyone quoting it to a developer should cite the module by name.
9. **Deferral vs `FIX_POLICY` §1.4 — link 01 chose right, and the policy text should say so.** `CONFIRMED` ·
   `SOURCE`. §1.4's letter prefers "a guard keyed on that caller's own state, not a later cleanup pass"; both
   caller-keyed shapes were measured wrong here (`KickResident` has three callers, `Residence.lua:368` +
   `sectionOccupantList.generated.lua:34` + `sectionResidenceList.generated.lua:34`, two benign;
   `user_forced_residence` lives a sol, `__const.lua:171-177`). Deferral is not a cleanup pass — nothing is
   published until the operation ends. Ideas list: amend §1.4 to admit "act after the enclosing operation has
   unwound" as a caller-agnostic guard, with the yield-free-continuation condition (item 4) as its precondition.
10. **The repair holds on 1.0.7 too, which matters because the portals serve ONE version.** `CONFIRMED` · `SOURCE`
    (archive `C:\Dev\SMR-SrcArchive\1.0.7.396349`). `Residence:GetFreeSpace` subtracts `reserved` (`:198-200`),
    `ColonistInteract` kicks at `:310` and assigns at `:316`, `Building:Destroy` sets `destroyed` at `:1473` before
    `OnDestroyed` at `:1489`, and there are 11 `SetResidence` call sites. A2 and A3 are 1.0.7 shapes and the deferral
    closes them there by the same mechanism; A1 does not exist on 1.0.7 (no `expedition_residence`). The frozen
    `v5-game-1.0.7` download still carries the pre-repair body (ck151 e, unchanged).
11. **§3a: "zero upvalues" is true of every name the body reads except `_ENV`.** `CONFIRMED` · `SOURCE`. Every Lua
    function closes over its environment; in an orphan save that is the fallback `LuaModEnv` (EF-023), so
    `SMRFixPack` resolves to nil and the gate at `:254` returns. Same footing as every other §3a-gated thread in the
    pack. `reports/D13_EXPOSED_SET.md` §2a still owes the row (E-numbered); not added here — D13 derives its own set.
12. **H-02 held; the build commit touched neither release file.** `CONFIRMED`. `git show --stat 3b41d9f` lists 12
    files, none of them `metadata.lua`/`items.lua`; the uncommitted `version 7 → 8` / `pdx_version "7"` /
    `saved 1789159802` diff in the tree is the owner's own Mod Editor writeback (comments stripped, both files), the
    expected post-sitting state, and I did not touch it.

### Surface sweep of Astra's eight verdicts (three questions each; PARTIAL rows first)

| module | cited line says what the report says? | conclusion follows? | absence claims one-sided? | my label |
|---|---|---|---|---|
| **F60 §7** | YES — `GatherFreeLivingSpaces` gates on the parent dome too (`_GameUtils.lua:541-544`); births `Community.lua:212`/`:323` and migration `Colonist.lua:3439`/`:3464`, arrivals `_GameUtils.lua:492`, `UniversalRocket.lua:2226` all go through `HasFreeLivingSpaceFor:402-418` / `HasAnyFreeLivingSpace:366-384`, which iterate residences on `working` and never read the tally; assignment `Residence.lua:452` reads `ui_working`; `PrepareApplicantsForTravel:137` → `GetAvailableResidencesFor:89-124` reads the tally and its `filters` (`:102-103`) and gates the housing popup at `:150-169` | YES | **NO — I enumerated the presence side.** `GetFreeLivingSpace(` has 9 call sites in the whole tree (Dome `:2600`, `:3358` deprecated, `:3877`, `:3908`, `:4283`; RocketUtilities `:102`; ColonyControlCenter `:1320`, `:1330`; `_GameUtils.lua:363` → CargoRequestNew `:358` and LanderRocketCargoRequest `:215`, both inside `is_asteroid_target` branches as the report says, plus `Traits.lua:205` and `ResupplyPassengersSummary.generated.lua:67-74`, UI). `Dome:HasFreeLivingSpace` (`:3357`) has NO caller in Lua/DLC/Data. `overpopulated` is a homeless-count test (`Dome.lua:1329-1331`), not tally-derived. | `SOURCE` throughout; the "can suppress the warning" step is correctly `INFERRED`. **Retirement is defensible; the trace would sustain B.** But see finding 13. |
| **F51 §2** | YES — cache keyed on community × pos (`Colonist.lua:3197-3203`), computed from `shuttles_available` (`:3111-3119`), invalidated by train/dome/rocket events only (`:3124-3149`); `BuildReachableGraph:3408` reads `IsLRTransportAvailable` directly; `FindEmigrationDome:3524-3525` consults the cache after choosing; `TryToEmigrateToDome:1959-1970` creates a shuttle task with no test of the cached mode | YES — a stale `false` no longer blocks emigration on its own | the "which remaining caller turns this into harm" question is left open, correctly | `SOURCE` mechanism, `INFERRED` narrowing; PARTIAL stands |
| **F52 §3** | YES — `Colonist.lua:1898-1912`: in vacuum `min_dist` is the dome walk cap and the passage lookup runs only above it; `:1914-1928` still walks when no passage exists | YES | n/a | `SOURCE`; PARTIAL stands |
| **F53/C83/F117 §4** | YES — `Colonist.lua:1612-1628` places at the rocket spot and commands the walk; `_GameUtils.lua:403-407` now skips negative foot routes; `ChooseDome:486-500` keeps `safety_dome` as the default | YES; C83's witness is the attended 09-10 log, not a desk result | n/a | `SOURCE`; PARTIAL stands |
| **F58 §6** | YES — `ColonistTransportTask:IsObsolete` (`LRTransport.lua:43-59`) expires uncommitted tasks by `creation_time`, committed rides exempt; `LRManager:50-62` releases through `ClearTransportRequest:2036-2038`; `TransportByFootDtor:3529-3539` cancels no reservation | YES | "no residual reproduced" is stated as unknown, not as absence | `SOURCE`; PARTIAL stands |
| **F73 §8** | YES — `Rest:2578-2581`, outside timer `:3015-3026`, suffocation `:4575-4578`, `Roam:1493-1512` enters a stand-alone habitat, `MicroGHabitatBase:ChooseResidence:162-171` keeps the current one | YES | n/a | `SOURCE`; PARTIAL stands |
| **F54 §5** | not re-read beyond the report (STILL NEEDED, no player-surface change) | — | — | not swept, by name |
| **F59 §1/§1a** | lowest value per the brief; the citations I read for the build (above) are the same ones | YES | YES — the "vanilla puts nothing in that window" absence was already enumerated by the ck151 re-derivation (`CheckHomeForHomeless` callers `:64`, `:173`, `:214`, `Hotel.lua:23`; I re-grepped: same four plus the `:203` alias) | `SOURCE` |
| **F80 §13** | YES — `TrainTransport.lua:373-378` raw index difference, `:397-409` endpoint wrap, `:422` return on missing edge, `:453` stride | YES | n/a | `SOURCE`; **nothing in `3b41d9f` touches a train file — capture-before-mitigate holds** |

13. **⛔ The F60 fix-list row is FALSE on 1.1.0 whether or not F60 is retired.** `REFUTED` (the row) · `SOURCE`.
    `SMR-CommunityMods/content/fix-list.md:113-122` says births and new arrivals were refused because the gate read
    the running-only tally, and "After the fix: they agree." On 1.1.0 the gate never reads the tally (finding table,
    F60 row) and with the pack the tally (`ui_working`) and the gate (`working`) still disagree. The row describes a
    repair the module no longer performs. The F51 row (`:82-91`, "building a hub is noticed, and the colonists
    move") and the F58 row (`:103-112`, reservations "had no expiry at all") overclaim on 1.1.0 for the reasons in the
    table. These are `prompts/perma/PUBLIC_SURFACE_SWEEP.md` work and are NOT in this chain; I name them because the
    brief said a wrong PARTIAL row reaches the player surface, and this one already has.

## 2 · Upload verdict

**SHIP A.** The F59 repair stops all three measured harms, keeps the benefit, is falsifiable in both directions on the
shipped bodies, holds on both game branches, and touched no release file. What it does NOT have is a boot: no sitting
has seen `[CommunityFixPack] … FreedHousingNotice … applied`, and `Sleep(0)`'s latency is a model. The post-release rule
(STATE "Rules in force": one boot `applied` log) is the gate that remains, and the four-click receipt in checklist 152
settles A2 in play in under a minute.

**B:** not built, not graded as a build. The trace Astra wrote for F60 §7 sustains at source with the presence side
enumerated (table above), so when the owner lands or drops the two v8 files the retirement can proceed as proposed —
but the fix-list row needs correcting first and regardless (finding 13).

**Retire-instead-of-repair?** No. §4a who-benefits, stated: retiring loses the immediate offer of every genuinely freed
bed (death, retirement, dome change, the infopanel kick), which at 3,600+ colonists is up to 12 hours per bed
(`City.lua:117-119`); keeping the repaired module loses nothing I could construct (finding 5). The owner's lean is
sustained by the evidence, not merely honoured.

## 3 · Ideas — suggestions, not defects

- **Amend `FIX_POLICY` §1.4** to admit deferral as a caller-agnostic guard (finding 9), with "no yield between the free
  and the re-take" as its stated precondition and the manifest rows that pin it as the example.
- **File the destroyed-residence assignment as a C candidate** (finding 7): vanilla's `ChooseResidence` can pick a
  destroyed residence; `MicroGHabitatBase:ChooseResidence:164` shows the authors' intent. Desk-only until a save shows it.
- **Promote `Building.lua:1560 → :1576` (destroyed before `OnDestroyed`) to an EF** — link 01 asked; I agree, it is
  load-bearing for A3 on both branches (1.0.7 `:1473 → :1489`).
- **Add the D13 §2a row** for `notify_freed_home` (finding 11) the next time D13 is re-derived.
- **`Sleep(0)` micro-measurement** could ride the owed sitting: one console line creating a GT thread that logs
  `GameTime()` before and after `Sleep(0)`. Cheap, and it turns finding 6 from a model into a number.
- **Thread fan-out** is bounded by the number of `SetResidence(false)` calls with a free slot, one one-shot thread each;
  a mass death creates as many threads as the old module made inline calls. Not a defect; noted so nobody re-derives it.

## 4 · Not checked, by name

- `Building:UpdateOccupation` (`Building.lua:3276-3318`) and `Community:ResetFreeSpace` (`:361-364`) as cited in report
  §1a — the ck151 re-derivation read them; I did not re-open them.
- **F54 §5** (STILL NEEDED) — not swept; no player-surface change rides on it.
- **Sections 9–12** of the report (F61/F62/F63/F79 policy observations) — outside the eight verdicts' player surface.
- **`Sleep(0)` semantics** — finding 6, needs a boot.
- **Any in-play reproduction** of A1, A2 or A3 on either branch — none exists; ck152's receipt is the first.
- **Paused-game and save-inside-the-window behaviour** of the deferred thread — reasoned by link 01 (EF-019 persistence,
  orphan gate first after the yield), not measured by either of us.
- **The TestKit probe's rewrite** (`4d34735` in `C:\Dev\SMR-BugFixPack-TestKit`, a repo with NO remote — invisible to
  this repo's log and to any push) beyond `desk_probes_f67_f59.py`'s 10/10, which already shows it FAILs on an inline
  wrapper and on an over-broad one.
- **A save/load A/B across the `Sleep` window** — link 01 named it as the sharpest control it did not build; still unbuilt.
- **`items.lua`/`metadata.lua`** — read (owner's v8 writeback, `version 7 → 8`), not verified further, not touched.

## 5 · What this commit changes

This report · checklist 152 addendum (verdict + the two decisions) · `bugs/F59.md` and `bugs/F60.md` appendices ·
`STATE.md` one line · `prompts/README.md` row · `git rm` of `prompts/migrationfix/02_AUDIT_fable.md` and
`prompts/migrationfix/README.md` (chain finished; the HANDOFF survives in git at `3b41d9f`). No code, no release file.
