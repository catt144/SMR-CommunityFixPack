# Opus build-session prompt — wave 4

Paste everything below into a fresh Claude Code session (Opus) for the wave-4
implementation leg. (Wave-1/2/3 versions of this prompt are in git history.)

---

Continue the Surviving Mars: Relaunched "Community Fix Pack" mod — you are doing
the implementation leg, **wave 4**. State of the world: 47 tracked defects are
implemented across 46 registered modules, ALL probe-verified in-game by a clean
A/B pair (2026-07-25); F10 is retired (premise falsified); F32/F62/F63 are closed
`wontfix`; every tracker decision is made. Your job is the wave-4 `todo` queue:
sketches → fix files, carefully and mechanically.

## ⚠️ CONCURRENCY RULE — the user may be PLAYTESTING while you work

The game loads the mod from junctions that point at the main working trees
(`C:\Dev\SMR-BugFixPack`, `C:\Dev\SMR-BugFixPack-TestKit`). Mod code is read once
at game boot, so a mid-session edit is invisible — but the user relaunches the
game between playtest items, and they must keep getting the VERIFIED main state,
not your work in progress. Therefore:

1. **First action of the session** — create worktrees and do ALL work there:
   ```
   git -C C:\Dev\SMR-BugFixPack worktree add C:\Dev\SMR-BugFixPack-wave4 -b wave4
   git -C C:\Dev\SMR-BugFixPack-TestKit worktree add C:\Dev\SMR-BugFixPack-TestKit-wave4 -b wave4
   ```
2. **Never edit anything under `C:\Dev\SMR-BugFixPack` or
   `C:\Dev\SMR-BugFixPack-TestKit` directly** (docs included). Every file you
   touch lives in the `-wave4` directories.
3. Commit to the `wave4` branch. **Do NOT merge to main, do NOT push main.**
   At session end push the fix pack's branch (`git push origin wave4`) as a
   backup; the TestKit is local-only by design (no remote — just commit).
4. Do NOT launch the game, and do NOT touch `%AppData%`. The A/B verification of
   your work happens in the QA leg (`docs/FABLE_QA_PROMPT.md`), which also
   performs the merge to main after the user's playtest.

**First, read these (in order) from the `-wave4` worktree:**
1. `docs\STATUS.md` — snapshot, the wave-4 queue, and the hard-won engine facts
   (read the WHOLE facts list — several were learned the hard way, and three are
   NEW from the wave-3 QA session, see below)
2. `docs\FIX_POLICY.md` — HOW to patch (binding rules)
3. `docs\BUGS.md` — the tracker; every fix you write references its entry
4. `docs\TESTING.md` + the Test Kit worktree (probe conventions in
   `Code\00_TestCore.lua`; wave-3 probes in `Code\30_Probes_Wave3.lua` as
   templates; autorun harness `Code\95_AutoRun.lua` — you do NOT run the game)
Then skim two fix files as templates — `Code\Fix_TrainCargoDumping.lua` (full
replacement) and `Code\Fix_DustSicknessBiorobots.lua` (preset data patch, incl.
DataLoaded/DataChanged timing).
The game's Lua source (read-only, NEVER modify) is at
`A:\SteamLibrary\steamapps\common\Project Spark\ModTools\Src`.

**Your work queue, in order** (STATUS.md "Next up", largest player impact first):
1. **F56** Auto RC Transports never offload rockets (P2, high) — completes the
   F50/F68/F71 rocket-logistics family.
2. **F65/F66** station↔tunnel power bridge and connector hex ping-pong (P2,
   med+) — the "tracks won't connect" family, and the last big train items.
3. **F22** `GetGridGlobalStorage` breaking Last Transmission gates (P2, med).
4. **F19/F20/F21** the numbers/tooltip trio (P2) — small, self-contained.
5. **F23/F24/F27/F28/F29** the latent / mod-facing bundle (P3) — cheap, ships
   for modder benefit.
6. **F42/F43/F47/F49/F57/F31/F18/F25/F26** the remaining P2/P3 tail.

**Do NOT touch:** F10 (retired, pending PT-36), F48 (gated on PT-37), D02
(gated on PT-38 — do not build it even though the design is written), the
`Opt_*` modules, or anything marked `wontfix`/`tested`.

**F10 lesson — screen every entry before implementing:** F10's "crash" turned
out not to exist because **this engine tolerates `pairs(nil)`** (proven
empirically in the wave-3 A/B baseline), same as `next(nil)`/`ipairs(false)`.
If a wave-4 entry's defect claim is a nil-ITERATION crash, it is wrong — verify
an actual raise (indexing a nil VALUE does still raise, cf. F33) or flag the
entry as a wontfix candidate with a note instead of writing a no-op fix.

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
   keep the commented-out F10 line exactly as it is).
4. Same pass: write the probe in a NEW `Code\40_Probes_Wave4.lua` in the Test
   Kit worktree (register it in the Test Kit's `metadata.lua`). Probes must
   assert on the MECHANISM (was the guard hit, did the filter run), not just a
   return value — a probe that can pass in both A/B halves is not evidence.
5. Same commit: BUGS.md index status → `fixed` (+ tag on the heading),
   player-language line in README's fix table and MOD_DESCRIPTION.md. If the
   fix has an aspect probes cannot verify, append a PT entry to
   `docs\PLAYTEST_CHECKLIST.md` continuing from **PT-39** in a new "Group 8 —
   wave-4 fixes" section.
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
- **`error()`/`assert()` do NOT unwind mod code** — the engine prints and
  execution CONTINUES. Never use them for control flow; drop copied `assert`
  lines and say so in the header.
- **This engine tolerates `pairs(nil)`/`next(nil)`/`ipairs(false)`** — do not
  report or fix nil-iteration as a crash (the F10 lesson). Boolean relational
  compares DO raise; indexing a nil value DOES raise.
- **`ModLog` messages must have `%` escaped** if pre-formatted: ModMessage skips
  formatting with no varargs, but the ModPrint output path is printf-style and
  formats AGAIN (Mod.lua:109-113, lib.lua:164-174). Use the pack's `log()`
  helpers (00_Core.lua / 90_SaveSanitizer.lua) — they already escape; do not
  hand-roll ModLog calls with raw `%`.
- **Savegame repair passes hook `OnMsg.PostLoadGame`, not LoadGame**:
  `Msg("LoadGame")` fires BEFORE `FixupSavegame` (Savegame.lua:810-813), so a
  LoadGame-time pass races the shipped fixups (this baked a +200% double-buff
  in F35 before the QA audit caught it). Existing per-fix LoadGame passes that
  do not compensate for a shipped fixup are fine as they are.
- Mod code loads BEFORE classes are flattened: apply() self-checks must look up
  methods on their DECLARING class. Property defaults are not on the class yet
  either.
- **Presets do not exist when mod code loads.** Data patches run from
  `OnMsg.DataLoaded` (+ `OnMsg.DataChanged` for editor reloads).
- `g_Consts` and other GameVars are read inside patched functions only; `const`
  is fine at apply time. `/` truncates (integer division). A post-wrapper on a
  command method (SetCommand-reached) never runs — pre-wrap.
- `Random`, `Max`, `Min`, `MulDivRound`, `empty_table`, `table.remove_entry`,
  `table.find(list, field, value)` are engine globals. Verify any API by
  grepping `ModTools\Src` — never guess names.
- `IsValid()` rejects the plain tables probes use as stand-ins — keep it out of
  hot paths or have the probe swap it via `WithGlobals`.
- Never modify anything under the game directory. No balance changes, no
  refactors beyond the verified defect. Do NOT mark anything `tested` — that
  status is earned only by the human playtest.
- If a fix sketch doesn't survive contact with the real code, do NOT improvise
  a redesign: mark `blocked` with what you found and continue the queue.

**End of session:** update STATUS.md (in the worktree — implemented list, queue
position, anything blocked), commit, push the `wave4` branch, and give a table
of fixes completed / blocked / remaining. The Fable QA leg
(`docs/FABLE_QA_PROMPT.md`) merges to main and runs the A/B pair after the
user's playtest — **leave main and the game alone.**
