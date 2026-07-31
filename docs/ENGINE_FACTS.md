# Engine Facts — hard-won, do not re-derive

**Sole authoritative home** for the engine behaviors this project has proven
(extracted verbatim from STATUS.md "Key technical facts", audit remediation
3.2, 2026-07-29 — additions go HERE, with a date). Read this before writing or
reviewing any fix: several of these behaviors are the opposite of what the
code suggests.

- **Mod code loads BEFORE the classes are built.** `autorun.lua:423` calls
  `ModsLoadCode()`; classes are assembled later in `OnMsg.Autorun`
  (`CommonLua\Core\classes.lua:980`). So at apply() time a class global is still
  its **classdef**, exposing only members the class declares ITSELF — an inherited
  method reads as nil. Two consequences:
  * `function Building:X() ... end` in a fix DOES propagate to every subclass
    (the classdef is what gets flattened later) — this is why class-method
    replacement works at all;
  * an apply() self-check must look for the method on its **declaring** class.
    Checking `Station.OnDemolish` (declared on Building), or
    `UniversalRocketBase.IsAutoModeEnabled` (declared on the AutoMode mixin),
    finds nil and silently deactivates the fix. F64 shipped broken this way and
  * **the flattening cuts BOTH ways at runtime (proven live 2026-07-28):** once
    classes are built, each class carries its own baked copy of every method —
    so a RUNTIME patch on a base class (console wrapper, TestKit logger toggle)
    is INVISIBLE to already-built derived classes. Live proof:
    `rawget(UniversalLanderRocket, "CreateAutoCargoRequest")` resolves to
    `Fix_LanderCargoRatchet.lua(124)` (the pack's pre-build replacement, baked
    in — the live lander RUNS the fix), while the TestKit `AutoCargo` logger's
    runtime wrap of `UniversalRocketBase` never fired across a full load cycle.
    Rule: pre-build (mod-load) patches on the declaring class propagate;
    runtime instrumentation must target the LEAF class the instances actually
    use (e.g. `UniversalLanderRocket`, not `UniversalRocketBase`). TestKit's
    AutoCargo logger needs the leaf-class repair (game-free item, queued).
    was corrected this session.
- `g_Consts` is a **GameVar** (`Lua\Modifiers.lua:427`) and does not exist while
  mods load — read it inside the patched function, never in apply(). `const` IS
  populated at that point.
- **`CurrentModOptions` is PER-MOD-ENV** (proven by the D09 probe A/B,
  2026-07-29 late): the engine loads each mod's options object before code
  (Mod.lua:2128-2131, values rawset onto it :679-683) and each mod env's
  `CurrentModOptions` aliases that mod's OWN object. A mod reading another
  mod's options (the TestKit driving the fix pack's dials) must go through
  `Mods["<id>"].options` — writing your own env's `CurrentModOptions` silently
  changes the wrong object. Runtime rawsets on `Mods[id].options` are
  session-only (AccountStorage saves only via the options dialog's Apply).
- Engine Lua tolerates `#nil`/`next(nil)`/`ipairs(false)` (verified from working
  code paths) but NOT boolean relational compares — don't report/fix nil-iteration
  as crashes. `/` truncates (integer division); that is what makes F12's
  `a*24/v*24` unsatisfiable.
- **Mods run in a sandbox (LuaModEnv) on ALL platforms**, including unpacked dev
  mods (Mod.lua:1730/:1750; blacklist at :1267-1428). Key facts: `debug`, `io`,
  `package`, `lfs`, all `Async*` file ops, load/dofile/require are BLACKLISTED;
  `os` is `{time}` only; `setmetatable` is available (:1408 commented out);
  `rawget` is a safe wrapper that reaches real `_G` for non-blacklisted names —
  the pack's `rawget(_G, "X")` pattern works; `_G` maps to the env, but NEW
  globals created at load are rawset into the REAL `_G` (:1557-1563), so
  `SMRFixPack`/`SMRTest` are cross-mod and console visible; `Msg`/`OnMsg` are
  filtered only for persist/debug messages. The fix pack Code/ uses no
  blacklisted API (verified) — sandbox- and console-clean.
- **`error()` and `assert()` do NOT unwind mod code — they report and execution
  continues** with the next statement (LuaExports.lua:567 "asserts pop instead of
  being printed out"). Never use them for control flow; `pcall` still catches
  genuine runtime errors. Cost us four bogus FAILs and ten ERRORs in the first
  A/B pair (see the diagnosis section).
- **`rawset(_G, k, v)` from mod code writes only into the mod's own env table**
  (`_G` IS that table, Mod.lua:1603; `rawset` is the real rawset, only `rawget`
  is replaced at :1606). To write a global the game can see, assign it —
  `_G[k] = v` goes through `ModEnvMeta.__newindex` (:1557-1563) into the real
  `_G`. `rawget(_G, "X")` for READS is fine (safe_rawget falls through, :1577).
- **CORRECTION of an earlier "fact": `debug.getinfo` is NOT available in mod
  code** (debug is blacklisted). The Test Kit's install probes
  (00_TestCore.lua:37) break under the sandbox; repair in progress — bridge
  real `debug` via a console-exec path or SKIP install probes with a
  `SMRTest.debug = debug` console instruction. `GetStaticMsgNames()` (F06 probe)
  is a real global and still fine.
- Patch points that work: `PeriodicRepeatInfo[name]` slots (THREAD/SLEEP/FUNC/COND
  = 1..4, CommonLua\Core\lib.lua:1538+), `GlobalGameTimeThreadFuncs[name]` +
  `RestartGlobalGameTimeThread(name)` on LoadGame (Lua\Config\_fixup.lua),
  class-method replacement, chained wrappers, `OnMsg.*` additive handlers,
  preset/data patches at ClassesPostprocess.
- A post-wrapper on a **command** method (anything ending in `SetCommand`) never
  runs — `DoSetCommand` kills the calling thread. `Colonist:Idle` must be
  pre-wrapped (F73).
- Mod registry: every fix goes through `SMRFixPack.Register(id, {title, apply})`
  (Code/00_Core.lua); apply self-checks the target and returns a reason string to
  deactivate gracefully; `SMRFixPack_Disabled` = user veto; `SMRFixPack.ListFixes()`
  console status.
- All line numbers reference `ModTools\Src`; the game executes `Packs\Lua.fpk`.
  **PARITY PROVEN 2026-07-29 (QA session): the shipped build IS Src.** The full
  `Lua.fpk` was extracted (FLPK container, zstd per file) and diffed:
  **2,250 of 2,256 shipped Lua files are byte-identical to Src**; the only 5
  divergences are engine/tooling files (Camera state, GED Stubs, asyncop/sound/
  xinput API wrappers) — zero gameplay logic. Shipped build stamp:
  `1.0.7.396349` (`_LuaRevision.lua`, fpk-only). Keep apply() self-checks — they
  guard *future* patches — and re-run the extraction diff after every game
  update.
  **The earlier "PROVEN DIVERGENT" fact recorded here was a misreading and is
  WITHDRAWN:** `GetCameraLookAtPassable` is a **`local function` in Cheats.lua
  (`:42`)** — a file-local upvalue, never a global, identical in Src and
  shipped. Probing it from the console returns `attempt to call a nil value`
  *by design* (console code cannot see file locals). The bare
  `CheatMeteors("storm")` no-op has a mundane explanation: the helper returns
  nil when no passable point exists within 100m of the camera look-at
  (`Cheats.lua:44`), and the body is `if pos then … end` with no else — so
  "always pass an explicit position" remains the right practice.
  `GatherTransportableResources` (`ResourceTracking.lua:216`) is *called* but
  defined in neither Src nor the shipped Lua (verified in the extraction) — a
  genuine engine C export. F12's fix checks for it at apply time.
- **`print` does NOT reach the log file — it goes ON-SCREEN** (recorded
  2026-07-29, correcting a backwards claim that had been carried in the
  continuation prompt's console facts). `print = CreatePrint{""}`
  (`CommonLua\Core\lib.lua:202`) passes no `output` option, and `CreatePrint`
  defaults `output = ConsolePrint` (`:149`), which the engine's own docs
  describe as printing "to the console" — as opposed to `OutputDebugString`,
  documented as "does not appear in the console log". **`ModLog(...)` is the
  only path proven to reach the on-disk log** (ModLog → ModPrint → DebugPrint,
  `Mod.lua:109-132`) — which is why every fix and probe reports through it, and
  why `FlushLogFile()` is needed before reading the log mid-session. Practical
  consequence: a console snippet whose output must survive the session has to
  call `ModLog`, not `print`.
- Sample mod format in `<game>\ModTools\Samples\Mods`; docs in `ModTools\Docs\index.md.html`.
- **Replacing an EXISTING global from mod code works**: `ModEnvMeta.__newindex`
  (`Mod.lua:1557-1563`) rawsets any non-blacklisted key into the real `_G`, and the
  "attempt to create a new global" assert only fires for names that do not already
  exist there. Generated closures (script conditions, sequence code) resolve the name
  at call time, so they pick the replacement up. Read the name back with
  `rawget(_G, ...)` in apply() to confirm the write landed — F22 does.
- **`OnMsg` is additive, confirmed structurally**: four shipped files each define
  `OnMsg.StationsConnected` (`Station.lua:1213`, `Track.lua:668`,
  `TrainTransport.lua:357`, `UnderconstructionSign.lua:87`) and all four must run.
- **GAME-TIME THREADS PERSIST BY DEFAULT — real-time threads do not** (popup
  audit 2026-07-30; the F83 investigation briefly assumed the opposite and
  retracted a fix recommendation on it). `MakeThreadPersistable`
  (cthreads.lua:224-230) exists to CLEAR the flag on GT threads
  (`XWindow.lua:1578` clears it on a maybe-GT thread) and to SET it on RT
  threads (`_fixup.lua:36`, `Notifications.lua:215` — their GT twins go bare);
  `OnMsg.PersistPostLoad` (`_fixup.lua:50-66`) expects global GT threads to
  arrive through the save. Persist serializes blocked STACKS —
  `PersistGatherPermanents` (cthreads.lua:451-464) registers `Sleep`/`WaitMsg`/
  `WaitWakeup`/`CObject.PlayState` as "sleeping function[s] found in the thread
  stack" — and preserves shared-reference identity across one save's graph.
  Corroborated in play constantly: unit command threads are bare
  `CreateGameTimeThread` (CommandObject.lua:100) and resume mid-command after
  every load. Consequences: a consequence computed after a wait is safe in a GT
  thread and LOST in an RT thread (the F83 family); "no MakeThreadPersistable"
  on a GT thread is the SAFE default, not a missing call.
- **Every shipped popup is ASYNC — the persistable popup path is dead code**
  (same audit). `ShowPopupNotification` opens with
  `assert(not bPersistable) -- we don't support these`
  (PopupNotification.lua:246); no call site passes it, so `OnMsg.PersistSave`
  (:347-355), which keeps only `sync_popup_id` entries, always saves an EMPTY
  popup queue — an OPEN popup's context never survives a load. The system is
  safe anyway because notifications persist (`GameVar("Notifications")`,
  closures included — observed, F83) and GT waiters persist (above); an open
  popup is modal + game-pausing + shortcut-eating, so no ordinary save can
  exist in its window (the shield is UI reachability, not the save system —
  `CanSaveGame` has no popup clause; see F85 for the rebind edge).
- **TOOLING: never round-trip a doc through PowerShell 5.1 `Get-Content -Raw` +
  `WriteAllText`.** `Get-Content` without `-Encoding` decodes UTF-8 files as cp1252, so
  every `—`, `↔`, `≤` comes back double-encoded and the whole file shows as changed.
  It happened to `BUGS.md` in the wave-4 session and was reversed with
  `Encoding.GetEncoding(1252).GetBytes(UTF8.GetString(bytes))`; nothing was committed
  corrupted. Use the editor's own file tools for docs, or pass `-Encoding UTF8` on
  BOTH ends.
