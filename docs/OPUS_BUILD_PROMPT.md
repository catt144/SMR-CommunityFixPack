# Opus build-session prompt — wave 5

Paste everything below into a fresh Claude Code session (Opus) for the wave-5
implementation leg. (Wave-1/2/3/4 versions of this prompt are in git history.)

---

Continue the Surviving Mars: Relaunched "Community Fix Pack" mod — you are doing
the implementation leg, **wave 5**, finishing the tail the wave-4 leg did not
reach.

State of the world: **61 modules are registered** (59 `Fix_*`, the
`90_SaveSanitizer`, and the opt-in `Opt_ClassicRockets`; one `Fix_` line is
deliberately commented out — F10, retiring). Waves 1-3 are probe-verified in-game
by a clean A/B pair (2026-07-25) plus an attended MarsDebug `[install]` pass
(49 PASS / 0 FAIL). **Wave 4's 14 modules are written but have never been run** —
they sit on the `wave4` branch with 13 probes in the Test Kit's
`Code\40_Probes_Wave4.lua` and playtest items PT-39..PT-44. Every tracker decision
is made: F10 retiring, F32/F56/F62/F63 closed `wontfix`, F48 gated on PT-37, D01
half-shipped, D02 planned.

Your job is the **eight `todo` entries left in BUGS.md**: sketches → fix files,
carefully and mechanically.

## ⚠️ CONCURRENCY RULE — the user may be PLAYTESTING while you work

The game loads the mod from junctions that point at the main working trees
(`C:\Dev\SMR-BugFixPack`, `C:\Dev\SMR-BugFixPack-TestKit`). Mod code is read once
at game boot, so a mid-session edit is invisible — but the user relaunches the
game between playtest items, and they must keep getting the VERIFIED main state,
not your work in progress. Therefore:

1. **The worktrees already exist and are already on the right branch.** Do NOT
   create new ones and do NOT branch off main — wave 4 is unmerged, so `main`
   does not have the 14 modules you are about to build on top of. Verify and
   continue in place:
   ```
   git -C C:\Dev\SMR-BugFixPack-wave4 status
   git -C C:\Dev\SMR-BugFixPack-TestKit-wave4 status
   ```
   Both must be clean and on branch `wave4`. If either is missing, recreate it
   from the branch, NOT from main:
   ```
   git -C C:\Dev\SMR-BugFixPack worktree add C:\Dev\SMR-BugFixPack-wave4 wave4
   git -C C:\Dev\SMR-BugFixPack-TestKit worktree add C:\Dev\SMR-BugFixPack-TestKit-wave4 wave4
   ```
2. **Never edit anything under `C:\Dev\SMR-BugFixPack` or
   `C:\Dev\SMR-BugFixPack-TestKit` directly** (docs included). Every file you
   touch lives in the `-wave4` directories.
3. Keep committing to the `wave4` branch. **Do NOT merge to main, do NOT push
   main.** Push the fix pack's branch (`git push origin wave4`) at session end as
   a backup; the TestKit is local-only by design (no remote — just commit).
4. Do NOT launch the game, and do NOT touch `%AppData%`. The A/B verification of
   waves 4 AND 5 happens together in the QA leg (`docs/FABLE_QA_PROMPT.md`),
   which also performs the merge to main after the user's playtest.

**First, read these (in order) from the `-wave4` worktree:**
1. `docs\STATUS.md` — snapshot, the wave-4 results, the remaining queue, and the
   hard-won engine facts (read the WHOLE facts list — several were learned the
   hard way, and four are NEW from wave 4, including a tooling trap that mangled
   a doc file)
2. `docs\FIX_POLICY.md` — HOW to patch (binding rules)
3. `docs\BUGS.md` — the tracker; every fix you write references its entry
4. `docs\TESTING.md` + the Test Kit worktree (probe conventions in
   `Code\00_TestCore.lua`; **wave-4 probes in `Code\40_Probes_Wave4.lua` are the
   best templates** — they cover global swaps, preset reads, message dispatch and
   a metatable trick for observing an installed closure; autorun harness
   `Code\95_AutoRun.lua` — you do NOT run the game)
Then skim three wave-4 fix files as templates — `Code\Fix_TrainCargoDumping.lua`
(full replacement), `Code\Fix_LastTransmissionStorage.lua` (preset patch with
DataLoaded/DataChanged timing), and `Code\Fix_TrackTunnelPowerBridge.lua`
(additive OnMsg + a PostLoadGame repair sweep).
The game's Lua source (read-only, NEVER modify) is at
`A:\SteamLibrary\steamapps\common\Project Spark\ModTools\Src`.

**Your work queue, in order** (STATUS.md "Still `todo` after wave 4", largest
player impact first):
1. **F47** Track salvage refunds ~1 hex for a whole track, 0 for a partial
   (P3, high) — completes the F44/F45 track-salvage family.
2. **F42** Buildings placeable on active dust devils (P3, high) and
   **F43** Layout construction bypasses tech locks (P3, high) — the two
   placement-rule bypasses.
3. **F49** Train minors bundle (P3, med) — several small items, screen each.
4. **F57** Drone/transport minors bundle (P3, med) — three items, one of which
   (b) is a nil-iteration-flavoured claim: apply the F10 screen below before
   writing it.
5. **F31** Anomaly cave-in hardcodes UndergroundMap (P2, med).
6. **F25** Tech description names wrong building (P3, pre-1.0.6 saves only) and
   **F26** Bombardment missiles fly parallel (P3, cosmetic) — cheapest, last.

**Do NOT touch:** F10 (retired, pending PT-36), F48 (gated on PT-37), D02
(gated on PT-38 — do not build it even though the design is written), D01's
unwritten export half (needs a design decision, and **F56's closed auto-offload
rides in the same module when it does** — never create a standalone
`Opt_AutoRocketOffload`), the `Opt_*` modules, or anything marked
`wontfix`/`tested`.

**Screen every entry before implementing — wave 4 changed two verdicts this way.**
* **The F10 lesson:** this engine tolerates `pairs(nil)`/`next(nil)`/`ipairs(false)`
  (proven empirically). If an entry's defect claim is a nil-ITERATION crash, it is
  wrong — verify an actual raise (indexing a nil VALUE does still raise, cf. F33)
  or flag the entry as a wontfix candidate with a note instead of writing a no-op
  fix. Wave 4 applied this to F28 and corrected the entry's title rather than
  claiming a crash it had not observed.
* **The F56 lesson:** ask whether the cited code is a DEFECT or a maintained
  design decision before you fix it. F56's "missing" behaviour turned out to be a
  declared, overridable accessor plus an exclusion a Relaunched developer had
  consciously re-stated through a compatibility shim — a feature request, not a
  repair (FIX_POLICY §4). It closed `wontfix`. Signals to weigh: is the omission
  named and overridable? was the guard updated for Relaunched? does any shipped
  text promise the behaviour? do siblings in the same file do it the other way?
* **Screening pays.** Both wave-4 screens uncovered REAL defects nobody had
  tracked — F74 (a class guard never converted to the Relaunched rocket classes)
  and F75 (six faction conditions wired to a property nothing reads). If you find
  one, file it as a new F## entry with full evidence and fix it there rather than
  bending an existing entry to fit.

**Per-fix procedure (do not deviate):**
1. Open the BUGS.md entry. Then READ the actual current function(s) in
   `ModTools\Src` at the cited file:line — never write a fix from the tracker
   description alone. If the code doesn't match the entry, set the entry's
   status to `blocked` with a one-line note and move on. If it matches but the
   *sketch* is wrong, implement what the code justifies and record the
   divergence as an "*Implemented differently, on better evidence:*" paragraph.
2. Write `Code\Fix_<Name>.lua` registered via
   `SMRFixPack.Register("<Name>", { title = ..., apply = function() ... end })`.
   - Prefer (in order): data/preset patch → additive OnMsg → registry/table
     surgery → chained wrapper capturing the original → full replacement.
   - Full replacements copy the shipped body byte-identical except lines marked
     `-- FIX:`; header comment cites source file + lines.
   - `apply` must self-check its target exists/looks broken and
     `return "<reason>"` to deactivate gracefully. Never error, never assume.
3. Add the file to `metadata.lua`'s `code` list (order matters: 00_Core first;
   `90_SaveSanitizer` stays near the end; keep the commented-out F10 line exactly
   as it is).
4. Same pass: write the probe in a NEW `Code\50_Probes_Wave5.lua` in the Test
   Kit worktree (register it in the Test Kit's `metadata.lua`, after
   `40_Probes_Wave4.lua`). Probes must assert on the MECHANISM (was the guard
   hit, did the filter run), not just a return value — a probe that can pass in
   both A/B halves is not evidence. If a fix genuinely cannot be probed, say so
   on the BUGS entry and cover it with a playtest item instead (wave 4's F24 is
   the precedent).
5. Same commit: BUGS.md index status → `fixed` (+ tag on the heading),
   player-language line in README's fix table and MOD_DESCRIPTION.md. If the
   fix has an aspect probes cannot verify, append a PT entry to
   `docs\PLAYTEST_CHECKLIST.md` continuing from **PT-45** in a new "Group 9 —
   wave-5 fixes" section.
6. Syntax-check everything you wrote: `python -m pip install --user luaparser`
   is already done on this machine; run a script over every changed .lua:
   `python -c "from luaparser import ast; import sys; ast.parse(open(sys.argv[1],encoding='utf-8-sig').read())" <file>`
7. Commit with `git -c user.name="SMR-BugFixPack"
   -c user.email="154917955+catt144@users.noreply.github.com"`,
   message: `Implement F## (<short name>)`. One fix per commit, on the `wave4`
   branch. Push the fix pack branch at session end.

**Hard rules — engine facts that shipped real bugs when violated:**
- **Mods run in a SANDBOX on all platforms**: no `debug`, no `io`, `os` is
  `{time}` only, no `Async*` file APIs, no load/dofile/require. `rawget(_G,"X")`
  works. New globals via plain assignment land in real `_G`; **never
  `rawset(_G, ...)`** (writes an invisible shadow).
- **Replacing an EXISTING global works too** — `ModEnvMeta.__newindex`
  (Mod.lua:1557-1563) rawsets any non-blacklisted key into the real `_G`, and the
  "attempt to create a new global" assert only fires for names that do not already
  exist. Generated closures (script conditions, sequence code) resolve names at
  call time, so they pick the replacement up. Read the name back with
  `rawget(_G, ...)` in apply() to prove the write landed (F22 does).
- **`OnMsg` is additive** — four shipped files each define
  `OnMsg.StationsConnected` and all four must run. A dead original handler can
  stay where it is (F23).
- **`error()`/`assert()` do NOT unwind mod code** — the engine prints and
  execution CONTINUES. Never use them for control flow; drop copied `assert`
  lines and say so in the header. Corollary learned in wave 4: a shipped
  `assert` that states an invariant does NOT enforce it — F66's ping-pong was
  exactly a violated assert the code then ignored, and enforcing the assert's own
  condition was the whole fix.
- **This engine tolerates `pairs(nil)`/`next(nil)`/`ipairs(false)`** — do not
  report or fix nil-iteration as a crash (the F10 lesson). Boolean relational
  compares DO raise; indexing a nil value DOES raise.
- **`ModLog` messages must have `%` escaped** if pre-formatted (Mod.lua:109-113,
  lib.lua:164-174). Use the pack's `log()` helpers (00_Core.lua /
  90_SaveSanitizer.lua) — they already escape; do not hand-roll ModLog calls with
  raw `%`.
- **Savegame repair passes hook `OnMsg.PostLoadGame`, not LoadGame**:
  `Msg("LoadGame")` fires BEFORE `FixupSavegame` (Savegame.lua:810-813), so a
  LoadGame-time pass races the shipped fixups. Existing per-fix LoadGame passes
  that do not compensate for a shipped fixup are fine as they are.
- Mod code loads BEFORE classes are flattened: apply() self-checks must look up
  methods on their DECLARING class. Property defaults are not on the class yet
  either.
- **Presets do not exist when mod code loads.** Data patches run from
  `OnMsg.DataLoaded` (+ `OnMsg.DataChanged` for editor reloads).
- `g_Consts` and other GameVars are read inside patched functions only; `const`
  is fine at apply time. `/` truncates (integer division). A post-wrapper on a
  command method (SetCommand-reached) never runs — pre-wrap. A method that BLOCKS
  for the duration of an activity is just as unhookable from behind: F21 needed a
  full replacement because `BoardVehicle` does not return until the ride ends.
- `Random`, `Max`, `Min`, `MulDivRound`, `empty_table`, `table.remove_entry`,
  `table.find(list, field, value)` are engine globals. Verify any API by
  grepping `ModTools\Src` — never guess names.
- `IsValid()` rejects the plain tables probes use as stand-ins — keep it out of
  hot paths or have the probe swap it via `WithGlobals`.
- **TOOLING: never round-trip a doc through PowerShell 5.1 `Get-Content -Raw` +
  `WriteAllText`.** `Get-Content` without `-Encoding` decodes UTF-8 as cp1252, so
  every `—`, `↔`, `≤` comes back double-encoded and the whole file shows as
  changed. It happened to `BUGS.md` in wave 4 and had to be reversed. Use the
  editor's own file tools for docs, or pass `-Encoding UTF8` on BOTH ends.
- Never modify anything under the game directory. No balance changes, no
  refactors beyond the verified defect. Do NOT mark anything `tested` — that
  status is earned only by the human playtest.
- If a fix sketch doesn't survive contact with the real code, do NOT improvise
  a redesign: mark `blocked` with what you found and continue the queue.

**End of session:** update STATUS.md (in the worktree — implemented list, queue
position, anything blocked), commit, push the `wave4` branch, and give a table
of fixes completed / blocked / remaining. The Fable QA leg
(`docs/FABLE_QA_PROMPT.md`) merges to main and runs the A/B pair over waves 4 AND
5 together after the user's playtest — **leave main and the game alone.**
