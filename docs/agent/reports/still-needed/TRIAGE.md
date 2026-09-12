# Disagreements — primary-artifact checks by coordinator

Coordinator `/root`, 2026-09-12. This is not another agent vote or a rerun of an
inherited fixture. It checks the actual 1.1.0.403908 bodies behind disagreements.
No loadable code or public surface has been changed. Final synthesis will distinguish
source contradictions, inferred wording risks and unverified residual benefit.

## SN-01 — F54 dust-storm example contradicts the actual predicate (SOURCE)

Primary tree `C:/Dev/SMR-SrcArchive/1.1.0.403908/Src`:
`Lua/Buildings/ShuttleHub.lua:413` requires either working or a permission-only
failure with NO work-not-possible reason. `Lua/Buildings/BaseBuilding.lua:635`
onward returns a suspension as work-not-possible; `:657` returns TurnedOff when
`ui_working` is false. The wrapper adds `ui_working` to the permission-only arm
(`Code/Fix_ShuttleHubOffAvailable.lua:85` onward); it leaves vanilla false alone.
It does not keep a dust-storm-suspended hub available. `fix-list.md:102` must not
use dust storms as an example of retained availability. Keep the live off-hub
repair; remove that example or use a source-supported permission-only condition.

## SN-02 — Saint bonus is dome/trait-scoped, not colony-wide (SOURCE)

Primary `Lua/TraitPreset.lua:78` reads unit.dome, `:86` resolves the trait label,
`:88` writes a modifier to that dome. `Data/TraitPreset.lua:396` explicitly says
Religious people in the Dome, and `:405` targets Religious. `fix-list.md:148`
calls it colony-wide. Narrow that phrase. The module's existing healing/legacy
disposition remains; the direct registry read resolved the transient inactive
log-count disagreement (see `RUNTIME.md`). No damaged Saint save was sampled.

## SN-03 — F58's ordinary foot-residual story misses a cleanup route (SOURCE)

Primary `Lua/Units/Colonist.lua:3546` calls SetDome at the start of TransportByFoot;
SetDome's `:449` calls UpdateResidence; `:2921` onward uses reserved_residence;
`Lua/Buildings/Residence.lua:110` calls CancelResidenceReservation when adopting
the resident. An omission in the foot destructor does not prove a continuing
ordinary foot reservation. The module instead cancels invalid, mismatched,
dying or aged holders, with a legitimate expedition exemption. Its age check is
not a test that a journey can no longer complete. Narrow `fix-list.md:112`
onward and reassess its half-empty-dome headline without claiming an organic
committed-shuttle limbo has been reproduced. A valid reservation consumer still
exists; this check does not establish a vanilla replacement for all its repairs.

## SN-04 — F52's card headline can read more broadly than its row (INFERRED)

The site row at `fix-list.md:46` states the built-passage case. The metadata
headline and intro omit that condition. Primary `Lua/Units/Colonist.lua:1914`
retains surface walking when no passage path exists; `:1927` passes a found path
to TransportByFoot. Suggest naming the available passage in the headline/intro.
This is a wording-risk recommendation, not a source-proven new player defect.

## SN-05 — F51 has a remaining current consumer, with an unrun geography case

The prior migration review's broader permanent-block story remains withdrawn.
Primary `Lua/Buildings/Dome.lua:315` onward reads current shuttle availability
inside the passage-walk predicate. A cached shuttle tuple can require walk
recomputation after availability falls. Whether a real directly passage-connected
pair meets the long outside-path precondition remains INFERRED; a far passage
chain is not automatically a valid recipe. The narrowed stale-value row remains
true. Preserve the report's separate fixed-false-query cache residual by name.

Paths `fix-list.md` above are in `C:/Dev/SMR-CommunityMods/content/`.

## SN-06 — F37 ordinary oxygen leak has a vanilla replacement (SOURCE)

Coordinator read primary Farm working updates at `Lua/Buildings/Farm.lua:165`,
:630 and :648, keyed clearing :641 and dome notification :643. Building destruction
sets destroyed :1560 then UpdateWorking(false) :1570 before Done's SetDome(false)
:537. Dome air demand still reads the value :1881; the repair is redundant because
cleanup happens earlier, not because oxygen lost its reader. Refab dying-worker
timing, direct custom Done/SetDome, old orphan modifiers and 1.0.7 remain limits.
Recommend RETIRE on the normal current route; owner decides those constituencies.

## SN-07 — F43 normal admission is already gated (SOURCE)

Coordinator independently read `Lua/Construction/LayoutConstruction.lua:215`,
:228, :270, :296 and `Lua/X/BuildMenu.lua:743`, :784, :845, :859. The shortcut
uses the same prerequisite action. The outer gate checks research and owned
prefabs before activation; current inner filter therefore adds nothing to stable
ordinary admission. Package-prefab exemptions match; repeat Place does not rerun
Activate. F118 repairs registration disturbed by this parent filter. Cached-gate
inventory races, custom/DLC entry and 1.0.7 remain unmeasured. Recommend RETIRE for
normal current play, and remove its unsupported current-data-hidden classification.

## SN-08 — F48 migration call is now correct; rollback is not exact (SOURCE)

Coordinator read `Lua/Buildings/Station.lua:1497-1512`: :1504 now passes ResolveMap
and elements correctly. AppliedSavegameFixups records are keyed by the unchanged
name, so old affected saves can still bypass the corrected migration. Retention
is conditional healing, not a still-broken fresh vanilla migration call.
`Lua/Tracks.lua:578-579`, :602 and :610 alter track state before :617-620 restores
only element list order. pcall does not reverse these writes. Correct the exact-
restoration sentence; preserve the already owner-accepted risk, not a new repair.

## SN-09 — F40 active lookup is not a fresh event route (SOURCE)

Coordinator checked obsolete StoryBit targets and the actual preset registration
and enumeration bodies: `CommonLua/Preset.lua:578` preserves named lookup;
:1773 excludes Obsolete in ordinary enumeration. Current remaster event routes
do not make these targets fresh grants. Existing illness carrier DailyUpdate/
work-status consumers remain. Narrow prevention to historical/dormant scope and
conditional carrier healing; owner decides constituency, without using registry
active as a cure witness. Judgment-call label remains correct.

## SN-10 — F21 lost Comfort consumer, retains statistics consumers (SOURCE)

Coordinator read `Lua/Units/ColonistTransport.lua:660-699`: :671 computes travel
time from start_wait, and :696-697 forwards it to train and track statistics.
`Data/StatsImpact.lua:133-138` instead supplies a fixed -12000 rest-target effect,
using recent-train travel and LuxuriousTrains, not start_wait. Remove the old
duration-based Comfort example from row and every maintained card introduction.
The restamp still repairs inflated train/track statistics; no code rebuild needed.

## SN-11 — F34 affected Embark units are drones (SOURCE)

Coordinator searched current SetCommand Embark sites and read the ordinary
RCCommander route: `Lua/Units/RCRover.lua:279` assigns it to drone; the colonist
Embark notification label is not that setter. LandscapeConstructionSiteBase's
filter is still discarded by its raw units_underneath Scatter callback, reaching
the ClearWasteRock site. Correct row/title colonists to drones. F115 old gate-only
record is superseded by the already owner-authorised hotfix-2 rearm, not a new fix.

## SN-12 — F77 coalesces only pending-window events (SOURCE)

Coordinator read working transition :184, uplink recursion :114-123 and the full
DroneControl removal chain :500 -> TaskRequester RemoveCommandCenter :164-167 ->
DroneControl RemoveBuilding :795-796 -> matching drone Idle :790. The module's
2000ms pending thread still performs one full rebuild. Edges separated by more
than this window each schedule a rebuild. Narrow row grouping promise and module
title; keep the card's true defect headline. EF-023 already disproves the opening
entry's old no-thread-persistence assertion; installed orphan gate is present.

## SN-13 — F50 cancellation does not prove every long trip impossible (INFERRED)

Primary hourly disconnect/Idle chain remains. Coordinator additionally read
`Lua/Units/Drone.lua:677-678`: Idle preserves carried cargo and restarts Deliver;
:1383 chooses a new demand and :1446 approaches it. A SetCommand Idle does not
source-prove a physical reset of every trip. Correct universal over-one-hour
noncompletion to repeated cancellation/delivery disruption. No organic current
permanent starvation was measured; the retained cancellation defect is SOURCE.

## SN-14 — F30 scatter exemption and actual rescue implementation (SOURCE)

Coordinator read `Lua/Buildings/ConstructionSite.lua:1918` and
`Lua/Units/RCConstructorBase.lua:233`: exemption is obstruction-clearing RCConstructor
Construct with matching site; the field is cleared before ordinary RoverWork.
The public all-building-rover explanation is too broad. Actual patch assigns
ExitImpassable after prefab placement to eligible Units map-wide; older bbox/
teleport and battery-to-Freeze sketches are not the current implementation.
Destination/eligibility limits remain; no cure or global side effect was measured.

## SN-15 — F06 rebroadcast has a ten-sol bound (SOURCE; late outcome INFERRED)

Coordinator read current ComposeProc one-shot departure and the scenario's popup
then WaitMsg, and actual Code/Fix_CrystalMysteryHang.lua:73-74 deadline/loop. Source
proves a finite ten-sol repeater; a later popup answer can miss it, but that player
route was not exercised. Replace unlimited after-fix guarantee with the real
rebroadcast window. State-based latch is a separate idea; F103 remains a known
restored-thread limit, not a newly demonstrated failure.

## SN-16 — F31 inspected stopped-story account is not established (SOURCE)

Coordinator read `Lua/RandomMap/RandomMapGenerator_Picard.lua:201` rule/environment
condition, :286 additional-map exclusion and :303 trigger assignment, plus current
CaveIn/FindCaveInLocation missing-map/buildability inputs. The inspected route
cannot simultaneously set the claimed trigger and meet its NoUnderground story.
Binary mapdata/custom/future routes remain unchecked. Keep guards as insurance
recommendation, cut the claimed observed current route; do not file inference.

## SN-17 — F73 requests eligible Idle-entry Rest, cannot promise arrival (SOURCE)

Coordinator checked the installed Idle wrapper and current working residence/
Rest request flow. `Lua/Units/Colonist.lua:2581` can refuse entry, and existing Roam
already has a shelter request. State eligible new Idle-entry attempt, not an
unqualified guaranteed home-before-oxygen outcome. Incremental organic benefit is
INFERRED and unverified. Judgment-call label accurate; homeless have no residence.

## SN-18 — F46 native cap premise now measured independently (MEASURED)

The coordinator avoided the inherited stub target and used a real paused Station
request. Archived native log :223-227 reports baseline2500 -> suspended2500 ->
cleared/restored2500, flags/eligibility exact and control/restore true. The Lua
consumer `Lua/Units/Train.lua:794-796` remains. KEEP: suspension does not close
this positive cap. Actual unload, route exception and cured cargo were not witnessed.
See RUNTIME/entry F46 for the complete log hash and save/probe reconciliation.

## Conditions which did not become false-claim findings

Connector force maintenance/abandoned-owner exceptions and tunnel later-cable
maintenance limits were checked in primary bodies. In their complete row context,
the former describes the ordinary steal loop and the latter the short hookup;
neither promises shared-hex support or enduring maintenance after cable removal.
Keep those modules/claims and retain precision ideas separately. Agreement after
this check does not count as another independent runtime witness.
