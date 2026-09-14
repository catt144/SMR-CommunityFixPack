# SMRTK 03B — cross-vendor judge of the 03A fan-out

2026-09-13, Claude (Opus), fresh context. Judged at pack `2be7c73`, TestKit
`cee5bab` (03A's stated final). One label fix applied here takes TestKit to
`87f3130`. **Verdict: PASS WITH FIXES.** No gate differed from 03A's pasted
output; no invariant is breached; two findings are routed, one fix applied.

⛔ Nothing in this report is a play claim. No game was launched (`tasklist`
below). 08 remains the first sitting for every page, stamp and native effect.

## Verdict

**PASS WITH FIXES.** 03A's five payloads plus the shared core/panel extensions
hold against every gate I could re-run and every route I opened. The build is
honest about what it did not measure, its DEPARTURES are real departures with
reasons that survive checking, and its DRIFT section is unusually complete —
including corrections that made 03A look worse, which is the right instinct.

No RE-FIRE. No payload failed a gate, and neither finding below is a defect in
a route, a taint breach or an idle patch — the class of thing that would send a
payload back.

## Disagreements with 03A — first

### D1. The Selected section replaces vanilla's per-object cheats with 22 of 106 members, and the report never says so

**Claim.** `73_SMRTK_Infopanel.lua:6-23` is a fixed table of 16 method names
plus `CheatUpgrade1..6` — 22 distinct member names. Vanilla's section does not
use a list: `InfopanelObj:CreateCheatActions` (`Lua/X/Infopanel.lua:22-40`)
walks the object's metatable chain and offers **every** member whose name
starts with `Cheat` or `AsyncCheat`. Measured on build 24995074: **94 distinct
`Cheat*` object methods and 12 `AsyncCheat*`**, 106 total. P2 covers 22.
**84 member names the vanilla section would offer are unreachable in the
toolkit**, and `AsyncCheat*` is absent as a category.

**Why this is a finding and not a departure.** The P2 brief named exactly this
list, so P2 conformed — I am not judging it on conformance. The finding is that
neither DEPARTURES nor SUGGESTIONS states the coverage ratio, states that
vanilla enumerates dynamically, or mentions `AsyncCheat*` at all — even though
`SMRTK_UI_HOOKS.md:108` records "AsyncCheat methods already avoid taint", so the
category was known and dropped silently. The report's only trace is
`P2 CATALOG: 21 selected leaf actions` with nothing to compare it against.

**Why it matters more than a count.** The owner's purpose is to *replace* the
built-in menu, and the toolkit deliberately never sets
`config.BuildingInfopanelCheats`, so there is no fallback to the other 84. The
sharpest case is a selected **Colonist**:

- `CObject:CheatDelete()` is `DoneObject(self)` (`_cobject.lua:1591-1593`) — a
  universal member, so it is the *one* action of the 22 that a Colonist matches.
- `Colonist:CheatKill()` (`Lua/Units/Colonist.lua:5144`) — the modelled
  removal — is **not** in the list. Nor is `Drone:CheatDespawn()`
  (`Lua/Drone.lua:2989`) for a drone.

So on a colonist the Tool Kit section offers Delete (raw `DoneObject`) plus
Dump/Pin, and hides the safe specific route while exposing the blunt universal
one. Vanilla's section on the same colonist offers Kill, Starve, MakeRenegade,
Age1Year, AddTouristTrait, MakeEarthsick, Delete and the inspection tools.
(P1's World page does serve colonists' traits, so they are not wholly unserved.)

**The safe route already exists and is cheap.** Vanilla's enumeration is not the
tainting part — line **:49** is (`NetSyncEvent("ObjCheat", self, ...)`). P2
already replaces that line with `obj[method](obj)` at `73:72`. Enumerating the
chain exactly as `Infopanel.lua:24-36` does and dispatching through P2's
existing untainted path crosses no invariant: it adds no wrapper, no sync call,
and every member reached is a leaf body of the kind `EF-095` clears.

**Recommendation (routed to ck175, item 1 below).** Keep the curated 22 as a
labelled top group — they carry guards the generic path cannot (busy-depot
refusal at `73:64-65`, before/after depot reads, the honest Delete caveat) — and
add a dynamically enumerated "More" group for the remaining members, dispatched
through the same `T.Run` leaf path with a generic result record. This is a
build, so it is outside my fence; it is the owner's scope call whether it lands
before 08 or after.

### D2. The legacy `00_TestCore` bootstrap calls the one function rule 10 forbids

03A handed me this ("03B owns the suggested legacy 00 bootstrap retirement").

**Claim.** `00_TestCore.lua:529` runs `SMRTest.EnableConsole()` unconditionally
at mod load, and `:519` calls `ConsoleSetEnabled(true)`, falling back to a plain
`ConsoleEnabled` assignment only if that raises. README rule 10 says the
opposite in as many words: *"Set `ConsoleEnabled = true` directly (not
`ConsoleSetEnabled`, which also shows the on-screen log — `EF-097`)"*.
`ConsoleSetEnabled` calls `ShowConsoleLog(enabled)` (`uiConsole.lua:459-463`),
so every TestKit boot forces the on-screen overlay that `70_SMRTK_Core.lua:354`
carefully avoids by plain assignment. 00 loads first, so 00 wins.

**My verdict: do NOT retire it — invert it.** Retirement is the wrong repair.
The console is how an operator runs `SMRTest.Run`, and 00's comment records a
real 2026-07-25 session where the Enter binding was dead, which is why both
fallbacks exist. The correct one-line-shaped change is to **try plain
assignment first and keep `ConsoleSetEnabled` as the fallback** — today's order
reversed. That keeps both paths, drops the forced overlay, and aligns 00 with
rule 10.

**I did not apply it.** It is pre-existing probe infrastructure outside the five
payload files and outside my scope fence. Routed to 07/99 with the exact edit.

**One thing 03A did not claim but 08 must not:** this bootstrap makes a *passive*
console observation attribute nothing to the toolkit's arm. That confounder is
already handled — 02 eliminated it with a discriminating A/B (`ConsoleEnabled`
false → rebuild → `console=false`; arm → `console=true`;
`SMRTK_SKELETON_SITTING.md:416-439`) and the toolkit keeps `console_control` for
it. So 08 must use `console_control`, not "the console opened". Noted for 07.

## Agreements — job by job

### 1. Every gate re-run on HEAD, by me

All output matched 03A's pasted output. I ran 03A's harness **and** the raw
greps independently, because the harness is 03A's own instrument.

| gate | my result |
|---|---|
| `SMRTK_FANOUT_GATES.py --ordered --presence` | `COORDINATOR GATES: PASS`; HEAD pack `2be7c73` testkit `cee5bab` |
| parse, all 9 SMRTK files + 80 + 90 | 0 errors [Lua 5.5] |
| `parsecheck.py --dir ../SMR-BugFixPack-TestKit/Code` | 34 files, 0 errors |
| **rule 6 raw grep** (`NetSyncEvent\|LogCheatUsed` on `7*_SMRTK*` + `80`) | **0 lines** |
| **rule 6 presence side** (`CheatDef.lua`) | **26 lines**; of which **13** are real `NetSyncEvent("` calls |
| **rule 7 raw grep** (`^\s*print(`) | **0 lines** |
| `def:run(` anywhere in toolkit | 0 lines |
| H-10, checked against `metadata.lua` directly | all 9 SMRTK files listed (lines 27-35) |
| `doccheck.py` | **GREEN** |
| the five payload smokes + `FANOUT_MERGE --selftest` | all PASS, 3 editor falsifiers RED as required |

I re-derived the two README derived-facts rather than inherit them:
`grep -rn LogCheatUsed …/ModTools/Src | wc -l` → **4**; `NetSyncEvent("` calls
in `CheatDef.lua` → **13**. Both hold.

⚠️ **doccheck WARNs, verbatim, per rule 19** — all pre-existing, none from 03A:

```
MARKER INTEGRITY: 86 on disk, 86 parsed; WARN
  warn duplicate ck:144 at lines 2562, 2636 (agree)
SKILLS: smr-bug-library 3622 B / smr-orientation 3248 B  ⚠ over the 3072 B target
ALIASCHECK: 34 file(s), 38 SMRTest member(s) derived, 9 finding(s)  (report-only)
  WARN UNKNOWN 76_SMRTK_Kit.lua  SMRTest.order/.probes/.last is defined by no kit file  (×9)
```

plus 13 frozen index-row/entry status warns (C16/C17/C34/C35/C37/C38/C39/C43/
C49/C50/C51/C52, F100). The nine ALIASCHECK UNKNOWNs are 03A's declared false
positives — `00_TestCore.lua:19-21` does declare `order`/`probes`/`last`; I
opened those lines and confirm the checker is wrong, not the code.

⛔ **One README defect found while re-running.** The "Derived facts" table's
re-check recipe reads `grep -c "NetSyncEvent" CheatDef.lua → 13`. It returns
**26** — 13 calls plus 13 `Comment =` lines that name the function. The recipe
is vacuous as a control: it would pass on a file with 26 comments and no calls.
Rule 6's own text ("returns 13+") is fine. Fix the table's recipe to
`grep -c 'NetSyncEvent("'`. Routed to 07.

### 2. Routes sampled against the facts

**P1 — all 54 registered actions opened.** Every one dispatches a leaf global
or an object method; **none** calls `def:run()` on any of `EF-098`'s 13, and
none goes through a wrapper. I extracted each leaf's body from source and
grepped it for `NetSyncEvent`/`LogCheatUsed`:

`CheatStopDisaster` · `CheatDustStorm` · `CheatDustDevil` · `CheatColdWave` ·
`CheatTriggerMarsquake` · `CheatRainsDisaster` · `CheatMeteors` ·
`CheatTriggerUndergroundCaveIn` · `CheatTriggerUndergroundMarsquake` ·
`CheatCompleteAllConstructions` · `CheatCompleteAllWiresAndPipes` ·
`CheatSpawnNColonists` · `CheatGenerateApplicants` · `CheatAddFunding` ·
`CheatUnlockAllBuildings` (both definitions) · `OpenAllDomes` · `CloseAllDomes` ·
`UnpinAll` · `SetGameSpeed` · `TechPointObj:GainTechPoint` · `Player:UIResearch` ·
`Colonist:AddTrait` · `Colonist:RemoveTrait` · `UniversalRocketBase:AddFlightTime` ·
`ReopenXBuildMenu` · `Building:CheatCleanAndFix` ·
`RequiresMaintenance:SetMalfunction` · `UniversalStorageDepotBase:CheatFill` ·
`MechanizedDepot:CheatFill` — **all CLEAN**.

The `MapSettings` group ids P1 passes (`DustStorm`, `DustDevils`, `ColdWave`,
`Marsquake`, `RainsDisaster`, `Meteor`) match vanilla's own
(`CheatDef.lua:153-293`) exactly, and each leaf's arity matches its definition.
⭐ The meteor route takes its position from an armed **map click**
(`72:70`, `event.pos`), not `GetCameraLookAtPassable()` — `EF-098`'s first
defect is designed out, not inherited.

**P2 — all 21 leaf actions + 4 companions opened.** Every one of the 22 method
names resolves to a real definition, and every definition's body is clean:
`CheatFill` (15 defs) · `CheatEmpty` (17) · `CheatDelete` (4) · `CheatDestroy` ·
`CheatCleanAndFix` · `CheatMalfunction` (3) · `CheatAddPrefab` · `CheatAddDust` ·
`CheatAddDustRC` · `CheatAddMaintenancePnts` · `CheatSpawnWorker` ·
`CheatSpawnVisitor` · `CheatSpawnChild` · `CheatSpawnColonist` (2) ·
`CheatSpawnDrone` (2) · `CheatSpawnShuttle` · `CheatUpgrade1..6`
(`Building.lua:1949-1953`, a loop over `const.Building.MaxUpgrades` = **6**,
body `self:ApplyUpgrade(i, true)`). Dispatch is `obj[method](obj)` at `73:72` —
the leaf, never `NetSyncEvents.ObjCheat`.

**P3–P5 — 29 actions opened, against a required minimum of 10.**
P3: `pin_A/B/C`, `note`, `screenshot_mark`, `trigger_sol`, `trigger_error`,
`trigger_field`, `trigger_rocket`, `watch_selected_field`.
P4: `save_A`, `load_A`, `load_override_A`, `run_all`, `run_probe`,
`console_open`, `fingerprint`, `dump_selected`, `snapshot`, `watch_field`,
`logger_*`.
P5: `layout_capture_selected`, `layout_plan`, `layout_stamp`, `layout_target`,
`layout_apply_upgrades`, `layout_fill_storages`, `layout_spawn_colonists`,
`layout_funding`.

Spot checks that could have gone wrong and did not:

- `SaveGame(display_name, params)` returns `err, name, meta`
  (`Savegame.lua:1069-1090`) — P4's `local err, saved_name, metadata = …` matches.
  `LoadGame` returns err (`:1092`). `Savegame.Load` exists (`:933`).
  P4's refusal to use `LoadMetadataCallback` because it calls `DoneGame()` is
  correct and load-bearing.
- `PlaceCableLine`/`PlacePipeLine` signatures are 14 parameters
  (`ElectricityGrid.lua:661`, `LifeSupportGrid.lua:940`); P5 passes 14, with
  `test=false` in the 6th slot. The return is `true, { … data = data … }`
  (`ElectricityGrid.lua:1112-1119`) — P5's `result.data[i]`, `cell.q/.r`,
  `cell[edge.k]` match the real shape. `for i = 0, edge.steps` honours
  `EF-099`'s endpoint correction.
- P5 completes its **own** sites with `site:Complete("quick_build")`
  (`ConstructionSite.lua:1675`), never `CheatCompleteAllConstructions()` — the
  bounded-completion departure is real, and `EF-099`'s amendment demanded it.
- `GenerateScreenshotFilename` (`gamelib.lua:330`) and `PropObjHasMember` (a
  native, used throughout vanilla) are both reachable — neither is blacklisted.
- All 23 messages the toolkit hooks have real senders and none is in
  `ModMsgBlacklist`. `OnLuaError` has no Lua sender but three vanilla listeners
  (`Gossip.lua:53`, `Mod.lua:3019`, `Savegame.lua:1608`) — engine-dispatched, as
  `EF-096` says.

⛔ **A false alarm I ran down, recorded so nobody repeats it.** `75_SMRTK_Saves.lua:6`
calls `os.time()` at load, and `os = true` **is** in `ModEnvBlacklist`
(`Mod.lua:1438`, inside the 1280-1441 table). That reads like a load-time crash
killing the whole Saves page. It is not: `LuaModEnv` rawsets
`env.os = { time = os.time }` at `Mod.lua:1618`, before attaching the metatable,
so `os.time` is deliberately exposed and nothing else on `os` is. **No finding.**
Two fact corrections fall out of it, routed below.

### 3. The shared techniques were actually shared

Read `SMRTK_UI_HOOKS.md` §1/§2/§3 against what P2 and P3 built. **No divergence.**

- **§1 infopanel injection.** P2's `section_attach` (`73:154-182`) is the
  decision line for line: `OnMsg.DialogOpen`, `IsKindOf(dlg,"InfopanelDlg")`,
  `named_child(dlg,"idContent")`, idempotent on `idSMRTKSection`,
  `ResolvePropObj(dlg.context)`, `PropObjHasMember` via `member()`, placed at
  `idSectionCheats + 1` when present and appended otherwise, and the declared
  fallback is the shared `T.Page("Selected")` — not a third route. Rejected
  route 1 (reusing `sectionCheats`) and 2 (patching `InfopanelDlg:Open`) are
  both genuinely absent from the tree.
- **§2 armed clicks.** Exactly **one** click service exists:
  `T.AcquireClick`/`T.ReleaseClick` in the core (`70:393-424`), using a
  `TerminalTarget` at priority 10001 added on arm and removed on disarm.
  `terminal.AddTarget` appears **only** at `70:416`. Its three consumers —
  P1 meteors (`72:78`), P3 slots (`74:42`), P5 rectangle/target (`77:545`) — all
  go through it. No payload built a second input route.
- **§3 dock + side panel.** P2 owns both (`dock_attach` at `73:319`,
  `XPopupMenu` + toolkit `XAction`s at `73:252-301`), the coordinator owns the
  panel adaptation. Every X class used exists: `InfopanelSection`,
  `XSleekScroll`, `XScrollArea`, `XActionsHost`, `XPopupMenu`, `XCombo`,
  `XTextEditor`, `TerminalTarget`.

### 4. The idle invariant, enumerated on the desk

I enumerated every write to a real global across the five files plus core,
panel and `80`. **Exactly three sites, in two toggles:**

| site | global | toggle | uninstall |
|---|---|---|---|
| `70:297` | `print` | `print_tee` arm `70:277` | disarm `70:299-301`, restores captured original |
| `72:160` | 7 disaster functions | `quiet` arm `72:128` | disarm `72:163-169`, restores **only if the wrapper is still ours** |
| `72:166` | (the restore itself) | — | — |

`rawset(_G` appears nowhere. Every other `X = function` in the sweep is a field
on a toolkit-owned object (`OnPress`, `def.run`, `target.OnMouseButtonDown`) or
a `T.*` table — not a vanilla patch. **Rule 9 holds: zero patched vanilla
functions while idle.** Both toggles are off by default and both are cleaned on
the lifecycle messages.

Rule 10 also holds, measured across the whole TestKit: **no** `Platform.cheats`,
**no** `AreCheatsEnabled()` dependency, **no** `config.BuildingInfopanelCheats`
write anywhere. Rule 11 holds: 03A's TestKit diff is the 9 SMRTK files + 7 lines
in `90_Loggers.lua` + `Layouts/README.md` + `metadata.lua`; the pack's `Code/`,
`items.lua`, `metadata.lua` and `version` are untouched.

⚠️ **One asymmetry worth 99's eye, not a finding.** `quiet` guards its restore
(`if rawget(_G, route.name) == route.wrapper`); `print_tee` restores
unconditionally. They patch disjoint globals so they cannot collide with each
other. The real adjacency is `quiet` vs `90_Loggers`' `DustDevils` logger — both
wrap `_G.GenerateDustDevilIn`. 03A guarded **both toolkit directions**: `quiet`
refuses to arm while any logger is on (`72:130-138`), and Kit's `logger_*`
refuses while `quiet` is armed (`76:117`). The unguarded path is a bare console
`SMRTest.Log.DustDevils(true)` while quiet is armed, which would strand quiet's
wrapper — 90's own toggle predates smrtk and has no quiet check. 03A's claim
("Quiet and any native/toolkit logger refuse nesting") is accurate for the
toolkit surfaces and I am not calling it overstated; the console path is a
documentation item for 07.

### 5. Stubs and cross-ids

**All resolve; nothing owed.** I wrote an independent resolver over every
literal `T.Run/Arm/Disarm/Fire("id")` and `T.actions|armed|triggers|fires["id"]`
reference in the nine files: 80 static ids registered, **zero** referenced-but-
unregistered. The dynamic families (`selected_*`, `logger_*`, `spawn_*`,
`meteor_*`, `slot_*`) appear in the merge script's live registry dump. The
cross-payload contracts hold: P2's companions `dump_selected` (P4) and
`pin_A/B/C` (P3) are registered; P4's `watch_field` creates P3's
`watch_selected_field` disarmed; P5's follow-ups delegate to P1's
`fill_storages`/`spawn_colonists`/`funding`; P2's dock "Sitting" group resolves
all 8 of `mark`/`copy`/`flush`/`clear`/`taint_read`/`eligibility` (core) and
`pause`/`stop_disaster` (P1). No "(not built)" label can render in the merged
build.

### 6. The two questions 03A handed me

- **Legacy 00 console bootstrap** — answered in D2: invert it, do not retire it.
- **P5's synthetic-plan second-unit gate** — **accepted.** The brief's gate
  wanted three native stamps; 03A substituted three synthetic clean plans. That
  substitution was *forced*, not chosen: no link before 08 may run the game
  (rule 17, and 08 is the first sitting), so a native-stamp gate was
  unsatisfiable inside 03A's fence. The three plans do exercise the planner and
  are explicitly "zero mutation" in `SMRTK_P5_DESK.py`. The gate is **not
  waived** — it moves to 08 with the five named witnesses 03A already lists
  (native fit, GameInit, dome membership, connected grids, upgrade state). 07
  must write those into the sitting script as a required leg, not an optional one.

## Fixes applied

**One**, in scope (a label), TestKit `87f3130`:

- `73_SMRTK_Infopanel.lua:123` — the Selected caveat read *"Delete uses class
  removal (tracks may demolish; rubble clears)"*, which describes buildings
  only. On a Colonist or Drone the matched member is `CObject:CheatDelete` =
  `DoneObject(self)`. Now: *"Delete uses class removal (units are removed
  outright, not killed; tracks may demolish; rubble clears)."* Re-gated after:
  parse 0 errors, rule 6 = 0, rule 7 = 0, P2 smoke PASS.

Neither D1 nor D2 is applied: D1 is a build and D2 is pre-existing infrastructure
outside the five files. Both are outside my fence and both are routed.

## For 07

1. **Document the Selected section's coverage honestly** — 22 of 106
   `Cheat*`/`AsyncCheat*` member names, and say the vanilla section is not
   reachable while the toolkit is loaded (`config.BuildingInfopanelCheats`
   is never set). Do not write "replaces the cheat menu" without that
   qualifier until ck175 item 1 is ruled.
2. **08 must prove the console with `console_control`**, never with "the console
   opened" — `00_TestCore` arms it at load, so the passive observation
   attributes nothing. 02's discriminating A/B is the pattern.
3. **The 00 bootstrap edit** (D2): plain `ConsoleEnabled = true` first,
   `ConsoleSetEnabled` as fallback. One line, `Mars.exe` closed, then re-gate.
4. **P5's deferred stamp gate is a required 08 leg**, with the five witnesses named.
5. **README derived-facts recipe fix**: `grep -c 'NetSyncEvent("'` (13), not
   `grep -c "NetSyncEvent"` (26).
6. Two fact corrections for `EF-096`, both small and both mine:
   `ModEnvBlacklist` spans `Mod.lua:1280-1441`, not 1280-1416; and `os` is in
   that blacklist **but** `LuaModEnv` rawsets `env.os = { time = os.time }`
   (`Mod.lua:1618`), so `os.time` is available to a mod and nothing else on `os`
   is. Worth recording — the naive read of the blacklist says the opposite.
7. Buttons, registries and the slot template are 03A's outbox, unchanged by me.

## For 99 — the cross-vendor split to adjudicate

- **D1 is my one substantive disagreement.** 03A built to the brief; I say the
  brief's list is a quarter of the surface it replaces and the report should
  have said so. 99 owns whether "conformed to the brief" or "unstated gap in the
  headline deliverable" is the right frame. My evidence: 106 measured member
  names, the Colonist Delete/Kill asymmetry, and `UI_HOOKS.md:108` showing the
  `AsyncCheat*` category was known.
- **D2** — 03A asked for a retirement ruling; I ruled invert, not retire, and
  gave the reason (both fallbacks exist because a binding really did die once).
- **Everything else in 03A's report that I could check, checked out**, including
  the parts that made 03A look bad. Its DRIFT is more complete than its summary
  needed it to be.
- **Instrument note.** 03A's gate/smoke scripts are its own; I re-ran the raw
  greps and re-derived both README facts by hand rather than inherit the
  harness's word. They agreed. The harness is not falsified, but it has never
  been falsified *against a known-bad tree* either — if 99 wants one cheap
  control, point `SMRTK_FANOUT_GATES.py` at a scratch copy with one
  `NetSyncEvent` inserted and require it to go RED.
- **Cosmetic drift:** 03A's close-out commit `b4aadb4` carries a UTF-8 BOM in
  its subject line (`﻿SMRTK 03A: record…`). PowerShell 5.1 encoding, the known rig hazard.
- No game ran here: `tasklist /FI "IMAGENAME eq Mars.exe"` →
  `INFO: No tasks are running which match the specified criteria.`

## What this judgment may NOT be read as

That any page works in play — 08 owns that. That no-taint holds at runtime for
the new routes — every route above is a **source read**; 02 measured the
premise, not these 100+ actions. That the desk smokes model the engine: they use
fake X classes and fake services, and 03A says so. That D1's absence of a finding
elsewhere means I opened everything — I opened all of P1 and P2 and 29 of
P3–P5, and I did not read the panel's rendering path or `91_Stress.lua`.
