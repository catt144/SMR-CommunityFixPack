# General playtest-standby prompt (model-agnostic) — rewritten 2026-08-01

Paste everything below into a fresh Claude Code session — **any Claude model;
the user picks per task.** **Start with `git log --oneline -10` + `git pull`**
— this file goes stale the moment another session commits. (The filename keeps
its historical `FABLE_` prefix so existing references stay valid; nothing in
it is model-specific.) Staleness anchor: rewritten with the project-chain
creation commit of 2026-08-01.

> 🗂 **THIS PROMPT IS FOR LIVE PLAYTEST SITTINGS ONLY.** All project work —
> the F86 phases, the audit follow-through, the D10/D12/F76 builds, the final
> QA — lives in **`docs/prompts/project/`**: a self-consuming, numbered
> prompt chain run in filename order (its `README.md` is the manifest and its
> rules bind those sessions). **Do not start project work from this prompt;
> do not duplicate anything the chain owns.** Until the chain's F86 prompts
> complete, F86 remains the release blocker and `FIX_POLICY.md` §3a binds any
> code any session writes. Drone work is separately owned by
> `docs/prompts/DRONE_PROJECT_PROMPT.md` — same rule.

> 📁 **DOCS LAYOUT** — `docs/README.md` if unsure where anything lives.
> Roots: `STATUS.md` (current state; counts live there and nowhere else),
> `BUGS.md` (defect truth), `PLAYTEST_CHECKLIST.md` (tests + protocol),
> `PLAYTEST_HELP.md` (all reference material). Rules: `docs/agent/`
> (`ENGINE_FACTS`, `FIX_POLICY`, `WORKFLOW`). Reports are not authority —
> if a report and a root/agent doc disagree, the root/agent doc wins.

You are assisting a LIVE PLAYTEST: the user is at the keyboard in the retail
game with both mods loaded. Your jobs:

0. **⛔ THE STALE-PROBE GATE — before ANY test, attended or unattended (HARD
   RULE).** Run `grep -rln "TEMPORARY" Code/ ../SMR-BugFixPack-TestKit/Code/`
   and put the result in your todo list. CLEAN = zero hits, or every hit
   explicitly declared by this session's test design. Not clean → repair
   (delete probe + metadata lines, commit) or stop — no result is recorded
   either way, and every result commit carries a `PROBE SWEEP:` line. Full
   rule: `WORKFLOW.md` "Probe hygiene".
1. **Set tests up** — walk the user through `PLAYTEST_CHECKLIST.md`'s own
   steps using `PLAYTEST_HELP.md`'s verified command table; hand exact
   console lines, **one command per line**.
2. **Process results as they arrive** — protocol at the bottom of the
   checklist: PASS → flip status in BOTH BUGS.md places (index row + heading
   tag) and archive the section; FAIL → diagnose live, file the finding with
   the full forensic trail.
3. **Diagnose surprises** — new defects get an F-number, an entry, a severity
   call. Mechanical repairs may land same-day WITH a re-verified A/B;
   redesigns go to the user. Anything that belongs to the project chain gets
   ROUTED to the right chain prompt's `## Notes from upstream`, not started
   here.
4. **Commit as you go** — every processed result or finding is a commit,
   pushed. Docs never lag play. Todo list per `WORKFLOW.md` element 1: one
   item per commit-and-verify unit, one in progress, current at all times.

**⚠️ A PT's own procedure is unverified until it has been executed once.**
Five tests have been found unrunnable-as-written by running them (PT-29,
PT-11, PT-25, PT-59 — and PT-54 was retired unrun into the F86 Tier-1 legs).
For any "nothing should happen" test insist on a **positive control** and an
**objective counter**.

## Standing session rules

- **Never modify the game directory** (`A:\SteamLibrary\steamapps\common\
  Project Spark`); `ModTools\Src` is read-only truth for line numbers.
- **Check `Mars.exe` is NOT running before touching loadable code**
  (`tasklist`) — before, never in the same command as the edit.
- **⛔ FUTURE_IDEAS.md is a parking lot** — nothing in it is work; defects
  never go there.
- **⛔ FIX_POLICY §4a** — this pack never fixes other mods' problems; the
  test is WHO BENEFITS (a player, now or after a patch → real fix; only
  another mod → barred). Judge by enumeration, never by an entry's own words.
- **PT-52 A/B/B2 are FROZEN** (drone-owned). PT-10 is NOT frozen (F55).
- **Account state: READ IT, NEVER ASSUME IT** — the leg's own
  `fix pack present: N/74 fixes active` line and `SMRFixPack.ListFixes()`
  are the only valid reads; toggles AND dials. This sentence has gone stale
  repeatedly; the reading is the truth, this file never is.
- Cheat use is logged per save and blocks achievements — fixture saves only.
  Sanctioned speed techs: `AdvancedDroneDrive`, `LowGDrive`,
  `MartianAerodynamics`.

## F76 — READ BEFORE THE USER TOUCHES AN RC TRANSPORT OR DOZER (vanilla P1, unfixed until chain prompt 11 lands)

The resource picker renders far from the cursor and cannot be clicked on the
user's setup — and interacting with it can **HARD-LOCK the UI (session
lost)**. Surface: ANY vehicle whose click-load reaches a storage-depot-class
object. Avoid the picker paths entirely; loose ground piles are safe;
route-mode loading works for single-resource depots. Verified workaround:
`rc:SetCommand("TransferResources", depot, "load", "<Resource>", <amount*1000>, true)`
**No live UI-internals prototyping in a play session — hard rule.**

## Live-session console facts (hard-won — do not re-derive)

- ONE command per line — a pasted multi-line block silently concatenates and
  fails `not understood`.
- `not understood` = the line did not COMPILE; overwhelmingly a `--` comment
  inside a `*r`/`*g` snippet (they splice onto one line). Never write a
  console snippet with a trailing comment.
- Bare expression for simple reads; `*r`/`*g` for multi-statement snippets
  and assignments (an assignment is not an expression).
- `SMRFixPack.ListFixes()` prints to the LOG — `FlushLogFile()` + newest log,
  or the on-screen loop variant in `PLAYTEST_HELP.md`.
- `ModLog(...)` is the ONLY path proven to reach the log file; the buffer
  flushes at exit — `FlushLogFile()` forces it mid-session.
- Runtime console wrappers must target the LEAF class.
- Console: Enter / Alt-Shift-C / Ctrl-Alt-C; TestKit auto-opens in-colony;
  NO main-menu console. Infopanel cheat buttons need `Platform.cheats = true`
  and ride the game-time queue (dead while paused).

## Harness facts (for any A/B pair / same-day repair)

- Launch: `& "c:\program files (x86)\steam\steam.exe" -applaunch 3215050 -smrautorun`.
  A leg ≈75 s; Mars.exe may take minutes to appear; never kill on a short
  timeout (25-min guard).
- Arm autorun: uncomment `"Code/96_AutoRunFlag.lua"` in TestKit metadata;
  re-comment to disarm. Enable-path leg: `98_EnablePathLeg.lua` instead,
  pack DISABLED first (the click persists — disable again before re-runs);
  recipe in `PLAYTEST_HELP.md`.
- Baseline = fix-pack `metadata.lua` with an emptied `code` list — keep
  `default_options`; restore from a saved copy, NOT `git checkout`; never
  `git commit -a` with that edit in the tree.
- Opt-in leg: temporary `97_OptInLeg.lua` in the FIX PACK sets
  `SMRFixPack_Optional`; delete after. The bridge is one-way (forces ON
  only); a true default-config leg needs the six toggles off by hand.
- Probe-authoring: every probe ends with an explicit `return "PASS", …`
  (nil → silent SKIP). Stand-in probes assert the MODULE's action, never
  vanilla bookkeeping around stubs.
- Known synthetic-map noise (benign): ~50-60 `Flight.lua objects_to_mark`,
  a few GameInit nil-calls, the TestKit shutdown artifact, the MultipleSuns
  lift transient, 2 `ResManager LawOfficeDoor` lines.
- Parse sweep before ANY commit touching Lua (python + luaparser,
  `utf-8-sig`). Docs via editor tools, never bare PS5.1 `Get-Content`
  round-trips. Commits: `git commit -F <file>`, no embedded double quotes,
  project author config (`WORKFLOW.md`), push the fix pack (TestKit is
  local-only).

## Read first, from `C:\Dev\SMR-BugFixPack`

1. `docs/agent/ENGINE_FACTS.md` — whole file (several behaviours are the
   opposite of what code suggests). Then `docs/STATUS.md`.
2. `docs/PLAYTEST_CHECKLIST.md` (tests + protocol) with
   `docs/PLAYTEST_HELP.md` (ground rules BEFORE handing any console line).
3. `docs/BUGS.md` — the entries the sitting touches. **F76 before ANY
   depot-picker interaction** (block above).
4. `docs/agent/FIX_POLICY.md` — §4a, §3a, §2 binding for any code written.
5. `docs/reports/REACHABILITY_AUDIT.md` "Challenge review" — before writing
   ANY new fix: tier vocabulary, hard tells, injection-evidence rule.

**End of session:** update `STATUS.md` and this prompt's staleness anchor if
state changed, commit, push, summarize. Chain-owned work discovered → route
to `docs/prompts/project/`, never start it here.
