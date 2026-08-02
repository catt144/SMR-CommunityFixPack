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
    finds nil and silently deactivates the fix. F64 shipped broken this way
    and was corrected in that session.
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
    AutoCargo logger got that leaf-class repair on 2026-07-28
    (`90_Loggers.lua` — an earlier "queued" note here had gone stale; caught
    by the 2026-08-01 agent-doc review).
- **"OFF" IS THREE DIFFERENT THINGS, and only ONE of them touches the save**
  (established 2026-08-01 from the F86 Site 2 mechanism + PT-58; the project had
  been using "off" loosely and it matters to F86 and to D13). Ranked by what they
  actually remove:

  | switch | hooks installed? | mod env exists? | seeds NEW frames into saves? | orphans frames already in a save? |
  |---|---|---|---|---|
  | **Mod Options toggle** (optional modules) | **YES** — wrappers stay installed and pass through at call time (`SMRFixPack.IsActive`, `00_Core.lua:39-42`) | yes | **YES** | no |
  | **`SMRFixPack_Disabled[id]`** user veto | **depends on where the module installs** — `Register` returns before `run_apply` (`00_Core.lua:384-388`), so an apply()-time installer never hooks; a **FILE-SCOPE** installer (e.g. `Opt_DroneOverhaul` parts 1-2) has already hooked before `Register` is reached, and the veto only flips its status | yes | apply()-installers: no · file-scope installers: **YES** | no |
  | **Mod Manager disable / uninstall** | no — mod code never loads | **NO** | no | **YES** → `Unpersist missing permanent: Mod/<id>` and `[LUA ERROR]` from any captured body that touches a mod-created name |

  **So "all toggles off" is NOT equivalent to "pack removed", and the difference
  is the whole of F86.** With any toggle off the environment still exists, so a
  captured frame resumes, resolves `SMRFixPack`, reads inactive and no-ops
  cleanly — harmless *at that moment*. Removal is what turns the same frame into
  an orphan. A toggle is therefore a loaded gun with no trigger: **it decides
  nothing about persistence, only about behaviour.** This is exactly why
  `Opt_DroneOverhaul` leaked with its own toggle OFF (the founding Site 2
  finding, 98/session) — and why a save made by a player who "turned the mod off"
  still carries whatever was installed at file scope.

  ⚠️ **Corollary for D13:** the cleaner cannot assume a save is clean because the
  player had the pack toggled off. The only state that keeps frames out of a save
  is *not having installed the hook*.

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
- **`Msg`/`OnMsg` are PER-ENV OWN KEYS and cannot be stubbed or deleted from
  mod code** (measured 2026-08-01, Tier-1 sitting; source: Mod.lua). LuaModEnv
  installs `env.Msg = safe_Msg` / `env.OnMsg = safe_OnMsg` as env-locals
  (:1600-1610) AND `ModEnvBlacklist` lists both (:1288-1289), which gates them
  out of `ModEnvMeta.__newindex` and `safe_rawget`'s fall-through alike. So:
  assignment through `_G` is a SILENT NO-OP, and `rawset(_G, "Msg", nil)`
  deletes the env's own wrapper PERMANENTLY (nothing can read the real one
  back — blacklisted) while the real `_G` and every other env stay untouched.
  Observed live: a TestKit probe stubbing `Msg` blinded only the TestKit env;
  a later probe's `Msg(...)` errored (`60_Probes_Opt.lua:417`) and popped the
  engine's "Mod Flagged" warning; the game and the fix pack were unaffected.
  Guard: TestKit `00_TestCore.lua` ENV_SPECIALS refuses these keys in
  `SetGlobal`/`WithGlobals`. Same class: `rawget`, `getmetatable`, `os`, `_G`.
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
  code** (debug is blacklisted). RESOLVED: the Test Kit's install probes SKIP
  in the retail sandbox — the 9 `[install]` SKIPs in every A/B leg's expected
  numbers are exactly this, by design. `GetStaticMsgNames()` (F06 probe) is a
  real global and still fine. (An earlier "repair in progress" note here had
  outlived its resolution; caught by the 2026-08-01 agent-doc review.)
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
- **A MOD-AUTHORED CLOSURE STORED ON A PERSISTED GAME OBJECT GOES INTO THE SAVE,
  SURVIVES UNINSTALL, AND KEEPS RUNNING** (measured 2026-07-31, drone Q1/Q2
  sitting). A temporary experiment module assigned an instance-level
  `GetPriorityForRequest` onto a Building. The colony was saved, the module was
  removed from the mod's `code` list, and the save was loaded. The read
  `rawget(obj, "GetPriorityForRequest")` returned **`function: 000001E95D57A6B0`**
  — and it was still being *called*: a `ReconnectTaskRequesters` re-filed that
  building's requests using the vanished mod's logic. Zero Lua errors throughout.
  Persist serialises the function rather than dropping it, because a mod function
  is not in `PersistGatherPermanents`.
  **Consequences:**
  * Writing a function onto a game object is a **permanent, un-removable
    modification to the player's savegame** — a far larger footprint than a
    GameVar, and one FIX_POLICY §3 does not currently name.
  * The orphaned closure runs in a world where its mod's globals are gone, so
    any reference to `SMRFixPack.*` inside it would index nil after uninstall.
  * **UI windows are NOT affected** (XWindows are not savegame-persisted).
  * ⚠️ **CORRECTED 2026-07-31 by PT-20 — the "class tables are NOT affected"
    clause below was WRONG, and so was framing the hazard as "specifically
    instances".** Class tables really are restored as permanents by name, and
    that turns out not to protect anything: `Opt_DroneOverhaul` writes
    `Drone.Idle` — a class-table write — and it leaked into the save anyway,
    because the route is a **thread stack**, not the storage location. See the
    entry immediately below.
  * ~~Unverified adjacent risk~~ — **MEASURED 2026-07-31:**
    `GlobalGameTimeThreadFuncs[name]` replacements do leak.
    `Fix_MeteorFrequency` was caught red-handed (F86).

- **THE REAL RULE (measured 2026-07-31, PT-20 — supersedes the framing above):
  A SAVE CAPTURES EVERY GAME-TIME THREAD WITH ITS BLOCKED STACK, SO ANY MOD
  FUNCTION SITTING BELOW A YIELD ON SUCH A THREAD GOES INTO THE SAVE.** The test
  is not *where is this function stored* but:
  > can it be executing, or blocked, below a `Sleep`/`WaitMsg`/`WaitWakeup` on a
  > **game-time** thread at the moment the save is written?
  * Serialisation is **by value**, not by name — a mod function is not in
    `PersistGatherPermanents`. Writing a body with no upvalues does NOT make it
    persist "by the global name it is written to"; that belief is in two of our
    own file headers and is false.
  * Each mod env is a permanent (`Mod.lua:1642-1644`,
    `permanents["Mod/" .. mod.id] = mod.env`). With the mod gone it cannot
    resolve and a **fallback table** is substituted
    (`Unpersist missing permanent: Mod/<id> | Fallback permanent: table: …`).
    ~~so the orphan runs with an empty `_ENV` and every global lookup inside it
    fails.~~ ⚠️ **CORRECTED — MEASURED 2026-07-31 21.23 (orphan-env probe, clean
    absence control) + source-pinned: the fallback is a fresh
    `LuaModEnv{CurrentModId=…}`** (`Mod.lua:1647-1656` — the resolver; the log's
    `[7]` is its seven seeded entries) **whose `ModEnvMeta.__index` falls
    through to the real `_G`. An orphan resolves every VANILLA global and loses
    ONLY the names its own mod creates** (`SMRFixPack` is nil after uninstall
    because the mod that creates it never loaded — not because lookups fail);
    its upvalues survive by value. **Consequence: an orphan dies loudly iff its
    body touches a mod-created global name; otherwise it KEEPS EXECUTING** —
    bounded if it self-limits (`Fix_CrystalMysteryHang`'s frozen 10-sol
    deadline), forever if it loops (`Fix_RainsDeadlock`'s `fixed_loop` is
    all-vanilla names and would run our rains loop permanently in an
    uninstalled player's save). The zero-upvalue discipline — adopted on the
    false by-name premise — is worth keeping for the inverted reason: global
    helper lookups make orphans die loudly, the safer failure. Per-module
    outcomes: `docs/reports/F86_ADJUDICATION.md` §8.1-8.2. This also explains the
    `GetPriorityForRequest` orphan above running with zero errors.
  * A save only captures **blocked** threads, so purely synchronous mod code —
    data patches, getters, `Can…` predicates, UI handlers — can never be
    captured **through the thread-stack route**.
    ⚠️ **CORRECTED 2026-07-31 (F86 adjudication): that clause is not the whole
    test, and "the test is not where is this function stored" above is wrong as
    written.** Persist serialises by value everything reachable from a captured
    thread — every frame's function, locals and upvalues — plus persisted
    storage. The full rule: **a mod function enters a save iff its VALUE is
    reachable from the persisted graph at write time** — (a) its frame below a
    yield on a blocked persistable GT thread; (b) held in a live local/upvalue
    of ANY captured frame, engine frames included (measured shape:
    `Fix_CaveInsNoDisasters`' wrapper sits in the `info` local the engine's
    periodic-repeat loop keeps live across the yielding UndergroundMarsquake
    FUNC — ~1 in 9 Underground-map saves, inert because layer-2-shaped); or
    (c) stored in persisted state — the instance-closure experiment above IS
    this route and remains true. Class tables, presets, `OnMsg` registrations
    and UI windows are safe (permanents / rebuilt / not persisted).
    Full evidence: `docs/reports/F86_ADJUDICATION.md` §3.1/§5.1.
  * ~~A proper Lua tail call (`return orig(...)`) removes our frame from the
    stack — (believed, not yet measured).~~ ⚠️ **CANCELLED as unfalsifiable
    (F86 adjudication + owner, 2026-07-31): do not measure this and do not
    rely on it.** A tail call has nothing after it, so a vanished frame and a
    surviving frame produce identical silence — no experiment exists, and
    adding a detector after the call stops it being a tail call. FIX_POLICY
    §3a's layer 2 was restated to need no engine guarantee: *no mod code
    after a call that can block*, checkable by reading source.
  * Real-time threads are unaffected — they are not persisted at all.
  * Evidence, harm and the exposure list (**13** after two same-day membership
    corrections): **BUGS.md F86**.
  * ⚠️ The disproven by-name persistence belief still sits in TWO shipped file
    headers — `Fix_MeteorFrequency.lua:53` and `Fix_RainsDeadlock.lua:52`
    (named here 2026-08-01 so nobody inherits them as facts). Both bodies are
    deleted by the F86 Tier-1 rewrite (project chain prompt 4), which retires
    the comments with them; do not cite either header in the meantime.

- **MODS *DO* GET A PRE-SAVE HOOK — `OnMsg.SaveGameStart` and
  `OnMsg.SaveGameDone` reach mod code** (measured 2026-07-31 with a Test Kit
  probe, alongside `OnMsg.LoadGame` as a positive control). **This corrects an
  earlier recorded "fact" that mods have no save hook and that tidying up on
  save is therefore impossible — it is possible.**
  * `ModMsgBlacklist` (`CommonLua/Classes/Mod.lua:1430-1440`) blocks only
    `PersistGatherPermanents`, `PersistLoad`, `PersistSave`,
    `ModBlacklistPrefixes`, `ModBlacklistGather`, `DebugDownloadExternalMods`,
    `DebugCopyExternalMods`, `PasswordChanged`,
    `UnableToUnlockAchievementReasons`. `SaveGameStart` is not among them.
  * `DoSaveGame` (`CommonLua/Savegame.lua:1037-1063`) fires
    `Msg("SaveGameStart", params)` **before** the write and
    `Msg("SaveGameDone", name, autosave, err, metadata)` after. Observed
    `SavingGame=true` inside the handler.
  * **Autosaves are the same path**: `SaveAutosaveGame` (`:1450-1453`) just sets
    `params.autosave = true` and calls `DoSaveGame`. So the hook covers them —
    and so does the leak. The `autosave` flag is visible to the handler
    (a manual save logged `autosave=nil`).
    ⬆️ **This bullet was SOURCE-ONLY when written; it is now MEASURED
    (2026-08-01, F86 Phase 0 §0.2 — `autosave=true err=false` observed twice).
    See the dedicated entry below; the source reading was correct.**
  * ⚠️ Consequence for any tear-down design: autosaves fire ~once a sol, so a
    handler that *restarts* a long-interval loop would reset its timer forever.
    Re-arm from a persisted deadline instead.

- **ENABLING A MOD AT THE MAIN MENU IS A DIFFERENT LOAD ORDER FROM A COLD BOOT,
  AND IT IS THE ONE EVERY PLAYER GETS FIRST** (measured 2026-07-31, F87; source
  traced the same day). A mod is never auto-enabled, so the first time our code
  ever runs it runs on this path, not the one every A/B leg measures.
  * Ticking the box calls `ModsReloadItems` (`Mod.lua:2073`), which calls
    `ReloadLua()` (`:2145`) because our mod has code. `ReloadLua`
    (`lib.lua:353-374`) does `dofile("CommonLua/Core/autorun.lua")` — mod code
    loads at `autorun.lua:423` — then `Msg("Autorun")`, which is where classes
    are built (`classes.lua:980`). Then `ContinueModsReloadItems` loads the mod
    items and fires `Msg("ModsReloaded")` (`:2193`).
  * **`LoadData` is NOT part of that sequence, so `DataLoaded` never fires
    again.** The presets are already loaded from the original boot and survive
    the Lua reload. **A fix hung off `OnMsg.DataLoaded` alone is silently dead
    for that entire session** — three of ours were (F87 sweep).
  * **The engine's `DataLoaded` GLOBAL is the only evidence available**: it is
    declared under `if FirstLoad` (`Dlc.lua:51`) and set true at `:663`, so it
    survives a Lua reload where the message does not. ⚠️ It is set **after**
    `Msg("DataLoaded")` is posted (`:661` then `:663`), so inside a `DataLoaded`
    handler the global still reads false.
  * **`ClassesBuilt` (`classes.lua:1099`) DOES fire on both paths** and is the
    enable path's real trigger — and on a cold boot it fires *before*
    `DataLoaded`, so a handler there sees classes built and presets missing.
    `MsgClear` runs immediately after (`:1100`), so the handler must be
    registered at file scope — which is where our code already runs.
  * So the state at apply() time is **not** "nothing is loaded": on this path it
    is **presets loaded, classes NOT flattened** — the exact combination that
    made `HasTrait:new` throw in `Fix_DustSicknessBiorobots` (F87).
  * `g_Classes` is **not** a usable "are classes built" test: during a reload it
    still holds the PREVIOUS build's classes while the current ones are bare
    classdefs. The only truth is that your own `ClassesBuilt` handler has fired.
  * Mod options are loaded BEFORE code on this path too (`Mod.lua:2129-2131`),
    so `CurrentModOptions` is readable at apply() time exactly as on a cold boot.

- **`Msg` dispatches static handlers through `procall`** (`cthreads.lua:15-31`),
  so one handler throwing cannot break the others — and a throw inside a mod's
  `OnMsg` handler is **swallowed**. Consequence for this pack: a fix whose work
  happens in a message handler must `pcall` its own body and report the failure,
  or it will go on reporting `active` while having silently done nothing.

- **THE BY-VALUE THREAD SERIALISATION IS DOCUMENTED, INTENTIONAL ENGINE
  DESIGN** — primary source found 2026-07-31 (prior-art survey): the original
  game's own modding docs, `Surviving Mars\ModTools\Docs\LuaSavegame.md.html`:
  *"Any Lua threads sleeping when a savegame is triggered will be serialized …
  including any local variables anywhere in the call stack, any upvalues, and
  even the bytecode of the functions themselves, to allow loading the savegame
  even when a game update has changed the Lua code. This means that after
  loading, pieces of 'old' Lua code … will be running. New invocations of
  these functions, however, will use their new versions."* So F86's mechanism
  is designed update-tolerance that mods inherit; the last sentence is the
  official statement of the command-thread self-cleaning rule and the upgrade
  model. ⚠️ The REMASTER's ModTools docs no longer carry this page.
  Community norms built on it: `docs/reports/PRIOR_ART_SURVEY.md`.
- **THE SAVE/LOAD HOOK SURFACE — enumerated 2026-07-31 (F86 round 2), so no
  design discovers hooks one at a time again.** `ModMsgBlacklist` is exactly
  nine names (`Mod.lua:1430-1440`: PersistGatherPermanents, PersistLoad,
  PersistSave, ModBlacklistPrefixes, ModBlacklistGather,
  DebugDownloadExternalMods, DebugCopyExternalMods, PasswordChanged,
  UnableToUnlockAchievementReasons); **everything else reaches mods.** The
  save/load lifecycle:
  * **Save:** `CanSaveGameQuery(query, request)` (`Savegame.lua:94` — any entry
    a handler puts in `query` **blocks the save**; vanilla uses it,
    `Lua/Savegame.lua:54`; ⛔ **barred for this pack** — a stuck veto is a
    can't-save bug, invisible on console, worse than F86) →
    `SaveGameStart(params)` (`:1043`, MEASURED) → write →
    `SavegameSaved` (`:1085`) → `SaveGameDone(name, autosave, err, metadata)`
    (`:1061`, MEASURED). Autosaves additionally bracket with
    `AutosaveStart`/`AutosaveEnd` (`:1502`/`:1544`) — observing autosaves needs
    neither `params.autosave` nor the shared path.
  * **Load, in order:** `UnpersistStart` → `PreLoadGame(metadata)`
    (`Savegame.lua:802-804`) → `PersistPreLoad` → `PersistLoad`⛔ →
    **`PersistPostLoad(data)`** (`persist.lua:106-113`) → `LoadGame(metadata,
    version, params)` → `PostLoadGame(metadata, version)` → `UnpersistEnd(err)`
    (`Savegame.lua:810-816`).
  * **`PersistPostLoad` is NOT blacklisted and receives `data`** — a mod can
    read what the save carried (`data["Meteors"]`, …) before deciding to heal;
    it fires earlier than `LoadGame`, but mod handlers run after the engine's
    (registration order), so vanilla's `data[name]==nil` thread rebuild has
    already happened. Use `LoadGame` unless the heal needs `data`.
- **`CreateGameTimeThread` DEFERS — the body does NOT run before the creating
  statement continues** (MEASURED 2026-08-01, F86 Phase 0 §0.1, owner at the
  keyboard, loaded colony, unpaused; log
  `Mars.exe-20260801-14.59.57-6a22b86d.log`). This was the one fact gating both
  Tier-1 designs (`F86_ADJUDICATION.md` §4.1) and it could not be read from
  source: `CreateGameTimeThread` is a C export with no Lua body (the only
  definition in the tree is the empty stub
  `ModTools/Src/CommonLua/LuaExportedDocs/Global/thread.lua:6`).
  * **Form 1 — creator = console context.** `CreateGameTimeThread(function()
    ModLog("…thread body ran") end) ModLog("…statement after create ran")` logged
    `statement after create ran` **then** `thread body ran` (both at
    `Lua 0:01:43:086`).
  * **Form 2 — creator = a GAME-TIME thread, i.e. the shape that actually
    matters** (vanilla's `RainsDisasterLoop` creates its activation thread from a
    GT thread, `TerraformingDisasters.lua:310-316`). An outer GT thread created an
    inner GT thread that posts `Msg`, then the outer `WaitMsg`'d for it with a
    5000 ms timeout. Result at `Lua 0:04:29:476`: `outer past create, about to
    WaitMsg` → `inner ran, posting` → **`outer GOT the message`**. Form 2's
    verdict does not depend on log line order at all — receipt vs timeout is the
    discriminator. Form 1 was NOT generalised to Form 2 by inference; both were
    run.
  * **Consequences.** (a) The authorised rains repair works **as written** — a
    wrapper on `RainsDisasterActivation` that posts `RainDisasterEnd` on the
    collision early-return reaches a vanilla loop that is already in `WaitMsg`;
    the synchronous-heal fallback is NOT required. (b) `RestartGlobalGameTimeThread`
    (`_fixup.lua:21`) assigns `_G.Meteors` after the create returns, and under
    deferral the persisted body cannot make its first `GetDisasterWarningTime`
    call before that assignment — so the `CurrentThread()` key never misses on
    the first iteration. The F02 wrapper's defer-when-`rawget(_G,"Meteors")`-falsy
    guard is therefore **not load-bearing, and stays anyway as defence in depth**.
  * ⚠️ Scope of the claim: this measures the **create call**, not scheduling
    latency. In both forms the body ran within the same log-timestamp group, so
    deferral here means "next scheduler opportunity", not "much later".
- **THE PRE-SAVE HOOK COVERS AUTOSAVES — `SaveGameStart`/`SaveGameDone` fire on
  the autosave path with `autosave=true`** (MEASURED 2026-08-01, F86 Phase 0
  §0.2, same log `Mars.exe-20260801-14.59.57-6a22b86d.log`; closes
  `F86_ADJUDICATION.md` §4.2, which had this source-verified but never observed).
  Probe `97_SaveHookProbe.lua` (now torn down), positive control `LoadGame FIRED`
  present in the same log. Two autosaves observed, both clean:
  `SaveGameStart FIRED — params=table: … SavingGame=true` then
  `SaveGameDone FIRED — name=Autosave Sol 285.savegame.sav autosave=true
  err=false` (`Lua 0:02:29:324`/`0:02:30:011`, and a duplicate pair at
  `0:02:37:203`/`0:02:37:846`).
  * **How it was triggered, stated exactly:** both were forced from the console
    with `CreateRealTimeThread(Autosave)`, not left to fire on their own. That is
    the engine's own invocation, byte-for-byte — the periodic autosave thread
    does literally `CreateRealTimeThread(Autosave)` (`Savegame.lua:1550-1555`),
    and `Autosave` → `SaveAutosaveGame` (`:1450-1453`, sets `params.autosave =
    true`) → `DoSaveGame`. The trigger differs; nothing downstream of it does.
    `CanAutosave()` (`:1466-1477`) gates only *whether* the periodic thread fires,
    not what the path then does.
- **`IsValidThread` returns NO VALUE for an invalid thread — not `false`**
  (bit us twice 2026-07-31: a console read shows a blank line easy to misread,
  and `tostring(IsValidThread(x))` throws `bad argument #1 to 'tostring'`).
  Safe form: `IsValidThread(x) or false`.
- **`Wakeup(thread)` only wakes a thread sleeping in `WaitWakeup`** — not one in
  `Sleep` (`CommonLua/LuaExportedDocs/Global/thread.lua:62-71`). There is no way
  to shorten a `Sleep` already in flight; compressing the interval constant only
  affects the *next* roll. Cost one wasted step in PT-20 before the doc settled it.
- **TOOLING: never round-trip a doc through PowerShell 5.1 `Get-Content -Raw` +
  `WriteAllText`.** `Get-Content` without `-Encoding` decodes UTF-8 files as cp1252, so
  every `—`, `↔`, `≤` comes back double-encoded and the whole file shows as changed.
  It happened to `BUGS.md` in the wave-4 session and was reversed with
  `Encoding.GetEncoding(1252).GetBytes(UTF8.GetString(bytes))`; nothing was committed
  corrupted. Use the editor's own file tools for docs, or pass `-Encoding UTF8` on
  BOTH ends.
