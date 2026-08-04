# General playtest-standby prompt (model-agnostic) — full pass 2026-08-04

Paste everything below into a fresh Claude Code session — **any Claude model;
the user picks per task.** **Start with `git log --oneline -10` + `git pull`**
— this file goes stale the moment another session commits. Staleness anchor:
**full owner-directed pass 2026-08-04** (decision record:
`agent/reports/STANDING_PROMPTS_REDESIGN.md` + the pass commit).

> ⛔ **THIS PROMPT IS INSTRUCTIONS, NOT A LOGBOOK** (rule added 2026-08-04;
> doccheck enforces a 220-line cap). A sitting's lesson goes to its proper
> home in the SAME close-out commit: testing discipline → `WORKFLOW.md` ·
> console/procedure recipes → `PLAYTEST_HELP.md` · proven engine behaviour →
> a new `agent/facts/EF-###.md` (+ regenerate the INDEX) · result narrative →
> the `agent/bugs/` entry. The only edits this file takes are corrections to
> its own instructions. **Litmus: anything in here naming a specific PT or
> entry ID is probably a squatter** — statuses live in the checklist and the
> entries, never here.

> 🗂 **THIS PROMPT IS FOR LIVE PLAYTEST SITTINGS ONLY** — the campaign is the
> main line of work. Standing non-playtest work: `agent/STATE.md` and
> `CHAIN_QA_REPORT.md` §8. `FIX_POLICY.md` §3a binds any code any session
> writes. Drone work is separately owned by
> `docs/agent/prompts/DRONE_PROJECT_PROMPT.md`.

> 📁 **LAYOUT** — `docs/README.md` is the map (`CLAUDE.md`, auto-loaded,
> carries the contract). Two judgment rules that bite in sittings: **both
> INDEX.md files are GENERATED — edit the entry/fact file, never the index**;
> and **reports are not authority** — if a report and a root/agent doc
> disagree, the root/agent doc wins.

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
   checklist: PASS → flip status in BOTH places inside `agent/bugs/<ID>.md`,
   front matter FIRST, then the heading tag to match (`WORKFLOW.md` mechanical
   rule 6; INDEX.md is generated, never hand-edited) and archive the section;
   FAIL → diagnose live, file the finding with the full forensic trail.
3. **Diagnose surprises** — new defects get an F-number, an entry, a severity
   call. Mechanical repairs may land same-day WITH a re-verified A/B;
   redesigns go to the user. Anything too big for the sitting gets FILED —
   an `agent/bugs/` entry, plus a checklist rider when the precondition is a
   situation (TAKEABLE-WHEN, `WORKFLOW.md` binding rule 3) — never started
   here. No project chain is active to route to.
4. **Commit as you go** — every processed result or finding is a commit,
   pushed. Docs never lag play. Todo list per `WORKFLOW.md` element 1: one
   item per commit-and-verify unit, one in progress, current at all times.

**⚠️ A PT's own procedure is unverified until it has been executed once** —
five tests have been found unrunnable-as-written only by running them. For any
"nothing should happen" test, the leg-design rules in `WORKFLOW.md` "Testing
checklist" bind: a positive control, and an objective counter **that can
fail**.

## Standing session rules

- **Never modify the game directory** (`A:\SteamLibrary\steamapps\common\
  Project Spark`); `ModTools\Src` is read-only truth for line numbers.
- **Check `Mars.exe` is NOT running before touching loadable code**
  (`tasklist`) — before, never in the same command as the edit.
- **⛔ FUTURE_IDEAS.md is a parking lot** — nothing in it is work; defects
  never go there.
- **Fix/file judgments are `FIX_POLICY.md`'s** (§4a who-benefits, §3a
  save-safety, §2 enable-path) — open it before writing any fix, and **judge
  by enumeration, never by an entry's own words.**
- **Account state: READ IT, NEVER ASSUME IT** — the leg's own
  `fix pack present: N/74 fixes active` line and `SMRFixPack.ListFixes()`
  are the only valid reads; toggles AND dials. This sentence has gone stale
  repeatedly; the reading is the truth, this file never is.
- **Cheat discipline is `PLAYTEST_HELP.md`'s** ("Cheating without
  contaminating results" — incl. the sanctioned speed techs): cheat the
  setup, never the mechanism under observation; fixture saves only.
- ⛔ **NO live UI-internals prototyping in a play session** — hard rule; the
  lock story and the one sanctioned pattern (read-only hooks) are
  `PLAYTEST_HELP.md` ground rule 5. If a depot/heap click-load ever
  misbehaves: the **F76/C41 recurrence rider** in the checklist (hooks +
  workaround there), never a verbal report — a screenshot plus a description
  once cost this project nine days.

## Console and harness — where the recipes live

**All console facts and harness recipes are `PLAYTEST_HELP.md`'s** ("Console:
what works and what silently does nothing" · "Harness quick facts" · the
enable-path and MarsDebug sections) — read them before handing a single
console line; they are hard-won and several are the opposite of what you
would guess. The three that must bind before you have read anything:
- **ONE command per line**, never a trailing `--` comment (multi-line pastes
  silently concatenate; comments splice and kill the compile).
- **Readings come from the LOG FILE, not the screen**, with `nil` made
  visible (`tostring` inside a labelled `print_format`).
- Commits: `git commit -F <file>` (no embedded double quotes), project author
  config per `WORKFLOW.md`, parse-sweep any Lua change first, push the fix
  pack (TestKit is local-only).

## Read first, from `C:\Dev\SMR-BugFixPack` (file granularity — WORKFLOW element 8)

1. `docs/agent/STATE.md` — state, gates, counts (`CLAUDE.md` points here).
2. `docs/agent/facts/INDEX.md` — scan the one-line rows so you know what
   exists (several behaviours are the opposite of what code suggests), then
   open ONLY the fact files the sitting's tests touch — reading every fact
   file re-spends what the restructure saved.
3. `docs/PLAYTEST_CHECKLIST.md` (tests + protocol) with
   `docs/PLAYTEST_HELP.md` (ground rules BEFORE handing any console line).
4. `docs/agent/bugs/INDEX.md` → the `<ID>.md` entries the sitting touches
   (the row answers status/priority; the entry has the narrative).
5. `docs/agent/FIX_POLICY.md` — §4a, §3a, §2 binding for any code written.
6. `docs/agent/reports/REACHABILITY_AUDIT.md` "Challenge review" — before
   writing ANY new fix: tier vocabulary, hard tells, injection-evidence rule.

**End of session:** update `agent/STATE.md`. **STATE.md is hard-capped at 60
lines (doccheck red), so adding means evicting** (`WORKFLOW.md` mechanical
rule 8): move resolved or superseded lines to `docs/archive/SESSION_LOG.md` —
append-only, newest-first — in the same commit; never evict open gates, holds,
owner decisions or the counts block. Route any lesson per the logbook rule at
the top. Then commit, push, summarize. Work too big for the sitting was FILED
as you went (job 3) — say where.
