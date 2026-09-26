# C119 build — load-time cleanup of stale power-connection cells

## Must_Read_Header

One-off build brief, authored 2026-09-26 at the commit that filed C119 (parent `ee72eb8`).
Consumed when the module and its desk evidence land and the attended sitting is preloaded.
Delete this file and its `prompts/README.md` row in that commit.

## Authority and outcome

The owner ruled the fix shape on 2026-09-26. The ruling is quoted verbatim in
[C119](../bugs/C119.md), "Owner ruling on the fix shape". Build v1 exactly as recorded there. Do not
reopen load-only versus a connect-path guard, and do not widen the scope to water. The owner's
standing rule is to add shapes as they are witnessed and confirmed.

**Settled by C119, not reopened here.** C119's origin is unknown. FIX_POLICY §4's "proven,
reachable" test is met by the measured harm (throw, gridless element, spread, persistence), and the
owner ruled a repair of the state rather than of the trigger. If §4 reads otherwise to you, record
that in the commit message and build anyway.

**End state:**

- A pack module that, after each load on every loaded map, zeroes electricity connection cells
  that are nonzero, lack the tunnel bit (32768), and have no object with `.electricity` on the hex.
- It then reruns the connect for electricity objects left with no grid (all electricity classes,
  not only `ElectricityGridObject`).
- It logs one line of counts.
- It follows FIX_POLICY: §2 fail-safe, §2a/§2b guard and manifest, §3/§3a save safety (no
  persisted fields, threads or functions), and the toggle convention.
- Desk evidence, and SMRTK slots for the attended sitting.
- C119 updated with the build's SHA, the desk results and the sitting plan. The status stays
  `cand` until the sitting.

## Evidence you would otherwise re-derive

All numbers come from `docs/archive/logs/kkag4870_Mars.exe-20260926-10.33.35-6aad2d75.log` (a
retail 1.1.1.405907 session with the pack on). Recheck each with `grep -n "^SCAN\|^GSPLIT" <log>`.

- **Reporter's save, fresh load** (`saves/game/KKAG-4870_Europe Sol 280.savegame.sav`): 355 of 1094
  electricity cells are stale; 2 of 216 water cells.
- **Clean controls:** two owner colonies read 0 stale (4854 cells; 1211 cells). A DomeHexa removed
  cleanly: 48 cells each for power and water.
- **The probe predicate used for those counts:**
  `HexGridGetObject(map.object_hex_grid, q, r, nil, nil, function(o) return o.electricity end)`
  over `q, r` in `0..size-1` of `object_hex_grid:size()`. This is the vendor loop shape in
  `SavegameFixups.CleanupStaleHandlesInObjectHexGrid` (`Lua/GridObject.lua`).
  - **Falsifier:** the same predicate over a clean colony must return 0. If it does not, the rule
    is wrong before any code is written.
- **Mechanism anchors** (1.1.1 `Lua/SupplyGrid.lua`; re-derive the lines with `grep -n`):
  - cells are written at the `SupplyGridApplyBuilding(` call inside `SupplyGridConnectElement`;
  - the throws are at the `adjacent[supply_resource]` indexes;
  - `SupplyGridDisconnectElement` returns at `if not grid then return` before
    `SupplyGridRemoveBuilding`.
- **Load ordering:** `Code/90_SaveSanitizer.lua` documents why a repair runs on PostLoadGame and
  not LoadGame. Decide where this belongs: a new module or that sanitizer.

## Judgment delegated to you

- Where it lives, how it is guarded, and how reconnection is done safely:
  - a reconnect that throws must not abort the pass;
  - partial connections from the original failure may leave duplicate visuals.
- Whether underground and asteroid maps need anything beyond iterating `LoadedMaps`.
- How to handle construction sites with elements.
- Performance: one pass is about 437,000 hexes on the reporter's map (615 x 710). Measure it
  rather than estimate.

## The one pre-ship check the ruling requires

C119 names the Excavator, terraforming buildings, the Regolith Extractor and Open City as buildings
whose connection shape may reach past their model. Show, at the desk from source or in a fixture
that contains them, whether their cells read as matched under the predicate. Any that do not are
added to the claimed set from their own `GetSupplyGridConnectionShapePoints("electricity")`, and
you record which ones in C119.

## Tests

Follow `docs/agent/WORKFLOW.md` "Testing checklist per fix" and "Fixtures, mutations and
owner-typed lines". The reporter's save is a third-party fixture: never overwrite it, and work on
a copy.

**Desk:**

- stale cells are cleared;
- tunnel-bit cells are kept;
- cells claimed by an object are kept;
- a module-off control shows the stale cells unchanged;
- a mutant with the tunnel-bit skip removed must fail.

**Sitting (owner-attended, preloaded into SMRTK slots per `tools/SMRTK.md`; the owner clicks):**

1. The reporter's save loads with the module on. The log line reports 355 cleared (or explains any
   difference by name), and a follow-up scan slot reads 0.
2. A cable laid across the old footprint connects with no `SupplyGrid.lua` error.
3. A clean owner colony reports 0 cleared.
4. A colony with a powered track between stations, a passage, a hub and a tunnel end reports
   0 cleared, and power stays connected.

## Scope

- **In:** the electricity connection grid on load, plus reconnecting gridless electricity objects.
- **Out:** water, the connect-path guard, the seed's origin, and track object leftovers
  (`Fix_TrackSalvageWipe` owns those). Report findings outside scope; do not edit for them.

## Stops (report instead of continuing)

1. The predicate reads nonzero on a clean colony, or it would clear a cell that a shipped object
   legitimately claims and cannot be kept by the shape rule.
2. Reconnection cannot be made safe without patching the connect path, which is outside the ruling.
3. FIX_POLICY blocks the load-time write in a way the ruling did not anticipate.

## Working rules

- Use the todo tool before any write, with one item per commit-and-verify unit and one item in
  progress.
- Start with `git log --oneline -3` and `git pull`. Peers move HEAD.
- Commit with a pathspec; run doccheck to GREEN.
- Skills: `smr-bug-library`, and `doc-editing` for the C119 update.
- House rules: `CLAUDE.md`. Code rules: `docs/agent/FIX_POLICY.md`. Process:
  `docs/agent/WORKFLOW.md`.
- If you run unattended, your result is audited on a different owner-selected model before it
  enters the record.

**Claim limits:**

- Do not claim the fix prevents stale cells. It removes them at load; mid-session spread continues
  until the next load (ruled acceptable).
- Do not claim C119's origin is fixed.
