# Project Status — read this first in a new session

Updated: 2026-07-25 late (**wave-4/5 QA leg DONE — merged to main, A/B pair CLEAN
(58 PASS / 0 FAIL / 0 ERROR, 66/67 active), 14-audit fan-out done, 7 repair commits
landed** — see "QA session (waves 4+5)" below. Prior entry: wave-5 build leg wrap-up).
**Two prompts, two triggers:**
- `docs/FABLE_NEXT_PROMPT.md` — the NEXT Fable work session: the F02 regression hunt
  (PT-01 FAILed with NO reloads — user confirmed — so the meteor thread genuinely
  stopped) and the F66 rebuild-trigger repair (user decision 2026-07-25: "rebuild
  instead of half baking it"), plus the queued tail (F47 under-refunds, §1.5 version
  tags, MarsDebug install pass).
- `docs/FABLE_PLAYTEST_PROMPT.md` — processes the user's manual playtest report
  (PASS→`tested` flips, FAIL→new findings, the PT-36/37/38 decision gates). The
  playtest RESUMES on the merged wave-4/5 pack; PT-03 needs a re-run (F44 rework);
  PT-01 needs a fresh run once F02 is repaired.
- ~~`docs/OPUS_BUILD_PROMPT.md`~~ done; ~~`docs/FABLE_QA_PROMPT.md`~~ done (2026-07-25).
BUGS.md is
the canonical defect tracker, FIX_POLICY.md the patching rules, WORKFLOW.md the
dev/test/release process, RESEARCH.md the lead catalog (incl. ChatGPT dossier
cross-check), MOD_DESCRIPTION.md the player-facing mod-page draft (update its fix
list in the same commit that implements a fix; only `tested` fixes ship in the
final text), TESTING.md the force-the-bug test plan, CHEATS_INVENTORY.md the
shipped cheat/debug surface the tests drive.

## Follow-up session — Fable, 2026-07-26: F02 hunt + watchdog, F66 reclaim, F47 composition, version tags — A/B CLEAN

**Task 1 — F02 regression hunt (PT-01 FAIL, no reloads).** Every static explanation
was FALSIFIED against the playtest log (Mars.exe-20260725-19.04.10) — full record on
the F02 entry. Established: one uninterrupted session (single `Load Game:` marker,
day counters monotonic to 36, wave-3 roster); no `[LUA ERROR]` anywhere near the
stall; the tower wait-math is bounded (warning = Min(6h+12h·3, 75h) = 42h, two sleeps
total ≤ spawn+1s ≤ 60h on Meteor_VeryHigh); the descriptor-nil day-loop needs
Atmosphere > the **80%** MeteorStormStop threshold (TerraformingDisasters.lua:69,
TerraformingParam.lua:80-84) — impossible at sol 12; nothing in Src or either mod
deletes/restarts the thread mid-game; the PT-03 track debris postdates the silence.
Bonus finding: the first MeteorStorm (birth_hour = 250h + 0..25h) was due in the SAME
window and never visibly fired — BOTH disaster threads went quiet at t≈8.2-8.3M, so
the mechanism sits outside both loop bodies (scheduler/persist side) and needs a live
capture. **Root cause NOT pinned; the rework captures it next time:** heartbeat
phases in the thread body (zero closure upvalues — the persisted thread keeps the
engine-proven persistence shape), loud top-of-body exits, a daily OnMsg.NewDay
watchdog (`SMRFixPack.MeteorsWatchdogCheck`, threshold spawn+random+75h+1 sol, gives
up loudly after 3 restarts, respects the fix's status — F75 lesson) that logs
**thread ALIVE-but-stuck vs DEAD + last phase** before restarting, and a LoadGame
necropsy of the persisted thread — loading the user's sol-36 save answers
dead-vs-stuck directly. Probe reworked install→behavior (drives the watchdog with a
synthetic stale heartbeat; discriminates in the retail sandbox instead of SKIPping).

**Task 2 — F66 rebuild trigger (user decision: repair).** Landed in
Fix_TrackConnectorPingPong.lua: post-wrap of `TrackConnectedObjBase:Done` (declaring
class; destructor, not command-killed) records the dying building's connector hexes
before the shipped body runs, then `SMRFixPack.TrackConnectorReclaim` queries each
hex with `map:MapForEach(pos, "hex", 3, "TrackConnectedObjBase", …)` (spots reach
≤ ~2 hexes; no global rebuild) and schedules the engine's own deferred idiom with
in-thread revalidation (TrackElement.lua:194-198) for every other live,
non-destructing candidate; guarded CreateConnectorElements makes re-runs idempotent;
done_map early-returns. Probe extended: exactly one rebuild scheduled (live
neighbour), dying self + destructing excluded, hexes deduplicated.

**Task 3 — F47 composition under-refunds (both audit MEDIUMs).** Landed in
Fix_TrackSalvageRefund.lua: the stand-down test is now the `demolishing` stamp
`TrackBase:OnDemolish` writes (Track.lua:250 — survives object death), so a
trim-to-empty (dies via CanDelete→DoneObject, no OnDemolish) refunds instead of
being misread as "already handled"; map/drop-pos captured pre-orig. The
construction-site early-return is narrowed to the repair-site delegation only —
plain sites fall through and their zone's stamped completed elements are accounted
(no double-refund: sites never carry stamps). Details on the F47 entry.

**Release item:** all full-replacement headers now name the game version the copy
came from — **game 1.0.7.396349** (was "shipped Src, 2026-07" / "post-1.0.7").

**A/B pairs (both clean; probe-count change is by design: the F02 probe moved from
install-SKIP to a discriminating behavior probe, so 12 SKIP → 11, 57 FAIL → 58):**

| Leg | Log (Mars.exe-20260726-…) | Result |
|-----|---------------------------|--------|
| Baseline #1 (pack emptied) | 00.06.11 | 1 PASS, 58 FAIL, 11 SKIP, 0 ERROR |
| Fixed #1 (F02+F66 in) | 00.08.03 | **59 PASS, 0 FAIL, 11 SKIP, 0 ERROR** — watchdog exercised end-to-end in-log |
| Baseline #2 (after F47 + version tags) | 00.11.46 | 1 PASS, 58 FAIL, 11 SKIP, 0 ERROR |
| Fixed #2 (everything in) | 00.13.02 | **59 PASS, 0 FAIL, 11 SKIP, 0 ERROR**, 66/67 active (ClassicRockets opt-in) |
| Baseline #3 (after the seed-crash repair) | 00.48.22 | 1 PASS, 58 FAIL, 11 SKIP, 0 ERROR |
| Fixed #3 (seed repair + sweep extension in) | 00.50.08 | **59 PASS, 0 FAIL, 11 SKIP, 0 ERROR**, 66/67 active |
| Baseline #4 (after the F18 savegame sweep) | 11.33.34 | 1 PASS, 58 FAIL, 11 SKIP, 0 ERROR |
| Fixed #4 (F18 sweep in) | 11.34.58 | **59 PASS, 0 FAIL, 11 SKIP, 0 ERROR** — F18 probe verifies the sweep both ways |

Parse sweep: every .lua in both mods parses (python luaparser).

**Live playtest, same night (user on the sol-36 save, results processed live):**
- **F02 necropsy answered: the wedged Meteors thread was ALIVE** — "persisted
  Meteors thread on load was alive" — a live thread whose wake-up never came
  (scheduler/persist side), not a dead one. Post-load natural gaps **+49h and
  +40h**, both in band; >42h is impossible under the broken code with 3 towers, so
  the cadence+towers check is satisfied on real play. Watchdog reported `healthy`.
  Also confirmed: single meteors get NO tower-scaled warning banner in the shipped
  game (the singles thread posts no notification; only the ~30 s Predict marker,
  and only with objects in the blast area) — the PT-01 checklist expectation was
  corrected accordingly (towers' lead shows in the STORM countdown).
- **PT-03 F44 halves PASS:** the load sweep removed the 40 orphaned elements from
  the first attempt; repeated build → salvage → rebuild cycles on straight AND
  curved tracks clean; train survives; **partial-salvage Metals refund observed
  live** (F47's half B).
- **New defect found during the F45 attempt, repaired same night (seed crash):**
  destroying a repair site in the deletion zone ALSO destroys its broken twin
  (TrackGridElement:Done, TrackElement.lua:200-201); the twin shares the site's
  node_idx and can sit just outside the zone at the seed index, and the shipped
  blind seeds (`all_elements[last]`/`[first]`) then crash ExpandTrackFromElement
  on a dead element (TrackElement.lua:718-719, `map` nil — mod-flagged MouseEvent
  error; unreachable in vanilla because broken tracks were unsalvageable before
  F45). Repair in Fix_TrackSalvageWipe.lua: seeds walk outward to the first
  still-VALID survivor, a side with no survivor is tolerated (empty new_track
  destroyed), and the LoadGame sweep now ALSO purges destroyed entries left
  inside track arrays by the aborted split (log line reports both counts —
  expect it on the user's save). **F45's salvage step remains the open PT-03
  item** (retry procedure written into the checklist).

**Open for the user after this session:** PT-01 longer silence-watch (cadence and
necropsy already good; the watchdog self-reports if the wedge recurs); PT-03 F45
retry (checklist procedure; the sweep line should report both counts on load);
PT-41 (F66 reclaim); rest of the merged-pack checklist; PT-36/37/38 gates;
MarsDebug attended [install] pass for wave-4/5.

**F18 open half CLOSED (2026-07-26, user-driven):** the user asked whether
resetting the tech was the easy fix; the investigation it prompted found better —
the stored modifier is keyed by the effect object and the shipped applier passes
the tech preset as parent (`GameEffect.lua:36-40`), so a LoadGame sweep re-runs
`effect:OnApplyEffect(UIColony, tech)` argument-identically to research and
replaces the stale -10 with -20 in place. No reset, no re-research, no first-load
flag (state-detected, idempotent). Probe extended to drive the sweep both ways.
F18 status is now plain `fixed`.

**User decision 2026-07-26 (D01 export half): match the ORIGINAL game, not a new
design.** Spec = the legacy loader (RocketBase.lua:1729-1736: standing
PreciousMetals demand to max_export_storage, any-drone flags, per-rocket
allow_export toggle). Build queued for a build leg with three research items
(toggle mapping onto UniversalRocket, modern sell-on-arrival path, whether the
original auto-offloaded RC transports — decides if F56's behavior rides along);
own probe + playtest item; same ClassicRockets flag. Details on the D01 entry.

## QA session (waves 4+5) — Fable, 2026-07-25 evening: merge + audits + A/B CLEAN

**Task 0 — merge:** `wave4` merged to main in BOTH repos with zero conflicts (fix pack
2f09133, TestKit 17f7b3c), worktrees removed, branches deleted, fix pack pushed. The
commented-out F10 metadata line survived. 21 new modules → 68 metadata entries,
67 registered modules.

**Task 1 — parse sweep + A/B pair:** all 80 Lua files in both mods parse. Logs in
`%AppData%\Surviving Mars Relaunched\logs`:

| Leg | Log (Mars.exe-20260725-…) | Result |
|-----|---------------------------|--------|
| Baseline (pack code list emptied) | 22.46.34 | 1 PASS, **57 FAIL**, 12 SKIP, 0 ERROR — every armed probe FAILs |
| Full pack | 22.48.50 | **58 PASS, 0 FAIL**, 12 SKIP — exposed the F75/F18 status-relabel defects (fixed, cdff2ce) |
| Verification (status repairs in) | 22.52.57 | **66/67 active** (ClassicRockets opt-in inactive), **58 PASS, 0 FAIL, 12 SKIP, 0 ERROR** |

The 12 SKIPs: 10 `[install]` probes (retail sandbox — MarsDebug pass covers them),
ClassicRockets (opt-in, verified separately in the wave-3 opt-in leg), and
TechDescriptionBuilding (below). Non-Flight `[LUA ERROR]`s present in BOTH legs are
synthetic-map GameInit noise in shipped files (BuildingWayPoints/TaskRequest/GridObject);
nothing names an SMR file. A `[mod] Error in mod … Test Kit` line at quit time is a
shutdown artifact (fires at the harness's own `quit()`, exit code 0, results complete).

**The two wedged legs (21.01.55 and 22.29.10) were a TestKit probe defect, not the
game:** the TrainWaitTime probe faked the sleeping `PlayPrg` as a no-op, so the shipped
`while self.holder == vehicle do self:PlayPrg() end` ride loop span without yielding and
starved EVERY Lua thread — including the harness watchdog (why it never fired) and the
log writer (why the logs looked empty; the buffer only flushes at exit). Repairs
(TestKit bafbd61 + 80de593): the fake now ends the ride; the harness flushes the log
per line so a killed run keeps its evidence; `ShowStartGamePopup` is neutered when the
autorun is armed (the "Welcome to Mars, Commander!" popup was on screen but was NOT the
wedge); watchdog raised to 15 min. **Engine-fact lesson: a probe must never fake a
blocking primitive as a no-op inside a driven loop.**

**Task 2 — probe discrimination:** 19/20 wave-4/5 probes FAILed baseline → PASSed
fixed: RocketInteractGuard, TrackConnectorPingPong, TrackTunnelPowerBridge,
GridGlobalStorage, LastTransmissionStorage, TrainWaitTime, GraphConsumedCaption,
MoraleComfortTooltip, ReplaceTechCount, StorageRateModifiers, SequenceLatents,
FounderTraitNotification, IndependenceTerraforming, TrackSalvageRefund, LayoutTechLock,
TrainMinors, DroneTransportMinors, AnomalyCaveInMap, BombardmentSpread. **Not
discriminating: TechDescriptionBuilding** — SKIPs both legs ("the tech has no
description T": the probe finds `TechDef.UndergroundLargeDome.description` is not a
table at probe time). F25 is therefore NOT probe-verified; its playtest item is the
evidence path (or a console read of the description). F24 has no probe by design
(PT-44). FactionFundingCheck PASSes both legs as always (F10 retired, PT-36 gate).

**Task 3 — audit fan-out (14 read-only subagents, every verdict verified before
action):** CLEAN: F20, F21, F22, F24, F74 (premises held; only LOWs). Findings that
led to repairs, all landed and covered by the final A/B:
- **F57a HIGH (live game-breaker):** `rfRestrictorRocket` is a FILE-LOCAL
  (DroneControl.lua:12); the replacement read it as a global and raised on every
  rocket-restrictor update → drones would stop servicing rockets. Repaired 493f054.
- **F28 MEDIUM:** the dropped `assert(tech_def.group == status.field)` was load-bearing
  through its ARGUMENT (raises on unknown tech_id_new BEFORE mutation); the copy mutated
  first. Guard restored b66995f.
- **F26 HIGH (dead fix):** preflight checked BombardMissile for methods declared on
  BaseMeteor (invisible pre-flattening — the F64 lesson AGAIN) and required the
  SessionRandom GameVar at apply time; the fix could never activate. Repaired 11ecd22.
- **F75 HIGH + F18 sibling:** preset-patch fixes relabeled themselves
  "inactive: already correct" when the engine's post-DataLoaded `DataChanged(false)`
  reran them over their own corrections; F75 also bypassed the SMRFixPack_Disabled veto
  in its OnMsg path and misread the EMPTY pre-DataLoaded GlobalMap as a vanished
  target. Repaired 11ecd22 + cdff2ce. **Engine fact: `Msg("DataChanged", false)` fires
  right after every DataLoaded (Dlc.lua:715-717, :680-685); FactionDefs/TechDef
  GlobalMap tables exist EMPTY before DataLoaded.**
- **F43 HIGH (latent):** `IsValid()` on pure-Lua InitDone controllers is always falsy
  (C-side check; cf. RealTimeCommandObject's own override) — the teardown was dead code
  and would have leaked the cursor object when a tech-gated layout entry ever goes
  live. Guard dropped 11ecd22. **Engine fact: IsValid() rejects pure-Lua objects, not
  just probe stand-ins.**
- **F31 MEDIUMs:** the divergence paragraph's marsquake claim was FALSE (every engine
  TriggerCaveIn call is already Underground-gated, Marsquake.lua:285/:294/:323-325) —
  corrected in place; and the 8th call site crashes inside `FindCaveInLocation`
  (CaveInRubble.lua:27) before the wrapper — a second decline-wrapper now covers it
  (11ecd22, 8/8 sites).
- **F49:** (d)'s rationale was backwards (GameInit is DEFERRED, _object.lua:187-192 —
  the surviving track is the real defect, which the fix covers) and coverage gaps via
  AutoConnectTracks/instant-build reuse are recorded as accepted (sweep corrects on
  load); (c) implemented per the user's decision (below); (b)(e) screenings verified
  sound. F20/F74 wrappers got vararg pass-throughs (§1.4).
- **F65 HIGH:** the 2-element special deletion path (TrackConnectedObjBase:Done,
  TrainTransport.lua:24-27) DoneObjects the track with NO DisconnectFromGrids — and
  only F65 ever creates a bridged 2-element track, so demolishing an endpoint leaked
  tunnel mask/adjacency into the save. Repaired 8e0b177: TrackBase:Done is pre-wrapped
  to run the shipped DisconnectFromGrids (tolerates a dead endpoint by design;
  RemoveSupplyTunnel clears the flag so demolish-path double-calls no-op). The
  MEDIUM (different-grids test is one-shot; cable-topology declines re-check only on
  next load's sweep) is documented as accepted in the fix header.
- **F47 MEDIUMs (recorded, NOT yet repaired — both under-refunds, no over-refund/save
  hazard):** F44's trim-to-empty exit skips the refund (composition gap), and the
  construction-site early-return is broader than repair sites. On the list for a
  future leg.
- **F66 MEDIUM (recorded, awaiting user decision):** after the blocking neighbour is
  demolished, the guarded building never reclaims the connector hex (no rebuild
  trigger reaches it) until any track demolish fires the global rebuild or it is
  re-placed. Options given to the user: accept+document vs a demolition-path rebuild
  trigger.
- Recurring minors: full-replacement headers date the copy instead of naming the game
  version (FIX_POLICY §1.5) — release-checklist item; assorted citation drift fixed.

**User decisions recorded this session:** F42 CLOSED `wontfix`; F49(c) = "the click
does nothing", implemented.

**Playtest findings processed live (first sitting, wave-3 pack):** PT-02 PASS, PT-04
PASS (status flips belong to the playtest-report session). **PT-03 F44 curve FAIL →
diagnosed and REWORKED (a38cbf2):** the split branch could delete a physically
scattered zone whenever sorted order diverged from physical order (exactly the
non-numeric node_idx state the old comparator sorted as -1 and carried on with),
stranding orphaned elements (track_obj == false) that raise on every later click —
the user's "broke itself, became immune" with screenshots. Now: orphan clicks delete
the debris, the salvage declines BEFORE deleting anything when order can't be trusted,
the split tail is IsValid-guarded, and a LoadGame sweep removes orphans already baked
into saves (the user's playtest save will log `TrackSalvageWipe: removed N orphaned
track element(s)`). **PT-03 needs a re-run.** PT-01 (meteors stopped after sol ~12.5,
FAIL) is NOT yet diagnosed — first question is whether the user reloaded during the
quiet stretch (every load re-rolls the 65-90h Low-threat interval; frequent reloads
legitimately push strikes out). If they didn't reload, F02 has a real regression to
find.

**Commits this session (fix pack):** 2f09133 merge, b66995f F28, 493f054 F57a,
09af088 playtest notes, 11ecd22 audit repairs, 8e0b177 F49c+F65, 75c54f6 doc
corrections + F42 (NOTE: accidentally committed the baseline's emptied metadata via
`commit -a`; restored in 1321795 — never use `-a` while an A/B leg's metadata edit is
in the working tree), a38cbf2 F44 rework, cdff2ce F75/F18 status. TestKit: 80de593
harness hardening, bafbd61 probe wedge fix + 15-min watchdog.

**Open after this session (both user answers now in, 2026-07-25 late):**
- **PT-01: NO reloads** → F02 is genuinely regressed (meteors stopped for 560+ game
  hours on a max-threat map after Sensor Towers went up) — REOPENED `fixed*`,
  investigation speced in docs/FABLE_NEXT_PROMPT.md Task 1.
- **F66: user chose the rebuild-trigger repair** over accept-and-document — spec on
  the F66 entry + docs/FABLE_NEXT_PROMPT.md Task 2.
- PT-03 re-run (user, next sitting); F47 composition under-refunds; MarsDebug
  [install] pass for wave-4/5 (attended, SetupOnly); game-version tags on
  full-replacement headers (release checklist).

## What this project is

"Community Fix Pack" — a runtime-Lua bug-fix mod for Surviving Mars: Relaunched
(game dir `A:\SteamLibrary\steamapps\common\Project Spark`, Haemimont Sol engine,
NOT Unreal; full gameplay source shipped in `<game>\ModTools\Src`). No game files
are modified; planned community release after user testing. Dev repo:
`C:\Dev\SMR-BugFixPack` (git). Installed via junction at
`%AppData%\Surviving Mars Relaunched\Mods\SMR-BugFixPack`.

Companion **Test Kit** mod (never shipped): `C:\Dev\SMR-BugFixPack-TestKit` (git).
`SMRTest.RunAll()` runs one probe per fix and prints PASS/FAIL/SKIP; run it with
the fix pack disabled (expect FAILs) and enabled (expect PASSes). It also enables
the Lua console at load and carries observability loggers and state reports.

## Discovery: COMPLETE

- 73 tracked findings (~85 distinct defects) verified against the CURRENT
  (post-1.0.7) shipped source, each with file:line evidence + fix sketch in BUGS.md.
- 1 design-change verdict (D01 rocket auto-refuel/rare-metals — plan opt-in module).
- 2 candidates needing runtime checks (C01 BreakthroughOrder, C02 asteroid cave-ins).
- 3 critical UNTRACED leads (RESEARCH.md): 90%-breathable-atmosphere freeze,
  Last War mystery import lock at 54%, game-stops-saving. Plus smaller new leads
  from the ChatGPT dossier cross-check (top of RESEARCH.md).

## Implementation: 47 tracked defects DONE across 46 registered modules (ALL probe-verified in-game 2026-07-25 — wave-3 A/B pair clean, see the QA session section; F10 retirement STAGED 2026-07-26, premise falsified, final wontfix gated on PT-36)

Wave 1 (earlier session): F01 cave-ins/NoDisasters, F02 meteor frequency,
F03* upgrade-modifier leak, F04 night shift, F05 milestone crash, F07+F15* wisp
power/rewards, F08 tourist applicants, F10 faction funding, F64 trains-to-void.

Wave 2 (earlier session, in queue order): F67 lander empty launch, F68 lander cargo
ratchet, F69 lander return fuel, F73 shelter reflex, F45 broken-track salvage,
F44 track salvage wipe, F30 lake entombment, F37 ghost farm oxygen, F50 rocket
drone churn, F51 shuttle transport cache, F52* vacuum walks, F53 arrival deaths,
F55* drone unreachable-forever, F58* stale reservations, F61 home-dome migration
gate, F06 crystal mystery hang, F09 tourist satisfaction, F11 train platform
wedge, F12 low-storage warning, F13 Command Center numbers, F14 Domes Overview
highlight.
(* = partial; the remaining half is recorded on the BUGS.md entry.)

Wave 3, first leg (session 3, in queue order): F46 train cargo dumping, F36 university
overtraining, F38 destroyed tunnels, F39 second artificial sun, F40 Dust Sickness on
Biorobots, F17 Dust Sickness randomization, F41 Gene Forging, F16 Mirror Sphere site,
F70 Edit Payload template refill.

Wave 3, second leg (session 4, in queue order): **F71** auto-export capacity priority
(folded into `Fix_LanderCargoRatchet.lua` — F68 already replaced that function),
**F72** asteroid-lander availability gate, **F54** switched-off shuttle hubs,
**F59*** freed housing notifies the homeless, **F60** dome free-space member mismatch,
**F33** small landscaping site drone crash, **F34*** landscape units-underneath filter,
**F35 + F03 sweep** in the new `Code/90_SaveSanitizer.lua`, and **D01** as the opt-in
`Code/Opt_ClassicRockets.lua` (fuel half only).
(* = partial; the remaining half is recorded on the BUGS.md entry.)

**The whole wave-3 queue is now done.** Nothing from the session-3 handoff list is left
except the four entries deliberately parked as `blocked` (see below).

**Wave-3 fixes are now probe-verified in-game (2026-07-25 QA session):** the RunAll A/B
pair ran clean — every armed probe flipped FAIL→PASS, 46 fixes + sanitizer `applied`,
ClassicRockets `inactive` by default and `applied`+PASS in the opt-in leg. Full results
in the "QA session (wave 3)" section below.

Three first-leg fixes add their own `OnMsg.LoadGame` repair pass: F38 (close destroyed
tunnels left open in pathfinding), F39 (reconnect solar panels to a sun in range), F40
(clear Dust Sickness from already-infected Biorobots).

`Code/90_SaveSanitizer.lua` now exists and carries the remaining consolidated sweeps:
**F35** (restore the Frictionless Composites label modifiers the shipped migration fixup
dropped) and **F03** (remove upgrade modifiers orphaned by salvaged buildings). Both are
idempotent, both run on **`OnMsg.PostLoadGame`** (NOT LoadGame — the QA audit found that
`Msg("LoadGame")` fires BEFORE `FixupSavegame`, `Savegame.lua:810-813`, so a LoadGame-time
F35 pass raced the shipped turbine fixup and could bake +200% onto Shrouded turbines on a
never-patched save's first load; see the F35 entry), and both are exposed on
`SMRFixPack.Sanitizer` so QA can re-run them from the console (`RepairTurbineBuff` /
`RepairLeakedUpgradeModifiers`, each returns a repair count). **F48 is NOT in it** — see
its BUGS.md entry.

Other fixes carrying their own one-shot `OnMsg.LoadGame` / `OnMsg.NewDay` pass for state
already baked into savegames: F02 (thread restart), F45 (stamp repair sites), F37 (remove
phantom farm oxygen), F58 (release stale reservations), F06 (restart the crystal repeater),
plus F55's expiry which self-heals.

**Savegame footprint** (FIX_POLICY §3 — all absent-tolerant): `colonist.SMRFixPack_reserved_at`
(F58), `transporter.SMRFixPack_payload_set` (F70), an entry keyed `smr_shuttles` on a
transport-cache entry (F51, a hash key that does not affect `table.unpack`), and — only
where the sanitizer repaired one — a label modifier under `SMRFixPack_F35_<label>` (F35).
README's old "stores nothing in your savegames" claim has been corrected accordingly.

## Optional modules (new in session 4)

Off by default, enabled with `SMRFixPack_Optional = { <Id> = true }` before the mod loads;
`SMRFixPack.ListFixes()` reports them as `inactive` with the opt-in reason until then.
Files use an `Opt_` prefix instead of `Fix_` to mark them as not-bug-fixes.

- **ClassicRockets** (D01, `Code/Opt_ClassicRockets.lua`) — a player-controlled rocket
  parked at the colony keeps its launch ration requested even with no destination selected,
  so drones refuel it while it waits. Only the fuel half of D01; the standing Rare Metals
  export half is deliberately unwritten (see the D01 entry).
  **This module is also where F56 would land** if the closed-`wontfix` auto-offload
  decision is ever reopened (user decision 2026-07-26): auto-offload and the export half
  are the same "rockets should load and unload themselves like they used to" request over
  the same machinery, so they ship together behind this one flag or not at all. Do not
  create an `Opt_AutoRocketOffload`.

## QA session (wave 3) — Fable, 2026-07-25 evening: A/B pair CLEAN, audits done

All four RunAll legs unattended via `-smrautorun` (Steam `-applaunch 3215050`); a
Python `luaparser` pre-pass first proved all 57 mod Lua files parse (no file-level
load failures possible). Logs in `%AppData%\Surviving Mars Relaunched\logs`:

| Leg | Log (Mars.exe-20260725-…) | Result |
|-----|--------------------------|--------|
| Baseline (pack code list emptied) | 16.19.54 | 1 PASS, **38 FAIL**, 11 SKIP, 0 ERROR — every armed probe FAILs, all discriminate |
| Full pack | 16.22.38 | **39 PASS, 0 FAIL**, 11 SKIP — 46/47 active + ClassicRockets `inactive` (expected); found the ModLog `%` defect (below) |
| Opt-in (`SMRFixPack_Optional.ClassicRockets`) | 16.28.35 | **40 PASS, 0 FAIL**, 10 SKIP — ClassicRockets `applied`, its probe asserts; F69 chain intact |
| Final verification (default config, repairs in) | 16.31.30 | **39 PASS, 0 FAIL**, 11 SKIP, zero errors from our code |

(The ~49 `[LUA ERROR] Flight.lua objects_to_mark` blocks per leg are engine noise on
the synthetic map — present in the baseline too, not ours.)

**Defects found and repaired this session (all verified by the later legs):**
1. **HIGH — SaveSanitizer fixup race** (subagent audit, verified first-hand): pass moved
   `OnMsg.LoadGame` → `OnMsg.PostLoadGame`; see the F35 BUGS entry. Not probe-coverable
   (needs a real never-patched save — PT-35 case C).
2. **ModLog re-formats its message**: `ModPrint` is a printf-style `CreatePrint`
   (Mod.lua:109-113 + lib.lua:164-174), so a literal `%` in an already-formatted message
   raises `[LUA ERROR] string.format` — three per fixed leg (sanitizer "+100%" lines,
   TurbineBuff PASS line). All four log helpers now escape `%` for the second pass
   (fix pack 00_Core + 90_SaveSanitizer; TestKit 00_TestCore + 95_AutoRun, whose
   "ModLog is %-safe" comment was WRONG — corrected). **Engine-facts correction.**
3. **F35 amount now scaled** via `GetModifiablePropScale` (dormant hardening, matches
   Tech.lua:298-301).

**Spot-audits of the six highest-risk wave-3 divergences (subagent fan-out, each
verified against Src):** F59 CLEAN (ordering + assert-race claims true; recursion
bounded — homeless have `residence == false`), F71/F68 CLEAN (body diff exact; pcall
degrades to shipped alphabetical order; reorder provably cannot drop or starve a
resource), F72 CLEAN (strict pass-through; scan is an exact subset of
GetRocketsForExpedition incl. supply-pod exclusion), F54 CLEAN (full reason-state
enumeration found a FIFTH string `ExceptionalCircumstancesMalafunction` (sic) —
provably never admitted, malfunction forces GetWorkNotPossibleReason truthy), F34(d)
CLEAN (params table matches shipped; engine never mutates it; per-call dedup),
SaveSanitizer = the HIGH defect above, now repaired. Recurring minor: header/BUGS
line-number drift (off-by-ones, catalogued in the session transcript — cosmetic).

**Probe-discrimination sweep (Task 2):** ground truth from the pair — every armed
probe FAILed baseline and PASSed fixed except **F10 `FactionFundingCheck`**, which is
**fundamentally non-discriminating**: the baseline drove the shipped body over 240 nil
hours and it returned 0 — **this engine tolerates `pairs(nil)`** (new engine fact,
consistent with the `next(nil)` tolerance). F10's defect premise is falsified; entry
updated, probe PASS message now says "not evidence". Decision for the user below.
The rewritten F51 probe now discriminates (FAIL→PASS observed). 10 `[install]` probes
still SKIP on retail — the MarsDebug.exe pair remains the missing coverage.

**MarsDebug [install] pass (2026-07-26, attended) — FULL COVERAGE, 49 PASS / 0 FAIL /
0 ERROR** (1 SKIP = ClassicRockets opt-in, verified separately in the opt-in leg). Logs:
MarsDebug.exe-20260725-17.40.38 (baseline, installs SKIP — see below) and -17.46.04
(fixed, attended). All 10 `[install]` probes PASS with real verdicts, and **F73's Idle
pre-wrapper half is verified** ("Idle carries the shelter branch") — the last unverified
wiring in the pack. Install-probe baselines are FAIL-by-construction (they test function
provenance), so the attended fixed leg alone completes the coverage.
Three facts corrected/learned doing it:
- **The mod sandbox applies on ALL builds including MarsDebug.exe** — the wave-2
  assumption that an asserts build un-sandboxes mod code is WRONG. An asserts build
  unsandboxes the CONSOLE (g_ConsoleFENV reads real `_G`, console.lua:36-44), and
  `ConsoleExec` is on the ModEnvBlacklist (Mod.lua:1285), so the introspection bridge
  cannot be automated — it is typed: `SMRTest.EnableIntrospection(debug)` then
  `SMRTest.RunAll()`.
- The TestKit autorun now has a flag-gated **SetupOnly mode** (95_AutoRun +
  96_AutoRunFlag comment) that builds the colony and hands the session to the human —
  the attended-leg harness.
- **The debug build pops MODAL dialogs for asserts** — the first is the known vanilla
  `Flight.lua:465 objects_to_mark` noise; click **Ignore All** or the run blocks (and
  the 8-min watchdog can then expire; harmless, relaunch).

**D01/ClassicRockets (Task 4):** default-off / opt-on / no-spam claims all verified;
the no-spam citation in the Opt file pointed at the wrong file (the `arrival_loc`
gates live in the UniversalRocketBase override, UniversalRocket.lua:1687-1692) —
corrected; a third benign `Msg("RocketRefueled")` path via DroneUnloadResource is
now documented in the file. MOD_DESCRIPTION wording tightened so the module text
cannot be read as promising the unwritten Rare Metals half.

## QA session snapshot (Fable, 2026-07-25) — kept for the audit record

**NOTE — everything actionable below is RESOLVED:** the F53 and F12 reworks
LANDED (commits aa980e7 / 40d5a73) and survived the final A/B pair; the autorun
harness IS committed (TestKit); the RunAll pair HAS run clean — see the FINAL
A/B section above. Still open from this section: F68 capacity-cap in-game check,
F44 curve-ended track visual check, wave-1 heading tags.

- BUGS.md index was stale (16 wave-2 rows said `todo` despite tagged headings) —
  synced in commit 0ef4e7c. README/MOD_DESCRIPTION verified complete. Follow-up:
  wave-1 detail headings (F04/05/07/08/10/15/64) lack the `[fixed]` tag.
- Nothing was marked `blocked` in the build session. F55's "open-air entrance half
  not actionable" verdict was re-verified and is CORRECT (CalcOpenAirSkin only
  empties skin[2] configurable attaches; Dome_Entrance is entity-spot auto-attach
  data, Dome.lua:404 — not patchable from Lua). F55 drone half diffs clean.
- Spot-audit of 6 fixes (F61, F12, F44, F53, F68, F73) — full reports in the
  session transcript; summary:
  * **F53 CRITICAL — rework before release.** The `not IsInWalkingDist` gate in
    Fix_ArrivalDeaths.lua is always true for cross-map elevator destinations
    (IsInWalkingDistDome returns false when maps differ, Dome.lua:248-251), so
    every legitimate elevator arrival triggers the re-choose; the re-choose
    discards ChooseDome's elevator return and never clears stale
    self.emigration_elevator → TransportByFoot rides the stale elevator, fails
    the map-slot check (Colonist.lua:2731) → SetCommand("Abandoned"). Repair:
    skip the gate when ValidateBuilding(self.emigration_elevator) routes to
    dome; on re-choice take BOTH returns and assign emigration_elevator.
  * **F12 MODERATE — rework.** Post-wrapper leaves shipped dead branch removing
    the notification hourly, wrapper re-adds → destroy/recreate churn + FX replay
    every game hour while active; dismiss/suppression semantics differ. Docs
    prescribe full replacement — do that instead.
  * **F68 MODERATE — verify in-game.** The requested-floor (belt-and-braces
    block) doesn't debit hold capacity: with multiple exports, an alphabetically
    earlier resource's request can exceed remaining capacity → status stuck
    "loading", automode rocket sits on pad (departure gate needs "ready").
    Consider capping the floor against remaining capacity.
  * **F61 CLEAN**, **F44 CLEAN** (in-game check: curve-ended remainder track
    visuals; F45-comparator fold-in disclosed), **F73 CLEAN** (note:
    IsSuitable is AutoResolveMethods "and"-combined with Residence.IsSuitable —
    correct today, document it; partial-application isn't reported in the log).
  * Recurring minor: header/BUGS line-number drift (off-by-ones); apply()
    self-checks don't pre-check every runtime symbol.
- AccountStorage research (for the RunAll pair): enabled mods live in
  AccountStorage.LoadMods (plain array of metadata.lua `id` strings), persisted
  in `%AppData%\Surviving Mars Relaunched\<SteamID64>\account.dat` — an
  in-memory HPK (magic BPUL) containing `account.lua`, AES-encrypted+HMAC with
  key SHA256(GetAppId()..config.ProjectKey), compressed. BUT the loader is
  best-effort: a plaintext `return {...}` account.lua inside the container still
  loads (lib.lua:2187-2216). Edit only with the game closed; ids for missing/
  too-old mods are auto-stripped at menu (Mod.lua:2033-2059). Escape hatch:
  `AccountStorage.LoadAllMods = true` loads every discovered mod, bypassing the
  list. Unpacked mods in Mods\ need metadata.lua with `id` + `lua_revision` ≥
  350453. No Paradox cloud sync of account.dat (CloudSavesAllowed() = false).
- RunAll before/after pair NOT run: the Relaunched profile has never been created
  (%AppData%\Surviving Mars Relaunched\ has only Mods; no saves/logs/AccountStorage;
  no Steam userdata for appid 3215050) and mods can't be enabled until first launch.
  TestKit is now junctioned next to the fix pack. An opt-in autorun harness
  (TestKit Code\95_AutoRun.lua: flag-file gated, auto new game via
  NewGame/InitNewGameMissionParams/LoadLastNewGameSettings + fill g_CurrentMapParams
  + GenerateCurrentRandomMap, then RunAll with [SMRAUTO] markers, watchdog, quit())
  was being built when the session ended — it is NOT committed; check the TestKit
  repo before relying on it. Retail exe ignores -save/-map (goldmaster-gated,
  autorun.lua:126-144); Mars.exe launches directly, no external Paradox launcher.

## Parked by decision, not by effort — one entry left open (F48)

Each has a full write-up on its BUGS.md entry. None was parked for effort; each was parked
because the remedy is not a defect repair, or because the shipped code no longer matches
the tracker. **Only F48 is still open** — the other four are closed.

| ID | Why it is parked | What would unblock it |
|----|------------------|------------------------|
| **F56** | ~~blocked~~ **CLOSED `wontfix` 2026-07-26 (user decision), same grounds as F62/F63.** Screened in the wave-4 build leg: the cited code is designed scope (`GetAutoGatherDeposits` is a declared accessor; the `Automation_Unload` rocket exclusion goes through the Relaunched `IsRocketClass` shim, i.e. maintained intent; auto mode promises only "gather resources"). **No standalone opt-in** — if revisited it belongs in `Opt_ClassicRockets` beside D01's unwritten export half, never in an `Opt_AutoRocketOffload` of its own. | — done. Rides on whatever design decision D01's export half gets, or stays closed. |
| **F32** | ~~blocked~~ **CLOSED `wontfix` 2026-07-26 (user decision).** The shipped data already carries the fix (`NotWorkingBuildings` is now `Suppressable`); the other two presets are one-shot adds. The residual by-design annoyance (2-real-minute window, per-category suppression, no per-building ack) is spun out as **D02** — a planned `Opt_AcknowledgedWarnings` module, gated on **PT-38**; MOD_DESCRIPTION carries a player-facing "looks like a bug, isn't" explainer. | — done. D02 build belongs to a wave-4+ leg after PT-38. |
| **F42** | **NEW, wave-5 screening.** `blocked` — wontfix candidate. The tracked observation is entirely correct and does not add up to a defect: the guard it names exists to stop units being entombed, a dust devil has no footprint to be entombed in, the omission sits in declared overridable class members, no shipped text promises the block, and the game's one weather-gated placement rule (`RocketLandingDustStorm`) is implemented and working. Full write-up on the entry. | **A user decision.** Recommend `wontfix` on the F56/F62/F63 grounds. |
| **F48** | Mechanism confirmed, but the corrected call runs `OrderTrackElements`, which clears and rebuilds `el.connections` and rewrites `node_idx` on **every element of every track**, with a non-unwinding `assert` as its only failure handling. Too invasive to ship untested for a P3. | **PT-37** (added 2026-07-26) — exact console steps for the healthy-network + meteor-damaged-track test, on the user's in-person list. PASS → sanitizer behind a one-shot flag; FAIL → `wontfix`. |
| **F62** | ~~blocked~~ **CLOSED `wontfix` 2026-07-26 (user decision).** Verified identical to the original game (same one-hop algorithm, same two transitive-predicate callers): carried-forward dev vision in both games, breaks nothing. No opt-in module planned. | — done. |
| **F63** | ~~blocked~~ **CLOSED `wontfix` 2026-07-26 (user decision), same grounds** — no training term ever existed in either game's emigration score. | — done. |

Recorded on those entries but deliberately untouched (real inconsistencies, no action):
walkability says A↔C is walkable while services say C is invisible from A;
`CanWorkTrainHereDomeCheck` permits training at a train-reachable school that
`ChooseTraining` never offers; the `PlanetaryAsteroidVisitPossible` legacy branch's
`and`/`or` precedence slip; `IsDifferentAsteroidLocation` comparing a map to a
MapDescriptor. All are permissive failures — none blocks a player.

## Wave 4 — build leg DONE (branch `wave4`, NOT merged, NOT probe-run)

**14 new fix modules, 13 new probes, 6 new playtest items (PT-39..PT-44).** Everything
lives on the `wave4` branch in `C:\Dev\SMR-BugFixPack-wave4` and
`C:\Dev\SMR-BugFixPack-TestKit-wave4`; main is untouched, the game was never launched, and
**no probe has been run** — the A/B pair belongs to the wave-4 QA leg
(`docs/FABLE_QA_PROMPT.md`), which also performs the merge.

Implemented, in queue order:

| ID | Module | Note |
|----|--------|------|
| **F74** *(new)* | `Fix_RocketInteractGuard` | found by screening F56; the shipped guard at `RCTransport.lua:341` names only the pre-Relaunched trade/refugee classes |
| **F66** | `Fix_TrackConnectorPingPong` | enforces the invariant the shipped assert only states |
| **F65** | `Fix_TrackTunnelPowerBridge` | bridges only when the two stations demonstrably sit on different grids; PostLoadGame sweep |
| **F22** | `Fix_GridGlobalStorage` | one ratio over summed inputs instead of a sum of ratios plus a sentinel |
| **F75** *(new)* | `Fix_LastTransmissionStorage` | found by implementing F22; six conditions were on `Prerequisite`, which `Eval` never reads, and the Oxygen one measured Power |
| **F19** | `Fix_GraphConsumedCaption` | caption counts maintenance, like the bar |
| **F20** | `Fix_MoraleComfortTooltip` | hides the one row `UpdateMorale` no longer grants |
| **F21** | `Fix_TrainWaitTime` | full replacement — `BoardVehicle` blocks for the whole ride |
| **F23** | `Fix_FounderTraitNotification` | additive handler beside the dead one |
| **F24** | `Fix_DomePipeMoveInside` | `dome` → `self`; no probe, PT-44 covers it |
| **F27** | `Fix_StorageRateModifiers` | three post-wrappers |
| **F28** | `Fix_ReplaceTechCount` | entry title corrected: no crash is claimed, only that the line is wrong either way |
| **F29** | `Fix_SequenceLatents` | `fixed*` — items 1 and 3; item 2 is a Mod Editor code generator, deliberately left |
| **F18** | `Fix_IndependenceTerraforming` | `fixed*` — preset half; already-researched saves keep 10% |

**Screened and CLOSED `wontfix` (user decision 2026-07-26): F56.** Screening before
implementing found designed scope, not a defect — `GetAutoGatherDeposits` is a declared
accessor, the `Automation_Unload` rocket exclusion goes through the Relaunched
`IsRocketClass` shim (i.e. a developer consciously re-stated it for the new class tree),
and auto mode promises only "gather resources". Closed on the same grounds as F62/F63:
deliberately maintained design, breaks nothing. **No standalone opt-in is planned** — if it
is ever revisited it belongs in `Opt_ClassicRockets` beside D01's unwritten Rare Metals
export half, not in a module of its own (same request, same machinery, and shipping them
apart would let a player enable emptying without refilling). Full write-up on both entries.

**Still `todo` after wave 4 — eight entries, the P2/P3 tail:** F25, F26, F31, F42, F43,
F47, F49, F57. ~~Suggested order for a wave-5 build leg~~ **All eight were taken in wave 5
— seven implemented, F42 screened to `blocked`. Nothing is `todo` any more.** The `fixed*`
partials whose open half is recorded on the entry are now: F15, F18, F29, F34, F49, F52,
F55, F57, F58, F59.

**Every wave-4 fix is unverified in-game.** The four full replacements (F66
`CreateConnectorElements`, F21 `BoardVehicle`, F24 `MoveInside`, F28 `ReplaceTech`) and the
one global-function replacement (F22 `GetGridGlobalStorage`) are the highest-risk items for
the QA audit; F20's per-call instance `GetProperty` override and F65's PostLoadGame sweep
are the two most unusual techniques in the pack and deserve a look.

## Wave 5 — build leg DONE (branch `wave4`, NOT merged, NOT probe-run)

**7 new fix modules, 7 new probes, 3 new playtest items (PT-45..PT-47).** Everything lives
on the `wave4` branch beside wave 4's; main is untouched, the game was never launched, and
**no probe has been run** — the A/B pair belongs to the QA leg, which covers waves 4 and 5
together. **The BUGS.md `todo` queue is now empty.**

| ID | Module | Note |
|----|--------|------|
| **F47** | `Fix_TrackSalvageRefund` | sums every construction group's stamp instead of reading one; + partial-salvage refund |
| **F43** | `Fix_LayoutTechLock` | latent — no shipped layout has a tech-gated entry |
| **F49** | `Fix_TrainMinors` | `fixed*` — items (a) palette and (d) train cap; (b)(c)(e) screened, see the entry |
| **F57** | `Fix_DroneTransportMinors` | `fixed*` — (a) latent restrictor leak and (b) the unreachables table; (c) would undo F61 |
| **F31** | `Fix_AnomalyCaveInMap` | guards the argument, not the environment — the sketch's test would have killed marsquake cave-ins |
| **F25** | `Fix_TechDescriptionBuilding` | preset patch reusing the original translation id, so localised builds are untouched |
| **F26** | `Fix_BombardmentSpread` | the pack's **sixth and largest full replacement** (100 lines) |

**Screened items — both user decisions made 2026-07-25 (wave-4/5 QA session):**
- **F42** (buildings placeable on active dust devils) → **CLOSED `wontfix`** on the
  F56/F62/F63 grounds: the guard it names exists to stop units being *entombed*, a dust
  devil has no footprint and cannot be trapped, the omission is in declared overridable
  class members, and no shipped text promises the block.
- **F49(c)** (a salvage click on a station's connector hex reaches the station) →
  **user chose "the click does nothing"; IMPLEMENTED** in `Fix_TrainMinors.lua` as a
  demolish-mode pre-guard on `TrackGridElement:SelectionPropagate`.

**Every wave-5 fix is unverified in-game.** Highest-risk items for the QA audit, in order:
**F26** (100-line copy of `WaitBombard` — mechanically diffed against the shipped body,
identical apart from the function header, the dropped non-unwinding `assert`, and the one
`-- FIX:` line, but it replaces a whole disaster path); **F47's** partial-salvage wrapper on
`TrackGridElement:Demolish` (places resource stockpiles from a before/after snapshot);
**F49's** replacement of the global `ExpandTrackFromElement`; and **F43's** teardown of
live construction controllers inside a post-wrapper on `Activate`.

**New engine facts learned this leg (do not re-derive):**
- **Track is billed per construction GROUP, not per hex.** Groups hold at most
  `const.ConstructiongGridElementsGroupSize` = 5 elements (`_GameConst.lua:480`), and
  `Tracks.lua:463` leaves the leader's `construction_cost_multiplier` at 100 — one
  element's cost per group. Passages do it the other way (`Passage.lua:1969`).
- **`ConstructionGroupLeader:Complete` stamps the group's whole spend onto exactly ONE
  finished element** — the last it completed — after suppressing every member's own
  `MarkSpentResources` (`ConstructionSite.lua:2469`, `:2479-2489`). So
  `construction_cost_at_completion` is one stamp per group, spread along a track. This is
  what F47 turns on.
- **A T can be corrected without breaking translations** by rebuilding it with the SAME
  translation id: localised builds resolve the id and never see the literal, English builds
  fall back to it. Minting a fresh T would push English text into every language (F25).
- **`UndergroundMap` is a GameVar defaulting to `false`** (`RandomMapGenerator_Picard.lua:263`)
  and stays false under the "No Underground and Asteroids" rule — eight scenario call sites
  hand it straight to `TriggerCaveIn`, which indexes it unguarded (F31).
- **Verify every full replacement mechanically.** F26's 100-line copy was diffed against
  `ModTools\Src` with a throwaway Python script that strips comments and whitespace; it
  caught nothing this time, but it is the only way to be sure a copy that large is faithful.

## Key technical facts (hard-won, do not re-derive)

- **Mod code loads BEFORE the classes are built.** `autorun.lua:423` calls
  `ModsLoadCode()`; classes are assembled later in `OnMsg.Autorun`
  (`CommonLua\Core\classes.lua:980`). So at apply() time a class global is still
  its **classdef**, exposing only members the class declares ITSELF — an inherited
  method reads as nil. Two consequences:
  * `function Building:X() ... end` in a fix DOES propagate to every subclass
    (the classdef is what gets flattened later) — this is why class-method
    replacement works at all;
  * an apply() self-check must look for the method on its **declaring** class.
    Checking `Station.OnDemolish` (declared on Building), or
    `UniversalRocketBase.IsAutoModeEnabled` (declared on the AutoMode mixin),
    finds nil and silently deactivates the fix. F64 shipped broken this way and
    was corrected this session.
- `g_Consts` is a **GameVar** (`Lua\Modifiers.lua:427`) and does not exist while
  mods load — read it inside the patched function, never in apply(). `const` IS
  populated at that point.
- Engine Lua tolerates `#nil`/`next(nil)`/`ipairs(false)` (verified from working
  code paths) but NOT boolean relational compares — don't report/fix nil-iteration
  as crashes. `/` truncates (integer division); that is what makes F12's
  `a*24/v*24` unsatisfiable.
- **Mods run in a sandbox (LuaModEnv) on ALL platforms**, including unpacked dev
  mods (Mod.lua:1730/:1750; blacklist at :1267-1428). Key facts: `debug`, `io`,
  `package`, `lfs`, all `Async*` file ops, load/dofile/require are BLACKLISTED;
  `os` is `{time}` only; `setmetatable` is available (:1408 commented out);
  `rawget` is a safe wrapper that reaches real `_G` for non-blacklisted names —
  the pack's `rawget(_G, "X")` pattern works; `_G` maps to the env, but NEW
  globals created at load are rawset into the REAL `_G` (:1557-1563), so
  `SMRFixPack`/`SMRTest` are cross-mod and console visible; `Msg`/`OnMsg` are
  filtered only for persist/debug messages. The fix pack Code/ uses no
  blacklisted API (verified) — sandbox- and console-clean.
- **`error()` and `assert()` do NOT unwind mod code — they report and execution
  continues** with the next statement (LuaExports.lua:567 "asserts pop instead of
  being printed out"). Never use them for control flow; `pcall` still catches
  genuine runtime errors. Cost us four bogus FAILs and ten ERRORs in the first
  A/B pair (see the diagnosis section).
- **`rawset(_G, k, v)` from mod code writes only into the mod's own env table**
  (`_G` IS that table, Mod.lua:1603; `rawset` is the real rawset, only `rawget`
  is replaced at :1606). To write a global the game can see, assign it —
  `_G[k] = v` goes through `ModEnvMeta.__newindex` (:1557-1563) into the real
  `_G`. `rawget(_G, "X")` for READS is fine (safe_rawget falls through, :1577).
- **CORRECTION of an earlier "fact": `debug.getinfo` is NOT available in mod
  code** (debug is blacklisted). The Test Kit's install probes
  (00_TestCore.lua:37) break under the sandbox; repair in progress — bridge
  real `debug` via a console-exec path or SKIP install probes with a
  `SMRTest.debug = debug` console instruction. `GetStaticMsgNames()` (F06 probe)
  is a real global and still fine.
- Patch points that work: `PeriodicRepeatInfo[name]` slots (THREAD/SLEEP/FUNC/COND
  = 1..4, CommonLua\Core\lib.lua:1538+), `GlobalGameTimeThreadFuncs[name]` +
  `RestartGlobalGameTimeThread(name)` on LoadGame (Lua\Config\_fixup.lua),
  class-method replacement, chained wrappers, `OnMsg.*` additive handlers,
  preset/data patches at ClassesPostprocess.
- A post-wrapper on a **command** method (anything ending in `SetCommand`) never
  runs — `DoSetCommand` kills the calling thread. `Colonist:Idle` must be
  pre-wrapped (F73).
- Mod registry: every fix goes through `SMRFixPack.Register(id, {title, apply})`
  (Code/00_Core.lua); apply self-checks the target and returns a reason string to
  deactivate gracefully; `SMRFixPack_Disabled` = user veto; `SMRFixPack.ListFixes()`
  console status.
- All line numbers reference `ModTools\Src`; the game executes `Packs\Lua.fpk`
  (slightly newer date) — runtime self-checks in apply() are the guard.
  `GatherTransportableResources` (`ResourceTracking.lua:216`) is *called* but
  defined nowhere in Src — an engine export or an fpk-only function. F12's fix
  checks for it at apply time.
- Sample mod format in `<game>\ModTools\Samples\Mods`; docs in `ModTools\Docs\index.md.html`.
- **Replacing an EXISTING global from mod code works**: `ModEnvMeta.__newindex`
  (`Mod.lua:1557-1563`) rawsets any non-blacklisted key into the real `_G`, and the
  "attempt to create a new global" assert only fires for names that do not already
  exist there. Generated closures (script conditions, sequence code) resolve the name
  at call time, so they pick the replacement up. Read the name back with
  `rawget(_G, ...)` in apply() to confirm the write landed — F22 does.
- **`OnMsg` is additive, confirmed structurally**: four shipped files each define
  `OnMsg.StationsConnected` (`Station.lua:1213`, `Track.lua:668`,
  `TrainTransport.lua:357`, `UnderconstructionSign.lua:87`) and all four must run.
- **TOOLING: never round-trip a doc through PowerShell 5.1 `Get-Content -Raw` +
  `WriteAllText`.** `Get-Content` without `-Encoding` decodes UTF-8 files as cp1252, so
  every `—`, `↔`, `≤` comes back double-encoded and the whole file shows as changed.
  It happened to `BUGS.md` in the wave-4 session and was reversed with
  `Encoding.GetEncoding(1252).GetBytes(UTF8.GetString(bytes))`; nothing was committed
  corrupted. Use the editor's own file tools for docs, or pass `-Encoding UTF8` on
  BOTH ends.

## FINAL A/B RunAll pair (repaired TestKit) — CLEAN SWEEP (2026-07-25)

Re-run after the TestKit repairs (WithGlobals now writes real globals; sentinel
SKIPs; probe fixes). Logs: Mars.exe-20260725-14.17.33 (baseline) / -14.20.37
(fixed). **19/19 discriminating probes flipped FAIL→PASS; zero FAILs remain;
all 30 fixes `applied`.** Probe-verified fixes: F03, F04, F07, F08, F09, F11,
F13, F14, F15, F50, F51*, F52, F55, F58, F61, F67, F68, F69, F73, F06.
Not discriminated on a virgin colony: F10 (funding table non-nil → PASS both),
F51 probe PASSed both runs (cache re-evaluated even unfixed in this synthetic
scenario — probe may need a stricter setup). 10 [install] probes SKIP on retail
(sandbox); run the pair once under MarsDebug.exe for that coverage. F73's Idle
wrapper half also needs the debug-exe run (PASS was the IsSuitable half).
`tested` status remains reserved for scenario/manual verification per
TESTING.md — probe-verified ≠ full in-game scenario pass, but the wiring and
regression harness are now proven.

## Superseded: first pair (buggy TestKit) — kept for the record

Unattended harness works end-to-end (TestKit 95_AutoRun, `-smrautorun` via Steam
relaunch; Steam DRM blocks direct Mars.exe launch — bootstrap exits in 28ms).
Baseline = fix pack metadata `code` emptied; B = full pack. **All 30 fixes
report `applied`** (no inactive/error self-checks). Results:
- **FAIL→PASS (10):** UpgradeModifierLeak, TouristApplicants, LanderEmptyLaunch,
  LanderReturnFuel, RocketDroneChurn, StaleReservations, CrystalMysteryHang,
  TouristSatisfaction, TrainPlatformWedge, CommandCenterNumbers.
- **Applied but probe still FAILs (4) — diagnose fix-vs-probe:** WispPower (nil
  power units both runs), LanderCargoRatchet (request still drops to 0 with
  cargo aboard), HomeDomeMigrationGate (same fail text both runs),
  DomeOverviewHighlight (baseline "renders as 0", B "renders as table:0x…" —
  behavior changed, probe may mis-parse a T() value).
- **Probe/tooling casualties:** 10 [install] probes ERROR both runs — the
  no-introspection sentinel itself crashes (00_TestCore.lua:76 indexes nil
  'lib'); ShelterReflex ERROR in B (same crash via its wrapper check);
  VacuumWalks SKIP in B ("unexpected route value: unset").
- **Non-discriminating on a virgin colony:** FactionFundingCheck PASS both
  (funding table not nil on fresh game); NightShiftWork/WispResearch/
  ShuttleTransportCache/DroneUnreachableForever SKIP both (need colonists/
  mystery/shuttle state).
- Full logs: %AppData%\Surviving Mars Relaunched\logs\Mars.exe-20260725-13.56.49
  (baseline) and -13.58.35 (fixed).
- For [install] coverage: run the pair under MarsDebug.exe (console/asserts
  build un-sandboxes introspection; auto-bridge then fires).

### Diagnosis of the four "applied but still FAIL" probes — ALL FOUR FIXES ARE SOUND

Every one of the four was a Test Kit defect; **no fix pack code changed**. Two
engine facts (both now recorded in the Test Kit sources) explain all of them plus
the tooling casualties:

1. **`error()` does not unwind mod code.** It REPORTS (the `[LUA ERROR]` block
   with stack + locals) and execution continues with the next statement — the
   same treatment `assert` gets ("asserts pop instead of being printed out",
   LuaExports.lua:567). So `SourceOf`'s sentinel printed a stack and then ran the
   line it was guarding (00_TestCore.lua:76 → ERROR, not SKIP), and
   `WithGlobals`' `if not ok then error(res, 0) end` swallowed every error raised
   inside a probe's driven code — the probe carried on with a nil result and
   reported FAIL. Never use `error()` for control flow in mod code.
2. **`rawset(_G, k, v)` from mod code writes nothing the game can see.** In the
   sandbox `_G` IS the mod's own env table (Mod.lua:1603) and `rawset` is the
   real rawset (only `rawget` is replaced, :1606), so the Test Kit's fake globals
   were shadows in the Test Kit's env — invisible to shipped code (real `_G`) and
   to the fix pack (its own env). Plain assignment `_G[k] = v` goes through
   `ModEnvMeta.__newindex` (:1557-1563), which rawsets the REAL `_G`; that is the
   write a probe needs. **Every `WithGlobals` probe in the pair was therefore
   driving the real globals**, which is why the numbers looked absurd.

Per item, with the evidence that settled it:
- **WispPower (F07) — probe.** The fake `MainCity.labels.LightTrap` was invisible,
  so `SetLightTrapMode` iterated the live (empty) label and never called
  `el_prod_modifier:Change` → `granted` stayed nil in BOTH runs. The `* 1000` fix
  (Fix_WispRewards.lua:49) matches the sibling call sites exactly.
- **LanderCargoRatchet (F68) — probe.** The fixed method ran; the fake
  `GetTotalCargoAvailable` was invisible, so the real one crashed on the
  synthetic city (`[LUA ERROR] Lua/ResourceOverview.lua:30: attempt to call a nil
  value (method 'GetMap')`, raised from WithGlobals) and the swallowed error left
  `captured` nil → "request dropped to 0". The requested-floor block is intact
  and would have engaged (`is_on_automode_target_loc` true, `export_above.Metals`
  set, 300k aboard). The separate audit finding stands and is NOT this:
  the floor still does not debit hold capacity — verify in-game with multiple
  exports.
- **HomeDomeMigrationGate (F61) — probe.** Proof the fix worked: the fake global
  `ChooseWorkplace` was invisible, so the *real* one ran on the synthetic
  colonist and crashed (`Lua/Buildings/Workplace.lua:1095: attempt to index a nil
  value (local 'traits')`) — which it can only have been handed after
  `GetCommutableWorkplaces` produced the connected list, i.e. after the
  `accept_colonists` gate was gone. No fifth ungated call path is involved.
- **DomeOverviewHighlight (F14) — probe.** The fix is right and the shipped UI
  wants exactly what it now passes: a T value is a TABLE in this engine
  (`Untranslated(s)` → `T{s, untranslated = true}`, localization.lua:343) and the
  shipped sibling paths hand the same kind of table to the same `SetText`
  (ColonyControlCenter.lua:502-507). The probe `tostring()`ed it and saw
  `table: 0x…`; it now reads the literal out of the T.
- **VacuumWalks (F52) — probe** (same root cause; the fixed run's "unset" meant
  `SetCommand` was never reached because the real `GetDomesPassagePath` answered).

Test Kit repairs (repo `C:\Dev\SMR-BugFixPack-TestKit`): deferred-verdict
mechanism replacing the raise (657b668), WithGlobals write-through (413d87c),
F73 partial PASS (57139f5), F14 T reader (3f1abb4), F52 message (77fdb72),
AutoRun `wait_for` timeout (d2636b7), Meteors logger global swap (42d9f43).
**The A/B pair must be re-run** — with the fakes finally visible, several probes
that "passed" or SKIPped were not testing what they claimed.

## Waiting on the user

1. DONE 2026-07-25/26 — retail A/B pairs clean AND the MarsDebug [install] pass is
   complete (49 PASS / 0 FAIL, F73 fully verified — see the QA session section).
   **Automated + attended probe coverage is now 100%**; nothing further is owed to
   the harness. All that remains is the human playtest.
2. DONE 2026-07-26 — author set to **catt144** in both mods' metadata.lua.
3. For the save-failure lead: logs from `%AppData%\Surviving Mars Relaunched\logs`
   and Ctrl+F1 reports from affected players would pin it.
4. An in-game observation for F55: do drones still enter a dome after the roof is
   opened? The Lua half of that report turned out not to be actionable (see the
   F55 entry) — only play can tell us whether the entity data is at fault.
5. Manual playtest per `docs/PLAYTEST_CHECKLIST.md` (35 tests — PT-23..PT-35 are the
   wave-3 group 6; no third-party mods;
   covers what scripts can't: feel, visuals, UI, long-running behavior). Results
   reported back flip each covered fix's BUGS.md status to `tested` — see that
   file's "Reporting protocol" section for the exact follow-up workflow.
6. **All decisions made (2026-07-26).** F32 closed `wontfix` → D02 filed (planned
   `Opt_AcknowledgedWarnings`, gated on PT-38); F62/F63 closed `wontfix` (carried-forward
   design in both games, user decision); F10 retirement STAGED (46 modules / 45 active,
   final `wontfix` gated on PT-36; rollback is one metadata line); F48 rides on PT-37;
   TestKit stays local-only. Nothing is blocked on a decision anymore — only on play.
8. ~~TestKit remote~~ **DECIDED 2026-07-26: local-only, by design.** The kit was never
   meant to ship publicly, so no remote is created. Note the consequence: the repo's
   51 commits exist in exactly one place — if a local backup is ever wanted,
   `git -C C:\Dev\SMR-BugFixPack-TestKit bundle create <somewhere-else>\testkit.bundle --all`
   is the one-liner (a bundle is a single file that `git clone` accepts).
7. A donated save that researched **Frictionless Composites before the game patched the
   tech** is the only true fixture for the F35 sanitizer pass (PT-35 case C). Everything
   else about that pass is probe-covered.

## Save-rescue expectations (for release messaging + sanitizer design)

~60% of fixes help broken saves IMMEDIATELY (behavioral code re-evaluated every
tick/cycle: drones, colonists, schedulers — F02 pattern of thread-restart on
LoadGame where needed). ~25% need active repair; those passes now ship — eight in
their own fix files plus F03 and F35 in `Code/90_SaveSanitizer.lua`. Only F48
remains queued, and it is blocked on an in-game test (see the blocked table). ~15% is irreversible history (dead colonists,
lost expeditions; F64 voided trains have no recorded count — heuristic
compensation option at best, and document the vanilla train re-purchase at
stations, Station.lua:573-611). Save rescue is the headline differentiator vs
official patches ("new games only") — lead with it.

## Distribution facts (researched 2026-07-25, source-verified)

- BOTH Steam Workshop AND Paradox Mods are supported; the in-game Mod Editor has
  upload buttons for each (ModEditor.lua:78/:115). Steam Workshop reaches PC
  only; **Paradox Mods is the only channel that reaches Xbox/PS5** — platform
  fan-out is automatic on the backend, no platform fields, no modder-side
  signing (PS5 signatures are created client-side at install, Mod.lua:49-95).
  Console loads packed Lua code mods fine; no engine restriction found.
- PDX upload hard-requires: title, short_description (≤200 chars), description,
  preview image, lua_revision; last_changes on every update; ≤10 tags
  (ParadoxMods.lua:13-54, Mod.lua:410). GitHub repo link goes in metadata
  `external_links` — "github" is a supported LinkType shown on the PDX portal
  (Mod.lua:180-201). Default ignore_files already excludes *.git/*.
- Public repo: github.com/catt144/SMR-CommunityFixPack (main). Commit identity
  is the GitHub noreply address — never commit with a real email again.
- **CORRECTED 2026-07-26 (user unlocked one in play):** achievements are NOT
  disabled by mods on PC/Steam. `DoModsBlockAchievements()` returns
  `Platform.playstation or Platform.xbox or Platform.windows_store`
  (Achievement.lua:61-63) — the ModManager.lua:78 string is warning TEXT shown
  only behind that gate. Mods block achievements on console/MS Store ONLY.
  Separately, cheat use is logged per save (`LogCheatUsed` → persisted
  `CheatsUsed`, Network.lua:241-255) and adds "cheats used" to the
  unlock-refusal reasons on retail — so cheated fixture saves self-block their
  achievements. Mod description: say achievements keep working on PC, are
  disabled on consoles.

## Release checklist (when fixes are tested)

Real author + version bump in metadata.lua; player-facing fix list in README +
mod description; upload via in-game Mod Editor (check docs/.git exclusion; the
Test Kit must NOT be uploaded); credit ChoGGi (Fix Bugs) + LukeH (Martian
Express) as prior art; keep per-fix disable instructions in the description.
Three `[DRAFT NOTE]` markers remain in `MOD_DESCRIPTION.md` (lines ~6, ~257, ~277) and are
deleted before the text ships. The one at ~257 is load-bearing: do NOT promise the
ClassicRockets module's unwritten Rare Metals export half.
