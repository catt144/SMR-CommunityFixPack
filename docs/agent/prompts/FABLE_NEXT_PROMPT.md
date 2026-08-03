# General playtest-standby prompt (model-agnostic) — rewritten 2026-08-01

Paste everything below into a fresh Claude Code session — **any Claude model;
the user picks per task.** **Start with `git log --oneline -10` + `git pull`**
— this file goes stale the moment another session commits. (The filename keeps
its historical `FABLE_` prefix so existing references stay valid; nothing in
it is model-specific.) Staleness anchor: **updated 2026-08-03 by chain prompt
12's close-out commit — THE CHAIN IS COMPLETE and `docs/prompts/project/` is
EMPTY.** The final QA's verdict, findings, adjudications (F97 keep / D12 stands
/ F76 closed-refuted, residue = C41) and the ordered campaign top are in
`docs/reports/CHAIN_QA_REPORT.md`; doc-structure recommendations await the
owner in `docs/reports/DOC_STRUCTURE_REVIEW.md`.

> 🗂 **THIS PROMPT IS FOR LIVE PLAYTEST SITTINGS ONLY.** The project chain is
> **complete and its folder is empty** (2026-08-03) — the campaign this prompt
> serves is now the main line of work. Standing non-playtest work is listed in
> `CHAIN_QA_REPORT.md` §8 (D13 is the hard launch dependency, post-campaign;
> release gates; owner decisions). `FIX_POLICY.md` §3a still binds any code any
> session writes. Drone work is separately owned by
> `docs/prompts/DRONE_PROJECT_PROMPT.md` — same rule as before.

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

## F76 — ⛔ THIS WARNING WAS FALSIFIED 2026-08-02. THE PICKER WORKS; USE IT NORMALLY

**Rewritten by the chain prompt 11 attended sitting, which measured the claim
this block used to make and found it wrong.** The old text told you to *"avoid
the picker paths entirely"*. **Do not.** The resource picker is **vanilla** (the
pack touches none of it — verified across all 82 `Code/` files) and it anchors
**exactly at the cursor**: measured `anchor (2051,887)` against live
`mouse (2058,885)`, box centred on the anchor x with its **bottom edge AT** the
anchor y, every number matching prediction to the pixel. The owner clicked the
hex in that sitting and it loaded.

⚠️ **It opens ABOVE the cursor by its own height** (429px at 4K), so a click
high on the screen puts it near the top of the screen. **That is intended, not
displacement.** ✅ F76 is **CLOSED — REFUTED** (chain-12 QA, job 10,
2026-08-03). The one live residue is **C41** (the OG "icon does not appear"
witness + the out-of-range-mouse lead for game windows off the virtual-desktop
origin) — if a sitting ever sees the picker fail to APPEAR, install the
`F76MISS` hook and read where the engine thought the mouse was.

**Two things from the old block that DO still stand, for different reasons:**
- ⛔ **The hard rule survives: NO live UI-internals prototyping in a play
  session.** The 2026-07-27 lock (`XWindow:SetVisibleInstant` on a destroyed
  window, every mouse event erroring, Alt-F4) happened under a wrapper that
  **MUTATED `align_pos`**. The chain-11 sitting was the sanctioned exception and
  it used **read-only** hooks — call `orig` first, print, mutate nothing.
- **The workaround still works and is still worth knowing** if a depot ever does
  refuse a load:
  `rc:SetCommand("TransferResources", depot, "load", "<Resource>", <amount*1000>, true)`

**If a depot or heap click-load misbehaves, do not report it verbally** — take
the two read-only console lines on the **F76 recurrence rider** in
`PLAYTEST_CHECKLIST.md`. A screenshot plus a description is exactly what cost
this project nine days on this entry.

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
3. `docs/BUGS.md` — the entries the sitting touches. **F76 only if a
   depot-picker interaction actually misbehaves** — the old "read this before
   ANY depot-picker interaction" instruction was retired 2026-08-02 with the
   claim behind it (block above).
4. `docs/agent/FIX_POLICY.md` — §4a, §3a, §2 binding for any code written.
5. `docs/reports/REACHABILITY_AUDIT.md` "Challenge review" — before writing
   ANY new fix: tier vocabulary, hard tells, injection-evidence rule.

**End of session:** update `STATUS.md` and this prompt's staleness anchor if
state changed, commit, push, summarize. Chain-owned work discovered → route
to `docs/prompts/project/`, never start it here.
