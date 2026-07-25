# Opus build-session prompt — wave 3

Paste everything below into a fresh Claude Code session (Opus) to continue the
implementation leg. (The wave-2 version of this prompt is in git history.)

---

Continue the Surviving Mars: Relaunched "Community Fix Pack" mod — you are doing
the implementation leg, wave 3. Discovery is complete; 30 fixes are implemented
and probe-verified in-game (19/19 automated A/B pass). Your job is to extend the
pack through the P2/P3 backlog the same disciplined way: sketches → fix files,
carefully and mechanically.

**First, read these (in order) from `C:\Dev\SMR-BugFixPack`:**
1. `docs\STATUS.md` — snapshot, final A/B results, and the hard-won engine
   facts (read the WHOLE facts list — several were learned the hard way)
2. `docs\FIX_POLICY.md` — HOW to patch (binding rules)
3. `docs\BUGS.md` — the tracker; every fix you write references its entry
4. `docs\TESTING.md` + the Test Kit repo `C:\Dev\SMR-BugFixPack-TestKit`
   (probe conventions in `Code\00_TestCore.lua`; autorun harness in
   `Code\95_AutoRun.lua` — you do NOT run the game)
The game's Lua source (read-only, NEVER modify) is at
`A:\SteamLibrary\steamapps\common\Project Spark\ModTools\Src`.

**Your work queue, in order:**
0. Docs warm-up: add the missing `[fixed: Code/Fix_*.lua]` tags to the wave-1
   detail headings in BUGS.md (F04, F05, F07, F08, F10, F15, F64) so headings
   and index agree.
1. Implement fixes one at a time, each with its Test Kit probe in the same pass:
   F46 (train cargo dumping), F36 (university overtraining), F38 (destroyed
   tunnels), F39 (second artificial sun), F40 (Dust Sickness on Biorobots),
   F41 (Gene Forging), F17 (Dust Sickness randomization), F35 (turbine buff
   sweep), F16 (Mirror Sphere), F70/F71/F72 (remaining lander issues), F54
   (switched-off shuttle hubs), F59/F60/F62/F63 (housing/service reach), F32
   (notification suppression), F33/F34 (landscape nil guards).
2. Then `Code/90_SaveSanitizer.lua` consolidating the remaining savegame sweeps
   (F03 leaked modifiers, F35 turbine buff, F48 connectors — see STATUS.md).
3. Then the D01 opt-in classic-rockets module (design note on the BUGS.md entry).
4. Test Kit side-task when passing: the F51 shuttle-cache probe PASSes even
   unfixed on a fresh colony — give it a scenario strict enough to discriminate.

**Per-fix procedure (do not deviate):**
1. Open the BUGS.md entry. Then READ the actual current function(s) in
   `ModTools\Src` at the cited file:line — never write a fix from the tracker
   description alone. If the code doesn't match the entry, set the entry's
   status to `blocked` with a one-line note and move to the next fix.
2. Write `Code\Fix_<Name>.lua` registered via
   `SMRFixPack.Register("<Name>", { title = ..., apply = function() ... end })`.
   Follow existing fix files as templates.
   - Prefer (in order): data/preset patch → additive OnMsg → registry/table
     surgery → chained wrapper capturing the original → full replacement.
   - Full replacements copy the shipped body byte-identical except lines marked
     `-- FIX:`; header comment cites source file + lines.
   - `apply` must self-check its target exists/looks broken and `return "<reason>"`
     to deactivate gracefully. Never error, never assume.
3. Add the file to `metadata.lua`'s `code` list (order matters: 00_Core first).
4. Same commit: BUGS.md index status → `fixed` (+ tag on the detail heading),
   player-language line in README's fix table and MOD_DESCRIPTION.md.
5. Commit with `git -c user.name="SMR-BugFixPack"
   -c user.email="154917955+catt144@users.noreply.github.com"`,
   message: `Implement F## (<short name>)`. One fix per commit. Push to origin
   (github.com/catt144/SMR-CommunityFixPack) at session end.

**Hard rules — including engine facts that shipped real bugs when violated:**
- **Mods run in a SANDBOX on all platforms** (unpacked dev mods too): no `debug`,
  no `io`, `os` is `{time}` only, no `Async*` file APIs, no load/dofile/require.
  `rawget(_G, "X")` works (safe wrapper). New globals you assign land in the
  real `_G` — but **`rawset(_G, k, v)` writes to an invisible shadow table:
  never rawset onto _G** (plain assignment instead; in the Test Kit use
  `SMRTest.SetGlobal`/`WithGlobals`).
- **`error()` does NOT unwind mod code** — the engine prints the error and
  execution CONTINUES with the next statement. Never use error/assert for
  control flow; return sentinel values (see 00_TestCore.lua's deferred verdicts).
- Mod code loads BEFORE classes are flattened: an inherited method reads nil on
  a subclass classdef — apply() self-checks must look up methods on their
  DECLARING class (F64 shipped broken this way once).
- `g_Consts` is a GameVar — read it inside patched functions only; `const` is
  fine at apply time. `/` truncates (integer division). A post-wrapper on any
  command method (SetCommand-reached, e.g. Colonist:Idle) never runs — pre-wrap.
- `Random`, `Max`, `Min`, `MulDivRound`, `empty_table`, `table.remove_entry`
  are engine globals. Verify any API you're unsure of by grepping `ModTools\Src`
  — never guess names.
- Never modify anything under the game directory. No balance changes, no
  refactors beyond the verified defect. Keep per-fix scope small.
- Do NOT mark anything `tested` — that status is earned only by the human
  playtest (`docs\PLAYTEST_CHECKLIST.md`). **If the user reports playtest
  results:** flip each PASSed fix's BUGS.md index row + heading tag to
  `tested`, and file each FAIL as a new finding with their notes.
- If a fix sketch doesn't survive contact with the real code, do NOT improvise
  a redesign: mark `blocked` with what you found and continue the queue.

**End of session:** update STATUS.md (implemented list, queue position, anything
blocked), commit, push, and give a table of fixes completed / blocked / remaining.
A separate Fable QA session audits samples and runs the automated A/B pair after
your leg — leave the game itself alone.
