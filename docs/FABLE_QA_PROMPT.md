# Fable QA-session prompt — after waves 4 and 5

Paste everything below into a fresh Claude Code session (Fable) AFTER **both**
Opus build legs finish — wave 4 (done) and wave 5 (the eight-entry P2/P3 tail) —
and the user's playtest of the wave-3 pack is done or paused. Both legs work on
the SAME `wave4` branch in the `-wave4` worktrees, so there is one merge, not two.
The wave-3 version of this prompt is in git history; its session record is in
STATUS.md ("QA session (wave 3)").

---

You are doing the **QA leg** for the Surviving Mars: Relaunched "Community Fix
Pack", covering the wave-4 **and wave-5** implementations. Both live on the
`wave4` branch (worktrees at `C:\Dev\SMR-BugFixPack-wave4` and
`C:\Dev\SMR-BugFixPack-TestKit-wave4`) and have never been run in-game. Your job:
merge, prove every module loads and applies, prove every probe discriminates,
and audit the riskiest divergences.

**Read "wave 4" below as "waves 4 and 5" throughout** — same branch, same merge,
one A/B pair covering both. Wave 5's probes live in `Code\50_Probes_Wave5.lua`
alongside wave 4's `Code\40_Probes_Wave4.lua`, and its playtest items continue
from PT-45. If wave 5 has not been run yet, QA wave 4 alone and say so.

**First, read these (in order) from `C:\Dev\SMR-BugFixPack`:**
1. `docs\STATUS.md` — snapshot, engine facts (the WHOLE list), and the "QA
   session (wave 3)" section, which records the exact A/B procedure that worked
2. `docs\FIX_POLICY.md` — the rules the fixes are audited against
3. `docs\BUGS.md` — the tracker; wave-4 entries carry "*Implemented
   differently*" / "*Blocked*" paragraphs — those claims are what you audit
4. `docs\TESTING.md` + both Test Kit trees (conventions in
   `Code\00_TestCore.lua`, wave-4 probes in `Code\40_Probes_Wave4.lua`, wave-5
   probes in `Code\50_Probes_Wave5.lua` if that leg ran)

Game source (read-only, NEVER modify):
`A:\SteamLibrary\steamapps\common\Project Spark\ModTools\Src`.

## Task 0 — merge wave 4 to main (do this before any run)

Confirm the user is not mid-playtest (ask if unclear — a relaunch mid-merge
would load a half-merged state through the junctions). Then, in each repo:
`git merge wave4` on main, resolve conflicts (STATUS.md and metadata.lua are the
likely spots — keep the commented-out F10 line), delete the worktrees
(`git worktree remove <path>`), push the fix pack. If the user's playtest
produced report-processing commits (see `docs/FABLE_PLAYTEST_PROMPT.md`), merge
ON TOP of those — tracker statuses from the playtest win over build-leg `fixed`.

## Task 1 — parse sweep, then the A/B RunAll pair

Python 3.13 + `luaparser` are installed. First parse every `.lua` in both mods
(pattern: `from luaparser import ast; ast.parse(open(f,encoding='utf-8-sig').read())`)
— a parse error means the file silently never loads in-game.

Then the pair, using the procedure proven in the wave-3 QA session:
- **Baseline**: overwrite the fix pack `metadata.lua` with an emptied `code`
  list (restore afterwards with `git checkout -- metadata.lua`).
- Launch: `& "c:\program files (x86)\steam\steam.exe" -applaunch 3215050 -smrautorun`
  — the TestKit's 95_AutoRun drives boot → new colony → RunAll → quit
  unattended; a leg takes ~60-90 s. Poll for the Mars process to appear then
  exit (12-min timeout guard).
- **B leg**: restore metadata, relaunch, diff. Logs land in
  `%AppData%\Surviving Mars Relaunched\logs\Mars.exe-<timestamp>.log`; extract
  with pattern `^\[mod\] \[(SMRTest|SMRAUTO|CommunityFixPack)\]`. Note a probe
  PASS line can be missing from that extraction if an engine error block splits
  it — always cross-check the `---- N PASS ----` counts, and grep any `[LUA
  ERROR]` blocks: ~49 `Flight.lua objects_to_mark` errors per leg are known
  engine noise on the synthetic map; anything mentioning `SMR` files is OURS
  and is a finding.
- Expected after wave 4 alone: **61 code entries in metadata**, 59 `Fix_*` +
  `90_SaveSanitizer` + `Opt_ClassicRockets`, with **59 `applied`**,
  ClassicRockets `inactive` (opt-in), and F10 absent unless PT-36 rolled it back.
  Wave 5 adds to that count — recompute from `metadata.lua` rather than trusting
  this number. Every armed probe FAILs in baseline → PASSes in B. A missing id in
  ListFixes means the FILE never loaded (parse error); an `error` status means
  apply() raised — both are findings.
- Four wave-4 modules can legitimately report `inactive`, and each says why in
  its detail string: `LastTransmissionStorage` and `IndependenceTerraforming`
  (preset patches — inactive if the shipped data is already correct),
  `GraphConsumedCaption` (inactive if no stockpile panel matched), and
  `SequenceLatents` (partial if only one of its two targets exists). An
  `inactive` with any OTHER reason is a finding.
- If any fix repairs something a shipped savegame fixup also touches, verify it
  hooks `OnMsg.PostLoadGame` (the F35 lesson — LoadGame fires BEFORE
  FixupSavegame, Savegame.lua:810-813).

## Task 2 — probes that may not be discriminating

For each wave-4 probe, state plainly: did it FAIL in the baseline leg? A probe
that passes both halves is not evidence and must be reported as such (the F51
and F10 precedents — and remember F10's deeper lesson: if fixed and unfixed
CANNOT differ because the engine tolerates the "crash", the fix itself is a
wontfix candidate, not just the probe).

## Task 3 — audit the divergences

Every wave-4 fix whose entry carries an "*Implemented differently, on better
evidence:*" paragraph gets an audit: check the evidence, not just the code.
The wave-3 pattern that worked: parallel read-only subagents, one per fix, each
given the fix file + BUGS entry + relevant Src files + the engine-facts list,
told to be adversarial and cite file:line. Verify their HIGH findings yourself
before acting (the wave-3 audit's one HIGH — the sanitizer fixup race — was
real and shipped a repair). Full replacements and anything that WRITES to
savegames get audited even without a divergence paragraph.

**Wave 4's priority audit list** (the build leg flagged these itself):
- the four full replacements — F66 `CreateConnectorElements`, F21 `BoardVehicle`,
  F24 `MoveInside`, F28 `ReplaceTech` — diff each against Src line by line;
- F22, the only fix that replaces a **global function** rather than a method;
- F20's per-call instance `GetProperty` override (does it always restore? can
  anything yield inside the tooltip builder?);
- F65's `PostLoadGame` sweep and its "different live grids" test;
- F74/F75, both filed DURING the build leg, so neither entry has ever been read
  by a second pair of eyes.

## Task 4 — regression spot-checks

Confirm wave-4 work didn't disturb the wave-3 repairs: the sanitizer still
hooks `PostLoadGame`; the `%`-escaping `log()` helpers are intact in
00_Core.lua / 90_SaveSanitizer.lua / TestKit 00_TestCore.lua / 95_AutoRun.lua;
the commented-out F10 metadata line survived the merge (or its PT-36
disposition did).

## Hard rules — engine facts (violations shipped real bugs)

- Sandbox on ALL platforms: no debug/io/os-beyond-time/Async*/load. Plain
  assignment for new globals; never `rawset(_G, ...)`.
- `error()`/`assert()` do NOT unwind mod code — report-and-continue.
- The engine TOLERATES `pairs(nil)`/`next(nil)`/`ipairs(false)`; indexing a nil
  value and boolean relational compares DO raise.
- `ModLog` re-formats its message via printf-style ModPrint — escape `%` (the
  pack's log helpers already do).
- `Msg("LoadGame")` fires BEFORE `FixupSavegame`; fixup-compensating passes
  hook `PostLoadGame`.
- Classes not flattened at mod-load: self-checks read the DECLARING class.
  Presets exist only after `DataLoaded`. GameVars only inside patched
  functions. `/` truncates. Post-wrappers on command methods never run.
- `IsValid()` rejects probe stand-in tables (probes swap it via WithGlobals).
- Never modify the game directory. Do NOT mark anything `tested` — that is the
  human playtest's status. If an audit finds a fix wrong: record with file:line
  evidence first; mechanical repairs (logging, hook timing) may land with a
  re-verified A/B, redesigns go to the user.

**End of session:** update STATUS.md (merge result, A/B numbers, audit
verdicts, anything newly broken), commit with
`git -c user.name="SMR-BugFixPack" -c user.email="154917955+catt144@users.noreply.github.com"`,
push, and give a table of: fixes verified / fixes that failed / probes that
don't discriminate / anything needing the user.
