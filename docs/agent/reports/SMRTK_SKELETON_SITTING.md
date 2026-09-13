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
- [x] Fixture survey + backup of the only 1.1.0 save on the rig.
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
  (`autorun.lua:249-256`). `Autosave Sol 490`'s header serialises the whole
  `Platform` table (`Savegame.lua:779`) and it lists exactly
  `desktop, editor, goldmaster, paradox, pc, steam` — **no `cheats`, no
  `developer`, no `asserts`**. So on this build, with the Mod Manager closed,
  `cond` reduces to `ConsoleEnabled` alone and 01's
  `discriminates=true negative=false positive=true` is well-founded rather than
  hopeful. ⚠️ This is derived from a save header, not from the console. Step 0's
  `PLATFORM_READ` is still the authoritative read, and it answers 01's open
  question ("record the actual `cheats` value; it was unverified at authoring")
  — expect `cheats=false`, and treat anything else as the surprise it would be.

## Fixture — one candidate, and it is the owner's colony

Scanned the plain-text header of all 61 saves in
`%APPDATA%\Surviving Mars\76561198020568696\` (the Relaunched build has no saves
folder of its own; it writes to the legacy one). **Exactly one is a 1.1.0 save:**

| save | `lua_revision` | `orig_lua_revision` | sols | sponsor | mods at save |
|---|---|---|---|---|---|
| `Autosave Sol 490.savegame.sav` | **403908** | **403908** | 490 | Japan | `active_mods = {}` |

`403908` is the baseline build exactly (`EF-075`); `orig_lua_revision` equal to it
means natively created on 1.1.0, not migrated. Every other save is the **original**
Surviving Mars (`lua_revision` 1009413 / 1011166 / 245618), not this game.

⛔ **`AreCheatsUsed()` is NOT readable from disk.** `CheatsUsed` is a `GameVar`
(`Network.lua:241`), so it lives in the compressed body, not the ~2 KB header.
**Step 0's first line IS the fixture test** — if it reads `used=true`, this save
cannot serve the leg and fixture provisioning is owed (STATE prices a new 1.1.0
colony in hours, `EF-079`/`EF-080`).

**Backed up before anything touches it** — `Autosave Sol 490.savegame.sav`,
38,643,956 B, md5 `a8d9532f4bb3aee84779b069a15be4b8`, copied to the session
scratchpad and verified byte-identical by md5. The sitting writes only new names
(`SMRTK_BASELINE_CLEAN`, `SMRTK_SCRATCH_TAINTED`, `SMRTK_ROUNDTRIP_CLEAN`) and
never saves over the autosave; the colony stays paused, so no new autosave can
land either.

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
