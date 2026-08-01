# General continuation prompt (model-agnostic) — playtest standby + the F86 sweep, 2026-07-31 late

Paste everything below into a fresh Claude Code session — **any Claude model;
the user picks per task and everything here works identically on either.**
**Start with `git log --oneline -10` + `git pull`** — this file goes stale the
moment another session commits. (The filename keeps its historical `FABLE_`
prefix so existing references stay valid; nothing in it is model-specific.)

Staleness check: written after **`8d201c3`** (F86 owes no measurements), then
updated the same evening with the **four F86 owner decisions** — layer ordering
adopted, sweep authorised, F02 held, D10/D12 sequenced behind the rules.

> ⚖️ **SUPERSEDED FOR F86 (2026-07-31, late evening).** The F86 section below
> predates the adjudication rounds, the prior-art survey, and the evening's
> owner decisions. **If this session is about F86, use
> `docs/F86_NEXT_SESSION_PROMPT.md` (the Phase-0/1 handover) and
> `docs/F86_EXECUTION_PLAN.md` (the plan of record) instead.** Known-stale
> claims below: "comes back with an empty `_ENV`" (wrong — orphans resolve
> vanilla globals; ENGINE_FACTS has the measured correction), "~62 safe by
> construction / 12 exposed" (thread-route only; ≥13 incl. compliant CaveIns),
> "F02 HELD / one game-free item owed" (hold lifted; sweep done; build
> authorised; next owed item is the Phase-0 measurement session). F88 is now
> filed. Playtest-standby guidance below remains valid.

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

**⚠️ A PT's own procedure is unverified until it has been executed once.** Four
tests have now been found unrunnable-as-written by running them (PT-29, PT-11,
PT-25, PT-59). PT-59 cost a leg on 2026-07-31: it never said which of two popups
to answer, and the wrong one produced a result indistinguishable from a fix
failure — reported as a FAIL before source settled it. For any "nothing should
happen" test, insist on a **positive control** and an **objective counter**.

---

## 🛑 The one thing blocking release — F86

**We write executable code into the player's savegame and it keeps running after
the mod is removed** (measured 2026-07-31 by PT-20 step 5; `BUGS.md` F86, P1).
A save captures every game-time thread **with its blocked stack**; a mod function
sitting there is serialised by value and comes back with an empty `_ENV`.

- Proven at two sites: **`Fix_MeteorFrequency`** — the colony's meteors stop
  **permanently** and do not self-heal — and **`Opt_DroneOverhaul`** (98
  errors/session, log-only harm) which leaked **with its own toggle OFF**.
- **The test is NOT "where is the function stored".** It is *can it be blocked
  below a `Sleep`/`WaitMsg`/`WaitWakeup` on a **game-time** thread when the save
  is written*. Synchronous code can never be captured, so ~62 of 74 modules are
  safe by construction; **12 are exposed** (list on the F86 entry — the sweep
  corrected the membership both ways: `Fix_DroneUnreachableForever` IN,
  `Fix_TrainCargoDumping` OUT).
- ✅ **THE DECISION IS TAKEN (2026-07-31) — and exactly ONE game-free item is
  owed: the layer-3 sweep.** All four calls in **`docs\SAVE_SAFETY_REDESIGN.md`**
  §4 are answered:
  1. **Layer ordering 3 → 2 → 1 ADOPTED**, now a hard rule in **`FIX_POLICY.md`
     §3a** — read that, not this summary, before writing any fix. It binds new
     fixes as well as F86 repairs.
  2. **The layer-3 sweep was AUTHORISED at FULL scope** and ✅ **is COMPLETE —
     both halves** (`SAVE_SAFETY_REDESIGN.md` §5). See board item 6. Nothing
     further is owed on it.
  3. ✅ **F02's hold is LIFTED (2026-07-31)** — `Fix_MeteorFrequency` leads the
     authorised build; it is the only site with *measured* permanent harm.
  4. **D10 and D12 stay HELD until these repairs LAND and verify** — the owner
     confirmed the hold means *until built*, not *until the rules were written*.
  ⚠️ When F02 is unheld, the wrapper keys on **`CurrentThread()`**, not the
  meteor descriptor — both `Meteors.lua:279` and the **`MeteorStorm`** thread at
  `:326` pass the same descriptor, so descriptor-keying would fire the storm
  warning ~5 sols early (a balance change, FIX_POLICY §4). Correction is on the
  F86 entry and in the redesign §2.
- ✅ **NOTHING IS OWED BEFORE THE DECISION — the two measurements this block used
  to list are both RESOLVED (2026-07-31, PT-20 leg). Do not re-run them.**
  - **(a) `Fix_ShelterReflex` / the tail-call question — CANCELLED as
    unfalsifiable, and the rule no longer depends on it.** A tail call has
    nothing after it, so a vanished frame and a surviving frame produce
    *identical silence*; adding a detector after the call stops it being a tail
    call. **There is no experiment here — do not design one.** Layer 2 was
    restated to need no engine guarantee: *no mod code after a call that can
    block*, which is true whether or not the frame is serialised, and is
    checkable by reading source. `Opt_DroneOverhaul:188-190` violates it
    (measured leak); `Fix_ShelterReflex:73` complies.
  - **(b) does reinstalling the pack heal a damaged save — YES, measured.**
    `PT-20TEST-B` loaded with the pack back: `IsValidThread(Meteors)` → `true`,
    phase `restarted`, our own `LoadGame` doing it. The answer for an affected
    player is *"put the mod back"* — real, and uncomfortable.
  Those two are still resolved and still must not be re-run. What F86 owes is
  the **sweep**, and nothing else.
- **Three facts to spend nobody's time re-deriving** (all in ENGINE_FACTS):
  **mods DO get a pre-save hook** — `OnMsg.SaveGameStart`/`SaveGameDone` reach
  mod code and autosaves are the same path, so tear-down-on-save is
  implementable; **`debug.getinfo` is absent in the sandbox** and **`Wakeup`
  only wakes a `WaitWakeup` sleeper, never a `Sleep`** — both were proposed
  during PT-20 and killed by controls.
- **Still true and load-bearing:** no mod can run after its own removal, so
  residue already inside a player's save is unreachable by the pack. (The
  cleanup-mod proposal is drone-owned and not approved to build.)

## 🚧 Two prompts — this one does NOT drive drone work

The drone project grew its own open design decision, its own frozen tests and
constraints that do not generalise. It lives in
**`docs\DRONE_PROJECT_PROMPT.md`** (re-runnable), which owns D06, D08, D09, F77,
the drone queue machinery, the consolidated drone playtest and the cleanup mod.

- **You MAY answer drone questions in passing**, from the `BUGS.md` D06 entry and
  `docs\DRONE_PRIORITY_SYSTEM.md` (§8-§10 are the decisive ones).
- **You may NOT start drone work, plan it, schedule it, or list it as owed here.**
  If a session turns into drone work, **stop and load the drone prompt instead.**
- Drone state appears below **as context only, never as a task.**
- ⛔ **PT-52 A/B/B2 remain FROZEN** — they test D06 v1's design and the design is
  unsettled. **PT-10 is explicitly NOT frozen** (F55, different subject).

## Standing rules for planning a session

> ⛔ **SCOPE CONTROL — `docs\FUTURE_IDEAS.md`.** Ideas not needed before launch
> are PARKED. **Nothing in that file is work**: not owed, not scheduled, not
> counted, never reported as outstanding. Reason on record: every three items
> closed were adding about six. **Defects never go there** — they stay in BUGS.md
> with a real status; declining one is a `wontfix` with reasoning.

> 📋 **Todo lists: ONE ITEM PER COMMIT-AND-VERIFY UNIT** (`WORKFLOW.md`). The
> owner reads that list to time when to step in. A list coarser than the work
> gives a confident wrong answer.

> 🧭 **UNDECIDED, deliberately — a possible PACK SPLIT** (true fixes + a companion
> mod holding the opt-ins). **Not owed, not scheduled, and it may not gate
> anything.** The owner's reason for not deciding is on the record in `STATUS.md`:
> one mod is one configuration matrix, and every measurement we hold is
> calibrated to it. Impacts are recorded there too.

---

## Build state

**74 registered modules — 68 active by default**, 6 opt-in via Options → Mod
Options (D05, `tested`), plus the D09 stat-dials module (`Opt_DroneStatDials`,
active-at-base = vanilla, `tested`). `Code/` = 75 files. **TestKit probes: 78.**
Pinned game build **1.0.7.396349** (fpk parity proven, ENGINE_FACTS). Everything
committed and pushed.

**The code gate is clear on BOTH load orders and nothing is owed on the harness
side** (78 probes, all 2026-07-31):

| Leg | Active | Result |
|---|---|---|
| Cold boot, all toggles ON (12.30) | 74/74 | 68 / 0 / 10 / 0 |
| Cold boot, default config (12.44, and again 18.44 post-F87-repair) | 68/74 | 63 / 0 / 15 / 0 |
| Cold boot baseline, `code` list emptied (12.32) | — | 1 / 62 / 15 / 0 |
| **Enable path**, default config (19.09) | 68/74 | 63 / 0 / 15 / 0 |
| **Enable path**, all modules ON via the bridge (19.24) | 74/74 | 68 / 0 / 10 / 0 |

**The enable path is the session a player's FIRST run actually is** — they tick
the mod at the main menu, which triggers an in-place reload where presets are
already loaded and classes are not yet flattened. It was unmeasured until
2026-07-31 and F87 lived there; it now has its own leg (TestKit
`Code/98_EnablePathLeg.lua`, recipe in `PLAYTEST_HELP.md`, disarmed at rest).

**Account state — READ IT, NEVER ASSUME IT.** As of the 19.24 leg: **the fix pack
is ENABLED** (the enable-path leg's own click persists — `ModsUIDialogEnd` calls
`SaveAccountStorage`), **the six opt-in toggles are OFF**, and **both D09 dials
are at base** (the probe reported it on entry). Treat that as a reading with a
timestamp — this sentence went stale twice on 2026-07-30 alone. **Read the leg's
own `fix pack present: N/74 fixes active` line** to learn which configuration you
actually measured, and read the toggles with `SMRFixPack.ListFixes()` or
`SMRFixPack.fixes.<Id>.status`.

## ▶️ The board — user picks

> ⭐ **Item 6 — the F86 save-safety build — is the authorised work right now.**
> Playtests remain available. ⛔ **D10 and D12 stay on HOLD until those repairs
> land and verify**; do not start either and do not re-ask per sitting, the
> answer is recorded.

1. **PT-53 Trigger E** — the last thing between D07 and `tested`.
2. **PT-54** — wave-6 disaster fixes. ⚠️ **The "live 194-sol save" named in the
   test is GONE** (owner, 2026-07-31). Current long-running fixtures are
   `test 2i` (288 sols) and `test 2e`-`2h` (~150-250 sols); `PT-20TEST` /
   `PT-20TEST-B` are the F86 evidence saves and should not be played on.
3. **Checklist §6 needs-eyes riders** — cheap single observations; the genuinely
   new ones are **F34(d)**, **F74**, **F06** and F11's console read.
4. **F74 and F53(a)** — no longer bundled with PT-20: a pack-lineage save is not
   a vanilla control, so they need a colony that has never had the pack installed
   (one fresh 10-minute save covers both).
5. **PT-10, PT-15, PT-18, PT-25, PT-27/28/30, PT-35, PT-42, PT-44, PT-47**, then
   **PT-21/22** last.
6. **⏸️ F86 — BUILD AUTHORISED BUT PAUSED BY THE OWNER 2026-07-31.** Nothing
   was written; every repair below is unstarted. The owner is having the session's
   findings compared against another agent's before code is written — full
   write-up with per-finding confidence labels in **`docs\F86_SESSION_FINDINGS.md`**,
   which also carries **an unrecorded shipped defect the owner found** (our
   `OnMsg.LoadGame` restarts the meteor timer on EVERY load, so a player who
   loads more often than the 35-115 h interval never gets a meteor — report
   §1.4). **Read that report before resuming.**
   *Authorised scope, when it resumes:* Scope in
   `SAVE_SAFETY_REDESIGN.md` **§6**; read it before writing a line.
   **Tier 1 first:** `Fix_MeteorFrequency` (layer 3, thread-keyed
   `GetDisasterWarningTime`; delete the body; split the PT-01 watchdog onto
   `Msg("MeteorDone")`) and `Fix_RainsDeadlock` (layer 2, wrap
   `RainsDisasterActivation`; leave vanilla's loop alone). **Then Tier 2:**
   `Fix_DroneUnreachableForever` (layer 3 — patch the *consumer*
   `CleanUnreachables`), `Fix_TrainWaitTime` (layer 3 via the sync
   `AddSpentTime`), `Fix_ArrivalDeaths` half (b) via `ChooseDome`.
   ⛔ **`Opt_DroneOverhaul` is in scope but BLOCKED on the drone carve-out.**
   ⛔ **LAYER 1 IS NOT TO BE BUILT** — the four own-thread modules and
   `BombardmentSpread` are an accepted residual; do not re-propose it.
   ⚠️ **`Fix_ArrivalDeaths` half (a) (the raw `SetPos`) has NO route yet** — it
   needs a design pass, not a guess.
   *(Superseded framing: the sweep reported and the owner has since picked.)*
   Result in `SAVE_SAFETY_REDESIGN.md` §5. **Five of the twelve exposed modules
   have a layer-3 or layer-2 route out** — `MeteorFrequency`,
   `DroneUnreachableForever`, `TrainWaitTime` and `RainsDeadlock` fully,
   `ArrivalDeaths` by half — each through an input verified **synchronous**.
   Only **four own-thread modules plus `BombardmentSpread`** are layer-1
   candidates, and `BombardmentSpread` has **no** layer-3 route.
   ✅ **The non-exposed half ran too (§5.4, all 22 modules): 6 convert cleanly to
   a chained wrapper, 4 need a design pass, 9 are correctly full replacements, 3
   already optimal. THE SWEEP IS COMPLETE and decision 2 is discharged.**
   **Nothing is built; no code without a further owner go.**
   ⚠️ **Sequencing note:** the `Opt_DroneOverhaul` half of the layer-2 repair
   sits inside a drone-owned module. It is save-safety surgery on a wrapper's
   call position and touches no drone design, so it should be carved out of the
   drone scope fence rather than waiting on the D06 decision — **owner to
   confirm the carve-out.**
7. ⏸️ **D10 — workshops module BUILD. NOT YET — held until the F86 repairs LAND
   AND VERIFY** (owner, 2026-07-31; re-confirmed that the gate is the *build*,
   not the written rules). Speced, user-approved, game-free, un-gated by
   PT-56, and otherwise ready: T1 text repairs + T2 capacity dial
   (base/+50%/+100%, `max_workers` AND `consumption_amount` **PAIRED**), adding
   PT-57 (~7 min) at build time. Full spec on the D10 BUGS entry. **Do not start
   it** — it touches colonist assignment, which is command-thread territory.
8. ⏸️ **D12 — no-homeless dome policy. NOT YET — same hold, same gate (the F86
   repairs must land and verify first).** DECIDED
   and speced. Its own module; `Opt_ResidencyControl` as donor pattern ONLY.
   **Hard constraint:** the new flag must NOT route through
   `CanAcceptNewColonists` (D03's gate) or it blocks the cohort delivery it
   exists to protect. Never expel to the surface. **When the hold lifts: D10 and
   D12 both touch colonist assignment — land them separately, each with its own
   A/B, never entangled.**

**Decisions owed (user):** the **FIX_POLICY §4 amendment** (drafted at the end of
`REACHABILITY_AUDIT.md` — resolve its R4 contradiction with F49(a) first; three
options are on the F49 entry); **D08** and **D06-structural** (UNDECIDED, a third
state — and drone-owned, see the drone prompt); **D11** (feasibility is on the
entry but it is NOT approved — ask fresh; multi-hop passenger routing is
REJECTED). ~~F79~~ is CLOSED `wontfix` — do not re-propose or park it.
**F85 stays observation-gated — do not build it.**

**Release-time owner tasks** (audit plan 2.5): preview image (PDX ≤2 MB / Steam
≤1 MB), screenshots, Paradox portal console-publishing rules.

**🚦 `docs\BETA_READINESS_REVIEW.md` is re-runnable** — derives every fact at run
time, hard gates that cannot be judgement-softened. **Do NOT run it until the
drone design decision has settled.**

### Closed recently — do not re-open or re-file as owed

- **F87** (`Fix_DustSicknessBiorobots` threw at apply on the enable path) —
  **fixed and verified on both load orders 2026-07-31.** The repair is in the
  shared `SMRFixPack.DataPatch` scaffold; the sweep it earned found three more
  modules silently dead on that path, all repaired via the new
  `SMRFixPack.OnDataReady`. The rule is in FIX_POLICY §2 and the load-order
  sequence in ENGINE_FACTS. Only deliberately-undone piece: the C1
  `error`-vs-`inactive` wording split, a FALLBACK the owner did not want in place
  of a real fix — **ask before building it.**
- **Audit A2** — answered YES in play by **PT-55 on 2026-07-30**. A claim that the
  enable-path leg "also verifies A2" was carried in several docs during the F87
  work and is **withdrawn**; A2 is the MODULE toggle flipped mid-session, not the
  PACK enabled at the main menu.
- **F79** — `wontfix` by owner decision 2026-07-31.

---

## First, read (in order) from `C:\Dev\SMR-BugFixPack`

1. **`docs\ENGINE_FACTS.md` — the whole file.** Several behaviours are the
   opposite of what the code suggests; it carries the closure/thread-stack
   persistence facts and the enable-path load order. Then `docs\STATUS.md`
   (compact current state). Session legs are in `docs\archive\SESSION_LOG.md`,
   newest first.
2. `docs\PLAYTEST_CHECKLIST.md` — tests + the reporting protocol only. §1
   standing watches, §2 owed halves, §3 wave-6, §4 fixture sittings, §5
   cross-cutting (PT-20/21), §6 the needs-eyes list. **All reference material —
   ground rules, external-validity rule, cheat discipline, console facts, the
   verified command table, Test Kit helpers, the enable-path leg recipe,
   save-fixture recipes — lives in `docs\PLAYTEST_HELP.md`.** Read its ground
   rules before handing the user any console line.
3. `docs\BUGS.md` — the entries the sitting touches. **F76 before ANY
   depot-picker interaction.** For drone anomalies, the DroneControl bullet in
   "Not yet swept" carries the assignment-machinery trace and the R1-R7
   paste-ready forensics.
4. `docs\FIX_POLICY.md` — binding for any code you write. **§4a is the owner hard
   rule (below); §3a is the NEW save-safety hard rule (layer ordering 3→2→1,
   adopted 2026-07-31 — read it before writing anything that replaces a blocking
   body, wraps a command method, or creates a game-time thread); §2 carries the
   F87 cold-boot rule; §4 has a drafted replacement awaiting the owner.**
5. **`docs\REACHABILITY_AUDIT.md` — the "Challenge review 2026-07-30" at the end,
   before writing ANY new fix.** Tier vocabulary (R1/R2/R3/R4/U + `I`), the hard
   tells that distinguish a defect from designed behaviour, and two standing
   rules: *a state producible only by console/debug injection is evidence
   AGAINST reachability*, and *re-read `git log` between assembling conclusions
   and publishing them*.
6. **Drones: do NOT read in to start work — load `docs\DRONE_PROJECT_PROMPT.md`
   instead.** To answer a passing question only, the sources are the `BUGS.md`
   D06 entry and `docs\DRONE_PRIORITY_SYSTEM.md`.
7. **`docs\FUTURE_IDEAS.md` — the hard rule at the top, before planning ANY
   session.** A proposed-parking list at the bottom awaits the owner's yes/no.
8. Only when relevant: `docs\SAVE_SAFETY_REDESIGN.md` (F86);
   `docs\archive\AUDIT_FINDINGS.md` (ARCHIVED — Phases 1-3 done 2026-07-29,
   Phase 4 EXECUTED 2026-07-31); `docs\DRONE_OVERHAUL_OPTIONS.md`.

Game source (read-only, NEVER modify):
`A:\SteamLibrary\steamapps\common\Project Spark\ModTools\Src`.
Both mods load through junctions from `C:\Dev\SMR-BugFixPack` and
`C:\Dev\SMR-BugFixPack-TestKit`. **Check `Mars.exe` is NOT running BEFORE
touching loadable code** (`tasklist`) — and check it *before*, not in the same
command as the edit.

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
  in-colony; there is **NO main-menu console**).
- Infopanel cheat buttons need `Platform.cheats = true` AND ride the game-time
  sync queue (dead while paused). Direct `SelectedObj:Cheat*()` bypasses both.
- Speed techs sanctioned for setup: `AdvancedDroneDrive`, `LowGDrive`,
  `MartianAerodynamics`. Hive Mind is NOT a drone tech in Relaunched.
- Cheat use is logged per save and blocks that save's achievements — fixture saves
  only.

## Harness facts (for any A/B pair / same-day repair)

- Launch: `& "c:\program files (x86)\steam\steam.exe" -applaunch 3215050 -smrautorun`.
  A leg takes ~75 s; Mars.exe may take minutes to appear. **Never kill on a short
  timeout** (25 min no-kill guard; harness watchdog 15 min).
- Arm the TestKit autorun by uncommenting `"Code/96_AutoRunFlag.lua"` in the TestKit
  metadata `code` list; re-comment to disarm (commented at rest).
- **Enable-path leg** (a player's first run): uncomment
  `"Code/98_EnablePathLeg.lua"` instead, make sure the **fix pack is DISABLED**,
  launch, and have the owner tick it at the main menu — the harness takes over
  from there. Full recipe in `PLAYTEST_HELP.md`. ⚠️ **That click persists**
  (`ModsUIDialogEnd` → `SaveAccountStorage`), so every run must disable the pack
  again first; the leg's guard aborts loudly if it was already on.
- Baseline = overwrite fix pack `metadata.lua` with an emptied `code` list — **keep
  the `default_options` block**. **Restore from a saved copy, NOT `git checkout`,
  while uncommitted metadata changes exist. NEVER `git commit -a` while that edit
  is in the working tree.**
- Opt-in leg mechanism: temporary `Code/97_OptInLeg.lua` in the FIX PACK right
  after 00_Core, setting `SMRFixPack_Optional`. Delete after the leg. **The bridge
  is one-way — it can only force a module ON** (it is checked before
  `CurrentModOptions`, so it overrides an OFF toggle and never touches account
  state). **A true default-config leg (68/74) requires the user to turn the six
  toggles off by hand first** — proven five times over.
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
report-and-continue; self-checks read the DECLARING class; **no `apply()` may
assume a cold boot** (F87 — no class/preset construction at apply time, and
`OnMsg.DataLoaded` alone is not a sufficient trigger); presets only after
DataLoaded (which can fire MORE THAN ONCE); GameVars only inside patched
functions; post-wrappers on command methods never run; `IsValid()` is falsy for
ALL pure-Lua objects; **the shipped build IS Src** (2250/2256 byte-identical —
keep apply-time self-checks anyway, they guard future patches); **a mod function
blocked on a persisted game-time thread enters the save and survives uninstall**
(F86 — and the remedy ordering **3→2→1 is now binding, FIX_POLICY §3a**: patch a
synchronous input over replacing a blocking body, never put mod code after a
call that can block, `SaveGameStart` tear-down last and only with its own A/B +
soak); never modify the game directory; only the playtest flips statuses to
`tested`; mechanical repairs land with a re-verified A/B, redesigns go to the
user; **no live UI-internals prototyping on the user's play sessions**. Commit
with
`git -c user.name="SMR-BugFixPack" -c user.email="154917955+catt144@users.noreply.github.com"`,
push the fix pack (TestKit stays local-only).

**End of session:** update STATUS.md and this prompt (rewrite stale blocks — no
banner stacking), commit, push, summarize.
