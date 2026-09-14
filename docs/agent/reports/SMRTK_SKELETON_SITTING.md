# SMRTK 02 — the skeleton sitting (attended kill gate)

⛔ **NO GAME LEG HAS RUN.** This file currently holds the **pre-flight only**.
P1–P4 are unread and the verdict line is empty until the owner sits. Nothing
below moves a status (rule 17); every claim here is source- or command-derived
and says which.

Attending session: Claude (Opus 5), 2026-09-13. Builder was Codex (01,
`reports/SMRTK_SKELETON_PREDICTIONS.md`) — rule 22 holds, the non-building
vendor scores the predictions. Pack HEAD `320d359`; TestKit HEAD `5d8d3b3`.

## Live todo

- [x] Pre-flight gates (staleness, fingerprint, parse, stale probe, rules 6/7).
- [x] Script pre-flight: every symbol and every game route the paste script uses,
      checked against the built code and against `ModTools\Src`.
- [x] Fixture survey (corrected after the owner named the real saves) + backup of both.
- [x] Decoded both fixtures' savegame bodies; `CheatsUsed` read false against a positive control.
- [x] Step 0 COMPLETE: clean read scored, baseline saved and verified on disk, vanilla control fired RED (`entries=1`).
- [x] Step 1 COMPLETE: fresh clean boot, PreLoadGame arm, hotkey both ways, `used=false`, scratch discarded.
- [x] Step 2 COMPLETE: ⭐ **P2 PROVEN** — `discriminates=true negative=false positive=true`.
- [x] Step 3 COMPLETE: ⭐⭐ **P1 PASSES** — leaf filled the depot, `used=false`, zero `ObjCheat` all boot.
- [x] Step 4 COMPLETE: ⭐ **P3 PASSES** on the native path; clipboard verified from Windows itself.
- [x] Step 5 COMPLETE: tee arm/fire/disarm clean, `same=true`, ⭐ P3 confirmed on both routes.
- [x] Steps 6-7 COMPLETE: NOT_BUILT stubs exact, error witness exact.
- [x] Step 8 COMPLETE: ⭐ **P4 PASSES** — auto-disarm on save, state round-trips both directions.
- [ ] Verdict, archived log path, outbox to 03A/99, ck175 append.
- [ ] Prediction-by-prediction scoring; verdict; archived log path.
- [ ] Outbox to 03A and 99; ck175 in plain language; strike the row; `git rm` 02.

## Pre-flight — gates, all emitted

| gate | command | result |
|---|---|---|
| staleness, both trees | `git log --oneline -5`, `git status --short` | pack `320d359` clean; TestKit `5d8d3b3` clean; 01's three commits present (`774b55a`, `b400683`, `5d8d3b3`) |
| fingerprint | `python tools/doccheck.py --emit-fingerprint` | installed game build **24995074** — identical to 01's; `doccheck: GREEN`, `TESTKIT TREE: clean` |
| parse | `python tools/parsecheck.py --dir C:/Dev/SMR-BugFixPack-TestKit/Code --quiet` | `PARSE: 27 file(s) ... 0 error(s) [Lua 5.5]` |
| stale probe | `grep -rln "TEMPORARY" Code/ ../SMR-BugFixPack-TestKit/Code/` | zero matches (exit 1) — the expected result, not a missing path |
| rule 6 | `grep -n 'NetSyncEvent\|LogCheatUsed'` on both SMRTK files | 0 |
| rule 7 | `grep -nE '^\s*print\('` on both SMRTK files | 0 |
| H-10 | `metadata.lua` `code` list | `Code/70_SMRTK_Core.lua`, `Code/71_SMRTK_Panel.lua` both listed, core before panel |
| junction | `%APPDATA%\Surviving Mars Relaunched\Mods\` | `SMR-BugFixPack-TestKit -> C:\Dev\SMR-BugFixPack-TestKit` live |
| game closed | `tasklist /FI "IMAGENAME eq Mars.exe"` | not running |

## Pre-flight — the script itself

Every `SMRTK.*` symbol the paste script uses exists in the built code
(`TaintRead ConsoleControl Mark CopySince PrintTee ArmedCount OnLuaError
PanelState Action Run Log ring mark_index error_count mark_errors`), and the
action ids it dispatches are registered (`taint_read`, `eligibility`, `flush`,
`clear`, `print_tee`, `console_control`, `mark`, `copy`). `SMRTK` is a real
global (`70_SMRTK_Core.lua:4`). `pause` and `stop_disaster` are panel buttons
with **no** registered action — `dispatch` returns `NOT_BUILT`
(`70_SMRTK_Core.lua:164`), which is what step 6 predicts.

**The console route is reachable.** `ConsoleRules` (`uiConsole.lua:355-365`)
carries `{ "^*r%s*(.*)", "CreateRealTimeThread(function() %s end) return" }`, so
the `*r` prefix in steps 3/4/5 is real and runs the body in a real-time thread.
Console input is evaluated in `g_ConsoleFENV`, a `LuaModEnv` behind
`ModEnvBlacklist` (`console.lua:27-56`). Enumerated that blacklist (149 entries,
`Mod.lua`): `print`, `ConsolePrint`, `CreateRealTimeThread`, `IsKindOf`,
`XShortcutsTarget`, `ReloadShortcutsImmediate`, `ConsoleEnabled`, `CheatsUsed`,
`AreCheatsUsed`, `cls`, `FlushLogFile`, `LocalStorage`, `GameTime`, `Platform`,
`AreModdingToolsActive`, `SMRTK` — **none blacklisted**. `CanUnlockAchievement`
**is** blacklisted, so step 0's `type(CanUnlockAchievement)` reads `nil` from the
console for the blacklist reason, independently confirming `EF-096` and 01's
disagreement 1.

**Echo-proofing holds.** `Console:Exec` writes `AddConsoleLog("> " .. text)`
(`uiConsole.lua:369-374`), so each pasted line also produces an echo. Step 4's
`tap_read` compares `r.text` for **exact** equality with the witness strings, so
an echo (`> print("SMRTK_NATIVE_PRINT_100%")`) cannot satisfy it. The `%` in the
witnesses is safe: the user text is a `string.format` **argument**, never the
format string (`console.lua:14-24`).

**Step 3's leaf is the real leaf.** `StorageDepot:CheatFill()`
(`Lua/Buildings/StorageDepot.lua:196-209`) is the body the script calls, and
`max_amount_<resource>` is the real field (`:65`, `:199`). The guard chain
(`IsKindOf` StorageDepot, string `resource`, `supply[resource]`) correctly
excludes `MultiResourceDepotBase`, which has its own `CheatFill` (`:486`).
`needs="selected"` reads `rawget(_G, "SelectedObj")` (`70_SMRTK_Core.lua:161`).

## ⭐ The control is NOT vacuous — the vanilla taint route, read end to end

The pre-declared RED was traced at source before the owner presses anything, so
a GREEN in step 3 is a real contrast and not an artefact:

1. `Infopanel.lua:41-51` builds one `XAction` per `Cheat*` method on the object,
   stripping the prefix — the depot's button is labelled **Fill** — and its
   `OnAction` fires `NetSyncEvent("ObjCheat", self, "CheatFill")`.
2. `NetSyncEvents.ObjCheat` (`Network.lua:214-226`) gates on `AreCheatsEnabled()`
   — hence the Mod Manager toggle in step 0b — then calls `InvokeObjCheat`.
3. `InvokeObjCheat` (`Network.lua:208-215`) calls **`LogCheatUsed(method, obj)`
   and only then `obj[method](obj)`**.
4. `LogCheatUsed` (`Network.lua:242-245`) appends one row to the `CheatsUsed`
   GameVar; `AreCheatsUsed()` is `#CheatsUsed > 0` (`:247-249`).

So vanilla Fill ⇒ **exactly one** entry, and the toolkit's direct `o:CheatFill()`
passes none of those four sites. `LogCheatUsed` has exactly four call sites in
the whole tree (`ClassDef-PresetDefs.generated.lua:947`, `Network.lua:212`,
`:234`, plus its own definition) — none reachable from a direct leaf call.

⚠️ **Finding for 03A/P2, filed not acted on:** the same builder treats
`AsyncCheat*` methods differently — `Infopanel.lua:45-47` calls
`self["AsyncCheat"..name](self)` **directly, bypassing `ObjCheat` entirely**, so
those vanilla buttons never taint either. P2 should know which of its per-object
actions are already taint-free in vanilla before it re-implements them.

## ⭐ Why the console keeps switching itself off — and why step 2 should discriminate

The gate that creates the console shortcut is one line
(`CommonShortcuts.generated.lua:176`):

```lua
local cond = AreCheatsEnabled() or ConsoleEnabled or Libs.DevToolsPublic
```

and `AreCheatsEnabled()` is `Platform.cheats or AreModdingToolsActive()`
(`gamelib.lua:1014-1016`), where `AreModdingToolsActive()` is
`IsModEditorOpened() or IsModManagerOpened() or IsModEditorMap() or
Game.testModGame` (`Mod.lua:146-148`).

⚖️ **That is the mechanism behind the owner's complaint** — *"I have to
re-activate it every time I load"*. `IsModManagerOpened()` is **live, not
sticky**: the vanilla cheat surface exists only while the Mod Manager is
actually open, and closing it takes the console with it unless something else
holds `cond` true. The toolkit's `ConsoleEnabled` arm is the second disjunct,
which is exactly the right place to intervene.

**Two consequences for the sitting, both good:**

- **Step 0b does not poison step 2.** Opening the Mod Manager for the control
  flips `AreCheatsEnabled()` true only *while it is open*; nothing persists.
  The existing order (control → quit → fresh load with the Mod Manager never
  opened) is already safe. It does mean the "Mod Manager CLOSED throughout"
  clause in P1 and P2 is load-bearing in a stronger sense than it reads: it is
  not hygiene, it is the variable under test.
- **Step 2 should discriminate.** `Libs.DevToolsPublic` is set only under
  `Platform.developer`, or under `Platform.asserts` with the lib folder present
  (`autorun.lua:249-256`). A savegame header serialises the whole `Platform`
  table (`Savegame.lua:779`), and **both fixtures** (`My game`, `Mygame2`) list
  exactly `desktop, editor, goldmaster, paradox, pc, steam` — **no `cheats`, no
  `developer`, no `asserts`**. So on this build, with the Mod Manager closed,
  `cond` reduces to `ConsoleEnabled` alone and 01's
  `discriminates=true negative=false positive=true` is well-founded rather than
  hopeful. ⚠️ This is derived from a save header, not from the console. Step 0's
  `PLATFORM_READ` is still the authoritative read, and it answers 01's open
  question ("record the actual `cheats` value; it was unverified at authoring")
  — expect `cheats=false`, and treat anything else as the surprise it would be.

## Fixture — ⚠️ my first survey was wrong three ways; corrected

**The correction, because the first version of this section is in git history.**
I reported "exactly one 1.1.0 save on the rig, `Autosave Sol 490`, and it is the
owner's colony". All three parts were wrong:

1. **Wrong folder.** Relaunched writes to
   `C:\Users\stkot\Saved Games\Surviving Mars Relaunched\76561198020568696\`
   (**126 saves**), not `%APPDATA%\Surviving Mars\`, which belongs to the
   *original* Surviving Mars and holds 2024-era saves. A `find` under the user
   tree exited 2 on `Saved Games` and I read the truncated result as a complete
   one.
2. **Instrument defect in my header scanner.** `active_mods` sorts before
   `lua_revision` in the metadata table, and each mod entry carries its **own**
   `lua_revision`. A first-match regex therefore reported our mods' declared
   `350453` as the savegame's build. Re-parsed with a brace-depth walk that
   takes depth-1 keys only. (`EF-051`-adjacent lesson, and the house rule:
   suspect the instrument first.)
3. **Wrong provenance.** `Autosave Sol 490` is the **C92 reporter's** save, not
   the owner's colony — `reports/C92_INVESTIGATION.md:20-26` records the owner
   loading it from `Downloads`, and byte copies sit in
   `C:\Dev\SMR-C92-Evidence-20260913\`. It is evidence, not a fixture, and the
   sitting must not touch it.

**⚖️ Owner authority, 2026-09-13:** *"Mygame and mygame 2 should both be cheat
free. I have never used cheats on them."* That settles cleanliness; step 0's
`TaintRead` records the value because the report needs the measured line, not
because the statement needs checking.

### The real candidates

| save | `lua_revision` / `orig` | sols | sponsor | map | `active_mods` |
|---|---|---|---|---|---|
| `My game` | 403908 / **403908** | 9 | BlueSun | `BlankBig_01` | TestKit, Fix Pack, `3787202810`, OptInPack |
| `Mygame2` | 403908 / **403908** | 9 | BlueSun | `BlankBig_01` | same four |

`orig_lua_revision` equal to `lua_revision` means both were created natively on
1.1.0, not migrated (`EF-079` does not bite). Both already carry the TestKit in
`active_mods`, which is what the sitting needs loaded. `Mygame2` is the newer of
the two (2026-09-13 19:50 local). `required_lua_revision` is 402200 on both.

**Backed both up** before anything touches them, verified byte-identical by md5:
`My game.savegame.sav` 28,986,325 B `134addfd9d3d93662b8ce5b0001f3814`;
`Mygame2.savegame.sav` 28,951,471 B `d43979e921b2112f32d8fe4fd34ed8e6`.

### ⭐ Nothing in our own tooling could have tainted them

Worth stating because `CheatsUsed` catches more than a player calling it
cheating: **any** `Cheat*` method routed through `ObjCheat` appends a row,
including probe code. The TestKit is clean by construction — `NetSyncEvent`,
`ObjCheat` and `LogCheatUsed` appear **zero** times across its 27 files, and its
single `Cheat*` call site (`91_Stress.lua:815`, `:CheatCleanAndFix(`) is a
**direct leaf call**, which by the route traced above logs nothing. So the
TestKit was already taint-free by the same discipline SMRTK is being built on —
a useful precedent, and corroboration rather than a check on the owner's word.


## ⭐ The fixtures' cheat flag IS readable from disk — measured, both sides

The earlier claim in this file — "`AreCheatsUsed()` is not readable from disk" —
was **too weak**. `CheatsUsed` lives in the compressed body, but the body
decodes, so the flag is readable without launching the game.

**Route.** A `.savegame.sav` is a `BPUL` container: a 92-byte header, the
plain-text `savegame_metadata` table, then records. Each compressed record is
`ZSTD` + a 4-byte uncompressed size + 4 bytes + a raw zstd frame. Two gotchas
cost a retry each and are worth recording: the decompressor needs
`max_window_size=2**31`, and a record must be read to **exactly** its declared
size — reading to the end of the slice runs into the next record's container
header and throws `Unknown frame descriptor` mid-stream, which reads like a
corrupt frame and is not one. Both fixtures decode fully, 226,788,852 +
~13.9 M bytes each, in well under a second.

**The reading, with its presence side.** In the persisted stream the GameVar
key is length-prefixed (`\n` = 10 = `len("CheatsUsed")`) and the value follows:

| save | bytes at the `CheatsUsed` key | reads as |
|---|---|---|
| `Mygame2` | `(\nCheatsUsed\x03:NG\x03(\x0bPlanetScene` | scalar, next key follows |
| `My game` | `(\nCheatsUsed\x03(\x0fg_LastBuildItem` | scalar, next key follows |
| `TEST 2I` | `(\nCheatsUsedZA\x01\x01V\x01…(\x10CheatMalfunction` | **table**, holding cheat method names |
| `CORUN1` | `(\nCheatsUsedZ\xa8\x01\x01V\x01…(\x10CheatMalfunction` | **table**, holding cheat method names |

A token sweep for `Cheat[A-Za-z]+` across every decoded byte says the same thing
at a second angle. `Mygame2` and `My game` carry exactly three such tokens —
`CheatsUsed`, `CheatsVegGrowthModifier`, `CheatUnlockAllSponsorBuilding`, the
latter two being unrelated persisted global names that merely start with those
letters — and **no cheat method name at all**. The project's own playtest saves
(`TEST 2I`, `CORUN1`, `saint test`) carry the full roster: `CheatFill`,
`CheatEmpty`, `CheatCleanAndFix`, `CheatDestroy`, `CheatMalfunction`,
`CheatRepair`, `CheatStarve` and a dozen more — exactly the `method` strings
`LogCheatUsed` stores (`Network.lua:242-245`). That is the presence side, so the
absence in the fixtures is a sample, not a silence.

⇒ **`Mygame2` and `My game` are cheat-free, measured independently of the
owner's word and agreeing with it.** Step 0's `TaintRead` is now a confirmation
of a known value rather than a gate on an unknown one. (`POST 105-DIRTY` scans
clean by the same measure too — its name refers to the F105 leg, not to cheats.)

⚠️ **What this does NOT settle: the depot.** Every one of the eleven
single-resource depot classes (`StorageMetals` … `StorageSeeds`) plus
`UniversalStorageDepot` and `MechanizedDepot` appears in **both** fixtures — and
a Sol 9 colony has not built all eleven. Those hits are the template/class name
table, not instance evidence, so this instrument cannot say whether the colony
holds a **partly empty single-resource depot** for step 3. That stays an
on-screen check for the owner, and it is the one remaining fitness question for
these two saves as step-3 targets.


## Boot evidence already on disk (main menu only, no save loaded)

`Mars.exe-20260913-19.35.49-6a91a190.log`, a boot **after** 01's commits
(19:15 local), carries the skeleton loading in the real game:

```text
[SMRTK] SMRTK_CORE loaded=true tee=false t=1224 id=1
[SMRTK] SMRTK_CONSOLE_ARM enabled=true hook=DataLoading t=1224 id=2
[SMRTK] SMRTK_SHORTCUT console=true key=Ctrl-Shift-F11 t=1224 id=3
[SMRTK] SMRTK_SHORTCUT console=true key=Ctrl-Shift-F11 t=1224 id=4
```

This is **not** a P1–P4 reading: that boot quit from the main menu at 1:36
without loading a game. Three things it does establish, and two it does not:

- The tag and the one-logger shape (requirement B) survive the real mod loader.
- `hook=DataLoading` is **not** a miss against step 1's `hook=PreLoadGame`
  prediction. There are three arm sites — `DataLoading`, `PreNewMap`,
  `PreLoadGame` (`70_SMRTK_Core.lua:338-343`). A boot that loads no save reaches
  only the first. Step 1 loads a save and should therefore add a
  `hook=PreLoadGame` line.
- ⚠️ **The doubled `SMRTK_SHORTCUT` line is a rebuild, not a double
  registration** — I suspected a double-toggling hotkey and it is not one.
  `ReloadShortcutsImmediate` does `table.clear(XShortcutsTarget.actions)` before
  respawning (`XShortcuts.lua:67-72`), and `Msg("Shortcuts", XShortcutsTarget)`
  is emitted once per rebuild (`:63`) against the one singleton host. Two
  rebuilds at boot (the second from `OnMsg.DataChanged`, `:27-31`) ⇒ two log
  lines, one live action. Expect 1–2 of these lines and score neither as a
  defect.
- `console=true` in those lines is the **old TestKit's** console bootstrap
  (01's disagreement 2) already having created `DE_Console`. It is exactly the
  confounder step 2 exists to isolate; it is not evidence for P2.
- Nothing here reads taint, the tap, the clipboard, or persistence.

## Step 0 — RESULT: the control is established, both sides measured

⭐ **This is the precondition for the whole kill gate.** P1 asks whether a leaf
action leaves `CheatsUsed` empty; that question is only meaningful if the vanilla
route demonstrably fills it on this exact fixture. It does.

| leg | line in the archived log | predicted (01) | |
|---|---|---|---|
| 0a clean | `SMRTK_TAINT_READ action=taint_read status=OK used=false` (id=15) | same | ✅ exact |
| 0a clean | `SMRTK_ELIGIBILITY action=eligibility reason=UNAVAILABLE:sandbox status=OK` (id=16) | same | ✅ exact |
| 0a clean | `SMRTK_PLATFORM_READ cheats=nil eligibility_api=nil mod_tools=false` (id=17) | `cheats` unverified; api nil | ✅ api/mod_tools exact; `cheats` answered |
| 0a clean | `SMRTK_SCRATCH_READ entries=0` (id=24) | — | baseline count, taken before the control |
| 0b RED | `ObjCheat CheatFill` (vanilla's own print, `Network.lua:216`) | — | ✅ the vanilla route provably dispatched |
| 0b RED | `SMRTK_TAINT_READ action=taint_read status=OK used=true` (id=26) | same | ✅ exact |
| 0b RED | `SMRTK_TAINT action=taint_read before=true used=true` (id=27) | same | ✅ exact |
| 0b RED | `SMRTK_SCRATCH_READ entries=1` (id=28) | `entries=1` | ✅ exact |
| 0b RED | `SMRTK_TAINT action=flush before=true used=true` (id=30) | — | taint is sticky; the assert fires on every later action, as designed |

**The four-step source trace is confirmed end to end in play.** `ObjCheat
CheatFill` is printed by `NetSyncEvents.ObjCheat` only *after* its
`AreCheatsEnabled()` gate (`Network.lua:215-216`), so its presence proves the
gate passed and `InvokeObjCheat` ran `LogCheatUsed` before the leaf. One button
press produced **exactly one** row — the arithmetic the trace predicted, not one
per drone, per resource unit, or per interrupted request.

⇒ **RED = `used=true`, `entries=1`. GREEN (step 3) must be `used=false` with the
strip CLEAN after a leaf `CheatFill` through `SMRTK.Run`.** The contrast is now
anchored on the same fixture, the same depot and the same method.

### ⭐ Same-colony positive control for the disk reader

The scratch save turned the earlier byte-level method from "validated against
borrowed playtest saves" into "validated on this fixture, both sides". The two
saves are the same colony minutes apart, and the `CheatsUsed` key is followed by
the **same next key** in both, so this is the same location differing only in its
value:

```text
SMRTK_BASELINE_CLEAN    (
CheatsUsed(RainsDisasterThreads…
SMRTK_SCRATCH_TAINTED   (
CheatsUsedRVýúx (	CheatFill8…(RainsDisasterThreads…
```

Clean carries the scalar ``; tainted carries a table (`R`, then `` =
one entry) whose row holds the game time and the length-prefixed method name
`	CheatFill` — exactly the `{ GameTime(), method, class, handle }` shape
`LogCheatUsed` writes (`Network.lua:242-245`). The `Cheat*` token sweep agrees:
`CheatFill` appears in the tainted save and in neither clean one.

⇒ The reading that cleared `Mygame2` and `My game` is now anchored on a positive
control from the owner's **own** colony, not only on `TEST 2I`/`CORUN1`. It also
explains the scanner's odd `CheatsUsedR` / `CheatsUsedZ` tokens: the letter after
the key is the serialiser's table opcode, and a clean save has no such letter.

### Two corrections this leg produced

1. **`Platform.cheats` reads `nil`, not `false`.** This session predicted
   `false`. Falsy either way and the gate arithmetic is unchanged, but the
   literal is `nil` — the key is absent from the `Platform` table, matching both
   fixtures' saved `platform` tables. 01's "unverified at authoring" is now read.
2. **The first control attempt was unrun, not failed, and the log said so
   before the owner did.** `SMRTK_TAINT_READ used=false` / `entries=0` with **no
   `ObjCheat` line anywhere** distinguishes "the vanilla path never dispatched"
   from "it dispatched and did not taint" — a distinction worth having, because
   only the second would have been a finding. Cause: a **dome** was selected, and
   `Infopanel.lua:26-38` builds the Cheats list from the selected object's own
   `Cheat*` methods, so a dome has no `Fill`. Not a defect in anything.

### ⭐ Measured for 03A/P2: which infopanel cheats already avoid taint in vanilla

From the dome's live Cheats section, classified at source. `AsyncCheat*` entries
are dispatched by `self[…](self)` directly (`Infopanel.lua:45-47`), bypassing
`ObjCheat`, so they never reach `LogCheatUsed`:

- **Never taint (6, all inspection-only):** `ClassHierarchy`, `ClipPlane`,
  `Gizmo`, `Inspect`, `Properties`, `Screenshot`.
- **Taint (16, all state-mutating):** `AddDust`, `AddMaintenancePnts`,
  `AddPrefab`, `CleanAndFix`, `Delete`, `Destroy`, `FillConsumptionRes`,
  `LightningStrike`, `Malfunction`, `MeteorHit`, `NoConsumption`, `QuickRefab`,
  `SpawnChild`, `SpawnColonist`, `SpawnVisitor`, `SpawnWorker`, `Unfreeze`.

P2 re-implements the second group through leaf calls; the first group it can
route to the vanilla method unchanged, because there is no taint to avoid.


## Step 1 — RESULT: fresh boot, no hand-enabled cheats, panel and taint correct

Boot `Mars.exe-20260913-20.40.33`. `Platform.cheats` never set, Mod Editor never
opened, no vanilla cheat button touched.

| line | predicted (01) | |
|---|---|---|
| `SMRTK_CONSOLE_ARM enabled=true hook=PreLoadGame` (id=6) | same, before load completion | ✅ exact |
| `SMRTK_SHORTCUT console=true key=Ctrl-Shift-F11` ×6 | a registration | ✅ present (see below) |
| `SMRTK_PANEL_RESTORE open=true tab=Sitting` | panel returns | ✅ restored unprompted after the load |
| `SMRTK_PANEL action=panel_toggle open=false status=OK tab=Sitting` (id=12) | hotkey hides it | ✅ |
| `SMRTK_PANEL action=panel_toggle open=true status=OK tab=Sitting` (id=13, +869 ms) | hotkey returns it | ✅ |
| `SMRTK_TAINT_READ action=taint_read status=OK used=false` (id=14) | `used=false` | ✅ exact — the taint died with the discarded branch |
| `SMRTK_SCRATCH_DISCARDED name=SMRTK_SCRATCH_TAINTED` (id=15) | records the owner's act | ✅ posted only after deletion was verified on disk |

⭐ **The duplicated-`SHORTCUT` suspicion is now falsified in play, not just at
source.** The pre-flight flagged that repeated `SMRTK_SHORTCUT` lines might mean
a doubly-registered hotkey that would toggle twice per press and appear dead.
This boot logged **six** such lines, and one keypress produced **exactly one**
`panel_toggle`, the next keypress exactly one more. Six rebuilds against one
singleton host, one live action — as `XShortcuts.lua:67-72`'s
`table.clear(XShortcutsTarget.actions)` predicted.

⛔ **What step 1 does NOT establish.** `console=true` appears on the shortcut
line from the **first** boot registration onward, because the old TestKit's
bootstrap already created `DE_Console` (01's disagreement 2). Enter working here
shows the console is reachable; it does not attribute that to our arm. P2 is
undecided until step 2.

⚠️ `SMRTK_SCRATCH_TAINTED` confirmed absent from the saves folder before the
discard line was posted. `EF-051` note: Steam Cloud has restored deleted saves
before, so absence now is not a permanent guarantee — if it reappears it must be
deleted again and never loaded.

## Step 2 — RESULT: ⭐ P2 PROVEN. The console gate is ours, confounder eliminated

```text
SMRTK_SHORTCUT console=false key=Ctrl-Shift-F11 t=7369525 id=25
SMRTK_SHORTCUT console=true  key=Ctrl-Shift-F11 t=7369525 id=27
SMRTK_CONSOLE_CONTROL action=console_control discriminates=true negative=false positive=true status=OK id=28
```

01 predicted `discriminates=true negative=false positive=true status=OK`.
**Measured identically.** This is the leg the whole `ConsoleEnabled` claim rested
on, and it is the one leg the old TestKit's bootstrap could have faked.

⭐ **The discrimination is independently witnessed, not merely summarised.** The
diagnostic drives two shortcut rebuilds, and our own `OnMsg.Shortcuts` handler
logged the host's state at each: with `ConsoleEnabled = false` the rebuild
produced **`console=false`** — `DE_Console` genuinely absent — and after the
toolkit's arm the next rebuild produced **`console=true`**. Three lines from two
code paths agreeing beats one boolean.

⇒ On this build, with `Platform.cheats` unset and no GED tool open, the gate
`AreCheatsEnabled() or ConsoleEnabled or Libs.DevToolsPublic`
(`CommonShortcuts.generated.lua:176`) reduces to `ConsoleEnabled` **alone**, and
the toolkit's arm is what sets it. The old TestKit bootstrap is excluded as an
explanation because turning the flag off removed the console and our arm brought
it back inside the same synchronous call.

The pre-flight predicted this from the save headers' `Platform` tables (no
`cheats`, no `developer`, no `asserts`); the sitting confirms it from the game.

### Step 6 partially satisfied early

The owner exercised the tab bar while working: `SMRTK_TAB` for
`World`, `Agent`, `Sitting`, `World`, `Saves`, `Kit` (ids 17-22), all
`status=OK`, plus two `SMRTK_MOVE ... status=OK`. Every registered page
switches and the drag persists. No page content was expected or seen.

## Step 3 — ⛔ REFUSED by its own guard: 01's script targets a class no shipped depot uses

```text
SMRTK_ACTION action=skeleton_fill reason="select a single-resource depot" status=REFUSED id=32
SMRTK_TAINT_READ action=taint_read status=OK used=false id=33
SMRTK_ELIGIBILITY action=eligibility reason=UNAVAILABLE:sandbox status=OK id=34
```

**P1 is NOT decided and NOT failed — the leaf never ran.** No mutation occurred,
`used=false` held, and `ObjCheat` appears **zero** times in this boot, so nothing
touched the vanilla taint path either. The guard did exactly its job; what it
caught is that the guard's premise is wrong.

### The defect

01's step-3 body tests `IsKindOf(o,"StorageDepot")` and then
`type(o.resource)=="string"`, and calls `StorageDepot:CheatFill`
(`StorageDepot.lua:196`) with `o["max_amount_"..o.resource]`. That is the shape
of `StorageDepot`'s **single-resource** base body. **No shipped storage building
instantiates that shape.**

- Every storage template — `StorageMetals`, `StorageConcrete`, `StoragePolymers`,
  `StorageFood`, … and `UniversalStorageDepot` — declares
  `object_class = "UniversalStorageDepotBase"`.
- `UniversalStorageDepotBase.__parents = { "StorageDepot" }`
  (`StorageDepot.lua:329-330`), so the `IsKindOf` clause **passes**.
- But `UniversalStorageDepotBase:GameInit` ends with
  **`self.resource = self.storable_resources`** (`:444`) — a **table**, always.
  So `type(o.resource)=="string"` is false for every depot in the game, and the
  action can only ever refuse. ⇒ **01's step 3 could not have passed on any
  fixture.**
- The real leaf is **`UniversalStorageDepotBase:CheatFill` (`:710-730`)**, which
  overrides the base body and walks `storable_resources`, calling
  `AddResource` per resource. `UniversalStorageDepotBase.Fill` is aliased to it
  (`:733`).

⚠️ **Instrument defect on this session's side, stated plainly.** The pre-flight
reported "step 3's leaf is the real leaf" after confirming `StorageDepot:CheatFill`
and `max_amount_<resource>` exist. Both statements are true and both are
irrelevant: existence of a method is not evidence that any shipped object *is*
of that class. Worse, the sweep that should have found the override
(`grep -rn "CheatFill"`) was truncated with `head -15`, and `StorageDepot.lua:710`
sat past the cut — the tool hid the answer and the truncation was not treated as
a partial result. A total is not a set, and a `head` is a total.

### Requirement (A) is unaffected by the correction

`UniversalStorageDepotBase:CheatFill` contains **0** occurrences of
`LogCheatUsed` or `NetSyncEvent`, and the tree-wide count of `LogCheatUsed` call
sites remains four, none of them in `StorageDepot.lua`. So the corrected leaf is
taint-free by the same argument as the original, and P1's thesis is unchanged —
only the object model was wrong.

### ⭐ Consequence for 03A/P2 — larger than this sitting

P2 builds Fill / Empty / Delete / Destroy / CleanAndFix per object. It must
target **`UniversalStorageDepotBase`**, use `storable_resources`,
`GetStoredAmount(res)`, `GetMaxStorage(res)` and `max_storage_per_resource`, and
call the `:710` leaf. Anything written against `StorageDepot.resource` /
`max_amount_<resource>` will refuse on every depot in the game while looking
correct in review. The "single-resource vs Universal" distinction is **not** a
class distinction in this build — both are `UniversalStorageDepotBase`, and the
discriminator is `#storable_resources`.

### Corrected script used for the retry

```lua
IsKindOf(o,"UniversalStorageDepotBase")            -- passes for every depot
#o.storable_resources == 1                          -- single-resource vs Universal
before = o:GetStoredAmount(); cap = o:GetMaxStorage()
o:CheatFill()                                       -- the :710 leaf
```

Verified before use: `StorageMetals`/`Concrete`/`Polymers`/`Food` each declare
`storable_resources = {"<one>"}`; `UniversalStorageDepot` declares no override
and inherits the eight-resource default, so the `#==1` test genuinely separates
them.

## Step 3 retry — ⭐⭐ P1 PASSES. Requirement (A) holds in play

```text
SMRTK_ACTION action=skeleton_fill after=180000 before=13000 cap=180000              object=StorageMetals(1054) resource=Metals status=OK id=37
SMRTK_TAINT_READ action=taint_read status=OK used=false id=38
SMRTK_ELIGIBILITY action=eligibility reason=UNAVAILABLE:sandbox status=OK id=39
SMRTK_TAINT_READ action=taint_read status=OK used=false id=40   (later t=7550325)
```

01 predicted `SMRTK_ACTION action=skeleton_fill after=<amount> before=<amount>
object=<Class(handle)> status=OK`, `after > before`, then `used=false` and a
CLEAN strip. **Measured exactly**, including the `Class(handle)` rendering
(`StorageMetals(1054)`).

**The mutation was real, not a no-op:** `before=13000 → after=180000` against
`cap=180000`. A depot that did nothing would have refused on the `before>=cap`
guard or returned equal amounts. The toolkit filled the depot.

**And `CheatsUsed` stayed empty.** `ObjCheat` appears **zero** times across this
entire boot, so the vanilla taint route was never entered. The read was taken
twice, at two different game times (`t=7526350` and `t=7550325`), both
`used=false` — so this is not a sampling artefact of reading too early.

### ⭐ The contrast, on one fixture, one depot, one method

| | route | visible effect | `CheatsUsed` |
|---|---|---|---|
| step 0b | vanilla **Fill** button → `ObjCheat` → `LogCheatUsed` | depot fills | **1 row** |
| step 3 | `SMRTK.Run` → `UniversalStorageDepotBase:CheatFill` leaf | depot fills | **0 rows** |

Same colony, same `StorageMetals` depot class, same underlying leaf body. The
only difference is the dispatch path, and the taint tracks the dispatch path
exactly as the source trace said it would.

⇒ **Requirement (A) is satisfied at the source level. P1 PASSES.** The chain's
central premise — that every useful cheat action can be called through its leaf
body without registering as a cheat — is now a measured fact on this build,
not a design intention.

⚠️ **What this does not claim.** Achievement eligibility remains
`UNAVAILABLE:sandbox` and unread (`EF-096`); no-taint is necessary for
eligibility, not proven sufficient. This is one action on one class; P2 must
re-establish the same property per action as it builds them, and the step 3
defect above shows the object model is where that will go wrong.

## Step 4 — ⭐ P3 PASSES on the native path, with echo-rejection proven empirically

```text
SMRTK_MARK action=mark label=MARK   mark=69 status=OK id=43   (the button)
SMRTK_MARK action=mark label=native mark=71 status=OK id=44
SMRTK_TAP_READ action=tap_read native_console=1 native_print=1 status=OK id=45
SMRTK_COPY action=copy from=71 lines=9 status=OK truncated=false id=46
```

01 predicted `native_console=1 native_print=1`, clipboard carrying the output
witnesses as `source=console` and toolkit records as `source=toolkit`.
**Measured exactly.**

**The clipboard was read from the Windows clipboard by the attending session**
(`Get-Clipboard -Raw`, 1079 bytes, 9 lines — matching `lines=9`), not
transcribed by the owner. That is a stronger result than the brief asked for:
it proves the copy reached the real OS clipboard, not merely an internal buffer.

### ⭐ Echo rejection is now empirical, not just argued

The ring contains **both** the typed echo and the real output for each witness,
and the counter took only the output:

```text
[tap n=73 ... source=console] > print("SMRTK_NATIVE_PRINT_100%")      <- echo
[tap n=74 ... source=console] SMRTK_NATIVE_PRINT_100%                  <- output, counted
[tap n=75 ... source=console] > ConsolePrint("SMRTK_NATIVE_CONSOLE_100%")
[tap n=76 ... source=console] SMRTK_NATIVE_CONSOLE_100%                <- output, counted
```

`native_print=1` and `native_console=1`, not 2. The pre-flight predicted this
from `tap_read`'s exact-string comparison against `AddConsoleLog("> " .. text)`
(`uiConsole.lua:369`); the sitting confirms it with both rows visible in the same
capture. A tap that counted echoes would have read 2 and would have passed for
the wrong reason.

`source` metadata also discriminates as designed: `source=toolkit` on our own
`SMRTK_MARK`/`SMRTK_TAP_READ` records, `source=console` on native delivery. So
"a ring full of our own lines" is excluded as an explanation — 01's stated
falsifier for this leg.

⇒ **P3's requirement is met on the native route alone**: a real `print` output
reached the tap, and the clipboard pasted it. Step 5's tee is therefore a
*redundancy* check rather than P3's last chance, and is still worth running for
the ARM/FIRE/DISARM machinery that step 8 depends on.

## Step 5 — tee ARM/FIRE/DISARM clean; ⭐ P3 confirmed on the SECOND route too

```text
SMRTK_ARM     action=print_tee status=OK id=49
SMRTK_FIRE    action=print_tee status=OK text=SMRTK_TEE_WITNESS_100% id=50
SMRTK_DISARM  action=print_tee reason=manual status=OK id=54
SMRTK_TEE_RESTORE armed=0 same=true id=55
SMRTK_COPY action=copy from=84 lines=20 status=OK truncated=false id=56
```

01 predicted ARM, one FIRE carrying the witness text, DISARM, and a restore with
captured-function identity intact. **Measured exactly**, and the armed counter
moved `0 → 1 → 0` (`armed=1` at id=52 while still armed, `armed=0` at id=55).

**`same=true` is the load-bearing one.** It shows the tee put the *original*
`print` back rather than leaving a wrapper installed, which is the
**idle = zero patched vanilla functions** invariant. Between id=52 and id=55 the
invariant was genuinely violated (`same=false`, `armed=1`) and the teardown
restored it.

⭐ **The clipboard carries the witness on `source=print` AND `source=console`:**

```text
[tap n=89 ... source=print]   SMRTK_TEE_WITNESS_100%
[tap n=91 ... source=console] SMRTK_TEE_WITNESS_100%
```

So one real `print` was captured independently by the **tee** and by the
**native ConsoleLine tap**. P3 asked that at least one route carry actual print
output and that the clipboard paste it; both routes do. 01's fallback was never
needed as a fallback and is confirmed as redundancy.

### The skipped command diagnosed itself

Step 5's first pass logged no `SMRTK_DISARM` and ended `armed=1 same=false`.
Attributed at source: `T.PrintTee(false)` routes to `T.Disarm`, and `dispatch`
**always** calls `T.Log` before returning, so a silent disarm is impossible ⇒
the command had not run. The ring then **proved** it: the echo record jumps from
`> SMRTK.CopySince("tee")` (n=92) straight to
`> SMRTK.Log("TEE_RESTORE",...)` (n=95) with no `> SMRTK.PrintTee(false)`
between them, and that echo appears only later at n=98. The toolkit's own tap
reconstructed the operator's command history and settled the question — an
unplanned demonstration of what the tap is for.

### ⛔ Procedural finding: `CopySince` is destroyed by the operator's next copy

Step 5's first clipboard read returned 94 bytes containing the **text of the next
command**, not the copied range, even though `SMRTK_COPY ... lines=9 status=OK`
had succeeded. Cause: the attending agent hands over commands, the owner copies
each one to paste it, and **each copy overwrites the clipboard**. Step 4 survived
only because `CopySince` happened to be the last command in its block.

⇒ **`CopySince` must be the final command of any block**, and 08's script must
be written that way. ⭐ More usefully for 03A: the panel's **Copy since mark
button** is immune, because invoking it requires no copying. The console form of
this feature is fragile in exactly the agent-hands-over-commands workflow it
exists to serve — a concrete argument for button-first evidence capture in P4.

⭐ **Attending-session technique worth keeping:** the clipboard was read directly
with `Get-Clipboard -Raw` from the attending session rather than pasted into an
editor by the owner. It is faster, it removes a transcription step, and it is
stronger evidence — it proves the text reached the real OS clipboard.

## Step 8 — ⭐ P4 PASSES: auto-disarm on save, and state round-trips

```text
SMRTK_PANEL action=panel_toggle open=false status=OK tab=Kit id=73   (panel closed, see below)
SMRTK_MARK label=roundtrip mark=134 id=74
SMRTK_DISARM action=print_tee reason=SavegameSaved status=OK id=75   <- auto-disarm, BEFORE the load
SMRTK_CONSOLE_ARM enabled=true hook=ChangeMap id=76,77
SMRTK_CONSOLE_ARM enabled=true hook=PreLoadGame id=79
SMRTK_TAINT_READ action=taint_read status=OK used=false id=84
SMRTK_ROUNDTRIP_READ armed=0 collapsed=false open=false same_print=true tab=Kit x=1125 y=243 id=86
SMRTK_COPY action=copy from=134 lines=24 status=OK truncated=false id=87
```

⭐ **The load-bearing line is `SMRTK_DISARM ... reason=SavegameSaved`.** An armed
hook tore itself down *because the game saved*, before the load — so a patched
`print` cannot ride into a savegame. `armed=0` and `same_print=true` after the
round trip confirm the global was restored, i.e. the
**idle = zero patched vanilla functions** invariant survives a save/load.

`tab=Kit`, `x=1125`, `y=243`, `collapsed=false` all round-tripped exactly, and
`used=false` held.

### ⚠️ `open=false`, and why that is a PASS rather than a miss

01 predicted the panel "returns open". It returned `open=false` — because the
owner had closed it at **id=73**, moments before saving, to run a (flawed)
control for the flicker report below. `panel_toggle` persists
`SavePanelState { open = false }`, so the toolkit restored the state that was
actually in force. That is persistence working, not failing.

⭐ **And the untested half is already measured elsewhere in this same sitting.**
Step 1 saved/loaded with the panel **open** and produced
`SMRTK_PANEL_RESTORE open=true tab=Sitting` twice on the load. So across the
sitting the `open` field round-tripped in **both** directions:

| state at save | after load | evidence |
|---|---|---|
| open | restored open, right tab | step 1, `PANEL_RESTORE open=true tab=Sitting` |
| closed | restored closed, tab/x/y intact | step 8, `ROUNDTRIP_READ open=false tab=Kit x=1125 y=243` |

That is stronger than the single observation 01 asked for — a persistence route
that only ever restored "open" would pass the predicted test while being wrong.

⇒ **P4 PASSES.** Recorded as PASS WITH CORRECTION to the prediction's wording:
the predicted observation was displaced by an operator action, and the property
is established from two legs instead of one.

## ⚠️ Flicker/strobe report — REAL, MEASURED, CAUSE UNATTRIBUTED

Owner reported during the sitting: strobing when hovering menu buttons, with an
audio buzz; the same strobing on toolkit panel buttons with no audio; also on the
main HUD bar icons; **not** in the Save Game dialog, which behaves normally.

**Measured from a 12.9 s 4K/30 recording** (frames via ffmpeg, diffed in numpy):

| region | signature |
|---|---|
| `SAVE GAME` menu row | frame-to-frame diff bimodal ~0.03 ↔ ~1.2, irregular, up to 30 Hz |
| panel `Saves` tab button | bimodal ~0.02 ↔ ~0.48, 36 % of frames |
| changed bbox, menu | x 180-704, y 439-521 = the row's **highlight bar** |
| changed bbox, in-game | x 2906-3148, y 647-703 = the **tab button under the cursor** |
| audio | continuous low buzz rising during hover; **no discrete click transients** |

⇒ A **hover-highlight state oscillation** on whatever element is under the
cursor, retriggering the vanilla rollover sound fast enough to buzz. Toolkit
buttons strobe silently because they register no rollover FX.

Not a capture artifact: tearing does not produce a clean on/off of a single
highlight bar, and the owner hears the buzz live, which no video artifact can
explain.

### ⛔ The first control was VACUOUS — recorded because it was acted on

The attending session proposed "close the panel with Ctrl-Shift-F11 and re-test";
the strobe persisted, which looked like it exonerated the panel. **It does not.**
`panel_toggle` closes by `T.panel:SetVisible(false)` (`71_SMRTK_Panel.lua:166`)
and **neither deletes the panel nor stops its `SMRTKStatus` thread**, which loops
`T.RefreshPanel(); Sleep(250)` while `window_state ~= "destroying"` (`:156-157`).
So with the panel "closed" the object still exists and still repaints four times
a second. The control could not have cleared the panel and its negative result
carries no weight. (Whether a 4 Hz refresh could drive a ~30 Hz strobe is a
separate question — it is not obviously sufficient, but the control was not
clean, which is the point.)

⇒ **Valid controls, none yet run:** (1) hover at the **main menu**, where no
in-game interface and no panel can exist; (2) boot with TestKit + Fix Pack
**disabled** — the true vanilla control; (3) the house sound method, a log-only
`PlayFX` hook, to turn "a buzz" into a retrigger count (⛔ code change, needs
`Mars.exe` closed, rule 16).

⚠️ The discriminator the owner already supplied is the most interesting datum:
**the Save Game dialog does not strobe** while the game-options menu and the HUD
bar do. If (2) shows this is vanilla, it is a defect entry and the project's own
business, not an 03A item. Nothing here is attributed yet.

### Flicker — boot comparison, and the confound in the owner's own test

| boot log | `Loaded mod items for:` | strobe |
|---|---|---|
| `19.58.32` | TestKit, FixPack, OptInPack | not reported |
| `20.40.33` (the sitting) | same three, **then a second, EMPTY line** = the runtime disable | **yes; persisted across the disable** |
| `21.26.59` | *(line absent — no mod items loaded)* | none |

The empty `Loaded mod items for: ` line is the owner's mid-session mod disable,
and the strobe outliving it is consistent with already-executed mod Lua not
unloading. `SMR_FR1TempWorkaround`'s **def** loads in every boot because the
folder is present, but it appears in **no** boot's items list, so the Linux
workaround mod is enabled in none of them and is not a factor.

⚠️ **The owner's clearing test changed two variables at once** — mods off **and**
a process restart — so "the restart alone fixed it" is not excluded. Attribution
needs a boot with the mods ON.

⛔ **Hypotheses ruled out at source, recorded so they are not re-tried:**

- *The on-screen console log steals hover.* No: `ConsoleLog:MouseInWindow(pt)`
  returns **false** unconditionally (`uiConsoleLog.lua:63-65`).
- *We create the global mouse target.* No: `XShortcutsTarget` is a
  `DeveloperInterface` created by `ReloadShortcuts()` at file scope in **vanilla**
  (`XShortcuts.lua:7-25`), with `terminal.AddTarget(self)`,
  `terminal_target_priority = -100` and `ZOrder = 10000000`
  (`DeveloperInterface.lua:35-47`). It exists in every boot, mods or not — which
  also means a global hover fight is plausible *without* any mod.

**The one process-persistent thing unique to the strobing boot** is step 2's
`SMRTK.ConsoleControl()`, which calls `ReloadShortcutsImmediate()` **twice**
(clearing and respawning every shortcut action, then `UpdateToolbar()`). The
`19.58` boot carried the same three mods and ran no such rebuild. That is a
**hypothesis, not a finding** — it has not been tested.

⇒ **Single-variable ladder, to run when convenient:** boot with the three mods
ON and, before running anything, hover the main menu and the HUD bar. If it
strobes already, nothing this sitting ran is implicated and the next control is
a mods-off boot. If it does **not** strobe, run `SMRTK.ConsoleControl()` and
hover again — a strobe appearing there names step 2's diagnostic as the trigger
and makes it an 03A item.

### ⭐ Owner's hypothesis (2026-09-13): a presentation/compositing fight, not Lua

> *"it sounds like this is a rendered chrome window so its a window on top of a
> window which can cause a single space where two windows are fighting for
> exclusion at the same time. That can happen on my other monitor if I take smr
> out of full screen exclusive and put it in windows mode and try to use things
> on my other monitor."*

This explains what the Lua-level hypotheses could not: **why every widget class
strobes equally** — vanilla menu rows, vanilla HUD icons and our `XButton`s alike.
No single Lua defect touches all three; a presentation-layer fight touches all of
them by construction. It also fits *survives mod-disable* and *cleared only by a
full restart*, both of which are process/display-mode properties, not mod-state
properties.

**Machine state, read this session (not owner-reported):**

| | |
|---|---|
| GPU / display | RTX 4080, `Resolution = point(3840, 2160)`, `DisplayIndex = 0` |
| **`Vsync`** | **`false`** |
| **`Upscaling`** | **`DLSS`** (temporal) |
| preset | `VideoPreset = "Ultra"` throughout |
| overlay stacks live | **Discord** (6 processes), **GameBarPresenceWriter** + **XboxPcAppFT**, **nvcontainer** (NVIDIA), **Steam** + 7 `steamwebhelper` |

Four independent overlay/compositor stacks were resident, and the clip itself was
made with a screen recorder (`Recording 2026-09-13 210923.mp4`, Windows
recorder naming) — i.e. a capture overlay was active **while the symptom was
being filmed**. Unsynced presentation (`Vsync = false`) plus temporal upscaling
(DLSS) plus a compositing overlay is a known-plausible producer of exactly the
alternating-frame signature measured above, and a thin hover highlight is the
element most likely to alternate under temporal reconstruction.

⛔ **Not proven, and it does not clear the mod** — but it is cheaper to test than
the mod ladder and it now has the stronger prior. **Test order (cheapest first,
one variable each):** ① `Vsync = true` or an fps cap · ② `Upscaling` off DLSS ·
③ close Discord / Game Bar / NVIDIA / Steam overlays · ④ only then the mod A/B.
⚠️ Also note the sitting's own working pattern — the owner alt-tabbed to the chat
on nearly every step — which is repeated focus loss on a 4K exclusive-fullscreen
title and is itself a candidate trigger.

⇒ Routed, not filed. If ①-③ clear it, this is a rig/display-stack matter and
**not** an SMRTK item and **not** a vanilla defect entry. If it survives all
three, the mod ladder above is next.

## Outbox items raised during the sitting (for 03A / 99)

### ⛔ The owner's cheat route sets `Platform.cheats`, and it would poison step 2

**Owner, during the sitting:** *"I have to manually copy and paste these to
commands `Platform.cheats = true` `CheatToggleInfopanelCheats()`"*.

That is a **session-global** enable, not the transient GED-window one this
report described earlier. Consequence, from the gate read above
(`CommonShortcuts.generated.lua:176`): with `Platform.cheats = true` in force,
`AreCheatsEnabled()` is true, so `SMRTK.ConsoleControl()`'s negative leg reads
`negative=true` and step 2 is **non-discriminating** — it would fail to credit
our hook for a reason that is the sitting's own doing, not a defect.

⇒ **Step 2 is only valid in a boot where `Platform.cheats` was never set.**
The brief's ordering already protects this (control → quit → fresh load), because
`Platform` is rebuilt per process. The binding instruction is: in the boot used
for steps 1–8 the owner must **not** paste `Platform.cheats = true`. Making that
paste unnecessary is a large part of what the toolkit is for.

Step 0A's `PLATFORM_READ cheats=nil` was taken **before** any such paste, so the
baseline reading stands.

⭐ **This is also a scope finding for 03A/P4.** The owner's habitual route is two
pasted lines every session, one of which flips a global that changes what the
game's own shortcut gate does. A toolkit button that arms the *console* without
touching `Platform.cheats` is the thing that retires that paste — and the
difference is exactly what step 2 measures. Whatever P4 builds for "force-open
console", it must not set `Platform.cheats`.

### Duplicated-line question — READ IN THE FILE, both shapes explained

Raised mid-sitting by `smr-bugfixpack-8f` from the owner's screen. The
diagnostic asked for was whether the duplication is in the **log file** or only
on screen. Counted in the file (`Mars.exe-20260913-20.40.33`):

| id | verb | lines in file | `[mod]`-prefixed | bare |
|---|---|---|---|---|
| 7, 8 | `SHORTCUT` | 2 each | 1 | 1 |
| 9, 10 | `PANEL_RESTORE` | 2 each | 1 | 1 |
| 14, 17, 25, 27, 28 | various | 2 each | 1 | 1 |
| **15** | `SCRATCH_DISCARDED` (console-typed) | **3** | 1 | **2** |

**Two lines per `Log` call is by design, not duplication.** `T.Log` emits once
through `ModLog` (which the game prefixes `[mod]`) and once through
`ConsolePrint` (`70_SMRTK_Core.lua`, `T.Log` body). Every internal call shows
exactly this 1+1.

**Shape 2 — same id twice — is a console echo of a return value, not a doubled
record.** `T.Log` ends with `return line`, and the console wraps a typed
expression as `ConsolePrint(print_format(<expr>))` (`uiConsole.lua:362`). So a
`SMRTK.Log(...)` **typed at the console** gets its own returned line printed a
second time. It affects only console-typed `Log` calls — confirmed against the
previous boot's log, where the two console-typed `Log` calls (`PLATFORM_READ`,
`SCRATCH_READ`) show 3 lines each and every internal call shows 2. No id is ever
written twice by the logger. Counting toolkit actions by id remains sound.

**Shape 1 — different ids at the same `t` — is two genuine calls, and only one
of them is worth acting on.**

- `SHORTCUT` ×2: two shortcut rebuilds. Already falsified as harmless in step 1
  — six such lines, one keypress, one toggle.
- `PANEL_RESTORE` ×2: **real, and an 03A item.** `restore_panel()` is registered
  on **three** messages — `OnMsg.InGameInterfaceCreated`, `OnMsg.PostLoadGame`
  and `OnMsg.CurrentMapChangeDone` (`71_SMRTK_Panel.lua:207-209`). A savegame
  load fires the first two, which is the 2 lines measured here; the map-change
  route was never exercised by 02, so a logging fix tested only against a load
  would cover two of three callers. (Third registration caught by
  `smr-bugfixpack-8f`; this report first said "both", which was wrong.)

⚠️ **But it is a logging-precision finding, not a double panel.** `T.OpenPanel()`
opens with `if T.panel and T.panel.window_state ~= "destroying" then
T.panel:SetVisible(true); return T.panel end`, so the second restore reuses the
existing instance. Behaviourally confirmed: one drag produced exactly one
`SMRTK_MOVE`, one keypress exactly one `panel_toggle`. Two panel instances would
each own a strip and a tab bar and would have doubled those. **One panel, two log
lines.** Recommendation for 03A: log `PANEL_RESTORE` only when the panel was
actually created or made visible, so an agent counting restores is not misled.
⛔ This is P4's persistence evidence, so the count mattering was the right worry.

**Not ours:** `[SMRTest] console enable requested` appears 8 times = 4 calls ×2,
from the **legacy** `00_TestCore.lua:526`, outside the SMRTK fence. It is the
bootstrap 03B is asked to decide about retiring, and step 2 has now supplied the
evidence for that decision.

### Root cause for the whole "UI chrome on screen" family

`SMRTK_CLEAR`, `SMRTK_TAB` and `SMRTK_MOVE` all reach the screen for one reason:
`T.Log` calls `ConsolePrint` for **every** line, unconditionally. So a
destination policy is a change in **one place** — a per-verb or per-call
destination on `T.Log` — not a change per action. Requirement (B) is unaffected
either way: the line still reaches the log file and the ring.

### CLEAR logs onto the screen it just wiped — peer finding, verified, fix corrected

Raised by the orchestrator session `smr-bugfixpack-8f` during the sitting.
**Verified here, both sides:**

- Live log carries `SMRTK_CLEAR action=clear status=OK t=7506849 id=22`.
- Mechanism confirmed at source: `dispatch` runs `pcall(callback, ...)` — for
  `clear` that is `cls()` (`70_SMRTK_Core.lua:258`) — and only then calls
  `T.Log(verb, fields)` (`:194`). The log line is printed after the wipe, so a
  "clear screen" button reliably leaves exactly one line on screen.

⚠️ **Correction to the proposed fix.** The peer described it as "a one-line
reorder in the core", emitting `SMRTK_CLEAR` before `cls()`. It is not, because
the line is not emitted by the action body at all — it is emitted by the generic
`dispatch` after the callback returns. Three shapes, only one of which is sound:

1. ⛔ **Move `T.Log` before `pcall(callback)` for all actions** — breaks every
   action whose fields come from the callback's return value. Step 3's own
   `SMRTK_ACTION` line carries `before=`/`after=`, which do not exist yet at that
   point. This would silently empty the most important record in the sitting.
2. ⚠️ **Defer `cls()` onto a thread** so it lands after the log — reintroduces
   ordering nondeterminism for a cosmetic gain.
3. ✅ **A per-action opt-in honoured by `dispatch`** (e.g. `log_first = true` on
   the `clear` definition), so the record reaches file, ring and screen, and the
   wipe then takes the screen. Requirement (B) is untouched: one line, one
   logger, still present everywhere an agent reads.

Dropping the line is the worst option — an agent reading the log wants to know
the screen was cleared at that moment. **No code was changed during the sitting**
(rule 16, `Mars.exe` live; and the core is the instrument under measurement).
03A/03B decide the shape.


## VERDICT — ✅ PASS WITH CORRECTIONS. The kill gate does not fire.

All four premises were read in play on 2026-09-13, build **24995074**, fixture
the BlueSun `BlankBig_01` colony (`SMRTK_BASELINE_CLEAN`, sol 10, `EF-075`
baseline `403908`). **99 runs its full form, not the reduced one. 03A is
released.**

| # | premise | verdict | the line that decides it |
|---|---|---|---|
| **P1** | a leaf action leaves `CheatsUsed` empty | ✅ **PASS** | `SMRTK_ACTION action=skeleton_fill after=180000 before=13000 object=StorageMetals(1054) status=OK` then `TAINT_READ used=false`, against a control that produced `entries=1` |
| **P2** | `ConsoleEnabled` gives the console with mod tools closed | ✅ **PASS** | `CONSOLE_CONTROL discriminates=true negative=false positive=true status=OK`, witnessed by `SHORTCUT console=false` then `console=true` across the two rebuilds |
| **P3** | the tap sees console lines | ✅ **PASS** | `TAP_READ native_console=1 native_print=1`, clipboard read from Windows itself carrying `source=console` **and** `source=print` |
| **P4** | the panel survives a save/load | ✅ **PASS** | `DISARM action=print_tee reason=SavegameSaved`, then `ROUNDTRIP_READ armed=0 same_print=true tab=Kit x=1125 y=243` |

⭐ **The single most compact statement of the result** is the archived logs' own
`ObjCheat` counts: **1** in `smrtk02_…19.58.32.log` (the deliberate vanilla
control) and **0** in `smrtk02_…20.40.33.log`, which contains every toolkit leg
including the depot fill. The toolkit filled a depot and never once entered the
route that writes the taint.

### Archived evidence

- `docs/archive/logs/smrtk02_Mars.exe-20260913-19.58.32-6a91a190.log` — step 0:
  the clean baseline read and the RED control. 69 `SMRTK_` lines, **1** `ObjCheat`.
- `docs/archive/logs/smrtk02_Mars.exe-20260913-20.40.33-6a91a190.log` — steps 1-8.
  196 `SMRTK_` lines, **0** `ObjCheat`.

### Corrections that strike and supersede `SMRTK_SKELETON_PREDICTIONS.md`

1. ⛔ **Step 3's script, § "Predictions for 02" row 3 and the DEPARTURES bullet
   "The sitting registers its own Fill action".** The body tests
   `type(o.resource)=="string"` and calls `StorageDepot:CheatFill` with
   `max_amount_<resource>`. **No shipped depot instantiates that shape** — every
   storage template is `object_class = "UniversalStorageDepotBase"`, whose
   `GameInit` sets `self.resource = self.storable_resources`, a **table**
   (`StorageDepot.lua:444`). The action could only ever refuse. Superseded by the
   corrected body using `IsKindOf(o,"UniversalStorageDepotBase")`,
   `#storable_resources == 1`, `GetStoredAmount`/`GetMaxStorage` and the `:710`
   leaf. **Requirement (A) is unaffected** — the corrected leaf carries no
   `LogCheatUsed`/`NetSyncEvent` either.
2. **Step 0's `cheats` value.** Predicted unverified, this session predicted
   `false`; **measured `nil`** — the key is absent from `Platform`. Falsy either
   way, gate arithmetic unchanged.
3. **Step 8's "panel is open after the load".** Not observed as written: the
   panel was closed at save time by an operator action, and `open=false` was
   correctly restored. The property is established instead from **two** legs —
   step 1 restored `open=true`, step 8 restored `open=false` — which is stronger.
4. **Step 1's `hook=PreLoadGame` is not the only arm.** Four arm sites were seen
   in play: `DataLoading`, `PreLoadGame`, `PreNewMap` (unexercised) and
   **`ChangeMap`**, the last during the round trip.
5. **`SMRTK_SHORTCUT` appears many times per boot** (six in one boot), not once.
   Rebuilds against one singleton host; **one live action**, falsified in play by
   one keypress producing exactly one `panel_toggle`.

### What may NOT be claimed from this sitting

- **Achievement eligibility.** `UNAVAILABLE:sandbox` throughout;
  `CanUnlockAchievement` is blacklisted and was confirmed `nil` from the console.
  No-taint is **necessary, not proven sufficient** (`EF-096`, `EF-094`).
- **Gamepad.** Not tested.
- **Native `OnLuaError`/`OnThreadError` delivery.** Step 7 invoked our handler
  directly; it proves formatting and counting, not engine delivery.
- **Any page beyond the skeleton.** Every page is a placeholder; `pause` and
  `stop_disaster` correctly returned `NOT_BUILT`.
- **That P1 generalises.** One action, one class. P2 must re-establish it per
  action — and correction 1 shows the object model is where that will go wrong.

### Outbox to 03A (one paragraph, for every payload's inbox)

P1-P4 all PASS on build 24995074; the core, the logger, the taint assert, the
`ConsoleEnabled` arm, the ring, the clipboard and LocalStorage persistence are
all confirmed in play, so build on them. The native console tap **and** the print
tee both carry real output, so either is a valid capture route. Five things to
carry: **(a)** per-object code must target `UniversalStorageDepotBase` and
`#storable_resources`, never `StorageDepot.resource` — 01's leaf refused on every
depot in the game; **(b)** `AsyncCheat*` infopanel entries bypass `ObjCheat` and
never taint even in vanilla (`ClassHierarchy`, `ClipPlane`, `Gizmo`, `Inspect`,
`Properties`, `Screenshot`), so they need no re-implementation; **(c)** `CLEAR`
logs onto the screen it just wiped, and the fix is a per-action opt-in honoured
by `dispatch`, never moving `T.Log` before the callback, which would empty
`before`/`after` on every action; **(d)** `PANEL_RESTORE` logs once per
registration and there are **three** (`InGameInterfaceCreated`, `PostLoadGame`,
`CurrentMapChangeDone`) though only one panel results — log on actual
create/make-visible; **(e)** `CopySince` is destroyed by the operator's next
copy, so it must be the last command of a block, and the panel **button** form is
immune. The owner's surface ruling and ranked fallback ladder are in ck175.

### Outbox to 99

The taint invariant is re-derivable from the archived logs alone: `ObjCheat`
count 1 in the control boot, 0 in the toolkit boot. The four `LogCheatUsed` call
sites were enumerated tree-wide and none is reachable from a direct leaf call.
Two instrument defects on the attending side are recorded in full rather than
quietly fixed — a truncated `grep | head -15` that hid the `CheatFill` override,
and a proposed flicker control that could not have cleared the panel because
`panel_toggle` only calls `SetVisible(false)`. The flicker itself is routed,
measured and **unattributed**; the last boot carried the mod with no strobe, so
it does not reproduce on mod-load alone.
