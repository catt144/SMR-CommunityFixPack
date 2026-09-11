# fixtoggles 04 — convert the wrapper and handler modules

Link 04 of `fixtoggles`. README binding rules 1–18 are yours. Runs only after a 03 **PASS** (or PASS WITH CORRECTIONS).
Staleness: `git log` + `git pull`; the spec (`reports/FIXTOGGLES_SPEC.md`, as corrected by 03) is the contract.

## The set (the research report's shape a/d rows; the spec §3 table is authoritative if it re-split them)

AnomalyCaveInMap · ArrivalDeaths · BrokenTrackSalvage · DestroyedTunnels · DroneTransportMinors · ExtenderFlapChurn ·
FounderTraitNotification · FreedHousingNotice · GeneForging · GhostFarmOxygen · GraphConsumedCaption ·
JumboCaveReinforcementWedge · LakeEntombment · LanderEmptyLaunch · LayoutTechLock · MirrorSphereSite · NightShiftWork ·
RocketInteractGuard · SequenceLatents · ShelterReflex · ShuttleHubOffAvailable · StaleReservations · TrainsToVoid ·
TrainWaitTime — **minus the one 02 already converted**.

## Job, per module

1. Open the module and the shipped body it wraps (1.1.0 tree). Confirm the spec row; if it is wrong, stop on that
   module, correct the spec row (strike-and-supersede) and note it for 99.
2. Put the gate in per the spec's helper: while the fix is off the call reaches the captured original untouched;
   inert for a foreign object first. `WhenActive` handlers already honour the registry — confirm, do not duplicate.
   LoadGame one-shots and sweeps: follow the spec §7 disposition (skip while off; never un-do a repair).
3. The `Colonist:Idle` pair (ArrivalDeaths, ShelterReflex): prove with the harness that either can be off while the
   other is on, in both load orders.
4. Header: the real switch semantics, both directions, and what stays in the save.
5. Extend `tools/desk_toggles.py` with the module (gate on/off; falsifier seen RED).

Batch 4–6 modules per commit; one todo item per commit. Self-split to `04b` at a clean boundary if the set will not
finish comfortably (README rule 4).

## Scope fence

IN: the listed module files, the harness. OUT: `00_Core.lua` (frozen after 02 — route a needed change through the
README and 99's inbox), link declarations (06b), text (08), any version work.

## Stop conditions

A module whose defect path cannot be gated without changing its unswitched behaviour · a spec row wrong in a way that
moves it to 06/06b · any gate that would need a restore (rule 7).

## What may NOT be claimed

"Converted" without the harness case GREEN and its falsifier RED. Anything in-game.

## Close-out

Green gates (rule 14), `Mars.exe` closed. Outbox to 06b (every module in a cluster 06b must link) and 99; strike your
row; `git rm` this file; push.

## Notes from upstream

- (links 01–03 append here)
