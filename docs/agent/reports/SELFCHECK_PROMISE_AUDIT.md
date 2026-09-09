# SELFCHECK PROMISE AUDIT — can the store's self-check sentence be made literally true?

**VERDICT: YES BUT SCOPED.** The sentence can be made true for *the code the fix
patches*: the sandbox leaves `string.dump` reachable, so every module can read
the shipped target's compiled signature at boot with no per-module authoring
(this alone would have caught F115 with zero false positives on the 1.1.0 patch)
and its compiled body against a pin (this would have caught F114 and six of the
other seven surviving FIX rows). It cannot be made true for *what the fix was
written for* in the sentence's broad reading: a patch that changes the meaning
of code around an untouched target — measured here on `StaleReservations`, whose
two pinned bodies are byte-identical on 1.0.7 and 1.1.0 — is invisible to any
runtime check by construction, and hand-written behaviour probes only test the
axes their author already knew about (F114's axis was unknown to its author).
So the honest sentence is "stands down by itself if an official patch changes
the code it patches", built on a universal fingerprint, not on 44 probes. The
cost is real and is stated in §5: on a patch the size of 1.1.0 a body
fingerprint would have stood down 24 modules on day one, 17 of them working.

> ⚠️ **CROSS-CHECKED 2026-09-09 by Codex** (`reports/SELFCHECK_PROMISE_CROSSCHECK_CODEX.md`,
> commit `397bf15`): verdict shape upheld (PARTLY AGREE), **four supporting
> claims REFUTED and verified refuted by this session** — the F-2 ceiling, the
> F114 probe impossibility, the ≤17 false-stand-down bound, and the act1 blame
> line's explanation — plus one under-costing and one gap in the sentence's
> third clause. **§10 at the end records every correction; read it before
> citing anything above.** The body is left as written so the record shows
> what was claimed and why.

Audited 2026-09-09 by `smr-bugfixpack-db` under `prompts/SELFCHECK_PROMISE_AUDIT.md`.
Tree read at HEAD `3fdde36`, clean, `git pull` up to date. Game trees: 1.1.0 at
`A:\SteamLibrary\steamapps\common\Project Spark\ModTools\Src` (mtime 2026-09-08),
1.0.7 archived at `C:\Dev\SMR-SrcArchive\1.0.7.396349\Src`. ⛔ Nothing was run in
a game. Every "measured" below is one of: a tool run on both trees, a string
read of `Mars.exe`, an archived log, or the engine's own sandbox Lua executed on
a desk Lua 5.3 (`lupa 2.8`, this rig). Each is labelled. ⛔ No code, no store
text, no status moved; `Code/`, `metadata.lua`, `bugs/`, `STATE.md` and the
checklist are untouched. Proposed checklist and STATE text is in §9 for the
chain's owners to land.

**Size decision (brief §3).** One session, not a chain. The sandbox question
turned out to be desk-measurable (§4), and the 44-module classification was
fanned out to four read-only subagents under one written brief (§3 says what I
spot-checked myself). Checkpoints were committed after §2, §4, §7 and §3.

**Framing correction, from the prompt's own author (peer message 2026-09-09).**
ck112 is recorded in commit `e1095d5` as "DEFERRED". It was not deferred: the
owner rejected both recorded options and commissioned this audit as a third
route. This report cites it that way.

---

## 1 · The coverage table, re-derived

Counted by script over `Code/*.lua` (comment lines stripped first; a `{ probe =`
inside a helper counts, a commented-out one does not), then reconciled by hand
against the four modules the script found with no `Require` block at all.

| strongest check a module carries | modules | what it proves at boot |
|---|---|---|
| `probe` (behaviour on a stub) | **5** | the shipped body behaves as the module assumes *on the probed axis* |
| `test` only (a content or shape verdict, no probe) | **4** | a discriminating shape or datum is present |
| existence only (`global` / `class` / `path`) via `Require` | **31** | the target EXISTS |
| existence only, inline `rawget`/`type` with no `Require` block | **3** | the target EXISTS (`ExtenderFlapChurn`, `SequenceLatents`, `ShelterReflex`) |
| `DataPatch` with no `Require` block | **1** | the preset shape the pass reads (`DustSicknessBiorobots`) |
| **total** | **44** | |

Cross-counts: modules carrying at least one `test` = 7, at least one `probe` = 5
(three modules carry both: `LandscapeUnitFilter`, `TrainCargoDumping`,
`VacuumWalks`); modules with NEITHER = 35; `SetGlobal` sites = 5; `DataPatch`
modules = 3 (`SaintBlessing` and `SinkholeIndestructible` also have `Require`).

**Delta against the prompt's seed table**, which its author says came from a
bare `grep` and asked me to treat as a claim: the pack has **44** registered
modules, not 43 (`90_SaveSanitizer` registers like any other, `items.lua`
agrees, doccheck's module-set gate agrees); "39 existence" was 43 minus the
probe count and so double-counted the three probe+test modules — the true
"existence-only" figure is **35 of 44**. A second peer's "probes ship in
exactly two modules" predates link 04b and is stale by three. None of the
deltas changes the verdict's shape: **the promise holds, at best, for 5 of 44.**

What the other instruments cover, for the record (desk-time, players never run
them): `bodycheck.py` 97 manifest rows over 43 stamped modules (2 with no
manifest, 3 `SRC: none`, 1 pinned with no `DEFECT`), `sigcheck.py` 43
replacement sites of which 12 carry no `SRC` pin of their own function.

---

## 2 · §1a — would today's mechanism have caught the two real failures?

"Today's mechanism" is the `probe` form (`00_Core.lua:151-166`): the shipped
function is called on a stub under `pcall`; only literal `true` applies; a throw
is a decline. Probes run inside `apply()`, i.e. at the main menu before any game
is loaded, so a decline always precedes the first in-play call.

### 2a · F115 (`LandscapeUnitFilter`) — the control

**The probe as it ships** (`Fix_LandscapeUnitFilter.lua:150-177`, commit
`799f145`): a stub map whose `Landscapes` table records which key is asked for;
`fn(stub_map, PROBE_MARK, cb)`; `true` iff the key asked was `PROBE_MARK`.

**Would a 1.0.7-era equivalent have declined on 1.1.0 before the throw?** Yes,
and I measured the mechanism rather than reasoning about it. A 1.0.7-shaped
probe calls `fn(PROBE_MARK, cb)`; on the 1.1.0 body that binds `map` to a
string, and `("string").Landscapes` resolves through the string metatable to
`string.Landscapes` = nil, so `nil[mark]` throws — desk Lua 5.3, same shapes:
`attempt to index a nil value (field 'Landscapes')` ⇒ pcall false ⇒ decline.
The reverse direction (the shipped 1.1.0-shaped probe on a 1.0.7 body) also
declines: at the main menu the 1.0.7 GameVar holds `false`, so `false[mark]`
throws (`attempt to index a boolean value`); once a game is loaded the global is
a table, the probe's stub is used as the *key*, nothing is asked, `asked == nil`
⇒ decline. Three-valued as the module header claims.

**What the probe actually detects — verified, not repeated.** The 1.1.0 body
(`Landscaping.lua:509-523`) reads `map.Landscapes[mark]` at `:510` and returns
at `:512` when it is nil. Every line the probe can reach is therefore lines
509–512. The F34(d) defect line — `callback` passed where `filter_embark` was
built, `:523` — is **unreachable on any stub**: reaching it needs a real
landscape object and calls `Landscape_ForEachObject`, which is C. So the probe
detects the **signature change and the storage move**, which shipped together,
and says **nothing about the defect line**. A future patch that keeps
`(map, mark, callback, ...)` and `map.Landscapes[mark]` but rewrites the sweep
passes the probe. That is a correlate, exactly as the prompt feared; the
correlate happens to be the thing that broke this time.

### 2b · F114 (`TrainCargoDumping`) — the harder case

**The probe as it ships** (`Fix_TrainCargoDumping.lua:148-185`, `3d4c933`): a
stub station listing one storable resource with no `demand` entry — the exact
F114 input; `true` iff the shipped body asked for that resource's stored amount,
moved nothing, and replaced `assigned_resources`. On the 1.0.7 body
(`Train.lua:783-803` archived) `station.demand[res]:GetTargetAmount()` indexes
nil and throws ⇒ decline. On 1.1.0 (`:794-795`) the nil-guard yields cap 0 ⇒
`true`. So **today's probe would catch a reversion of the guard.**

**Would an equivalent probe have caught F114 at the time?** No, and this is the
finding that bounds Option 1. A 1.0.7-era author would have had to write a
probe that feeds a storable resource with no demand request and expects the
shipped body to *throw* — but the 1.0.7 author did not know that input could
exist (that a station lists lock-hidden resources with no request is a 1.1.0
fact, `Station.lua:110-111`). A probe tests the assumptions its author holds.
F114 was a change on an axis nobody had a assumption about. Only a check that
sees the body *as a whole* — the desk `bodycheck.py`, or a runtime fingerprint
(§4) — sees an unknown-axis change.

Corollary the owner should hear plainly: **full probe coverage does not deliver
the sentence.** It delivers "stands down if the code stops behaving the way the
fix assumed on the axes we thought of", which is weaker than "if a patch changes
what it was written for" and is not what a player reads.

### 2c · Against the current failures, per instrument

| instrument | F115 (signature) | F114 (body) | when |
|---|---|---|---|
| existence checks (what shipped) | no | no | boot |
| `probe`, as a 1.0.7 author would have written it | **yes** (via the storage correlate) | **no** (unknown axis) | boot |
| `probe`, as it ships now | yes | yes (guard reversion only) | boot |
| runtime arity read (§4, buildable) | **yes** | no | boot |
| runtime body fingerprint (§4, buildable) | yes | **yes** | boot |
| `sigcheck.py` / `bodycheck.py` | yes | yes | desk, after the patch |

---

## 3 · §1b — the 44-module classification

### 3a · Method and provenance

Four read-only subagents, one written brief (the probe contract from
`00_Core.lua:117-141` and `FIX_POLICY` §2a, the two shipping probes as models,
a fixed output format, `NOT OPENED` mandatory where a body was not read).
`Code/` read at `3fdde36`; unchanged through `641613e` (link 06 touched only
`metadata.lua` and docs). Shipped tree: 1.1.0. Each row below is that reader's
verdict; §3d says which I re-derived myself. Check counts: E = existence forms,
T = `test`, P = `probe`; "inline" = a hand-rolled `rawget`/`type` check outside
any `Require` block.

Four engine facts every reader hit and cited, stated once: (1) `apply` runs
inside `ModsLoadCode()` before class flattening and before presets load, so a
probe may call only what a class DECLARES and any target that walks preset
tables at body level throws on every stub; (2) every `GameVar` is `false` at
apply time (`lib.lua:1069-1083`) — `g_Consts`, `UIColony`, `MainCity`,
`SessionRandom`, `MainMap` all index-throw at the menu; (3) `IsValid`,
`IsKindOf`, `IsKindOfClasses` are C and a plain-table stub never passes them;
(4) `OnMsg` is write-only (`cthreads.lua:64-73`), so a shipped handler has no
callable handle and `Msg(...)` fires every listener.

### 3b · The table

| # | module | checks | install site(s) | verdict | why, in one line |
|---|---|---|---|---|---|
| 1 | `90_SaveSanitizer` | E2 | HANDLER | UNPROBEABLE | both compensated fixups mutate live state from their first statement (`WindTurbine.lua:96`, `Station.lua:1500 DoneObject`) |
| 2 | `Fix_AnomalyCaveInMap` | E2, SetGlobal×2 | PRE-TAIL ×2 | UNPROBEABLE | the unguarded map read (`CaveInRubble.lua:109`) is observable but no stub path returns cleanly: `SessionRandom` is `false` at the menu, else rubble is placed |
| 3 | `Fix_ArrivalDeaths` | E9 | PRE-TAIL ×2 | PARTIAL | the `Idle` seam (`Colonist.lua:2233-2236`) is stub-safe; the pinned `Arrive` body fires `Msg`, `Attach` and a `Sleep` destructor |
| 4 | `Fix_BombardmentSpread` | E8, SetGlobal | REPLACE | UNPROBEABLE | the defect line sits inside the spawn loop after `PlayFX`; the body yields and spawns threads; `SessionRandom` throws at the menu |
| 5 | `Fix_BrokenTrackSalvage` | E1 T1 | POST + HANDLER | UNPROBEABLE | the params copy (`Track.lua:631-640`) is observable only past `PlaceConstructionSite` (`:641`); the existing `test` on `node_idx == false` is the right proxy |
| 6 | `Fix_CrystalMysteryHang` | E2 | HANDLER ×3 | UNPROBEABLE | a thread proc (`Crystals.lua:46` spawns at its first statement); nothing is wrapped |
| 7 | `Fix_DestroyedTunnels` | E2 | PRE-TAIL + HANDLER | UNPROBEABLE | the only guard is `IsValid` (`Tunnel.lua:194`), false on any stub and indistinguishable from a body that gained a `destroyed` test; past it is `pf.AddTunnel` |
| 8 | `Fix_DomeFreeSpaceMismatch` | E2 | REPLACE | PARTIAL | call/result shape observable; the second-argument axis (`_GameUtils.lua:541/:544`) sits behind `ValidateBuilding` on a real object |
| 9 | `Fix_DomeOverviewHighlight` | E2 | REPLACE | PARTIAL | the exact defect line (`ColonyControlCenter.lua:1300`, `v` vs `tv`) is observable, but `:1294` indexes `g_Consts`, `false` at apply ⇒ always declines at the menu |
| 10 | `Fix_DroneTransportMinors` | E2 | PRE-TAIL | **PROBEABLE** | stub restrictor table with two keys; `true` iff only `Fuel` was cleared (`DroneControl.lua:673-674`); an empty serviced list stops the loop |
| 11 | `Fix_DustSicknessBiorobots` | DataPatch, no `Require` | DATA + HANDLER | UNPROBEABLE | no function; the pass's own walk is the content check |
| 12 | `Fix_ExoticDepositSign` | E2 T2 | DATA + HANDLER | UNPROBEABLE | a class-default write; the `test` on `entity` is the content verdict |
| 13 | `Fix_ExtenderFlapChurn` | inline E1, no `Require` | REPLACE (PRE-TAIL bypass when inactive) | **PROBEABLE** | stub records Disconnect→Connect on the CAPTURED `orig` (`DroneHubExtender.lua:109-112`); installs at file scope, so a probe must hook that path |
| 14 | `Fix_FounderTraitNotification` | E2 | HANDLER | UNPROBEABLE | an `OnMsg` handler; the defective table is file-local (`ColonyViability.lua:300`); `Msg`-based probing posts a real notification |
| 15 | `Fix_FreedHousingNotice` | E3 | POST | **PROBEABLE** | `Residence.RemoveResident` on a stub: `true` iff `ResetFreeSpace` ran and no homeless wake (`Residence.lua:119-126`); positive capture required (`Colonist.lua:2901` early return does nothing) |
| 16 | `Fix_GeneForging` | E2, SetGlobal | POST | UNPROBEABLE | a parameterless global over live research state (`Colonist.lua:4398`); its header forbids a branch guard anyway |
| 17 | `Fix_GhostFarmOxygen` | E2 | PRE-TAIL + HANDLER | **PROBEABLE** | `FarmBase.ApplyOxygenProductionMod` on a stub dome: `true` iff `SetModifier("air_consumption", farm_id, 0, 0)` (`Farm.lua:634-644`); never probe `SetDome` (C `IsKindOf` on self) |
| 18 | `Fix_GraphConsumedCaption` | E5 | POST | UNPROBEABLE | body iterates `GroupResourceIds`/`Presets.TerraformingParam`, empty until presets load (after `ModsLoadCode`); `GetCityResourceOverview` leaks an object on a bare stub |
| 19 | `Fix_JumboCaveReinforcementWedge` | E3 | HANDLER ×2 | UNPROBEABLE | pinned target is a file-local consuming `InteractionRand` (`WasteRock.lua:328-331`); handler inputs are live-game only |
| 20 | `Fix_LakeEntombment` | E2 | POST | PARTIAL | the timing premise needs the engine `PlacePrefab` (`LandscapeLake.lua:290`); a stub-safe proxy exists for the RC exemption in `ScatterUnitsUnderneath` (`ConstructionSite.lua:1918`) |
| 21 | `Fix_LanderEmptyLaunch` | E5 | POST | **PROBEABLE** | seven-method stub; `true` iff the shipped `IsCargoReady` says ready for an auto-mode rocket in its wait window with an empty request (`UniversalRocket.lua:535-559`); keep `instant` nil |
| 22 | `Fix_LandscapeUnitFilter` | E2 T1 P1 | REPLACE | **PROBEABLE (probed)** | sees the 1.1.0 signature/storage (`Landscaping.lua:510`), not the defect line (`:522`) — §2a |
| 23 | `Fix_LayoutTechLock` | E3 | POST | UNPROBEABLE | **HIGH**: a naive probe leaks the stub into the `s_ConstructionControllerDeleteOnLoad` GameVar (`LayoutConstruction.lua:385`) |
| 24 | `Fix_MirrorSphereSite` | E1 T1 | PRE-TAIL | PARTIAL | guard-order proxy only; past `:838` the body writes `InteractionSeeds`, calls `NetUpdateHash` and leaks a thread |
| 25 | `Fix_NightShiftWork` | E1 | POST | UNPROBEABLE | reads live colony state; nothing discriminating on a stub |
| 26 | `Fix_PayloadTemplateRefill` | E8 P1 | REPLACE ×2 | **PROBEABLE (probed)** | ⚠️ the probe indexes `FlightPolicies`, a `ClassesBuilt` global; safe by boot order (the mod-less first pass built it), fragile; this probe has NEVER run in a real boot (`177c7b2` postdates the newest log) |
| 27 | `Fix_RocketDroneChurn` | E3 T1 | REPLACE | PARTIAL | the defect axis is observable on an empty list; the `refuel_disabled` branch is not; the header explains its `test` |
| 28 | `Fix_RocketInteractGuard` | E3 + inline ×2 | PRE-TAIL ×2 | UNPROBEABLE | a plain-table stub meets C `IsValid`/`IsKindOfClasses` before anything discriminating |
| 29 | `Fix_SaintBlessing` | E3 P1, DataPatch | DATA + HANDLER | **PROBEABLE (probed)** | the F-1 probe; positive capture of the filed label |
| 30 | `Fix_SequenceLatents` | inline E2, no `Require` | POST + PRE-TAIL | UNPROBEABLE | (a) writes `InteractionSeeds`/`NetUpdateHash` past the guard; (b) `GameInit` on a stub reaches `AddToLabel` in-game |
| 31 | `Fix_ShelterReflex` | inline E2, no `Require` | PRE-TAIL | UNPROBEABLE | re-enters a command thread in-game; at the menu a stub throws at C `IsValid`/`GetMap` |
| 32 | `Fix_ShuttleHubOffAvailable` | E3, SetGlobal | POST | **PROBEABLE** | stub city with a hub label: `true` iff the shipped `IsLRTransportAvailable` answers on the hub's mere presence |
| 33 | `Fix_ShuttleTransportCache` | E3 | REPLACE | UNPROBEABLE | assigns the live routing cache past `:3179` (`Colonist.lua:3182`); ⚠️ plain-assignment global replacement, no `SetGlobal` read-back |
| 34 | `Fix_SinkholeIndestructible` | E2, DataPatch | DATA | UNPROBEABLE | a class-table write by design |
| 35 | `Fix_StaleReservations` | E2 | POST + HANDLER | **PROBEABLE** | stub residence: `true` iff `ReserveResidence` records the unit and returns truthy; do not inherit from `Residence` (`IsSuitable` reads a global filter) |
| 36 | `Fix_TrackConnectorPingPong` | E11 | REPLACE + POST (tail exit) | UNPROBEABLE | **HIGH**: places real `TrackBase`/`TrackGridElement` objects (`TrainTransport.lua:133-152`) |
| 37 | `Fix_TrackSalvageRefund` | E7 | REPLACE + POST (PRE-TAIL early exit) | **PROBEABLE (half A)** | `GetRefundResources` on a stamped stub element; half B shares row 38's dangerous body |
| 38 | `Fix_TrackSalvageWipe` | E7 | REPLACE + HANDLER | PARTIAL | branch-shape proxy only; **HIGH** past `:493` (`Msg("StationsDisconnected")`, `SuspendPassEdits`, `DoneObject`/`PlaceObjectIn`) |
| 39 | `Fix_TrackTunnelPowerBridge` | E6 | PRE-TAIL + HANDLER ×2 (⚠️ neither `WhenActive`) | UNPROBEABLE | a static handler is the target; `ConnectToGrids` merges real grids |
| 40 | `Fix_TrainCargoDumping` | E3 T1 P1 | REPLACE | **PROBEABLE (probed)** | contract verified line for line against `Train.lua:779-805`; misses its own DEFECT line — §2b |
| 41 | `Fix_TrainWaitTime` | E8 | PRE-TAIL | PARTIAL | call-order proxy; the `PlayPrg` loop (`ColonistTransport.lua:636`) runs on the apply thread if the stub's `SetHolder` is not a no-op |
| 42 | `Fix_TrainsToVoid` | E3 | PRE-TAIL | UNPROBEABLE | **HIGH**: `Msg("BuildingDemolished")` fan-out (`Building.lua:908`) and a possible thread (`:906`); never probe |
| 43 | `Fix_VacuumWalks` | E14 T1 P1 | REPLACE | **PROBEABLE (probed)** | contract verified against `Colonist.lua:1886-1983`; a task without `shuttle = true` reaches `CreateColonistTransportTask` |
| 44 | `Fix_WispRewards` | E1 | REPLACE (⚠️ bare global, no read-back) | UNPROBEABLE | **HIGH** in-game (kills wisps, grants RP); throws at the menu on `false.mystery` |

### 3c · Tallies

| | count |
|---|---|
| PROBEABLE | **13** (5 already probed + 8 candidates: rows 10, 13, 15, 17, 21, 32, 35, 37) |
| PARTIAL — a proxy of the assumption, not the assumption | **8** |
| UNPROBEABLE | **23** |
| modules whose reader recorded a side-effect hazard for a naive probe | **30 of 44** (6 marked HIGH; group A's seven describe object placement, thread leaks or engine writes without the word) |
| targets that are "observable only through a throw" (the contract reads a throw as decline) | 3 (rows 2, 5, 3's `Arrive`) |

Install sites, 64 over 44 modules: **PRE-TAIL 15 · PRE-NOTAIL 0 · POST 13 ·
REPLACE 15 · HANDLER 17 · DATA 4.** ⭐ Every pre-wrapper in the pack already
ends in `return orig(...)`; there is nothing to rewrite for §7e-2, only a rule
to write down.

**What the tally means for the sentence.** Even if all 8 candidates were built
and every PARTIAL were accepted as a proxy, 23 modules can never carry a probe,
and the 8 that can would test one known axis each. "Every fix checks" cannot
be made true by probes; "checks the code it patches" can be made true only by
something that sees the whole body (§4).

### 3d · What I re-derived myself (control)

One shipped body per group, chosen where the verdict rested on a specific
line: `DroneControl.lua:672-677` (row 10 — the literal `r_t.Fuel = nil` is
there, the loop bound is `#self.serviced_rockets`), `Fix_GhostFarmOxygen.lua:44-58`
(row 17 — the wrapper's last statement is `return orig(self, dome, ...)`),
`Fix_WispRewards.lua:33-45` (row 44 — a bare `function SetLightTrapMode(mode)`
with no `SetGlobal`), and the sanitizer paren on both trees (§3e). All four
held. The Lua 5.3 facts the readers leaned on — `IsValid` on a plain table,
`GameVar` = `false` before a game — are the same facts the pack's own headers
and `FIX_POLICY` §2 (the F110 rule) already record.

### 3e · Findings the classification surfaced that are NOT this audit's to land (for 99's inbox, via the owner)

1. **`90_SaveSanitizer.lua:28` states a false reason.** "F48 STAYS. The paren
   is still misplaced upstream." On 1.1.0 `Station.lua:1504` reads
   `ProcessTrackElements(ResolveMap(track), track.elements)` — correct; the
   misplaced form survives only in the 1.0.7 archive (`:1346`). I confirmed
   both lines myself. The pass may still be warranted for a migrated save whose
   `AppliedSavegameFixups` already lists the fixup (that bookkeeping route,
   `CommonLua/SavegameFixup.lua`, was NOT OPENED by anyone), but the header's
   stated reason is wrong on the shipped tree. A REMOVE-shaped question, so it
   needs the replacement traced, not a verdict from this report.
2. **Two modules replace a global by plain assignment**, skipping
   `SMRFixPack.SetGlobal`'s §1.4b read-back: `Fix_WispRewards.lua:39`,
   `Fix_ShuttleTransportCache.lua:61`. `sigcheck.py` resolves both (they are
   `function Name(` declarations), so arity is bounded; the read-back is not.
3. **Three `OnMsg` handlers are registered without `WhenActive`:**
   `Fix_CrystalMysteryHang.lua:115` (`MysteryEnd`),
   `Fix_TrackTunnelPowerBridge.lua:160` and `:166` (`StationsConnected`,
   `PostLoadGame`). `FIX_POLICY` §2's A1 rule asks every handler to re-check
   status and veto; whether these three are benign by construction was not
   assessed here.
4. **`Fix_PayloadTemplateRefill`'s probe has never run in a boot** and indexes
   a `ClassesBuilt` global (`FlightPolicies`) at apply time; correct today by
   the boot order, fragile by construction. 07's re-read of 04b's probes should
   include it.
5. **Three modules carry no `Require` block** (`ExtenderFlapChurn`,
   `SequenceLatents`, `ShelterReflex`; a fourth, `DustSicknessBiorobots`, is a
   `DataPatch` whose checks live in the pass). Their inline checks are
   existence checks; any pack-wide mechanism in `Require` (§5, Option 3) does
   not reach them until they are routed through it.

---

## 4 · §1c — what the mod sandbox actually permits

Evidence classes: **[tree]** a read of the shipped 1.1.0 Lua; **[exe]** a
string read of `Mars.exe` (18,741,760 bytes, mtime 2026-09-08); **[log]** an
archived boot log; **[desk]** the engine's own sandbox lines executed on Lua
5.3; **[not measured]** stated as such.

1. **`debug` is blacklisted for mods, and it is absent in ONE context, not from
   the engine.** [tree] `ModEnvBlacklist` carries `debug = true`
   (`CommonLua/Modding/Mod.lua:1436`); the table closes at `:1441`. [log] The
   Test Kit's own runtime read on 1.1.0 prints `no debug.getinfo (mod sandbox)`
   (`archive/logs/first110_…-6a91a190.log:70`, 2026-09-08) — a measurement
   inside the sandbox on the shipped build. [tree] 16 shipped files call
   `debug.getinfo` (`CommonLua/Core/lib.lua`, `cthreads.lua`, …), and [exe] the
   binary carries `getinfo`, `nparams`, `isvararg`, `istailcall`, `getupvalue`,
   `sethook`. So arity via `debug.getinfo` exists for the engine and the console
   and is withheld from mod code only. ⚠️ A console read of `debug` measures the
   wrong environment; the TestKit is the right instrument because it IS a mod.

2. **`string` is not blacklisted, and the gate is on the top-level name only.**
   [tree] `ModEnvMeta.__index` (`Mod.lua:1559-1568`): `if env_blacklist[key]
   then return end` then `rawget(original_G, key)`, the whole real table.
   [desk] I executed `Mod.lua:1280-1441` (the blacklist) and `:1551-1627`
   (`ModEnvMeta` + `LuaModEnv`) verbatim on Lua 5.3 with four one-line stubs
   (`FirstLoad`, `Loading`, `PersistableGlobals`, `empty_table`), built an env
   with `LuaModEnv()` and ran a chunk inside it. Results: `debug` nil, `io` nil,
   `load` nil, `loadstring` nil, `os` = `{time}`, `getmetatable` the safe
   wrapper, `setmetatable` real, **`string` the real table, `string.dump` a
   function, `string.byte` a function.** The replica enforced the blacklist on
   my first attempt (my test used `load` and it was nil), which is the
   falsifier for the replica itself.

3. **`string.dump` is compiled into the engine.** [exe] `Mars.exe` carries the
   literal `unable to dump given function` (the error text of Lua's `str_dump`)
   and `Lua 5.3` once. ⛔ **Not a runtime proof** that the engine registers
   `dump` under `string` — an engine may strip it at registration. This is the
   one measurement left for a game boot, and it is a 5-line TestKit probe:
   `type(string.dump)`, `pcall(string.dump, LandscapeForEachUnit, true)`, print
   the length and the first 16 bytes in hex. Everything in §5's Option 3 is
   conditional on that line reading `function`.

4. **What `string.dump` returns, and how stable it is.** [desk, Lua 5.3, this
   rig — NOT the engine's build]
   - A C function refuses: `unable to dump given function`. The engine's
     C-side surface (`Landscape_ForEachObject`, `GetTargetAmount`, …) can never
     be fingerprinted; every target the pack replaces is a Lua function in a
     shipped `.lua`, so the pack's 43 replacement sites are all dumpable *if*
     item 3 holds.
   - A stripped dump (`string.dump(f, true)`) is byte-identical across chunk
     names, local-variable renames and comment edits, and **differs across line
     positions**: two dumps of the same body five lines apart differ in exactly
     the bytes holding `linedefined`/`lastlinedefined` (positions 36 and 40 of
     the outer proto, 129 and 133 of its nested closure). So a raw hash flips on
     any edit *above* the target in its file. Those ints sit at fixed places in a
     self-describing format (header 34 bytes: signature, version, format,
     `LUAC_DATA`, five size bytes, `LUAC_INT`, `LUAC_NUM`; then upvalue count;
     then per proto: source, two ints, `numparams`, `is_vararg`, `maxstacksize`,
     code, constants, upvalues, nested protos, debug). A ~80-line Lua walker can
     zero the two ints in every proto and must land exactly on the last byte of
     the dump — if it does not, the format is not what it assumed and the check
     **abstains** rather than declines. That is the built-in falsifier the
     peer's "flips every hash" hazard needs.
   - **Arity needs no pin at all.** `numparams` and `is_vararg` are single bytes
     at offset `36 + 2 × sizeof(int)` of a stripped dump. [desk, inside the
     sandbox replica] the 1.1.0-shaped shipped function reads `3, vararg`; the
     1.0.7-shaped replacement reads `2, vararg`; mismatch = true. The expected
     value is our own replacement's dump, so the check is self-describing:
     `arity(shipped) == arity(ours)`, computed at install, per site, forever.
   - Cost: FNV-1a in pure Lua over 43 × 200 bytes ran in 1 ms on the desk; real
     targets are 0.5–5 KB, so tens of milliseconds per boot at most.

5. **Bytecode can be hashed but never loaded.** [tree] `load`, `loadstring`,
   `dofile`, `pdofile`, `dostring` are all blacklisted (`Mod.lua:1424-1432`).
   This kills the ck73 "trampoline" idea (no separately-loaded chunk, no custom
   chunk name) and removes the only injection route a `string.dump` capability
   could otherwise open.

6. **Body-versus-source comparison is desk-only, by two independent bars.**
   [tree] `io` is blacklisted (`:1437`), and players do not have `ModTools/Src`
   in the first place — the shipped game carries packed `.hpk` code. So the
   `SRC:` sha256 pins and `bodycheck.py` cannot reach runtime in their present
   form; what CAN reach runtime is a second pin of the *compiled* body, taken
   from the engine itself (item 4).

7. **The two-branch measurement of what a fingerprint would have done on
   1.1.0.** [tool, both trees] With the current 1.1.0 pins compared against the
   archived 1.0.7 tree, `bodycheck.py --src <archive>` reports **27 BODY-CHANGED
   rows + 1 TARGET-ABSENT across 24 of 44 modules**; `sigcheck.py --src
   <archive>` reports **1 MISMATCH** (`LandscapeUnitFilter`, F115) and 42 OK.
   Reconciled against the re-verification's verdicts:

   | | modules |
   |---|---|
   | pinned body differs between branches | 24 |
   | … of which the re-verification ruled FIX (F-1, F-3, F-6, F-7, F-8, F-9, F-10) | 7 |
   | … of which it ruled KEEP (fix still correct on the new body) | 17 |
   | FIX rows whose pinned bodies are identical on both branches | **1 — `StaleReservations` (F-2)** |
   | replacement signatures that differ | 1 (F115) |

   ⇒ A body fingerprint pinned on 1.0.7 would have stood down 24 modules at the
   first 1.1.0 boot: 7 correctly (the ones that were broken or reverting 1.1.0
   improvements, F114 among them) and 17 needlessly (a source edit that left the
   fix correct). An arity read would have stood down exactly F115 and nothing
   else. Neither sees F-2, because nothing in the code we pin changed — 1.1.0
   added a new reservation *kind* elsewhere. ⚠️ Source hashes are the proxy
   here; a stripped bytecode hash is invariant to comment and rename edits, so
   its false-positive count is at most 17 on this patch and probably lower.
   1.1.0 was the largest patch this title has had; a hotfix touches fewer files.

8. **Class (c) is the ceiling, and the prompt's count of it is off.** The
   re-verification's own table (`PACK_1_1_0_REVERIFICATION.md` §4) lists six
   class-(c) instances in total — F111, F112, F-1, F-2, F-3, F-5 — of which
   **four**, not six, are among the ten FIX rows. Of those four, two are
   caught by fingerprinting a *callee* the module depends on rather than its
   target (F-1: `AddDomeColonistsModifier`'s body changed; F-3:
   `Community:GetScoreFor`'s signature changed), one is data (F-5, a rewritten
   profile preset — a data hash on the fields a `DataPatch` reads would see it),
   and one is genuinely invisible (F-2). So "class (c)" as the audit uses it
   mixes "we pinned the wrong function" with "no function changed"; only the
   latter is the hard ceiling, and it is one module of 44 on this patch.

9. **The "whole pack stands down at once" hazard, sized.** The Lua compiler is
   inside `Mars.exe`; hashes flip pack-wide only if its code generator changes
   (a Lua version bump, an optimisation change). The header carries the version
   and format bytes, so a version bump makes the walker abstain, not decline;
   an optimisation change under the same version would flip every hash and is
   the one case that decline-all reaches. It is discriminable after the fact in
   five minutes — desk `bodycheck.py` OK on the same targets while every runtime
   pin mismatches means "recompiled, not changed" — and recoverable with one
   boot to re-pin plus one upload. Whether the pack should decline-all or
   abstain-all on a quorum of simultaneous mismatches is an owner call (§9).

---

---

## 5 · The options, costed, and a recommendation

Costed against four questions: what it makes TRUE, build cost, runtime cost,
cost per future module, and how it fails. "Sentence" means HOW IT WORKS bullet
3 as it stands (`metadata.lua`, unchanged by link 06 on the owner's ruling).

### Option 1 — probe everything probeable, scope the sentence to that

- **Makes true:** "stands down if the shipped code stops behaving the way the
  fix assumes, on the axis the author thought of" — for 13 of 44
  modules (§3). It cannot make "every fix" true: 23 modules are UNPROBEABLE —
  handlers, data patches, thread-spawning targets, and three whose only
  observable outcome on a stub is a *throw*, which the contract reads as a
  decline (§3c).
- **Build:** one probe per module at the `Fix_TrainCargoDumping` discipline —
  a stub contract written from the shipped body, the F-1 positive-capture rule,
  a desk harness run — is 30–60 lines and roughly an hour each with the
  reading; the 8 unwritten candidates ≈ two sessions, plus a review pass
  because **a probe is shipped code that runs on every player's boot**.
- **Runtime:** negligible per probe; the risk is not time but side effects.
  §3's danger column lists 30 targets where a naive stub reaches
  object placement, a broadcast `Msg`, a thread, or the interaction RNG. Every
  one of those is a shipped bug if the stub contract is wrong.
- **Per future module:** the same hour, forever.
- **Fails:** silently, in the direction that matters. F114's axis was unknown to
  its author, so a 1.0.7-era probe would have passed (§2b). Option 1 converts
  "we do not check" into "we checked" without closing that gap — the exact
  shape F114 shipped under, which is why the brief calls Option 2 worse than
  nothing. Option 1 is Option 2 with better intentions.

### Option 2 — probe everything, weak probes accepted

Rejected on the brief's own reasoning and on §2b: a weak probe that passes is a
false clearance. Not costed further.

### Option 3 — a universal runtime fingerprint (two tiers, separable)

**3a · Signature (arity) — self-describing, zero authoring.** In `00_Core.lua`,
at every install of a *replacement* (a `SetGlobal` and each `function C:M`
copy), read `numparams`/`is_vararg` from `string.dump(shipped, true)` and from
`string.dump(ours, true)` and decline on mismatch. Abstain, with a log line,
when `string.dump` is nil, throws, or the header signature/version/format bytes
are not the ones the reader was written for.
- **Makes true:** "stands down if a patch changes the signature of the function
  it replaces" — for every replacement site, present and future. [tool] On the
  1.1.0 patch this stands down exactly F115 and nothing else (§4 item 7).
- **Build:** ~40 lines in core + a `--selftest` fixture; one TestKit probe first
  to confirm `string.dump` at runtime (§4 item 3). One session including the
  desk harness.
- **Runtime:** microseconds per site. **Per future module:** zero.
- **Fails:** abstains (never declines) on any format surprise; a wrapper that
  forwards `...` is not a replacement and is not checked — correctly.

**3b · Body — pinned, normalised bytecode hash.** A ~80-line walker of the 5.3
dump format zeroes `linedefined`/`lastlinedefined` in every proto and must
consume the dump exactly; FNV-1a over the result; compared at apply against a
`-- BYTECODE: <selector> <hash>` header line beside the existing `SRC:` pin.
Pins are read from the game itself: a pack "pin mode" (or a TestKit probe) that
prints every target's hash at boot, and a `tools/` script that writes them into
the headers — one boot per patch, which the patch-day workflow already spends.
- **Makes true:** "stands down if a patch changes the code it patches" — for
  every pinned function, including callees a module chooses to pin (which is
  how F-1 and F-3 become visible, §4 item 8). With a 20-line data-hash in the
  `DataPatch` runner, also "or the data it patches" (F-5's class).
- **Build:** core walker + hasher + selftest (one session); pin tooling (half a
  session); first pin cycle on 1.1.0 (one owner boot + one script run).
- **Runtime:** [desk] ~1 ms for 43 × 200 B; real bodies are larger, so tens of
  milliseconds per boot. **Per future module:** one header line from the boot
  log; zero reading.
- **Fails, in the safe direction, and loudly:** [tool, §4 item 7] on 1.1.0 it
  would have stood down 24 of 44 modules at first boot, 17 of them working. The
  C1 dialog already reports the count; the recovery is the desk
  `bodycheck.py` run the patch day already performs, a re-pin boot, and the
  upload the patch already needs. The whole-pack case (a compiler change) is
  discriminable in five minutes and recoverable the same way; the decline-all
  versus abstain-all policy on a quorum of simultaneous mismatches is an owner
  call (§9). ⛔ It does NOT see class (c) in its strict sense — F-2 — and never
  will.

### Option 4 — move the guarantee to process

`bodycheck.py`, `sigcheck.py`, `parsecheck.py`, `logscan.py` and the
re-verification chain already exist and were built this week. Making the
sentence a promise about the project — "every game update gets a compatibility
pass" — costs nothing to build and one desk run per patch.
- **Makes true:** a project claim, which the store card can carry honestly.
- **Fails:** on patch day, for every player, until the pass ships. F114 reached
  a reporter within hours of 1.1.0; the pass took two days. Only a runtime
  route protects the window the process cannot.

### Option 5 — reword smaller (ck112's rejected (a))

Fallback only. The evidence that it is NOT needed: Options 3a and 4 are
buildable now and Option 3b is buildable in one cycle, and together they make
a scoped sentence literally true. The evidence that it IS needed *for now*: the
sentence is false today and stays false until 3a/3b ship (§9 puts that choice
to the owner).

### Recommendation

**Build Option 3 in two steps, keep Option 4 as its desk half, and scope the
sentence to "the code it patches".**

1. **First** (one session, no policy question): the `string.dump` TestKit probe
   — a 5-line runtime read that decides everything below. If it reads `nil`,
   Option 3 is dead and the honest answer is Option 4 + Option 5's wording.
2. **3a immediately after** (one session): self-describing arity at every
   replacement site. Zero authoring, zero false positives on the largest patch
   this title has had, and it closes the F115 class for good.
3. **3b in the following cycle** (two sessions + one owner boot): the body
   fingerprint with pins, the quorum policy the owner chooses, and the
   `DataPatch` data-hash.
4. **Probes stay what §2a of `FIX_POLICY` says they are** — the branch guard
   for a module carrying a branch-specific body, written where a stub is shown
   safe — not a coverage target. Do not chase 44.
5. **The sentence changes once, when 3a ships**, to the 3a/3b wording in §6.

---

## 6 · §1d — draft wordings, one per route (drafts; `06_TEXT`'s successor owns the string)

Each is route-checked against what EVERY fix would actually do at boot on a
player's machine. "Every" survives only where the mechanism is pack-wide.

**Today (no build) — what is literally true now:**
> Every fix checks that the game code it patches is still there before it
> touches anything, and stands down by itself if an official patch has renamed
> or removed it. A fix that stands down does nothing at all — it never guesses.

**After 3a (arity) — true for every replacement, and still true for wrappers
because "renamed or removed" already is:**
> Every fix checks the game code it patches before it touches anything, and
> stands down by itself if an official patch has renamed, removed or reshaped
> it. A fix that stands down does nothing at all — it never guesses.

**After 3a + 3b (body fingerprint) — the strongest defensible sentence:**
> Every fix checks the game code it patches before it touches anything, and
> stands down by itself if an official patch changes that code. A fix that
> stands down does nothing at all — it never guesses. Each game update also
> gets a compatibility pass, because a change *around* a fix can matter too.

**Option 1 (probe coverage, scoped) — "every" cannot survive:**
> Most fixes check how the game's code behaves before they touch anything, and
> stand down by themselves if it no longer behaves the way the fix expects.
> A fix that stands down does nothing at all — it never guesses.

**Option 4 only (process) — a project claim, not a code claim:**
> Every fix checks that the game code it patches is still there before it
> touches anything, and stands down if it has been renamed or removed. That
> check cannot see every kind of change, so each game update gets a
> compatibility pass before the pack is called good on it.

⛔ In every draft, "what it was written for" is gone: on the evidence of §4
item 7 no runtime check reaches it, and one module of 44 on this patch (F-2)
sits outside every route. That phrase is the part of the sentence that cannot
be made true, and it is the only part.

---

## 7 · JOB TWO — stop the pack being blamed for other mods' faults

### 7a · The mechanism, re-verified on the 1.1.0 tree

`CommonLua/Modding/Mod.lua`, all [tree]: the block is live in retail because it
is gated `if not Platform.asserts` (`:2968`). `OnMsg.OnLuaError(err, stack,
os_paths)` (`:3019-3031`, its own comment at `:3018`: *"rough estimation based
on call stack"*) walks `ModsLoaded` and calls `ReportModLuaError` for every mod
whose `content_path` is a case-insensitive substring of **either** the error
text **or** the stack. `ReportModLuaError` (`:2975-3012`): returns if
`config.DisableErrorReporting`; returns if `ReportedMods[mod.id]` is already
set (**once per mod id per process**, `:2980-2983`); otherwise appends the mod
to `ModsToReport` and, on the first append, starts a real-time thread that
drains the list, `ModPrint`s one `Error in mod <title> (id …, v…) from <source>`
per mod and shows ONE `CreateMessageBox` whose body joins the titles with
newlines (`:3001-3010`). The `OnLuaError` message itself is raised from C —
no Lua file in the tree raises it (`Gossip.lua:54` only forwards it).

Consequences that follow directly:
- **Any mod with a frame anywhere in the stack is named**, whether it threw or
  was passed through. Our paths read `Mod/SMR_CommunityFixPack/Code/<file>` in
  every archived stack, packed or unpacked (`EF-065`).
- **Order in the box = enable order.** `ModsLoaded` is filled from
  `GetModsToLoad()` → `GetModsEnabledByUser()` → `AccountStorage.LoadMods`
  (`:2137-2143`, `:2003-2009`), which `TurnModOn` appends to with
  `table.insert_unique` (`CommonLua/UI/ModManager.lua:35-36`). So "who is named
  first" is whichever matching mod the player ticked earliest; alphabetical
  sorting exists only for the UI list (`SortModsList`, `:1687`).
- **The dedupe cuts both ways.** After one report, nothing later in the session
  can un-name us — and nothing later can name us again either, so a genuine
  fault of ours after a benign pass-through goes unreported in the box.
  [log] Measured: in the 2026-09-08 15:57 session F115 threw at `0:01:03` and
  drew the session's one `Error in mod` line (`f114repro110_…log:274`); F114
  then threw **157 times** from `0:25:42` and drew none.

### 7b · How often is this real? Every blame line in the archive, per line

`grep "Error in mod"` over `docs/archive/` (95 root logs + 10 in `logs/`): **4
lines in 4 files, 3 distinct sessions** — `unforced110_…15.57.09` is a 274-line
prefix of `f114repro110_…15.57.09` (same session, archived twice; `cmp` ends at
byte 14539 = line 274).

| # | log | line | throw site | verdict, with the reasoning |
|---|---|---|---|---|
| 1 | `act1_Mars.exe-20260819-15.18.19` (1.0.7) | `:522` | Test Kit's own `quit()` at suite end | **Test Kit's, not the pack's** — the named id is `SMR_CommunityFixPackTestKit`; `SESSION_LOG.md:7891` recorded it as a shutdown artefact at the time. Not a misattribution: the kit's frame IS the throw site. |
| 2 | `forced110_Mars.exe-20260908-15.43.37` (1.1.0) | `:300` | `Fix_LowStorageWarning.lua:125`, nil global `GetCommandCenterLifeSupportGrids` | **Ours by construction** — the Test Kit's FORCE leg applies modules past their own decline; the throw is in our body. Not a misattribution. |
| 3 | `f114repro110_…15.57.09` (1.1.0) | `:274` | `Fix_LandscapeUnitFilter.lua:63` (F115) | **Ours** — our replacement body is the throw site. Not a misattribution. |
| 4 | `unforced110_…15.57.09` | `:274` | same session as #3 | duplicate archive of #3. |

⇒ **Zero misattributions in the archive.** Every archived blame line names the
mod whose code threw. The two misattributions the owner remembers are the two
**field** reports (`bugs/F104.md`, `bugs/F105.md`, 2026-08-23/24, one
reporter), whose reporter logs are not in the repo but whose stacks the entries
quote and which the owner's rig reproduced for F104:
- **F104** — `Lua/Passage.lua:1117` nil `networks`; our frame
  `Fix_ShuttleTransportCache.lua(86)` is a pass-through (`FindEmigrationDome →
  our FindTransportationModeToCommunity → GetTransportationModeToCommunity →
  … → AreDomesConnectedWithPassage`); the culprit (Passage Network's
  `CreateDomeNetworks` returning nil) had **already returned** and has no frame.
  Named: **us, alone.**
- **F105** — `ConstructionSite.lua:673` on a vanilla landscape site; our frame
  `Fix_MilestoneCrash.lua(73)` (module since deleted, link 02) is the
  `Msg("MilestoneCompleted")` in a copied body. Vanilla has no `content_path`.
  Named: **us, alone.**

So the measured harm is **2 player-visible boxes and 2 GitHub issues in the 17
days the pack has been live**, both from one reporter, both naming us alone
because the real cause was structurally unnameable (a returned frame, or
vanilla). The owner's "a few times" is those two plus the standing risk that
any of our 43 replacement sites sits above a throw. It is a real cost in owner
time per incident (each needed a session to derive), not a frequent one.

### 7c · Can our frame leave the stack? The tail-call hypothesis

**The mechanism holds, by the language definition and by measurement, and it
is narrower than the brief hoped.** Lua 5.3 §3.3.7: a call of the exact form
`return f(args)` is a proper tail call and *"erases any debug information about
the calling function"* — the caller's activation record is reused, so no stack
walker can recover it afterwards. [desk] `debug.traceback` through a
`return thrower(...)` wrapper shows the thrower, then `(...tail calls...)`, and
**no line of the wrapper**; through `thrower(...)` followed by `end`, or
`local r = thrower(...) return r`, the wrapper's line is present. [exe]
`Mars.exe` carries the literal `(...tail calls...)` (so `luaL_traceback` is
compiled in) and `istailcall`. ⛔ [not measured] the engine's own `GetStack`
(C, custom `file(line):  method Name` format) has never been seen printing a
tail-called frame in any archived log — because none of the archived throws
went through one. Any walker sits on `lua_getstack`, which cannot return a
frame the VM has discarded, so the property does not depend on the printer.

**Where it can apply — the install-site split** (44 modules, sites read by
the four classification passes in §3; my own spot checks in §3d):

| site shape | count | our frame present when a callee throws? |
|---|---|---|
| PRE-TAIL — wrapper ends `return orig(...)` | 15 | **no** — the tail call removed it |
| PRE-NOTAIL — calls the original last but not as `return orig(...)` | **0** | yes; a one-line rewrite to PRE-TAIL removes it |
| POST — work after the original returns | 13 | yes, unavoidably: there is no tail position |
| REPLACE — a copied or rewritten body | 15 | yes, and correctly so — the throw is in our copy |
| HANDLER / DATA | 17 / 4 | our own handler frame only |

Two limits the numbers do not show. (1) A PRE-TAIL wrapper's frame is gone only
for throws **below** the original; a throw in the wrapper's own prologue (its
`IsKindOf` test, its field read) is ours and names us correctly. (2) **F104
would not have been prevented**: the throwing call in
`Fix_ShuttleTransportCache.lua` is mid-body (`:86`, the result is stored into
a cache entry), so no tail-call rewrite applies to it. A cache wrapper is a
POST shape by nature.

### 7d · What else is available, and what is not

- **A breadcrumb we can write ourselves, without touching an engine function.**
  `OnLuaError` is not in `ModMsgBlacklist` (`Mod.lua:1443-1452`), so a mod may
  register `OnMsg.OnLuaError(err, stack)` and receive the same arguments the
  engine's handler gets. One handler that finds the FIRST stack frame and logs
  `[CommunityFixPack] named in an error raised at <file:line>; that file is not
  part of this pack` (or `…is part of this pack: <module>`) costs ~15 lines,
  runs only on an error, and would have made F104 and F105 a one-line triage
  instead of a session each. ⚠️ Route-check: the log is read by the owner and
  by PC reporters who attach it (the tracker already asks for the log); console
  players have no log to read, so this is an OWNER surface, not a player one.
- **Owning the box's wording** (ck73 option 3): `ReportModLuaError` is a plain
  global, not blacklisted, so `SetGlobal` could wrap it and, for our id only,
  substitute a message that says where the throw was — while still calling the
  original for every other mod. This is the only route that changes what a
  **console** player sees. It replaces an engine function for self-defence,
  which ck73 already flagged as a `FIX_POLICY` question, not an engineering one.
- **The trampoline (ck73 option 2) is dead**: `load`/`loadstring` are
  blacklisted (§4 item 5), so no separately-named chunk can be made.
- **Renaming out of the substring is dead**: the substring is `content_path`,
  derived from the mod id (`Mod.lua:1755-1758`); changing the id costs every
  player's enable (`H-08`).
- **Load order buys nothing**: the box names every matching mod; order only
  changes the line order in one dialog.
- ⛔ **Reachable and REJECTED, restated so nobody reads this section as
  permission:** `config` is not blacklisted, so `config.DisableErrorReporting =
  true` works from mod code and silences the box for **every mod on the
  machine**; pre-seeding `ReportedMods[our_id]` silences us before any error
  exists. Both hide real faults — ours included — from the player. ⛔ **And
  under no option may a wrapper catch another mod's or vanilla's error to keep
  our name out of the stack.** Every mitigation above leaves the error raised,
  logged and reported; the tail call merely stops adding an innocent frame.

### 7e · Recommendation for job two

1. **Do now (cheap, no policy question):** the `OnMsg.OnLuaError` breadcrumb.
2. **Do with the next code cycle:** write the rule down. §3 found ZERO
   PRE-NOTAIL sites — all 15 pre-wrappers already end in `return orig(...)` —
   so there is nothing to rewrite, only a `FIX_POLICY` §2 line to keep it so
   for new wrappers (the sibling of the "inert for a foreign object" rule:
   *end a pre-wrapper with `return orig(...)`*). The 13 POST and 15 REPLACE
   sites stay named, correctly.
3. **Owner decision:** whether to own the box wording via `ReportModLuaError`
   (the only console-visible remedy). My recommendation is **no for now**: two
   incidents in 17 days, both triaged, do not justify replacing an engine
   diagnostic; revisit if the breadcrumb shows a real rate.
4. **Re-state the fact:** `EF-065` should gain the dedupe measurement (7a) and
   the enable-order finding; the checklist's ck73 should gain "option 2 is
   dead — `load` is blacklisted" so it is not re-proposed.

---

## 8 · What I did NOT check — named

- **Nothing ran in a game.** `string.dump`'s presence under `string` in
  `Mars.exe`'s Lua state is inferred from the binary's strings and from the
  engine's sandbox code executed on a desk Lua 5.3, never from a boot. The
  engine's dump FORMAT (assumed stock 5.3; the `Lua 5.3` string and shipped
  `math.type` use are the evidence) is unmeasured. The engine's `GetStack`
  rendering of a tail-called frame is unmeasured.
- **The per-module classification is four subagent reads.** I read every
  verdict line, every `sites` line and every danger flag, and opened the shipped
  body myself for one module per group (`DroneControl.lua:672-677`,
  `Fix_GhostFarmOxygen.lua:44-58`, `Fix_WispRewards.lua:33-45`) plus the
  sanitizer paren on both trees. Any module's shipped body I did not open
  myself is a module whose classification I relay, not one I verified.
- **`GetTargetAmount` on a suspended request** (the F-10 premise) is C-side and
  still unread by anyone; nothing here changes that.
- **The reporter logs for F104/F105** are not in the repo; I used the stacks
  the bug entries quote and the owner's F104 repro as recorded.
- **F111 / F112** (deleted modules) were not re-read; their class-(c) status is
  taken from the re-verification table.
- **The opt-in pack and the Test Kit** have their own blame surfaces and their
  own self-checks; neither was examined.
- **Console rendering** of the engine's box and of our C1 dialog: unobserved,
  as `EF-065` already records.
- **`bodycheck --src <archive>` rows are source-hash proxies** for what a
  bytecode hash would flag; the two can differ on cosmetic edits in the
  bytecode-insensitive direction only.

---

## 9 · Landing sites — who implements what, in which cycle, and the text the chain's owners should land

⚠️ **The coordination gap, stated by the prompt's author and confirmed by link
06's outbox:** 06 left bullet 3 untouched because "a separate session owns
making that sentence TRUE", and this audit is read-only on `metadata.lua`. So
as of this report **nobody writes bullet 3.** The table below is the fix.

| item | implementer | cycle | fence |
|---|---|---|---|
| `string.dump` runtime probe (5 lines, prints type + dump length + 16 header bytes for one shipped Lua function and one C function, from inside the mod env) | Test Kit (07's lane if open; else a one-off local-kit edit) | before 3a; one owner boot | TestKit only |
| 3a arity check in `Require`/`SetGlobal`/install path | a new code prompt, `prompts/SELFCHECK_3A.md`, Fable | **after 99 closes** (a `00_Core.lua` edit mid-chain collides with 99's audit) | `Code/00_Core.lua`, `items.lua` untouched (no new module) |
| `OnMsg.OnLuaError` breadcrumb (7e-1) | same prompt | same | `Code/00_Core.lua` |
| tail-call rule for pre-wrappers (7e-2) — a `FIX_POLICY` §2 line, no code (0 sites to rewrite) | same prompt | same | `FIX_POLICY.md` |
| 3b body fingerprint + pin tooling + `DataPatch` data-hash | `prompts/SELFCHECK_3B.md`, chain of 2 (`CHAIN_METHOD`) | the cycle after 3a ships | `Code/00_Core.lua`, every module header, `tools/` |
| bullet 3 wording | the text lane of the release that carries 3a (06's successor) | with 3a's upload | `metadata.lua`, `UPLOAD_WORKFLOW` §3, `STORE_CARD_LIVE` |
| `EF-065` dedupe + enable-order addendum; ck73 "option 2 dead" | any session, facts lane | now | `facts/EF-065.md`, checklist item 73 |
| `90_SaveSanitizer.lua:28` header reason is false on 1.1.0 (§3, relayed) | 99's inbox | hotfix-2 | `Code/90_SaveSanitizer.lua` header only |

**Proposed checklist text** (`docs/PLAYTEST_CHECKLIST.md` → "Decisions waiting
on you"; not written by me):

> **1xx. The self-check promise — verdict YES BUT SCOPED, and three calls.**
> `reports/SELFCHECK_PROMISE_AUDIT.md`. The sandbox leaves `string.dump`
> reachable (measured on the engine's own sandbox code, not yet in a boot), so
> every fix can check the compiled signature and body of the code it patches
> at boot. What no runtime check can see is a change *around* an untouched
> target (F-2 on this patch). (a) **Build it?** Recommend yes: arity first
> (zero authoring, catches exactly F115 on 1.1.0), body hash next. (b) **On a
> patch that flips many pins at once, decline all or abstain all?** Recommend
> decline all with the dialog — it is what the sentence promises and the
> recovery is one boot plus one upload; the cost is that on a 1.1.0-sized
> patch 17 working fixes would go dark until re-pinned. (c) **Bullet 3 until
> then?** It stays false through hotfix-2's upload (you accepted that on
> ck112). Recommend leaving it if 3a is scheduled as the next cycle; otherwise
> take ck112(a) as an interim and re-strengthen with 3a. Job two: two field
> misattributions in 17 days, zero in the archive; a log breadcrumb and a
> tail-call rule are recommended, owning the engine's box wording is not.

**Proposed STATE line** (one line, under "Now"; an eviction must accompany it,
STATE is at 9211 of 9216 bytes):

> ⭐ SELFCHECK_PROMISE_AUDIT 09-09: YES BUT SCOPED — `string.dump` reachable (desk, not boot); arity check = 0 authoring; body pin = 24/44 dark on a 1.1.0-size patch; ck1xx.

---

## 10 · CORRECTIONS after the Codex cross-check (2026-09-09, same session, each re-verified against the primary evidence)

Codex's report is `reports/SELFCHECK_PROMISE_CROSSCHECK_CODEX.md` (`397bf15`).
It was written against a brief that asked it to refute this audit; it did, in
four places, and I confirmed each refutation myself before recording it. The
verdict's SHAPE — the sentence can be made true for the code a fix patches and
depends on, never for "what it was written for" in the broad reading — stands.
Its supporting claims change as follows.

**X1 · §4 item 8 and the verdict paragraph: F-2 is NOT the ceiling.** [MEASURED,
both trees] `Residence:CancelResidenceReservation` gained
`unit.expedition_residence = false` on 1.1.0 (`Residence.lua:393`; archive
`:353` lacks it). `Fix_StaleReservations.lua:100` already DECLARES that method
in its `Require` block and `:159` CALLS it. A pin over the functions a module
declares — not only the `SRC:` targets — would have declined F-2. I had checked
only the two `SRC:` pins. Consequence: the honest scope is "the code it patches
**and the code it declares it depends on**", and the strict class-(c) residue
on this patch is zero modules that we know of, not one.

**X2 · §2b: "no 1.0.7-era probe would have caught F114" is too strong.**
[READ, both bodies] 1.1.0's `local demand = station.demand and
station.demand[res]` (`Train.lua:794`) indexes `station.demand` twice where
1.0.7 (`:796`) indexed it once. A probe that records the whole ACCESS TRACE of
the shipped body on an ordinary input (a present demand request, zero carried)
and compares it to a recorded trace distinguishes the two bodies without
anticipating the failing input. What stands is the narrower claim: an
OUTPUT-only probe, which is what the pack's five probes are, would not. Trace
probes are brittle by design (any extra read declines) and still need a
per-target safe stub; they are a third option between hand probes and body
pins, not a universal one.

**X3 · §4 items 7 and 9, §5 Option 3b: source hashes do NOT upper-bound
bytecode mismatches, and "source same + bytecode different ⇒ recompiled" is not
a valid diagnosis.** [MEASURED, both trees] `Colonist.lua:13` gained `local
ipairs = ipairs` on 1.1.0, so `FindTransportationModeToCommunity` — whose own
text is unchanged — now compiles `ipairs` as an upvalue instead of a global;
`DroneControl.lua` gained four top-level locals above `UpdateRocketsInternal`
(18 vs 14), so its captured `rfRestrictorRocket` sits in a different upvalue
slot. Both are KEEP modules whose bytecode would flip. Codex's whole-chunk
compile puts the affected set at 25 modules (7 FIX / 18 KEEP), and any edit to
a file's top-level locals can flip every function below it. Also [Codex,
stock Lua]: closures capturing different VALUES dump identically — a body pin
does not see a changed captured value. The false-stand-down cost of Option 3b
is therefore HIGHER than §5 says and not reliably separable from a compiler
change by desk `bodycheck`. A better discriminator is Codex's calibration
witnesses: pack-local functions with known dumps, compared first.

**X4 · §7b line #1: the act1 blame line was mis-explained.** [MEASURED,
`act1_…-6a22b86d.log:397`, `:416`] two `[LUA ERROR]`s were raised in VANILLA
code, `Data/LawDef/LawDef-Welfare.lua:1892` and `:2026` (`ActiveLaws` is a
GameVar, `false` at the menu), called from the Test Kit's wave-4 probe
(`40_Probes_Wave4.lua(921)` via `with_globals`); the box named the kit. My
"shutdown artefact at `quit()`" came from `SESSION_LOG.md:7891`, which
describes the 2026-07-25 legs, not this 2026-08-19 log. Corrected verdict for
that line: the throw SITE was vanilla and the CAUSE was the kit's synthetic
call — the named mod did cause it, so still not a misattribution, but it is an
archived example of a box naming a mod whose frame is a caller, not the throw
site. The "zero misattributions of the pack" count is unchanged.

**X5 · §5 Option 3a under-costed.** [READ] Method replacements are direct
assignments (`function C:M()`), which core cannot intercept; `SetGlobal` covers
5 sites; three modules bypass `Require`; a `-- BYTECODE:` comment is not runtime
data (a Lua literal is needed). So the arity check needs an install API or a
per-site edit across the pack, not "~40 lines in core". Zero authoring holds
only for the EXPECTED VALUE (our own function's dump).

**X6 · A gap in the sentence's THIRD clause that neither the brief nor this
audit examined: "A fix that stands down does nothing at all."** [MEASURED,
`00_Core.lua:447-462`, `Fix_AnomalyCaveInMap.lua:99-121`] `run_apply`'s `pcall`
is not a rollback. A multi-site module installs its first site and can decline
on its second; `AnomalyCaveInMap` installs `TriggerCaveIn` at `:99` before it
attempts `FindCaveInLocation` at `:120`; a decline there returns a reason,
status reads `inactive`, and the first wrapper stays installed. Today that
path is near-unreachable (`SetGlobal` fails only if the write does not land);
under any fingerprint regime, where a second site's check can legitimately
decline, it becomes an ordinary path. "Before it touches anything" therefore
requires an ALL-CHECKS-BEFORE-ANY-WRITE install transaction in core (Codex's
I10a), and deferred handlers and data passes need their own phase checks. This
is a precondition of the sentence, not an optimisation.

**X7 · "Abstain" contradicts an unconditional sentence.** [READ] §4 item 9 and
§5 let the fingerprint abstain on a missing dumper, a format surprise, or a
mass mismatch. Under the wording "stands down by itself if …", UNKNOWN must
DECLINE, or the wording must name the exception. Owner policy (§9 already
poses it); the default consistent with the sentence is decline.

**X8 · The sandbox analysis was incomplete.** [READ, `CommonLua/Core/ToLuaCode.lua:390`]
`LuaCodeToTuple(code, env)` is not blacklisted and calls
`load("return " .. code, nil, nil, env or _ENV)` in the ENGINE's environment;
the C-side `ChecksumRemove` in front of it is the unmeasured gate. If that
gate passes arbitrary text, mod code has an indirect `load` and, through it,
`debug`. §4 item 5's "no loading route exists" was deduced from the blacklist
alone. ⛔ Not a foundation to build on (withheld authority, closable by any
patch), but it must be known: Codex's R2 probe measures it in one boot.

**X9 · Smaller corrections.** `SaintBlessing`'s probe runs in its deferred data
pass, not at apply (§1's "5 probe" count stands; "at apply" does not). The
box's order is `GetLoadingQueue`'s dependency order (`Mod.lua:1907`), which
need not equal enable order (§7a). `os_paths` substitutes the OS path only when
it exists; it does not test both forms (§7a). Our `OnMsg.OnLuaError` handler
runs AFTER the engine's and cannot alter the box (§7d). Exact bytes, not
FNV-1a, if literal identity is the claim. Codex followed the exe's registration
POINTER table: `char`, `lower`, `match`, `upper` ARE registered; my "missing
neighbours" note in the Codex brief was string placement.

**What did NOT change.** `string.dump` reachability by desk replica and binary
(Codex went further and agrees; the boot read is still owed). The arity read
flags exactly F115 across the branches (Codex re-derived it at all 15
replacement sites). The four archived blame lines, the prefix-duplicate log,
the F114 dedupe measurement, the two field cases, the tail-call property
(unmeasured in-engine on both sides), the 44/5/7/35 census, and the
"every pre-wrapper already tail-calls" count (Codex: PRE-NOTAIL 0).

**Revised recommendation, superseding §5's list.**
1. **Capability pilot first, one owner boot**, using Codex's R1–R5 Test Kit
   chunks (they subsume my 5-line probe and add the header, the arity
   controls, the indirect-load gate, `GetStack` on a tail call, and
   `find_lower` semantics).
2. **Then a bounded prototype, three modules**: `LandscapeUnitFilter` (F115),
   `TrainCargoDumping` (F114), `StaleReservations` (F-2's callee) — a
   declarative install in core that checks arity AND dependency pins over the
   module's declared `Require` set, ALL before ANY write, with UNKNOWN
   declining; calibration witnesses instead of a revision or quorum rule;
   receipts of checked-vs-installed identity. Measure its false stand-downs on
   the 1.0.7→1.1.0 delta with real engine dumps before scaling.
3. **No wording change until that ships.** Arity alone earns none of §6's
   drafts; §6's "after 3a" draft is withdrawn.
4. Job two unchanged in substance: breadcrumb (throw site + pack-frame
   presence, never cause), tail-call rule, no engine-box changes; Codex's
   caution stands that a throw site narrows triage and cannot acquit.
5. `LuaRevision` only ever as an observation label, if at all; the owner
   should clarify §2a's heading before any prose says so.
