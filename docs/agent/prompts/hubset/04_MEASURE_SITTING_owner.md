# hubset 04: measure the hub footprint, markers and rescue anchors (attended)

Chain rules: [README.md](README.md). Read them, then `## Notes from upstream` below, first.
**Attended:** the owner loads the save and types the lines; the session prepares, relays and records.
It can fire at any time, even before link 01. It builds nothing.

## Authority and outcome

C114 and C116 (link 05) need a physical "is this colonist on the hub" test. The resweep forbids a
marker-only version while the hub's walkable footprint is unknown. On TheGodUncle's save, 35 of the
45 units held by hub 2692 stood beyond its collision radius (`SMRHUBOFF`, field findings §4), but its
ramps may reach that far. End state: an archived log carrying the four readings below, and a
verdict for each prediction appended to [C114](../../bugs/C114.md), [C115](../../bugs/C115.md) and
[C116](../../bugs/C116.md) and to 05's inbox, committed on `main`.

## Setup

- The owner's copy of the reporter's save (`New Horizons 2 83`), game `1.1.1.405907`, the junction on
  `main` (the shipped pack touches none of this code). Passage Network off, as in the mods-off run.
- Console on: the TestKit's enable (Enter, or Alt-Shift-C, once in the colony).
- Unpause at normal speed for a few minutes before the first reading, so shifts move colonists over
  the hubs.

## The lines (checked against archived 1.1.1.405907, parsed and smoke-run on the desk)

Type line 0 first each time the game starts; it defines the helper the others use. Then run 1, 2
and 3. Wait about five game minutes, and run 1, 2 and 3 again. When a colonist's status shows "Moving
to a new Dome: Brussels", run 3 again.

```lua
SMRCLS = function(m, p) if not p then return "nopos" end local g = m.object_hex_grid local b = HexGetBuilding(g, WorldToHex(p)) if not b then return GetDomeAtHex(g, WorldToHex(p)) and "dome" or "none" end if IsKindOf(b, "PassageHub") then return "hub" .. b.handle end if IsKindOf(b, "PassageGridElement") then return "passage" end if IsKindOf(b, "Dome") then return "dome" end return b.class end print("SMRCLS ready")
```
```lua
for _, h in ipairs(MapGet("map", "PassageHub")) do local m = h:GetMap() local t, n = {}, 0 for _, u in ipairs(h.units or {}) do n = n + 1 local p = u:IsValidPos() and u:GetVisualPos() local c = SMRCLS(m, p) t[c] = (t[c] or 0) + 1 if c ~= "hub" .. h.handle then local gz = p and terrain.GetHeight(m, p) or 0 print(string.format("SMRFOOTU hub %d unit %d at %s dist %d dz %d cmd %s", h.handle, u.handle, c, p and h:GetDist2D(p) or -1, p and ((p:z() or gz) - gz) or 0, tostring(u.command))) end end local s = "" for k, v in sorted_pairs(t) do s = s .. " " .. k .. " " .. v end print(string.format("SMRFOOT hub %d held %d%s", h.handle, n, s)) end
```
```lua
local n, t = 0, {} for _, c in ipairs(MapGet("map", "Colonist")) do local h = c.passage_hub if IsValid(h) then n = n + 1 local m = c:GetMap() local p = c:IsValidPos() and c:GetVisualPos() local at = SMRCLS(m, p) t[at] = (t[at] or 0) + 1 print(string.format("SMRMARKU col %d hub %d at %s dist %d outside %s holder %s cmd %s", c.handle, h.handle, at, p and h:GetDist2D(p) or -1, tostring(c.outside_start), c.holder and c.holder.class or "none", tostring(c.command))) end end local s = "" for k, v in sorted_pairs(t) do s = s .. " " .. k .. " " .. v end print(string.format("SMRMARK marked %d%s", n, s))
```
```lua
local n = 0 for _, c in ipairs(MapGet("map", "Colonist")) do local t = c.transport_task if t and t.dest_dome and t.dest_dome == c.dome and t.source_landing_site then n = n + 1 local m = c:GetMap() local a = t.source_landing_site[1] local p = c:IsValidPos() and c:GetVisualPos() print(string.format("SMRANCH col %d cmd %s at %s anchor %s anchor_dist %d outside %s marker %s holder %s shuttle %s age %d", c.handle, tostring(c.command), SMRCLS(m, p), SMRCLS(m, a), (p and a) and c:GetDist2D(a) or -1, tostring(c.outside_start), tostring(IsValid(c.passage_hub)), c.holder and c.holder.class or "none", tostring(not not t.shuttle), GameTime() - (t.creation_time or 0))) end end print("SMRANCH rescues " .. n)
```

What each reports. `at` is the building owning the hex under the unit: `hub<handle>`, `passage` (a
passage element), `dome`, another building's class, `none` (bare ground) or `nopos`. `dz` is height
above terrain; a unit on a ramp or deck stands above it.

- `SMRFOOT` per hub: how many held units stand on which kind of hex. `SMRFOOTU` lists each held unit
  not on that hub's own hexes, with distance and height.
- `SMRMARK` / `SMRMARKU`: every colonist carrying a hub marker, where it stands, and whether its
  outside timer runs.
- `SMRANCH`: every own-home rescue in flight: where the colonist is, where its pickup is, and whether
  it is outside.

## Predictions (write the verdict for each)

1. **Footprint (S4, C114/C116).** If every held unit stands on `hub<same>` or `passage` hexes or has
   `dz` above zero, the hub's walkable area is its hexes plus its passages: S4 is refuted, and a
   hex-ownership test is a sound "on the hub" discriminator for 05. If held units stand on `none` with
   `dz` 0, S4 holds: the holder is carried off the hub, and 05 must not trust `holder == hub`.
2. **Markers (C116).** Marked colonists at `none` or `dome`, far from the hub, with `outside false`,
   confirm the stale marker in play. All marked colonists on hub or passage hexes refute its field harm.
3. **Anchors (C115).** A rescue whose colonist is at `dome` while its anchor is at `passage` or `hub`
   shows the obsolete pickup. An anchor at `none` beside a colonist also at `none` is the ordinary
   case.
4. **Reconciliation.** Each `SMRFOOT` line's category counts sum to its `held`; each `SMRMARK` total
   to its `SMRMARKU` lines. A mismatch voids that reading.

## Close-out

Archive the newest `Mars.exe-*.log` to `docs/archive/logs/` (force-add past the `*.log` ignore) in the
commit that cites it. Append each verdict, with its log lines, to C114, C115 and C116, and the
footprint verdict and any discriminator it supports to 05's inbox and 99's. Strike your row,
`git rm` this file, commit on `main`. If prediction 1 comes back mixed, stop and route it to the owner
before 05 fires.

## Notes from upstream
