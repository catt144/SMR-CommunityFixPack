# HOTFIX 2 — TERMINAL AUDIT (chain link 99)

**VERDICT: SHIP WITH CHANGES — one code change (F117, a throw the pack already ships on 1.1.0, found in a KEEP module) and one text/code coupling the owner's open item 126 decides. If the owner declines the code change, the pack ships no worse than v5 does today; it does not ship at the owner's stated bar.**

Audited 2026-09-09 by a fresh session (`smr-bugfixpack-a8`) that implemented
nothing in the chain. Brief: `prompts/hotfix2/99_TERMINAL_AUDIT.md`. Tree at
`24eaea0`, clean; `git pull` up to date; folder gate read at start: `99` +
`README.md` only, every row 01–08 struck. Game trees read: the shipped 1.1.0
tree at `A:\...\ModTools\Src` and the archived 1.0.7 tree at
`C:\Dev\SMR-SrcArchive\1.0.7.396349\Src`. ⛔ **Nothing ran in a game. No status
moved. Every "verified" below is a source read or a tool run unless it says
"measured", and the only measurements are the 2026-09-08 boot logs of an
80-module pack that no longer exists.**

Format and standard follow `reports/HOTFIX_1_AUDIT.md`.

## 1 · Findings, most severe first

### F-1 (P1, code, in a KEEP module — the change that decides the verdict) — `Fix_ArrivalDeaths` half (b) throws on 1.1.0 when its re-choose branch fires

`Fix_ArrivalDeaths.lua:201` calls `ChooseDome(self.traits, domes, false, dome_elevators)`.
That was the 1.0.7 signature (`_GameUtils.lua:426`, `ChooseDome(traits, …)`).
1.1.0 changed it to `ChooseDome(colonist, …)` (`_GameUtils.lua:486`) and both
callees now index the argument's `.traits`:
`Community:GetScoreFor(colonist)` → `TraitFilterColonist(self.traits_filter, colonist.traits)`
(`Community.lua:442-445`) and `Residence:IsSuitable(colonist)` → `pred(colonist.traits)`
(`Residence.lua:198-200`; the preds index their argument, `Stats.lua:192-197`).
Our traits table has no `.traits`, so the callee receives `nil`:
`FilterObjectAttributes(filter, nil)` indexes nil for every key of a non-empty
`traits_filter` (`Filter.lua:113-121`), and `pred(nil)` indexes nil for any
residence whose `filter_residents ~= "Everyone"` (`HasFreeLivingSpaceFor`
`:402-418`, `GetScoreFor` `:449-456`). A colony with one dome trait filter, or one
nursery / retirement home / hotel with free space, throws inside the arriving
colonist's `Idle` command thread. Trigger: an arriving colonist whose assigned
dome is not within walking distance of the landing spot and has no elevator
route — exactly the F53(b) case the branch exists for.

**How I know.** Both `ChooseDome` bodies read on both trees; the two 1.1.0
callees and the filter function read in full; our wrapper `:180-210` read. This
is class (c) — semantics moved under a wrapper. `Require` sees names (all
present), `sigcheck` bounds arity of replacement sites (this is a wrapper),
`bodycheck` pins `Colonist:Arrive` (unchanged). The re-verification's KEEP row
did not open `ChooseDome`. Found by the branch diff of `Colonist:Idle` + a
callee read; confirmed by me on the shipped lines.

**Why it matters now.** v5 ships this to every 1.1.0 player today (08-30). This
patch keeps the module unchanged, so it ships it again, knowing. It is the
F115 shape: a Lua error in a mod frame → the engine's mod-error dialog naming
the pack (`EF-065`) → exactly the "release and immediately repatch" outcome the
owner named as the bar. ⛔ **Not reproduced.** Control in `bugs/F117.md`.

**Recommended change** (fresh context, one small link; `Mars.exe` closed):
pass the colonist on the 1.1.0 body. ⛔ Not `self` on both branches unguarded —
ck118 binds: a per-module discriminator, read from a callee body at call time
(a one-shot probe of `Community.GetScoreFor` on a stub once `g_Consts` exists),
never a version label. Design is the fixing link's, sketched in `F117.md`.
Riders for the same link, each one line: F-2 below and the F-6 named guard
(§2 item 3).

### F-2 (P3, code, KEEP module) — `Fix_LayoutTechLock` clears a delete-on-load registration 1.1.0 added

1.1.0 `LayoutConstructionController:Activate` now ends with
`s_ConstructionControllerDeleteOnLoad = self` (`Lua/Construction/LayoutConstruction.lua:385`;
absent on 1.0.7). Our post-wrapper (`Fix_LayoutTechLock.lua:98-119`) tears down
each tech-locked sub-controller with `controller:Deactivate()`, and
`ConstructionController:Deactivate` opens with
`s_ConstructionControllerDeleteOnLoad = false` (`Construction/Construction.lua:1226-1227`).
After our loop the layout controller is unregistered, so a save taken with the
layout dialog open and a locked entry present is not cleaned by
`OnMsg.PersistPostLoad` (`:1052-1056`). On 1.0.7 the same call cleared a
sub-controller's registration (`:991` set it), a smaller divergence nobody had
named. Player-visible effect unmeasured (a leaked controller after load).
One-line repair in `bugs/F118.md`.

### F-3 (text, P2 — ships inside the mod) — the change note's bullet 2 contradicts the pass link 08 built

`metadata.lua` `last_changes` bullet 2: *"two extractor types keep a small
Astrogeologist bonus the pack gave them, which removing the fix cannot take
back; a new game is clean."* Link 06 wrote that on 2026-09-09 under ck120
(cleanup OFF). Link 08 landed the F95 residue pass in `90_SaveSanitizer.lua`
later the same day (`dcb4ef4`), which removes exactly that bonus on load. If
the pass ships, the sentence is false on upload; if the owner rules the pass
out under 126, the code moves. Either way one of the two moves before the
upload, and the §3 paste backups + `STORE_CARD_LIVE` move with it (proven
byte-identical today, §2 below). The site FAQ's save-repair list
(`faq.md:114-118`) enumerates the passes and would gain a line too.
⚠️ **Chain-shape cause:** the text link (06) ran before the last code link
(08). A text link that is not last-but-one is a text link that can be
falsified by its own chain. Routed to `100_DOCSWEEP.md` with both wordings.

### F-4 (semantics, no code change proposed) — `Fix_DomeFreeSpaceMismatch` no longer reaches the gate it repairs

1.1.0's dome gate stopped reading the tally: `Community:HasFreeLivingSpaceFor`
(`Community.lua:402-418`) and `HasAnyFreeLivingSpace` (`:366-384`) iterate
residences on `working` and never touch `free_spaces`, while `ChooseResidence`
still assigns on `ui_working` (`Residence.lua:452`). Our copy makes
`free_spaces` count on `ui_working`; on 1.1.0 that feeds only the passenger
count (`GetAvailableResidences`, `_GameUtils.lua:356-367` → `CargoRequestNew.lua:358`),
the UI and `Dome:CheckLivingSpace`. Vanilla = tally/gate on `working`,
assignment on `ui_working`; ours = tally/assignment on `ui_working`, gate on
`working`. Neither is consistent; which is better for a player is unmeasured.
REMOVE candidate for hotfix 3, after a measurement (an enabled-but-unpowered
residence + a passenger rocket). Recorded on `bugs/F60.md`. Not a change here.

### F-5 (vanilla, filed not fixed) — 1.1.0's pre-sort pass cannot order a track holding a repair site

`DemolishAndSplitTrack` now runs `track_obj:ProcessAllElements()` before the sort
(`TrackElement.lua:473-476`). `OrderTrackElements` walks by hex (`Tracks.lua:586-596`);
a repair site shares its hex with the hidden broken element (`Track.lua:641-644`),
so the walk comes up short, logs `assert(false, "unable to find the expected number…")`
(`Tracks.lua:616`, on both branches) after rewriting `connections` on the
visited elements, and returns without stamping `node_idx` (`:633` unreached,
`:818-820`). Two consequences: F45 is still live on 1.1.0 and our
`Fix_BrokenTrackSalvage` stamp is still what makes the sort possible (KEEP
confirmed); and every salvage of such a track logs that assert, pack on or
off — our F116 body carries the same pre-sort call by design. Filed as `C55`.
Runtime read owed at the sitting.

### F-6 (robustness, one line) — `Fix_PayloadTemplateRefill`'s probe would decline silently if `FlightPolicies` were ever absent at apply time

`FlightPolicies` is created in `OnMsg.ClassesBuilt` (`CommonLua/Preset.lua:1404-1412`,
`rawset(_G, map, rawget(_G, map) or {})`), and the probe calls
`GetFlightPolicy` → `FlightPolicies[...]` (`ClassDef-Default.generated.lua:99-101`).
Mod `apply()` runs before the current pass's ClassesBuilt. It is safe on both
real boot paths because the pack's apply runs inside a `ReloadLua` after a full
first pass (the 09-08 log: pack block `:74-166`, `Reloading done` `:169`;
`ModsLoadCode` is "called while reloading Lua", `Mod.lua:2283`), and `_G`
persists across the reload. That is a boot-order dependency, not a contract
(the SELFCHECK audit said the same). A throw there is a `probe` decline: no
`update_suspect`, not named in the dialog, F70 silently off. One Require line,
`{ global = "FlightPolicies", kind = "table" }` before the probe, turns a silent
decline into a named one. Rider for the F-1 link; otherwise the sitting's log
line `PayloadTemplateRefill: applied` is the control.

### F-7 (process) — no boot of THIS pack exists, and every census in the chain describes the previous one

The newest log (`17.51.09`, 2026-09-08 17:53) predates the first deletion
(`2dc1dbe`, 21:34). Every `applied` line cited anywhere in the chain is for the
80-module pack. The 44-module pack has never loaded. Pass C's boot-log half is
therefore UNVERIFIABLE today, and so is every new gate (five probes, two
`test`s). **Prediction for the sitting, computed from the 09-08 log and the
module set, not typed: 44 applied / 0 inactive (heal-aware); a first-pass read
may show 43/1 because `SaintBlessing` latches then heals.** Any `inactive` line
is a finding, and eight modules changed their self-check since that boot:
`SaintBlessing`, `PayloadTemplateRefill`, `RocketDroneChurn`, `LandscapeUnitFilter`,
`VacuumWalks`, `TrainCargoDumping`, `GeneForging`, `DroneTransportMinors`.

### F-8 (process, the ck119 mechanism) — a recorded divergence with no checklist number is operationally unrecorded

Asked for by the chain's author. The root cause is that `bugs/` and module
headers are connected to the surfaces work is planned from (checklist, STATE,
a chain folder) by nothing but memory. **Mechanism, no tooling required to
adopt, one gate to enforce:** a deliberate divergence from a shipped body gets
a checklist number *at the moment it is recorded*, written as a machine-readable
header line beside `SRC:`/`DEFECT:` — `-- DIVERGENCE: ck<NN> <one line>` — and
`doccheck` goes RED on a `DIVERGENCE:` line without a `ck`, WARN on the prose
forms ("deliberate divergence", "deliberately diverge") outside one. Count
today, a lower bound from a phrase grep (a name proxy, said so): `Code/` 2 files
(`Fix_BombardmentSpread.lua:33`, a dropped assert — the convention class;
`Fix_TrackSalvageWipe.lua:52`, ruled), `bugs/` 12 hits across 9 entries, most
already numbered. F-4 above is a new one and is filed with a number.

### F-9 (drift corpus, Pass H) — the pattern

Every one of the eight links corrected its own brief: 01 (the "no 1.0.7 game
body" limit, moot two links later), 02 (C54 filed and refuted; 37 rows), 03
(one fixup was two), 04 (the `SRC:` re-stamp instruction, false, in two
prompts), 04b ("reach is Clear-Waste-Rock only", wrong in the wider direction;
"gates decline on 1.0.7" imprecise), 05 ("15 SetGlobal sites" → 5; 63/17 →
64/16; "10 NO-MANIFEST" → 2), 06 ("DEFERRED" mislabel; the spent §12 seed),
07 ("37 orphans / ~45 FAILs" → 12 + 26; "5 stale probes" → 8), 08
(`display_text == nil` would have made the pass inert). Plus this prompt: Pass D
named two KEEP exceptions where six KEEP-side files changed (all ruled), the
"5 bytes of STATE headroom" that the owner's cap raise mooted, and the README
read path still saying the 1.0.7 tree is GONE. **The pattern is not carelessness;
it is that a brief encodes the tree as it was when the brief was written, and
the chain runs after the tree moves.** Numbers typed into a brief are the worst
case: 6 of the corrections above are counts. The rule that caught every one was
chain rule 6 (re-derive the route). ⇒ For `CHAIN_METHOD`: a brief carries the
*command that regenerates* a number, never the number (the STATE build-state
block is the model); and a hand-off note is a claim with a timestamp whose
shelf life ends when a later link's fence covers it (06's own framing).

### F-10 (prompt drift, recorded) — Pass D's "two named exceptions" are six

Files under `Code/` outside the FIX set that differ from `e2490f3`: `00_Core.lua`
(A-2 log string, link 05), `90_SaveSanitizer.lua` (F03 pass removed by 02 under
ck117; F95 pass added by 08, ck126 open), `Fix_DroneTransportMinors.lua` (half
(b) deleted by 02, R-7; its Require now declines the whole module on a miss
where half (b) used to carry it — correct, since (a) is the whole module),
`Fix_GeneForging.lua` (A-1, named), `Fix_TrackConnectorPingPong.lua` (ck125(a),
one line, ruled 09-09), `Fix_TrackSalvageWipe.lua` (F116 ck111/ck119, named).
All six ruled or inbox-explained; none unexplained. Not drift in code.

## 2 · What I verified, and what I could not

### Pass A — instruments, re-run and falsified

`doccheck` GREEN (18 pre-existing frozen-index-row warns, verbatim in the
session summary; STATE 9461 B against warn 12288); `--emit-counts` 45 files /
44 modules / 94 probes / 116 F + 12 D + 54 C. `sigcheck` 43 sites, 0 MISMATCH,
selftest 9 legs. `bodycheck --all` 97 rows, 93 OK / 1 NO-DEFECT / 3 SRC-NONE /
2 NO-MANIFEST (`00_Core`, `90_SaveSanitizer`), selftest 10 legs. `logscan` on
the canonical log: 64 applied / 16 inactive heal-aware, 63/17 first-pass, 0
error-shaped lines, 14 named; selftest 13 legs; `--retire` 0 candidates.
**Falsified by me, not by the tool's own fixtures:** on a scratch copy of
`Code/`, a zeroed `SRC:` hash on `TrainCargoDumping` → `BODY-CHANGED`, exit 1;
a `DEFECT:` rewritten to a string no body holds on `VacuumWalks` →
`DEFECT-GONE`, exit 1; the real F46 defect expression (`Min\(carried,\s*station_cap\)`)
reads OK, not GONE. `bodycheck --src <1.0.7 archive>`: 27 BODY-CHANGED / 1
TARGET-ABSENT, the set link 04b reported. Kit: `parsecheck` 24 files 0 errors,
`aliascheck` 0 findings (both run by doccheck). `upload_preflight`: 20 checked,
0 FAIL, 1 UNCHECKABLE (login); code list = items = disk, 45.

### Pass B — every code change re-derived against the 1.1.0 body

Mechanical three-way diff (comments stripped; ours vs 1.1.0 vs 1.0.7, via
`luafn.find_bodies`) for every copied body, then the shipped lines read:

- **F-1 `SaintBlessing`**: probe strict-`true` via `Require` (`00_Core.lua:151-165`),
  UNKNOWN latches non-benign (`:284-291`); re-base (B) armed only on the resolved
  verdict, keyed on `dome.label_modifiers[label][colonist]` — reachable when the
  pass declines, which the old `rebased_from` heal was not; `ctx.heal()` keeps the
  module active (`00_Core.lua:341-354`). `GetPropScale(1)` is pure (`PropertyObject.lua:1760-1768`).
  Matches QA §0.3.
- **F-2 `StaleReservations`**: one clause; no 1.1.0 body; correct.
- **F-3 `ShelterReflex`**: half (a) gone (diff since `e2490f3` removes only the
  `IsSuitable` replacement and the `applied[]` bookkeeping), half (b)'s wrapper
  body byte-identical; reason string reworded, stated in the file.
- **F-6 `PayloadTemplateRefill`**: `RetrieveRequests` = 1.1.0 minus the assert;
  `resolve_loc_cargo_template` = 1.1.0 + the gate AFTER the tutorial return;
  `Apply` = 1.1.0 + the stamp inside `if not res or res == 1`, both confirmed
  branches, not the cancel branch. Probe reads the destination-pick shape.
  `CargoType` at apply time is measured (the old Require had it, logged applied
  09-08). See §1 F-6 for the `FlightPolicies` dependency.
- **F-7 `RocketDroneChurn`**: 1.1.0 body + the F50 changes; the one branch line
  (`not self.refuel_disabled`, `:1442`) carried; `test` on `UniversalRocketBase`
  (`DefineClass` at `UniversalRocket.lua:28`, `refuel_disabled` in `properties`
  `:70`, `ToggleRefuel` `:3319`) — a shape, not a label; deviation from "probe"
  stated with its reason (`TransportableResourceIds` empty at cold-boot apply).
- **F-8 `LandscapeUnitFilter`**: `(map, mark, callback, ...)` reading
  `map.Landscapes[mark]`, filter passed; F115 gate KEPT with sense inverted; probe
  captures the key the shipped body asks the stub for. `sigcheck` MISMATCH cleared.
- **F-9 `VacuumWalks`**: 98-line 1.1.0 body, one line differs (`or 0`); all
  seven 1.1.0 changes present in the diff; NOT a distance pre-wrapper; the
  accidental path-spec gate is gone, replaced by a `test` + shape specs +
  probe. `const.Colonist.<id>` is populated at definition time (`DefineConst` →
  `GetConstGroup` → `const[group][id]`, `ConstDef.lua:210-221`, `:349-375`;
  `GetGlobalGroup("Colonist")` is nil, `:194-209`) — source-derived.
- **F-10 `TrainCargoDumping`**: 1.1.0 body (both nil-guards, BlackCube hook
  `:800-802`) + the F46 guard; F114 gate KEPT inverted; probe feeds the F114
  input. `BlackCubeMystery_AdjustStored` is a plain global (`BlackCubes.lua:33`).
  `route_accepts_elsewhere` indexes `city.train_track_routes[train.track]`, keyed
  by track on 1.1.0 (`TrainTransport.lua:308`, `Train.lua:44`). ⛔ Premise unread,
  and every surface says so (`F46`, `F114`, the header, the change note's
  "re-enabled"). The 10-second console read at the sitting decides.
- **F116 `TrackSalvageWipe`**: the diff since `e2490f3` is exactly the header
  rewrite + the split-branch tail: vanilla's rehome loop (`:580-595`) verbatim with
  a `tracks` list built from the seeded sides, vanilla's tail (`:597-608`) as a
  counted loop, combined-list processing through `ProcessTrackElements`
  (= `TrackBase:ProcessAllElements`, `Track.lua:466-469`). **04b's residue question
  answered mechanically: of the 12 1.0.7-only lines in this function, 0 remain in
  our body.** Everything else ours differs in from 1.1.0 is K-11's settled
  F44/F45/F91 guarding. No gate, by design; not re-derived (K-11).
- **A-1 `GeneForging`**: `Techs.GeneForging:ResolveValue("param1")` is what the
  shipped body does for GeneSelection (`Colonist.lua:4398-4402`); `IsTechResearched`
  is a global on 1.1.0 (`Tech.lua:468`); vararg kept. 04b's "drop the unit" note
  would have broken 1.0.7 — link 05 caught it; confirmed.
- **ck125 `TrackConnectorPingPong`**: one line, `(force or not owned_by_live_other)`,
  mirrors 1.1.0's relaxed assert (`TrainTransport.lua:129`).
- **Link 08 `90_SaveSanitizer` F95 pass**: value fields `prop`/`percent`/`amount`/
  `display_text` are what `Effect_ModifyLabel:OnApplyEffect` writes
  (`MarsGameEffects.lua:277-283`); `display_text` stays the class default `false`
  when `Reason` is empty (`:269-276`, `Modifiers.lua:228-235`); the deleted module
  placed `Percent = 10`, no Amount, no Reason (`2dc1dbe^:Fix_AstrogeologistExtractors.lua:67-70`,
  `:131-135`); the key test mirrors vanilla's own fixup (`:325-334`). **No vanilla
  effect matches the shape** — the only `Label = "AutomaticMetalsExtractor"` /
  `"MicroGAutoWaterExtractor"` hits in `Data/`+`Lua/`+`DLC/` on either branch are
  `ScriptCheckLabelCount` (`FactionDef/Japan.lua`), not `Effect_ModifyLabel`. The
  pass cannot remove a vanilla bonus. No flag: overturnable, I do not overturn it.

### Pass C — the deletions, in four places

`Code/` 45, `items.lua` 45, `metadata.lua` code list 45, symmetric differences
empty (script + doccheck's MODULE SETS gate + `upload_preflight`). All 36
deleted ids listed by name in the session scratch (`deleted_ids.txt`), none in
any of the three. **Boot log: UNVERIFIABLE** — the only logs predate the
deletion (§1 F-7). **Site, committed:** 46 entries (`grep -c '^??? '`), all 46
titles map to a live module (mapped by hand, one entry each for the sanitizer's
F35/F48 and WispRewards' two defects, two for ShuttleHub); no deleted module's
symptom survives. **Site, LIVE:** fetched today — 82 `<details>` (76 success +
6 question), `Eighty-two` still on the page. Consistent with v5, wrong for v6.
Save cleanups: F-1's re-base keyed as §0.3; F-5's keyed on `prop` + label +
`Percent`/`Amount` + `IsKindOf` (narrower than §0.2 specced, and said so).

### Pass D — the KEEP set, and the wrappers re-read against their branch diff

35 KEEP modules: six files differ from `e2490f3`, all explained (§1 F-10).
Wrapper re-read (owner-ruled mine, per module): branch diffs generated for all
58 pinned/unpinned targets (`scratchpad/branchdiff/`), and every KEEP module
whose target changed was read by one of four fresh readers against the diff and
the shipped lines, with every FINDING re-opened by me on the shipped tree:

| module | target(s) changed | verdict |
|---|---|---|
| ArrivalDeaths | `OnArrival` 4, `Idle` 58 | **FINDING → F117** (§1 F-1) |
| LayoutTechLock | `Activate` 5 | **FINDING → F118** (§1 F-2) |
| DomeFreeSpaceMismatch | `GatherFreeLivingSpaces` 13 | **FINDING → F60 addendum** (§1 F-4) |
| BrokenTrackSalvage | `BreakTrackElement` 8, `DemolishAndSplitTrack` 53 | SURVIVES; vanilla residue → C55 (§1 F-5) |
| ExtenderFlapChurn | `OnSetWorking` 4 | SURVIVES; 1.1.0's new orphan-drone gather on power-up now sits inside our 2 s debounce — noted on F77 |
| LakeEntombment, GhostFarmOxygen, JumboCaveReinforcementWedge, MirrorSphereSite, AnomalyCaveInMap, SinkholeIndestructible (formatting only), DestroyedTunnels, TrackSalvageRefund, TrackConnectorPingPong `Done`, TrainsToVoid, TrainWaitTime, LanderEmptyLaunch, RocketInteractGuard (wraps, does not copy — 04b's table said copy), FreedHousingNotice, ShelterReflex (`Idle`) | 2–16 lines each | SURVIVES, each with a falsifier in the readers' reports |
| WispRewards, ShuttleTransportCache, SequenceLatents, CrystalMysteryHang, TrackTunnelPowerBridge, NightShiftWork, FounderTraitNotification, GraphConsumedCaption, DomeOverviewHighlight, TrainWaitTime, BombardmentSpread | 0 changed | SURVIVES (confirmation reads) |

Not opened by anyone: `Unit:ExitImpassable`'s C side; the engine's handling of
a thrown command thread (bears on F117's player-visible shape); `UndergroundMap`
defaulting; `Demolishable:DoDemolish` 1.1.0; two stale module comments
(`JumboCave:102`, `AnomalyCaveInMap:106`) → doc sweep.

### Pass E — the 1.0.7 constraint

No version detector anywhere in `Code/` (grep for `lua_revision`, `LuaRevision`,
`ModMinLuaRevision`, `403908`, `396349`, `GameVersion`, `IsObsolete`: 0 hits).
Every module carrying a 1.1.0 body declines per module: F-1 probe; F-6 probe;
F-7 shape `test`; F-8 `test` + probe; F-9 `test` + shape specs + probe; F-10
`test` + probe. F116, A-1, ck125 and the F95 pass carry no 1.1.0 body and are
dual-branch by construction. ⛔ **No 1.0.7 decline has ever been booted on 1.0.7**
— structurally impossible on this rig (Steam holds one branch, ck98). All
argued from the archived tree and 04/04b's desk harnesses.

### Pass F — text against reality

Mechanically (`scratchpad/verify_sync.py`): `description` 5342 chars == the
§3 plain block, 0 differing lines; §3 BBCode == `STORE_CARD_LIVE` BBCode;
`last_changes` == the change-note block; `short_description` == the summary
block; `STORE_CARD_LIVE` plain = +143 chars, exactly the two portal passages,
by design. Fix-list count 46 recounted; "three ... cannot see" = 3 entries under
*Under the hood*; judgment calls 3 on the list, "Three" in `faq.md` ×3 and
`index.md`. Every one of the 20 "SOME OF WHAT IT FIXES" bullets and the four
headline clauses maps to a live module. **Claims that no one has confirmed
(every one is a claim under the 09-08 rule):** bullet 3 in full ("works again",
"keep the home", "no longer causes an error"), bullet 4 in full ("respects",
"works with", "re-enabled", "kept on its own track"), bullet 1's "a few of ours
had quietly become slightly worse" (R-6/R-23/R-30/R-33, source-read), bullet 2's
train-count line (R-34). Bullet 5 disclaims all of them in the player's words;
acceptable at this bar, and named here so the sitting knows what it is
confirming. **False if link 08's pass ships:** bullet 2's "cannot take back"
(§1 F-3). ck112 bullet 3: still overpromises, ruled to ship so, not flagged;
with five modules now on behaviour probes it is truer than in v5 and still not
true in general (class (c) — F117 is a fresh instance).

### Pass G — what has not been run in a game (I move no status)

Everything this patch built. Specifically: the five probes and two shape tests
(never evaluated in a boot); the F-1 re-base (never touched a save; its log
line is one-shot per save — do not load the poisoned save before the sitting);
F-2's expedition exemption; F-3's throw removal (never reproduced); F-6 (dialog,
pick, tutorial, cancel); F-7 (toggle); F-8 (no landscaping site on 1.1.0 with
this body; needs a Dozer Rover + the mid-tree tech, `EF-083`); F-9 (vacuum walking
never exercised on 1.1.0 at all); F-10 (no train unloaded since F114; premise
unread); F116 (destructive, save-persistent, changed twice, never reproduced —
row 6 matters most); A-1 (desk ladder only); ck125 (no rig control exists);
the F95 pass (no save loaded with it); the 32 `retired` and 8 rewritten kit
probes; the 44/0 boot census; PT-20 uninstall safety on 1.1.0 (verified on 1.0.7
only); every 1.0.7 decline. Claims resting on source reads alone: all of the
above, plus every KEEP verdict in Pass D.

### Instruments audited, and their blind spot

Four tools, each falsified: they see classes (a) (b) (d) (e) (f). **Class (c)
— semantics moving under a wrapper — is still seen by nothing, and this audit
found three new instances of it in the KEEP set by reading (F117, F118, F60).**
That is the honest reason the description's bullet 3 stays false and the reason
a green run is not a clearance.

## 3 · The chain's shape, audited

The 04/04b split was right and pre-authorised. 07 and 08 were added mid-run:
07 because no fence owned the Test Kit (a decomposition miss the author named),
08 because the owner reversed ck120 — the reversal is now ck126 and is the
owner's to re-rule, not drift. The ck111 reversal (delete → rehome) is defensible
on the machinery argument and the code matches vanilla's loop verbatim; the
risk stated when (a) was recommended has not gone away, and row 6 of the sitting
is where it is paid. The one structural fault: 06 (text) ran before 08 (code),
so the change note describes a pack link 08 then changed (§1 F-3). Rule for
`CHAIN_METHOD`: the text link runs last-but-one, or re-runs.

## 4 · What would make this half-baked

1. **Shipping F117 knowing.** A throw in a colonist command thread naming the
   pack, on an ordinary colony, in a module the patch leaves untouched — the
   F115 shape the owner just paid for.
2. Shipping bullet 2 as written with the F95 pass in the pack, or shipping the
   pass without re-ruling ck120 (item 126).
3. Uploading without publishing the site in the same sitting — the card says
   forty-six and sends the reader to a page that says eighty-two.
4. Reading the sitting's boot log against the old prediction. It is 44/0 for
   this pack; any `inactive` line is a probe that declined on 1.1.0.
5. Loading the SaintBlessing poisoned save before the sitting (perishable evidence).
6. F-10's guard on an unread premise: if `GetTargetAmount` reads 0 for a
   suspended request the module is inert and the fix-list entry "Trains dumped
   cargo at stations you had told not to store it" describes nothing.
7. A `FlightPolicies` boot-order surprise silently switching F70 off (§1 F-6).
8. F116 never having run: destructive, save-persistent, two behaviour changes.
9. Treating the 46-entry committed page as deployed — it is not (`workflow_dispatch`).
10. Treating any KEEP verdict as re-verified: three of 35 moved under their
    wrappers and no instrument saw it.

## 5 · The changes

| # | where | what to write |
|---|---|---|
| 1 | `Code/Fix_ArrivalDeaths.lua:201` (+ a probe in the kit) | F117: pass the colonist on the 1.1.0 body behind a per-module runtime discriminator; one small link, fresh context, `Mars.exe` closed; then `bodycheck`/`sigcheck`/`parsecheck`; a kit probe on the re-choose branch |
| 2 | `Code/Fix_LayoutTechLock.lua` (rider on 1) | F118: read `s_ConstructionControllerDeleteOnLoad` before the teardown loop; if it was `self`, re-assert it after |
| 3 | `Code/Fix_PayloadTemplateRefill.lua` Require (rider on 1) | `{ global = "FlightPolicies", kind = "table" }` before the probe |
| 4 | `metadata.lua` `last_changes` bullet 2 + `UPLOAD_WORKFLOW` §3 + `STORE_CARD_LIVE` + `faq.md:114-118` | after ck126: if the pass ships, "…and a small Astrogeologist bonus an earlier version of this pack gave two extractor types is removed from an existing save the next time it loads"; if not, the sentence stands and the pass comes out. Both drafts in `100_DOCSWEEP.md` |

None made by me. Each is somebody else's prompt; the executor is the wrong
person to certify its own rewrite, and the auditor is the wrong person to
execute.

## 6 · Owed AFTER upload, and by whom

- **The one consolidated sitting** (owner, with the on-call session; ruled
  09-08): boot → `logscan` (prediction 44/0, named exceptions above) → `RunAll()`
  against the LINK 07 census → rows 1–10 controls → the `SaintBlessing: restored`
  line on the poisoned save → `SaveSanitizer: F95` line → the F-10 console read
  → F116 row 6 → the F117 control if unfixed. Status words move only then, by
  that session.
- Publish the site in the same sitting (`UPLOAD_WORKFLOW` §4).
- `WORKFLOW.md:407`'s suite baseline re-stamped after the sitting (link 07's
  filing); `bugs/F115.md` `:10`/`:14`/`:168` "17 inactive" → live-claim wording
  (link 05's filing); both in `100_DOCSWEEP.md`.
- Hotfix 3 candidates, after measurement: F60 disposition (§1 F-4); C55 runtime
  read; the F46 REMOVE question if the console reads 0.

## 7 · Kickoff

`prompts/hotfix2/100_DOCSWEEP.md` — authored by this audit, first-class, fires
after the owner rules 126 and 127. Then the sitting.

## 8 · Bindings honoured

No code edited. No game launched. No Mod Editor, no `version` edit, no upload,
no portal API. Game trees read only. No status moved; no `tested` granted.
Four fresh readers' findings were re-opened on the shipped lines before any was
relayed. `doccheck` result and its warns are in the session summary verbatim.
