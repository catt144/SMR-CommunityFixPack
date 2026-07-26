# Fable continuation prompt — after the wave-4/5 QA leg (2026-07-25)

Paste everything below into a fresh Claude Code session (Fable). The wave-4/5 QA leg
is DONE (merge, 14-audit fan-out, 9 repair commits, A/B pair CLEAN — full record in
STATUS.md "QA session (waves 4+5)"). This session picks up the two items the user
decided at the end of that leg, plus the queued tail.

---

You are continuing the Surviving Mars: Relaunched "Community Fix Pack" QA/build work.

**First, read (in order) from `C:\Dev\SMR-BugFixPack`:**
1. `docs\STATUS.md` — the "QA session (waves 4+5)" section AND the whole engine-facts
   list (two new facts landed there: `Msg("DataChanged", false)` fires right after
   every DataLoaded with GlobalMap tables existing EMPTY before it; `IsValid()` is
   falsy for ALL pure-Lua objects, not just probe stand-ins).
2. `docs\FIX_POLICY.md` — the patching rules.
3. The BUGS.md entries for **F02** and **F66** — both carry the exact state and spec.

Game source (read-only, NEVER modify):
`A:\SteamLibrary\steamapps\common\Project Spark\ModTools\Src`.
Both mods load through junctions from `C:\Dev\SMR-BugFixPack` and
`C:\Dev\SMR-BugFixPack-TestKit` — confirm the user is not mid-playtest before any
edit that the game could load mid-session.

## Task 1 — F02 regression hunt (PT-01 FAIL, user confirmed NO reloads)

The observed data (also on the F02 entry): Variant B, max-threat map, natural strikes
at ~sol 5.5 → 7.5 (+60h) → 8.4 (+39h) → 10.3 (+39h) → [3 Sensor Towers built ~10.5,
warning received] → 12.5 (logger printed "+57 game hours") → **silence through sol 36**
(~560+ game hours; the design band is 35-60h). No reloads, so the load-time re-roll
explanation is dead. The TestKit logger prints once per `MeteorsDisaster` call —
silence means the thread stopped calling, not a logging gap.

Investigate, in order:
1. The user's playtest logs `%AppData%\Surviving Mars Relaunched\logs\
   Mars.exe-20260725-18.34.12-*.log` and `-19.04.10-*.log`: find the last
   `MeteorsDisaster` line and grep the region after it for `[LUA ERROR]` — an error
   inside the fixed thread would kill the loop permanently (that is exactly what the
   fix's LoadGame restart exists to recover from, but no reload happened).
2. `Code\Fix_MeteorFrequency.lua` against `Lua\Meteors.lua:271-292` (thread body) and
   the MeteorStorm sibling (`:322-342`): walk the fixed wait math with Sensor Towers
   present — `const.SensorTowerPredictionAddTime = 12h` per tower is WARNING lead, not
   interval; three towers = +36h of warning. Check whether warning_time can exceed
   spawn_time in the fixed body and what the wait becomes then (a negative or
   永-blocked wait after towers went up fits the timeline: towers at 10.5, one more
   strike whose roll predated them, then silence).
3. If (2) is the defect: mechanical repair + a probe that arms with a large
   warning_time, and rerun the A/B pair (procedure below). If an in-game error killed
   the thread: find and fix the raiser instead.
4. PT-01 then needs a fresh no-reload run from the user.

## Task 2 — F66 rebuild-trigger repair (user decision: "rebuild instead of half baking it")

Spec (also on the F66 entry): wrap `TrackConnectedObjBase:Done` (declaring class,
`TrainTransport.lua:14`; pre/post choice is yours — verify Done is not command-killed;
the shipped body itself runs during destruction) so that after the shipped body runs,
nearby `TrackConnectedObjBase` objects that are valid and not being destructed get
`CreateGameTimeThread(o.CreateConnectorElements, o)` — the engine's own deferred
pattern (`Track.lua:181-183`, `TrainTransport.lua:26`). Connector spots reach ≤ ~2
hexes, so a small-radius map query around the dying building's connector hexes is
enough; do NOT trigger a global rebuild. The F66-guarded `CreateConnectorElements` is
safe to re-run for buildings that already own their elements. Audit-grade care:
- the wrap must tolerate `done_map` teardown (early-return like the shipped body);
- no work when the map itself is being destroyed;
- verify against Src what query primitive is sandbox-safe (`MapForEach`/`HexGridGetObjects…`);
- extend the `TrackConnectorPingPong` probe (TestKit `Code\40_Probes_Wave4.lua:146`)
  or add a second probe for the reclaim, then run the A/B pair.

## Task 3 — queued tail (as time allows)

- **F47 composition under-refunds** (entry + STATUS): F44's trim-to-empty exit skips
  the refund; construction-site early-return broader than repair sites. Both
  under-refunds only.
- Game-version tags on all full-replacement headers (§1.5) — release checklist.
- MarsDebug attended `[install]` pass for the wave-4/5 fixes (SetupOnly mode; see the
  wave-3 QA section for the procedure and the modal-dialog warning).

## Harness facts (hard-won this session — do not re-derive)

- Launch: `& "c:\program files (x86)\steam\steam.exe" -applaunch 3215050 -smrautorun`.
  A leg takes ~75 s; watch for Mars.exe to appear (up to 4 min — Steam can lag after a
  recent exit) then exit. **Never kill on a short timeout** — use a no-kill watcher
  (25 min guard) and rely on the harness's own 15-min watchdog.
- Baseline = overwrite fix pack `metadata.lua` with an emptied `code` list; restore
  with `git checkout -- metadata.lua`. **NEVER `git commit -a` while that edit is in
  the working tree** (it shipped an empty pack once; restored in 1321795).
- The TestKit flushes the log per line and neuters `ShowStartGamePopup` when armed.
  A wedged leg with a silent log now means a NON-YIELDING busy loop (the TrainWaitTime
  probe lesson: never fake a blocking primitive as a no-op inside a driven loop —
  starves every Lua thread including the watchdog).
- Expected healthy numbers (2026-07-25): baseline 1 PASS / 57 FAIL / 12 SKIP / 0 ERROR;
  full pack 58 PASS / 0 FAIL / 12 SKIP / 0 ERROR with 66/67 active (ClassicRockets
  opt-in inactive). Non-discriminating by design: FactionFundingCheck (F10 retired,
  PT-36 gate), TechDescriptionBuilding (SKIPs — F25 rides its playtest item), F24 (no
  probe, PT-44). ~49 Flight.lua `objects_to_mark` errors per leg plus a few
  GameInit-path `attempt to call a nil value` lines are synthetic-map noise (both
  legs, shipped files only); a `[mod] Error in mod … Test Kit` line at quit is a
  shutdown artifact.

## Hard rules

Same as ever (STATUS.md engine facts govern): sandbox on all platforms;
`error()`/`assert()` report-and-continue; self-checks read the DECLARING class;
presets only after DataLoaded (GlobalMaps exist EMPTY before it; DataChanged(false)
re-fires right after); GameVars only inside patched functions; post-wrappers on
command methods never run; never modify the game directory; do NOT mark anything
`tested` (playtest's job); mechanical repairs land with a re-verified A/B, redesigns
go to the user. Commit with
`git -c user.name="SMR-BugFixPack" -c user.email="154917955+catt144@users.noreply.github.com"`,
push the fix pack (TestKit stays local-only).

**End of session:** update STATUS.md and this prompt (or retire it), commit, push,
and summarize: what was found for F02, whether the F66 repair shipped, A/B numbers,
anything new for the user. Open user items to carry forward: PT-03 re-run (F44
rework verification, incl. the damaged save's orphan-sweep log line), the rest of the
playtest checklist on the merged pack, PT-36/37/38 gates.
