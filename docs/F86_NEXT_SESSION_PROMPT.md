# One-off prompt — F86 Phase 0+1: the two measurements, then the Tier-1 spec

**Paste everything below into a fresh session. One-off: this file is DELETED
by the session that completes it** (WORKFLOW brief rule 6). Model-neutral.
The measurement half needs the OWNER AT THE KEYBOARD in the retail game;
the spec half is game-free — if the owner is not available, do Phase-1 items
that don't depend on probe results and leave the rest clearly marked.

---

You are continuing the Surviving Mars: Relaunched "Community Fix Pack"
(`C:\Dev\SMR-BugFixPack`, git). **F86 is the single release blocker; the
analysis is finished and twice-verified; your job is the first two phases of
`docs/F86_EXECUTION_PLAN.md`** — measure two engine facts, then finalise the
Tier-1 spec and write the build prompt.

**Start with `git log --oneline -10` + `git pull`.** Staleness check: this
prompt was written just after the prior-art survey commit (`b9acccb`) and the
plan/decision commit that follows it. If commits you don't recognise have
landed since, read them before acting.

## Read first (in this order — nothing else is required reading)

1. `docs/F86_EXECUTION_PLAN.md` — the plan; you are Phase 0 + Phase 1.
2. `docs/F86_ADJUDICATION.md` §4.1, §8.4-8.6 — why each measurement gates a
   design, and the hook-surface table.
3. `docs/FIX_POLICY.md` §3a (as amended: value-reachability + orphan reach +
   orphan gate) and `docs/ENGINE_FACTS.md` (the 2026-07-31 entries).
4. `docs/SAVE_SAFETY_REDESIGN.md` §6 — the authorised build you are speccing.

## Standing project rules (all of them binding)

- **Todo list before starting, one item per commit-and-verify unit, updated
  the moment each unit completes, exactly one in progress** — the owner reads
  it to decide when to step in (WORKFLOW brief rule 1).
- Console lines for the owner: **one command per line** — pasted multi-line
  blocks silently concatenate.
- **Never modify the game directory**; Src is read-only. TestKit edits are
  fine (that's where the probes live).
- Commit with
  `git -c user.name="SMR-BugFixPack" -c user.email="154917955+catt144@users.noreply.github.com"`,
  push after each unit; messages via `git commit -F <file>`, **no embedded
  double quotes** (PowerShell 5.1 splits them).
- Docs never lag findings: each probe result lands in ENGINE_FACTS in the same
  commit that records the log evidence.
- `ModLog` (never `print`) for anything that must reach the log file;
  `FlushLogFile()` before reading mid-session; `IsValidThread(x) or false`
  when displaying thread validity.

## Phase 0 — the two measurements (owner at keyboard)

### 0.0 ⛔ The stale-probe gate FIRST (HARD RULE, owner, 2026-08-01)

Run `grep -rln "TEMPORARY" Code/ ../SMR-BugFixPack-TestKit/Code/` and put the
result in your todo list before anything else. **Expected state for THIS
session: exactly two hits.**
- `97_SaveHookProbe.lua` — **declared**: it IS the 0.2 instrument. Keep.
- `99_OrphanEnvProbe.lua` — **STALE (answer recorded) and NOT inert**: it
  re-arms on every `LoadGame` and fires a loud `[LUA ERROR]` ~1 sol later —
  straight into the log 0.2 reads, and it parks a probe thread in any save
  made. **Delete it (+ its TestKit metadata/items lines) and commit BEFORE
  the owner launches the game.** This moves half of step 0.3 up front; 0.3
  then only tears down `97` after its result is recorded.
Any OTHER hit is undeclared: stop and repair before testing. Every result
commit this session carries the `PROBE SWEEP:` line. Full rule:
`WORKFLOW.md` "Probe hygiene".

### 0.1 GT-creation ordering — does `CreateGameTimeThread` run the body before the creating statement continues?

Hand the owner these, one per line, in a loaded colony (game UNPAUSED so game
time advances; a paused game may defer GT scheduling and mask the answer —
if the result looks like "deferred", re-run unpaused before recording):

```
CreateGameTimeThread(function() ModLog("SMRPROBE-GTORDER: thread body ran") end) ModLog("SMRPROBE-GTORDER: statement after create ran")
FlushLogFile()
```

(That is ONE console line — both calls on it — so the ordering of the two log
lines is the entire answer. If the console rejects the compound line, fall
back to a TestKit probe file that does the same at `OnMsg.LoadGame`.)

- body line FIRST → **run-at-creation**: the rains wrapper's naive shape is
  DEAD (its Msg posts before the vanilla loop can WaitMsg) — the spec takes
  the synchronous-heal branch; the F02 wrapper's defer-when-global-falsy
  guard is load-bearing.
- statement line FIRST → **deferred**: both authorised shapes work as
  written; the F02 guard stays anyway (defence in depth).
- Record the verdict + log filename in ENGINE_FACTS. **A test that cannot
  discriminate is worse than none** — if both lines appear in an order you
  can't trust (e.g. log interleaving doubt), say so and re-run; do not guess.

### 0.2 The autosave hook (probe already armed)

`SMR-BugFixPack-TestKit/Code/97_SaveHookProbe.lua` is live. The owner plays
~1 sol past an autosave (or forces one), quits to desktop, and you read the
newest log for `SaveGameStart`/`SaveGameDone` with `autosave=true`. Record in
ENGINE_FACTS (the entry currently says "same path, source-only" — upgrade or
correct it).

### 0.3 Teardown

Delete `97_SaveHookProbe.lua` AND `99_OrphanEnvProbe.lua` from the TestKit
plus their metadata/items lines, same commit as the recorded results. (The
orphan-env probe's result is already recorded — adjudication §8.1 — its file
is just still armed.)

## Phase 1 — spec and paperwork (game-free)

Per `F86_EXECUTION_PLAN.md` Phase 1, in this order:

1. Amend `SAVE_SAFETY_REDESIGN.md` §6.2 into the FINAL Tier-1 spec: the F02
   wrapper (thread-keyed, defer-on-falsy, +latched heal via GameVar version
   latch, +watchdog split) and the rains repair (shape per 0.1, +migration
   pass with version-stamped marker and id-less-entry handling). State each
   module's orphan-gate compliance explicitly.
2. Re-run the exposure enumeration over `Code/` with ALL FIVE assignment
   shapes (class-method / table-slot / global assignment / preset-field /
   own-thread); record the durable list + dispositions in the BUGS.md F86
   entry. Expected 13 — if you find a 14th, file it, don't fix it.
3. Read the faction-likes evaluation path in Src and close adjudication §4.4
   (`Fix_LastTransmissionStorage`'s `Condition.eval`) either way.
4. Write the **Tier-1 build prompt** (`F86_TIER1_BUILD_PROMPT.md`), compliant
   with WORKFLOW's six brief requirements, carrying: the final spec, the
   orphan-gate rule, the StormWedgeHeal reorder, the F88 regression leg
   (load 3× inside a rolled interval), and the PT-20-method uninstall leg.

## Scope fence

- **In:** the two measurements, ENGINE_FACTS updates, probe teardown, the
  Tier-1 spec amendment, the enumeration re-run, §4.4, the build prompt.
- **Out:** ANY `Code/` change beyond deleting the two probe files from the
  TESTKIT repo (the pack's `Code/` is untouchable this session); layer 1;
  the cleaner mod (Phase 5); D06/D10/D12.
- Anything interesting found out of scope: **file it, do not fix it.**

## Stop conditions (reporting beats pushing through)

- 0.1 refuses to discriminate after two attempts → record "unresolved", spec
  the rains repair as the synchronous heal (the shape that needs no ordering
  guarantee), and say so.
- The enumeration finds a 14th exposed module that is NOT layer-2 compliant →
  stop after filing; the build spec may need re-scoping and that is the
  owner's call.
- The owner is unavailable for Phase 0 → do Phase-1 items 2-3, mark 1 and 4
  blocked on the probe, and stop.

## What may NOT be claimed

- Do not label anything MEASURED without a log filename + line you read this
  session. Do not label anything RE-VERIFIED whose chain includes an
  inherited recorded fact you did not re-derive (the round-2 lesson —
  ENGINE_FACTS itself has been wrong twice this week).
- The Tier-1 spec may not claim save-cleanliness for existing saves without
  naming the mechanism that clears them (the latched heal / migration), and
  may not claim it for layer-2 residue at all (inert, accepted, disclosed).

## On completion

Delete THIS file in the final commit. The Tier-1 build prompt you wrote is
the next handover; `FABLE_NEXT_PROMPT.md`'s F86 banner should point to it.
