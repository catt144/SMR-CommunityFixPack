# CORUN_RIG_SPEC — the co-run rig, specced against provenance

Written by chain prompt 1 (Fable, 2026-08-04). Prompt 2 executes §5 VERBATIM;
prompt 3 builds on §1–§3 only through what co-run #0 proved; prompt 4 finalizes
§4 and integrates. Chain rules (folder README) bind, especially rule 10: **no
step below rests on a primitive outside §1's PROVEN or VERIFIED-IN-SRC bins,
and every VERIFIED-IN-SRC primitive the skeleton uses is flagged for proof in
co-run #0.** Provenance words per R3: MEASURED / SOURCE / INFERRED / GUESS;
predictions are labeled predictions.

## §0 The rig's architecture in one paragraph

The agent's drive surface for a RUNNING game is exactly two things: **code
staged before launch** (TestKit modules — OnMsg hooks, timed threads, the
autorun-harness patterns) and **the log, read back after a flush**. Nothing can
type into a live game from outside: `ConsoleExec` is on `ModEnvBlacklist`
(`Mod.lua:1285`, MEASURED 2026-07-26 — the introspection bridge could not be
automated), so mid-session console lines are owner hands at measure moments,
and OS-level keystroke injection is DESCOPED (never attempted, fragile, not in
the record). Everything else — launch, save staging, scenario scripting,
readiness detection, quit, log round-trip — the agent does. The owner is on
call for: the launch click, modal surprises, console lines the script cannot
schedule, and eyes at measure moments.

## §1 Capability inventory (Job 2)

### PROVEN — EXECUTED-ONCE (or more) in the record

| # | Primitive | Provenance |
|---|-----------|------------|
| P1 | **Launch via Steam**: `& "c:\program files (x86)\steam\steam.exe" -applaunch 3215050 [-smrautorun]` — launched from agent sessions, unattended | MEASURED: four RunAll legs 2026-07-25 (`SESSION_LOG.md` "QA session (wave 3)"), three legs 2026-07-31 (`docs/archive/fingerprint_*.txt` headers, `[SMRAUTO] armed (cmdline -smrautorun)`) |
| P2 | **Direct `Mars.exe` launch is REFUTED** — Steam DRM; bootstrap exits in 28 ms | MEASURED 2026-07-25 (`SESSION_LOG.md` "Superseded: first pair") |
| P3 | **`-save`/`-map` command line is DEAD on retail** — goldmaster-gated | SOURCE `CommonLua/Core/autorun.lua:126-144` (`if not Platform.goldmaster`), corroborated in the 2026-07-25 record ("Retail exe ignores -save/-map") |
| P4 | **Unattended colony bring-up + in-game readiness**: poll `GetPreGameMainMenu()`, then `game_is_live` (`MainCity`+`UIColony`+labels), settle 30 s | MEASURED: every `-smrautorun` leg; patterns at `TestKit/Code/95_AutoRun.lua:185-231` |
| P5 | **Watchdog + programmatic `quit()`** — separate real-time thread, hard stop, log flush before quit | MEASURED: every unattended leg ends in `quit()`; watchdog fired for real during the 2026-07-25 wedge (`95_AutoRun.lua:271-284`) |
| P6 | **Per-line log flush → on-disk trace survives a kill**: `[SMRTest]`/`[SMRAUTO]` lines flush per line; `ModLog` is the only path that reaches the file (EF-015) | MEASURED 2026-07-25 (wedge lesson, `00_TestCore.lua:32-36`); `FlushLogFile()` console form RAN 2026-08-03 (F11 sitting) |
| P7 | **Agent reads the log mid-session after a flush** — that is how F99 was found | MEASURED 2026-08-03 (F99 entry "How it was found"); logs at `%AppData%\Surviving Mars Relaunched\logs`, newest `Mars.exe-YYYYMMDD-HH.MM.SS.log`; **rotation cap ~20 files** (WORKFLOW R8 — it has eaten founding measurements; archive load-bearing logs in the result commit, `git add -f`) |
| P8 | **The one-click hybrid shape works** (owner clicks, harness does the rest): the enable-path leg | MEASURED 2026-07-31 19.09 (`PLAYTEST_HELP.md` "EXECUTED ONCE"; `98_EnablePathLeg.lua`) |
| P9 | **MarsDebug legs are attended BY CONSTRUCTION** — modal `Assert failed` dialogs (engine binding, no Lua switch), Steam-picker launch | MEASURED 2026-08-03 (`[install]` pass, 87/87). Envelope limit, not a problem to solve (README scope fence). ⛔ Never quote MarsDebug tallies as retail (F98) |
| P10 | **Owner-typed console driving at measure moments** — incl. driving a shipped call site directly (`col:SetCommand("EnterTransporter", rocket)`) | MEASURED 2026-08-03 (F11 settling observation, owner at keyboard, agent supplying lines) |
| P11 | **Game-speed/pause caveats that shape scenario scripts**: notification windows run on GAME time; compressed `g_Consts` intervals need `RestartPeriodicRepeatThread`; retail player-reachable speed caps at 5× | MEASURED 2026-07-27 / 2026-07-29 / EF-038 (`PLAYTEST_HELP.md`) |

> ⭐ **CO-RUN #0 RAN 2026-08-04 — VERDICT: PASS WITH CORRECTIONS** (prompt 2,
> Opus). U1 executed end to end on the first attempt; **S1, S2, S4, S5 and S7
> below are hereby PROMOTED to PROVEN** and their ⚠️ flags are struck. Costs and
> corrections: §8, appended by that run. Raw lines:
> `docs/archive/corun0_Mars.exe-20260804-10.51.15.log`.

### VERIFIED-IN-SRC — cited, never executed by us; ⚠️ = skeleton must prove in co-run #0

| # | Primitive | Source citation | Flag |
|---|-----------|-----------------|------|
| S1 | **Load a SPECIFIC save programmatically**: `LoadGame(savename, params)` — `savename` is the on-disk FILE name; the engine's own find-by-display-name pattern is `WaitQuickLoadGame` (`ListForTag("savegame")` → match `save.displayname` → `LoadGame(save.savename, {save_as_last=true})`) | `CommonLua/Savegame.lua:1094-1117`, `:1407-1425` | ~~⚠️ #0 core proof~~ → **PROVEN 2026-08-04**: `LoadGame("CORUN0.savegame.sav", {})` returned no error; the bare filename+ext form is correct (`GetSavePath`, `:541-547`) |
| S2 | **`LoadGame`/`Savegame` are callable from mod code and console** — neither is in `ModEnvBlacklist` (grep of `Mod.lua:1267-1428` this session: only `GetLuaSaveGameData`, `GetLuaLoadGamePermanents`, `DebugDownloadSavegameMods` match save/load names); `LoadGame` yields (loading screens, render-mode waits) so it MUST run in a thread — `CreateRealTimeThread` per the 95_AutoRun precedent | `Mod.lua:1267-1428`; `Savegame.lua:1098-1110` | ~~⚠️ #0 — the TestKit-calls-LoadGame composite is the skeleton~~ → **PROVEN 2026-08-04** from a `CreateRealTimeThread` body. ⭐ Reason strengthened: `Savegame.Load` is `_Wrap`ped (`:337-344`), and the wrapper itself `WaitThread`s — a thread is required by the wrapper, not merely by the loading screens |
| S3 | **Where saves live + what a copy is**: `saves:/` (`GetPCSaveFolder`, `AccountStorage.lua:16`) = `C:\Users\stkot\Saved Games\Surviving Mars Relaunched\76561198020568696\` (VERIFIED ON DISK this session — `TEST2H TRAIN.savegame.sav`, 55,667,524 bytes, 2026-08-03 22:21). Name format `<display>.<tag>.sav`, tag `savegame`, ext `config.SaveGameExt = ".sav"` (`config.lua:21`, `Savegame._UniqueName :295-318`) | as cited | — |
| S4 | **The game SEES a renamed copy**: enumeration is a file listing (`MetadataCache:Enumerate` — `AsyncListFiles(saves:/, *.sav)`), tag parsed from the FILENAME (`_InternalListForTag :479-481`), displayname read from metadata INSIDE the file (`MetadataCache:GetMetadata :85-91`). So `CORUN0.savegame.sav` copied in with the game CLOSED is listed (showing the ORIGINAL display name — cosmetic duplicate in the load menu) and loadable by FILENAME via S1. The engine even ships `Savegame._DefaultCopy` (`:528-535`) — not needed; agent-side file copy is simpler | as cited | ~~⚠️ #0~~ → **PROVEN 2026-08-04**: a plain `Copy-Item` with the game closed produced a file the engine listed and loaded by FILENAME |
| S5 | **Game speed from console/script**: `UIColony:SetGameSpeed(n)` (`Colony.lua:564`); `SetGameSpeedState("ultra")` reaches `SetGameSpeed(20)` unconditionally when called DIRECTLY — the `Platform.debug` gate is only on the +/- cycling lists (`HUD.lua:465-468` vs `:528-544`); needs a live HUD (in-colony). Pause = `SetGameSpeed(0)` | as cited | ~~⚠️ #0 free ride-along (set 3×, read back)~~ → **PROVEN 2026-08-04**: `UIColony:SetGameSpeed(3)` read back `3` via `GetTimeFactor()/const.DefaultTimeFactor`. ⭐ Bonus: the read BEFORE was **`0`** — a freshly loaded save arrives PAUSED, so any game-time work a script schedules is dead until it sets a speed |
| S6 | **Real-time threads run while game time is paused** — the watchdog/harness architecture depends on it (`RealTime()`-based waits); the MarsDebug procedure note relies on it (`*r` while paused) | `95_AutoRun.lua` throughout; `PLAYTEST_HELP.md` step 3 | INFERRED from architecture; #0 need not prove it separately |
| S7 | **Readiness on the LOADED-save path**: `OnMsg.LoadGame` fires (`Lua/_init.lua:77`); `game_is_live` poll should go true after load exactly as after generation | as cited | ~~⚠️ #0 (the poll has only ever run on the new-colony path)~~ → **PROVEN 2026-08-04, and the poll turns out to be redundant**: `game_is_live` was ALREADY true the instant `LoadGame` returned (`STEP 3-waiting-city END 0ms`). `LoadGame` is synchronous to city-live; the wait costs nothing but proves nothing either |
| S8 | **Sandbox map** (what executes where): mod/TestKit code sandboxed on ALL builds incl. MarsDebug (EF-006/EF-010, MEASURED 2026-07-26); retail console = same blacklist (`console.lua:27-56`); asserts-build console = real `_G` (`console.lua:36-44`) | as cited | — |

### UNKNOWN — answered by co-run #0 or descoped

| # | Unknown | Disposition |
|---|---------|-------------|
| U1 | **The composite chain**: staged copy → launch → TestKit `LoadGame` at menu → colony live → scripted read → flush → quit → agent reads log. Every link PROVEN or Src-verified above; the CHAIN has never run | **= co-run #0.** Kill-gate if it fails |
| U2 | **Wall-clock of a ~56 MB save load** (record's legs were ~70 s TOTAL on a tiny synthetic map — `SESSION_LOG.md` 2026-07-30 "~70 s each") | #0 measures; predictions in §5 |
| U3 | **Does the Steam launch picker interpose on `-applaunch`** now that MarsDebug has been used (2026-08-03, "Always use this option" left unticked)? The 07-25/07-31 unattended legs predate that sitting | #0 answers at step 1; the owner's launch click is already budgeted, so either answer is survivable — record which |
| U4 | **`TEST2H TRAIN` contents vs payload needs** (running passenger line? landed surface rocket? depot?) — the record shows what existed IN THE SITTING that evening, not what the save captured | #0 confirm list, §6 |
| U5 | **Simulating a Mod-Manager click, main-menu UI driving** | DESCOPED: `AccountStorage`/`SaveAccountStorage`/`ModsReloadItems` blacklisted (`Mod.lua:1270/:1279/:1392`), no console at main menu — the enable-path click stays human (P8). Not needed by this chain's payloads |
| U6 | **OS-level input injection into the game window** | DESCOPED (§0). If a future payload truly needs it, it is a new chain, not a rider |

## §2 The capability envelope (Job 3) — what routes where

**An UNATTENDED agent run can settle** (all on PROVEN + S1-S7 once #0 passes):

- A/B probe-suite legs on synthetic colonies (the existing harness — routine).
- **Scripted state reads on a staged copy of any save** — the C42 passage
  counter, the F99RESIDUE probe pre-reload, label counts, `ReportTrains`-class
  reads. Today these wait for a sitting; post-#0 they are a launch cycle each.
- **Log-demonstrable mechanism traces with forced upstreams** — the F11
  Done-timing trace (§5 ride-along): wrap a binding, force the upstream, print
  the ordering verdict. Forced-vs-organic rule applies: these establish
  MECHANISM, never organic-witnessed upgrades.
- Amplification loops that need no eyes — loop a suspect path N times at 20×
  and count log hits (C41's spawn/open loop MINUS the eyes half).

**A CO-RUN adds** (owner on call, not on duty):

- **Eyes at measure moments** — C41's vanishing picker (the poster child: agent
  amplifies, owner watches for what only eyes see), the F11 pre-wrapper watch
  (a train visibly unloading and LEAVING; disembark stat movement).
- **Hands for the unscriptable clicks** — Mod-Manager enable/disable (U5),
  the launch click if the picker interposes (U3), killing a truly hung process
  (prompt 2's stop condition).
- **Judgment calls in the moment** — "is that clumping normal?", salvage-cursor
  reads, anything PLAYTEST_HELP's salvage/external-validity notes need a human
  for.
- **Console lines at moments code cannot schedule** — reacting to something
  that just happened on screen (P10).

**Stays ORGANIC-ONLY** (no rig version exists; do not try):

- **Reachability claims** — F99's no-cheat producer (the co-run discriminator
  forces the break and lets drones repair, which is legitimate MECHANISM
  evidence; but "a player hits this" stays organic), F80's trigger.
- **Evidence upgrades to organic-witnessed** — F02/F78/F81 fired organically
  2026-08-03 and that is what upgraded them; a forced repro never does (rule 11).
- **Feel, severity, "does the player notice"** — behavioural/timing claims do
  not generalise from rigged colonies (EXTERNAL VALIDITY, PLAYTEST_HELP);
  D06-class judgments; the owner's win-calls (PT-62).
- **The owner's own campaign** — never a rig target (FIX_POLICY §3a; runs use
  a staged COPY of the designated save, only).

## §3 Risk register + effort model (Job 4)

**Effort model (predictions, labeled — co-run #0 measures):**

- **One launch cycle** (launch → menu → load 56 MB → settle → read → flush →
  quit → log read): PREDICTED 5–8 min wall-clock. Basis: ~70 s full synthetic
  legs (MEASURED) + an unmeasured save load; menu/city timeouts already allow
  5 min each (`95_AutoRun.lua:85-88`).
- **Iteration cost of a wrong script**: one full relaunch cycle — mod code
  loads at boot, there is no hot reload in the rig's shape. A session that
  ships 5 script errors pays ~30–40 min. This is THE cost driver; mitigations
  below.
- **Token cost per chain prompt**: GUESS 60–150k output; this prompt is the
  live sample and prompt 4 audits actuals.
- **Owner-attended minutes**: #0 ≈ 10 (launch click + stand by); #1 ≈ 15–20
  across all four candidates (measure moments only, batched per WORKFLOW
  "Batch aggressively"). Anything trending past the promise mid-run: stop and
  reschedule, do not stretch the sitting.

**Top 3 ways this rig eats 3 days, and what in this spec prevents each:**

1. **Building payloads on an unproven load path.** The classic hasty plan:
   write all four candidate scripts, discover `LoadGame`-from-mod-code has some
   unrecorded gotcha, rework everything. **Prevention:** the kill-gate ORDER —
   co-run #0 proves U1 with ONE trivial read before prompt 3 exists; §1 rule 10
   forbids any payload step citing an unproven bin.
2. **Relaunch churn from script defects.** Each error costs a cycle (~6 min +
   agent overhead), and in-game Lua fails unhelpfully (`error()` does not
   unwind mod code — EF-008 — so a probe half-runs and lies). **Prevention:**
   parse sweep before EVERY launch (binding, WORKFLOW); scripts copy PROVEN
   patterns only (`95_AutoRun`'s rawget/sprocall/watchdog style, `00_TestCore`
   deferred verdicts); one probe = one question; per-line flush means even a
   wedged run leaves its trace (P6), so no cycle is a total loss.
3. **Contaminated measurements forcing re-runs.** Stale probes (the 2026-07-31
   armed-for-days incident), wrong toggle state read as a fix failure ("OFF is
   three different things"), warmed-vs-cold confusion, MarsDebug numbers quoted
   as retail (F98). **Prevention:** probe-hygiene hard gate before every run +
   `PROBE SWEEP:` line in result commits (binding); run-conditions header on
   every recorded number (`ListFixes` count READ never assumed); rig runs are
   always COLD loads of a staged copy — state that in every card; §1 P9 keeps
   debug-build evidence quarantined.

**Also on the register:** save-folder pollution (staged copies are Steam-Cloud
synced — the `saves:/` folder is under `remotecache.vdf`; delete `CORUN0*.sav`
in the same commit that records the run, probe hygiene applied to saves) ·
log rotation eating evidence mid-effort (P7 — archive in the result commit) ·
the owner's ~10 min stretching into a debugging session (prompt 2's stop
condition: owner unavailable or budget blown → commit prep, report, stop).

## §4 Sign-off tiers — DRAFT (Job 5) ⛔ drafted, NOT adopted; prompt 4 finalizes against real cards and ROUTES the decision (it changes the `tested` policy, which is the owner's)

**The classification rule** (mechanical, so a future session applies it without
judgment):

> (a) Would owner eyes at the screen add information the log cannot carry?
> → **Tier A**. Else (b) can a probe falsify the claim without human judgment?
> → **Tier C**. Else → **Tier B**.

- **Tier A — WITNESS.** Visible behaviour is the evidence. The owner attends
  the measure moment; the brief's measure-moments list names what they look at
  and the verdict words. Examples from the live candidates: the F11
  pre-wrapper watch (train unloads and LEAVES; stats move), C41's picker watch.
- **Tier B — EVIDENCE CARD.** Log-demonstrable; the owner quick-reads a card
  and OKs. **The card template (MUST contain, capped at ONE screen):**

  ```
  EVIDENCE CARD — <ID> <claim being signed off>
  Scenario: <one paragraph: what ran, on what save, cold/warmed>
  Forced: <what was forced> / Organic: <what was not>
  Raw log, before:  <the actual lines — never summaries>
  Raw log, after:   <the actual lines>
  Build: 1.0.7.396349 · pack <N/81 line as read> · session <uptime>
  PROBE SWEEP: <clean | armed: files, declared by test>
  This card is wrong if: <the falsifier, one sentence>
  ```

  The card exists so "I only hit flushed logs and said ok" stops being true:
  the owner sees the scenario, the raw lines, and the falsifier — enough to
  genuinely disagree — in under a minute.
- **Tier C — DELEGATED.** Mechanically self-verifying (the A/B probe-suite
  class): ships on the suite verdict; the owner gets a one-line digest per
  batch, retains veto, is not asked per item.
- **Worked classifications (DRAFT, to be tested against prompt 3's real
  cards):** F11 watch → A · F11 Done-timing trace → B (mechanism read, needs
  the forced/organic framing a human should see) · hex tie-break console read
  → B · C41 picker → A · F99 no-cheat discriminator → C candidate (the
  `TrackElement.lua:805` line either appears or does not) — but its FIRST
  occurrence is a severity fact the owner asked to own, so route the initial
  verdict as B.

## §5 Co-run #0 — the walking skeleton (Job 6; prompt 2 executes verbatim)

**Purpose:** prove U1 end-to-end at minimum cost, measure U2, answer U3/U4.
Nothing ambitious rides on it except one free trace.

**Prep (all unattended, before the owner sits down):**

1. Probe-hygiene sweep; record the line.
2. Stage the copy, game closed:
   `Copy-Item "TEST2H TRAIN.savegame.sav" "CORUN0.savegame.sav"` in
   `C:\Users\stkot\Saved Games\Surviving Mars Relaunched\76561198020568696\`
   `[NEVER RUN]` — the save itself is never written (README owner decision).
3. Write ONE TestKit file `Code/97_CoRun0.lua` (header carries the literal
   `TEMPORARY`), added to TestKit `metadata.lua` code list. It must:
   - **not** arm `96_AutoRunFlag` and the launch must **omit** `-smrautorun`,
     so `95_AutoRun` stands down by itself (its `Requested()` finds nothing);
   - copy 95's proven patterns: real-time thread + `Sleep(1)`; own watchdog
     (10 min hard quit); `say()`-style per-line-flushed `[CORUN0]` markers;
     `sprocall` for yielding steps; poll `GetPreGameMainMenu()`;
   - then: `LoadGame("CORUN0.savegame.sav", {})` (S1/S2 — filename form; if it
     returns err, log `[CORUN0] LOADERR <err>` and quit);
   - poll `game_is_live` (S7), settle 30 s;
   - trivial reads, each one `ModLog` line: the `fix pack present: N/81` count
     (via `SMRFixPack.order` walk), `SMRTest.ReportTrains`-class counts (PROVEN
     helper), a label count for stations/rockets/depots (the §6 confirm list),
     `UIColony:SetGameSpeed(3)` + read-back (S5 flag);
   - the ride-along (below), guarded so its absence cannot kill the skeleton;
   - `FlushLogFile()`, `quit()`.
4. Parse sweep (python + luaparser, `utf-8-sig`) — before EVERY launch, not
   just the first.
5. Pre-write the measure-moments list for the owner (expected: launch click,
   stand by; verdict words: "menu up", "loading", "desktop back" + read out
   anything modal).

**The ride-along — the F11 `OnTransferToMapDone`-timing trace** (from `F11.md`
"Route claim narrowed"; settles route (a) vs (b)):

- Pre-wrap `Unit.OnTransferToMapDone` (plain method wrap from TestKit, the
  pack's standard shape): at entry, log the unit id, `holder` identity, and
  `table.find(holder.units, self)`; call the original; log the find again.
- Scripted forced upstream, in a game-time thread after settle: find a colonist
  aboard a train (`train.units`), find a surface rocket, drive the shipped call
  site `col:SetCommand("EnterTransporter", rocket)` — verbatim the F11 sitting's
  MEASURED procedure (P10), now scripted. Log the same before/after finds the
  sitting printed, plus container identity and `#units` immediately before (the
  F11 entry's own prophylactic).
- Verdict table: Done-wrapper fires with the unit still IN `holder.units` and
  it is gone after → route (a) confirmed. Done never fires for the transfer, or
  fires with the list already clean → route (b). Either way MEASURED; **forced:
  the abduction; organic: the cleanup ordering under measurement.**
- If the save carries no train rider or no surface rocket at read time: log
  `[CORUN0] RIDEALONG SKIP <which>` — a §6 gap, NOT a skeleton failure.

**Run steps, predicted costs, abort thresholds (each threshold = 3× prediction;
tripping ANY aborts per the kill-gate):**

| step | prediction (PREDICTED, not fact) | abort at |
|------|------------------|----------|
| 1. Owner clicks launch (steam `-applaunch 3215050`, NO `-smrautorun`); records whether the picker appeared (U3) | menu in ≤2 min | 6 min |
| 2. Harness loads the copy | load ≤3 min | 9 min |
| 3. Readiness + settle | ≤1 min | 3 min |
| 4. Scripted reads + ride-along | ≤1 min | 3 min |
| 5. Flush, quit, desktop back | ≤1 min | 3 min |
| 6. Agent reads newest log, records actuals vs predictions | ≤5 min | — |

Whole-cycle prediction: **5–8 min game-side, owner envelope ~10 min.**

**Abort criteria (any → the kill-gate, prompt 2 Job 4):** `LOADERR`; any step
over its 3× threshold; watchdog fires; the game needs more than the single
launch click from the owner to reach the menu; any §1 ⚠️-flagged primitive
answers NO. A clean abort that recorded WHY is the gate working.

**After the run (same session):** delete `97_CoRun0.lua` + its metadata line
and `CORUN0.savegame.sav` in the commit that records the answers; `PROBE
SWEEP:` line; archive the log if any recorded number cites it; Done-timing
verdict to `F11.md` (prompt 2 Job 5).

## §6 The designated save — `TEST2H TRAIN`, validated (Job 7)

**Confirmed from the record and disk (no re-choice — the owner chose it):**

- ON DISK: `TEST2H TRAIN.savegame.sav`, 55,667,524 bytes, last written
  **2026-08-03 22:21** — the same evening as the F11 rider sitting (log
  `Mars.exe-20260803-21.18.38`) and minutes before the campaign suite log
  (`22.23.59`). MEASURED this session.
- That sitting's colony HAD: a passenger train line with live riders (`#train.units`
  = 6, a rider measured aboard — F11 entry), an underground build-out with
  track (F99's seven throws during its cheat completion), and a surface rocket
  with a 1543-colonist gather pool (F11 measurement). INFERRED, flagged: the
  SAVE's capture of each is unverified — a save records a moment, not a sitting.

**Confirm in-game at co-run #0 (§5 step 4 reads; a gap is routed as a gap —
"needs X staged" — never as a re-choice):**

| payload | needs | if missing |
|---------|-------|-----------|
| F11 watch + Done-timing trace | a colonist actually aboard a train at read time; a landed/waiting surface rocket to abduct into | rider: wait/loop a few game-hours at speed 3 before declaring SKIP; rocket: co-run #1 preps one (cheat-place — forced upstream, named) |
| Hex tie-break read | underground track with a breakable element | if absent: co-run #1 stages a meteor break (`CheatMeteors` at a position — forced, named) |
| C41 loop | any resource depot or heap for the picker | if absent: cheat-place a depot in #1 prep (forced setup, organic measured path — the click/picker) |
| F99 discriminator | damaged track + outstanding `repair_cgs` + drones able to repair, NO completion cheat on the measured path | needs a meteor break staged in #1; the REPAIR must stay organic |

**GO routing:** the schedule ask for co-run #0 (~10 min owner stand-by) goes on
`PLAYTEST_CHECKLIST.md` "Decisions waiting on you" in this prompt's closing
commit — R10; an ask recorded only here is not asked.

## §7 Pointers

*(§8 below is appended by co-run #0 itself. §1–§7 are prompt 1's text, corrected
in place by strike-and-supersede only.)*

Harness patterns: `C:\Dev\SMR-BugFixPack-TestKit\Code\95_AutoRun.lua`,
`00_TestCore.lua` (deferred verdicts, `set_global`, env-specials guard) ·
payload entries: `agent/bugs/F11.md`, `F99.md`, `C41.md` · binding process:
folder README rules 8/10/11, WORKFLOW "Co-runs" + probe hygiene · console
facts + verified command table: `PLAYTEST_HELP.md`.

## §8 CO-RUN #0 — WHAT ACTUALLY RAN (2026-08-04, prompt 2; ⛔ kill-gate verdict: **PASS WITH CORRECTIONS**)

**Run conditions.** Retail `Mars.exe` **1.0.7.396349**, launched
`& "c:\program files (x86)\steam\steam.exe" -applaunch 3215050` with **no**
`-smrautorun` (95_AutoRun stood down as designed). Cold load of
`CORUN0.savegame.sav`, a `Copy-Item` copy of `TEST2H TRAIN` staged with the game
closed. Fix pack read **81/81 active, 0 inactive, 0 disabled, 0 error**.
`PROBE SWEEP: armed: TestKit Code/97_CoRun0.lua, declared by co-run #0` — probe
and staged save both deleted in the commit carrying this section. Raw lines
archived: `docs/archive/corun0_Mars.exe-20260804-10.51.15.log`.

### Costs — PREDICTED vs ACTUAL

| step | predicted | abort at | **ACTUAL** |
|------|-----------|----------|------------|
| 1. launch → main menu | ≤2 min | 6 min | **~2.7 s** (launch cmd 10:51:13.8 → log 10:51:16.0; menu found 0.5 s after mod load) |
| 2. harness loads the copy | ≤3 min | 9 min | **9.97 s** (engine clock; ⛔ see correction C1) |
| 3. readiness + settle | ≤1 min | 3 min | **0 s + 30 s** settle (the 30 s is our own constant) |
| 4. scripted reads + ride-along | ≤1 min | 3 min | **15 s**, of which 15 s is the ride-along's own `Sleep`; the six reads were sub-frame |
| 5. flush, quit, desktop back | ≤1 min | 3 min | **~1.5 s** |
| 6. agent reads log | ≤5 min | — | ~4 min |
| **whole cycle, launch → desktop** | **5–8 min** | — | **79.9 s** (`Time (ms) 79876`) |
| **owner-attended minutes** | **~10** | — | **~1.5** — one GO, then watching; no click was needed at all |

Nothing came within 10% of any abort threshold. No `LOADERR`, no watchdog, no
`[LUA ERROR]`, no `Assert failed`, no modal.

### UNKNOWNS answered

- **U1 — the composite chain: YES.** staged copy → launch → TestKit `LoadGame` at
  the menu → colony live → scripted reads → flush → `quit()` → agent reads the
  log ran **end to end on the first attempt**, zero relaunch churn. This is the
  gate the whole chain existed to pass.
- **U2 — 56 MB load wall-clock: 9,968 ms.** Source: the engine's own
  `Game loaded on map BlankBigCanyonCMix_09 in 9968 ms` (`Savegame.lua:1114`,
  `GetPreciseTicks`). ~3.3× the record's ~3 s-equivalent synthetic legs, and
  **18× inside** the abort threshold. A launch cycle on the designated save is a
  **~80 s** affair, not the predicted 5–8 min — the effort model in §3 is
  **~4–6× pessimistic** and prompt 4 should re-derive the economics from this.
- **U3 — does the Steam picker interpose: NO.** MEASURED by timestamp: the game
  log was created **2.2 s** after the launch command returned, which no human
  click can fit inside. The owner was seated and reported no picker. The
  budgeted launch click was **not needed**.
- **U4 — `TEST2H TRAIN` contents:** §6 confirm table below.

### §6 confirm table — READ

| payload | needs | **as read 2026-08-04** |
|---|---|---|
| F11 watch + Done-timing | rider aboard a train; landed surface rocket | ✅ **both** — 8 trains, **59 riders aboard**; 5 `AllRockets`, `UniversalZeusRocket` `landed=true` `command=CmdWaitOrder` on the surface map |
| Hex tie-break read | underground track with a breakable element | ⛔ **GAP** — 926 `TrackGridElement`s, **0** with a live `broken` element |
| C41 loop | any resource depot or heap | ✅ **abundant** — 11 `UniversalStorageDepot`, 658 `ResourceStockpileBase` |
| F99 discriminator | damaged track + outstanding repair sites | ⛔ **GAP** — **0** repair construction sites on broken track |

**Both gaps are the ones §6 already anticipated**, and §6's own remedy stands:
co-run #1 stages a meteor break (`CheatMeteors` at a position — forced upstream,
named; the repair itself must stay organic for F99). Routed as a gap, **not** as
a re-choice of save — the save is otherwise richer than the record suggested.

### ⛔ CORRECTIONS to this spec (the "WITH CORRECTIONS" half of the verdict)

- **C1 — `RealTime()` deltas are NOT a valid step timer, and §5 assumed they
  were.** The same `LoadGame` call measured **864 ms** on the harness's
  `RealTime()` clock and **9,968 ms** on the engine's. `RealTime` advances per
  rendered frame and `LoadGame` blocks in `WaitRenderMode` where none run.
  **Any rig step spanning a loading screen must be timed by the engine's own
  line, by OS file timestamps, or externally.** Filed as `agent/facts/EF-045`.
- **C2 — §5's ride-along verdict table is conditional and does not say so.** Its
  SYNC/DEFERRED → route (a)/(b) mapping is valid **only for a cross-map
  abduction**. The run's pair was same-map (`cross_map=false`), so `DEFERRED`
  followed trivially from `TransferToMap` never being called and settled nothing
  about routes (a)/(b). A cross-map pair must be **selected for** — underground
  rider + surface rocket. What the run *did* settle (the same-map removal path,
  previously flagged unmeasured) is recorded in `agent/bugs/F11.md`.
- **C3 — S7's readiness poll is redundant on the loaded-save path.** `LoadGame`
  returns with the city already live (`STEP 3-waiting-city END 0ms`). Harmless,
  but it is not the safety net §5 presented it as; a script that *needs* a
  post-load settle must schedule it explicitly, as this one did.
- **C4 — §5 prep 3 does not mention that a freshly loaded save arrives PAUSED.**
  Game speed read back **`0`** before `SetGameSpeed(3)`. Any game-time thread a
  scenario schedules is dead on arrival until a speed is set — this run's
  15 s abduction window only worked because the speed call preceded it.
- **C5 — the `TEMPORARY` gate and `doccheck.py` disagree, and doccheck wins.**
  `WORKFLOW.md` probe hygiene defines CLEAN as "zero hits, **or** every hit is a
  probe this session's design explicitly declares"; `doccheck.py`'s
  `temporary_sweep()` has **no such escape hatch** and reds on any hit, and the
  pre-commit hook blocks. Co-run #0 is the first job to arm a probe since
  doccheck landed (2026-08-03), so it is the first to hit this. It was survivable
  here only because the owner was available immediately, letting prep and results
  land in one commit with the probe already deleted. **A co-run that must commit
  prep before the sitting is blocked today.** ~~Routed to prompt 4 (rig
  integration) — the fix is a declared-probe hatch in doccheck~~
  ⭐ **SUPERSEDED — DECIDED BY THE OWNER, 2026-08-04, same day:** *"I want to do
  whatever is safest, I do not want to get back into the situations where armed
  probes start giving us false problems or issues."* **The tool is NOT loosened
  — no declared-probe hatch is built.** The protocol tightens instead:
  **a probe file is present in `Code/` only while its run is actually happening**
  (`WORKFLOW.md` probe hygiene rule 5). Prep commits carry the probe's source as
  a fenced block in the brief — inert by construction, since the mod loads only
  files listed in `metadata.lua` `code` — and the file lands in `Code/` at the
  sitting and dies in the commit that records the answer. A slipped sitting then
  strands nothing and arms nothing. ⛔ `--no-verify` was never an option: the
  hook documents its meaning as "the docs are inconsistent, I know", which is a
  false statement when the only red is a declared probe. ⚖️ **The owner has
  asked prompt 4 to RECHECK both prompt 2's diagnosis and their own decision,
  and is open to recommendations** (2026-08-04) — the rule stays in force
  meanwhile. Prompt 4's note carries the four recheck targets, including the one
  claim prompt 2 did not verify (that `ModsLoadCode` reads only the
  `metadata.lua` `code` list) and the strongest objections prompt 2 found
  against its own recommendation.

### What may NOT be claimed from this run

- Not that the rig "works" beyond these steps. **Amplification loops, multi-cycle
  legs, watchdog-under-real-wedge and Mod-Manager driving are still unexercised.**
  The watchdog did not fire, so it is proven present, not proven effective.
  *(⭐ Amplification loops and multi-cycle legs are now exercised — §9.)*
- Not `tested` for F11 or anything else. The ride-along is MECHANISM evidence
  from a FORCED upstream; F11's evidence label is unchanged.
- Not owner-minutes savings — prompt 4 owns the economics audit. What is recorded
  here is one measurement (~1.5 min actual vs ~10 promised), not a trend.

## §9 CO-RUN #1 — THE PAYLOAD RUN (2026-08-04, prompt 3; ran TWICE)

**Run conditions.** Retail `Mars.exe` **1.0.7.396349**,
`steam.exe -applaunch 3215050` with no `-smrautorun` (95_AutoRun stood down as
designed, both times). COLD load of `CORUN1.savegame.sav`, a `Copy-Item` copy of
`TEST2H TRAIN` staged with the game closed; the campaign save read the same
55,667,524 bytes / 2026-08-03 22:21 afterwards. Fix pack **81/81 active**.
**Zero** `[LUA ERROR]`, **zero** `Assert failed`, **zero** modals, both runs.
`PROBE SWEEP: armed: TestKit Code/97_CoRun1.lua (run 1), Code/97_CoRun1b.lua
(run 2), declared by co-run #1` — both deleted with their `metadata.lua` lines
and the staged save. ⚖️ The armed-prep override was **DECLINED**
(`CORUN1_BRIEF.md` §6). Logs archived: `docs/archive/corun1_*.log`,
`corun1b_*.log`. Cards: `agent/reports/CORUN1_EVIDENCE_CARDS.md`.

### Costs — and ⚠️ §8's 80 s is the FLOOR, not the cycle cost

| | co-run #0 | **#1 run 1** | **#1 run 2** | **#1 run 3** |
|---|---|---|---|---|
| launch cmd → game log created | 2.2 s | **5.2 s** | **1.7 s** | ~1 s |
| menu poll | 2.5 s | 2.5 s | 2.5 s | 2.5 s |
| **load, by the engine's own line** | 9,968 ms | **9,784 ms** | **9,531 ms** | (not re-read) |
| readiness | 0 ms | 0 ms | 0 ms | 0 ms |
| settle (our own constant) | 30 s | 15 s | 15 s | 15 s |
| payload | 15 s | **~315 s** | **~35 s** | **~14 s** |
| **whole cycle (`Time (ms)`)** | 79,876 | **398,115** | **85,125** | **64,362** |
| **owner-attended** | ~1.5 min / ~10 | **~5 min** | **~1 min** | **~0.5 min** — three runs against **~15–20 promised**, **~6.5 min total** |

⚠️ **The load is stable at ~9.5–10.0 s across three cold loads** — that is the
one number the effort model can lean on. Everything else scales with the
payload. **A cycle costs `~30 s of fixed overhead + the payload`**, and the
payload is whatever the legs are; §3's "5–8 min per cycle" is still pessimistic
for a *thin* leg and roughly right for a *fat* one, which is a different claim
from §8's. ⚠️ **launch→log varied 1.7–5.2 s across three launches** — no human
click fits in any of them (U3 holds), but the figure is not a constant.

⭐ **Halving the settle from 30 s to 15 s cost nothing observable** — 81/81 read
active, every label read populated, no `[LUA ERROR]`. §5's 30 s is unjustified
by anything measured; 15 s is now the datum.

### What ran, and what it settled

| item | verdict |
|---|---|
| **1 · F11 pre-wrapper watch** (Tier A) | **2 of 3 readings PASS**; ⛔ not `tested` — the stat reading is unavailable on this save (`LuxuriousTrains` researched, 0 forest tracks). 340 holder removals, 7 trains, **0 wedges**. Close decision routed to the owner |
| **2 · F99 hex tie-break** (ride-along) | ⭐ **SETTLED — the hex returns the HIDDEN ELEMENT**, confirmed twice, against a pre-break control |
| **3 · C41 amplification** (Tier A) | ⭐ **the M5 lead is MEASURED** (29/300 organic, 20/20 forced; `x` to 7665) **and BOTH clamps fire for an out-of-range anchor** — run 3 reproduced a pre-registered corner box `(2224,1731)-(3840,2160)` **to the pixel**; ⛔ picker appeared **52/52** across three runs, so the OG symptom did **not** reproduce. `cand` unchanged |
| **4 · F11 cross-map Done-timing** (ride-along) | ⭐ **SETTLED — route (a)**; route (b) excluded. Run 1 skipped it (one-shot selector, no rider aboard at that instant); run 2's retry loop found the fixture on its first sweep |

⭐ **The class-2 use case is now exercised, which §8 listed as unproven.**
Amplification loops ran (20-cycle picker loop ×2, a 300-sample 5 Hz poll, a
238 s 1 Hz train poll) and a **multi-cycle leg** ran (two launches in one
sitting, second one authored from the first one's gaps). The watchdog still has
not fired, so it stays proven-present, not proven-effective.

### ⛔ CORRECTIONS TO THIS SPEC (co-run #1)

- **C6 — §6's `CheatMeteors` remedy is the worse of two routes.** `BreakTracks`
  (`Meteors.lua:599-607`) — what the cheat eventually reaches — calls
  `track:BreakTrackElement(element, cg)` on every element that is neither
  `start_el` nor `end_el` and carries no station. **Drive that site directly on
  a chosen element**: same mechanism, no disaster thread, no collateral, lottery
  removed, ~3 s instead of a disaster's game time. `WORKFLOW.md` leg-design
  rule 2 already says so; §6 predates it.
- **C7 — "wrap `Holder.OnExitHolder` and print its caller" is impossible.**
  `debug` is on `ModEnvBlacklist`, so mod code cannot read a stack at all.
  ⭐ **Ordering replaces it and is better:** several wraps sharing one sequence
  counter make nesting directly readable, which brackets the *transfer* as well
  as naming the *remover*. That is what settled payload item 4.
- **C8 — §5's `RealTime()`-timed step lines mislead even where C1 is honoured.**
  The probe printed `STEP 2-loading-save END 874ms` beside an engine line
  reading `9784 ms`. C1 says do not *trust* them; **the stronger rule is do not
  PRINT them for a step that spans a loading screen** — a future reader will
  quote the wrong number out of the log. `facts/EF-045` should say so.
- **C9 — §3's effort model needs re-deriving from payload runs, not from #0.**
  §8 called §3 "~4–6× pessimistic" on the strength of one 15 s-payload cycle.
  With three real payload runs the honest shape is **fixed ~30 s + payload**,
  and a fat leg reaches 6.6 min. Prompt 4 owns the re-derivation.
- **C10 — ⛔ a negative result must state the CONDITION it sampled, not just the
  count.** §5's abort/claim discipline and §8's "absence under N cycles is a rate
  bound" are both written about **counts**, and that is why neither caught this
  run's worst error: run 2 recorded a pre-registered prediction as **REFUTED**
  when the condition it needed had never been sampled, and supplied a confident
  false reason for it. Run 3 sampled the condition and the prediction was
  confirmed **to the pixel**. **The rate-bound rule should be generalised to
  cover sampling gaps, not only rate gaps** (prompt 4).
- **C11 — arming edits must be a script FILE, never an inline one-liner through
  PowerShell.** Run 3's `metadata.lua` edit was written as inline Python, whose
  quoting PowerShell mangled; the edit silently did not happen and **the game
  launched unarmed**. Nothing in the procedure caught it — only reading the tool
  output did. Same hazard class the project already records for
  `git commit -m` (use `-F <file>`).
