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
