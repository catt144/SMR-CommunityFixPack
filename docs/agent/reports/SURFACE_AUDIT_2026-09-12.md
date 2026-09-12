# Surface audit — the two retirements, the F31 dig, the 14 ruled sentences

**2026-09-12, session `smr-bugfixpack-07`, firing `prompts/SURFACE_AUDIT_FABLE.md` (grave: the commit that lands this
file).** Desk only: no game launched, no public surface, `Code/`, `items.lua` or `metadata.lua` touched. Trees: live
`A:\SteamLibrary\steamapps\common\Project Spark\ModTools\Src` = **1.1.0.403908** (`EF-075`); archive
`C:\Dev\SMR-SrcArchive\1.0.7.396349\Src` = **1.0.7**. Every citation names its version. Verdict words: CONFIRMED /
REFUTED / UNMEASURED. "Codex" = the still-needed sweep (`reports/STILL_NEEDED_SWEEP.md` + `still-needed/*.md`).

**New instrument, and the reason F31 is settled rather than swept:** every prior audit (REACHABILITY_AUDIT R3, BLIND_AUDIT,
Codex) left one hole open — the per-map `anomaly_sequence_list_names` live in binary map data no one had read. This audit
pulled `mapdata.lua` out of all **142** `Packs/Maps/*.fpk` with the project's own FLPK parser (`tools/flpk_extract.py`,
scratch script, nothing committed) and read the compiled chunks' string constants. A compiled chunk stores only
non-default properties, so a key's presence means it was set (`IsRandomMap` default false, `CommonLua/Classes/MapData.lua:204`;
`GameStates` default false, `:183`; `map_location_exclude`, `Lua/ClassDefs/ClassDef-Default.generated.lua:127`).

---

## 0 · Disagreements first

| # | with | claim | my finding |
|---|---|---|---|
| D1 | Codex (F31 KEEP-BUT-FIX-CLAIM) | the cheap guards should stay as insurance | **RETIRE.** Both halves of F31 are unreachable on 1.1.0 and the mapdata closes the hole Codex named. The `UndergroundAnomalies` list is declared by exactly the **16 underground blanks** and by no surface (41, all `MarsAnomalies`) or asteroid (20, all `GenericAnomalies`) map; the four `BuriedWonder_*` lists are on **no** map at all (wonders come only from the Underground-gated generator). §2 C2–C6. |
| D2 | WORDING_RULED item 3 (F58) | "a bed could stay reserved for a colonist who had **died, left, or moved to another dome**" | **Two of the three cases are vanilla's own release paths.** Death: `Colonist:Die`'s destructor calls `ClearTransportRequest` (`Lua/Units/Colonist.lua:1288`@1.1.0) whose first act is `CancelResidenceReservation` (`:2037`); `Erase` likewise (`:1250`). Moving in elsewhere: `Residence:AddResident` cancels the unit's reservation (`Lua/Buildings/Residence.lua:110`). The defect is the colonist who **never arrives** (committed-shuttle limbo, the walk path — `Code/Fix_StaleReservations.lua:73-82`). Replacement in §3 item 3. |
| D3 | WORDING_RULED item 1 (F54) | "Only hubs that are on and **able to fly** count" | Stronger than the module. The strict test is `hub.working or (hub.ui_working and permitted-reason and not possible-reason)` (`Code/Fix_ShuttleHubOffAvailable.lua:86`): a hub the **game** has paused (maintenance, exceptional circumstances) still counts, on purpose (entry F54, the four-state enumeration). The dropped sentence was the true one. Replacement in §3 item 1. |
| D4 | WORDING_RULED item 12 (F48) | "If the sort fails on a track, that track is **put back the way it was**" | Overstates. On failure the engine restores only the element **order** (`Lua/Tracks.lua:617-620`@1.1.0 copies `all_elements` back); `connections` and `node_idx` rewritten at `:578-579`, `:602`, `:610` stay rewritten, and the failure is an `assert` that does not unwind, so the sanitizer's `pcall` (`Code/90_SaveSanitizer.lua:224`) sees no error on that path. The entry's own 09-12 note says this ("pcall is isolation, not exact rollback"). Replacement in §3 item 12. |
| D5 | Codex + the brief (F37 residuals) | "refab during the last worker's dying window" is unmeasured; "1.0.7-born saves cannot load (`EF-079`), so that constituency is closed" | **The dying window is closed, not unmeasured**; the 1.0.7-save constituency is closed **on Steam only**. §2 A3. |
| D6 | Codex (F43 "cached-admission race" as an open limit) | an inventory change between the menu check and activation could admit a locked entry | Bounded, not open: it needs a layout entry that is tech-locked **and** has no unlocked resupply item **and** a prefab count that drops between the menu build and the click. No shipped entry qualifies (both locked entries are Moisture Vaporators with an unlocked resupply item, `Data/Cargo.lua:327-336`@1.1.0), so it is the same latent shape F43 always was. §2 B2. |
| D7 | WORDING_RULED item 14 (F73) | "a colonist **with a home** who is idling out in vacuum is sent home" | True only for a **working** home: the reflex requires `IsValid(self.residence) and self.residence.working` (`Code/Fix_ShelterReflex.lua:101`). Minor; plain alternative in §3 item 14. |

Everything else in the ruled batch is CONFIRMED as written (§3).

---

## 1 · What this audit did not do

- Launch the game, load a save, or run the TestKit. Every verdict is SOURCE + map data. No screen claim is made.
- Read 1.0.7's **underground** map data: the four `BlankUnderground_0x.fpk` were overwritten on 2026-09-08 (1.1.0). The 41
  surface blanks include files untouched since 2026-03-21, which are the 1.0.7-era data (claim C5 relies on those).
- Read mod-added maps, scenarios, rules or layouts. `Packs/Maps/Mod.fpk` is an editor stub with no anomaly list.
- Prove `map_location_exclude`'s stored value: bytecode presence ⇒ non-default ⇒ true (default false at
  `ClassDef-Default.generated.lua:127-128`@1.1.0); the value byte itself was not decoded.
- Re-run the 46-module sweep, or re-derive the site's 49 rows beyond the 13 the batch touches.
- Check `DLC/` for anything but layouts, farms, crops and scenario lists (all grepped; none relevant).

---

## 2 · The deep half

### Claim A — F37 `Fix_GhostFarmOxygen` is redundant on 1.1.0 (owner: RETIRE) — **CONFIRMED, with one named remainder**

- **A1 CONFIRMED — 1.1.0 applies the modifier only while working and clears it on the working edge.** All three
  `ApplyOxygenProductionMod` calls gate on `self.working` (`Lua/Buildings/Farm.lua:165`, `:630`, `:648`@1.1.0); the
  function itself writes the keyed modifier to 0 when handed no crop (`:641`). On 1.0.7 the `SetCrop` path was ungated
  (`Farm.lua:557`@1.0.7: `self:ApplyOxygenProductionMod(self.harvest_planted_time and crop)`), which was the whole leak
  window (a planted, never-worked farm salvaged).
- **A2 CONFIRMED — every ordinary removal clears before the dome detaches.** Salvage funnels into `Building:OnDemolish` →
  `Destroy` (`Lua/Buildings/Building.lua:901`@1.1.0); `Destroy` sets `destroyed` (`:1560`) and calls `UpdateWorking(false)`
  (`:1570`) → `GetWorkNotPossibleReason` = "Destroyed" (`:625`) → `SetWorking(false)` → `OnSetWorking(false)`
  (`BaseBuilding.lua:447-462`) → `Farm.lua:165` → `:641` clears, with `parent_dome` still set. `SetDome(false)` runs only
  from `Building:Done` (`:537`), later. Meteor/sabotage/refab-of-dome all reach `Destroy` or destroy the dome itself.
- **A3 — the residue, measured.**
  - *Dying-worker refab window* (Codex: unmeasured): **CLOSED.** `dying` is set in exactly two places, the `Die` destructor
    (`Lua/Units/Colonist.lua:1290`) and `Erase` (`:1252`), and each calls `SetWorkplace(false)` in the same synchronous
    block (`:1296`, `:1254`) — there is no yield between them, so `KickAllWorkers`'s `IsDying` skip
    (`Lua/Buildings/Workplace.lua:962`) can never see a listed worker.
  - *Refab of a working farm:* **CLOSED on shipped data.** `Refabricate` → `OnRefabricate` → `FarmBase:OnDestroyed`, which
    chains `Workplace.OnDestroyed` (`Farm.lua:416-420`) → `KickAllWorkers` → `RemoveWorker` → `SetWorkplaceWorking`
    (`ShiftsBuilding.lua:172-180`) → `UpdateWorking` → `HasWorkforce` false → modifier cleared, all before `DoneObject`
    (`Building.lua:1889`) → `Done` → `SetDome(false)`. A worker-free working farm would need `automation > 0` or
    `max_workers == 0` (`Workplace.lua:185`): no farm template sets `automation`; the automation upgrades floor at 4/2/4
    (`Data/BuildingTemplate/Farm.lua:39`, `HydroponicFarm.lua:61`, `FungalFarm.lua:54`; DLC 1/1/4, `DLC/norman/…/FarmSmall*.generated.lua:22`,
    `FarmUnderground.generated.lua:22`); the only `max_workers = 0` farm is the DLC Automated Farm, which is
    `dome_forbidden` (`AutomatedFarm.generated.lua:18`, `:39`) and so never has a `parent_dome` (`Farm.lua:635` returns).
  - *Scripted `SetDome`/`DoneObject` from console or another mod:* **UNMEASURED and unbounded** — the only route left.
  - *The LoadGame sweep's constituency:* a 1.1.0-born save can carry an orphan only through the route above. The brief's
    "1.0.7 saves cannot load (`EF-079`)" is true **on Steam**: `config.OldSavegameBehavior = Platform.steam and "block" or
    "warn"` (`Lua/Config/config.lua:175`@1.1.0) and off Steam the load dialog offers "Load anyway"
    (`CommonLua/SavegameMetadata.lua:164`). `EF-079` records the Steam refusal only. So a PDX/console player carrying a
    1.0.7 save with a phantom modifier loses the sweep's healing when the module retires. The same fact already governs
    the sanitizer (`Code/90_SaveSanitizer.lua:18-30`), where the owner kept the passes (ck117). **Owner's call, §5.**
- External witness: the PDX developer could not reproduce it (ck150) — consistent with A1/A2.
- Where I agree with Codex: A1, A2, the reader being `Dome.lua:1881`. Where I disagree: D5. What neither checked: nothing
  further that is reachable from shipped Lua; scripted routes are unbounded by nature.
- 1.0.7 players on the live pack (the portals serve one version, ck151 (e)): the 1.0.7 leak is real and returns for them.
  Already ruled (frozen v5 keeps the module; live pack tracks 1.1.0). Stated, not re-litigated.

### Claim B — F43 `Fix_LayoutTechLock` + F118 rider are redundant on 1.1.0 (owner: RETIRE) — **CONFIRMED**

- **B1 CONFIRMED — the outer gate exists and runs before both ordinary activations.**
  `GetLayoutConstructionMissingBuildings` checks each entry's tech status and compares the missing count with owned prefabs
  (`Lua/Construction/LayoutConstruction.lua:207-234`@1.1.0); `GetLayoutConstructionLockedReason` turns that into the lock
  text (`:268-297`). `UIGetBuildingPrerequisites` asks it for every `LayoutConstructionBuilding` (`Lua/X/BuildMenu.lua:743`)
  and sets `can_build = false` (`:784-786`); the item action returns on a disabled item unless a whole-layout prefab is
  owned (`:836-846`). The keyboard shortcut goes through the same call and passes `can_build` into the same action
  (`Lua/XDef/GameShortcuts.generated.lua:2069`, `:2082`). Absent on 1.0.7 (0 hits for either helper in the archive).
- **B2 CONFIRMED — callers of the HOOKED function, `LayoutConstructionController:Activate`, enumerated (the F59 lesson):**
  1. `ConstructionModeDialog:OnStartup` (`Lua/Construction/Construction.lua:302`) — the only in-game path, reached by
     `SetMode(template.construction_mode)` with `construction_mode = "layout"`; three `SetMode` sites feed it:
     `BuildMenu.lua:859` (gated above), `GameShortcuts.generated.lua:2082` (gated above), and `CopyBuilding`
     (`Lua/X/Infopanel.lua:457-495`), gated by `CanCopy` → `UIGetBuildingPrerequisites` (`Lua/Buildings/BaseBuilding.lua:1131`)
     and moot for layouts, which leave no `LayoutConstructionBuilding` object to copy. The other `SetMode` literals
     (`"construction"`, `"track_grid"`, `"passage_ramp"`) never select the layout controller (`ConstructionControllers.lua:79`).
  2. `RegisterLayout` (`LayoutConstruction.lua:20`) — reached only from the Ged editor RPCs (`:37-49`). Not a player route.
  - Inheritors: **0** subclasses of `LayoutConstructionController` (grep `__parents.*LayoutConstructionController`, Lua+DLC).
  - Layout presets: **1** populated (`SelfSufficientDome`, `Data/LayoutConstruction.lua:3-54`) + the empty `testing`; **0** in
    `DLC/norman`, `DLC/thomas`. Live DLC overrides: none (0 hits for `LayoutConstruction`/`LayoutList` under `DLC/`).
  - The race (D6): bounded to a non-shipped entry shape.
- **B3 CONFIRMED — F118 has no standalone job.** Vanilla's `Activate` creates no controller for an entry it skips
  (`:346-379` only runs under `add`), so nothing vanilla calls `ConstructionController:Deactivate` (`Construction.lua:1226-1227`)
  before the registration at `:385`; the only disturbance is our teardown (`Code/Fix_LayoutTechLock.lua:119-134`). Retiring
  F43 retires the disturbance and the rider with it. F118 stays `filed`, never reproduced; nothing to keep.
- **B4 CONFIRMED — consumers.** In `Code/`: one comment (`Fix_ArrivalDeaths.lua:343`). TestKit: `LayoutTechLock`
  (`50_Probes_Wave5.lua:183`) and a hook-census row (`64_Probes_Wave14.lua:130`) retire with the module.
- Where I agree with Codex: all of it. Where I disagree: D6 (it is bounded). What neither checked: a running colony.

### Claim C — F31 `Fix_AnomalyCaveInMap` — **DIG. Verdict: RETIRE. Neither half is reachable on 1.1.0.**

- **C1 — was the stop ever observed? No.** The entry is source-derived end to end (`bugs/F31.md`: "Confirmed, and wider
  than recorded", from grep). `REACHABILITY_AUDIT.md:528-536` (07-30): "no player report", R3. `BUG_LIST_AUDIT.md:163`:
  B2 UNREP, and the one witness ever offered (an asteroid cave-in quote) was **rejected** as fitting C02, not F31.
  `BLIND_AUDIT.md:272` could not settle reachability. The kit probe `AnomalyCaveInMap` (`50_Probes_Wave5.lua:400`) hands
  the wrapper a literal `false` — an instrument test, not an observation. **No save, no log, no report exists.** The public
  row's "What you saw" (`fix-list.md:561-570`) was written from source.
- **C2 CONFIRMED — the rule route is closed on 1.1.0.** `NoUndergroundAndAsteroids` carries `Obsolete = true`
  (`Data/GameRuleDef.lua:53-63`@1.1.0; the 1.0.7 definition `:59-68` has no such flag). `ForEachPreset` skips
  `preset.Obsolete` (`CommonLua/Preset.lua:1773`), `PresetArray` is built on it (`:1783-1789`), and the new-game rules combo
  is `PresetArray("GameRuleDef")` (`Lua/GameRules.lua:2`); `ForEachActiveGameRule` walks `Presets` raw precisely so an
  obsolete rule survives only "still active in loaded games" (`:71-76`). A 1.1.0 game cannot be created under the rule;
  a 1.0.7 game under it cannot be loaded on Steam (`EF-079`) — off Steam it can (A3), and that case is settled by C5.
- **C2b CONFIRMED — the "non-Surface map" route is closed for a player.** The underground map is generated only from a
  Surface start (`Lua/RandomMap/RandomMapGenerator_Picard.lua:285-311`@1.1.0: `GetEnvironment(CurrentMap) == "Surface"`),
  and `UndergroundMap` is assigned in exactly one place, that generator's `on_map_generated` (`:303`; whole-tree grep).
  The new-game picker takes `IsRandomMap and not map_location_exclude` (`Lua/UI/PreGameMenus.lua:47-48`); in the map
  data all **41** surface blanks lack the exclude key and all **16** underground + **20** asteroid maps carry it
  (`GameStates` = Underground / Asteroid; surface maps have no `GameStates`, so `GetEnvironment` defaults to "Surface",
  `Lua/MapData.lua:57-72`). A non-Surface start exists only for the developer harness (`Lua/AgentPlayTest.lua:1`,
  `Platform.developer`) or a mod.
- **C3 CONFIRMED — the eight sequences run only on the underground map, so the sequence-local `map` IS `UndergroundMap`.**
  Sequences start from anomaly objects on the map that owns them (`Lua/Buildings/Anomaly.lua:141-156`: `PlaceAnomaly(…,
  self:GetMap())`; the list script's `Create = function(map)` binds that map, `Lua/Scenario/*.generated.lua:7`). The
  `UndergroundAnomalies` list (site :241, "Shivering stalactite") is declared by `anomaly_sequence_list_names` on the 16
  underground blanks and nowhere else; the four `BuriedWonder_*` lists are on no map — the wonder buildings carry them
  (`Data/BuildingTemplate/JumboCave.lua:23`, `CaveOfWonders.lua:23`) and are placed only by
  `RandomMapGen_PlaceArtefacts_UndergroundWonders` under `GetEnvironment(env.map) == "Underground"` (`Picard.lua:201`).
  The surface `BuildingAnomalies` scenario does spawn one `UndergroundAnomalies` sequence ("Hole in the ceiling resource",
  `BuildingAnomalies.generated.lua:55-59`), and that sequence has no cave-in step (the file's only `TriggerCaveIn` is
  `:241`). `UndergroundAnomalies_Rare`/`_FollowUps`: no `TriggerCaveIn`. There is one underground map per colony
  (`PickUndergroundMap`, `:270-281`; `map_slot = 2`). ⇒ the global and the local name the same object; the wrong-map half
  cannot occur, and the missing-map half needs a sequence that cannot exist without the map it runs on.
- **C4 CONFIRMED — both trees, all eight sites, and what `false` does.** 1.1.0: `UndergroundAnomalies.generated.lua:241`,
  `BuriedWonder_Jumbo_Cave.generated.lua:340/543/776`, `BuriedWonder_Jumbo_Cave_106.generated.lua:339/542/775`,
  `BuriedWonder_Cave_Of_Wonders.generated.lua:431` (twice). 1.0.7: `:240`, `:340/539/769`, `:339/538/768`, `:430`.
  `TriggerCaveIn` guards `pos` and then calls `map:MapFindNearest` unguarded (`Lua/Buildings/CaveInRubble.lua:103-109`@1.1.0;
  `:95-101`@1.0.7); `FindCaveInLocation` indexes `map.buildable` (`:21-23`@1.1.0; `map.object_hex_grid` `:21-27`@1.0.7).
  Handed `false` either raises. The engine's own callers pass a real map (`Lua/Marsquake.lua:292-295`, `:319`@1.1.0).
- **C5 — could a 1.0.7 player under the rule have hit it? No.** The rule skipped the underground map on 1.0.7 too
  (`Picard.lua:266`@1.0.7 `return`; wonder/cave-in placement gated `:204`, `:244`), and the surface blanks' data files
  dated 2026-03-21 (pre-1.1.0, unchanged) declare `MarsAnomalies` only. With no underground map there is no underground
  anomaly or wonder to run a sequence, so no call site executes. The frozen v5 build keeps the module regardless (ck156).
- **C6 — recommendation: RETIRE.** No guard with a player-visible reach survives; the row tells players a story stopped
  that no one on either branch could have seen. Module out under H-10 (`items.lua` entry), row `fix-list.md:561-570` and
  the card headline off all five copies, counts re-derived (§4). The kit probe `AnomalyCaveInMap` and the census row
  `64_Probes_Wave14.lua` retire with it. If the owner prefers to keep it as pure insurance for mods, it must then have
  **no public row** — there is no true sentence to write in the voice rule for a symptom nobody can have.

---

## 3 · The surface half — the ruled sentences, one claim each

Checked against the entry, the module header, and the shipped 1.1.0 line. "CONFIRMED" = true on 1.1.0, no stronger than
measured, and in the voice rule. Card copies: `metadata.lua` (1) + `docs/UPLOAD_WORKFLOW.md` (2) +
`docs/agent/reports/STORE_CARD_LIVE.md` (2) = **five**, as the batch says.

| item | verdict | evidence, and the plainer sentence where I offer one |
|---|---|---|
| 1 · F54 | **REFUTED as written** (D3) | Module `Fix_ShuttleHubOffAvailable.lua:86`; entry's four-state enumeration. Offer: **After the fix:** a hub you switch off stops counting. Only hubs you have left switched on count. |
| 2 · F92 Saint | CONFIRMED | Dome-scoped, Religious-only: `Colonist.lua:373/376` (entry F92), module title `Fix_SaintBlessing.lua:398`. |
| 3 · F58 | **REFUTED in one clause** (D2) | Headline and After are true (invalid/desynced/dying released, `Fix_StaleReservations.lua:38-66`; age branch exempts `expedition_residence`, `:44`). Offer **What was wrong:** a bed could stay reserved for a colonist who was never going to arrive — one still waiting for a ride that never came, or one who set off on foot — and those reservations are invisible in the interface. |
| 4 · F52 | HELD | not redone. |
| 5 · F21 | CONFIRMED | `ExitVehicle`: `travel_time = GameTime() - ticket.start_wait` (`ColonistTransport.lua:671`@1.1.0), fed to train and track (`:696-697`); `start_wait` stamped at the platform (`:602`) and charged to the station at boarding (`:622`), never re-stamped; panel line `ipTrain.generated.lua:85`, `ipTrack.generated.lua:186`, `Track.lua:601`; `ChangeComfort` 0 hits in the file. Module re-stamps at boarding (`Fix_TrainWaitTime.lua:120`). |
| 6 · F34 | CONFIRMED | Embark is a drone command (entry F34 07-30 correction; owner-observed 20/20 drones into an RC Commander 08-12); vanilla still passes `callback` not `filter_embark` (`Landscaping.lua:509-523`@1.1.0). ⚠️ The in-game title (`Fix_LandscapeUnitFilter.lua:121`, "boarding colonists") is a `Code/` string — the release lane changes it, not this audit. |
| 7 · F77 | CONFIRMED | `DEBOUNCE = 2000` game-ms (`Fix_ExtenderFlapChurn.lua:56`); separated edges still rebuild (entry 09-12 note) — the sentence says "within two seconds of each other", which is exactly that. |
| 8 · F30 | CONFIRMED | Wrapper assigns `ExitImpassable` after `PlacePrefab` (`Fix_LakeEntombment.lua`, `Unit:ExitImpassable` required); "sent to solid ground nearby" is what that command does when a destination exists. |
| 9 · F06 | CONFIRMED | Hourly `Msg("CrystalFlyAway")` for `10 * const.DayDuration` (`Fix_CrystalMysteryHang.lua:73-83`). |
| 10 · F50 | CONFIRMED | Hourly `HourlyUpdate` → `UpdateCargoResourceRequests` with the disconnect bracket (`CargoTransporterNew.lua:1430-1463`@1.1.0); copy only disconnects when a request is missing (`Fix_RocketDroneChurn.lua:26-30`). |
| 11 · F40 | CONFIRMED | All six DustSickness story bits carry `Obsolete = true` (`Data/StoryBit/DustSickness.lua:12`, `_GeneratSick.lua:47`, `_GeneratSickNotWorking.lua:42`, `_Cure.lua:7`, `_CureFound.lua:46`, `_Deaths.lua:4`); story-bit states are created by `ForEachPreset("StoryBit")` (`Lua/_StoryBits.lua:901-903`), which skips them (`Preset.lua:1773`), and the only `Enables` chains into them start from `DustSickness` itself. Cure-on-load `Fix_DustSicknessBiorobots.lua` LoadGame pass. |
| 12 · F48 | **REFUTED in one clause** (D4) | Vanilla corrected the call (`Lua/Buildings/Station.lua:1504`@1.1.0); the latch skips it on an already-stamped save (entry). Offer **After the fix:** the pass runs properly, once, when you load. A track it cannot sort keeps its old order, and the rest carry on. |
| 13 · F31 | HELD → §2 C6 | — |
| 14 · F73 | CONFIRMED, one word short (D7) | `Fix_ShelterReflex.lua:101-108`. Offer: a colonist whose home is up and running, idling out in vacuum, is sent home once half their oxygen time is gone. |

---

## 4 · The arithmetic (re-derived once from the actual list, 2026-09-12)

- Site rows: **49** `???` blocks in `content/fix-list.md`@`a061665`. F37 = `:257`, F43 = `:611`; F118 has no row. ⇒ **47**
  after the two ruled retirements, **46** if F31 (`:561`) retires. Card word Forty-nine → Forty-seven / Forty-six. ✔
- Card headlines: **21** bullets in the "SOME OF WHAT IT FIXES" block (counted in `metadata.lua:81`); F37's farm line and
  F31's cave-in line are in it, F43 has none ⇒ **20** with F37 out, **19** with F31 out too. ✔ (the batch's "21 → 19"
  presumes F31 retires; say 20 if it stays.)
- "Three of them repair things you cannot see" → **two** (F57a rocket restriction, F29 helpers; F43 leaves). ✔
- Judgment calls: **3** `??? question` rows (`:166`, `:189`, `:437`). ✔ unchanged.
- Modules / files: the batch's 46 → 44 and 47 → 45 hold **for the two retirements alone** — but the sibling C85/C88/C89
  build is landing three new modules in the same v10 (the first, `Code/Fix_CloggedBuildingRelease.lua`, landed in
  `59c8c47` while this audit ran; doccheck already reads 48 files / 47 modules). Derive at apply time from
  `doccheck --emit-counts`, never from this table.
- TestKit (local, not shipped): retire `GhostFarmOxygen` (`20_Probes_Wave2.lua:395`), `LayoutTechLock`
  (`50_Probes_Wave5.lua:183`), the already-orphaned `DomeFreeSpaceMismatch` (`30_Probes_Wave3.lua:464`, F60 left in v9),
  and — if F31 goes — `AnomalyCaveInMap` (`50_Probes_Wave5.lua:400`); plus the hook-census rows in `64_Probes_Wave14.lua`
  (`:110`, `:116-117`, `:130`, and the CaveIn rows if any).

---

## 5 · What the owner must decide (mirrored to checklist 159)

1. **F31: retire** (recommended) — or keep as unlisted insurance with no public row.
2. **F37's load-time sweep and non-Steam players:** the module's retirement also removes the healing for a PDX/console
   player who loads a 1.0.7 save through "Load anyway". The same constituency kept the sanitizer's passes (ck117). Accept
   the loss (recommended: the leak needed a farm salvaged before it ever worked, and the developer could not reproduce
   it), or move the sweep half into `90_SaveSanitizer.lua` as a third pass.
3. **Three sentences to change** before the release lane applies the batch: items 1, 3 and 12 (§3; the offered text is
   written to ship). Item 14 is optional.

---

## 6 · Ideas (not findings)

- Tell the Paradox developers about the eight `UndergroundMap` literals where the sequence-local `map` is meant — harmless
  today, a landmine for any future non-underground cave-in content. Zero cost to them; it belongs in the ck150 reply.
- The map-data string dump (142 packs, seconds) is a reusable instrument; if it is wanted as `tools/mapdata_strings.py`,
  that is a build for Astra, not a paste from this scratchpad.
- The F58 public row could name its two real remaining cases in the "What was wrong" line (offered text does).
- `EF-079` should carry the off-Steam "Load anyway" line (`config.lua:175`, `SavegameMetadata.lua:164`) so the next
  reader does not close the 1.0.7-save constituency on every platform at once. A one-line fact edit; not done here
  (facts are claims, and this audit's scope is the surfaces).
