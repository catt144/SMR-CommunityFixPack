# Build the game-patch triage system

**One-off.** The commit that lands the result deletes this file and its row in `prompts/README.md`.
Start: `git pull`; `git log -1 --format=%h -- docs/agent/prompts/GAME_PATCH_BUILD_high.md` is the
authoring sha; an empty `git diff --stat <sha>..HEAD -- tools/ Code/ docs/agent/reports/GAME_PATCH_INSTRUMENTS.md`
means the facts below hold. Put the work list in your todo tool before the first write, one item per
commit, and mark each as it lands.

## Decided (owner, 2026-09-18/19): not yours to reopen

The design is `docs/agent/reports/GAME_PATCH_INSTRUMENTS.md` (`a54b72b`). The coordinator re-ran its
backtest cold and it reproduces exactly. One correction: on the reverification's own class-c list
(F-1/2/3/5) the `Require` hash catches 3 of 4; the true sentence is "every FIX row the pinned body
misses (F-1, F-2, F-4, F-5), the `Require` hash catches". The owner ruled on its §6:

1. **Verdict limits:** scoped at ≤ 12 flagged modules, full above that or above 1,000 changed hand
   declarations. These are budget defaults, not measurements. The perma prompt records each run's
   counts and has the limits revisited after the first real patch.
2. **Unattended suite A/B (G3)** runs on scoped/full only; on none, the boot census at the next sitting.
3. **No fire-rate counters (G4)** now. No `Code/` edits in this build.
4. **Dependencies are harvested (D1), never stamped.** It also serves the opt-in pack, which has no stamps.
5. **Patch notes are fetched by the tool** and can only escalate: they may add modules to the read
   list or raise the verdict, with a stated reason, and never drop a module or lower a verdict.
   (1.1.0's notes named none of the ten breakages.)
6. **Runs in the fix pack first; the opt-in pack gets an outbox entry in the fork** (`6f421fd`,
   report §5 step 8).

The first real run is expected to be a 1.1.1 hotfix. That is the small-patch regime, where the limits
have only a synthetic control behind them. The installed game today is Steam `24995074` =
`1.1.0.403908`, already archived (`C:\Dev\SMR-SrcArchive\README.md`).

## End state

1. **`tools/patchcheck.py`**: the report's D4 runner with D1, D2 (incompatible ranked above
   prefix-compatible), D3, D5, fpk parity, T, B, the notes fetch and the §2 verdict. It emits one
   block and every count in it; no count is ever typed by hand. It takes the archived old tree, a new
   tree (default: the live install) and `--code` (default `Code/`, also run against
   `C:\Dev\SMR-OptInPack\Code`). Modules pinning an anonymous callback are flagged whenever their
   file changes (report §3.3). A failed notes fetch prints `notes: not fetched` and the run goes on.
2. **Its regression test, kept in the repo and runnable by one command**, on the pre-patch pack
   (`git archive f7bd288 Code`) over 1.0.7 → 1.1.0: the per-column counts for PIN, REQ, SIGCALL, CITE
   and D1 equal the report's §3.1 table; identity overlay 0/80; the one-file `Residence.lua` overlay
   flags exactly `StaleReservations` and `FreedHousingNotice`; D2 finds `ArrivalDeaths`/`ChooseDome`
   (F117). Make it fail once on purpose, for example by dropping the `Require` column, before you trust a pass.
3. **First real output:** run it on today's `Code/` over 1.0.7 → 1.1.0 and read each D2 hit that no
   record already covers; `DustSicknessBiorobots` → `Affect` is the known unread one. A defect is filed
   (`smr-bug-library`), not fixed. Today's pack over 1.1.0 → 1.1.0 must say **none**.
4. **`docs/agent/prompts/perma/GAME_PATCH_PROMPT.md`**, a job prompt with rails, from the report's §5
   sketch as amended by the rulings above. Its steps: archive → `patchcheck` → D3 rows first → act per
   verdict → notes (escalation only) → in-game legs by verdict → FIX/REMOVE prompts → the outbox entry.
   Keep the drop order. A per-step token line goes in its todo list, and a limits-review line after the run.
5. **The fork's outbox:** `C:\Dev\SMR-OptInPack\docs\agent\prompts\perma\gamepatch\README.md` plus a
   `done/` folder, with the entry format of report §5 step 8.
6. **PROMPT MAP rows in both repos**, and a `TOOL CATALOG` entry for the new script. Correct the "6 of
   the 10 FIX rows" sentence at `WORKFLOW.md:97-98` and `tools/bodycheck.py:94-95` (report §0.1).
   `python tools/doccheck.py` GREEN in both repos.

If budget runs out, drop in this order: the D5 list, then B, then parity. Never drop D1–D3, the
regression test or the outbox.

## Your call

The prototypes in `.claude/gamepatch_scratch/` (`backtest.py`, `w42.py`, `facts_cite.py`,
`backtest_rows.tsv`; the pickled index is not kept, a cold run is about 50 s) are starting material,
not a spec. Choose the module split, whether the regression test is a flag or its own script, how
notes map to modules, and whether `SMRFixPack.ListFixes()` at autorun quit (report §1, 3 lines) is
worth adding to the kit. Where you depart from the report, say so in the commit message with the reason.
Your report lists departures and suggestions.

## Scope

In: the six items above. Out: `Code/` modules, the G3 recall boot (§3.4), G4, `STANDDOWN_AUDIT.md`,
and any mod content in the fork. An out-of-scope finding goes in your report.

## Stops

Report instead of pushing on if: the built tool does not reproduce §3.1 and the cause is not in your
code · a fork file you must write is dirty or held by a running seat there · a new game build lands mid-build.

## Do not claim

That the limits are validated, or that the scoped regime works: there is one synthetic control. Write
"reproduces the 1.1.0 backtest; the small-patch regime is uncalibrated until the first real patch".
