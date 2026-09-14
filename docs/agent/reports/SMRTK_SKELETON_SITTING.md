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
- [ ] Owner sitting, steps 0–8.
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

## Verdict

⛔ **NOT REACHED.** Fill in per prediction after the sitting.
