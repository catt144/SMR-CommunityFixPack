# Game patch 1.1.1.405907 — both-pack triage (2026-09-23)

Run from `docs/agent/prompts/perma/GAME_PATCH_PROMPT.md` against the archived
1.1.0.403908 and 1.1.1.405907 source trees, followed by the owner's unattended
retail A/B on 2026-09-23. The verdict table remains a source-audit result; the retail
legs add the explicitly bounded measurements in section 4.

**Adjudicated 2026-09-23 on a second seat** (`FULL_BODY_PRIORITY_2026-09-23.md`,
`GAMEPATCH_1.1.1_ADJUDICATION_2026-09-23.md`). Two rows in section 3 were corrected by
that adjudication and say so in place; the verdict totals below were re-measured after
the correction. Everything else in this report was confirmed or is marked unproven there.

## 0 · Work list

The prompt requires a todo tool before the first write. This session exposes no todo
tool, so this report carries the same nine-item live list.

- [x] 1. Archive the live tree and verify its manifest.
  tokens: ~2,000 (estimate)
- [x] 2. Run the patchcheck falsifier and sweep; run bodycheck as the defect-expression router.
  tokens: ~5,000 (estimate)
- [x] 3. Read D3 rows first; the instrument block contains no flagged D3 row.
  tokens: ~100 (estimate)
- [x] 4. Apply the full-verdict source-read method to every fix-pack module and read flagged seams.
  tokens: ~24,000 (estimate)
- [x] 5. Apply patch-note additions.
  tokens: ~200 (estimate)
- [x] 6. Write the owner launch line for the unattended in-game A/B pair and logscan.
  tokens: ~3,000 (estimate)
- [x] 7. File findings and write the combined FIX / REMOVE prompts.
  tokens: ~10,000 (estimate)
- [x] 8. Write and commit the opt-in outbox entry.
  tokens: ~1,500 (estimate)
- [x] 9. Review the limits from the actual reads and put the proposed pair on the checklist.
  tokens: ~1,000 (estimate)

## 1 · Patchcheck block — verbatim

```text
== patchcheck · 2026-09-23 · fix pack HEAD 2812098 ==
command: python tools/patchcheck.py --code Code --code B:\Dev\SMR\SMR-OptInPack\Code
old: 1.1.0.403908  B:\Dev\SMR\SMR-Shared\SMR-SrcArchive\1.1.0.403908\Src
new: 1.1.1.405907  A:\SteamLibrary\steamapps\common\Project Spark\ModTools\Src  [live install, Steam build 25390750]
A archived: live Src == 1.1.1.405907\MANIFEST.sha256 (digest d753f949af92e2b7…)
P holds — Lua.fpk 2374/2374 byte-identical, 0 divergent, 0 absent; Data.fpk 2192/2192 byte-identical, 0 divergent, 0 absent
index: old 33404 declarations, new 33547; identical 32948 · body 406 · body+sig 35 · removed 12 · moved 0 · moved+body 3; added 158
files (non-DLC): changed 311 · identical 4255 · added 2 · removed 0
T 315 changed hand declarations = body 286 + body+sig 14 + removed 12 + moved+body 3 (moved 0, added 140 excluded)
B 0 file(s) with a DefineClass/__parents line changed under a pinned/required/cited file
notes: fetched — 'Patch 1.1.1 - Patch Notes' (2026-09-23)

── code: Code — 52 modules ──
columns: PIN 17 · REQ 2 · CITE 34 · ANON 19 · SIGCALL 0 · D1 36 · M 43
modules with no resolvable pin (covered by REQ/CITE/ANON only): 7
D3 save-exposed sites in this Code/: 6; flagged 0
D2 0 call(s) in 0 module(s), ranked gone > incompatible > prefix-compatible
M — flagged modules (43):
  90_SaveSanitizer  [CITE ANON]
      CITE Effect_ModifyLabel.OnApplyEffect  body  Lua/MarsGameEffects.lua:257 -> Lua/MarsGameEffects.lua:257  (cited :277)
      ANON Lua/Modifiers.lua  file changed  (cited :228 is outside every keyed declaration)
  ArrivalDeaths  [ANON]
      ANON Lua/Units/Colonist.lua  file changed  (cited :92 is outside every keyed declaration)
      ANON Lua/Units/Unit.lua  file changed  (cited :945 is outside every keyed declaration)
  BombardmentSpread  [PIN CITE]
      PIN  WaitBombard  body  Lua/Bombardment.lua:55 -> Lua/Bombardment.lua:52
      CITE GenerateDir  body+sig (dir,angle)->()  Lua/Bombardment.lua:38 -> Lua/Bombardment.lua:38  (cited :38)
      CITE WaitBombard  body  Lua/Bombardment.lua:55 -> Lua/Bombardment.lua:52  (cited :55)
  BrokenTrackSalvage  [PIN CITE ANON]
      PIN  TrackGridElement.DemolishAndSplitTrack  body  Lua/Buildings/TrackElement.lua:467 -> Lua/Buildings/TrackElement.lua:467
      CITE TrackGridElement.DemolishAndSplitTrack  body  Lua/Buildings/TrackElement.lua:467 -> Lua/Buildings/TrackElement.lua:467  (cited :467)
      ANON Lua/Buildings/TrackElement.lua  file changed  (cited :164 is outside every keyed declaration)
  BuildingCodesPrefab  [CITE ANON]
      CITE Data/LawDef/LawDef-Efficiency.lua  file changed  (cited :696)
      CITE Data/LawDef/LawDef-Efficiency.lua  file changed  (cited :904)
      ANON Lua/Factions/Laws.lua  file changed  (cited :393 is outside every keyed declaration)
      ANON Lua/Factions/Legislature.lua  file changed  (cited :1 is outside every keyed declaration)
  CloggedBuildingRelease  [CITE]
      CITE Data/ClassDef-Effects.lua  file changed  (cited :4307)
      CITE Data/StoryBit/BuildingClogged.lua  file changed  (cited :4)
      CITE Data/StoryBit/BuildingClogged.lua  file changed  (cited :6)
      CITE Building.GetUIWarning  body  Lua/Buildings/Building.lua:2918 -> Lua/Buildings/Building.lua:2939  (cited :2930)
      CITE Lua/ClassDefs/ClassDef-Effects.generated.lua  file changed  (cited :2770)
  CrystalMysteryHang  [CITE]
      CITE Create@5c6200  body  Lua/Scenario/Mystery 10.generated.lua:9 -> Lua/Scenario/Mystery 10.generated.lua:9  (cited :232)
  DestroyedTunnels  [PIN CITE]
      PIN  TunnelBase.AddPFTunnel  body  Lua/Buildings/Tunnel.lua:193 -> Lua/Buildings/Tunnel.lua:193
      CITE TunnelBase.AddPFTunnel  body  Lua/Buildings/Tunnel.lua:193 -> Lua/Buildings/Tunnel.lua:193  (cited :193)
  DomeOverviewHighlight  [PIN CITE]
      PIN  Community.UICommandCenterStatUpdate  body  Lua/X/ColonyControlCenter.lua:1290 -> Lua/X/ColonyControlCenter.lua:1290
      CITE Community.UICommandCenterStatUpdate  body  Lua/X/ColonyControlCenter.lua:1290 -> Lua/X/ColonyControlCenter.lua:1290  (cited :1290)
  DroneTransportMinors  [CITE ANON]
      CITE Drone.PickUp  body  Lua/Units/Drone.lua:1116 -> Lua/Units/Drone.lua:1124  (cited :1209)
      ANON Lua/Buildings/DroneControl.lua  file changed  (cited :12 is outside every keyed declaration)
      ANON Lua/Units/Drone.lua  file changed  (cited :73 is outside every keyed declaration)
  DryFarmingFarms  [REQ CITE ANON]
      REQ  Effect_ModifyLabel.OnApplyEffect  body  Lua/MarsGameEffects.lua:257 -> Lua/MarsGameEffects.lua:257
      CITE Data/Tech.lua  file changed  (cited :769)
      CITE FarmBase.PlantNextCrop  body  Lua/Buildings/Farm.lua:574 -> Lua/Buildings/Farm.lua:583  (cited :619)
      CITE Effect_ModifyLabel.OnApplyEffect  body  Lua/MarsGameEffects.lua:257 -> Lua/MarsGameEffects.lua:257  (cited :257)
      ANON Lua/Buildings/Building.lua  file changed  (cited :2556 is outside every keyed declaration)
      ANON Lua/Modifiers.lua  file changed  (cited :228 is outside every keyed declaration)
  DustSicknessBiorobots  [ANON]
      ANON Lua/_fixup.lua  file changed  (cited :148 is outside every keyed declaration)
  ExoticDepositSign  [ANON]
      ANON Lua/Buildings/SubsurfaceDeposit.lua  file changed  (cited :496 is outside every keyed declaration)
  FactionDomeSizeGate  [CITE]
      CITE Data/FactionDef/JusticeMovement.lua  file changed  (cited :104)
      CITE Data/FactionDef/JusticeMovement.lua  file changed  (cited :123)
      CITE Data/FactionDef/JusticeMovement.lua  file changed  (cited :129)
      CITE Data/FactionDef/MarsDemocraticParty.lua  file changed  (cited :84)
      CITE Data/FactionDef/MarsDemocraticParty.lua  file changed  (cited :88)
      CITE Data/FactionDef/MarsDemocraticParty.lua  file changed  (cited :102)
      CITE Data/FactionDef/MarsDemocraticParty.lua  file changed  (cited :103)
      CITE Data/FactionDef/NewSol.lua  file changed  (cited :43)
      CITE … 8 more (--rows N)
  FounderTraitNotification  [CITE]
      CITE OnMsg.ColonistAddTrait  moved+body (colonist,trait_id,init)->(colonist,trait_id)  Lua/ColonyViability.lua:306 -> Lua/Factions/Factions.lua:1466  (cited :306)
  FreedHousingNotice  [CITE]
      CITE Data/TraitPreset.lua  file changed  (cited :772)
  GeneForging  [PIN CITE]
      PIN  GetRareTraitChance  body  Lua/Units/Colonist.lua:4398 -> Lua/Units/Colonist.lua:4719
      CITE GetRareTraitChance  body  Lua/Units/Colonist.lua:4398 -> Lua/Units/Colonist.lua:4719  (cited :4398)
  GraphConsumedCaption  [PIN CITE]
      PIN  City.GetColonyStatsButtons  body  Lua/X/ColonyControlCenter.lua:8 -> Lua/X/ColonyControlCenter.lua:8
      CITE City.GetColonyStatsButtons  body  Lua/X/ColonyControlCenter.lua:8 -> Lua/X/ColonyControlCenter.lua:8  (cited :8)
  HabitatExpeditionDraft  [PIN]
      PIN  CargoTransporterNew.GatherAvailableColonists  body  Lua/CargoTransporterNew.lua:235 -> Lua/CargoTransporterNew.lua:235
  HabitatExpeditionReturn  [PIN]
      PIN  Colonist.UpdateWorkplace  body  Lua/Units/Colonist.lua:1794 -> Lua/Units/Colonist.lua:1797
  LakeEntombment  [CITE]
      CITE Drone.Deliver  body+sig (d_request,do_not_improve_req)->(d_request,do_not_improve_req,assign_request)  Lua/Units/Drone.lua:1366 -> Lua/Units/Drone.lua:1379  (cited :1478)
  LandscapeUnitFilter  [ANON]
      ANON Lua/Landscape/LandscapeConstructionSite.lua  file changed  (cited :3 is outside every keyed declaration)
  MirrorSphereSite  [PIN CITE ANON]
      PIN  MirrorSphereBuildingBase.StartAction  body  Lua/Mysteries/MirrorSphere.lua:826 -> Lua/Mysteries/MirrorSphere.lua:828
      CITE MirrorSphereBuildingBase.IsActionEnabled  body  Lua/Mysteries/MirrorSphere.lua:786 -> Lua/Mysteries/MirrorSphere.lua:786  (cited :813)
      CITE MirrorSphereBuildingBase.StartAction  body  Lua/Mysteries/MirrorSphere.lua:826 -> Lua/Mysteries/MirrorSphere.lua:828  (cited :826)
      ANON Lua/Mysteries/MirrorSphere.lua  file changed  (cited :16 is outside every keyed declaration)
  NightShiftWork  [PIN CITE]
      PIN  Colonist.ShouldLeaveForWork  body  Lua/Units/Colonist.lua:2194 -> Lua/Units/Colonist.lua:2396
      CITE Colonist.ShouldLeaveForWork  body  Lua/Units/Colonist.lua:2194 -> Lua/Units/Colonist.lua:2396  (cited :2194)
  PayloadTemplateRefill  [CITE]
      CITE Data/FlightPolicyDef.lua  file changed  (cited :93)
  RocketDroneChurn  [ANON]
      ANON Lua/Buildings/DroneControl.lua  file changed  (cited :720 is outside every keyed declaration)
  RocketInteractGuard  [PIN CITE]
      PIN  RCTransport.CanInteractWithObject  body  Lua/Units/RCTransport.lua:409 -> Lua/Units/RCTransport.lua:415
      PIN  RCTransport.InteractWithObject  body  Lua/Units/RCTransport.lua:458 -> Lua/Units/RCTransport.lua:464
      CITE RCTransport.CanInteractWithObject  body  Lua/Units/RCTransport.lua:409 -> Lua/Units/RCTransport.lua:415  (cited :409)
  SaintBlessing  [CITE]
      CITE Data/TraitPreset.lua  file changed  (cited :405)
      CITE Lua/ClassDefs/ClassDef-PresetDefs.generated.lua  file changed  (cited :1774)
  SequenceLatents  [CITE]
      CITE Data/Scenario/Mystery 2.lua  file changed  (cited :235)
  ShelterReflex  [ANON]
      ANON Lua/Units/Colonist.lua  file changed  (cited :94 is outside every keyed declaration)
  ShuttleHubOffAvailable  [CITE]
      CITE RequiresMaintenance.BuildingUpdate  body  Lua/RequiresMaintenance.lua:101 -> Lua/RequiresMaintenance.lua:101  (cited :129)
  ShuttleTransportCache  [CITE]
      CITE Colonist.VisitService  body  Lua/Units/Colonist.lua:2431 -> Lua/Units/Colonist.lua:2630  (cited :2504)
  SinkholeIndestructible  [CITE ANON]
      CITE Lua/BuildingTemplate/Sinkhole.generated.lua  file changed  (cited :1)
      CITE Lua/BuildingTemplate/Sinkhole.generated.lua  file changed  (cited :4)
      ANON Lua/Buildings/Building.lua  file changed  (cited :209 is outside every keyed declaration)
  StaleReservations  [ANON]
      ANON Lua/_GameConst.lua  file changed  (cited :144 is outside every keyed declaration)
      ANON Lua/__const.lua  file changed  (cited :171 is outside every keyed declaration)
  TrackSalvageRefund  [CITE ANON]
      CITE TrackGridElement.DemolishAndSplitTrack  body  Lua/Buildings/TrackElement.lua:467 -> Lua/Buildings/TrackElement.lua:467  (cited :503)
      CITE ConstructionController.UpdateConstructionStatuses  body  Lua/Construction/Construction.lua:2576 -> Lua/Construction/Construction.lua:2576  (cited :2911)
      ANON Lua/Buildings/ConstructionSite.lua  file changed  (cited :2479 is outside every keyed declaration)
      ANON Lua/Buildings/TrackElement.lua  file changed  (cited :124 is outside every keyed declaration)
  TrackSalvageWipe  [PIN CITE]
      PIN  TrackGridElement.DemolishAndSplitTrack  body  Lua/Buildings/TrackElement.lua:467 -> Lua/Buildings/TrackElement.lua:467
      CITE TrackGridElement.DemolishAndSplitTrack  body  Lua/Buildings/TrackElement.lua:467 -> Lua/Buildings/TrackElement.lua:467  (cited :467)
  TradeRocketFuelRefresh  [PIN CITE]
      PIN  UniversalRocketBase.OnModifiableValueChanged  body  Lua/UniversalRocket.lua:1916 -> Lua/UniversalRocket.lua:1922
      CITE Data/FlightPolicyDef.lua  file changed  (cited :561)
      CITE UniversalRocketBase.OnModifiableValueChanged  body  Lua/UniversalRocket.lua:1916 -> Lua/UniversalRocket.lua:1922  (cited :1916)
  TrainCargoDumping  [PIN CITE ANON]
      PIN  Train.UnloadAll  body  Lua/Units/Train.lua:779 -> Lua/Units/Train.lua:787
      CITE MultiResourceDepotBase.SetAcceptResource  body  Lua/Buildings/MultiResourceDepot.lua:251 -> Lua/Buildings/MultiResourceDepot.lua:251  (cited :251)
      CITE Train.UnloadAll  body  Lua/Units/Train.lua:779 -> Lua/Units/Train.lua:787  (cited :779)
      ANON Lua/Buildings/MultiResourceDepot.lua  file changed  (cited :247 is outside every keyed declaration)
      ANON Lua/Units/Train.lua  file changed  (cited :85 is outside every keyed declaration)
  TrainWaitTime  [PIN REQ CITE ANON]
      PIN  Colonist.BoardVehicle  body  Lua/Units/ColonistTransport.lua:614 -> Lua/Units/ColonistTransport.lua:615
      REQ  Colonist.ExitVehicle  body  Lua/Units/ColonistTransport.lua:660 -> Lua/Units/ColonistTransport.lua:662
      CITE Colonist.BoardVehicle  body  Lua/Units/ColonistTransport.lua:614 -> Lua/Units/ColonistTransport.lua:615  (cited :614)
      ANON Lua/Buildings/Station.lua  file changed  (cited :84 is outside every keyed declaration)
  TrainsToVoid  [CITE]
      CITE OnMsg.BuildingDemolished  body  Lua/Buildings/Station.lua:289 -> Lua/Buildings/Station.lua:289  (cited :289)
  VacuumWalks  [PIN CITE]
      PIN  Colonist.TryToEmigrateToDome  body  Lua/Units/Colonist.lua:1886 -> Lua/Units/Colonist.lua:1894
      CITE Colonist.TryToEmigrateToDome  body  Lua/Units/Colonist.lua:1886 -> Lua/Units/Colonist.lua:1894  (cited :1886)
  WildfireCureVisit  [CITE ANON]
      CITE Data/Scenario/Mystery 8.lua  file changed  (cited :204)
      CITE Data/TraitPreset.lua  file changed  (cited :116)
      CITE Data/TraitPreset.lua  file changed  (cited :144)
      CITE Colonist.VisitService  body  Lua/Units/Colonist.lua:2431 -> Lua/Units/Colonist.lua:2630  (cited :2482)
      ANON Lua/Units/Colonist.lua  file changed  (cited :164 is outside every keyed declaration)
  WispRewards  [PIN CITE ANON]
      PIN  SetLightTrapMode  body  Lua/Mysteries/Fireflies.lua:677 -> Lua/Mysteries/Fireflies.lua:712
      CITE Firefly.DetachFromWaterSource  body  Lua/Mysteries/Fireflies.lua:325 -> Lua/Mysteries/Fireflies.lua:358  (cited :346)
      CITE SetLightTrapMode  body  Lua/Mysteries/Fireflies.lua:677 -> Lua/Mysteries/Fireflies.lua:712  (cited :677)
      ANON Lua/Mysteries/Fireflies.lua  file changed  (cited :674 is outside every keyed declaration)
no row (9): ExtenderFlapChurn, JumboCaveReinforcementWedge, LanderEmptyLaunch, OpenPastureStockpiles, RoverSubclassManifest, ScanDowngrade, SilentHitMomentFX, TrackConnectorPingPong, TrackTunnelPowerBridge
notes: 0 module(s) matched, 0 added to the read list

── code: B:\Dev\SMR\SMR-OptInPack\Code — 4 modules ──
columns: PIN 0 · REQ 0 · CITE 2 · ANON 2 · SIGCALL 0 · D1 2 · M 3
modules with no resolvable pin (covered by REQ/CITE/ANON only): 1
D3 save-exposed sites in this Code/: 3; flagged 0
D2 0 call(s) in 0 module(s), ranked gone > incompatible > prefix-compatible
M — flagged modules (3):
  AcknowledgedWarnings  [ANON]
      ANON Lua/RequiresMaintenance.lua  file changed  (cited :234 is outside every keyed declaration)
  DroneStatDials  [CITE ANON]
      CITE Colony.CityStart  body  Lua/Colony.lua:41 -> Lua/Colony.lua:41  (cited :102)
      ANON Lua/MarsGameEffects.lua  file changed  (cited :161 is outside every keyed declaration)
  MultipleSuns  [CITE]
      CITE UIGetBuildingPrerequisites  body  Lua/X/BuildMenu.lua:704 -> Lua/X/BuildMenu.lua:705  (cited :711)
no row (1): ResidencyControl
notes: 0 module(s) matched, 0 added to the read list

D5 facts: 117 files, 72 with a resolvable game-function citation, 11 cite a function that changed
  EF-055   OpenPreGameMainMenu
  EF-061   SetAtmosphereBreathable
  EF-063   customUniversalRocket.Init
  EF-065   OpenPreGameMainMenu
  EF-074   Drone.PickUp
  EF-083   UIGetBuildingPrerequisites
  EF-091   CargoTransporterNew.DroneUnloadResource, Drone.Deliver
  EF-099   PlacePipeLine
  EF-104   CargoTransporterNew.GatherAvailableColonists
  EF-107   Workforce.HasFreeWorkplacesAroundForSpecialist
  EF-115   Drone.CanBeControlled

summary Code: modules 52 · M 43 · notes-added 0 · D3 0
summary B:\Dev\SMR\SMR-OptInPack\Code: modules 4 · M 3 · notes-added 0 · D3 0
verdict: FULL — |M| = 43 > 12  (limits 12 modules / 1000 declarations are budget defaults; the small-patch regime is uncalibrated until the first real patch)
```

## 1a · Archive

The live 1.1.1.405907 `ModTools/Src` tree was copied to
`B:\Dev\SMR\SMR-Shared\SMR-SrcArchive\1.1.1.405907\Src`. The archive manifest and
the independently rehashed live tree matched digest
`d753f949af92e2b753f44163a2e47229e371f810ef3c2752d30a98953af2663c`; Steam build
`25390750` was re-read from the appmanifest. The exact archive paths and README row
were committed in the shared archive as `75eeb0a`; unrelated `SMR-HubBackups/` content
was left untouched.

## 2 · Bodycheck routing

`python tools/bodycheck.py --selftest` initially exposed a stale positive fixture:
1.1.1 repaired the `Train:UnloadAll` expression that the fixture expected to remain.
The positive control was made patch-stable without changing the checker, and the
self-test then passed. Bodycheck candidates are read against both archived bodies
before any verdict; `DEFECT-GONE` is never itself a REMOVE verdict.

## 3 · Full-sweep verdicts

Every module was read against archived 1.1.0.403908 and 1.1.1.405907. A patchcheck
row routed the read but never supplied the disposition; modules with no row received
the same two-tree source read. `treediff.py` and `presetdiff.py` were self-tested, then
used only on the flagged systems. No D3 call contract was flagged. Patch notes added no
module.

| module | verdict | decisive 1.1.1 result |
|---|---|---|
| `90_SaveSanitizer` | KEEP | Its three legacy/save repairs remain valid; modifier display changes do not alter their structural matches. |
| `Fix_ArrivalDeaths` | KEEP | Arrival, safe-dome, and expedition-return defects remain; changed colonist code is elsewhere. |
| `Fix_BombardmentSpread` | KEEP | Vanilla still launches one shared direction for the volley; the per-missile spread remains absent. |
| `Fix_BrokenTrackSalvage` | REMOVE | Native split logic now excludes repair sites from the physical sort and rehomes them through the broken element. Adjudicated 2026-09-23: that body runs in a shipping pack only after F124 rebases `Fix_TrackSalvageWipe`, so this row is one unit with F124 and is owned by the FIX brief. |
| `Fix_BuildingCodesPrefab` | REMOVE | Both Building Codes handlers removed the prefab exit and apply their modifiers to prefab completions. |
| `Fix_CloggedBuildingRelease` | FIX | Native Duration prevents new losses, but our stand-down abandons already-stranded 1.1.0 saves (F121). |
| `Fix_CrystalMysteryHang` | KEEP | Fresh play is fixed, but a restored old thread can still be waiting on the former message; retain legacy rescue. |
| `Fix_DestroyedTunnels` | REMOVE | `TunnelBase:AddPFTunnel` now rejects either destroyed half. |
| `Fix_DomeOverviewHighlight` | REMOVE | Native fixes the label and guards empty domes; our old full replacement regresses that guard (F122). |
| `Fix_DroneTransportMinors` | KEEP | The stale non-Fuel restrictor-key path is unchanged. |
| `Fix_DryFarmingFarms` | KEEP | Vanilla added only `FarmSmall`; the other three Feeding the Future farms remain omitted. |
| `Fix_DustSicknessBiorobots` | KEEP | Both StoryBit filters still exclude Child but not Android. |
| `Fix_ExoticDepositSign` | KEEP | The class still names the suspect precious-minerals sign; the changed extraction body is unrelated. |
| `Fix_ExtenderFlapChurn` | KEEP | The unchanged work-state handler still triggers a full disconnect/reconnect rebuild. |
| `Fix_FactionDomeSizeGate` | KEEP | All seven target percentage evaluations remain unguarded; patch data changes are elsewhere. |
| `Fix_FounderTraitNotification` | REMOVE | Corrected 2026-09-23 (was KEEP). 1.1.1 deleted the dead handler and the `FounderGainsTrait` notification preset itself (`Data/NotificationPreset.lua`, 0 hits in the 1.1.1 tree against 2 files in 1.1.0), so the vendor removed the feature; our additive handler now adds a notification under an id with no preset, which `AddNotification` builds from the base class (F126). |
| `Fix_FreedHousingNotice` | KEEP | Residence release still does not promptly recheck homelessness; relevant bodies remain compatible. |
| `Fix_GeneForging` | REMOVE | Native now adds Gene Forging; our delegating wrapper adds it a second time (F123). |
| `Fix_GraphConsumedCaption` | REMOVE | Native caption now sums consumption and maintenance, matching the plotted series. |
| `Fix_HabitatExpeditionDraft` | KEEP | New child filtering does not exclude habitat residents from expedition draft buckets. |
| `Fix_HabitatExpeditionReturn` | KEEP | The held far-habitat return omission remains; new migration code does not enter that selector path. |
| `Fix_JumboCaveReinforcementWedge` | KEEP | The random unreachable-rock wedge remains; the added cave fixup only marks flight visibility. |
| `Fix_LakeEntombment` | KEEP | Lake placement/scatter ordering and the RC Constructor exemption are unchanged. |
| `Fix_LanderEmptyLaunch` | KEEP | An empty automatic request remains vacuously ready. |
| `Fix_LandscapeUnitFilter` | KEEP | `LandscapeForEachUnit` still constructs a filter but passes the raw callback. |
| `Fix_MirrorSphereSite` | REMOVE | `IsActionEnabled` now rejects real `max_progress` while same-action cancellation remains available. |
| `Fix_NightShiftWork` | REMOVE | `ShouldLeaveForWork` now uses a modular-day window that covers midnight. |
| `Fix_OpenPastureStockpiles` | REMOVE | Native adds a comprehensive pool rebuild and old-save fixup; the retail on-leg cleared the live asset gate when the module declined because the entity mismatch is gone. |
| `Fix_PayloadTemplateRefill` | KEEP | The zero-row template fallback remains unchanged. |
| `Fix_RocketDroneChurn` | KEEP | Cargo refresh still disconnects/reconnects the rocket unconditionally. |
| `Fix_RocketInteractGuard` | KEEP | The Universal trade/refugee class omission remains; target changes concern Elevator validity. |
| `Fix_RoverSubclassManifest` | KEEP | Exact leaf-class sourcing/counting remains in every named receiver. |
| `Fix_SaintBlessing` | KEEP | The modifier-label mismatch remains; changed trait data is unrelated. |
| `Fix_ScanDowngrade` | KEEP | The downgrade path and module seam remain unchanged. |
| `Fix_SequenceLatents` | KEEP | The repaired sequence-latent defects remain live; Mystery data changes do not replace them. |
| `Fix_ShelterReflex` | KEEP | `Colonist:Idle` still has no outside-oxygen shelter branch. |
| `Fix_ShuttleHubOffAvailable` | KEEP | Availability still admits switched-off hubs without checking `ui_working`. |
| `Fix_ShuttleTransportCache` | KEEP | The cache still ignores `shuttles_available`. |
| `Fix_SilentHitMomentFX` | KEEP | Target bodies are unchanged and the named animation metadata remains absent from decoded data. |
| `Fix_SinkholeIndestructible` | REMOVE | Both native Sinkhole definitions now set `indestructible = true`. |
| `Fix_StaleReservations` | KEEP | Residence reservations still have no general timeout at the named methods. |
| `Fix_TrackConnectorPingPong` | KEEP | Connector creation retains the ownership-steal/rebuild loop. |
| `Fix_TrackSalvageRefund` | KEEP | Whole and partial salvage refund omissions remain; its outcome wrapper composes with the new split body. |
| `Fix_TrackSalvageWipe` | FIX | F44 remains, but the old full replacement erases new repair-site split/rehome semantics (F124). |
| `Fix_TrackTunnelPowerBridge` | KEEP | The two-element connection path still skips `ConnectToGrids()`. |
| `Fix_TradeRocketFuelRefresh` | REMOVE | Native refreshes landed rockets and adds `ZZZ_UpdateRefuelRequests` for upgrading landed non-player rockets. |
| `Fix_TrainCargoDumping` | REMOVE | Rewritten unload logic checks resource enablement and preserves assigned cargo. |
| `Fix_TrainsToVoid` | REMOVE | Station demolition now calls the same `DestroySilent` storage path. |
| `Fix_TrainWaitTime` | REMOVE | Boarding now resets `transport_ticket.start_wait` directly. |
| `Fix_VacuumWalks` | FIX | F52 remains in two sites, while the old replacement erases the new multi-leg state machine (F125). |
| `Fix_WildfireCureVisit` | KEEP | Cure, at-home Health payment, and random interest choice remain; visit changes are unrelated. |
| `Fix_WispRewards` | REMOVE | Native removes the duplicate batch research grant and scales free-mode power by 1,000. |

Measured verdict totals from the table: **33 KEEP + 3 FIX + 16 REMOVE = 52**
(re-measured 2026-09-23 after the `Fix_FounderTraitNotification` correction; the
original read was 34 / 3 / 15). Command and filter:
`(rg '^\| .* \| KEEP \|' $p | Measure-Object).Count`, repeated for FIX
and REMOVE; their sum reconciles to the patchcheck module total. The Open Pasture
REMOVE is conditional on the live entity-spot control; it is named rather than
silently moved to another count.

The source reads filed five patch-induced pack defects: F121 through F125. F122 and
F123 are removed with their obsolete modules; F121, F124, and F125 require code repair.
The adjudication filed a sixth, F126, from the corrected `Fix_FounderTraitNotification`
row.
All five were source-read at filing. The retail on-leg additionally measured F123's
pack-on arithmetic as 100 against its own live parameter 50; that probe's pack-off
branch short-circuited at “fix pack not loaded,” so the removal brief still owns the
focused post-deletion A/B.

## 4 · In-game A/B

Both unattended legs completed `SMRTest.RunAll()`, printed `[SMRAUTO] END` and
`[SMRAUTO] done`, and quit. No `Mars`/`MarsDebug` process remained before either log
was read.

| leg | finished log | loaded mod items | TestKit result |
|---|---|---|---|
| Fix Pack off | `Mars.exe-20260923-10.37.07-6aad2d75.log` | TestKit only | 31 PASS, 36 FAIL, 26 SKIP, 5 ERROR |
| Fix Pack on | `Mars.exe-20260923-10.39.06-6aad2d75.log` | TestKit, Fix Pack, Opt-In Pack, Train Hub dev | 61 PASS, 11 FAIL, 23 SKIP, 3 ERROR |

The totals were read with `Get-Content <log> | Where-Object { $_ -match
'^\[SMRTest\] ---- \d+ PASS' }`. Each leg totals 98 probes, and each plain summary
agrees with the immediately preceding `[mod]` copy in the same log. The extra Opt-In
and Train Hub mods on the on-leg mean this is not a single-variable A/B. The two
completed legs are still valid observations of their named configurations, but they do
not support a blanket pack-only comparison.

`python tools/logscan.py <log>` reported 6 error-shaped lines off and 46 on. The off
count is the three current-build retired probes (`LanderCargoRatchet`,
`DroneUnreachableForever`, `AutoExportPriority`), each printed twice; the suite's two
additional rawget errors are real `ERROR` results but do not match logscan's
error-shaped filter. The on count reconciles by name and age as follows, all from the
2026-09-23 current-build leg: 36 lines are twelve synthetic Opt-In object-destruction
throws, each present as the engine error plus two SMRTK copies; 6 are the same three
retired-probe failures printed twice; 2 are the deliberately caught old-call exception
quoted in the passing `ArrivalDeathsChooseDomeArg` result; 1 is the Fix Pack's caught
`TradeRocketFuelRefresh` behaviour-probe decline; and 1 is an uncaught
`ArtSpecEditor.lua:573` boot error. The member counts sum to logscan's 46-line total.
Neither leg meets ck208's zero-error acceptance condition, so no clean-boot or retail
compatibility claim is made.

The on-leg did settle the remaining audit gate. Its boot census saw 52 Fix Pack modules,
46 applied and 6 inactive (46 + 6 = 52), and `OpenPastureStockpiles` declined at log
line 135 because “the Outside Ranch entity variants no longer have the nine-versus-six
stockpile mismatch.” That live result clears the module for the REMOVE brief. The same
leg also reproduced F123 (`GeneForging` 100, expected 50) and exposed the expected
active/removal and stale-probe work; it is evidence for the follow-up prompts, not a
release pass.

## 5 · Prompts, filings and opt-in outbox

- FIX brief: `docs/agent/prompts/GAMEPATCH_1_1_1_FIX_fanout_level_3.md` for F121,
  F124, and F125.
- REMOVE brief: `docs/agent/prompts/GAMEPATCH_1_1_1_REMOVE_medium.md` for the fifteen
  native replacements, with the cleared Open Pasture evidence and the still-open
  trade-rocket migration gate explicit.
- Findings filed: `docs/agent/bugs/F121.md` through `F125.md`.
- F123's evidence now includes the bounded pack-on retail measurement; its focused
  pack-off/post-removal control remains in the REMOVE brief.
- Opt-in outbox: `docs/agent/prompts/perma/gamepatch/1.1.1.405907_2026-09-23.md`
  in the opt-in fork, committed as `d372c1f`. Its patchcheck section was compared
  line-for-line with the captured block, and the fork's doccheck was GREEN.

## 6 · Limits review

Patchcheck routed FULL at M=43, T=315, B=0, and D3=0. The complete source read found
34 KEEP, 3 FIX, and 15 REMOVE; this is the first real post-1.1.0 calibration. Those
verdict counts are measured and reconciled by the command/filter recorded in section 3.

The 12-module limit sized this patch correctly: it forced a full sweep, which was
necessary because action rows included modules with no patchcheck row. T did not reach
1,000, so this patch does not independently calibrate that limit. Proposed pair for the
owner in checklist ck207: retain 12 modules / 1,000 declarations, provisionally.

The recommended deep-sweep decision is to stop at the completed all-module and
flagged-system seam read, finish the named repairs/removals, and clear their focused
verification before any broader tree-wide investigation. A broader sweep is estimated at 2–3 focused agent
sessions plus another owner A/B; that cost is an estimate, not a measured duration.

## 7 · Named limits

A source read is not `tested`. The patchcheck `none` claim would certify only the
one-hop named neighbourhood; this run is `full`. The small-patch regime is
now measured once but remains provisional until the owner rules on checklist ck207.

## 8 · Verification at handoff

- `python tools/patchcheck_selftest.py`: GREEN; every synthetic/backtest leg passed.
- `python tools/bodycheck.py --selftest`: PASS after replacing the stale F46 gameplay
  expression with a patch-stable declaration positive control; checker logic was not
  weakened. Current fix-pack bodycheck returned the expected routing REDs, all read in
  section 3; opt-in bodycheck returned only its expected no-manifest routing rows.
- `python tools/doccheck.py --regen`: generated bug index changes reviewed; no unrelated
  source entry or fact was dirty before regeneration. Final `python tools/doccheck.py`:
  GREEN.
- The patchcheck block in section 1 compares line-for-line with the captured scratch
  output after newline normalization. The verdict-table filter remeasured 34 KEEP,
  3 FIX, and 15 REMOVE and reconciled them to the patchcheck module total.
- Shared archive commit: `75eeb0a`. Opt-in outbox commit: `d372c1f`.
- The owner A/B completed and checklist ck208 was removed in the commit recording its
  result. Both autoruns reached `[SMRAUTO] done`, but neither met the zero-error gate;
  section 4 records the exact failures and the mismatched on-leg mod set. No clean-boot,
  release-readiness, or general in-game compatibility claim is made.
