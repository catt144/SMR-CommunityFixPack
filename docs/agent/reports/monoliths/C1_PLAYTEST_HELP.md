> ⛔ **SUBAGENT OUTPUT — THIS IS A CLAIM, NOT A FINDING.** Produced 2026-09-14 by a read-only
> characterisation agent under checklist **181**. Only the items graded **CONFIRMED** in
> [`../C1_MONOLITHS.md`](../C1_MONOLITHS.md) were re-derived by the orchestrator seat; everything
> else here is unverified. ⚠️ At least one claim in this set was materially imprecise — read the
> adjudication first, and never quote a number from this file without re-deriving it.

# C1 — docs/PLAYTEST_HELP.md characterisation

Read in full (721 lines, 63,429 B, two Read calls: 1-582, 583-721). Read-only job; no edits made, no writing git commands run.

**Standard applied per the brief: this is a human-facing reference doc for the owner mid-playtest. Density is a feature. The verdict axis is staleness/correctness of what it tells the owner to type or expect — not length.**

---

## 1. Section inventory (by size, descending)

| Bytes | Lines | Heading |
|---|---|---|
| 15,955 | 353-416 | `### Verified command reference (every entry checked in ModTools\Src)` |
| 9,537 | 218-352 | `### Console: what works and what silently does nothing` |
| 6,136 | 417-480 | `### Test Kit helpers (names read from TestKit\Code\90_Loggers.lua / 00_TestCore.lua)` |
| 4,371 | 492-558 | `## The ENABLE-PATH leg — the session shape the harness never measured` |
| 4,113 | 98-158 | `### Cheating without contaminating results` |
| 4,011 | 628-687 | `## The co-run rig — how an agent-driven launch actually runs` |
| 3,900 | 12-67 | `## Ground rules` |
| 3,092 | 559-605 | `` ## The MarsDebug `[install]` pass `` |
| 2,788 | 688-707 | `## Save fixtures — create these once, reuse them` |
| 1,957 | 68-97 | `### ⚠️ EXTERNAL VALIDITY — how far our results generalise` |
| 1,793 | 189-217 | `### Salvage mode — how to read the cursor` |
| 1,752 | 159-188 | `` ### ⚠️ Compressing a scheduler with `g_Consts` — the false-PASS trap `` |
| 1,517 | 710-721 | `## Commands cited in the archived TESTING.md that could NOT be verified` |
| 1,417 | 606-627 | `### ⛔ NEVER read a MarsDebug tally as a retail tally` |
| 609 | 481-491 | `### Harness quick facts` |
| 481 | 1-11 | `# Playtest Help — setup, commands, reference` (intro) |

Purpose one-liners: intro = doc's own scope statement; Ground rules = the 8 binding rules for any test; External validity = how far results generalise; Cheating section = SMR Tool Kit walkthrough; g_Consts trap = a specific debugging trap write-up; Salvage mode = cursor-reading facts; Console section = sandbox/console mechanics + a big table; **Verified command reference = the payload — the console command table**; Test Kit helpers = the SMRTest.* API table + stress harness; Harness quick facts = three misc facts; ENABLE-PATH leg = a specific test procedure + its one executed run; MarsDebug pass = a specific procedure + its one executed run; NEVER-read-tally = a standing warning; co-run rig = agent-launch mechanics + 4 executed runs; Save fixtures = build-once recipes; archived-TESTING.md table = a "do not use" list.

---

## 2. STALENESS — the headline

### 2A. The verified command table is substantially broken against the CURRENT 1.1.0.403908 tree

I read the current `A:\SteamLibrary\steamapps\common\Project Spark\ModTools\Src` (mtime 2026-09-08, matches the 1.1.0.403908 baseline per `docs/agent/facts/EF-075`/STATE.md) and diffed it against every callable the table cites. This tree switched the cheat system from standalone global `CheatXxx()` functions to a data-driven `Data/CheatDef.lua` registry whose `run =` closures often inline the logic instead of calling a named function. Net effect: **several console commands the doc tells the owner to type no longer exist as callables at all.**

**Confirmed GONE (zero hits, `grep -rn "function.*\bNAME\b"` over the whole `Lua/` + `CommonLua/` tree):**

| Doc row | Cited at | Current state |
|---|---|---|
| `CheatFillAllStorages()` | `Lua/Buildings/StorageDepot.lua:2020` | **Gone.** `CheatDef.lua:391` id `"FillAllStorages"` now inlines `AllMapsForEach(true, "MechanizedDepot", "StorageDepot", function(o) o:CheatFill() end)` — no wrapper function exists. |
| `CheatResearchAll()` | `Lua/Cheats.lua:78` | **Gone from Cheats.lua** (current `Cheats.lua` has 33 top-level functions, none named this — full list checked). Logic lives inline in `CheatDef.lua:852` id `"ResearchAll"`. |
| `CheatToggleAllShifts()` | `Lua/Cheats.lua:192` | **Gone.** Inline in `CheatDef.lua:1309` id `"ToggleAllShifts"`. |
| `CheatUnlockAllTech()` | `Lua/Cheats.lua:166` | **Gone** — no `CheatDef` id either found for a plain "UnlockAllTech" (only `UnlockAllBreakthroughs`/`UnlockBreakthroughs` remain, see below). |
| `CheatUnlockAllBreakthroughs()` | `Lua/Cheats.lua:281` | **Gone as a function.** Inline in `CheatDef.lua:900` id `"UnlockAllBreakthroughs"`. |
| `CheatUnlockBreakthroughs()` | `Lua/Cheats.lua:264` | **Gone as a function.** Inline in `CheatDef.lua:936` id `"UnlockBreakthroughs"`. |
| `CheatClearForcedWorkplaces()` | `Lua/Cheats.lua:214` | **Gone.** Inline in `CheatDef.lua:1297` id `"ClearForcedWorkplaces"`. |
| `CheatSpawnPlanetaryAnomalies()` / `CheatBatchSpawnPlanetaryAnomalies()` | `Lua/Cheats.lua:26` / `:38` | **Both gone.** Inline in `CheatDef.lua:564`/`:485`. |
| `CheatOpenAllDomes()` / `CheatCloseAllDomes()` | `Lua/Cheats.lua:414` / `:426` | **Both gone.** Inline in `CheatDef.lua:1040`/`:1059` (bodies now call the *other* doc row, `OpenAllDomes(MainCity)`, directly). |
| `SetGameSpeedState("ultra")` | `Lua/X/HUD.lua:528` | **Gone from the entire tree** — zero hits, case-insensitive, anywhere. This is the doc's own suggested way to hit ultra speed. |

For every one of these, typing the command in console on the current build should raise `attempt to call a nil value` (the doc itself, at line 268, teaches the owner that this is what an unavailable global looks like) — not the behaviour the row promises. The in-game *capability* usually still exists (reachable through the DevMenu cheat menu, which reads `CheatDef.lua`), but the **console shortcut the doc hands the owner does not**.

**Confirmed present but with drifted `file:line` citations** (the doc's own framing is "every entry checked in `ModTools\Src`" — this is no longer true for the citation, even where the function survives):

| Function | Doc cites | Now at |
|---|---|---|
| `CheatCompleteAllConstructions()` | `Cheats.lua:118` | `:89` |
| `CheatCompleteAllWiresAndPipes()` | `Cheats.lua:99` | `:55` |
| `CheatAddFunding(n)` | `Cheats.lua:132` | `:103` |
| `CheatUnlockAllBuildings()` | `LockablePreset.lua:626` | now in **`Cheats.lua:138`**, a different file entirely |
| `CheatUnlockAllSponsorBuildings()` | `Cheats.lua:337` | `:236` |
| `MultiCheat()` | `Cheats.lua:328` | `:227` |
| `CheatSpawnNColonists(...)` | `Cheats.lua:225` | `:169` |
| `CheatUpdateAllWorkplaces()` | `Cheats.lua:210` | `:156` |
| `CheatMeteors(...)` | `Cheats.lua:62` | `:40` |
| `CheatStopDisaster()` | `Cheats.lua:74` | `:51` |
| `CheatRevealDarkness()` | `Cheats.lua:390` | `:262` |
| `dbg_ToggleRocketInstantTravel()` | `RocketUtilities.lua:451` | `:546` |

**Signature change, not just a line move:** `CheatDustDevil(major, setting)` (doc row, the largest single row in the whole document — ~35 lines of hedged corrections) is now `function CheatDustDevil(major, setting, pos)` — a third parameter was added. I did not have budget to re-verify the whole electro-devil recipe against the new signature/body; flagging as **unverified, not confirmed-broken**.

**Confirmed still resolve cleanly** (function present, at least one definition found; line drift not individually checked beyond the sample above): `OpenAllDomes`/`CloseAllDomes` (Dome.lua), `SetTerraformParamPct`/`GetTerraformParamPct`, `RestartPeriodicRepeatThread`, `MapGameTimeRepeat`, `CheatTriggerMarsquake`/`CheatTriggerUndergroundMarsquake`/`CheatTriggerUndergroundCaveIn`, `CheatStartMystery`, `CheatFinishMystery`, `CheatDustStorm`, `CheatGenerateApplicants`, `UnlockUnderground`, `OnDiscoveryCompleted`, `CompleteMilestone`, `ColonyGetPrefabs`, `OpenCommandCenter`/`CloseCommandCenter`, `SetLightTrapMode`, `UIColony:SetGameSpeed`, `CheatMapExplore` (only one whose line, `:5`, is unchanged).

**New cheats that exist now and aren't mentioned** (secondary finding, not required by the brief but load-bearing for "would the owner find what they need"): `CheatDiscoverAsteroid(mode)` (`Cheats.lua:274`) looks like a direct replacement for the doc's manual `UIColony:OnDiscoveryCompleted("Asteroid", false, true)` recipe used in SAVE-E; `CheatMaxColonistStats(lock)` (`:283`) looks like a direct replacement for the doc's "DevMenu Max All Stats (Temp) equivalent... set comfort/health/sanity... inline per colonist" row, which currently tells the owner to hand-edit colonists one at a time.

### 2B. `SMRFixPack.ListFixes` row (line 431) — the single most consequential stale line for a live playtest

The doc says: *"since the opt-in split (2026-08-12)... every registered fix in this pack is now default-active and the gate reads **74/74** in every configuration."*

`python tools/doccheck.py --emit-counts` (a derived fact, one command, HEAD-stamped) currently reports:

```
COUNTS: 47 Code/*.lua files, 46 registered modules (46 default-active, 0 files carry optional = true), 97 probes
```

**Current truth is 46/46, not 74/74.** Cross-checked against `docs/agent/STATE.md`'s "Now" block, which records a chain of module retirements after the 08-12 snapshot the doc row is keyed to: v10's "C85+C89+C88 in, F37/F43+F118/F31 out", and "`GhostFarmOxygen`/`LayoutTechLock`/`AnomalyCaveInMap` (modules retired 09-12)". An owner running `SMRFixPack.ListFixes` mid-playtest today and seeing `46/46` — a number roughly 40% smaller than the doc's number — has no way from this doc alone to know that's expected rather than a broken install.

The doc's own citation for the log line (`TestKit/Code/00_TestCore.lua:351`, itself already flagged in-doc as a correction from an earlier `:286`) has drifted again: the line is now `TestKit\Code\00_TestCore.lua:459`.

The opt-in-pack half of the same row (`SMROptInPack.ListFixes`, line 432, "reads `1/8`") is **still correct** — checked `python tools/doccheck.py --emit-counts` in `C:\Dev\SMR-OptInPack`: `8 registered modules (1 default-active, 7 files carry optional = true)`.

### 2C. Probe-suite tallies are stale, and the doc doesn't know the current number is *unknown*

Line 619-624 states the "both-mods retail read" as of 2026-08-13 is `78 PASS / 16 SKIP` of 94 probes. The most recent actually-measured tally I could find in the repo is from 2026-09-11 (`docs/agent/reports/F106_AUDIT.md:119`): `75 PASS, 1 FAIL, 24 SKIP, 0 ERROR` of **100** probes — a different total from either the doc's 94 or the current tree's 97 (`doccheck --emit-counts`, above). More importantly, `docs/agent/STATE.md`'s "Now" block explicitly lists as **OWED**: *"the first `RunAll()` on the probe kit (re-stamps `WORKFLOW.md:537`, **VOID since 09-09**)."* The current true tally is not just different from the doc's number — it is **not yet measured** by the project's own record. The doc presents `78/16` as current fact with no such caveat.

### 2D. Tombstone — `Fix_MeteorStormWedge` no longer ships (confirmed, highest-priority actively-wrong finding)

Line 369 (inside the huge `CheatMeteors` row) tells the owner: *`"storm"` reliably WEDGES (F78) — with the pack loaded, `Fix_MeteorStormWedge` heals it automatically ~2 game hours after the storm notification expires... manual recovery remains `*g for i = 1, 10 do g_MeteorStormStop = true Sleep(4000) end`.*

`git show 2dc1dbe --stat` (commit titled "hotfix2 link 02: the 36 REMOVE deletions...", 2026-09-08) shows:
```
 Code/Fix_MeteorStormWedge.lua            | 219 --------------
```
The module is gone from `Code/` (confirmed: `find Code -iname "*MeteorStorm*"` — zero results). The project's own bug file says so explicitly, `docs/agent/bugs/F78.md:350`:
> `⇒ Fix_MeteorStormWedge — removed from the pack in hotfix 2 (re-verification row R-10; ...`

**This is the one place in the document where following the written advice actively misleads the owner about safety net that no longer exists.** An owner who deliberately triggers `CheatMeteors("...", "storm", ...)` on the strength of this row, expecting the auto-heal, will get a wedged storm with no automatic recovery — only the manual `g_MeteorStormStop` loop the doc lists as a fallback still applies.

### 2E. Tombstone — `Fix_TechDescriptionBuilding` (F98/F25) also removed in the same commit

Not directly cited by name in PLAYTEST_HELP.md's body, but the doc's "NEVER read a MarsDebug tally as a retail tally" section (lines 606-624) leans its entire teaching example on this module still shipping and being live: *"`Fix_TechDescriptionBuilding` genuinely works here and is a no-op in the build players use."* Same commit (`2dc1dbe`) deleted `Code/Fix_TechDescriptionBuilding.lua` (97 lines) entirely. The MarsDebug-vs-retail *lesson* (a debug build passes probes that are silently vacuous on retail) is still a valid teaching point in the abstract, but its worked example now cites a module that does not exist in the shipped pack any more — so a reader who goes looking for `Fix_TechDescriptionBuilding.lua` to understand the example will not find it.

### 2F. Save fixtures — cannot confirm any of SAVE-A/D/E/F/(Mirror Sphere) currently exist, and the branch-lock fact makes pre-09-08 builds of them unloadable

`docs/agent/facts/EF-079.md` (verified 2026-09-08) states as fact: *"1.0.7 SAVES DO NOT LOAD ON 1.1.0"* and names, exhaustively, *"the whole playtest save library"* that is branch-locked: `USA Sol 302`/`Sol 298`, `F95 Baseline`/`F95 fresh`/`f95 healed`, `F90 Alert`, `F59 Test1/test2`, `T1-UNINSTALL(-R)`/`T2-Uninstall(-R)`, "and the rest." **None of SAVE-A, SAVE-D, SAVE-E, SAVE-F, or the Mirror-Sphere fixture appear in that exhaustive list**, nor in a full listing of the one live save folder (`Saved Games\Surviving Mars Relaunched\76561198020568696\`, 24 `.sav` files, none named `SAVE-*` or matching the doc's fixture descriptions) or anywhere in `STATE.md`/`facts/*.md` (zero grep hits for the literal strings). Two readings are consistent with this: (a) these fixtures were built once under different real filenames the doc doesn't record, or (b) the "Save fixtures" section is an unexecuted recipe list rather than an inventory of things that exist. **I cannot tell which from the evidence available, and I want that stated plainly rather than asserting either.** What I *can* say: if any of them were built before 2026-09-08 under any name, EF-079/EF-080 mean they are now unloadable on Steam without the `config.OldSavegameBehavior` override (triage-only per EF-080, never a verdict). The doc's own retirement note for SAVE-B/SAVE-C ("no longer needed") shows the section IS actively maintained for at least some entries — so the silence on SAVE-A/D/E/F's branch status looks like a genuine gap, not a deliberate omission.

### 2G. TestKit helpers — mostly solid

Checked the actual TestKit repo (`C:\Dev\SMR-BugFixPack-TestKit\Code\`). All of `90_Loggers.lua`, `00_TestCore.lua`, `91_Stress.lua`, `95_AutoRun.lua`, `96_AutoRunFlag.lua`, `98_EnablePathLeg.lua` exist. Confirmed defined: `SMRTest.RunAll`, `SMRTest.EnableIntrospection`, `SMRTest.SourceOf`, `SMRTest.ReportBrokenTrack`, `SMRTest.ReportReservations`, `SMRTest.ReportTrains`, `SMRTest.Stress.{Targets,Break,Report,Compare,HealAll,Stop}` (as documented comments matching the doc's table), `SMRFixPack.ListFixes` (defined in the main pack's own `Code/00_Core.lua`, not the TestKit — the doc doesn't say which repo, which is fine), `SMROptInPack.ListFixes` (defined in `C:\Dev\SMR-OptInPack\Code\00_Core.lua`). The one file the doc tells the owner to create ad hoc, `97_OptInLeg.lua`, correctly does **not** exist (it's meant to be a temporary drop-in, per the doc's own instructions) — not a defect.

---

## 3. Tombstones (summary — full evidence in §2)

| Quote | Referent gone | Proof command |
|---|---|---|
| Line 369: "`Fix_MeteorStormWedge` heals it automatically ~2 game hours after..." | Module deleted 2026-09-08 | `git show 2dc1dbe --stat \| grep MeteorStormWedge` → `219 --------------`; `docs/agent/bugs/F78.md:350` states removal explicitly |
| Line ~614 (worked example): "`Fix_TechDescriptionBuilding` genuinely works here" | Module deleted 2026-09-08, same commit | `git show 2dc1dbe --stat \| grep TechDescriptionBuilding` → `97 ------` |
| Row 359: `CheatFillAllStorages()` at `StorageDepot.lua:2020` | Function removed from source | `grep -rn "function CheatFillAllStorages" ModTools/Src` → 0 hits |
| Row 362: `CheatResearchAll()` at `Cheats.lua:78` | Function removed | `grep -n "^function " Lua/Cheats.lua` → not in the current 33-function list |
| Row 367: `CheatToggleAllShifts()` | Function removed | same method, 0 hits |
| Row 391: `CheatUnlockAllTech()`/`CheatUnlockAllBreakthroughs()` | Both removed as functions | 0 hits each |
| Row 392: `CheatUnlockBreakthroughs()` | Removed as function | 0 hits |
| Row 393: `CheatClearForcedWorkplaces()` | Removed as function | 0 hits |
| Row 397: `CheatSpawnPlanetaryAnomalies()`/`CheatBatchSpawnPlanetaryAnomalies()` | Both removed as functions | 0 hits each |
| Row 382: `CheatOpenAllDomes()`/`CheatCloseAllDomes()` | Both removed as functions | 0 hits each |
| Row 388: `SetGameSpeedState("ultra")` | Removed from entire tree | 0 hits, case-insensitive, tree-wide |
| Row 431: "`#SMRFixPack.order` = 74... gate reads `74/74`" | Now 46 | `python tools/doccheck.py --emit-counts` → `46 registered modules` |

---

## 4. Dated session records (partial inventory — boundary stated)

These are the clear, large cases; smaller dated asides are sprinkled through nearly every console-fact bullet (e.g. "measured 2026-08-01", "found the hard way 2026-07-29") and I did not catalog those individually — that would require re-reading every bullet a second time, which I didn't budget for. The ones below are structurally session narration, not standing reference, and are candidates to move to `docs/archive/SESSION_LOG.md`:

| Lines | Bytes (approx) | What it narrates |
|---|---|---|
| 532-539 | ~700 | "✅ EXECUTED ONCE, 2026-07-31 19.09" — the specific run of the ENABLE-PATH leg, its `68/74` → `63/0/15/0` result, the two log lines it produced |
| 561-565 | ~500 | "✅ EXECUTED ONCE, 2026-08-03" — the specific MarsDebug run, its `87 PASS, 0 FAIL, 0 SKIP` result, its log filename |
| 630-632 | ~350 | "✅ EXECUTED FOUR TIMES, 2026-08-04" — the four co-run executions and their raw log filenames |
| 670-680 | ~900 | "⭐ Three numbers added 2026-08-04 by unattended-1 cycle 0" — save-cost/load-cost/boot-cost measurements from one specific cycle |
| 375 (row): "✅ [RAN 2026-09-11, F119 sitting]" | ~150 | inline in the command table, narrates one specific execution |
| 395 (row): "✅ [RAN 2026-08-04, log...]" (CheatDustStorm) | ~200 | inline in the command table, narrates one specific execution |
| 394 (row): the whole DustDevil correction chain ("Row corrected 2026-08-04...", "RAISES. Measured: 34 of 40 calls...") | ~2,400 | this is the single largest embedded session narrative in the doc — three rounds of dated correction inside one table cell |

**Tension to flag explicitly:** the brief's own framing says dated session records "belong in `docs/archive/SESSION_LOG.md`." But several of these (the ENABLE-PATH and MarsDebug "EXECUTED ONCE" lines) are the doc's *only* evidence that the procedure above them was ever actually run rather than merely written — the doc states this rule itself ("the standing rule: a test's own procedure is unverified until it has been run"). Moving the proof-of-execution sentence out could leave the procedure looking untested. I'm flagging this as a genuine design tension, not resolving it — that's for the orchestrator/owner.

---

## 5. Superseded-in-place

**I did not find a confirmed case meeting the brief's evidence bar** (quote both sides, original still sitting in full) in the time available. The doc has several self-correcting passages (F101's inspector-attribution correction at lines 290-296; the CheatMeteors mechanism correction at ~line 369; the DustDevil `table.copy`/`SessionRandom:Random` corrections at line 394), but in each case I checked, the **original wrong text was edited away and replaced**, not left duplicated alongside the correction — the correction paragraph *describes* what the row used to say, in past tense, rather than the old text sitting in full as its own block. This is a PARTIAL finding: I read the whole document once; I did not diff it against prior git revisions line-by-line to rule out an older duplicate the current text doesn't reference. If the orchestrator wants that ruled out with certainty, it needs a `git log -p` pass I didn't budget for here.

---

## 6. Rules inventory (binding statements — for the pending "rules header" pass)

**Ground rules block (lines 12-67), the explicit numbered list:**

| Line | Rule | Binds |
|---|---|---|
| 14-21 | NO third-party mods; only console, shipped `Cheat*`, `g_Consts`/`const`, Test Kit helpers | Owner |
| 22-23 | Both mods stay enabled for every test except PT-20 | Owner |
| 24-25 | Test Kit must NEVER be uploaded anywhere | Owner |
| 26-31 | Achievements stay ON; cheat use blocks that save's further unlocks | Owner (informational + behavioural) |
| 32-39 | ⛔ HARD RULE: no live UI-internals prototyping in a play session; only read-only hooks (call orig, print, mutate nothing) | Owner + agent |
| 40-41 | If setup fails, write that down — a valid result | Owner/agent |
| 42-62 (numbered "5a") | ⭐ Default is a WARMED-UP save, not as-saved, unless told otherwise; three binding consequences on the rider's author (say so explicitly if as-saved needed; never write "play for a while first"; record which state the reading actually got) | Whoever authors a test rider |
| 63-66 | Use dock icon / Ctrl-Shift-F11 for the toolkit; console via Enter/Alt-Shift-C | Owner |

**Scattered ⛔/⚠️ hard rules outside the numbered list** (non-exhaustive — these are the ones stated as unconditional):

| Line | Rule |
|---|---|
| 137 | "Do not use the old Platform.cheats/menu-enable paste." |
| 240-245 | ⛔ Read the LOG FILE, never the screen; wrap uncertain reads in `print_format` |
| 246-252 | ⛔ An OS-side measurement from a non-DPI-aware process is not a measurement |
| 253-259 | ONE command per line; never a trailing `--` comment in a console snippet |
| 260-261 | `ModLog(...)` is the ONLY path proven to reach the log file |
| 262-263 | Runtime console wrappers must target the LEAF class |
| 264-269 | Blacklisted names read back as `nil` with no error — list given; do not use in snippets |
| 312-318 | ⚠️ NEVER put a `--` comment in a `*r`/`*g` snippet |
| 319-322 | The console input is ONE LINE — paste one command at a time |
| 323-333 | ⛔ `ConsolePrint` takes exactly ONE string argument |
| 339-340 | `g_Consts` does not exist at the main menu — run from inside a loaded colony |
| 403-408 | "No cheat exists... do not look again" for five named actions |
| 410-415 | ⚠️ Cheat keyboard shortcuts do NOT exist on retail — always type the function call |
| 477 | Turn loggers off when a test is done |
| 483-485 | Baseline restore from a saved copy, NOT `git checkout`; never `git commit -a` with that edit in the tree |
| 501-504 | The enable-path leg needs one human click; cannot be scripted (blacklist reasons given) |
| 509-514 | ⚠️ EVERY run needs the disable step, including back-to-back runs; disable + fully quit, never untick/retick in one process |
| 540-542 | A toggles-OFF run leaves opt-in probes uncovered — do NOT ask the owner to flip toggles for this; use the temp file instead |
| 548-549 | ⚠️ The pre-load lever cannot be set from a companion mod |
| 649 | The probe-arming edit must be a script FILE, never an inline PowerShell one-liner |
| 657-658 | The loaded save arrives PAUSED — set a speed before any game-time work |
| 663-664 | ⛔ Never print or trust `RealTime()` deltas across a loading screen |
| 690-691 | Save fixtures: keep a pristine `-base` copy before a destructive test |

---

## 7. Findability

**No table of contents.** The doc opens straight into "## Ground rules" at line 12; there is no anchor list, no "jump to command table" pointer anywhere in the first section.

**Can the owner find the command table in under 10 seconds mid-playtest?** Only via full-text search (Ctrl-F for "Verified command reference" or a remembered command name) or by scrolling ~50% into a 721-line file — the table starts at line 353 of 721, i.e. just past the halfway point, and is preceded by 350 lines of ground rules / external-validity / cheating-instructions / g_Consts-trap / salvage-mode / console-mechanics material the owner has to scroll past (or know to skip) every time.

**Concrete fix suggestions** (not implemented — read-only job):
- A 5-10 line TOC immediately under the intro (line 10), one entry per `##`/`###` heading, would make every section reachable in one Ctrl-F for the section name instead of a scroll.
- The two heaviest-traffic sections for a mid-session lookup — "Verified command reference" (15,955 B) and "Test Kit helpers" (6,136 B) — are also the two most likely to be searched for by content (a specific command name) rather than by heading, so a TOC helps the "what sections exist" case but an owner who already knows the command name is probably fine with Ctrl-F today. The TOC mainly helps the *first-time-this-session* orientation, not the repeat lookup.

---

## 8. Honest verdict

**Actively WRONG / would cost the owner a sitting (highest priority):**
1. **`Fix_MeteorStormWedge` heal claim (line 369).** Confirmed removed from the pack 2026-09-08. Following this row's advice to trigger a `"storm"` meteor cheat, on the stated expectation that the pack auto-heals the wedge, will leave the owner with a wedged storm and no automatic recovery.
2. **`SMRFixPack.ListFixes` → "`74/74` in every configuration" (line 431).** Confirmed current truth is `46/46`. An owner seeing `46/46` mid-playtest has nothing in this doc telling them that's expected.
3. **A cluster of console commands the table tells the owner to type no longer exist as callables**: `CheatFillAllStorages`, `CheatResearchAll`, `CheatToggleAllShifts`, `CheatUnlockAllTech`, `CheatUnlockAllBreakthroughs`, `CheatUnlockBreakthroughs`, `CheatClearForcedWorkplaces`, `CheatSpawnPlanetaryAnomalies`, `CheatBatchSpawnPlanetaryAnomalies`, `CheatOpenAllDomes`, `CheatCloseAllDomes`, `SetGameSpeedState`. All confirmed by tree-wide grep against the current 1.1.0.403908 source. Typing any of these in console should raise `attempt to call a nil value`.

**Merely stale (still work, or work differently, but won't surprise the owner with a hard failure):**
- Every surviving `Cheats.lua` function's cited `file:line` has drifted (sampled a dozen, all moved); the underlying calls still work when typed by name.
- `CheatDustDevil` gained a third parameter (`pos`) — behaviour of the doc's giant recipe block unverified against the new signature.
- The `78 PASS / 16 SKIP` probe tally (line 619-624) is stale, and per STATE.md the *true current* tally is not yet measured (OWED since 09-09) — so the doc is not just out of date, it's citing a number the project itself no longer trusts.
- `TestKit\Code\00_TestCore.lua` line citations for the "fix pack present" log line (`:351`) has drifted again to `:459` — this is the SECOND time this exact citation has gone stale (the doc already documents correcting it once, from `:286`).
- Save fixtures SAVE-A/D/E/F/Mirror-Sphere: cannot confirm they currently exist under those names anywhere I could check; if built pre-09-08 they are branch-locked per EF-079 regardless.

**Fine / holds up:**
- File and folder paths: every path and log file I checked (TestKit repo + files, opt-in pack repo, `ModTools\Src`, all cited `docs/archive/*` logs, the cited git object `93088ba`) resolved.
- TestKit helper API surface: essentially all named `SMRTest.*`/`SMRFixPack.*`/`SMROptInPack.*` calls exist as documented.
- `SMROptInPack.ListFixes` → "`1/8`" is still accurate.
- Ground rules, external-validity framing, console sandbox mechanics (blacklist, ONE-LINE rule, `ConsolePrint` single-arg rule) — nothing here is game-version-dependent; these are Test-Kit/console-engine facts, not gameplay-cheat facts, and I found no evidence any of them broke.

**What I'm unsure about (explicitly, not resolved):**
- Whether SAVE-A/D/E/F/Mirror-Sphere fixtures exist at all, under any name — inconclusive from available evidence (§2F).
- Whether `CheatDustDevil`'s new third parameter changes the doc's giant recipe's correctness — not re-verified.
- Whether any *other* rows in the 15,955 B command table besides the ones I checked are also gone — I checked roughly 30 of the ~40 rows; I did not verify `CheatToggleInfopanelCheats` (doc already marks it "retired for toolkit playtesting"), `dbg_ToggleRocketInstantTravel`'s two side-effect mechanisms, or the DevMenu "Max All Stats" manual-recipe row against the newly-discovered `CheatMaxColonistStats` (flagged in §2A as a likely-better replacement, not confirmed the doc's manual version is broken).
- Whether a stricter git-history diff would surface a genuine "superseded-in-place, original duplicated" case that my single read-through didn't catch (§5).
