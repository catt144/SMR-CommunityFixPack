# Chain — unattended-2 (the decision-drive build batch; 2 prompts, self-consuming)

**Why this chain exists.** Owner orders from the 2026-08-10/11 decision drive
(SESSION_LOG rounds 1–5), authored the same night at peak knowledge: **build
what was decided and verify all of it in one launch.** Four items:

1. **F48 — SHIP** (owner, 2026-08-11): the corrected station-connector pass
   joins the sanitizer. `blocked` → `directed`; this chain makes it `fixed`
   honestly or reports why not.
2. **C43 — option 2** (owner): `set_global` restricted to names that already
   exist; probes with undeclared stub targets SKIP with a stated reason.
   TestKit-only.
3. **F100 — reason-string fix ONLY** (owner, hold lifted): the boot log's
   false `inactive (…game update…)` line states the recorded truth instead.
4. **PT-35 leg A re-run** — the turbine half, UNSAMPLED since 2026-08-04,
   unblocked by **`PT35FIXTURE.savegame.sav`** (verified on disk 2026-08-10;
   contents on F35.md: FrictionlessComposites researched, ONE Large Wind
   Turbine working, Remote Medic on a Hospital for the F03 half).

One launch verifies all four: the sanitizer (with the new F48 pass) runs its
do-no-harm reads on the fixture, the suite run proves C43's silence, the boot
log proves F100's new line. **This folder must be EMPTY when prompt 2
finishes.** Model placement lives in the filenames; bodies are model-neutral.

## Manifest

| # | file | owner needed? | what it does |
|---|------|---------------|--------------|
| 1 | `01_OPUS_RUN.md` | **No** — fully unattended | re-derive each item from its entry · build the three changes · stage the F48 case-A state · launch, load the fixture, take every read with its R4 round trip · record incrementally, archive logs, outbox |
| 2 | `02_FABLE_AUDIT.md` | No (routes decisions) | adversarial audit vs the archived logs · R4/R7 enforcement · integration · folder empty · owner report + next kickoff |

## Binding chain rules

1. **Staleness check first, every prompt**: `git log --oneline -10` + `git pull`.
2. **Inbox/outbox in writing.** Each prompt appends its handoff to the next
   prompt's `## Notes from upstream`, commits, deletes its own file in the
   same commit. Folder emptiness is prompt 2's done-condition.
3. **Route, don't drop**; unsure who owns a discovery → STOP AND ASK.
4. **Self-split at a clean commit boundary** if context runs short — results
   are banked incrementally, so a split loses nothing.
5. **Drift-evidence capture** — disagreements with the record are corrected
   visibly, never silently. ⛔ **Recorded facts are claims**: re-derive each
   item's ROUTE from its entry + source before building (the decision blocks
   summarize; they do not substitute for the read).
6. **WORKFLOW binds in full**, including the Co-runs harness rules
   (unattended-1's 1–4, batch-1's 1–6, batch-2's 1–9) and the two rules the
   owner adopted 2026-08-11: **R4** — every state-transition claim carries a
   save/reload ROUND-TRIP step, taken and read, or says PRE-RELOAD ONLY;
   **R7** — every verdict evidences its EFFECT, not its execution.
7. **FIX_POLICY §3a**: all game runs on staged COPIES. ⛔ **TWO protected
   files**: `TEST2H TRAIN.savegame.sav` (MD5 `103B320A1434513BC8773553096A8958`,
   mtime 2026-08-03 22:21:48 — verify unchanged at close-out) and
   **`PT35FIXTURE.savegame.sav` — a STANDING FIXTURE, load a COPY of it, and
   it SURVIVES this chain** (it also serves future PT-35 cases). Every other
   staged/throwaway save dies in the recording commit, and **close-out LISTS
   the save directory against the expected survivors** (standing rule).
8. **Probe hygiene binds unchanged** — sources authored as text in the run
   prompt or resurrected from git (batch-2's parked instruments survive at
   `7110384`, batch-1's at `530df63`, unattended-1's via
   `git log --all --oneline -- docs/agent/prompts/unattended-1/`); files in
   `Code/` only while the run happens; C11 + its piping corollary; **ARM GATE
   before every launch**; `PROBE SWEEP:` line in every result commit; R8
   `git add -f` for every cited log.
9. **doccheck green before every doc commit**; STATE 60-line cap; commits via
   `git commit -F <file>`; parse sweep before any commit touching Lua; push.
   PS 5.1 hazards: no-BOM UTF-8 via `[System.IO.File]`; `.ps1` needs a BOM.
10. **⛔ NO ASSUMED CAPABILITY.** Every never-run call follows first-execution
    discipline (`pcall` printed, liveness witness). Known-good primitives and
    their CURRENT witnesses: in-run SAVE (witness = on-disk bytes + load-back,
    **never `ListForTag`** — EF-049), staged-copy load by FILENAME, speed
    set/read-back. ⛔ Mid-session log reads are PRESENCE-only (EF-047);
    absence verdicts come from the final archived log. ⛔ `== true` is a
    reader defect (EF-048) — test truthiness/type.
11. **⛔ The forced-vs-organic rule**: every finding names what was forced.
    Everything this chain runs is FORCED/staged — no organic claims, no
    `tested` grants anywhere.
12. **⛔ ANTI-SPRAWL.** Results land on entries, the checklist, SESSION_LOG,
    STATE. No new standing document or document class.
13. **Src IS on this machine** (EF-014):
    `A:\SteamLibrary\steamapps\common\Project Spark\ModTools\Src` — the
    installdir is literally `Project Spark`. Src-verify every line number the
    builds rely on; mark anything trust-carried.
14. **⭐ Kickoff + next-chain handoff.** Prompt 2's owner report ENDS with the
    next kickoff line (source: STATE's NEXT — the PT-20 redo co-run is the
    expected front; if its chain is unauthored, say so plainly).

## Scope fence — the whole chain

**In:** the four items above; their verification; recording + integration;
the whole-log review (grep every log for `TrackElement.lua:805` — F99 passive
watch — and `invalid pos with no holder` — C45).
**Out:** the PT-20 redo co-run (attended, next chain); the Ctrl-F9/F85 check
(attended, rides PT-20); PT-35 cases B/C (parked); any module conversion
(F46's group-B row is a recorded question, not work); anything the decision
drive closed; changing any owner decision.

## Stop conditions (chain-wide)

- The F48 build fails its own acceptance (the staged case-A state is not
  repaired, or ANY do-no-harm read drifts) → **do not ship**: revert the
  module edit in the same session, record the readings on F48.md, route to
  the owner. The other three items proceed independently.
- Any `[LUA ERROR]` naming pack code in any window → stop that item, record
  verbatim, continue with independent items.
- `PT35FIXTURE.savegame.sav` missing or failing its content reads at confirm
  time → PT-35 leg A becomes `SKIP <fixture broken — say what read wrong>`;
  the three builds still run (they need no fixture).
- Context runs short → self-split at a clean commit boundary (rule 4).
