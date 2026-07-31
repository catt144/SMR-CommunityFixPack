# General continuation prompt (model-agnostic) — rewritten 2026-07-31 late

Paste everything below into a fresh Claude Code session — **any Claude model;
the user picks per task and everything here works identically on either.**
**Start with `git log --oneline -10` + `git pull`** — this file goes stale the
moment another session commits. (The filename keeps its historical `FABLE_`
prefix so existing references stay valid; nothing in it is model-specific.)

Staleness check: this was written at **`e07cece`** (the F87 repair leg).

> 🛑 **READ FIRST — PT-20 FAILED AND WE HAVE A P1 DEFECT OF OUR OWN. `BUGS.md`
> F86, and it BLOCKS RELEASE.** Measured 2026-07-31: **pack code is written into
> the player's savegame and keeps running after the mod is removed.** A save
> captures every game-time thread **with its blocked stack**; a mod function
> there is serialised by value and returns with an empty `_ENV`.
> - Proven at two sites: **`Fix_MeteorFrequency`** — the colony's meteors stop
>   **permanently** and do not self-heal — and **`Opt_DroneOverhaul`** (98
>   errors/session, log-only harm) which leaked **with its own toggle OFF**.
> - **The test is NOT "where is the function stored".** It is *can it be blocked
>   below a `Sleep`/`WaitMsg`/`WaitWakeup` on a **game-time** thread when the save
>   is written*. Synchronous code can never be captured, so ~62 of 74 modules are
>   safe by construction; **12 are exposed** (list on the F86 entry).
> - The 2026-07-31 audit's "class tables are safe" clearance is **void** —
>   `Drone.Idle` is a class-table write and leaked anyway.
> - **Nothing is built.** The three-layer redesign lives in
>   **`docs\SAVE_SAFETY_REDESIGN.md`** — per-module disposition for all 12, the
>   autosave timer trap, and the four decisions owed. It is an **owner decision**;
>   do not build against it unquoted.

> **Same leg, two corrections to recorded "facts" — both were believed and both
> were wrong:**
> - **MODS *DO* GET A PRE-SAVE HOOK.** `OnMsg.SaveGameStart` / `SaveGameDone`
>   reach mod code (measured, with `OnMsg.LoadGame` as a positive control); only
>   `PersistSave`, `PersistLoad`, `PersistGatherPermanents` are blacklisted
>   (`Mod.lua:1430-1440`). The "tidying up on save is unimplementable" claim is
>   dead, and the D06 cleanup-mod argument resting on it is corrected in place.
>   Autosaves are the same path (one flag) — so the hook covers them, and so does
>   the leak.
> - **`debug.getinfo` and `Wakeup` are both dead ends** — the first is absent in
>   the sandbox (already in ENGINE_FACTS:69, and it is why `[install]` probes
>   SKIP); the second wakes only `WaitWakeup` sleepers, never a `Sleep`. Both were
>   proposed and killed by controls during PT-20. Do not re-derive them.

> ✅ **F87 IS FIXED (2026-07-31 late) — ONE THING IS OWED AND IT NEEDS YOU FOR ONE
> CLICK.** The repair went into the shared `SMRFixPack.DataPatch` scaffold, not
> the one file: nothing runs before `ClassesBuilt`, the enable path gets its own
> triggers, and the pass is `pcall`ed (a throw in a msg handler is swallowed by
> `procall`, so the fix would have reported `active` while doing nothing).
> - **The sweep it earned found THREE MORE modules silently dead on the enable
>   path** — `Fix_TechDescriptionBuilding`, `Opt_MultipleSuns`,
>   `Fix_FirstAsteroidPrefabs` — all repaired via the new
>   `SMRFixPack.OnDataReady`. The blast radius was four modules, not one.
> - Rule written (**FIX_POLICY §2**: no `apply()` may assume a cold boot) and the
>   load-order sequence traced into **ENGINE_FACTS**.
> - **Both legs ran and both are CLEAR.** Cold boot 18.44 (`68/74` →
>   `63/0/15/0`) and — for the first time in this project — **the ENABLE PATH
>   itself, 19.09, owner ticking the box at the main menu: `68/74` →
>   `63/0/15/0`**, probe-for-probe identical bar two RNG lines, with
>   `DustSicknessBiorobots` PASSing on live preset data. The leg logs its own
>   positive control (`ARMED — the pack is OFF` → `ENABLE DETECTED`).
> - ⚠️ **ONE GAP LEFT: audit A2.** That run had the six toggles OFF, so all five
>   `Opt_` probes SKIPped and A2's three flattening-unsafe `Opt_` hooks are
>   **still unverified on the enable path**. **Owed: the same leg with the
>   toggles ON** (TestKit `Code/98_EnablePathLeg.lua`, recipe in
>   `PLAYTEST_HELP.md`; the click cannot be automated —
>   `AccountStorage`/`SaveAccountStorage`/`ModsReloadItems` are all
>   sandbox-blacklisted and there is no main-menu console).

> 🚧 **THERE ARE NOW TWO PROMPTS, AND THIS ONE DOES NOT DRIVE DRONE WORK.**
> The drone project grew its own open design decision, its own frozen tests, and
> constraints that do not generalise — sharing a prompt was making both worse. It
> now lives in **`docs\DRONE_PROJECT_PROMPT.md`** (re-runnable), which owns D06,
> D08, D09, F77, the drone queue machinery, the consolidated drone playtest, and
> the cleanup mod.
> - **You MAY answer drone questions in passing**, from the `BUGS.md` D06 entry
>   and `docs\DRONE_PRIORITY_SYSTEM.md`.
> - **You may NOT start drone work, plan it, schedule it, or list it as owed
>   here.** If a session turns into drone work, **stop and load the drone prompt
>   instead.**
> - Drone state appears below **as context only, never as a task.**

---

## Where the project stands

> 🚁 **DRONE CONTEXT ONLY — the work belongs to `docs\DRONE_PROJECT_PROMPT.md`.**
> All four research gates were answered 2026-07-31 (Q1 **honoured** — bands 4-5
> are visible to the C matcher and consumed on both the repair and haul legs; Q2
> hub queues **persist**; Q3 both data tests settled; Q4 defaults omitted from
> saves). **An open design decision follows from it and is NOT owed here** — the
> band scheme passed but picked up two constraints that did not exist when it was
> drafted (uninstall lossiness with an expiring heal path, and a duplicate leak
> that bites with the mod installed). Detail: `BUGS.md` D06 entry and
> `docs\DRONE_PRIORITY_SYSTEM.md` §8-§10. **Answer questions from those; start
> nothing.**
>
> ⛔ **PT-52 A/B/B2 remain FROZEN** — they test D06 v1's design and the design is
> unsettled. **PT-10 is explicitly NOT frozen** (F55, different subject).

> 🆕 **THE ENGINE FACT THAT STARTED IT — now superseded in scope by F86 above.**
> A mod-authored closure on a persisted game object goes into the savegame,
> survives removal and keeps running. **PT-20 proved the hazard is wider than
> "instances":** the route is a persisted **thread stack**, so class-table writes
> and `GlobalGameTimeThreadFuncs` replacements leak too. UI windows (XWindows)
> remain genuinely safe — they are not savegame-persisted. Read the corrected
> ENGINE_FACTS entries before writing any fix.
>
> **Still true and still load-bearing:** no mod can run after its own removal, so
> residue already inside a player's save is unreachable by the pack. *(The
> cleanup-mod proposal is drone-owned — see the drone prompt. Not approved to
> build, and its "no save hook" justification has been corrected.)*

> 🧭 **UNDECIDED, deliberately — a possible PACK SPLIT** (true fixes + a companion
> mod holding the opt-ins). **Not owed, not scheduled, and it may not gate
> anything.** The owner's reason for not deciding is itself on the record in
> `STATUS.md`: one mod is one configuration matrix, and every measurement we hold
> is calibrated to it. Impacts (harness counts, the `OptionsMenu` probe's eight
> assertions, D05's options surface, its composition with the cleanup mod, and
> that it is cheap before beta and expensive after) are recorded there too.

> ⛔ **SCOPE CONTROL IS A STANDING RULE — `docs\FUTURE_IDEAS.md`.** Ideas not
> needed before launch are PARKED. **Nothing in that file is work**: not owed,
> not scheduled, not counted, never reported as outstanding. Reason on record:
> every three items closed were adding about six. **Defects never go there** —
> they stay in BUGS.md with a real status; declining one is a `wontfix` with
> reasoning.

> 📋 **Todo lists: ONE ITEM PER COMMIT-AND-VERIFY UNIT** (`WORKFLOW.md`). The
> owner reads that list to time when to step in. A list coarser than the work
> gives a confident wrong answer.

## Build state

**74 registered modules — 68 active by default**, 6 opt-in via Options → Mod
Options (D05, `tested`), plus the D09 stat-dials module (`Opt_DroneStatDials`,
active-at-base = vanilla, `tested`). `Code/` = 75 files. **TestKit probes: 78.**
Pinned game build **1.0.7.396349** (fpk parity proven, ENGINE_FACTS). Everything
committed and pushed.

**The cold-boot code gate is clear** — current legs at 78 probes: all-toggles-ON
`74/74` → **68/0/10/0** (12.30.34); default config `68/74` → **63/0/15/0**
(12.44.39, dials at base); baseline **1/62/15/0** (12.32.11).

> ⚠️ **"Nothing is owed on the harness side" is NO LONGER TRUE (2026-07-31).**
> Every one of those legs launches the game with the pack **already enabled**, so
> they measure the *second session onward*. **The session in which a player turns
> the mod on has still never been measured** — F87 lived there. The leg that
> measures it is now **built and unrun**: it is board item 0, it needs one click
> at the main menu, and it also verifies audit finding A2's three `Opt_` modules,
> whose "a first mid-session enable works" remediation has never been checked end
> to end. A **post-F87-repair cold-boot re-verify DID run** (18.44, `68/74` →
> `63/0/15/0`) and is clear — it proves no regression, nothing more.

**Account state — READ IT, NEVER ASSUME IT.** The 2026-07-31 13.18 log showed all
six opt-in modules reporting `inactive (opt-in …)`, i.e. **all six toggles OFF**.
But treat that as a reading with a timestamp: this sentence went stale twice on
2026-07-30 alone. **Read the leg's own `fix pack present: N/74 fixes active`
line** to learn which configuration you actually measured, and read the toggles
with `SMRFixPack.ListFixes()` or `SMRFixPack.fixes.<Id>.status`. The dials are
account-persistent too.

## ▶️ Next session — the board, user picks

> ⚠️ **Item 0 needs the owner at the keyboard for one click and takes ~5 minutes;
> 0b blocks release.** Items 1-2 are BUILDS — writing new fixes before the
> save-safety rules are settled risks adding leak sites, and both D10 and D12
> touch colonist assignment, which is command-thread territory. Confirm the
> owner's intent before starting any build.

0. **▶️ RE-RUN THE ENABLE-PATH LEG WITH THE SIX TOGGLES ON — the last thing F87
   owes, and the only way to close audit A2.** The leg itself is built, executed
   once (PASS) and disarmed at rest; the 19.09 run had the toggles OFF, so the
   five `Opt_` probes SKIPped and A2's three flattening-unsafe `Opt_` hooks were
   never exercised on that path. Recipe: `PLAYTEST_HELP.md` → "The ENABLE-PATH
   leg". In short: **turn the six Mod Options toggles ON in an earlier session**
   (account state carries them in), then uncomment
   `"Code/98_EnablePathLeg.lua"` in the **TestKit** metadata `code` list, make
   sure the **fix pack is DISABLED** in the Mod Manager, launch, and at the main
   menu tick "Community Fix Pack" and close the dialog. Re-comment to disarm.
   - **Expect** the all-toggles-ON numbers on the enable path — `74/74` →
     `68/0/10/0` if it matches the cold boot. Read the
     `fix pack present: N/74` line first, always.
   - A FAIL here is a real first-run defect: `FixMissing` FAILs any probe whose
     fix is not `active`, and the data-patch probes read live preset data.
   - **Still undone and deliberately so:** the C1 `error`-vs-`inactive` wording
     split on the F87 entry. It is a FALLBACK — the owner's direction was to
     solve the bug so no player message is needed, and that is what landed. Ask
     before building it.
0b. **🛑 F86 — the save-safety redesign.** Owner decision owed on the three
   layers (input-patching, the tail-call rule, `SaveGameStart` tear-down). Two
   cheap measurements are owed first and both are quick: **(a)** does
   `Fix_ShelterReflex` stay off the stack via its proper tail call — if yes, the
   whole wrapper class collapses into a coding rule; **(b)** does reinstalling
   the pack heal a damaged save (our `LoadGame` restarts the thread), which
   decides what we tell an affected player.
1. **⭐ D10 — workshops module BUILD.** Speced, user-approved, game-free, un-gated
   (PT-56 passed). Full spec on the D10 BUGS entry: T1 text repairs + T2 capacity
   dial (base/+50%/+100%, `max_workers` AND `consumption_amount` **PAIRED**).
   Adds PT-57 (~7 min) at build time. **This is the ready-to-go build item.**
2. **D12 — no-homeless dome policy.** DECIDED and speced, build owed. Its own
   module; `Opt_ResidencyControl` as donor pattern ONLY. **Hard constraint:** the
   new flag must NOT route through `CanAcceptNewColonists` (D03's gate) or it
   blocks the cohort delivery it exists to protect. Never expel to the surface.
   **Sequencing: D10 and D12 both touch colonist assignment — land them
   separately, each with its own A/B, never entangled.**
3. ~~**PT-20**~~ — **RUN 2026-07-31: steps 1-4 PASS, step 5 FAIL → F86.** Its
   remaining work is item 0. **F74 and F53(a) are NO LONGER bundled with it** —
   a pack-lineage save is not a vanilla control, so they need a colony that has
   never had the pack installed (a fresh 10-minute save covers both).
4. **PT-53 Trigger E** — the last thing between D07 and `tested`.
5. **PT-54** — wave-6 disaster fixes. ⚠️ **The "live 194-sol save" named here is
   GONE** (owner, 2026-07-31). The current long-running fixtures are `test 2i`
   (288 sols) and `test 2e`-`2h` (~150-250 sols); `PT-20TEST`/`PT-20TEST-B` are
   the F86 evidence saves and should not be played on.
6. **Checklist §6 needs-eyes riders** — cheap single observations; the genuinely
   new ones are **F34(d)**, **F74**, **F06** and F11's console read.
7. **PT-10, PT-15, PT-18, PT-25, PT-27/28/30, PT-35, PT-42, PT-44, PT-47**, then
   **PT-21/22** last.

**Decisions owed (user):** the **FIX_POLICY §4
amendment** (drafted at the end of `REACHABILITY_AUDIT.md` — resolve its R4
contradiction with F49(a) first; three options are on the F49 entry); **D08** and
**D06-structural** (UNDECIDED, a third state — and drone-owned, see the drone
prompt); **D11** (feasibility is on the
entry but it is NOT approved — ask fresh; multi-hop passenger routing is
REJECTED). ~~F79~~ is CLOSED `wontfix` — do not re-propose or park it.
**F85 stays observation-gated — do not build it.**

**Release-time owner tasks** (audit plan 2.5): preview image (PDX ≤2 MB / Steam
≤1 MB), screenshots, Paradox portal console-publishing rules.

**🚦 `docs\BETA_READINESS_REVIEW.md` is re-runnable** — derives every fact at run
time, hard gates that cannot be judgement-softened. **Do NOT run it until the
drone design decision has settled.**

---

You are continuing the Surviving Mars: Relaunched "Community Fix Pack". Sessions
are usually **LIVE PLAYTEST STANDBY**: the user is at the keyboard in the retail
game with both mods loaded, and you assist in real time. Your jobs:

1. **Set tests up** — walk the user through the checklist's own steps
   (`PLAYTEST_CHECKLIST.md`) using the verified command table
   (`PLAYTEST_HELP.md`); hand them exact console lines to paste, **one command
   per line** (see the console facts below — a pasted multi-line block silently
   concatenates and fails with `not understood`).
2. **Process results as they arrive** — protocol at the bottom of
   `PLAYTEST_CHECKLIST.md`: PASS → flip status in BOTH BUGS.md places (index row
   + heading tag) and move the section to `PLAYTEST_ARCHIVE.md`; FAIL → diagnose
   live, file the finding with the full forensic trail.
3. **Diagnose surprises** — new defects get an F-number, an entry and a severity
   call. Mechanical repairs may land same-day WITH a re-verified A/B; redesigns
   go to the user.
4. **Commit as you go** — every processed result or finding is a commit, pushed.
   Docs never lag play.

**⚠️ A PT's own procedure is unverified until it has been executed once.** This
cost a leg *again* on 2026-07-31: PT-59 never said which of two popups to answer,
and the wrong one produced a result indistinguishable from a fix failure — which
was reported as a FAIL before source settled it. For any "nothing should happen"
test, insist on a **positive control** and an **objective counter**.

## First, read (in order) from `C:\Dev\SMR-BugFixPack`

1. **`docs\ENGINE_FACTS.md` — the whole file.** Several behaviours are the
   opposite of what the code suggests, and it now carries the
   closure-persistence fact. Then `docs\STATUS.md` (compact current state).
   Session legs are in `docs\archive\SESSION_LOG.md`, newest first.
2. `docs\PLAYTEST_CHECKLIST.md` — tests + the reporting protocol only. §1
   standing watches, §2 owed halves, §3 wave-6 + PT-59 (now archived), §4
   fixture sittings, §5 cross-cutting (PT-20/21), §6 the needs-eyes list. **All
   reference material — ground rules, external-validity rule, cheat discipline,
   console facts, the verified command table, Test Kit helpers, save-fixture
   recipes — lives in `docs\PLAYTEST_HELP.md`.** Read its ground rules before
   handing the user any console line.
3. `docs\BUGS.md` — the entries the sitting touches. **F76 before ANY depot-picker
   interaction.** For drone anomalies, the DroneControl bullet in "Not yet swept"
   carries the assignment-machinery trace and the R1-R7 paste-ready forensics.
4. `docs\FIX_POLICY.md` — binding for any code you write. **§4a is the owner hard
   rule (below); §4 has a drafted replacement awaiting the owner.**
5. **`docs\REACHABILITY_AUDIT.md` — the "Challenge review 2026-07-30" at the end,
   before writing ANY new fix.** Tier vocabulary (R1/R2/R3/R4/U + `I`), the hard
   tells that distinguish a defect from designed behaviour, and two standing
   rules: *a state producible only by console/debug injection is evidence
   AGAINST reachability*, and *re-read `git log` between assembling conclusions
   and publishing them*.
6. **Drones: do NOT read in to start work — load `docs\DRONE_PROJECT_PROMPT.md`
   instead.** To answer a passing question only, the sources are the `BUGS.md`
   D06 entry and `docs\DRONE_PRIORITY_SYSTEM.md` (§8-§10 are the new, decisive
   ones).
7. **`docs\FUTURE_IDEAS.md` — the hard rule at the top, before planning ANY
   session.** A proposed-parking list at the bottom awaits the owner's yes/no.
8. Only when relevant: `docs\archive\AUDIT_FINDINGS.md` (ARCHIVED — Phases 1-3
   done 2026-07-29, Phase 4 EXECUTED 2026-07-31); `docs\DRONE_OVERHAUL_OPTIONS.md`.

Game source (read-only, NEVER modify):
`A:\SteamLibrary\steamapps\common\Project Spark\ModTools\Src`.
Both mods load through junctions from `C:\Dev\SMR-BugFixPack` and
`C:\Dev\SMR-BugFixPack-TestKit`. **Check `Mars.exe` is NOT running BEFORE
touching loadable code** (`tasklist`) — and check it *before*, not in the same
command as the edit (that slip happened 2026-07-31; no harm, wrong order).

> ⛔ **READ BEFORE WRITING ANY FIX — FIX_POLICY §4a, owner hard rule: this pack
> NEVER fixes other mods' problems.** Not bugs caused by another mod, and not
> vanilla bugs reachable only from mod code. **"For modder benefit" is not a
> valid reason to ship anything.** The test is **who benefits**: could a PLAYER
> be harmed, now or after a future patch/DLC? Yes → real fix, ship it (invisible
> and latent are irrelevant). Only-a-mod-benefits → barred. Operationally the
> **R4/R3 boundary**: R4 needs new *calling code* (barred), R3 needs new *data*
> (allowed). Override is an explicit per-case ask to the owner, never inferred,
> never carried to a second case. **Judge by enumeration, never by an entry's own
> words** — F29 called itself "mod-facing / No shipped user" and had four live
> shipped callers.

## F76 — READ BEFORE THE USER TOUCHES AN RC TRANSPORT **OR DOZER** (vanilla P1, unfixed)

The resource picker (`ResourceItems`) renders far from the cursor and cannot be
clicked on the user's 4K/80%-scale setup — and interacting with it can **HARD-LOCK
the UI (Alt-F4, session lost)**. **Surface: ANY vehicle whose click-load reaches a
storage-depot-class object** — RC Transport depot LOAD, multi-type UNLOAD, route
resource choice, and the RC Terraformer clicking a waste-rock heap.
- **Avoid the picker paths entirely.** Loose ground/rubble piles are safe; route-mode
  loading works for single-resource depots (`RCTransport.lua:466-476`).
- **Verified workaround** (transports AND dozer):
  `rc:SetCommand("TransferResources", depot, "load", "<Resource>", <amount*1000>, true)`
- **NO live UI-internals prototyping in a play session** — hard rule since the lock-up.
  The F76 repair is a separate attended, game-free sitting.

## Live-session console facts (hard-won — do not re-derive)

- **Hand the user ONE command per line.** The console input is a SINGLE line; a
  pasted multi-line block silently concatenates and fails `not understood`
  (proven again 2026-07-31 — two lines arrived as `… endSMRFixPack_…`).
- **`not understood` = the console could not COMPILE the line** (`console.lua:24`).
  Overwhelmingly a `--` comment inside a `*r`/`*g` snippet: those splice your code
  into `CreateRealTimeThread(function() %s end) return` **on one line**
  (`uiConsole.lua:360-361`), so the comment eats the closing `end) return`.
  **Never write a console snippet with a trailing comment or a `--> value` note.**
- For a simple read prefer a **bare expression** — rule
  `{ "(.*)", "ConsolePrint(print_format(%s))" }` (`uiConsole.lua:363`) wraps
  anything that compiles as an expression. Reserve `*r`/`*g` for multi-statement
  snippets and for **assignments** (an assignment is not an expression).
- **`SMRFixPack.ListFixes()` prints to the LOG, not the console overlay.** Read it
  via `FlushLogFile()` + the newest log, or use the on-screen variant:
  `*r for _, id in ipairs(SMRFixPack.order) do local f = SMRFixPack.fixes[id] ConsolePrint(id .. " [" .. f.status .. "]") end`
- The log buffer only flushes at exit — **`FlushLogFile()`** forces it mid-session.
  **`ModLog(...)` is the ONLY path proven to reach the log file**; `print` and bare
  expressions are on-screen only.
- **Runtime console wrappers must target the LEAF class** — a runtime patch on a
  base class is invisible to already-built subclasses.
- Console opens via Enter / Alt-Shift-C / Ctrl-Alt-C (TestKit auto-opens it
  in-colony; there is NO main-menu console).
- Infopanel cheat buttons need `Platform.cheats = true` AND ride the game-time
  sync queue (dead while paused). Direct `SelectedObj:Cheat*()` bypasses both.
- Speed techs sanctioned for setup: `AdvancedDroneDrive`, `LowGDrive`,
  `MartianAerodynamics`. Hive Mind is NOT a drone tech in Relaunched.
- Cheat use is logged per save and blocks that save's achievements — fixture saves
  only.

## Harness facts (for any A/B pair / same-day repair)

- ✅ **THE ENABLE PATH IS MEASURED NOW — one leg, 2026-07-31 19.09, PASSED.**
  Every *other* leg is a cold boot (launched with the pack already enabled), so
  those `N/74` figures describe the *second session onward*. **A player's first
  session is different**: they tick the mod at the main menu, which triggers an
  in-place mod reload where presets are already loaded and classes are not yet
  flattened. That is where F87 lived. The leg is TestKit
  `Code/98_EnablePathLeg.lua` (recipe in `PLAYTEST_HELP.md`); it needs one human
  click and cannot be fully automated (`AccountStorage` / `SaveAccountStorage` /
  `ModsReloadItems` are all in `ModEnvBlacklist`, and there is no main-menu
  console). ⚠️ **The one run had the toggles OFF, so audit A2 is still open on
  that path — re-running it with the toggles ON is board item 0.**
- Launch: `& "c:\program files (x86)\steam\steam.exe" -applaunch 3215050 -smrautorun`.
  A leg takes ~75 s; Mars.exe may take minutes to appear. **Never kill on a short
  timeout** (25 min no-kill guard; harness watchdog 15 min).
- Arm the TestKit autorun by uncommenting `"Code/96_AutoRunFlag.lua"` in the TestKit
  metadata `code` list; re-comment to disarm (commented at rest).
- Baseline = overwrite fix pack `metadata.lua` with an emptied `code` list — **keep
  the `default_options` block**. **Restore from a saved copy, NOT `git checkout`,
  while uncommitted metadata changes exist. NEVER `git commit -a` while that edit
  is in the working tree.**
- Opt-in leg mechanism: temporary `Code/97_OptInLeg.lua` in the FIX PACK right
  after 00_Core, setting `SMRFixPack_Optional`. Delete after the leg. **The bridge
  is one-way — it can only force a module ON**, and the user's Mod Options toggles
  are account-persistent and apply during legs. **A true default-config leg (68/74)
  requires the user to turn the six toggles off by hand first** — proven five times
  over.
- **Probe-authoring trap:** a probe whose `run` falls off the end returns nil, and
  `SMRTest.Run` turns nil into **SKIP with an empty message** — it looks deliberate.
  Every probe needs an explicit `return "PASS", …`. Re-audited 2026-07-30: clean.
- **TestKit stand-in probe corollary:** WithGlobals stubs cannot reach a game file
  that localizes the global at load time — assert on the MODULE's own action, never
  on vanilla bookkeeping around the stand-ins.
- Synthetic-map noise (all benign): ~50-60 `Flight.lua objects_to_mark` errors, a
  few GameInit nil-call lines, the `[mod] Error in mod … Test Kit` shutdown
  artifact, the MultipleSuns "not found → lifted" transient, and two `ResManager`
  `LawOfficeDoor` missing-animation lines.
- Parse sweep before ANY commit touching Lua: python + luaparser,
  `ast.parse(open(f, encoding='utf-8-sig').read())` over every edited file.
- Docs tooling: never round-trip a doc through PowerShell 5.1 `Get-Content` without
  `-Encoding UTF8` both ends; prefer the editor's file tools. Commit messages via
  `git commit -F <file>`; **no embedded double quotes**.

## Hard rules

`docs/ENGINE_FACTS.md` governs: sandbox on all platforms; `error()`/`assert()`
report-and-continue; self-checks read the DECLARING class; presets only after
DataLoaded (which can fire MORE THAN ONCE); GameVars only inside patched
functions; post-wrappers on command methods never run; `IsValid()` is falsy for
ALL pure-Lua objects; **the shipped build IS Src** (2250/2256 byte-identical —
keep apply-time self-checks anyway, they guard future patches); **a mod closure
on a persisted object enters the save and survives uninstall**; never modify the
game directory; only the playtest flips statuses to `tested`; mechanical repairs
land with a re-verified A/B, redesigns go to the user; **no live UI-internals
prototyping on the user's play sessions**. Commit with
`git -c user.name="SMR-BugFixPack" -c user.email="154917955+catt144@users.noreply.github.com"`,
push the fix pack (TestKit stays local-only).

**End of session:** update STATUS.md and this prompt (rewrite stale blocks — no
banner stacking), commit, push, summarize.
