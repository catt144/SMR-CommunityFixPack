# SMRTK layout format v1

P5 contract, 2026-09-13. Source-derived on game build 24995074; real placement
and colony behavior await sitting 08. The TestKit owns this format.

```lua
return {
  v = 1,
  name = "fixture",
  anchor = { q = 120, r = 40 },
  buildings = {
    { t = "DomeBasic", dq = 0, dr = 0, a = 0, e = "DomeBasic" },
    { t = "LivingQuarters", dq = 1, dr = 0, a = 3600, dome = 1,
      upgrades = { 1 } },
  },
  grid = { { k = "cable", dq = 9, dr = 0 }, { k = "pipe", dq = 9, dr = 1 } },
  meta = { map = "BlankBig_01", sol = 10, captured = 7500000 },
}
```

This illustrates the schema, **not a buildable fixture or validated offsets**.
`name` is 1–48 ASCII letters/digits/underscores/hyphens, beginning with a letter
or digit. Anchors and offsets are integer axial hex coordinates; the anchor
records capture provenance and is replaced by the chosen target on replay.
Angles are the game's minute units, 0–21599, in multiples of 3600. V1 preserves
each angle and does not rotate the entire layout. `dome` is a one-based index
into `buildings`, never a handle; a dome cannot itself name a parent. Optional
`e` records the live entity and refuses replay against a different default
entity, rather than silently changing a skinned footprint. `upgrades` is a
strict ascending list of built upgrade tiers 1–6. Optional grid `unsupported`
records why a node is captured for inventory but cannot replay in v1.

Only these fields are accepted. Raw scalar fields are normalized into fresh
plain, acyclic tables and densely indexed arrays. `next` and `rawget` ignore
input metatable behavior; metatables are not copied or treated as data. This
is normalization, not a claim to reject every metatable-bearing input.
Unknown versions, unknown keys, duplicate grid nodes, dangling/cyclic/non-dome
references, invalid numbers and oversized captures refuse before placement.
Limits: 512 buildings, 2048 grid nodes, absolute anchor/offset magnitude 8192,
12 saved layout names, serialized capture at most 1 MiB. A whole-map capture
over either object cap refuses atomically; it does not silently clip the map.

## Capture and loading

Selected dome captures that dome and every enumerated `Building` whose center
`GetDomeAtPoint(map.object_hex_grid, obj:GetPos())` assigns to it. A selected
ordinary building captures itself and its enclosing dome as a dependency.
Rectangle capture uses two **world x/y** corners and object centers, inclusive;
it is not an axial parallelogram. Whole-map capture enumerates the current map.
Rectangle/whole-map captures close missing dome dependencies before indexing.
Capturing a dependency dome does not pull all its other interiors into a
rectangle. The recorded row order is deterministic, domes first.

The enumerated grid classes are `ElectricityGridElement`,
`LifeSupportGridElement`, and `PassageGridElement`. Construction sites, destroyed
objects and grids under construction are excluded. Passages, suspended grid
chains, grid switches, and pipe/cable pillars that represent a suspended span
retain an `unsupported` reason and produce a named skip in plan/stamp.

The explicit building exclusion families are `UniversalRocketBase`,
`UniversalSupplyPodBase`, `SupplyRocket`, `RocketBase`, `RocketLandingSiteBase`,
`LandingPadBase`, `ElevatorBase`, `TunnelBase`, `TrackBase`, `TrackGridElement`,
`PassageBase`, `PassageRampBase`, `PassageGridElement`, `OpenCityBase`,
`LandscapeLake`, `MarsReservationBase`, `DepositExploiter`,
`TerrainDepositExtractor`, and `SpireBase`. These need vehicle state, paired/map
endpoints, ordered routes, terrain/deposit data, or a snapped placement contract
that v1 does not capture. A template with a custom `PlaceConstructionSite`,
snapped placement, or absent/nonstandard build shape is also refused. Every
omission is logged by class/template and reason. Ordinary capture support is a
bounded enumeration, not a claim that every building class is equivalent.

Successful capture copies deterministic `return { ... }` text and stores a
normalized table in `LocalStorage.smrtk_layouts[name]`. The write is persisted
on a real-time thread, with a separate tagged persistence result. A duplicate
name refuses; changing the name or explicitly selecting the existing saved
layout avoids an accidental overwrite. No runtime file reader/compiler is used.

A metadata-listed `Layouts/<name>.lua` must **queue data**, because the mod code
loader discards a file's returned table and runs every non-`Code/` file before
every `Code/` file (`Mod.lua:492–514`), regardless of metadata order. Use:

```lua
SMRTK = rawget(_G, "SMRTK") or {}
SMRTK.layout_files = SMRTK.layout_files or {}
SMRTK.layout_files.fixture = (function()
  -- Paste the capture's literal return table here.
end)()
```

This is an authoring pattern, not a complete fixture. `77_SMRTK_Stamper.lua`
normalizes each queued value after its registry exists. Add the exact layout
path **and** `Code/77_SMRTK_Stamper.lua` to TestKit's metadata code list. Runtime
code with an already-loaded toolkit can use `SMRTK.RegisterLayout(table)`.
Agent/coordinator
edits occur with Mars.exe closed. Session-file registrations and LocalStorage
names occupy one namespace; collisions refuse rather than shadow silently.

## Plan and bounded replay

Plan is a side-effect-free placement forecast with tagged per-row evidence.
Buildings use terrain bounds, every rotated build-shape hex, native gridded and
ungridded obstruction queries, and captured-parent dependencies. There is
**no `test` parameter on `PlaceConstructionSite`** (`ConstructionSite.lua:2193`).
Its trailing booleans change passability/flattening and must never be mislabelled
as a dry run. The plan never calls that placer. It cannot certify construction
controller conditions, runtime GameInit behavior, or a future dome's collision
glass; those remain explicit dependencies and sitting observations.

`IsBuildableZoneQR` is only terrain classification (`BuildableGrid.lua:310–312`),
so a true result is not full fit. Native shape queries add occupancy checks.
No placement proceeds across a captured-parent failure, existing incompatible
object, terrain height mismatch, missing class/entity/shape, map change, save,
load, or reported Lua error. Both capture and replay bind the actual
`CurrentMap` object and its `City`, not a stored map-name string or `UICity` from
another map. Layout provenance does not prohibit deliberate stamping on a new
map; an operation cannot switch maps halfway through.

Pass order: domes, complete those new sites, ordinary/exterior and interior
buildings, complete those new sites, flat grids, complete those new groups.
Only the site references returned by our placements enter completion. Ordinary
sites use `:Complete("quick_build")`, retaining its returned object for a second
stage if it is still a site. Grid leaders use `:Complete("quick_build_skip_done")`
for **all owned groups before any owned site is removed**, matching the native
cross-group connection ordering (`Cheats.lua:55–104`,
`ConstructionSite.lua:2659–2706`). Existing construction is never included in
the completion set. The tool does not call the map-wide complete-all helper.

Cable/pipe line tests pass `test=true` and **no input construction group**; the
leaf's `or input_constr_grp` branch can otherwise mutate even during a test.
The returned `data` is indexed from **0**. A truthy first return means “can
build anything,” so every requested cell must also report `clear`. `steps=1`
means two nodes (`for i=0,steps`), used only for two captured adjacent nodes.
An isolated node uses `steps=0`. There is no invented neighbor outside the
capture. Retesting immediately before each actual line catches current-world
changes. Grid geometry is reconstructed from flat adjacency; skins, switch
state, suspended-span engineering and deliberate disconnected adjacency are
outside v1.

Passage replay is **OWNER-ROUTED / stopped**: `Passage.lua:1917–2275` needs
scratch/entrance data and shared `input_data.passage_obj`, ordered nodes and
endpoint domes. A bag of hexes does not preserve that contract. The inventory
survives export, but neither plan nor stamp invokes the passage placer.

Stamping is explicitly targeted by one armed click, then the click listener is
released. The actual work runs inside registered dispatch on a real-time
thread with a three-second GameInit deadline. Stamping refuses a paused game:
GameInit itself uses game-time threads (`CommonLua/Classes/_object.lua:187–195`),
so a real-time waiter cannot make it finish while paused. Planning works while
paused. Lifecycle cancellation
checks precede every later mutation. Cancellation preserves already-created
ordinary game objects and reports the partial result; it is not a rollback.
An API/engine failure stops later placements, and a fit refusal logs
`SMRTK_STAMP_SKIP template=<template-or-kind> hex=<q,r> reason=<reason>` and continues.
The core reserves `t` for game time; the prompt's `t=<template>` cannot survive
that logger and is deliberately replaced by `template`.
The summary counts successfully completed buildings and observed new grid
nodes, separately exposing left-over construction and skipped rows.

## State and future version

Upgrade tiers are captured before state replay is enabled. The optional state
step was added after the coordinator committed the base and the desk harness
passed three synthetic clean plans. This replaces the brief's impossible
building `test=true` stamp gate; it is a **DEPARTURE for 03B**, not native stamp
evidence. The follow-up acts only on the last
successful stamp's retained building references. `ApplyUpgrade(i,true)` can
unlock that upgrade colony-wide (`Building.lua:1131–1143`), and starts a built
upgrade enabled. The page discloses both effects. The log distinguishes an
unlock request from `IsUpgradeUnlocked(id)` afterward, since a force-lock can
still suppress the eligibility read (`UpgradeUnlocks.lua:23–33`). Funding,
colonists, and storage fill are explicit World actions resolved at invocation:
`funding(500000000)`, `spawn_colonists(10)` and `fill_storages()` (all maps).
Colonists follow vanilla's selected-dome/current-city rule, not automatically
the newly stamped dome. Capture never applies these actions implicitly.
Save/load/map lifecycle invalidates the retained last-stamp references.
No real stamp or upgrade success is claimed before 08.

V2 can rotate axial offsets with `HexRotate(q,r,dir)`, and add `dir*3600` to each
angle modulo 21600; the source pattern is `hex.lua:152–169` and
`Construction.lua:1408–1412`. It must rotate dome references, footprint evidence,
and any future ordered grid topology together. Passage ownership and endpoint
capture merit a separate versioned route structure before replay is enabled.
