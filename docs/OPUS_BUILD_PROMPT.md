# Opus build-session prompt — wave 3 (continuation)

Paste everything below into a fresh Claude Code session (Opus) to continue the
implementation leg. (The wave-1/wave-2 versions of this prompt are in git history.)

---

Continue the Surviving Mars: Relaunched "Community Fix Pack" mod — you are doing
the implementation leg, wave 3, **resuming part-way through**. Discovery is
complete; **39 fixes are implemented**. The first 30 are probe-verified in-game
(19/19 automated A/B pass); the 9 wave-3 fixes (F46, F36, F38, F39, F40, F17, F41,
F16, F70) have probes but **have never been run in-game at all**. Your job is to
finish the wave-3 queue the same disciplined way: sketches → fix files, carefully
and mechanically.

**First, read these (in order) from `C:\Dev\SMR-BugFixPack`:**
1. `docs\STATUS.md` — snapshot, the wave-3 "Next up" queue, and the hard-won
   engine facts (read the WHOLE facts list — several were learned the hard way)
2. `docs\FIX_POLICY.md` — HOW to patch (binding rules)
3. `docs\BUGS.md` — the tracker; every fix you write references its entry
4. `docs\TESTING.md` + the Test Kit repo `C:\Dev\SMR-BugFixPack-TestKit`
   (probe conventions in `Code\00_TestCore.lua`; the wave-3 probes are in
   `Code\30_Probes_Wave3.lua`; autorun harness in `Code\95_AutoRun.lua` — you do
   NOT run the game)
Then skim two wave-3 fix files as templates — `Code\Fix_TrainCargoDumping.lua`
(full replacement) and `Code\Fix_DustSicknessBiorobots.lua` (preset data patch,
including the DataLoaded/DataChanged timing that presets require).
The game's Lua source (read-only, NEVER modify) is at
`A:\SteamLibrary\steamapps\common\Project Spark\ModTools\Src`.

**Your work queue, in order** (this is STATUS.md's "Next up", repeated here):
1. **F71** auto-export allocates capacity alphabetically. Careful: the target
   (`CreateAutoCargoRequest`, `UniversalRocket.lua:1736-1758`) is ALREADY replaced
   by wave 2's `Fix_LanderCargoRatchet.lua` — fold F71 into that file's copy or
   layer it on top; do not write a second independent replacement of the same
   function.
2. **F72** "No available Asteroid Landers" while a lander sits on the pad.
3. **F54** switched-off shuttle hubs count as transport available.
4. **F59/F60/F62/F63** housing/service reach bundle.
5. **F32** notification suppression (data patch on three NotificationPresets).
6. **F33/F34** landscape nil guards.
7. **`Code/90_SaveSanitizer.lua`** consolidating the remaining savegame sweeps:
   **F35** (turbine buff — deliberately not done as a standalone fix, it is a pure
   LoadGame sweep with no live half), **F03** (leaked upgrade modifiers), **F48**
   (station connectors).
8. **D01** opt-in classic-rockets module (design note on the BUGS.md entry).
9. Test Kit side-task: the F51 shuttle-cache probe PASSes even unfixed on a fresh
   colony — give it a scenario strict enough to discriminate.
10. Small queued item from F70: the legacy
    `LanderRocketCargoRequest:RetrieveRequests` guard reads
    `self.initial_landing_completed` on the DIALOG instead of the rocket
    (`LanderRocketCargoRequest.lua:116`). One-word correction; first establish
    whether the legacy `LanderRocket` class is reachable in Relaunched at all.

**Per-fix procedure (do not deviate):**
1. Open the BUGS.md entry. Then READ the actual current function(s) in
   `ModTools\Src` at the cited file:line — never write a fix from the tracker
   description alone. If the code doesn't match the entry, set the entry's
   status to `blocked` with a one-line note and move to the next fix. If it
   matches but the *sketch* is wrong (this happened three times in wave 3 — F36,
   F40, F41), implement what the code actually justifies and record the
   divergence as an "*Implemented differently, on better evidence:*" paragraph on
   the entry.
2. Write `Code\Fix_<Name>.lua` registered via
   `SMRFixPack.Register("<Name>", { title = ..., apply = function() ... end })`.
   - Prefer (in order): data/preset patch → additive OnMsg → registry/table
     surgery → chained wrapper capturing the original → full replacement.
   - Full replacements copy the shipped body byte-identical except lines marked
     `-- FIX:`; header comment cites source file + lines.
   - `apply` must self-check its target exists/looks broken and `return "<reason>"`
     to deactivate gracefully. Never error, never assume.
3. Add the file to `metadata.lua`'s `code` list (order matters: 00_Core first).
4. Same pass: write the Test Kit probe in `Code\30_Probes_Wave3.lua` (and keep it
   registered in the Test Kit's `metadata.lua`).
5. Same commit: BUGS.md index status → `fixed` (+ tag on the detail heading),
   player-language line in README's fix table and MOD_DESCRIPTION.md. If the fix
   has an aspect script probes cannot verify (visuals, UI feel, long-running
   behavior), also append a PT-entry to `docs\PLAYTEST_CHECKLIST.md` in the
   existing format — continue the numbering from **PT-31**, inside "Group 6 —
   wave-3 fixes". Reuse its save fixtures; verify any console command against
   `ModTools\Src` (the checklist documents which cheats are retail-dead).
6. Commit with `git -c user.name="SMR-BugFixPack"
   -c user.email="154917955+catt144@users.noreply.github.com"`,
   message: `Implement F## (<short name>)`. One fix per commit. Push both repos to
   origin (github.com/catt144/SMR-CommunityFixPack) at session end.

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
  When copying a shipped body, drop its `assert(...)` lines and say so in the
  header.
- Mod code loads BEFORE classes are flattened: an inherited method reads nil on
  a subclass classdef — apply() self-checks must look up methods on their
  DECLARING class (F64 shipped broken this way once; wave 3 hit it again with
  `UniversalStorageDepotBase.IsResourceEnabled` and `TunnelBase.AddPFTunnel`).
  Property defaults (`properties = {{id = "automation", ...}}`) are NOT copied
  onto the class at that point either — check the classdef's `properties` list.
- **Presets do not exist when mod code loads.** `Data\` is read during `LoadData`
  → `Msg("DataLoaded")` (`CommonLua\Dlc.lua:640-662`), long after `ModsLoadCode()`.
  Data patches must run from `OnMsg.DataLoaded` (+ `OnMsg.DataChanged` for editor
  reloads), not `ClassesPostprocess`. See `Fix_DustSicknessDamage.lua`.
- `g_Consts` is a GameVar — read it inside patched functions only; `const` is
  fine at apply time. `/` truncates (integer division). A post-wrapper on any
  command method (SetCommand-reached, e.g. Colonist:Idle) never runs — pre-wrap.
- `GameInit` is a COMBINED method (`DefineCombinedMethod("GameInit", "procall",
  "Object")`) assembled from the classdefs at class-build time — wrapping it on a
  mixin works, and errors inside it are swallowed by `procall`.
- `Random`, `Max`, `Min`, `MulDivRound`, `empty_table`, `table.remove_entry`,
  `table.find(list, field, value)` are engine globals. Verify any API you're
  unsure of by grepping `ModTools\Src` — never guess names.
- `IsValid()` rejects the plain tables probes use as stand-ins. Either keep it out
  of the fix's hot path (prefer a structural check) or have the probe swap it via
  `WithGlobals`.
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
your leg — **that pair has not been run since wave 2, so all 9 wave-3 fixes are
unverified in-game.** Leave the game itself alone.
