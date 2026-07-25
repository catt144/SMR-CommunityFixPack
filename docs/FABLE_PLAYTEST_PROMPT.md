# Fable playtest-report prompt

Paste everything below into a fresh Claude Code session (Fable) when the user
reports manual playtest results (`docs/PLAYTEST_CHECKLIST.md`, PT-01..PT-38).
Partial reports are fine — process what was reported, leave the rest untouched.

---

You are processing the user's **manual playtest report** for the Surviving Mars:
Relaunched "Community Fix Pack". The playtest is the ONLY thing that turns a
fix's status from `fixed` (probe-verified) into `tested` (ships in the release
text), and three checklist items are decision gates that trigger real work.

**First, read (in order) from `C:\Dev\SMR-BugFixPack`:**
1. `docs\STATUS.md` — snapshot + the WHOLE engine-facts list
2. `docs\PLAYTEST_CHECKLIST.md` — the tests, which fixes each covers, and the
   "Reporting protocol" section at the end
3. `docs\BUGS.md` — the tracker you will be updating
4. `docs\FIX_POLICY.md` — binding rules for any code you end up writing

Game source (read-only): `A:\SteamLibrary\steamapps\common\Project Spark\ModTools\Src`.
The user's results arrive in their message — ask for the PT number, PASS/FAIL,
and their notes if anything is ambiguous. Trust their observations over the
tracker's predictions; when a result contradicts an entry, the save is right.

## Standard processing, per reported result

- **PASS** → for each fix the PT covers (named in its heading), flip the
  BUGS.md index row AND the entry heading tag to `tested`. A PT that covers
  only half a fix (e.g. one case of two) flips nothing until both cases pass —
  note the partial on the entry instead.
- **FAIL** → file a NEW finding (next free F## — check the index; F74 was next
  as of 2026-07-26) with the user's notes verbatim, then investigate: read the
  fix + the shipped code and record a diagnosis with file:line evidence on the
  new entry. Do NOT redesign the fix in place — diagnosis first, put anything
  non-mechanical in front of the user. The covered fix's status goes back from
  `fixed` to `broken (F##)` in the index.
- **SKIP / not run** → leave everything untouched.
- Keep `README.md` / `docs/MOD_DESCRIPTION.md` fix lists in sync only insofar
  as a FAIL removes a claim; the tested-only shipping sync happens at release.

## The decision gates (these trigger work, not just status flips)

- **PT-36 (F10 retirement)** — PASS: delete `Code/Fix_FactionFundingCheck.lua`,
  delete the commented-out line in `metadata.lua`, flip F10 to `wontfix` (heading
  + index), retire the `FactionFundingCheck` probe from the TestKit (delete the
  registration; note it in 10_Probes_Wave1.lua's header), record the close on
  the entry. FAIL (a real error on a real save): re-add the metadata line,
  reopen the entry with the user's error text, and flag loudly — it would mean
  the engine's `pairs(nil)` tolerance is conditional, which invalidates an
  engine fact; STATUS must be corrected.
- **PT-37 (F48 unblock)** — PASS on both cases: implement the corrected
  connector pass in `Code/90_SaveSanitizer.lua` behind a one-shot
  `SMRFixPack_*` flag on UIColony, SKIPPING tracks that carry repair sites;
  probe it; BUGS F48 → `fixed`; run one `-smrautorun` verification leg (the
  procedure is in STATUS's "QA session (wave 3)" section). Dirty FAIL on case
  B: close F48 `wontfix — repair riskier than the defect` with the user's
  record of what broke.
- **PT-38 (D02 cadence)** — expected result (~2-real-minute re-nag, second
  breakage hidden in window): record the measured intervals on the D02 entry
  and mark it ready for the next build leg. Surprise results: follow the
  branches written in PT-38 itself (module unnecessary → close D02; seconds-
  scale return → re-read the F32 close).
- **PT-17 case B / PT-32 (the F68/F71 capacity edge)** — this is the one
  suspected REAL failure. If the lander sticks at "loading": new finding with
  the export pair / hold contents / status text, diagnose (the requested floor
  not debiting remaining capacity, see the F68 entry), and design the repair
  (cap the floor against remaining hold) for the user to approve — do not land
  it unreviewed.
- **PT-10 (F55 open question)** — record the observation on the F55 entry
  either way; if drones DO enter through an opened roof, the entity-data
  hypothesis is confirmed and the entry closes as not-Lua-fixable.
- **PT-20 (uninstall safety)** — a FAIL here is a STOP-SHIP P0: identify which
  fix's savegame footprint broke the vanilla load (FIX_POLICY §3 lists the
  four persisted keys) and fix pack-side before anything else happens.
- **PT-35 case C** — only runs with a donated pre-patch save; a PASS here plus
  case A/B flips the SaveSanitizer heading to `tested`.

## If the user also ran the MarsDebug.exe pair

Diff its two logs the same way as a normal pair (STATUS has the procedure).
The 10 `[install]` probes and F73's Idle-wrapper half stop SKIPping there —
FAIL→PASS flips count as probe verification (record in STATUS), but still not
`tested`.

## Coordination

The Opus wave-4 leg may have run concurrently on `wave4` branches (worktrees).
Do NOT merge them here — that is the wave-4 QA leg's Task 0
(`docs/FABLE_QA_PROMPT.md`). Commit playtest processing to `main`; the QA leg
merges on top of it, and tracker statuses from THIS session win over the build
leg's in any conflict.

## Hard rules

- Engine facts in STATUS.md apply to any code you write (sandbox; error() does
  not unwind; pairs(nil) tolerated; ModLog `%` escaping via the pack's log
  helpers; PostLoadGame for fixup-compensating passes; declaring-class
  self-checks; DataLoaded for presets).
- Parse-check any .lua you touch (python + luaparser, installed).
- One logical change per commit,
  `git -c user.name="SMR-BugFixPack" -c user.email="154917955+catt144@users.noreply.github.com"`,
  push `main` at session end.

**End of session:** update STATUS.md (playtest outcomes, statuses flipped, new
findings, gate dispositions), commit, push, and give the user a table: tested /
failed (with new F##s) / gates resolved / still awaiting play.
