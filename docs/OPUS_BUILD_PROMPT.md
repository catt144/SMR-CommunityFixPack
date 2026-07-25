# Kickoff prompt for the build-out session (Opus)

Copy-paste everything below the line into the new conversation.

---

Continue the Surviving Mars: Relaunched "Community Fix Pack" mod — you are doing
the implementation leg. This is disciplined execution work, not discovery: the
bugs are already found, verified, and have fix sketches. Your job is to turn
sketches into fix files, carefully and mechanically.

**First, read these (in order) from `C:\Dev\SMR-BugFixPack`:**
1. `docs\STATUS.md` — project snapshot, implementation queue, hard-won engine facts
2. `docs\FIX_POLICY.md` — HOW to patch (binding rules)
3. `docs\BUGS.md` — the tracker; every fix you write references its entry
4. `docs\TESTING.md` — the test-kit spec and per-fix probes
The game's Lua source (read-only, NEVER modify) is at
`A:\SteamLibrary\steamapps\common\Project Spark\ModTools\Src`.

**Your work queue, in order:**
1. Build the Test Kit companion mod first (`C:\Dev\SMR-BugFixPack-TestKit`, per
   TESTING.md): `SMRTest.RunAll()` with the script probes for all ALREADY
   implemented fixes (F01-F64 wave), plus an inventory pass of `Lua\Cheats.lua`
   and `GameCheatShortcuts.generated.lua` noting useful cheat functions in a
   short `docs\CHEATS_INVENTORY.md`.
2. Then implement fixes strictly in this order, one at a time:
   F67, F68, F69 (asteroid lander trio), F73, F45, F44, F30, F37, F50, F51,
   F52, F53, F55, F58, F61, F06, F09, F11, F12, F13, F14.
   For each: write its Test Kit probe in the same pass (TESTING.md lists many).

**Per-fix procedure (do not deviate):**
1. Open the BUGS.md entry. Then READ the actual current function(s) in
   `ModTools\Src` at the cited file:line — never write a fix from the tracker
   description alone. If the code doesn't match the entry (game patched?), set
   the entry's status to `blocked` with a one-line note and move to the next fix.
2. Write `Code\Fix_<Name>.lua` registered via
   `SMRFixPack.Register("<Name>", { title = ..., apply = function() ... end })`.
   Follow the existing fix files as templates (Fix_TrainsToVoid.lua is a good
   wrapper example, Fix_MilestoneCrash.lua a good full-replacement example).
   - Prefer (in order): data/preset patch → additive OnMsg → registry/table
     surgery → chained wrapper capturing the original → full replacement.
   - Full replacements copy the shipped body byte-identical except lines marked
     `-- FIX:`; header comment cites source file + lines.
   - `apply` must self-check its target exists/looks broken and `return "<reason>"`
     (string) to deactivate gracefully if not. Never error, never assume.
3. Add the file to `metadata.lua`'s `code` list (order matters: 00_Core first).
4. Same commit: BUGS.md index status → `fixed` (+ tag on the detail heading),
   add a player-language line to README's fix table and MOD_DESCRIPTION.md's
   "fixes right now" section (move it out of the planned list).
5. Commit with `git -c user.name="SMR-BugFixPack" -c user.email="stkotor2@gmail.com"`,
   message: `Implement F## (<short name>)`. One fix per commit.

**Hard rules:**
- Never modify anything under the game directory. The mod is the only output.
- No balance changes, no refactors, no improvements beyond the verified defect.
- Do not mark anything `tested` — that status is reserved for the QA session
  (Fable) after in-game verification.
- Engine Lua quirks (from STATUS.md): `#nil`/`next(nil)`/`ipairs(false)` are
  tolerated; boolean relational compares are NOT. `Random`, `Max`, `Min`,
  `MulDivRound`, `empty_table`, `table.remove_entry` are engine globals. Verify
  any API you're unsure of by grepping `ModTools\Src` — never guess names.
- If a fix sketch doesn't survive contact with the real code, do NOT improvise
  a redesign: mark `blocked` with what you found and continue the queue.
- Keep per-fix scope small. The savegame-sanitizer module (90_SaveSanitizer.lua)
  and the D01 opt-in classic-rockets module are LATER phases — skip unless the
  queue is exhausted.

**End of session:** update STATUS.md (implemented list, queue position, anything
blocked), commit, and give me a table of fixes completed / blocked / remaining.
