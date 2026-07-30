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
| TrainsToVoid | Demolishing a station stores its trains instead of permanently deleting them from the colony |
| LanderEmptyLaunch | Automatic rockets and asteroid landers wait for cargo instead of taking off empty and coming straight back |
| LanderCargoRatchet | Automatic rockets stop unloading the cargo they just loaded (the hourly request no longer shrinks by what is aboard), and fill the hold with the valuable resources first instead of in alphabetical order |
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
| CrystalMysteryHang | The Philosopher's Stone mystery finishes even if you leave its Epilogue popup unread for a sol |
| TouristSatisfaction | Tourist satisfaction stops drifting downwards — a stat rising past two thresholds now pays as much as falling back charges |
| TrainPlatformWedge | A passenger who is no longer aboard no longer wedges the train at the platform forever |
| LowStorageWarning | The "Insufficient Resources" warning fires again for Food and maintenance resources |
| CommandCenterNumbers | Command Center resource rows show their numbers again instead of being blank |
| DomeOverviewHighlight | Domes Overview marks a dome's low colonist stats in red again |
| UniversityOvertraining | Universities stop graduating geologists for extractors that Extractor AI made self-sufficient |
| TrainCargoDumping | Trains stop unloading at stations where you switched that resource off (and hauling it back out again next trip) |
| DestroyedTunnels | A destroyed tunnel stays closed after you reload instead of silently becoming a working shortcut again |
| DustSicknessBiorobots | Biorobots stop catching Dust Sickness (and are cured of it when you load an affected save) |
| DustSicknessDamage | Dust Sickness does its intended 5-14 Health damage per sol instead of a flat maximum |
| GeneForging | The Gene Forging tech raises the rare-trait chance instead of doing nothing at all |
| MirrorSphereSite | A finished Mirror Sphere excavation stops accepting drone work it can no longer use |
| PayloadTemplateRefill | Edit Payload keeps the amounts you set instead of refilling emptied rows from the flight-policy template |
| AsteroidLanderAvailable | "No available Asteroid Landers" is no longer shown while an unassigned lander is sitting on the pad |
| ShuttleHubOffAvailable | Switching a Shuttle Hub off actually removes it from the colony's transport planning instead of leaving colonists waiting for shuttles that never launch |
| FreedHousingNotice | A home falling vacant is offered to the dome's homeless immediately instead of after their next update (up to 12 hours in a big colony) |
| DomeFreeSpaceMismatch | A dome's free-housing figure counts the same residences the game actually assigns colonists to, so a power dip no longer makes a dome read as full |
| SmallLandscapeSites | Small landscaping jobs (a few hexes of clearing, painting or levelling) get worked instead of stalling the drone sent to them |
| LandscapeUnitFilter | Landscaping over a rocket, train or shuttle boarding point no longer drags the colonists who are boarding it back out |
| IndependenceTerraforming | The Independent Terraforming technology discounts terraforming special projects by the 20% its own description parameter names, instead of 10% (applies to games where you research it after installing the pack) |
| FounderTraitNotification | You are told again when one of your Founders picks up a new trait — the check that decided whether to notify could never succeed |
| StorageRateModifiers | Modifiers that change how fast a battery or tank charges and discharges actually reach the grid (nothing in the base game uses these yet — this keeps mods and future updates working) |
| ReplaceTechCount | Swapping one researched technology for another (used by mods and story events) keeps the research counters correct instead of corrupting them |
| SequenceLatents | Two scripting-system bugs modders can hit: "pick N random objects with this label" returned all of them, and the Alien Digger timing swap left both values the same |
| GraphConsumedCaption | The Command Center graph caption for "Consumed" counts maintenance, so the number finally matches the bar it sits next to (Machine Parts and Electronics used to read as almost nothing beside a full-height bar) |
| MoraleComfortTooltip | A colonist's Morale tooltip stops promising a bonus for high Comfort that the game no longer grants, so the listed effects add up to the Morale shown |
| TrainWaitTime | Time spent waiting on a train platform is no longer charged a second time as time spent riding — it stopped costing extra Comfort and stopped inflating train and track travel statistics |
| GridGlobalStorage | "Power/Water/Oxygen stored for N sols" is measured across the whole colony as one figure again, instead of adding up each map's separately — an idle second map used to make every such check permanently true |
| LastTransmissionStorage | The Last Transmission faction actually reacts to your power, water and oxygen reserves. Six of its opinions were wired to a property the game never reads, so they scored nothing however well you stocked up, and its Oxygen goal was measuring Power |
| TrackConnectorPingPong | A station and a train tunnel (or two stations) one hex apart stop deleting each other's track connector over and over, which is why some track layouts would never connect |
| TrackTunnelPowerBridge | A station attached directly to a train tunnel — or to another station a short track away — carries power across again, as the Train Tunnel's description says it should |
| RocketInteractGuard | RC Transports refuse to load from or unload into trade and refugee rockets again — the game's own rule for that stopped matching when the rocket classes were rebuilt for Relaunched |
| TrackSalvageRefund | Salvaging a track pays back half of what the whole track cost, not half of one short section of it — long lines used to refund the same handful of Metals as a six-hex stub. Salvaging part of a track returns that part's Metals too, instead of nothing at all |
| BombardmentSpread | Missiles in a bombardment arrive from spread directions instead of in a parallel rank — the game already worked out a separate angle for each one and then threw it away |
| TechDescriptionBuilding | The Underground Medium Dome technology describes the building it actually unlocks, instead of naming "Jumbo Cave Reinforcements" (only appears in saves from before the 1.0.6 underground rework) |
| AnomalyCaveInMap | Underground anomaly and Buried Wonder story steps that trigger a cave-in no longer risk killing the whole story sequence when there is no underground map to collapse (playing with "No Underground and Asteroids") |
| DroneTransportMinors | Drones keep an accurate list of places they couldn't reach. Every time the map's passability changed — a building finished, a wall went up, terrain was reshaped — that list was rebuilt in a way that held onto buildings you had already salvaged and left its own tally wrong, which quietly throttled drone work |
| TrainMinors | Track that was placed instantly is coloured like track instead of like pipes, and a track's train limit follows its actual length — salvaging a long line down to a stub, or splitting one in two, used to leave the halves with the limit the original had |
| LayoutTechLock | Pre-set building layouts respect research locks, so a layout can't hand you a building you haven't unlocked (nothing in the base game triggers this yet — it keeps mods and future updates honest) |
| ExtenderFlapChurn | A Drone Hub Extender's power flicker no longer tears down and rebuilds its whole hub's task registration, which sent the entire fleet back to Idle every time |
| DisasterPredictionLeak | A finished meteor storm no longer switches off your weather forever — the game kept treating the storm as "still being predicted" after it ended, which silently blocked rains, cold waves and dust storms (existing saves are healed on load) |
| MeteorStormWedge | A meteor storm that wedges mid-drain is detected and released instead of blocking every future storm for the rest of the game |
| RainsDeadlock | A rain that collides with another disaster retries later instead of never raining again |
| SaveSanitizer | Repairs two things already baked into existing saves when you load them: Large Wind Turbines that lost their Frictionless Composites bonus, and upgrade bonuses left behind by buildings you salvaged long ago |

The full defect tracker (91 verified findings and counting) lives in
[docs/BUGS.md](docs/BUGS.md); project snapshot in [docs/STATUS.md](docs/STATUS.md).

## For players

Install to `%AppData%\Surviving Mars Relaunched\Mods\` and enable
"Community Fix Pack" in the Mod Manager. To disable a single fix, create a tiny
mod that loads before this one containing e.g.
`SMRFixPack_Disabled = { CaveInsNoDisasters = true }`, or run it in the console.
Console command `SMRFixPack.ListFixes()` shows what's active.

Removing the mod is always safe. It writes almost nothing into your savegames,
and what it does write is inert without it: a few `SMRFixPack_*` bookkeeping
fields (a timestamp on a housing reservation, a "the player has set this payload"
flag on a rocket, and — from the optional modules — an acknowledgment stamp on a
dismissed building warning and a "closed to new residents" flag on a dome) whose
absence simply means the pre-fix behaviour, and — where a save-repair pass
restored a bonus a broken patch migration dropped — an ordinary label modifier
the game handles like any other.

### Optional modules (off by default)

Some things players ask for are deliberate design changes rather than bugs, so
they ship switched off. Enable them in **Options → Mod Options → Community Fix
Pack** (main menu or pause menu; toggles take effect immediately, both
directions). Other mods can pre-seed the override table before this mod loads:

```lua
SMRFixPack_Optional = { ClassicRockets = true, AcknowledgedWarnings = true }
```

| Module | What it changes |
|--------|-----------------|
| ClassicRockets | A rocket parked at the colony keeps its launch fuel requested even before you pick a destination, so drones refuel it while it waits. Vanilla asks for no fuel at all until a destination is selected. |
| AcknowledgedWarnings | Dismissing a "Building Not Working" warning acknowledges those particular buildings until they recover, instead of silencing the whole category for 4 game hours and then re-nagging forever. Newly broken buildings always warn immediately. |
| ResidencyControl | A new per-dome policy row: "Closed to new residents" — no one new moves in, while current residents keep commuting, working and using services through passages. Quarantine (the accept-colonists toggle) is untouched. Manual relocation and tourists still work. |
| MultipleSuns | Lifts the one-Artificial-Sun-per-colony build limit, and ships the panel-binding repair that makes a second sun actually light the panels built around it (vanilla only ever checks the first sun — a real bug that generic "multiple wonders" mods run straight into). |
| DroneOverhaul | Experimental: repair and cleaning jobs go to the closest hub's fleet first (a far fleet still serves if the near one doesn't respond within seconds), and idle drones help a neighboring overloaded hub with nearby repairs. Player orders, hauling, construction and RC rovers untouched. |
| CohortHousing | Seniors and Children living in normal housing automatically move into free Retirement Home / Nursery slots — own dome first, any reachable dome second — and are left alone when no such slot exists. Employed Seniors stay put; manual assignments always win; quarantine and closed domes respected. |
| DroneStatDials | Not a toggle — two dropdowns on the same Mod Options page: **Drone speed** (1x base / 2x / 3x / 5x, stacking on top of the speed techs) and **Drone carry capacity** (+0 base / +1 / +2, stacking with Artificial Muscles). Both take effect immediately in both directions; the base positions are exactly vanilla, and the module ships at base. (No `SMRFixPack_Optional` entry — the dials are read from Mod Options directly.) |

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
