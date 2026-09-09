# VANILLA-FIX QA — are the "the developers fixed it" claims accurate?

Run 2026-09-08 on the owner's instruction (*"I would rather double check the
devs' work"*), brief `prompts/VANILLA_FIX_QA.md`. Three fresh-context readers
took the 46 REMOVE/FIX rows of `PACK_1_1_0_REVERIFICATION.md` in ranges
(F-1…F-10 + R-1…R-5 / R-6…R-20 / R-21…R-36), formed their own read of the
shipped 1.1.0 code BEFORE comparing with the report, and wrote the six answers
per row below verbatim. The assembling session re-verified the one disputed
verdict (R-20) against the tree itself. Tree `438ac90`. No code written.

## 0 · Synthesis (assembling session)

**Verdicts: 46 rows — 41 CONFIRMED, 4 PARTIAL (F-2, R-25, R-31, R-36:
verdict stands, a stated reason was wrong or incomplete), 1 DISPUTED on
consequence (R-20: the verdict REMOVE stands, but the module is an applies-
today HARM, not an inert redundancy). No REMOVE verdict flipped. No vanilla
replacement was found to be a rebreak.** What the QA changed in the patch plan:

1. **R-20 `DisasterPredictionLeak` moves to the applies-today list.** 1.1.0
   sets `g_DisastersPredicted.DisasterNormalRains` during a normal-rain warning
   with NO notification behind it (`TerraformingDisasters.lua:349`; the id is
   not a notification preset). Our `NewDay` sweep clears any flag without a
   notification (`Code/Fix_DisasterPredictionLeak.lua:97-103`), so on the day it
   lands in that window it cancels the game's own prediction gate and a dust
   storm or cold wave can start on top of the incoming rain (`DustStorm.lua:559`,
   `ColdWave.lua:198` test `IsDisasterPredicted()`). Re-verified by the
   assembling session. The first draft's §1h had this backwards ("the only belt
   for flags without a notification"). Remove the whole module; nothing to keep.
2. **F-5 removal owes a one-shot save cleanup.** Our two `Effect_ModifyLabel`
   entries live in the persisted `UIColony.label_modifiers`; deleting the module
   leaves +10% `production_per_day1` / `water_production` in every 1.1.0 save
   that ran under the pack. Key the cleanup on `prop` + label, as the module's
   own heal already does (`Fix_AstrogeologistExtractors.lua:207-215`).
3. **F-1 repair owes a save re-base.** Vanilla's one-shot
   `SavegameFixups.OrphanedDomeColonistsTraitModifiers` (`_fixup.lua:2143-2170`)
   already ran on any save loaded under the broken pack — with our
   `TraitReligious` value — and registered nothing; it will not run again. After
   the probe-gate declines, our own heal returns at its first line. The patch
   must re-apply through `AddDomeColonistsModifier` for every dome-colonists
   trait carrier missing its label entry. The probe must also fail CLOSED: a
   stub whose `GetPropertyMetadata` returns nil captures nothing, and "nothing"
   is a decline, not a 1.0.7 read.
4. **F-2's premise narrows.** 1.1.0 bounds the shuttle-wait case F58 was written
   for at one sol (`_GameConst.lua:144`, `LRTransport.lua:47-49`,
   `LRManager.lua:55-57`); what the sweep still covers is committed-shuttle limbo
   and the walk path. The one-clause exemption is right if the module stays;
   the owner chooses REMOVE vs FIX on that residual, not on "still shipped".
5. **Shapes the fix prompts must respect:** F-9 is a re-copy, never a
   distance pre-wrapper (`transport_mode_dist` also drives `:1904-1907` and
   `:1914`); F-6 stamps the payload flag on the confirmed path
   (`CargoRequestNew.lua:376-379`), not on `Apply` entry; F-7 and F-10 re-copies
   must carry `refuel_disabled` (`:1442`) and the BlackCube hook
   (`Train.lua:800-802`).
6. **R-36 `90_SaveSanitizer` is platform-conditional, not clean.** The F35
   reason in §1h was wrong (`WindTurbine.lua:98` re-applies `WindTurbine_Diffuser`
   only), and the whole REMOVE rests on 1.0.7 saves being unloadable — which is
   `Platform.steam and "block" or "warn"` (`Lua/Config/config.lua:174-175`). A
   non-Steam player (the pack ships on Paradox Mods, which reaches consoles)
   loads a 1.0.7 save with a warning and gets F35 and F48 residue back. ⇒
   R-36 leaves the REMOVE block and becomes an owner decision on platforms.
7. **R-17 is REMOVE, not "owner call"**, on the reader's argument: the copy
   hides demand that is real under the floor and reverts a rewritten body.
8. **Reasons corrected, verdicts unchanged:** R-14 (the cited fixup clears the
   flag itself, `:503-507` → `:256`; the §1h residual was overstated), R-25 (the
   second return IS read by the infopanel, `UniversalRocket.lua:3428-3436`,
   `:3614-3623` — a spurious "Return trip fuel" row, strengthening REMOVE),
   R-31 (the live gate is `Lua/Modifiers.lua:47-49`, not the shadowed
   `CommonLua` file), R-27 (the "possibly new untranslated string" is enrolled
   in the German pack — closed), R-3 (two dead `satisfaction` fields survive on
   `Colonist`, `Colonist.lua:168-169`; no behaviour), R-34 (two displays go
   stale after removal — patch-note item).

**Not opened by any reader:** engine-side `GetTargetAmount`,
`DisconnectFromCommandCenters`, `Landscape_ForEachObject`; the boot log for
F-1/F-5/F-9 (reader A); nothing was run in a game.

---

## Reader A — rows F-1…F-10, R-1…R-5

### VANILLA-FIX QA — section A: F-1…F-10, R-1…R-5

Fresh-context reader, 2026-09-08. Read order per the brief: our module → the
shipped 1.1.0 target under `ModTools/Src` → my own verdict → THEN the report
row and §1h. All `file:line` below are 1.1.0 Src unless prefixed `Fix_`.
`luafn.py` was used for every function body quoted.

---

### F-1 · `SaintBlessing` (F92)

1. **Our defect claim.** `AddDomeColonistsModifier` used `modify_trait` raw as the label; Saint's `"Religious"` is not in `fixed_labels`, so the +10 morale was filed under a label nobody is in. Our DataPatch rewrites `modify_trait` → `GetTraitLabel(raw)` (`Fix_SaintBlessing.lua:100-104`), and a LoadGame re-base re-applies on saves (`:151-181`).
2. **My read of 1.1.0.** `TraitPreset:AddDomeColonistsModifier` now does the lookup itself: `local label = (trait == "") and "Colonist" or GetTraitLabel(trait)` / `if not label then return end` (`Lua/TraitPreset.lua:86-87`; same in `RemoveDomeColonistsModifier` `:100-101`). `GetTraitLabel` returns `false` for a non-preset id (`Lua/Traits.lua:1325-1328`); `Religious` is absent from `fixed_labels` (`:1293-1323`) so the real label is `TraitReligious`. Shipped data still says `modify_trait = "Religious"` (`Data/TraitPreset.lua:405`). 1.1.0 also ships `SavegameFixups.OrphanedDomeColonistsTraitModifiers`, which strips every dome-colonists trait modifier and rebuilds it through the same function (`Lua/_fixup.lua:2143-2170`). With our pass on, the preset carries `"TraitReligious"`, `TraitPresets["TraitReligious"]` is nil, `GetTraitLabel` → `false`, return at `:87`: nothing registered, on joins (`Colonist.lua:443-446`) and in the fixup alike.
3. **Report accurate?** `CONFIRMED` (report cites `:85-86`; the lines are `:86-87` in this tree — same text).
4. **Vanilla replacement correct?** Yes: the label now comes from the same function the filing site uses (`Colonist.lua:443` vs `:445`), and the fixup re-bases old saves. No residual in vanilla.
5. **Patch impact.** The behaviour probe in the row is the right KIND of gate. Two things would make it half-baked: (i) **poisoned saves** — on any 1.1.0 save loaded while the broken pack was on, the one-shot fixup at `_fixup.lua:2143-2170` already ran and registered nothing; fixups do not re-run, `label_modifiers` is persisted, and nothing re-applies until the Saint changes dome. The patch must carry its own one-shot re-base for the 1.1.0 shape (the existing `:151-181` heal is keyed on `rebased_from`, which is EMPTY when the pass declines — so as written it will not fire). (ii) The probe must treat "captured nothing" as UNKNOWN → decline, not as "1.0.7": `AddDomeColonistsModifier` returns silently if the stub unit's `GetPropertyMetadata(modify_property)` is nil (`TraitPreset.lua:80-84`).
6. **Not opened.** `LabelContainer:SetLabelModifier` apply-to-newcomers path (`AddToLabel`) on 1.1.0; the `gated110_*.log:186` line the report cites.

### F-2 · `StaleReservations` (F58)

1. **Our defect claim.** Residence reservations taken for emigration have no timeout; a colonist whose shuttle never comes holds a slot forever. We stamp `ReserveResidence` (`Fix_StaleReservations.lua:48-55`) and a `NewDay` sweep cancels invalid/desynced/dying/older-than-`ForcedByUserLockTimeout` reservations (`:61-98`).
2. **My read of 1.1.0.** Three changes. (a) **A legitimate long hold now exists:** boarding an expedition rocket saves `expedition_residence` (`Colonist.lua:5027-5031`), `OnDisappear` reserves it through `Residence:ReserveResidence` (`:5003-5005` — so our post-wrapper stamps it), the colonist stays a valid object while away (`Unit.lua:1222-1230` detaches, does not delete), and `ReturnFromExpedition` keeps the slot only if still reserved (`:5076-5082`). `CancelResidenceReservation` now also wipes `expedition_residence` (`Residence.lua:391-395`; also `:90-97`). Lock = 3,600,000 ms (`__const.lua:174-176`, scale sols); `expedition_time` one-way 1,440,000–3,000,000 (`Data/POI.lua:23,58,104,139,190`). Our age branch therefore cancels a real hold. (b) **The ordinary case IS now bounded:** `const.ColonistTransportTaskExpirationTime = DayDuration` (`_GameConst.lua:144`), `ColonistTransportTask:IsObsolete` fires on it when no shuttle has committed (`LRTransport.lua:44-49`), `LRManager:ExpireColonistTransportTasks` runs on a `MapGameTimeRepeat` (`LRTransport.lua:125-130`; `LRManager.lua:49-62`) and calls `ClearTransportRequest`, whose first line is `CancelResidenceReservation` (`Colonist.lua:2036-2038`); plus a pickup-wait cap `ColonistMaxWaitShuttlePickupTimeMs = DayDuration` (`_GameConst.lua:143`, loop `Colonist.lua:3694-3701`) whose destructor cancels the reservation (`:3644-3652`). A load fixup stamps old tasks (`LRTransport.lua:132`). (c) The residence panel labels reserved slots ("Reserved slot", `sectionResidenceList.generated.lua:52-55`, `:70-73`).
3. **Report accurate?** `PARTIAL`. The expedition conflict: CONFIRMED, every line. The clause "The F58 defect itself (no timeout on ordinary reservations) is still shipped" is contradicted by `_GameConst.lua:144` + `LRTransport.lua:47-49` + `LRManager.lua:55-57`: the shuttle-wait case F58's header describes is bounded at one sol in 1.1.0. What is still unbounded is narrower: a task with a COMMITTED shuttle (`IsObsolete` returns false at `:44-46`) that never completes, and the walk path (`TransportByFootDtor` `:3529-3539` does not cancel).
4. **Vanilla replacement correct?** Yes for the expedition hold and the expiry. Residual: none found in vanilla; the committed-shuttle limbo is the one case our sweep still covers.
5. **Patch impact.** The one-clause exemption (`expedition_residence` truthy → skip) is correct and mandatory if the module stays. But the row's premise overstates what the module still buys: after 1.1.0 it protects only committed-shuttle limbo. State that in the row so the owner can choose REMOVE vs one-clause FIX on the real residual, not on "still shipped".
6. **Not opened.** `const.Scale.sols` value (engine-side; the "5 sols" conversion is the report's); `ColonistTransportTaskExpirationCheck` cadence; whether a committed shuttle can in fact stall indefinitely.

### F-3 · `ShelterReflex` (F73) half (a)

1. **Our defect claim.** `MicroGHabitatAutoResolve:IsSuitable` = `GetScoreFor(colonist.traits) > 0`, and the 100-point base is granted only while `HasLifeSupport()`, so one tick without power/air evicts the residents. We replace `IsSuitable` to add the 100 back (`Fix_ShelterReflex.lua:43-47`).
2. **My read of 1.1.0.** Signature changed: `IsSuitable(colonist)` → `GetScoreFor(colonist)` (`MicroGHabitat.lua:173-175`), and `GetScoreFor` reads `colonist.traits` itself (`Community.lua:442-445`, `:451-454`). No-life-support is now a −400 tier, not a missing +100: `CommunityEvalLifeSupport = 100` / `CommunityEvalNoLifeSupport = -400` (`Community.lua:436-437`, `:443`). Our body hands it `colonist.traits`; inside, `traits.traits` is nil and `FilterObjectAttributes` does `obj_attributes[attrib]` for every filter key (`Filter.lua:113-121`) — a throw whenever the habitat has any trait filter (default `{}`, `Community.lua:43`, so silent until the player sets one). With no filter: −400 + our +100 < 0, so the fix is a no-op.
3. **Report accurate?** `CONFIRMED`.
4. **Vanilla replacement correct?** It is a deliberate design (help text at `:437`), not a fix of F73a: an unpowered habitat still scores negative, `ChooseResidence` still returns false (`MicroGHabitat.lua:162-171`), and the heavy update still calls `UpdateResidence` (`Colonist.lua:2339-2344`) — so a blip still costs the residence; the colonist is re-homed on the next heavy update once life support is back (same path). Residual for a 1.1.0 player: F73a's symptom persists by design; half (b) is inert during the blip because it requires `IsValid(self.residence)` (`Fix_ShelterReflex.lua:62`).
5. **Patch impact.** Dropping (a) is right (§4 bars fighting a stated design). Keeping (b): its reads still exist — `outside_start` (`Colonist.lua:94`, `:3015-3020`), `g_Consts.OxygenMaxOutsideTime` (`__const.lua:1756`, used `Colonist.lua:4577`), `Colonist:Idle` (`:2212`), `Colonist:Rest` (`:2572`), `IsDying` (`:2666`). Name in the row that (a)'s removal returns the blip-eviction to 1.1.0 players.
6. **Not opened.** Whether a habitat lists itself under its own `labels.Residence` (decides if the `:451-454` comfort loop also throws); `TraitFilterColonist` callers other than `:445`.

### F-4 · `FirstAsteroidPrefabs` (F83)

1. **Our defect claim.** The First Asteroid popup waited on a REAL-TIME thread; after a save/load the callback that granted three Micro-G prefabs was dead. Our LoadGame sweep removes the stranded notification, grants the three, latches a GameVar, re-shows the popup (`Fix_FirstAsteroidPrefabs.lua:173-210`).
2. **My read of 1.1.0.** `OnMsg.SpawnedAsteroid` is now `CreateGameTimeThread(WaitPopupNotification, "FirstAsteroid")` with NO callback (`Lua/Asteroids.lua:418-423`); the waiter blocks on `WaitMsg(async_signal)` (`PopupNotification.lua:341-342`) and game-time threads persist. No `ColonyAddPrefabs` of any `MicroGAutoExtractor*` exists in `Lua/`, `Data/`, `DLC/` (grep). The prefabs are now resupply cargo unlocked by `Effect_UnlockResupplyItem` on techs `ReconCenter` and `MicroGLanders` (`Data/Tech.lua:8352-8358`, `:8606-8614`), priced 250 M each and `locked = true` until then (`Data/Cargo.lua:495-508`), with a save fixup `AddMicroGExtractorResupplyItems` (`AutomaticMicroGExtractor.lua:24-36`); the popup text says "can be ordered from Earth" (`PopupNotificationPreset-Asteroid.lua:36`). Our sweep matches the live minimized notification (`find_stranded_notification` keys only on text id + `popup_notification`), `RemoveNotification`s it — the persisted waiter then waits forever — grants three prefabs vanilla no longer grants, and re-shows the popup as a second minimized notification.
3. **Report accurate?** `CONFIRMED`.
4. **Vanilla replacement correct?** Yes — the deferred grant was replaced by a purchasable, save-safe route; nothing left to strand. Residual: none in vanilla.
5. **Patch impact.** REMOVE is right. Note for the notes: prefabs already granted by the pack on 1.1.0 saves cannot be taken back (ordinary `available_prefabs`), and the `SMRFixPack_FirstAsteroidPrefabs` GameVar is absent-tolerant per the module header. No cleanup owed.
6. **Not opened.** `Effect_UnlockResupplyItem:OnApplyEffect`; whether `MicroGAutoExtractorRareMetals`/`ExoticMinerals` cargo rows mirror `:501-508`.

### F-5 · `AstrogeologistExtractors` (F95)

1. **Our defect claim.** The profile enumerated ten `Effect_ModifyLabel`s and missed `AutomaticMetalsExtractor` (`production_per_day1`) and `MicroGAutoWaterExtractor` (`water_production`). We append two +10% entries (`Fix_AstrogeologistExtractors.lua:67-70`, `:117-142`) and heal saves on load (`:174-218`).
2. **My read of 1.1.0.** Profile rewritten: two label-wide effects — `Extractors` `performance` **+20** and `Extractors` `water_production` **+20%** (`Data/CommanderProfilePreset.lua:337-347`); text "Extractor performance increased by 20" (`:333`). `MicroGAutoWaterExtractor` carries `label3 = "Extractors"` (`Lua/BuildingTemplate/MicroGAutoWaterExtractor.generated.lua:77`), as does `AutomaticMetalsExtractor` (`AutomaticMetalsExtractor.generated.lua:80`). Our pass counts 2 existing (≠0, shape check passes at `:109`), finds neither Label, appends both → +10% on top of vanilla's +20.
3. **Report accurate?** `CONFIRMED` (the report cites `Data/BuildingTemplate/MicroGAutoWaterExtractor.lua:34` — a path I did not open; the same fact is at the generated-Lua line above).
4. **Vanilla replacement correct?** Yes, and it closes the F95 gap by construction: 17 templates carry `Extractors` (grep), including ConcretePlant, MoholeMine, TheExcavator and the two hidden legacy ones — all `ExtractorPerformance` carriers (`BaseExtractor.lua:19-26`; `MoholeMine.lua:2`, `TheExcavator.lua:3`, `Plant.lua:24`), so `performance +20` lands on every member; `water_production +20%` on a member without that property is a silent no-op (`Modifiers.lua:41-49` returns when `base_<prop>` is absent). `WaterExtractorBase` has no `ExtractorPerformance` (`WaterExtractor.lua:2-3`) so water extractors get only the +20%. Residual: the profile now also buffs three non-extractors (design, not a defect).
5. **Patch impact.** REMOVE is right, BUT it is half-baked without a save cleanup: our two `Effect_ModifyLabel` keys are written into `UIColony.label_modifiers`, which is PERSISTED (our own header, `:191-199`; `LabelContainer.lua:59-77`) — every 1.1.0 save played under the pack keeps +10% `production_per_day1` on AutomaticMetalsExtractors and +10% `water_production` on MicroGAutoWaterExtractors after the module is gone. One-shot sanitizer needed (there is a `90_SaveSanitizer` for exactly this class).
6. **Not opened.** `HasModifiablePropScale("performance")`; `GetLabelModifierId(parent)` key shape on 1.1.0 (whether our stored key and vanilla's collide).

### F-6 · `PayloadTemplateRefill` (F70)

1. **Our defect claim.** `RetrieveRequests` refills every 0 row from the flight-policy template on every open; we gate the template behind a per-transporter `SMRFixPack_payload_set` flag via a full body copy (`Fix_PayloadTemplateRefill.lua:81-125`) and a pre-wrapper on `Apply` (`:70-79`).
2. **My read of 1.1.0.** The refill is unchanged (`CargoRequestNew.lua:221-234`) and `CmdUnload` still zeroes every request (`UniversalRocket.lua:572-579`). Three things our copy reverts: `resolve_loc_cargo_template(transporter, from_destination_pick)` gained a tutorial branch (`:183-189`, `AsteroidTutorialExpectedCargo`) and a `CmdLoad` exemption for destination picks (`:174`); `RetrieveRequests` reads `prev_flight_data` and ignores stored cargo on a destination pick (`:215-217`); the automode branch nil-guards `cargo_items[id]` (`:199-213`). `Apply` is now an async prompt (`:368-385`) — our pre-wrapper sets the flag before the player confirms, so a cancelled prompt (`CancelFlight`, `:382`) still suppresses the template thereafter.
3. **Report accurate?** `CONFIRMED`.
4. **Vanilla replacement correct?** n/a — F70 is not fixed in 1.1.0.
5. **Patch impact.** A re-copy of the 1.1.0 body with the gate as `not from_destination_pick and transporter.SMRFixPack_payload_set` is the right repair. Two small things would leave it half-baked: set the flag on the CONFIRMED path (`:379` `SetCommand("CmdLoad")` / `:376-377`), not before the prompt; and the tutorial return (`:183-189`) must precede the gate so rocket 2 is still pre-filled.
6. **Not opened.** `Lua/TutorialsNew.lua:1019-1025`; `GetFlightPolicy` on 1.1.0.

### F-7 · `RocketDroneChurn` (F50)

1. **Our defect claim.** `UpdateCargoResourceRequests` disconnects/reconnects command centers unconditionally; the hourly auto-request therefore idles every inbound drone. Our full copy cycles only when a request must be created (`Fix_RocketDroneChurn.lua:42-86`).
2. **My read of 1.1.0.** Body still brackets with unconditional `Disconnect`/`Connect` (`CargoTransporterNew.lua:1431-1433`, `:1460-1462`); the hourly path is intact (`UniversalRocket.lua:1557-1568` → `CreateAutoCargoRequest` → `SetCargoRequest` `:2093` → `:1484`); `DroneControl:OnRemoveBuilding` still idles drones whose goto target is the building (`DroneControl.lua:784-793`; the new `oldp/newp` guard does not apply on a disconnect). One line changed inside the loop: `additional_amount = is_refuel_resource and not self.refuel_disabled and self:GetFuelResourceRequest()` (`:1442`); `refuel_disabled` is a new player toggle (`UniversalRocket.lua:70`, `:3320`). Our copy (`:63`) lacks the clause. Also new: the rocket override now calls `ForceInterruptIncomingDrones` when not in auto mode before delegating (`:1937-1943`) — orthogonal to our body.
3. **Report accurate?** `CONFIRMED`.
4. **Vanilla replacement correct?** n/a — F50 persists.
5. **Patch impact.** Re-copy with the `refuel_disabled` clause; right shape.
6. **Not opened.** The `DisconnectFromCommandCenters` definition — not found in `Lua/` or `CommonLua/` (call sites only, e.g. `Building.lua:1569`); presumed engine-side. `ForceInterruptIncomingDrones`.

### F-8 · `LandscapeUnitFilter` (F34d)

1. **Our defect claim.** `LandscapeForEachUnit` builds `filter_embark` and passes the raw `callback` instead. Our copy fixes the argument (`Fix_LandscapeUnitFilter.lua:121-138`); F115 gate declines on 1.1.0 (`:78-112`).
2. **My read of 1.1.0.** Signature is `(map, mark, callback, ...)` reading `map.Landscapes[mark]` (`Landscaping.lua:509-510`; `MapVar("Landscapes", {})` `:21`) and the body STILL passes `callback` at `:522` while `filter_embark` (`:516-521`) is unused; the sibling `LandscapeForEachStockpile` passes its filter (`:503`). The consumer moved: the only caller is `ClearWasteRockConstructionSite:GetUnitsUnderneath` (`ClearWasteRockConstructionSite.lua:79-85`), scattered by `ConstructionSite:ScatterUnitsUnderneath` (`ConstructionSite.lua:1914-1931`, `ExitImpassable` for non-trains); `LandscapeConstructionSite` no longer defines `GetUnitsUnderneath` (grep). `foreach_params_unit` unchanged (`:505-507`).
3. **Report accurate?** `CONFIRMED`; the row could add that the reach is now Clear-Waste-Rock sites only.
4. **Vanilla replacement correct?** n/a — not fixed.
5. **Patch impact.** Repair on the new signature, keep the gate: right. Half-baked only if the repair re-pins the old signature or the bare `Landscapes` global.
6. **Not opened.** `Landscape_ForEachObject` (engine); `HexGetUnits`.

### F-9 · `VacuumWalks` (F52)

1. **Our defect claim.** In vacuum `min_dist` = the 400 m walk cap, so a passage path is never looked up for domes within walking range and colonists cross the surface. Our full copy sets `min_dist = 0` in vacuum (`Fix_VacuumWalks.lua:49-98`).
2. **My read of 1.1.0.** The defect line is byte-for-byte the same (`Colonist.lua:1903`; consts `_GameConst.lua:149-150`, now `g_Consts`). Everything around it is rewritten: `need_work` slot reservation (`:1894-1896`, `:1920-1926`, `:1943-1949`, `:1972-1978`), `DiscardTransportTicket` (`:1918`), `-1` = passage-only → `max_int` (`:1904-1907`; produced by `CheckWalkableDistance`/`IsInWalkingDistDome`, `Dome.lua:212-231`, `:300-318`), `transport_task.shuttle` guard on the walk branch (`:1898`), `HasShuttleLandingSlots`/`IsSameMap` on the task branch (`:1932-1957`), new `src_dome` search (`:1959-1968`). Our copy has none of these; on a `-1` pair it would send the colonist `TransportByFoot` with no passage path.
3. **Report accurate?** `CONFIRMED`. The "inactive by accident" mechanism (path spec on `const.` fails because the consts moved to `g_Consts`) is consistent with `_GameConst.lua:149-150` being `DefineConstInt`; I did not read the boot log.
4. **Vanilla replacement correct?** n/a — F52 persists, but narrower: the `-1` convention already forces the passage lookup for no-outside-route pairs, so the residual is "outside route exists and < 400 m, in vacuum".
5. **Patch impact.** A pre-wrapper that inflates `transport_mode_dist` is the wrong shape: the same value decides walk-vs-shuttle at `:1914` (`< dome_passage_dist`) and the `-1` branch at `:1904`. A re-copy with `min_dist = 0` in vacuum is the only clean repair; make the gate deliberate.
6. **Not opened.** `GetDomesPassagePath`; `FindEmigrationDome`; `TryToEmigrateByTrain`.

### F-10 · `TrainCargoDumping` (F46)

1. **Our defect claim.** `Train:UnloadAll` dumps into a station regardless of the per-resource switch. Our copy skips the unload when the station has the resource off and another route station accepts it (`Fix_TrainCargoDumping.lua:108-136`); F114 gate declines on 1.1.0 (`:68-83`).
2. **My read of 1.1.0.** `UnloadAll` (`Train.lua:779-805`) nil-guards `dest.demand[res]` (`:785`) and `station.demand[res]` (`:794-795`) and adds a BlackCube hook (`:800-802`), but has no enabled check. `Station` is now a `MultiResourceDepotBase` (`Station.lua:48-56`); `IsResourceEnabled = IsStoring` = demand exists and not `rfSuspended` (`MultiResourceDepot.lua:242-247`); `SetAcceptResource` toggles `rfSuspended` and keeps the request (`:251-290`). So a switched-off station's demand still exists and `GetTargetAmount()` is called on it.
3. **Report accurate?** `CONFIRMED`, including the unread C-side caveat: `GetTargetAmount` has no Lua definition except `ResourcePile` (`ResourcePile.lua:99`).
4. **Vanilla replacement correct?** n/a — plausibly not fixed; depends on whether a suspended request reports a target.
5. **Patch impact.** Re-copy `:779-805` with `station:IsResourceEnabled(res)`; carry the BlackCube hook; `route_accepts_elsewhere`'s `st.demand[res] and st.IsResourceEnabled` still resolves on the new base. Half-baked if the copy drops `:800-802`.
6. **Not opened.** `GetTargetAmount` (engine); `Train:TransferCargo` load-side on 1.1.0 (`:869-935` matched by grep only).

### R-1 · `LowStorageWarning` (F12)

1. **Our defect claim.** Broken precedence made the Food/maintenance hours formula 0-or-≥24, so "Insufficient Resources" never fired for them; full body copy with the four lines fixed.
2. **My read of 1.1.0.** The function begins at the grid part (`ResourceTracking.lua:222-231`): the Food and maintenance branches are gone, the `MinDays*` consts are gone from `_GameConst.lua` (grep), and `SavegameFixups.InsufficientResourcesGridOnly` says so in words — "Rows for stockpiled resources are no longer produced" (`:318-330`). No replacement warning under any maintenance/food id (grep of `Lua/`, `Data/`); `maintenance_resources_consumed_yesterday` is still tracked (`:8`, `:38-72`) but unread here.
3. **Report accurate?** `CONFIRMED`.
4. **Vanilla replacement correct?** It is the "resolved the other way" case the brief warns about: the dead branches were deleted, not fixed. Nothing is wrong in code; the player simply gets no low-Food/maintenance warning on 1.1.0.
5. **Patch impact.** REMOVE is right for the module (its body would resurrect deleted code). If the owner wants the warning, it is a feature (§4), not a fix — say so in the checklist rather than leaving "nothing".
6. **Not opened.** `Data/NotificationPreset.lua:1019-1028`; `FixupObjectNotification` (`:316`).

⛔ **CORRECTION ADDED 2026-09-08 by hotfix2 link 02 (`smr-bugfixpack-11`). Point 4 above is WRONG, and this row's own item 6 is why.** The claim *"the player simply gets no low-Food/maintenance warning on 1.1.0"* does not survive a tree-wide read. **Both warnings were REPLACED, not deleted:** Food by `StarvingColonists` ("Missed Meals", voiced *"Warning! Food shortage"*, `NotificationPreset.lua:1387-1404`), driven per dome by `Community:UpdateStarvationNotification` (`Community.lua:536-543`) off `GetFoodServiceFailures` (`Dome.lua:2718-2745`) from six status-effect transitions, and **new in this branch** (`SavegameFixups.InitStarvingColonistsNotification`, `Dome.lua:1034`); maintenance by `MaintenanceStuckBuildings` ("Maintenance Problem", voiced *"A building is about to malfunction"*, `NotificationPreset.lua:1103-1120`) via `RequiresMaintenance.lua:342`.
⚠️ **The method lesson, which is bigger than the row.** The negative in point 2 — *"No replacement warning under any maintenance/food id (grep of `Lua/`, `Data/`)"* — is a FALSE NEGATIVE from grepping for the OLD vocabulary: neither replacement carries "food" or "maintenance" in its id. And the two artefacts item 6 honestly lists as **not opened are exactly the two that hold the answer** — `NotificationPreset.lua` is where both replacements are declared, and `FixupObjectNotification` (`:316`) is the migration off the old notification, i.e. a signpost to where it went. ⇒ **A report's "not opened" list is not a footnote; it is the map of where its conclusion could be wrong.** Link 02 inherited point 4, ran a one-file grep that agreed with it, and filed a checklist decision on it (item 121, now WITHDRAWN); the owner overturned it by asking why a food-focused DLC would delete food warnings. ⛔ REMOVE for the module still stands and is unaffected — the branches it repaired really are gone. Only the consequence was mis-stated. Details on `agent/bugs/F12.md`.

### R-2 · `LanderCargoRatchet` (F68 + F71)

1. **Our defect claim.** Hourly `CreateAutoCargoRequest` recomputed from city stock that no longer counted the loaded hold (ratchet → unload), and walked thresholds alphabetically (bulk first).
2. **My read of 1.1.0.** Rewritten (`UniversalRocket.lua:2028-2100`). Rockets are excluded from the C++ stockpile sum (`count_in_resource_overview = false`, `:198`); the overview adds only a landed rocket's `GetCargoSurplus` = amount above request (`ResourceOverview.lua:141-155`; `:2522-2535`; `CargoTransporterNew.lua:1676-1684`), and `:2046` adds back `GetLoadedCargoNotInOverview` = `Min(amount, requested)` (`:2537-2546`), fuel ration handled symmetrically (`:2542-2544` vs `:1680-1682`). Ground + surplus + kept = the whole hold, once. Budget: demands sorted by desired weight ascending, fair share of the remaining hold, then leftover (`:2069-2086`). New `IsImportLocked` embargo (`:2044`).
3. **Report accurate?** `CONFIRMED` — my trace matches §1h's line for line.
4. **Vanilla replacement correct?** Yes; no double count, no alphabetical order. Residual: none found (not measured in play).
5. **Patch impact.** Nothing; the F113 gate (`Fix_LanderCargoRatchet.lua:91-92`) declines on 1.1.0.
6. **Not opened.** `GetAutoModeThresholds`; `GetEarthAutomodeFundingState`.

### R-3 · `TouristSatisfaction` (F09)

1. **Our defect claim.** Threshold awards were asymmetric, so tourist Satisfaction ratcheted down.
2. **My read of 1.1.0.** `UpdateSatisfaction`, `ChangeSatisfaction`, `SatisfactionLowStatPenalty`: zero hits in `Lua/`, `Data/`. Where it went: the holiday score is now `(Comfort + Morale) / 2` at departure, bucketed into stars (`HolidayRating.lua:44-56`). Two dead class defaults survive: `stat_satisfaction = 0`, `log_satisfaction = false` (`Colonist.lua:168-169`).
3. **Report accurate?** `CONFIRMED` on the verdict; `DISPUTED` on one detail — §1h says the only "satisfaction" left in `Lua/` is `sight_satisfaction`; `Colonist.lua:168-169` contradicts that. Dead fields, no behaviour.
4. **Vanilla replacement correct?** Yes — a stateless read at departure cannot drift.
5. **Patch impact.** Nothing; the module's `Require` fails on `UpdateSatisfaction`.
6. **Not opened.** `GetCappedRating` (`:56`).

### R-4 · `AutomationLawCompensation` (C39, F112)

1. **Our defect claim.** Laws cut `max_workers` by label; the `law_scale` payback keyed on class; eight families got the cut and no payback. Post-wrapper adds the delta.
2. **My read of 1.1.0.** `GetWorkshiftPerformance` has no `law_scale` (`Workplace.lua:269-294`; 0 hits tree-wide) and the loop lives in `GetWorkersPerformance` (`:250-267`); the laws still cut `max_workers` by `automation_workforce_reduction` (`LawDef-Technology.lua:14-17`, `:107-110`, `:194-197`). Our `test` gate on `GetWorkersPerformance` declines (`Fix_AutomationLawCompensation.lua:252-256`).
3. **Report accurate?** `CONFIRMED`.
4. **Vanilla replacement correct?** Yes, and it is more than "uniform": `part_per_worker = 100 / self.max_workers` (`:255`) means a fully staffed building after the cut scores the same as before it — the cut is output-neutral at full staff, exactly what "require 50% less workers" (`:96`) promises. The 1.0.7 `law_scale` was therefore a 2× overpay for the in-class families (C39's own control, 114 → 268, measured that), so deleting it removes the asymmetry from the other side. Residual: none.
5. **Patch impact.** Nothing.
6. **Not opened.** `LawEffectModifyLabel:OnStart` on 1.1.0.

### R-5 · `UpgradeModifierLeak` (F03)

1. **Our defect claim.** `StopUpgradeModifiers` used `ipairs` on an id-keyed table and turned nothing off; post-wrapper sweeps `upgrade_id_to_modifiers`.
2. **My read of 1.1.0.** `for _, modifiers in pairs(self.upgrade_modifiers)` (`Building.lua:1303-1311`); both tables are appended together at `:1203-1206`, so the set is identical. Our second pass calls `TurnOff` again: `LabelModifier:TurnOff` → `SetLabelModifier(label, id, nil)` with no old mod = no-op (`Modifiers.lua:277-280`; `LabelContainer.lua:59-77`); `ObjectModifier:TurnOff` is guarded by `is_applied` (`Modifiers.lua:311-319`; `CommonLua/Classes/Modifiers.lua:479-484`).
3. **Report accurate?** `CONFIRMED`.
4. **Vanilla replacement correct?** Yes; `StopUpgradeModifiersForUpgrade` (`:1279-1287`) correctly uses `ipairs` on the per-id array. Residual: none.
5. **Patch impact.** Nothing; harmless either way.
6. **Not opened.** `MultipleObjectsModifier:TurnOff` (`CommonLua/Classes/Modifiers.lua:528`).

---

### Summary table

| row | module | claim | replacement correct? | patch impact | evidence |
|---|---|---|---|---|---|
| F-1 | SaintBlessing | CONFIRMED | yes | FIX shape right; **owes a 1.1.0 save re-base** (fixup already spent) + probe must fail closed | `TraitPreset.lua:86-87`; `Traits.lua:1326`; `_fixup.lua:2143-2170`; `Data/TraitPreset.lua:405` |
| F-2 | StaleReservations | PARTIAL | yes | exemption clause right; row overstates what remains ("still shipped" is wrong for the shuttle-wait case) | `Colonist.lua:5003-5005`, `:5076-5082`; `Residence.lua:391-395`; `_GameConst.lua:143-144`; `LRTransport.lua:44-49`, `:125-130`; `LRManager.lua:49-62`; `Colonist.lua:2036-2038`, `:3644-3652`, `:3694-3701` |
| F-3 | ShelterReflex (a) | CONFIRMED | design, not fix — blip eviction persists | drop (a), keep (b) — right; (b)'s reads verified | `Community.lua:436-445`, `:451-454`; `Filter.lua:113-121`; `MicroGHabitat.lua:162-175`; `Colonist.lua:2339-2344` |
| F-4 | FirstAsteroidPrefabs | CONFIRMED | yes | REMOVE right; no cleanup owed | `Asteroids.lua:418-423`; `PopupNotification.lua:341-342`; `Data/Tech.lua:8352-8358`, `:8606-8614`; `Data/Cargo.lua:495-508` |
| F-5 | AstrogeologistExtractors | CONFIRMED | yes | REMOVE right; **owes a label_modifiers save cleanup** | `Data/CommanderProfilePreset.lua:333-347`; `MicroGAutoWaterExtractor.generated.lua:77`; `Modifiers.lua:41-49`; `LabelContainer.lua:59-77` |
| F-6 | PayloadTemplateRefill | CONFIRMED | n/a (F70 persists) | re-copy right; flag on the confirmed path, tutorial before the gate | `CargoRequestNew.lua:169-192`, `:199-217`, `:221-234`, `:368-385` |
| F-7 | RocketDroneChurn | CONFIRMED | n/a (F50 persists) | re-copy + `refuel_disabled` clause | `CargoTransporterNew.lua:1431-1433`, `:1442`, `:1460-1462`; `DroneControl.lua:784-793` |
| F-8 | LandscapeUnitFilter | CONFIRMED | n/a (not fixed) | repair on `(map, mark, callback)`; reach is now Clear-Waste-Rock only | `Landscaping.lua:21`, `:505-523`; `ClearWasteRockConstructionSite.lua:79-85`; `ConstructionSite.lua:1914-1931` |
| F-9 | VacuumWalks | CONFIRMED | n/a (narrowed, not fixed) | re-copy only; a distance pre-wrapper is the wrong shape | `Colonist.lua:1886-1983` (`:1903`, `:1904-1907`, `:1914`); `_GameConst.lua:149-150` |
| F-10 | TrainCargoDumping | CONFIRMED | n/a (plausibly persists; C-side unread) | re-copy with `IsResourceEnabled`; carry BlackCube hook | `Train.lua:779-805`; `MultiResourceDepot.lua:242-247`, `:251-290` |
| R-1 | LowStorageWarning | CONFIRMED | deleted, not fixed (no warning at all) | REMOVE right; feature ask belongs in the checklist | `ResourceTracking.lua:222-231`, `:318-330` |
| R-2 | LanderCargoRatchet | CONFIRMED | yes, traced | nothing | `UniversalRocket.lua:198`, `:2028-2100`, `:2522-2546`; `ResourceOverview.lua:141-155`; `CargoTransporterNew.lua:1676-1684` |
| R-3 | TouristSatisfaction | CONFIRMED (one §1h detail DISPUTED) | yes | nothing | `HolidayRating.lua:44-56`; `Colonist.lua:168-169` |
| R-4 | AutomationLawCompensation | CONFIRMED | yes — 1.0.7 was a 2× overpay | nothing | `Workplace.lua:250-267`, `:269-294`; `LawDef-Technology.lua:14-17`, `:96` |
| R-5 | UpgradeModifierLeak | CONFIRMED | yes | nothing | `Building.lua:1203-1206`, `:1303-1311`; `Modifiers.lua:277-280`, `:311-319` |

### What would make the patch half-baked

Ranked by what a 1.1.0 player would be left with.

1. **F-5 REMOVE without a save cleanup.** Our two `Effect_ModifyLabel` keys live in `UIColony.label_modifiers`, which is persisted (the module says so itself, `Fix_AstrogeologistExtractors.lua:191-199`; mechanism `LabelContainer.lua:59-77`). Removing the module leaves +10% `production_per_day1` on every AutomaticMetalsExtractor and +10% `water_production` on every MicroGAutoWaterExtractor in every 1.1.0 save that ran under the pack, on top of vanilla's +20 — forever. The patch needs a one-shot sanitizer keyed on `prop` + label, the way the module's own heal already tests (`:207-215`).
2. **F-1 FIX without a 1.1.0 re-base.** `SavegameFixups.OrphanedDomeColonistsTraitModifiers` (`_fixup.lua:2143-2170`) is one-shot; on any save loaded while the broken pack was on, it ran with `modify_trait = "TraitReligious"`, registered nothing (`TraitPreset.lua:86-87`), and will not run again. After the gate is fixed the pass declines, `rebased_from` stays empty, and the existing heal (`Fix_SaintBlessing.lua:152`) returns at its first line. Saints in those saves bless nobody until they change dome. The patch must re-apply through `AddDomeColonistsModifier` for every dome-colonists trait carrier missing `dome.label_modifiers[GetTraitLabel(trait)][colonist]`.
3. **F-1 probe that fails open.** If the stub unit's `GetPropertyMetadata(self.modify_property)` is nil, `AddDomeColonistsModifier` prints and returns (`TraitPreset.lua:80-84`) capturing nothing; "captured nothing" must be read as decline, not as 1.0.7.
4. **F-2 rebuilt on "still shipped".** The residual after 1.1.0 is committed-shuttle limbo only (`LRTransport.lua:44-49` + `:125-130`, `_GameConst.lua:143-144`). Keep the module with the `expedition_residence` exemption if that residual is worth it; do not keep it on the row's stated reason.
5. **F-9 as a distance pre-wrapper.** `transport_mode_dist` also drives `:1904-1907` and `:1914`; inflating it flips walk-vs-shuttle. Re-copy or nothing.
6. **F-6 flag set before the prompt.** `Apply` is async with a cancel path (`CargoRequestNew.lua:368-385`); stamp on `:376-379`, not on entry.
7. **F-10 / F-7 re-copies that drop a 1.1.0 line.** BlackCube hook (`Train.lua:800-802`); `refuel_disabled` (`CargoTransporterNew.lua:1442`).

No row's REMOVE verdict is wrong; no vanilla replacement in this section is a rebreak. What I opened to know that: every 1.1.0 function named in the evidence columns above, plus `_fixup.lua:2060-2175`, `ResourceOverview.lua:140-175`, `Modifiers.lua:41-80`/`:255-325`, `Filter.lua:105-121`, `LRTransport.lua:28-135`, `LRManager.lua:45-62`, `Unit.lua:1177-1231`, `HolidayRating.lua:1-56`, `AutomaticMicroGExtractor.lua:1-45`, `BaseExtractor.lua:19-60`, the `Extractors` label grep over `Lua/BuildingTemplate/`, and the 1.1.0 `Data/` presets cited per row. Not opened anywhere: engine-side `GetTargetAmount`, `DisconnectFromCommandCenters`, `Landscape_ForEachObject`; the boot log the report cites for F-1/F-5/F-9.

---

## Reader B — rows R-6…R-20

### VANILLA-FIX QA — section B: rows R-6 … R-20

Fresh-context reader, 2026-09-08. Method per `prompts/VANILLA_FIX_QA.md`: for
each row I read only the module name + defect id, opened `Code/Fix_<id>.lua`,
opened the shipped 1.1.0 target under `ModTools\Src`, formed a read, and only
then opened the report's row and §1h. Line numbers are 1.1.0 `Src` unless
prefixed `Code/`. Status control: `docs/archive/logs/gated110_Mars.exe-20260908-17.51.09-6a91a190.log`
(:74-:190) — every "applied"/"inactive" cell below was checked against it.

Legend: CONFIRMED / DISPUTED / PARTIAL apply to the report's claim in §1b;
the §1h residual is judged separately where it differs.

---

### R-6 · `SmallLandscapeSites` (F33)

1. **Our claim.** `LandscapeConstructionSiteBase:GetClosestDests` copied
   `top_count` (default 5) entries out of `drone_dests_cache` with no bounds
   check; a small site's periphery has <5 entries, `dests[i]` is nil, the drone
   command thread dies (`Code/Fix_SmallLandscapeSites.lua:4-19`). Our pre-wrapper
   passes `Min(top_count or 5, n)` (`:60`).
2. **1.1.0.** `GetClosestDests` is a two-liner delegating to a new global
   (`LandscapeConstructionSiteBase.lua:204-208`). `GetTopClosestDests`
   (`:171-202`) defaults `top_count = top_count or 10` (`:172`) and bounds-checks
   first: `if count <= top_count then return table.icopy(dests) end` (`:175-177`);
   the copy loop `for i = 1, top_count` (`:198-200`) is only reached when
   `count > top_count`. The cache is still periphery-only (`:56-71`, `if border`
   at `:66`). The only site caller passes no `top_count` (`:217`); a second
   caller exists in `LandscapeLake.lua:72` with its own bound.
3. **Report accurate?** CONFIRMED. The row's "we narrow drones to 5" is right:
   with n ≥ 5 our `Min(5, n)` overrides the new default 10, so an applied module
   halves the candidate list on every big site.
4. **Replacement correct?** Yes. Overrun impossible by construction; connectivity
   sort (`:179-195`) puts unreachable hexes last. No residual found.
5. **Player after REMOVE.** Vanilla's 10 candidates (or the whole periphery, in
   cache order, when ≤10). Nothing lost.
6. **Not opened.** `drone:Goto(list)` semantics; `ConnectivityCheckAll`.

### R-7 · `DroneTransportMinors` **(b)** (F57b)

1. **Our claim.** `OnMsg.OnPassabilityChanged` rebuilt each drone's
   `unreachable_buildings` as a plain `{}` (losing `weak_keys_meta`) and left
   `unreachable_buildings_count` stale (`Code/Fix_DroneTransportMinors.lua:8-30`).
   Our extra handler re-applies the metatable and recounts (`:139-160`).
2. **1.1.0.** The handler is `BumpDroneUnreachablesVersion(map or CurrentMap)`
   only (`Drone.lua:935-937`, `:943-945`); no table is rebuilt. Tables are
   created only with `setmetatable({}, weak_keys_meta)` (`:892`, `:966`) and
   cleared in place (`:964`). `unreachable_buildings_count` survives as a
   declaration "kept for savegame compatibility" (`:73`) with **zero readers**
   tree-wide (grep `Lua/`+`CommonLua/`: the one hit is `:73`). Part **(a)** is
   unchanged: `r_t.Fuel = nil` (`DroneControl.lua:674`) vs `r_t[r.FuelResource]`
   (`:693`), `FuelResource` template default `"Fuel"` (`UniversalRocket.lua:47`)
   — the report keeps it as K-8, which my read supports.
3. **Report accurate?** CONFIRMED.
4. **Replacement correct?** Yes for the claim. One **unverified residual**:
   `Drone:TryTakeTask` does `next(self.unreachable_buildings)` (`:611`) while
   the field defaults to `false` (`:71`) and is reset to `false` on map transfer
   (`:979`). `EF-005` records `next(nil)`/`ipairs(false)` as tolerated, not
   `next(false)`; not sampled here — likely benign given the game boots and
   idles, but it is a claim, not a fact.
5. **Player after REMOVE (b).** Nothing changes; our handler currently sets a
   metatable that is already set and writes a field nothing reads, per drone,
   per passability change. **(a) must stay in the file.**
6. **Not opened.** The engine `next` implementation; `weak_keys_meta` def.

### R-8 · `DroneUnreachableForever` (F55)

1. **Our claim.** `ApproachWrapper` stamped `GameTime() + max_int`, defeating the
   5-sol expiry in `CleanUnreachables` (`Code/Fix_DroneUnreachableForever.lua:6-18`).
   Our pre-wrapper on `CleanUnreachables` normalises stamps `> now` (`:80-94`).
2. **1.1.0.** `MarkUnreachable` stamps `GameTime()` (`Drone.lua:909`) and evicts
   the oldest at 64 (`:896-907`). `CleanUnreachables` is now ONLY a version test
   → `ResetUnreachablesTable` (`:971-976`, `:960-969`); `const.UnreachablesCleanupDeltaT`
   has zero hits tree-wide. Version bumps: any passability change (`:935-937`),
   `Building:Done` (`Building.lua:528` header, `:546`), landscaping
   (`Landscaping.lua:328`). Old poisoned stamps are healed by a vanilla fixup,
   `SavegameFixups.UpdateDroneUnreachableTimestamps` (`:947-958`) — our
   normalisation is now vanilla's. Module inactive (log `:96`, missing const).
3. **Report accurate?** CONFIRMED.
4. **Replacement correct?** PARTIAL, as §1h says: the time-based expiry was
   deleted, not repaired. A building that becomes reachable without any
   passability/Done/landscape bump stays written off by that drone until the
   64-cap evicts it. Not the `max_int` forever, and in practice most
   "unblocking" IS a passability change. Not measured.
5. **Player after REMOVE.** No change (inactive).
6. **Not opened.** What emits `OnPassabilityChanged` at engine level; dome
   open-air skin's passability effect.

### R-9 · `MeteorFrequency` (F02, F88)

1. **Our claim.** The `Meteors` global thread's long wait was a dead `if`, so
   strikes came every ~6h (`Code/Fix_MeteorFrequency.lua:6-14`); F88: our old
   LoadGame restart re-rolled the timer per load. Our fix: a `GetDisasterWarningTime`
   wrapper keyed on `CurrentThread() == _G.Meteors` (`:90-100`), a NewDay
   watchdog calling `RestartGlobalGameTimeThread("Meteors")` (`:118-155`), a
   one-shot latched restart on PostLoadGame (`:164-187`).
2. **1.1.0.** `MapGameTimeRepeat("Meteors", …)` (`Meteors.lua:297-323`): roll
   `Random(spawntime, spawntime + spawntime_random)` → store the persisted
   `g_NextMeteorsTime` (`:295`, `:313-316`) → return the remainder (`:318-319`)
   → fire when reached (`:306-311`). `warning_time` is not used in this cycle at
   all (only the storm repeat reads it, `:365`). `Meteors` is
   `GameVar("Meteors", false) -- required only for the savegame fixup` (`:388`);
   `GlobalGameTimeThreadFuncs` still exists (`Config/_fixup.lua:5-21`) but only
   two names register now (`SubsurfaceDeposit.lua:233`, `DayTime.lua:33`).
   `SavegameFixups.MeteorsThreadToRepeat2` deletes the old thread and any thread
   inside `MeteorsDisaster` (`:390-404`) — old persisted bodies (vanilla's, our
   07-25 copy) are cleaned by vanilla on first 1.1.0 load. Module inactive
   (log `:75`).
3. **Report accurate?** CONFIRMED, including the danger that the watchdog would
   `CreateGameTimeThread(nil)` if the Require were loosened.
4. **Replacement correct?** Yes. Persisted `g_NextMeteorsTime` means a load
   resumes the remainder (F88 closed by design). No residual found.
5. **Player after REMOVE.** No change; `SMRFixPack_MeteorLatch` GameVar stays
   inert in saves.
6. **Not opened.** `MapGameTimeRepeat` internals; `OverrideDisasterDescriptor`.

### R-10 · `MeteorStormWedge` (F78)

1. **Our claim.** The storm drain loop `while not g_MeteorStormStop and #spawned
   > 0 do WaitMsg("MeteorDone", delta); table.validate(spawned) end` never
   emptied (descriptors never invalid) and blocked the scheduler forever
   (`Code/Fix_MeteorStormWedge.lua:4-20`). Our fix: hourly watchdog + heal that
   `RestartGlobalGameTimeThread("MeteorStorm")`s and pulses `g_MeteorStormStop`.
2. **1.1.0.** Drain loop validates on the meteor OBJECT:
   `table.validate(spawned, function(descr) return IsValid(descr.meteor) end)`
   (`Meteors.lua:267-270`); every fall path ends in `DoneObject` (`Fall`
   `:588-611` at `:609`; `ExplodeInAir` `:632`) and `Done` posts `MeteorDone`
   (`:458-465`). The scheduler is `MapGameTimeRepeat("MeteorStorm", …)`
   (`:329-385`), calling `MeteorsDisaster` inline (`:349`). Load-time heals:
   `MeteorsThreadToRepeat2` (`:390-429`) and `MeteorStormEmptySpawnLeak`
   (`:1365-1375`). Module inactive (log `:144`).
3. **Report accurate?** CONFIRMED.
4. **Replacement correct?** PARTIAL — §1h's residual holds: the loop is still
   unbounded if a meteor object stays valid without ever reaching `DoneObject`
   (a dead `fall_thread` after `:598`'s Sleep, for instance). The load fixups
   run once per save lineage, so they are not an in-play heal for a wedge that
   happens later. Not measured.
5. **Player after REMOVE.** No change. A residual watchdog would be new code on
   a new mechanism (`RestartPeriodicRepeatThread`, not `RestartGlobalGameTimeThread`).
6. **Not opened.** `GenerateMeteor`; MDS interception path; fixup once-only
   bookkeeping (assumed standard).

### R-11 · `AsteroidLanderAvailable` (F72 + F94)

1. **Our claim.** `PlanetaryAsteroidVisitPossible` (gate) and
   `GetRocketsForExpedition` (list) disagreed both ways: the gate demanded
   `CmdWaitOrder`/`CmdOnEarth` (F72, a `CmdUnload` lander refused) and a
   mis-parenthesised `elseif` let any `WaitLaunchOrder` supply rocket open an
   empty picker (F94). Our fix: a body copy with both repaired
   (`Code/Fix_AsteroidLanderAvailable.lua:101-137`).
2. **1.1.0.** `PlanetaryAsteroidVisitPossible` has zero hits tree-wide. The gate
   is `HasRocketForDestination(spot)` (`PlanetaryView.lua:258-265`, called from
   `Data/XDef/PlanetaryView.lua:250,:420`, `PlanetaryViewAsteroidResources.lua:38`,
   `POIAdditionalContent.lua:69`) over `IsRocketAvailableForFlight`
   (`:245-252`: `UniversalRocketBase`, not a supply pod, player-controlled,
   `IsRocketLanded()`, `working`, `departure_loc == OurColony`) plus
   `GetAvailableFlightLocations()` (`UniversalRocket.lua:1031-1055`). The list
   `GetRocketsForExpedition` (`PlanetUI.lua:1701-1713`) filters on exactly the
   same two calls (`:1706-1707`). `UniversalRocketBase:IsRocketLanded` includes
   `CmdUnload` (`:1574-1577`). `SupplyRocketBase` is a `RocketBase`
   (`SupplyRocket.lua:2`) → fails the class test → F94 impossible.
   The old `not arrival_loc` term became `IsRocketOnOrder` + a cancel
   confirmation (`:254-256`, `:320-323`). Module inactive (log `:114`).
3. **Report accurate?** CONFIRMED.
4. **Replacement correct?** Yes. Note the other F72 case, `CmdWaitMaintenance`,
   is resolved as "not available" on BOTH surfaces (not in `:1576`), and a
   non-`working` rocket likewise — consistent, so no false negative of the
   reported kind. No residual found.
5. **Player after REMOVE.** No change.
6. **Not opened.** `UIPickDestination`; `NoAsteroidLanders` popup wiring beyond
   `PlanetaryView.lua:482-490`.

### R-12 · `GridGlobalStorage` (F22)

1. **Our claim.** `GetGridGlobalStorage` summed two maps' hours-of-autonomy
   ratios and counted a no-demand map as a 1000-hour sentinel
   (`Code/Fix_GridGlobalStorage.lua:5-24`); our replacement sums inputs then
   takes one ratio (`:74-103`).
2. **1.1.0.** `GetGridGlobalStorage`, `GetGridGlobalStorageInSols` and
   `ScriptCheckGridGlobalStorage` have zero hits in `Lua/`, `Data/`,
   `CommonLua/`, `DLC/`. The consumer is per-dome now:
   `ScriptFunc_DomesGridStorage` (`ScriptBlocks.lua:387-419`) judges each
   inhabited dome that draws the resource (`:393-394`), compares
   `MulDivRound(current_storage, HourDuration, demand) >= sols` (`:400-403`),
   and `judged == 0 ⇒ false` (`:410`). Module inactive (log `:125`).
3. **Report accurate?** CONFIRMED.
4. **Replacement correct?** Yes for F22 — no sum of ratios, no sentinel. One
   design residual, documented in the preset help (`:428`): with
   `SkipDomesInShortage = true` a colony where EVERY dome is in shortage has
   `judged == 0` → false, so the "No Dome has 2 sols" negatives cannot fire in
   the worst state they describe. Design, not defect.
5. **Player after REMOVE.** No change.
6. **Not opened.** `Dome:CheckShortage`; `consumption_for_overview` units.

### R-13 · `LastTransmissionStorage` (F75)

1. **Our claim.** Six storage likes put their list on `Prerequisite` instead of
   `Condition` (so `Eval` returned 0 forever) and `TLEOxygenStorage2Sols`
   measured Power (`Code/Fix_LastTransmissionStorage.lua:8-39`). Our data patch
   moves the list and retargets `GridType` (`:115-141`).
2. **1.1.0.** All twelve storage likes carry `'Condition'`
   (`Data/FactionDef/LastTransmission.lua:110,:123,:138,:155,:172,:187,:203,:221,:239,:254,:270,:288`);
   the six our module names are among them. Evals are generated
   `ScriptFunc_DomesGridStorage(<resource>, 1440000, …)` (`:113`, `:158`,
   `:242`); the Oxygen entry passes `"Oxygen"` (`:242`, `Resource = "Oxygen"`
   `:245`). `FactionLikeGlobalCondition:Eval` still reads only `Condition`
   (`Factions/FactionDef.lua:959-965`). Our pass finds `like.Condition` set and
   no `ScriptCheckGridGlobalStorage` node → latches benign (log `:179`).
3. **Report accurate?** CONFIRMED.
4. **Replacement correct?** Yes. `'Prerequisite'` is used only where intended
   (`:329`, `:383`, each paired with a `'Condition'`).
5. **Player after REMOVE.** No change.
6. **Not opened.** `FactionDef:EvalApproval`'s HowTo display path in 1.1.0.

### R-14 · `RainsDeadlock` (F81b + C34)

1. **Our claim.** `RainsDisasterLoop` did an untimed `WaitMsg("RainDisasterEnd")`
   after spawning an activation that returned early on any active/predicted
   disaster → that rain type never rained again (`Code/Fix_RainsDeadlock.lua:7-22`).
   Our fix: a pre-wrapper on `RainsDisasterActivation` that posts the Msg on
   collision (`:102-113`), plus a PostLoadGame migration that `DeleteThread`s
   activation threads and recreates them on `RainsDisasterLoop` (`:180-206`).
2. **1.1.0.** `RainsDisasterLoop` has zero hits. Rains are two `GameTimeRepeat`s
   (`TerraformingDisasters.lua:396-410`) over `RainsDisasterRepeatCycle`
   (`:363-387`): hourly poll while a rain or activation is alive (`:374-376`),
   else spawn-due → `CreateGameTimeThread(RainsDisasterActivation)` (`:378-382`).
   `RainsDisasterActivation` now opens with `WaitCurrentDisaster()` (`:319`;
   `MapSettings.lua:238-242`, hourly poll) instead of returning. No `WaitMsg`
   anywhere in the file. Module inactive (log `:146`, missing `RainsDisasterLoop`).
3. **Report accurate?** CONFIRMED, and the "re-arming would be HARMFUL" point is
   right for a second reason: our wrapper's collision test would CANCEL a rain
   that vanilla now delivers after waiting.
4. **Replacement correct?** Yes for F81b. **§1h's residual is overstated
   (DISPUTED as written):** it says the load fixup `RainsDisasterLoopToRepeat2`
   deleting activation threads (`:485-487`) strands `DisasterNormalRains`. But
   the same function's `elseif not rain_disaster` branch (`:503-507`) calls
   `RemoveRainDisasterNotification` for every rain type, which nils exactly that
   flag (`:254-256`). The only way to reach `:485` with the flag set AND a rain
   active (so the else-branch is skipped) is a rain started under an existing
   normal-rain warning, which `WaitCurrentDisaster` forbids — leaving the cheat
   path `CheatRainsDisaster` (`:669-673`). Every other path that kills an
   activation clears the flag (`CancelRainsActivation` `:262-273`,
   `UpdateRainsThreads` `:631-633`). Cheat-only, not a residual for players.
5. **Player after REMOVE.** No change; the C34 structure/stale-ACTIVE heal is
   now vanilla's own fixup (`:483-517`).
6. **Not opened.** `UpdateRainsThreads` `:528-600`; `RainProcedure` past `:210`.

### R-15 · `DustSicknessDamage` (F17)

1. **Our claim.** The trait's `daily_update_func` computed `change = 5 +
   Random(param)` and then applied a flat `-trait.param`
   (`Code/Fix_DustSicknessDamage.lua:3-8`); our data patch replaces the function
   with one that applies `change` (`:31-36`, `:60`).
2. **1.1.0.** The hook is RENAMED `DailyUpdate(trait, colonist)`
   (`Data/TraitPreset.lua:81-85`), declared with default `empty_func`
   (`Lua/TraitPreset.lua:36-37`) and dispatched by `Colonist:TraitMethod`
   (`Colonist.lua:711` → `:596-604`, `trait[method](trait, self)`). The body
   is `if g_DustStormStart then colonist:ChangeHealth(-trait.param*const.Scale.Stat, trait.id) end`
   — the dead `change` line is DELETED and the flat damage KEPT. `param = 10`
   (`:94`). Our pass tests `trait.daily_update_func` → nil → latches
   "has no param/daily_update_func" (log `:178`) — a false-negative-on-rename
   latch that happens to land on the right answer.
3. **Report accurate?** CONFIRMED (the corrected row). The row's Infected
   comparison (`:143-147`) I did not open.
4. **Replacement correct?** It is a resolution, not a fix: the contradiction was
   settled by removing the randomness. Sound as code (`empty_func` default keeps
   `:601` safe for traits without a hook). Whether 5-14 or flat 10 was intended
   is now unknowable from the source; with the intent tell gone, reinstating the
   spread would be a balance change.
5. **Player after REMOVE.** No change (inactive). ⚠️ Retargeting the module to
   `DailyUpdate` "because the latch is a rename false negative" would ship a
   balance change against the shipped design — see half-baked §.
6. **Not opened.** `Data/TraitPreset.lua:143-147` (Infected); any other trait
   whose 1.0.7 hook survived the rename.

### R-16 · `IndependenceTerraforming` (F18)

1. **Our claim.** `param1 = 20` ("decrease percent") but the effect's `Amount =
   -10` (`Code/Fix_IndependenceTerraforming.lua:4-14`); our data patch sets
   `Amount = -20` on `TechDef.Independence_TerraformingProjects` (`:62-110`)
   and a LoadGame sweep re-applies it to researched saves (`:126-173`).
2. **1.1.0.** The live tech (`Data/Tech.lua:3552-3579`, class `Tech`, map
   `Techs` per `TechTree.lua:280`, read by research at `Research.lua:151,:219`)
   has `param1 = -10` (`:3560`, comment "decrease percent" `:3561`) and
   `Amount = -10` (`:3572`) with `param_bindings = { Amount = "param1" }`
   (`:3575-3577`). Consumer unchanged: `MulDivRound(res.amount,
   g_Consts.SpecialProjectResourcesModifier, 100)` (`SpecialProjects.lua:117`).
   Our pass writes into `TechDef` — the LEGACY `TechPreset` map
   (`ClassDef-PresetDefs.generated.lua:1709-1729`), whose entry
   (`Data/TechPreset.lua:715-719`) still says `param1 = 20` but carries NO
   effect child → `found == 0` → latch (log `:180`). Inactive.
3. **Report accurate?** CONFIRMED, with one wording correction: "`Amount` is
   BOUND to `param1`" is an editor-time relation — `param_bindings` is listed as
   an ignored non-property member (`ClassDefFunctionObjects.lua:53-59`) and is
   read only by `Ged.lua:2676,:3140`. At runtime both are literal `-10`. Still
   self-consistent, so the verdict stands.
4. **Replacement correct?** Resolved DOWN to 10%, both numbers agree, nothing
   contradicts (the description carries no percent, `:3553`). Design, not fix.
5. **Player after REMOVE.** No change. ⚠️ "Fixing" our latch by pointing the
   pass at `Techs` would make the module write `-20` over a resolved `-10` and
   the LoadGame sweep would re-apply it to researched colonies — see half-baked §.
6. **Not opened.** Whether any runtime code resolves `PresetParamNumber` into
   effects (none found in `CommonLua/Classes`); `Effect_ModifyLabel:OnApplyEffect`
   in 1.1.0.

### R-17 · `UniversityOvertraining` (F36)

1. **Our claim.** `City:GetNeededSpecialist` counts an automated extractor's
   posts as demand although staffing "changes literally nothing"
   (`Code/Fix_UniversityOvertraining.lua:3-17`); our full body copy adds
   `and (building.automation or 0) <= 0` (`:74-75`).
2. **1.1.0.** The body (`City.lua:631-668+`) still has no automation gate
   (`:648`) but was rewritten to reuse its cache table (`:637-642`,
   `table.clear`). The premise is gone: `Workplace:GetWorkshiftPerformance`
   now does `performance = Max(performance, self.auto_performance)` when
   `automation > 0` (`Workplace.lua:283-287`; also `:332-333`, `:377`,
   `:433-434`) — automation is a FLOOR. Extractor AI sets `auto_performance =
   50` (`Data/Tech.lua:857`, `:867`), so a geologist crew performing above 50
   raises output. Module applied (log `:106`), i.e. it currently REPLACES the
   1.1.0 body and hides that demand.
3. **Report accurate?** CONFIRMED. I would firm the judgement: on 1.1.0 the
   module is wrong on its own premise, not merely an opinion — staffed
   extractors do produce more than the floor, so specialists ARE needed there.
4. **Replacement correct?** Vanilla's demand count is right for the floor
   semantics. No residual.
5. **Player after REMOVE.** Universities resume training geologists for
   automated extractors — correct under the floor; and the 1.1.0 body's cache
   reuse returns. KEEP would ship a 1.0.7 body over a rewritten one.
6. **Not opened.** `MartianUniversity` consumers in 1.1.0; `Colony:GetNeededSpecialist`
   (`Colony.lua:760`).

### R-18 · `CaveInsNoDisasters` (F01)

1. **Our claim.** The `UndergroundMarsquake` repeat never checked the No
   Disasters rule (`Code/Fix_CaveInsNoDisasters.lua:3-8`); we wrap
   `PeriodicRepeatInfo.UndergroundMarsquake[3]` to return the interval without
   quaking while the rule is on (`:35-43`).
2. **1.1.0.** `MapGameTimeRepeat("UndergroundMarsquake", …)` (`Marsquake.lua:336-354`)
   condition: `GetEnvironment(map) == "Underground" and HasGameLogic(map) and
   UIColony and UIColony.underground_map_unlocked and not IsGameRuleActive("NoDisasters")`
   (`:351-354`). The surface repeat checks it too (`:66-68`). Slot layout is
   unchanged (`lib.lua:1559` THREAD=1, `:1561` FUNC=3), so our wrapper still
   lands (log `:74` applied) and is redundant: with the condition false the
   repeat's thread does not run at all.
3. **Report accurate?** CONFIRMED.
4. **Replacement correct?** Yes; the rule is fixed at game start. No residual.
5. **Player after REMOVE.** No change.
6. **Not opened.** `lib.lua:1566-1710` repeat driver; `ObjRepeatRestart`.

### R-19 · `CommandCenterNumbers` (F13)

1. **Our claim.** Command Center rows rendered `<metals(AvailableMetals)>`
   against eleven getters that no longer existed
   (`Code/Fix_CommandCenterNumbers.lua:3-15`); we add eleven
   `GetAvailable<Res>` shims (`:33-44`).
2. **1.1.0.** Every row renders `<resource(GetAvailable('<Res>'), '<Res>')>`
   (`Data/XDef/CommandCenterCategories.lua:226,:232,:238,:244,:255,:261,:267,:273,:315,:322,:328`
   — all eleven including WasteRock at `:328`); only Rockets/Pods keep named
   getters (`:118`, `:124`; `ResourceOverview.lua:356`, `:368`).
   `ResourceOverview:GetAvailable(resource_type)` (`:212-214`). No
   `GetAvailableMetals`/`GetAvailableFood` anywhere in `Lua/`+`Data/`. Our shims
   install (log `:103` applied) and are called by nothing.
3. **Report accurate?** CONFIRMED.
4. **Replacement correct?** Yes. No residual.
5. **Player after REMOVE.** No change.
6. **Not opened.** The generated XDef twin; `RoundDownResourceAmount`.

### R-20 · `DisasterPredictionLeak` (F81a)

1. **Our claim.** `AddDisasterNotification` sets `g_DisastersPredicted[id]` and
   only `RemoveDisasterNotifications` clears it; the meteor-storm duration
   notification expired through the notification lib without clearing, so
   `IsDisasterPredicted()` stayed true forever (`Code/Fix_DisasterPredictionLeak.lua:3-26`).
   Our fix: an additive `MeteorStormEnded` handler (`:81-89`) and a sweep on
   PostLoadGame + NewDay clearing any flag with no live notification (`:93-117`).
2. **1.1.0.** `EndMeteorStorm` removes first (`Meteors.lua:1204-1212`, `:1205`)
   and is called on every storm end (`:234`, `:279`); the storm repeat removes
   too (`:335`, `:346`). Expiry: the lib sets `notification.expired = true`
   BEFORE `RemoveNotification` (`Notifications.lua:229-232`) →
   `DeleteNotification` → `Msg("RemoveNotification")` (`:129`) →
   `OnMsg.RemoveNotification` nils the flag (`MapSettings.lua:223-228`). A
   load fixup clears four known ids (`Meteors.lua:1346-1363`). F81a is closed
   on every path. **But** flag-without-notification is now a LEGITIMATE state:
   normal rains set `g_DisastersPredicted.DisasterNormalRains = true` with no
   notification (`TerraformingDisasters.lua:349`; `DisasterNormalRains` is not a
   preset — zero hits outside `:256`/`:349`) for the warning window
   (`GetDisasterWarningTime`, up to `const.SensorTowerPredictionMaxTime`,
   `MapSettings.lua:122-126`), cleared at `:314` → `:256` when the rain starts.
   Module applied (log `:143`).
3. **Report accurate?** CONFIRMED on the vanilla fix; **DISPUTED on the
   module-impact cell** "the load/NewDay sweep polices an invariant vanilla
   keeps". Vanilla does NOT keep that invariant (`:349`). Our sweep's predicate
   `v and not FindNotification(id)` (`Code/…:97-98`) is true for
   `DisasterNormalRains` throughout a normal-rain warning, so on any NewDay or
   load inside that window the applied module clears a legitimate flag.
4. **Replacement correct?** Yes. **Our module is now a live harm, not a
   redundancy:** with the flag cleared, `IsDisasterPredicted()` (`:230-236`) no
   longer sees the incoming rain, so a dust storm (`DustStorm.lua:516-517`,
   `:559`), a cold wave (`ColdWave.lua:180-181`, `:198`, `:337`) or a toxic-rain
   activation (`WaitCurrentDisaster`, `TerraformingDisasters.lua:319`) may start
   on top of it; `RainProcedure` does not re-check (`:188-210`). Bounded (one
   warning window per rain), not measured, but it is exactly the class of
   interaction the sweep's own header rules out ("stranded by construction").
   §1h's "our sweep was the only belt for flags WITHOUT a notification" is the
   same fact read as a benefit: the sweep cannot tell stranded from legitimate,
   and the only stranding route left is cheat-only (R-14 §4).
5. **Player after REMOVE.** Vanilla's remove-on-end + clear-on-expiry; the
   normal-rain warning gate works as designed again. REMOVE is right and is the
   most urgent of my rows.
6. **Not opened.** `AddNotification` `:1-54`; `ExtendDustStorm`/`ExtendColdWave`.

---

### Summary table

| row | module | claim | replacement correct? | patch impact | evidence |
|---|---|---|---|---|---|
| R-6 | `SmallLandscapeSites` | CONFIRMED | yes | REMOVE restores 10 candidates (we narrow to 5) | `LandscapeConstructionSiteBase.lua:172,:175-177,:204-208,:217` |
| R-7 | `DroneTransportMinors` (b) | CONFIRMED | yes; `next(false)` at `:611` unsampled | REMOVE (b) only; (a) unchanged, stays (K-8) | `Drone.lua:73,:611,:935-945,:966`; `DroneControl.lua:674,:693` |
| R-8 | `DroneUnreachableForever` | CONFIRMED | partial (expiry deleted, not repaired) | none (inactive) | `Drone.lua:909,:947-958,:971-976`; `Building.lua:528,:546` |
| R-9 | `MeteorFrequency` | CONFIRMED | yes | none (inactive); latch GameVar inert | `Meteors.lua:295-323,:388,:390-404` |
| R-10 | `MeteorStormWedge` | CONFIRMED | partial (loop still unbounded) | none (inactive) | `Meteors.lua:267-270,:329-349,:588-611,:1365-1375` |
| R-11 | `AsteroidLanderAvailable` | CONFIRMED | yes | none (inactive) | `PlanetaryView.lua:245-265`; `PlanetUI.lua:1701-1713`; `UniversalRocket.lua:1574-1577` |
| R-12 | `GridGlobalStorage` | CONFIRMED | yes (design residual `judged==0`) | none (inactive) | `ScriptBlocks.lua:387-419,:428` |
| R-13 | `LastTransmissionStorage` | CONFIRMED | yes | none (inactive, benign latch) | `LastTransmission.lua:110-116,:155-164,:239-247`; `FactionDef.lua:959-965` |
| R-14 | `RainsDeadlock` | CONFIRMED; §1h residual overstated (fixup clears it, `:503-507`) | yes | none (inactive); re-arming would cancel rains | `TerraformingDisasters.lua:319,:363-410,:483-508,:669-673` |
| R-15 | `DustSicknessDamage` | CONFIRMED (corrected row) | resolved the other way (flat kept) | none; do NOT retarget to `DailyUpdate` | `Data/TraitPreset.lua:81-85`; `Lua/TraitPreset.lua:36-37`; `Colonist.lua:596-604,:711` |
| R-16 | `IndependenceTerraforming` | CONFIRMED ("bound" is editor-only) | resolved down to 10% | none; do NOT retarget to `Techs` | `Data/Tech.lua:3560,:3572,:3575-3577`; `Data/TechPreset.lua:715-719`; `PresetDefs:1709-1729` |
| R-17 | `UniversityOvertraining` | CONFIRMED; judgement should be REMOVE | yes | REMOVE restores real demand + 1.1.0 body | `Workplace.lua:283-287`; `Data/Tech.lua:857,:867`; `City.lua:637-648` |
| R-18 | `CaveInsNoDisasters` | CONFIRMED | yes | none (redundant wrapper) | `Marsquake.lua:351-354`; `lib.lua:1559-1561` |
| R-19 | `CommandCenterNumbers` | CONFIRMED | yes | none (inert shims) | `CommandCenterCategories.lua:226-328`; `ResourceOverview.lua:212-214` |
| R-20 | `DisasterPredictionLeak` | CONFIRMED on the fix; DISPUTED on "invariant vanilla keeps" | yes | REMOVE is urgent: applied sweep clears the legitimate `DisasterNormalRains` flag | `TerraformingDisasters.lua:349,:256`; `MapSettings.lua:223-236`; `DustStorm.lua:559`; `ColdWave.lua:198`; `Code/Fix_DisasterPredictionLeak.lua:97-103` |

### What would make the patch half-baked

Ranked. Acting on every REMOVE verdict in R-6…R-20 as written ships nothing
wrong; the risks are in NOT removing, removing the wrong half, or "fixing" a
latch instead of removing.

1. **R-20 — keeping or augmenting the sweep.** §1h frames the sweep as "the
   only belt for flags without a notification"; if the patch keeps it on that
   reasoning it keeps a handler that clears `g_DisastersPredicted.DisasterNormalRains`
   during every normal-rain warning it lands in. Proof: the flag is set with no
   notification at `TerraformingDisasters.lua:349`, `DisasterNormalRains` is not
   a `NotificationPresets` id (zero hits), and the sweep clears on
   `not FindNotification(id)` (`Code/Fix_DisasterPredictionLeak.lua:97-98`),
   after which `IsDisasterPredicted()` (`MapSettings.lua:230-236`) lets a dust
   storm/cold wave through (`DustStorm.lua:559`, `ColdWave.lua:198`). Remove
   the whole module.
2. **R-17 — "owner call" resolving to KEEP.** The applied body copy replaces a
   rewritten 1.1.0 function (`City.lua:637-642` cache reuse) and hides demand
   that is real under the floor: `Workplace.lua:285-286`
   `performance = Max(performance, self.auto_performance)` with
   `auto_performance = 50` (`Data/Tech.lua:857`). Remove.
3. **R-16 — repairing the latch instead of removing.** The pass is inactive only
   because it targets the legacy `TechDef` map whose entry has no effect
   (`Data/TechPreset.lua:715-719`). Pointing it at `Techs` (`TechTree.lua:280`)
   would write `-20` over the resolved `-10` (`Data/Tech.lua:3560`, `:3572`)
   and the LoadGame sweep (`Code/…:126-173`) would re-apply it to researched
   colonies. Remove.
4. **R-15 — repairing the rename false negative instead of removing.** Retargeting
   to `DailyUpdate` (`Lua/TraitPreset.lua:36-37`) would reinstate a 5-14 roll
   the developers deleted in favour of the flat value
   (`Data/TraitPreset.lua:81-85`). Remove.
5. **R-7 — deleting the file rather than the (b) handler.** Part (a)'s defect
   is unchanged (`DroneControl.lua:674` clears only `.Fuel`; `:693` writes
   `r_t[r.FuelResource]`) and the report keeps it (K-8). Remove `repair_unreachables`
   + `OnMsg.OnPassabilityChanged` (`Code/Fix_DroneTransportMinors.lua:139-160`)
   only; keep `:163-207` and its Require entries for `UpdateRocketsInternal`.
6. **R-14 — carrying §1h's "stranded by the fixup" residual into the patch as
   a reason to keep any sweep.** The cited fixup clears the flag itself
   (`TerraformingDisasters.lua:503-507` → `:256`); the only stranding route is
   the cheat (`:669-673`). Nothing to keep.

No half-baked risk found in R-6, R-8, R-9, R-10, R-11, R-12, R-13, R-18, R-19
when acted on as REMOVE: for each I opened the 1.1.0 body named in the row and
the module's Require/latch (boot log `:74-:190`), and either the target is gone
(R-9, R-10, R-11, R-12, R-14) or the applied module is a strict no-op against
the shipped body (R-6 narrows, R-18/R-19 inert).

---

## Reader C — rows R-21…R-36

### VANILLA-FIX QA — section C, rows R-21 … R-36

Reader: fresh context, 2026-09-08. Method per `prompts/VANILLA_FIX_QA.md`: for each
row the module under `Code/` and the shipped 1.1.0 target under
`A:\SteamLibrary\steamapps\common\Project Spark\ModTools\Src` were read and a verdict
formed BEFORE the report's row and §1h were opened. All `file:line` below are the
1.1.0 tree unless prefixed `Code/`. One extra control was run: `Local/German.fpk`
was extracted with `tools/flpk_extract.py` (this session, scratchpad `loc/German/`)
so translation-id claims are checked against a real 1.1.0 pack, not inferred.

### R-21 · `DustDevilSpawnGate` (F97)

1. **Our claim.** Old `DustDevils.lua:216` multiplied the wave COUNT by `spawn_chance/100`; we pre-roll the gate in a wrapper on `OverrideDisasterDescriptor` and hand the thread a copy with `spawn_chance=100` and `count 0/0` on a failed roll (`Code/Fix_DustDevilSpawnGate.lua:240-247`).
2. **1.1.0.** The scheduler is rewritten as a `MapGameTimeRepeat("DustDevils", …)` state machine (`Lua/DustDevils.lua:235-294`). The descriptor is fetched at the top of EVERY tick (`:237`). Count line `:256`: `SessionRandom:Random(100) < descr.spawn_chance and SessionRandom:Random(descr.count_min, descr.count_max) or 0`; `count < 1` → idle and `return 0` (`:257-261`). Same idiom as the marker path `:174`.
3. **CONFIRMED.**
4. **Replacement correct.** Gate-then-count; `Random(100)` is 0..99 so chance 100 always passes; a zero wave re-enters idle and immediately re-arms a countdown. No residual.
5. **Player on REMOVE.** Exactly vanilla. Worth stating: on 1.1.0 our wrapper is not merely redundant — `:237` runs per tick, including the `return 5000` loop while a dust storm is up (`:249-251`), so it burns a `SessionRandom` draw and builds a descriptor copy every 5 s in a storm. Effective probability is unchanged (vanilla's gate tests our 100 and always passes), but the header's "one extra draw per wave" is now many per wave.
6. **Not opened.** `OverrideDisasterDescriptor`'s 1.1.0 body (TerraformingDisasters.lua) and the 1.1.0 `MapSettings-DustDevils` preset values.

### R-22 · `DustDevilsDescrMap` (F93)

1. **Our claim.** `GetDustDevilsDescr` read `CurrentMap` twice; our copy reads `MainMap` (`Code/Fix_DustDevilsDescrMap.lua:60-68`).
2. **1.1.0.** `Lua/DustDevils.lua:58-66` reads `MainMap.mapdata.MapSettings_DustDevils` at `:59` and `:64` — byte-identical to our body. The scheduler additionally filters `map == MainMap` (`:292-294`) and `OnMsg.DisasterSettingsApplied` returns on `map ~= MainMap` (`:215`).
3. **CONFIRMED.**
4. **Replacement correct** — it is our function. No residual.
5. **Player on REMOVE.** Identical.
6. **Not opened.** `Cheats.lua`'s own map read (a separate caller our header excluded).

### R-23 · `DustStormUndergroundBreaks` (F90)

1. **Our claim.** `RandomBreakConnection` picked from an unfiltered cross-map connector list; we swap in a MainMap-only list around `orig` (`Code/Fix_DustStormUndergroundBreaks.lua:150-189`).
2. **1.1.0.** `Lua/SupplyGrid.lua:1097` takes `map`; `:1106-1112` `table.ifilter`s BOTH `connectors` and `elements` by `e.building:GetMap() == map` and returns on an empty pool; `SupplyGrid:RandomBreakElements` `:1517-1521` passes `self.city:GetMap()`; `City.lua:153` still gates on `HasDustStorm(self:GetMap())`, and `DustStorm.lua:41-44` is `MainMap == map`.
3. **CONFIRMED.**
4. **Replacement correct, and stricter than ours** — the probability exponent `#elements` (`:1114`) is per-map too, which closes the residual our header left open. Residuals: (a) `:1108-1109` call `e.building:GetMap()` with no validity test — a connector with a dead `building` would raise where our wrapper skipped it; vanilla's own `:1119-1120` already assumed `element.building` non-nil, so this is not new. (b) `IsBreakable` `:1136` still counts ALL connectors, so the ">10" gate is looser than the pool — harmless, the empty-pool return at `:1110` covers it.
5. **Player on REMOVE.** Vanilla's filter. Our swap made `IsBreakable` count surface connectors only; removal lets a merged fragment with ≤10 surface but >10 total connectors roll again — vanilla's intent.
6. **Not opened.** `BreakableSupplyGridElement:Break` and `MergeGrids` in 1.1.0.

### R-24 · `ExtractorStaffedPerformance` (F108, F111)

1. **Our claim.** `GetWorkshiftPerformance` returned `auto_performance` outright for `automation > 0`; owner ruled FLOOR; our post-wrapper re-derives the staffed value and returns it when higher (`Code/Fix_ExtractorStaffedPerformance.lua:112-125`).
2. **1.1.0.** `Lua/Buildings/Workplace.lua:269-294`: rubble → 0 (`:270-272`); `max_workers == 0` → auto/NoWorkers (`:279-281`); `performance = self:GetWorkersPerformance(shift)` (`:283`); `if self.automation > 0 then performance = Max(performance, self.auto_performance)` (`:285-287`). `GetWorkersPerformance` `:250-267` is the per-worker loop over `worker:GetWorkPerformance()` (`Lua/Units/Colonist.lua:794-796` = `Max(self.performance, 25)`) plus the `IsOvertime()` additive (`:263-265`; `:718-729` collapses the shift table to a boolean).
3. **CONFIRMED.** Independently reached the same "dead except rubble": our reconstruction can never exceed `orig`'s (same floor-25 loop; overtime additive either equal or absent on our side), but `orig` returns 0 for rubble and our wrapper does not check rubble, so a rubble-shrouded automated staffed extractor reports a positive value.
4. **Replacement correct** — the floor ruling verbatim. No residual.
5. **Player on REMOVE.** Vanilla floor; Russia's goal (`Data/SponsorGoals.lua:565` `extractor.performance >= performance`) is reachable by staffing. Removal also deletes the one wrong case.
6. **Not opened.** The C39 wrapper's 1.1.0 interplay; the ExtractorAI tech text in 1.1.0.

### R-25 · `LanderReturnFuel` (F69)

1. **Our claim.** `GetFuelResourceRequest` returned 0 with no `arrival_loc`, so after manual-mode `CmdLand` cleared the destination the reserved return ration was unloaded; we return `(reserve, reserve)` for a lander parked on an asteroid (`Code/Fix_LanderReturnFuel.lua:38-48`).
2. **1.1.0.** `Lua/UniversalRocket.lua:1891-1908`: no `arrival_loc` → `self:IsPlayerControlled() and not self:IsSpecialAutomode() and amount or 0` (`:1894`), a SINGLE return value; a LanderRocket is player-controlled (`:2631-2638`) and not special (`:2020-2026`). Order in `CmdLand`: `ConsumeFuel()` `:436` (destination still set → policy `(2x, x)` → burns x, `:1922-1931`), then `SetFlightData` clears it `:441`, then `CmdUnload` zeroes `requested` (`:577`) but the status check re-adds `GetFuelResourceRequest()` (`Lua/CargoTransporterNew.lua:1294-1296`) and the demand request carries it (`:1442`) → hold == request → "ready". `ConsumeFuel` has exactly one caller (`:436`), so the single-value branch never feeds `fuel_to_consume - nil`.
3. **PARTIAL.** The verdict holds; the sentence "our second return unreachable" does not. Two rollover builders read both values: `:3428-3436` (status) and `:3614-3623` (`GetFuelRequestText`). With ours, `target = requested - return_trip = 0` and a "Return trip fuel" row appears for a parked lander; vanilla prints "Fuel x/amount" and no return row. Cosmetic — another reason to remove, not a rebreak.
4. **Replacement correct.** Residuals: `refuel_disabled` (`:1442`) is the player's own toggle; the one-way `return_fuel_disabled` logic (`:1900-1903`) sits under `arrival_loc` only.
5. **Player on REMOVE.** One ration stays aboard; the infopanel shows the plain Fuel row.
6. **Not opened.** `Data/FlightPolicyDef.lua` `OnGetFuelResourceRequest` in 1.1.0; `StartManualEarthTrip`.

### R-26 · `LandscapeCostRefresh` (F105/F107)

1. **Our claim.** `RefreshConstructionResources` indexed `construction_costs_at_start == false` on landscape sites; our pre-wrapper returns when it is falsy (`Code/Fix_LandscapeCostRefresh.lua:92-98`).
2. **1.1.0.** `Lua/Buildings/ConstructionSite.lua:721` `if not self.construction_costs_at_start then return end -- subclasses that manage their own resources (e.g. LandscapeConstructionSite) don't track start costs`; body `:719-749`; the gatherer still creates both tables together (`:694`, `:707`).
3. **CONFIRMED.**
4. **Replacement correct** — same guard, same position (after the group-leader test `:720`, before the loop). The new tail `StartConstructionPhaseIfReady()` (`:748`) is also skipped by the guard, which is right for a volume-driven site. No residual.
5. **Player on REMOVE.** Identical.
6. **Not opened.** The three landscape `GatherConstructionResources` overrides in 1.1.0 (irrelevant given `:721`).

### R-27 · `LocalizedUIText` (C51)

1. **Our claim.** The terraforming heading was a plain string with no T id; the rocket "Back to Earth" button used two ids no pack contains (`Code/Fix_LocalizedUIText.lua:8-19`).
2. **1.1.0.** `Lua/XDef/TerraformingOverall.generated.lua:57` `Text = T(914616772802, "OVERALL TERRAFORMING PROGRESS")` (mirror `Data/XDef/TerraformingOverall.lua:52`). `idBackToEarth`, `807999655245`, `885571832096` are absent from `Lua/` and `Data/` (grep); the feature moved to an XAction `actionBackToEarth` in `Lua/XDef/GameShortcuts.generated.lua:1430-1446`, `ActionName = T(192345398558, "Back to Earth")`, driving `UniversalRocketBase:UIBackToEarth()` (`Lua/UniversalRocket.lua:2834-2839`). German 1.1.0 pack, `CurrentLanguage/Game.csv`: `192345398558 → "Zurück zur Erde"` (row cites `GameShortcuts.generated.lua(01432)`), `914616772802 → "TERRAFORMING-GESAMTFORTSCHRITT"`; the two broken ids are absent.
3. **CONFIRMED** — and the sub-reader's "possibly NEW untranslated string" is RESOLVED: the new id is enrolled and translated. Nothing is owed there.
4. **Replacement correct.** The old rollover sentence (`316233855405`) is no longer rendered anywhere — a design change (the action has only a name), not a defect.
5. **Player on REMOVE.** Nothing. Today the module installs (its Require `Code/…:328-342` passes: broken ids unenrolled, good ids enrolled, both `Init`s exist at `TerraformingOverall.generated.lua:18` / `customUniversalRocket.generated.lua:11`) and declines once per site with a log line (`:225-226`, `:269-270`).
6. **Not opened.** The other eight language packs (German only); `Data/XDef/GameShortcuts.lua`.

### R-28 · `MilestoneCrash` (F05)

1. **Our claim.** `eval_complete_all_milestones` summed a nil `GetScore()` for hidden milestones; we replace `CompleteMilestone` with a nil-safe copy (`Code/Fix_MilestoneCrash.lua:137`).
2. **1.1.0.** `Lua/Milestones.lua:116` `score_sum = score_sum + (milestone:GetScore() or 0)`; loop `:105-123`; `CompleteMilestone` `:125-159` otherwise identical to our copy (only the popup thread now takes explicit params, `:118-120`).
3. **CONFIRMED.**
4. **Replacement correct.** No residual.
5. **Player on REMOVE.** Identical.
6. **Not opened.** `Milestone:GetScore`.

### R-29 · `MoraleComfortTooltip` (F20)

1. **Our claim.** The Morale tooltip printed a "+Comfort" high-stat row that `UpdateMorale` had stopped granting; we rawset a temporary `GetProperty` on the colonist around the shipped text builder (`Code/Fix_MoraleComfortTooltip.lua:95-112`).
2. **1.1.0.** `Lua/Units/Colonist.lua:4862-4883` `UpdateMorale` now computes work performance from morale — no threshold sum at all. `UIStatUpdate` `:3784-3882`: the Morale/Comfort rollover is `AppendColonistOutlook` (`:3852-3855` → `Lua/Stats.lua:915-925`, `ColonistOutlookBreakdown` `:814-913`), a source list (traits, services, work, rest, permanent log, `base_morale` modifiers). No `value >= high` row loop exists. `GetProperty(stat)` is read only at `:3796` (bar) and `:3821` (`GetRolloverTitleRight`, which we do not wrap).
3. **CONFIRMED.**
4. **A rewrite, not a repair** — nothing of the old row survives to be wrong. Our override is inert (grep: no `GetProperty("Comfort")` anywhere under the shipped `GetRolloverText`), but it is still an instance-level `rawset` on every hover — pure risk if a future builder reads `GetProperty`.
5. **Player on REMOVE.** No visible change.
6. **Not opened.** `ConditionalStatImpacts` `Condition` bodies (grep shows none call `GetProperty("Comfort")`).

### R-30 · `SpaceYDroneCapBullet` (C50)

1. **Our claim.** SpaceY's `effect` text omitted its `+20 CommandCenterMaxDrones` modifier; we append a bullet at three pre-game render sites, gated on the id, the modifier and id 4706 (`Code/Fix_SpaceYDroneCapBullet.lua:269-311`).
2. **1.1.0.** `Data/MissionSponsorPreset.lua:631` keeps id `880574954148` and now reads "… Drone Hubs start with additional Drones and can control up to 40 Drones"; modifiers `:702-711` (Amount 20 on `CommandCenterMaxDrones`, base 20 at `Lua/__const.lua:63-67` → 40). German row for `880574954148` carries the updated sentence ("… und können bis zu 40 Drohnen steuern"). All three wrapped globals still exist (`Lua/PreGameMission.lua:551`, `:619`; `Lua/UI/PlanetUI.lua:364`).
3. **CONFIRMED.**
4. **Replacement correct.** Residual: "40" is a literal — a base-const change would stale the text (ours computed it). Our gates (`:279` id, `:300` value > base, `:304` 4706 enrolled) all pass → a fourth bullet duplicating bullet 3 on every pre-game sponsor screen today.
5. **Player on REMOVE.** The duplicate disappears.
6. **Not opened.** The other seven non-English packs; the three render sites' 1.1.0 bodies.

### R-31 · `StorageRateModifiers` (F27)

1. **Our claim.** All three `OnModifiableValueChanged` handlers listened for the rate props but copied only capacity/efficiency to the grid element; our post-wrapper copies `max_charge`/`max_discharge` (`Code/Fix_StorageRateModifiers.lua:54-69`).
2. **1.1.0.** `Lua/ElectricityStorage.lua:47-65` copies both rates (`:55-56`) and ships `SavegameFixups.SyncStorageMaxChargeDischarge` (`:239-248`). `Lua/LifeSupportStorage.lua` `WaterStorage` `:25-42` and `AirStorage` `:126-143` still do NOT copy the rates (`:32-33`, `:133-134`) while still naming them in the condition (`:27-28`, `:128-129`); the rate props carry no `modifiable = true` (`:9-10`, `:109-110`; capacity does, `:12`, `:112`). The LIVE gate is the game's own `Modifiable` (`Lua/Modifiers.lua:4` redefines the CommonLua class): `Modifiable:UpdateModifier` returns before anything `if not self:HasMember(base_prop)` (`:47-49`), and `base_<prop>` is created only for `meta.modifiable` props (`InitBaseProperties` `:30-37`). Every shipped route ends there — `SetModifier` `:181` → `UpdateModifier`; `LabelContainer:SetLabelModifier` `Lua/LabelContainer.lua:59-77` → `UpdateModWith/WithoutCheck` `:49-57` → `UpdateModifier`; `AddToLabel` `:16-27` → `UpdateModifier`.
3. **CONFIRMED, citation corrected.** The report grounds "can never fire" on `CommonLua/Classes/Modifiers.lua:106-109` / `:286` — that is `AddModifierObj`, the CommonLua path this game's `Lua/Modifiers.lua` redefinition does not use. The real gate is `Lua/Modifiers.lua:47-49` with `:30-37`. Same conclusion, right line.
4. **Electricity correct. Water/air unreachable, not fixed** — exactly §1h's residual, plus one route it does not name: `Modifiable:SetBase(prop, v)` (`Lua/Modifiers.lua:120-128`) writes `base_` itself and calls `OnModifiableValueChanged` directly, bypassing the gate. Mod-code only; no shipped caller.
5. **Player on REMOVE.** Nothing shipped changes. F27's stated purpose was the modding surface; on 1.1.0 that surface is closed by the missing flag rather than repaired.
6. **Not opened.** Whether any 1.1.0 tech/DLC now modifies the electricity rates (the reason the fixup exists); `NewSupplyGridStorage` beyond `:171-172`.

### R-32 · `TechDescriptionBuilding` (F25)

1. **Our claim.** The UndergroundLargeDome tech description named "Jumbo Cave Reinforcements"; we rewrite `TechDef[...].description` under the same T id when the literal is found (`Code/Fix_TechDescriptionBuilding.lua:52-77`).
2. **1.1.0.** `Data/Tech.lua:6738` `Description = T(841885693955, "Building: <em>Underground Medium Dome</em> …")`, DisplayName `:6739`, flavor split out to `:6745`, still legacy-gated `:6737`. German row `841885693955 → "Mittlere unterirdische Kuppel"` — the translation was corrected too. `TechDef` is the `GlobalMap` of `TechPreset` (`Lua/ClassDefs/ClassDef-PresetDefs.generated.lua:1709-1729`), whose entry is the stub `Data/TechPreset.lua:512-515` (group + id only) → our `desc` is nil → declines (`:58-74`).
3. **CONFIRMED.**
4. **Replacement correct.** No residual.
5. **Player on REMOVE.** Nothing visible.
6. **Not opened.** The `Tech` class's own GlobalMap name (inferred `Techs` from `Workplace.lua:290`).

### R-33 · `TouristApplicants` (F08)

1. **Our claim.** `RewardApplicants` rolled `Random(0,100) > bonus_chance` (inverted); our copy uses `<` (`Code/Fix_TouristApplicants.lua:213`).
2. **1.1.0.** `Lua/HolidayRating.lua:92` `if Random(0, 99) < reward.bonus_chance then`; body `:87-106`.
3. **CONFIRMED.**
4. **Replacement correct** — the codebase idiom; ours (`Random(0,100)`, 101 outcomes) is chance/101, marginally low.
5. **Player on REMOVE.** Vanilla's exact roll.
6. **Not opened.** The `rewards` table values in 1.1.0.

### R-34 · `TrainMinors` (F49d)

1. **Our claim.** `max_vehicles` is computed once in `GameInit` and goes stale after a salvage split; we recompute at `UpdateEndElements`/`ExpandTrackFromElement` and on `PostLoadGame` (`Code/Fix_TrainMinors.lua:98-146`).
2. **1.1.0.** `Lua/Buildings/Track.lua:62-67` unchanged (one-shot). But the GATE moved: `TrackBase:CanAddVehicle` `:423-426` = `GetTrainsOnRoute(self)` → `trains < cap`, cap = distinct stations on the route when ≥ 2 (`Lua/TrainTransport.lua:492-537`, `:521-523`); `AssignTrain` `:433` uses it. Remaining `max_vehicles` readers: `StationsLink:GetMaxVehicles` `:28-30` → overview row `Track.lua:596` and `Lua/X/ColonyControlCenter.lua:1586`; `StationsLink:CanAddVehicle` `:32-34` is overridden by `TrackBase` and Track is the only `StationsLink` inheritor (`Track.lua:29`).
3. **CONFIRMED.**
4. **Replacement correct for the gate.** Residual: two displays still read the stale one-shot value while the section title `:605-608` uses the route cap, so after a salvage a track can show two different "max" numbers. Cosmetic.
5. **Player on REMOVE.** Cap unaffected; the overview/CCC number stops refreshing after a split. Today our module stays active (all Require targets present) and keeps that number fresh — harmless.
6. **Not opened.** `TrackElement.lua` salvage/split paths in 1.1.0.

### R-35 · `TrainPlatformWedge` (F11)

1. **Our claim.** `Colonist:ExitVehicle`'s abducted-passenger guard called `table.remove(vehicle.units, self)` (position API on a value) and raised; our pre-wrapper re-states the guard with `table.remove_entry` (`Code/Fix_TrainPlatformWedge.lua:279-288`).
2. **1.1.0.** `Lua/Units/ColonistTransport.lua:660-667`: same guard, `table.remove_entry(vehicle.units, self)` at `:664`, then `DiscardTransportTicket()`; byte-identical to our branch.
3. **CONFIRMED.**
4. **Replacement correct.** No residual.
5. **Player on REMOVE.** Identical.
6. **Not opened.** `Train:UnloadTrain` in 1.1.0.

### R-36 · `90_SaveSanitizer` (F35, F03, F48)

1. **Our claim.** Three one-shot repairs for residue of 1.0.7 defects: the `WindTurbine_Large_ReapplyModifiers` fixup re-buffed only the Diffuser label (F35); leaked upgrade modifiers from `ipairs` on a keyed table (F03); the station-connector fixup's misplaced paren (F48) (`Code/90_SaveSanitizer.lua:26-47`, `:100-116`, `:170-225`).
2. **1.1.0.** F48: `Lua/Buildings/Station.lua:1504` `ProcessTrackElements(ResolveMap(track), track.elements)` — paren fixed; fixups run once per name (`CommonLua/SavegameFixup.lua:24-38`) and a new game pre-marks every fixup applied (`:10-16`). F03: `Lua/Buildings/Building.lua:1303-1311` uses `pairs`; `SavegameFixups.RemoveLeakedUpgradeModifiers` `:1313-1345` is vanilla's own copy of our sweep (same id pattern, `:1337`). F35: `Lua/Buildings/WindTurbine.lua:95-105` STILL re-applies only `WindTurbine_Diffuser` (`:98`); the tech still carries three labels (`Data/Tech.lua` FrictionlessComposites block, `Effect_ModifyLabel` on `WindTurbine`, `WindTurbine_Large`, `WindTurbine_Diffuser`, Percent 100). Old saves: `Lua/Config/config.lua:174-175` `SupportedSavegameLuaRevision = 402200`, `OldSavegameBehavior = Platform.steam and "block" or "warn"`; `Lua/UI/SaveLoad.lua:76` stamps "Deprecated save file format!", `Lua/Savegame.lua:88` skips them. Our F35 pass reads `TechDef.FrictionlessComposites`, which on 1.1.0 is the `TechPreset` stub (`Data/TechPreset.lua:235`, see R-32 for the GlobalMap) → zero effects → always 0.
3. **PARTIAL.** §1b's reasoning holds (save block + stub). §1h's "F35 buff re-applied by a vanilla fixup (`WindTurbine.lua:95-105`)" is wrong: `:98` names only the Diffuser label; nothing in 1.1.0 re-applies `WindTurbine` or `WindTurbine_Large`. F35 is excluded, not repaired.
4. **F48 and F03 correct.** F35 has no vanilla repair; it is correct-by-exclusion and the exclusion is `Platform.steam`-conditional (`config.lua:175`): a non-Steam 1.1.0 build gets "warn" and LOADS a 1.0.7 save, carrying the F35 residue — and the F48 residue too, because the fixup name is already in `AppliedSavegameFixups`. `EF-079` records the Steam observation only. Our F48 pass makes the same call as the fixed vanilla line, so on Steam it is a one-shot no-op with a log line.
5. **Player on REMOVE.** Steam: nothing. Off Steam with a migrated 1.0.7 save: Large turbines stay unbuffed (F35), F03 is covered by `:1313`, F48 is not.
6. **Not opened.** `Lua/Tracks.lua` `OrderTrackElements` in 1.1.0 (report cites `:520`, `:615-622`); whether the pack is distributed outside Steam (owner question, not code).

### Summary table

| row | module | claim | replacement correct? | patch impact | evidence |
|---|---|---|---|---|---|
| R-21 | DustDevilSpawnGate | CONFIRMED | yes | remove; today burns a draw per tick (5 s in storms) | `DustDevils.lua:237`, `:256`, `:249-251` |
| R-22 | DustDevilsDescrMap | CONFIRMED | yes (our body) | remove | `DustDevils.lua:59`, `:64` |
| R-23 | DustStormUndergroundBreaks | CONFIRMED | yes, stricter than ours | remove | `SupplyGrid.lua:1106-1112`, `:1114`, `:1518` |
| R-24 | ExtractorStaffedPerformance | CONFIRMED | yes | remove; deletes the rubble wrong-case | `Workplace.lua:270-272`, `:285-287`; `Colonist.lua:794-796` |
| R-25 | LanderReturnFuel | PARTIAL (2nd value IS read by UI) | yes | remove; cosmetic return-fuel row goes | `UniversalRocket.lua:1894`, `:436`, `:441`, `:3428-3436`, `:3614-3623` |
| R-26 | LandscapeCostRefresh | CONFIRMED | yes | remove | `ConstructionSite.lua:721` |
| R-27 | LocalizedUIText | CONFIRMED; sub-reader flag resolved (translated) | yes | remove | `TerraformingOverall.generated.lua:57`; `GameShortcuts.generated.lua:1432`; German row 192345398558 |
| R-28 | MilestoneCrash | CONFIRMED | yes | remove | `Milestones.lua:116` |
| R-29 | MoraleComfortTooltip | CONFIRMED | rewrite, nothing to be wrong | remove | `Colonist.lua:3852-3855`, `:4862-4883`; `Stats.lua:814-925` |
| R-30 | SpaceYDroneCapBullet | CONFIRMED | yes ("40" is a literal) | remove; duplicate bullet goes | `MissionSponsorPreset.lua:631`, `:702-711`; German row 880574954148 |
| R-31 | StorageRateModifiers | CONFIRMED, citation corrected | electricity yes; water/air unreachable-not-fixed | remove; name SetBase residual | `ElectricityStorage.lua:55-56`; `LifeSupportStorage.lua:9-10`, `:32-33`; `Lua/Modifiers.lua:30-37`, `:47-49`, `:120-128` |
| R-32 | TechDescriptionBuilding | CONFIRMED | yes (German corrected too) | remove | `Data/Tech.lua:6738`; `TechPreset.lua:512-515`; `ClassDef-PresetDefs.generated.lua:1729` |
| R-33 | TouristApplicants | CONFIRMED | yes | remove | `HolidayRating.lua:92` |
| R-34 | TrainMinors | CONFIRMED | gate yes; two displays stale | remove; note cosmetic | `Track.lua:423-426`, `:596`; `TrainTransport.lua:521-523`; `ColonyControlCenter.lua:1586` |
| R-35 | TrainPlatformWedge | CONFIRMED | yes | remove | `ColonistTransport.lua:664` |
| R-36 | 90_SaveSanitizer | PARTIAL (F35 "re-applied by fixup" is false; exclusion is Steam-only) | F48/F03 yes; F35 excluded not fixed | remove on Steam; off-Steam residue returns | `WindTurbine.lua:98`; `Station.lua:1504`; `Building.lua:1313-1345`; `config.lua:174-175`; `SavegameFixup.lua:10-16` |

### What would make the patch half-baked

Ranked. None of the sixteen REMOVE verdicts ships something wrong for a Steam 1.1.0 player; the items below are wrong REASONS in the record and one platform-conditional gap.

1. **R-36 / F35 — the recorded reason is false.** §1h says the Large-turbine buff is "re-applied by a vanilla fixup (`WindTurbine.lua:95-105`)". `WindTurbine.lua:98` re-applies `WindTurbine_Diffuser` only; the tech's `WindTurbine` and `WindTurbine_Large` labels have no fixup anywhere in 1.1.0. The verdict survives only through the old-save block, and that block is `Platform.steam and "block" or "warn"` (`Lua/Config/config.lua:175`). If the pack is ever shipped to a non-Steam storefront, removing the sanitizer re-exposes F35 (and F48, whose fixup name is already marked applied) on migrated 1.0.7 saves. Fix the §1h cell; record the platform condition on `EF-079`.
2. **R-31 — the gate is cited from a shadowed file.** The "can never fire" claim rests on `CommonLua/Classes/Modifiers.lua:106-109`; the live gate is `Lua/Modifiers.lua:47-49` (`HasMember(base_prop)`) with `:30-37`. Same conclusion, but a future reader checking the cited line would find a path this game does not use. Also name `Modifiable:SetBase` (`:120-128`) as the one route that bypasses it.
3. **R-25 — "second return unreachable" is not true.** `UniversalRocket.lua:3428-3436` and `:3614-3623` read both values; with our wrapper the infopanel shows a spurious "Return trip fuel" row for a parked lander. It strengthens REMOVE; the row's wording should say so rather than claim unreachability.
4. **R-34 — patch-note item, not a defect.** After removal the overview/CCC "x/max" (`Track.lua:596`, `ColonyControlCenter.lua:1586`) can disagree with the section title's route cap (`:605-608`) on a salvaged track. Say "cosmetic" in the notes so a report of it is not re-filed.
5. **R-27 — an owed item that is not owed.** The sub-reader's "possibly NEW untranslated string" (`T(192345398558, "Back to Earth")`) is enrolled and translated in the 1.1.0 German pack. Close it.

Opened to know the rest are clean: every 1.1.0 target named in rows R-21…R-36 above, the sixteen `Code/` modules, `Lua/Modifiers.lua` + `Lua/LabelContainer.lua` (R-31 route), `CommonLua/SavegameFixup.lua` + `Lua/Config/config.lua` + `Lua/UI/SaveLoad.lua` (R-36 save policy), `Lua/ClassDefs/ClassDef-PresetDefs.generated.lua:1709-1729` (what `TechDef` holds), and `Local/German.fpk` → `Game.csv` for ids 192345398558, 914616772802, 407456913268, 316233855405, 807999655245, 885571832096, 880574954148, 841885693955.
