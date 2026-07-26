# Fable continuation prompt — after the F02/F66/F47 follow-up leg (2026-07-26)

Paste everything below into a fresh Claude Code session (Fable). The 2026-07-26
follow-up leg is DONE (F02 hunt + watchdog rework, F66 reclaim trigger, F47
composition repairs, version tags, two clean A/B pairs — full record in STATUS.md
"Follow-up session — Fable, 2026-07-26"). What remains is playtest-gated: there is
no queued build work, so this session starts from whatever the user's playtests
turn up.

---

You are continuing the Surviving Mars: Relaunched "Community Fix Pack" QA/build work.

**First, read (in order) from `C:\Dev\SMR-BugFixPack`:**
1. `docs\STATUS.md` — the "Follow-up session — Fable, 2026-07-26" section AND the
   whole engine-facts list.
2. `docs\FIX_POLICY.md` — the patching rules.
3. The BUGS.md entry for any fix the user's playtest touched (F02 carries the full
   regression-hunt record and the watchdog design).

Game source (read-only, NEVER modify):
`A:\SteamLibrary\steamapps\common\Project Spark\ModTools\Src`.
Both mods load through junctions from `C:\Dev\SMR-BugFixPack` and
`C:\Dev\SMR-BugFixPack-TestKit` — confirm the user is not mid-playtest before any
edit that the game could load mid-session.

## The F02 situation (the one live investigation)

PT-01 regressed: on the user's max-threat run, the fixed Meteors thread struck 5×
on the designed cadence, then went silent for 24+ sols in one uninterrupted session.
The 2026-07-26 hunt FALSIFIED every static explanation (no thread error logged, no
mid-session load, bounded wait math even with towers, descriptor-nil needs 80%
atmosphere, nothing deletes the thread; the first MeteorStorm went quiet in the SAME
window — mechanism is outside both loop bodies). The fix now carries a heartbeat +
daily watchdog + LoadGame necropsy designed to capture the culprit live:

- When the user LOADS their sol-36 PT-01 save, the log prints
  `MeteorFrequency: persisted Meteors thread on load was <alive|DEAD|not created>`
  — that single line answers dead-vs-stuck for the wedged thread.
- If the stall recurs in play, the watchdog prints
  `WATCHDOG — Meteors thread silent for N game hours (last phase 'X', thread
  ALIVE but stuck|DEAD); restarting` and self-heals. The `last phase` value pins
  WHERE the loop stopped (rolled / long-sleep-done / striking / struck /
  descriptor-wait / …).

When those log lines come back: alive-but-stuck in a Sleep phase points at the
scheduler/persist layer (check how the save chain interacts with persisted
game-time threads); DEAD with no error points at a silent kill. Phase "striking"
means MeteorsDisaster never returned — walk its internals with the descriptor the
log implies. Design the real repair from that evidence; the watchdog stays either
way as defense-in-depth.

## Open user items (playtest-gated)

- **PT-01 re-run (F02):** load the sol-36 save FIRST (necropsy line), then a fresh
  no-reload stretch on the same map; collect the log.
- **PT-03 re-run (F44 rework):** the damaged save should print
  `TrackSalvageWipe: removed N orphaned track element(s)` on load; then the curve
  trim per the checklist.
- **PT-41 (F66):** two-building contested hex; demolish the winner; the loser must
  rebuild its connector within a tick (the new reclaim trigger).
- Track salvage refunds (F47): partial trims now refund; a trim that deletes the
  last elements must ALSO refund (the composition fix) — worth an eye during PT-03.
- Rest of the merged-pack playtest checklist; PT-36/37/38 gates.
- MarsDebug attended `[install]` pass for the wave-4/5 fixes (SetupOnly mode; see
  the wave-3 QA section for procedure and the modal-dialog warning).

## Harness facts (hard-won — do not re-derive)

- Launch: `& "c:\program files (x86)\steam\steam.exe" -applaunch 3215050 -smrautorun`.
  A leg takes ~75 s; watch for Mars.exe to appear (up to 4 min) then exit. **Never
  kill on a short timeout** — no-kill watcher (25 min guard); harness watchdog 15 min.
- Baseline = overwrite fix pack `metadata.lua` with an emptied `code` list; restore
  with `git checkout -- metadata.lua`. **NEVER `git commit -a` while that edit is in
  the working tree.**
- Expected healthy numbers (2026-07-26): baseline **1 PASS / 58 FAIL / 11 SKIP /
  0 ERROR**; full pack **59 PASS / 0 FAIL / 11 SKIP / 0 ERROR** with 66/67 active
  (ClassicRockets opt-in inactive). The 11 SKIPs: 9 `[install]` probes, ClassicRockets,
  TechDescriptionBuilding (F25 rides its playtest item). The F02 probe is now a
  discriminating behavior probe (drives the watchdog), hence 11 not 12 SKIPs.
  Synthetic-map noise unchanged: ~49 Flight.lua `objects_to_mark` errors + a few
  GameInit `attempt to call a nil value` lines in BOTH legs; a `[mod] Error in mod
  … Test Kit` line at quit is a shutdown artifact.
- Parse sweep: python + luaparser, `ast.parse(open(f,encoding='utf-8-sig').read())`.

## Hard rules

Same as ever (STATUS.md engine facts govern): sandbox on all platforms;
`error()`/`assert()` report-and-continue; self-checks read the DECLARING class;
presets only after DataLoaded (GlobalMaps exist EMPTY before it; DataChanged(false)
re-fires right after); GameVars only inside patched functions; post-wrappers on
command methods never run; `IsValid()` is falsy for ALL pure-Lua objects; never
modify the game directory; do NOT mark anything `tested` (playtest's job);
mechanical repairs land with a re-verified A/B, redesigns go to the user. Commit with
`git -c user.name="SMR-BugFixPack" -c user.email="154917955+catt144@users.noreply.github.com"`,
push the fix pack (TestKit stays local-only).

**End of session:** update STATUS.md and this prompt (or retire it), commit, push,
and summarize.
