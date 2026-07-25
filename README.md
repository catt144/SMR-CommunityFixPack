# Community Fix Pack — Surviving Mars: Relaunched

A bug-fix mod for Surviving Mars: Relaunched. Every fix targets a **verified
defect in the game's shipped Lua source** — no balance changes, no opinions,
no game files modified. Fixes are applied at runtime in a mod-compatible way
and can be individually disabled.

**Status: in development, not yet released.**

## Current fixes

| Fix | What it does |
|-----|--------------|
| CaveInsNoDisasters | Cave-ins no longer occur when the "No Disasters" game rule is active |
| MeteorFrequency | Meteors strike on their designed 35–115h schedule instead of ~every 6 hours (and Sensor Towers help again) |
| UpgradeModifierLeak | Salvaging an upgraded building removes its dome/colony-wide bonuses instead of leaking them forever |
| NightShiftWork | Night-shift colonists return to work after midnight instead of skipping the rest of their shift |
| MilestoneCrash | Completing all milestones no longer errors in No Terraforming / No Politics games |
| WispRewards | Mystery 11: "free the wisps" produces real power; destroyed-wisp research rewards match the notification |
| TouristApplicants | Higher tourist star ratings correctly give more bonus applicants (the chance roll was inverted) |
| FactionFundingCheck | Faction goals based on recent export/tourism income can actually trigger |
| TrainsToVoid | Demolishing a station stores its trains instead of permanently deleting them from the colony |
| LanderEmptyLaunch | Automatic rockets and asteroid landers wait for cargo instead of taking off empty and coming straight back |
| LanderCargoRatchet | Automatic rockets stop unloading the cargo they just loaded (the hourly request no longer shrinks by what is aboard) |
| LanderReturnFuel | Asteroid landers keep the fuel reserved for the trip home instead of dumping it on the asteroid |
| ShelterReflex | Colonists idling outdoors in vacuum head home before they suffocate; a habitat power blip no longer evicts its residents |
| BrokenTrackSalvage | Meteor-damaged tracks can be salvaged again (and existing damaged tracks in your save are repaired on load) |
| TrackSalvageWipe | Salvaging a single track piece trims the track instead of deleting the whole line and every train assigned to it |
| LakeEntombment | Building an artificial lake frees the RC Constructor and drones the new basin would otherwise seal in |
| GhostFarmOxygen | Salvaging a farm removes the oxygen it supplied to its dome (and existing phantom oxygen is cleaned up on load) |
| RocketDroneChurn | Landed rockets stop sending their delivery drones back to Idle every game hour |
| ShuttleTransportCache | Building a Shuttle Hub is noticed: colonists stop being stuck on a cached "there is no route" verdict |
| VacuumWalks | Colonists moving between nearby domes in an unbreathable atmosphere use the passages instead of walking across the surface |
| ArrivalDeaths | New arrivals stop marching to a dome they cannot reach, and no longer disembark into impassable ground |
| DroneUnreachableForever | A drone that once failed to reach a building tries again later instead of ignoring it for the rest of the game |
| StaleReservations | Housing reserved for colonists who never arrive is released again instead of being held forever |
| HomeDomeMigrationGate | Turning off "accept colonists" no longer stops a dome's own residents from shopping, working and training next door |
| CrystalMysteryHang | The Philosopher's Stone mystery finishes even if you leave its Epilogue popup unread for a sol |
| TouristSatisfaction | Tourist satisfaction stops drifting downwards — a stat rising past two thresholds now pays as much as falling back charges |
| TrainPlatformWedge | A passenger who is no longer aboard no longer wedges the train at the platform forever |
| LowStorageWarning | The "Insufficient Resources" warning fires again for Food and maintenance resources |
| CommandCenterNumbers | Command Center resource rows show their numbers again instead of being blank |
| DomeOverviewHighlight | Domes Overview marks a dome's low colonist stats in red again |
| UniversityOvertraining | Universities stop graduating geologists for extractors that Extractor AI made self-sufficient |
| TrainCargoDumping | Trains stop unloading at stations where you switched that resource off (and hauling it back out again next trip) |

The full defect tracker (73 verified findings and counting) lives in
[docs/BUGS.md](docs/BUGS.md); project snapshot in [docs/STATUS.md](docs/STATUS.md).

## For players

Install to `%AppData%\Surviving Mars Relaunched\Mods\` and enable
"Community Fix Pack" in the Mod Manager. To disable a single fix, create a tiny
mod that loads before this one containing e.g.
`SMRFixPack_Disabled = { CaveInsNoDisasters = true }`, or run it in the console.
Console command `SMRFixPack.ListFixes()` shows what's active.

Removing the mod is always safe — it stores nothing in your savegames.

## For modders

See [docs/FIX_POLICY.md](docs/FIX_POLICY.md). Short version: data patches and
chained wrappers over replacements; every fix self-checks the target code
before patching and deactivates itself (with a logged reason) if a game update
already fixed it; `SMRFixPack_Disabled` is the veto surface.

## Credits

- ChoGGi — the original Surviving Mars "Fix Bugs" mod documented several of
  these bug families years ago; this pack independently re-verified everything
  against the Relaunched source.
- LukeH — Martian Express patch research for the original game.
