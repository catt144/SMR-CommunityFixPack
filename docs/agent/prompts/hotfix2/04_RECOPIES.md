# 04 · The re-copies — five modules that take a 1.1.0 body

Chain: `prompts/hotfix2/README.md` (its binding rules are yours). Runs after 02.
Independent of 03 — either order.

⛔ **This is the highest-risk prompt in the chain, and the risk has a name.**
Every module here replaces a game function with a copied body. F114 shipped
exactly this way: a 1.0.7 body copied into the pack, the game rewrote the
function under it, and every instrument the project owned said OK — the name
sweep saw a name, `sigcheck` saw arity, the runtime check saw existence. You now
have `bodycheck.py` (link 01), which is the first instrument that can see this
class. **Use it, and do not treat any other GREEN as a clearance.**

## 0 · Start

`git log --oneline -10` · `git pull` · `ListAgents`. Todo list first, one item
per module — each is its own commit-and-verify unit.

**Read path:** `agent/STATE.md` · `VANILLA_FIX_QA.md` §0.5 and Reader A's rows
F-6…F-10 (**the shapes are pinned there; a departure must say why**) ·
`PACK_1_1_0_REVERIFICATION.md` §1a · `agent/FIX_POLICY.md` §1.4b · `bugs/F114.md`
and `bugs/F115.md` (how this goes wrong) · `docs/PLAYTEST_CHECKLIST.md` items
109, 115, 118 · your inbox — **01's Job D answer is your branch-guard design,
read it verbatim before writing any gate.**

## ⛔ 1 · Group C is BLOCKED on the owner

**B (F-6, F-7) is unblocked — start there.**

**C (F-8, F-9, F-10) needs a ruling** because taking them up partly reverts ck109
("gate, not repair" for F-8). All three defects ARE still shipped in 1.1.0; the
gates only remove our code from the path. If unruled, do B, route C, and say so.

## 2 · Group B — unblocked

### F-7 `RocketDroneChurn` — one clause
`UpdateCargoResourceRequests` still brackets with unconditional
`Disconnect`/`Connect` (`CargoTransporterNew.lua:1431-1433`, `:1460-1462`), so
F50 persists. One line changed inside the loop:
`additional_amount = is_refuel_resource and not self.refuel_disabled and
self:GetFuelResourceRequest()` (`:1442`). `refuel_disabled` is a new player
toggle (`UniversalRocket.lua:70`, `:3320`); our copy lacks the clause.
⇒ **re-copy the 1.1.0 body carrying `not self.refuel_disabled`.**

### F-6 `PayloadTemplateRefill` — three reverts to avoid
The refill is unchanged (`CargoRequestNew.lua:221-234`), so F70 persists. Our
copy would revert three 1.1.0 changes:
1. `resolve_loc_cargo_template` gained a **tutorial branch** (`:183-189`,
   `AsteroidTutorialExpectedCargo`) and a `CmdLoad` exemption for destination
   picks (`:174`);
2. `RetrieveRequests` reads `prev_flight_data` and ignores stored cargo on a
   destination pick (`:215-217`);
3. the automode branch nil-guards `cargo_items[id]` (`:199-213`).

**Shape, pinned by the QA:** gate as `not from_destination_pick and
transporter.SMRFixPack_payload_set`; ⛔ **the tutorial return (`:183-189`) must
precede the gate** so rocket 2 is still pre-filled; ⛔ **stamp the flag on the
CONFIRMED path** (`:376-379`, `SetCommand("CmdLoad")`), **not** on `Apply` entry
— `Apply` is now an async prompt (`:368-385`) and our pre-wrapper would suppress
the template even when the player cancels (`CancelFlight`, `:382`).

## 3 · Group C — only once ruled

### F-8 `LandscapeUnitFilter`
Body still passes `callback` at `Landscaping.lua:522` while `filter_embark`
(`:516-521`) is unused — the sibling `LandscapeForEachStockpile` passes its
filter (`:503`). Signature is now `(map, mark, callback, ...)` reading
`map.Landscapes[mark]` (`:509-510`; `MapVar("Landscapes", {})` `:21`).
⇒ repair the body on the new signature, passing `filter_embark`.
⚠️ **Reach is now Clear-Waste-Rock sites only** (`ClearWasteRockConstructionSite
.lua:79-85`); `LandscapeConstructionSite` no longer defines `GetUnitsUnderneath`.
⛔ Half-baked if the repair re-pins the old signature or the bare `Landscapes`
global. **Keep the F115 gate** — it is correct and measured, and the `sigcheck`
MISMATCH there is CORRECT because the body is deliberately untouched.

### F-9 `VacuumWalks`
The defect line is byte-for-byte the same (`Colonist.lua:1903`), but everything
around it was rewritten: slot reservation (`:1894-1896`, `:1920-1926`,
`:1943-1949`, `:1972-1978`), `DiscardTransportTicket` (`:1918`), the `-1`
passage-only convention → `max_int` (`:1904-1907`), a `transport_task.shuttle`
guard (`:1898`), `HasShuttleLandingSlots`/`IsSameMap` (`:1932-1957`), a new
`src_dome` search (`:1959-1968`). Our copy has none of it.
⇒ **re-copy the 1.1.0 body with `min_dist = 0` in vacuum; read `g_Consts` at
call time** (the consts moved from `const.`, which is why the module is
inactive-by-accident today).
⛔ **NEVER a distance pre-wrapper.** `transport_mode_dist` also drives `:1914`
(walk-vs-shuttle) and the `-1` branch at `:1904` — inflating it changes both.
Make the gate deliberate rather than accidental.

### F-10 `TrainCargoDumping`
`UnloadAll` (`Train.lua:779-805`) gained nil-guards (`:785`, `:794-795`) and a
**BlackCube hook (`:800-802`)**, but still has no enabled check. `Station` is now
a `MultiResourceDepotBase` (`Station.lua:48-56`); `IsResourceEnabled` =
`IsStoring` = demand exists and not `rfSuspended` (`MultiResourceDepot.lua
:242-247`).
⇒ **re-copy `:779-805` with `station:IsResourceEnabled(res)`; carry the BlackCube
hook.** ⛔ Half-baked if the copy drops `:800-802`. Keep the F114 gate for the
next change.
⚠️ Whether a suspended request still reports a positive `GetTargetAmount` is
C-side and unread — "plausibly persists", not established. Say so.

## 4 · Non-negotiable for every module here

1. **`SRC:` / `DEFECT:` manifest lines** per 01's spec, so the next game update
   is a tool run and not a week. Stamp after the edit.
2. **`bodycheck.py` GREEN** on the module, and you saw it go RED on a
   deliberately wrong pin at least once. An instrument you never watched fail is
   not an instrument.
3. ⛔ **Declines on 1.0.7.** These modules carry a 1.1.0 body; applied over a
   1.0.7 function that is the F114 failure in reverse, and nothing stops this
   build reaching a 1.0.7 player (ck118). Use 01's Job D design — the
   per-module probe, **never a game-version detector**.
4. **A parse sweep** of every touched `.lua`, with `Mars.exe` closed.

## 5 · Scope fence

**In:** the five modules, their headers/manifests/gates, their bug entries, their
drafted patch-note lines. **Out:** `items.lua`, `metadata.lua`, store text,
`00_Core.lua`, the KEEP set, the harms (03), F116 (K-11 — **do not re-derive it**;
its two open divergences are ck111 and are the owner's).
Found something out of fence? **File it, do not fix it.**

## 6 · Stop conditions

- Group C unruled ⇒ do B, route C, stop cleanly.
- A 1.1.0 body cannot be copied without also importing a change you cannot
  justify ⇒ **STOP AND ASK.** A re-copy you do not fully understand is the F114
  shape with a new date on it.
- A module cannot be made to decline on 1.0.7 without a version check ⇒ **STOP.**
  Do not build the detector; report it.
- `bodycheck.py` disagrees with your read of the body ⇒ believe the tool until
  you have proven it wrong, and record which of you was right for 99.

## 7 · What may NOT be claimed

- ⛔ **Not "tested".** Nothing here has run in a game. Trains and landscaping
  have never been exercised on 1.1.0 at all — the 09-08 boot was menu-only.
- ⛔ Not "matches vanilla" unless `bodycheck.py` says the pin matches; your
  reading of a diff is not the control.
- ⛔ Not "F-10 is fixed" — its premise rests on an unread C-side function.
- ⛔ Not "the gates are unnecessary now". They are measured and correct; you are
  adding repairs beside them, not replacing them.

## 8 · Close-out

Green gates. Your outbox to `06` and `99` must name, per module: the 1.1.0 lines
you copied, what you deliberately did NOT carry over, the gate's decline
condition, and **what has not been exercised in play** — which for these five is
everything. Route the in-play controls (first train leaves its platform, a
landscaping site progresses) to the checklist; they have been owed since
hotfix 1. Strike your README row, `git rm` this file, commit together, push.

## Notes from upstream

*(From the authoring session, `smr-bugfixpack-91`, 2026-09-08.)*

- ⚠️ From `smr-bugfixpack-a5`, which ran the F116 leg: F116 was filed off a
  keyword grep, **two of its four claims did not survive a real structural
  diff**, and a FIFTH divergence nobody had listed only appeared when the two
  bodies were diffed properly. `sigcheck.py` rated that module OK throughout.
  If your method for any module here is a grep rather than a body diff, it will
  inherit exactly that failure.
- The owner ruled ck109 as "gate, not repair" for F-8 on 2026-09-08 and then said
  "take up everything we can". Those pull in opposite directions, which is why
  group C is an explicit ask rather than an inference.
