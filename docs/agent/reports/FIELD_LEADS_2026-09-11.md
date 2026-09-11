# Field leads triage — 2026-09-11 (six owner-relayed reports)

Written by `smr-bugfixpack-0d` at the owner's ask ("investigate some new leads"; meteors: surface sweep only).
⚠️ Reports are NOT authority — where this and an entry disagree, the entry wins.

- **Inputs:** owner screenshots of Steam General Discussions threads and one r/SurvivingMars thread. The imgur album
  (`imgur.com/a/ZGK0ibJ`, the lake screenshot) could NOT be fetched (the agent's fetch tool is blocked for imgur).
- **Trees:** game 1.1.0.403908 (installed `ModTools\Src`) and the 1.0.7.396349 archive.
- **Method:** seven read-only investigators (six leads + one data decode), then every load-bearing claim re-read by this
  session. Tags: SOURCE = re-read here; INHERITED = the investigator's read, not re-checked; INFERRED = derived.
- **Nothing was launched or reproduced.** No save exists for any report.

| # | lead (where) | verdict | home |
|---|---|---|---|
| 1 | Wildfire cure rocket stuck on the pad, "20 fuel to unload" (Reddit, 2 players, PC + PS5) | **real vanilla defect, P1 mystery soft-lock** | [F119](../bugs/F119.md), checklist 146 |
| 2 | "Building codes" law doesn't apply to prefabs (Steam) | by design; at worst a gain for the player | here §2 |
| 3 | Producer "Clogged after a Dust Storm" never recovers (Steam, 2 players) | candidate; the failing link not pinned | [C85](../bugs/C85.md) |
| 4 | "Landscaping excavation is too deep" for lakes (Steam) | a real terrain rule, not a regression, not the pack; this map's cause undetermined | here §4 |
| 5 | Probe deep scan reveals nothing (Steam) | the ordinary Adapted Probes rule; a separate minor defect found | [C86](../bugs/C86.md) |
| 6 | Meteors always hit the base (Steam) | nothing concerning | here §6 |

Reply drafts for all six: `FIELD_REPORT_REPLIES.md` → "Field reports triaged 2026-09-11". Owner items: checklist 146, 147.

## 1 · Wildfire cure rocket → F119

See the entry. One line: a landed `Trade` rocket sizes its fuel request once at landing, and only player-controlled
rockets re-size on a fuel-cost change (`UniversalRocket.lua:1916-1920`, SOURCE, both trees). Advanced Martian Engines
(−20, the reported number) or — new in 1.1.0 — the Fuel Conservation law (and every Ministry of Technology working
flip under it) leaves the cure rocket unable to reach "ready", and Mystery 8 waits on it with no timeout.

## 2 · Building codes vs prefabs — by design

- INHERITED: 1.1.0 replaces the old cost-only law with Lax/Strict (`Data/PolicyDef.lua:296-303`); the old
  `Policy_BuildingCodes` is `Obsolete` (`LawDef-Efficiency.lua:476`). Lax: −20% Concrete/Metals construction cost, +50%
  maintenance for new buildings (`:692`); Strict: +20% cost, −30% maintenance (`:900`). Both maintenance effects open with
  `if from_prefab then return end` (`:697-705`, `:905-912`).
- INHERITED: every prefab route sets the site `supplied` + `prefab` (`X/BuildMenu.lua:839`, `X/Infopanel.lua:498-499`,
  `LayoutConstruction.lua:479-480`); a supplied site requests no resources (`ConstructionSite.lua:696-710`), so the cost
  change has nothing to act on; the `from_prefab` flag is new in 1.1.0 and read only by these two exits — a deliberate
  carve-out.
- SOURCE: the one layout reset that could split `prefab` from `supplied` is commented out
  (`Lua/Construction/LayoutConstruction.lua:496-505`); both flags come from the caller's params (`:316-317`).
- Effect: under Lax a prefab skips the +50% maintenance (a gain); under Strict it skips the −30% but never paid the +20%.
  No loss → nothing to repair (the "fix negatives" rule).

## 3 · Clogged after a dust storm → C85

A one-time story event, `BuildingClogged` — not maintenance. "We'll fix it after the storm" only arms a follow-up on the
NEXT storm end, which fires one follow-up per end (SOURCE, the pick at `Lua/_StoryBits.lua:199-216`). Two
hypotheses in the entry. SOURCE: the 1.0.7 body disables the building with no reason text
(`Data/StoryBit/BuildingClogged.lua:4-6 @1.0.7`, `SetBuildingEnabledState` nil); 1.1.0 adds "Clogged after a Dust Storm."

## 4 · Lakes: "excavation too deep" — a terrain rule; this map's cause undetermined

- SOURCE: the only raiser is `LandscapeLake:GatherConstructionStatuses` — `if z + z0 <= 0` with `z = prefab.min.z` and
  `z0` the cursor's visual Z (`Lua/Buildings/LandscapeLake.lua:347-358`), **byte-identical on 1.0.7** (`:295-305`). Not a
  regression.
- INHERITED: loc `ConstructionStatus.LandscapeLowTerrain` (`LandscapeConstructionController.lua:296`); `[`/`]` cycle
  `entity`/`entity2`/`entity3` (`GameShortcuts.generated.lua:882-918`, `Construction.lua:3209-3212`).
- INHERITED, the decode: `PrefabMarkers` come from `Packs\Data.fpk` → `MapData/PrefabGameplay_01..03.lua` (Lua 5.3
  bytecode; decoded with `tools/flpk_extract.py`, a 3-byte size-header patch to stock 5.3, and `lupa.lua53`). Every
  variant ships a marker:

  | entity | `min.z` (raw height units) |
  |---|---|
  | LakeSmall01_01 / _02 / _03 | −1020 / −1008 / **−947** |
  | LakeMid01_01 / _02 / _03 | −1420 / −1470 / −1523 |
  | LakeBig01_01 / _02 / _03 | −2090 / −2215 / −2155 |
  | LakeHuge01_01 | −3554 |

  `min.z` is in raw heightmap units (PrefabGameplay_01's grid is flat 10000; its lowest point 6446 = 10000 − 3554).
  The stock blank maps' lowest core ground is 5703–10000 raw; the asteroid map's is 1884.
- Hypotheses:
  - **"The one working variant has no prefab" — REFUTED** (all ten present).
  - **"Low terrain" — refuted for the stock blank templates, NOT for a generated map.** The decode read templates; a new
    game's terrain comes from `RandomMapGenerator`, and 1.1.0 added `terrain.QuantizeHeight(map, 8)` to it
    (`RandomMap/RandomMapGenerator.lua:3010`; C++, body unreadable). INFERRED: the report — every variant fails except the
    **shallowest** small one (−947 vs −1008/−1020) — is exactly what a cursor height between 947 and 1008 predicts.
- INHERITED side note: the check adds a raw-unit `min.z` to a world-unit `z0`; if `TerrainHeightScale > 1` that makes it
  more lenient, never stricter.
- **The pack: SOURCE-grep-negative** (INHERITED list: no `Code/` hit for `GatherConstructionStatuses`, `UpdateCursor`,
  `FixConstructPos`, `ConstructionStatus.`, `ChangeAlternativeEntity`, `PrefabMarkers`); `Fix_LakeEntombment` post-wraps
  `PlacePrefab`, which runs after placement, never during the status check.
- **Decisive check (optional, checklist 147):** on any 1.1.0 colony, try a lake. If it places, the report is
  map-specific. The runtime readout for a failing spot `[NEVER RUN]`:
  `local z=GetConstructionController().cursor_obj:GetVisualPos():z() print("LAKECHK", z)` — with the lake cursor over a
  failing hex.

## 5 · Deep scan finds nothing → the rule, plus C86

- SOURCE: a probe deep-scans only with **Adapted Probes** (`Lua/OrbitalProbe.lua:94-97`, both trees); Deep Scanning
  lets queue scans go deep on re-scan (`Exploration.lua:359`, `:852`, `CanBeScanned` `:154-172`). Probes fired without
  Adapted Probes only basic-scan. Reply 3 in the thread describes exactly this.
- INHERITED: revealed deposits show for 150 s of game time after a scan (`Exploration.lua:115`,
  `SetSectorSubsurfaceDepositsVisibleExpiration(sector, 150000)` — SOURCE line) and then hide unless the subsurface
  overlay is on — a second way to "see nothing".
- `MapSector:Scan` is byte-identical between trees (INHERITED). "A clean reinstall fixed it" proves nothing either way.
- A separate minor defect: the Advanced Orbital Probe downgrades deep-scanned neighbours → [C86](../bugs/C86.md).

## 6 · Meteors always hit the base — nothing concerning (surface sweep, owner's scope)

- SOURCE: a regular strike picks `GetRandomPassable(map)` — a random passable point anywhere (`Lua/Meteors.lua:109`,
  `:174`); INHERITED: `SpawnMeteor` is unchanged from 1.0.7 (`:81-113 @1.0.7`); building-aimed strikes exist only on
  scripted routes (`ClassDef-Effects.lua:5254`, `ScriptStatements.lua:1010-1016`). SOURCE: `Meteors.lua:700` only places a
  deposit beside a building a meteor already hit.
- SOURCE: the pack has no meteor module left (hotfix 2 deleted `Fix_MeteorFrequency` / `Fix_MeteorStormWedge`); the
  seven `Code/` files that mention meteors are comments naming the deleted module, `Fix_SinkholeIndestructible`,
  `Fix_BombardmentSpread` (Mystery 7 missiles) and `Fix_BrokenTrackSalvage` (post-damage) — none picks a target.
- INHERITED: 1.1.0 changed how a HIT counts (`GetHitObjects`, `Meteors.lua:488-513` vs `:394-408 @1.0.7`: hex-footprint
  building query, moving units skipped), not where it lands. A deeper dig, if ever wanted, starts there.
- The replies in the thread (small bases untouched, big ones hit) fit a uniform random pick.

## Not done

- The imgur album was unfetched; the map/landing site and mod list of every reporter are unknown.
- No game launched, nothing reproduced; F119's proposed fix is not built.
