# Continuation prompt (model-agnostic) — PLAYTEST STANDBY (rewritten 2026-07-30, end of the playtest day)

Paste everything below into a fresh Claude Code session — **any Claude model;
the user picks the model per task and everything here works identically on
either.** This is the ONE live prompt. **Start with `git log --oneline -5` +
`git pull`** in case another session ran since this prompt was written — this
file goes stale the moment another session commits. (The filename keeps its
historical FABLE_ prefix so existing references stay valid — nothing in it is
model-specific.)

## Where the project stands (end of 2026-07-30 — a long playtest day, no sitting currently live)

**Next session is PLAYTEST STANDBY.** Nothing is half-finished and nothing is
blocked on an agent. Do the two ⚠️ items at the top of the board first (read
§4a; dials-to-base + one A/B leg), then the owner picks a PT. Open playtests, in
suggested order: **PT-56** (D09 dials, ~5 min, un-gates the D10 build) ·
**PT-53 Trigger E** (last thing before D07 → `tested`) · **PT-54** (wave-6
disasters) · **PT-52 Trigger B + the B2 stress re-run** · checklist **§6
needs-eyes riders** (take them while you are in a qualifying save) ·
**PT-20/21** last. One decision is owed (FIX_POLICY §4 amendment) and one
build is queued behind PT-56 (D10 workshops).

**Build state: 73 registered modules — 67 active by default**, 6 opt-in via
Options → Mod Options (D05, `tested`), plus the D09 stat-dials module
(`Opt_DroneStatDials`, active-at-base = vanilla, PT-56 owed). **Two modules were
DELETED and one guard removed on 2026-07-30** — see "the reachability turn"
below. Everything committed and pushed.

> ⛔ **READ THIS BEFORE WRITING ANY FIX — FIX_POLICY §4a, owner hard rule,
> 2026-07-30: this pack NEVER fixes other mods' problems.** Not bugs caused by
> another mod, and not vanilla bugs reachable only from mod code. **"For modder
> benefit" is not a valid reason to ship anything.** Overridable only by asking
> the owner explicitly, for that one case — never inferred, never assumed from
> precedent, never carried to a second case. Existing shipped fixes are NOT
> precedent: two violated this rule and one is already retired under it (F28;
> F29 is flagged, awaiting the owner).

**The code gate is CLEAR.** Post-removal A/B leg (unattended, log
`Mars.exe-20260730-17.25.32`): **74/74 fixes active** — exactly one fewer than
the pre-removal 75/75, which is the F24 deletion and nothing else — **zero
`[CommunityFixPack]` error/inactive/disabled lines**, **77 probes**, result
**66 / 1 / 10 / 0**. ⚠️ **That leg predates the F28 removal**, which came later
the same evening: expect **73 registered / 67 default-active and 76 probes**
next run, and **a fresh A/B is OWED** because F28 took its probe with it. The single FAIL is a **TestKit defect, not a pack
regression**: the D09 dial probe takes its baseline from the live value
(`60_Probes_Opt.lua:411`) and the account dials are off-base. Full record on the
D09 entry and in the TestKit README's "Known probe defects".
Reference legs, measured **before** the removals (historical — the counts no
longer apply): baseline `1/61/15/0` · default config, six toggles OFF
`62/0/15/0 at 69/75` · all six ON + dials `67/0/10/0 at 75/75`.

**Account state — READ IT, NEVER ASSUME IT.** As of the last leg all six
toggles were **ON** (74/74) and the **carry dial is at +1, not base**
(`DroneResourceCarryAmount` read 3 where a techs-only save reads 2). A
default-config leg needs the six turned off by hand; **PT-56 needs both dials
set to base first** or its "baseline" step records an already-modified value.
`SMRFixPack.ListFixes()` or `SMRFixPack.fixes.<Id>.status`.

### The reachability turn (2026-07-30) — the day's most important outcome

The pack now asks a question it never used to: **can a player reach this
defect at all, and is the shipped behaviour even wrong?** Two modules failed it
and were deleted the same day.

- **F24** — real defect (water grid passes `dome` where its electricity twin
  passes `self`), **unreachable**: domes refuse to place over buildings, no dome
  template has an upgrade, interior shapes never change at runtime. Carried as a
  §1.5 full replacement. Deleted.
- **F49(c)** — worse: **not a defect at all.** The salvage cursor names its
  target for everything on the map, the
  `Salvage Train Station`→`Salvage Track` handoff is seamless to the
  millimetre, and no exposed control separates a station from its own connector
  track. The propagation it "fixed" is what makes that boundary continuous;
  the guard would have carved a dead band into it. Guard removed.

A full **reachability audit** of all 66 fix modules + 2 sanitizer passes
followed (`docs/REACHABILITY_AUDIT.md`) — the pack survives almost intact
(~21 R1, ~38 R2, 5 R3 kept, 1 U, 2 R4). It was then **challenged and corrected**
(same file, "Challenge review 2026-07-30"), which is the part worth reading:
its method was **decisive on reachability and near-mute on intent**, so a wrong
author-hypothesis passes with full confidence; exactly two verdicts in the
table were unenumerated; and its evidence base went stale mid-run. New tier
**`I` — Intentional** was added. **Standing rule earned: a state producible
only by console/debug injection is evidence AGAINST reachability, never for
it.**

**A whole-mod audit ran 2026-07-29 and its Phase 1-3 remediation is DONE
(same day, one-off fix session).** Findings + the plan (all Phase 1-3 boxes
ticked) live in `docs/archive/AUDIT_FINDINGS.md` (ARCHIVED 2026-07-30 — Phases 1-3 done; only the Phase 4 go/no-go is still live); Phase 4 (core helpers, merges,
deactivation surface) stays deferred pending a user go-decision. Playtest
consequences NOW:

1. **The opt-module first-enable defect is FIXED (audit 1.3) and CONFIRMED IN
   PLAY (PT-55, 2026-07-30):** a first mid-session enable of ClassicRockets /
   ResidencyControl / MultipleSuns works without a relaunch — hooks install at
   file scope. Do NOT treat a dead first-enable as legacy behavior any more; it
   would be a regression. The two known-and-explained exceptions are the D04
   panel-binding timing (self-healing on reload) and the D01 parked-rocket
   demand refresh (accepted limitation) — both recorded on their BUGS entries
   and in the archived PT-55 section.
2. The audit-era warning about running the fix prompt concurrently is
   obsolete — that one-off executed and deleted itself 2026-07-29.

## PT-55 — CLOSED IN FULL 2026-07-30 (nothing owed)

All three steps resolved. Step 1 per module: first mid-session enable works
for all three reworked opt-modules — D03 clean; D04 with the self-healing
binding-timing note (a panel built before the flip binds on reload); D01's
hook live (a rocket that LANDS after the flip fills immediately). Step 2
(toggle-OFF reverts) reported verified. Step 3 ran in the live sitting:
`ListFixes` agreed with the toggles through a full OFF/ON/OFF Mod Options
cycle and the log swept clean per PT-22. **The D01 parked-rocket limitation
is ACCEPTED by user call (`4f5f61e`)** — a parked rocket picks the behavior
up on its next landing; the `on_activate` enhancement stays on the D01 entry,
unbuilt. Audit A2 caveat retired. Full evidence: the archived PT-55 section
in `PLAYTEST_ARCHIVE.md`.

**Playtest state:** **PT-11 PASS → F01 `tested`** and **PT-29 PASS → F41
`tested`** (both 2026-07-29, archived). PT-53 (D07 CohortHousing) is 3-of-5
PASS, and **Trigger A PASSED 2026-07-30** (Forever Young A/B on one save:
employed seniors exempt, unemployed re-homed on reload; module confirmed
`active` for the employed half). **Only Trigger E is left** — player-forced
residence wins, toggle-off is instantly vanilla, save-ON/reload-OFF loads
clean. That is the last thing between D07 and `tested`. PT-52 (D06 + F77) has three
healthy passive sittings; Trigger B is un-run and the **B2 stress A/B re-run on
the v2 harness is the natural centrepiece of the next live sitting**. PT-54
gates the wave-6 disaster fixes. PT-56 gates D09 (and its PASS un-gates the
D10 build).

**A live sitting is in progress on a SAVE-B-derived no-disasters save** with
Forever Young researched, a dedicated nursery-only child dome, and homelessness
/ unemployment deliberately saturated. That save is the fixture for D12's
origin evidence — do not assume a healthy colony.

**Open decisions on the user (nothing blocks on you):** F79 D-item or not
(trains never serve service trips — confirmed vanilla gap); audit Phase 4
go/no-go (core-helper extraction + module merges — deferred, see
AUDIT_FINDINGS); D06 iteration beyond knobs (design changes are user calls;
the stat dials are BUILT — D09, 2026-07-29 late, range widened to 1x/2x/3x/5x
by user call after the live no-clamp probe; PT-56 owed).
D08 (extender overhaul) is speced in `DRONE_OVERHAUL_OPTIONS.md`, nothing built.
**D10 (workshops: text repairs + capacity dial) is DECIDED and speced
(2026-07-30, BUGS.md entry) — build it after PT-56 PASSes; not a decision.**
Deferred decision recorded there: seniors-in-workshops (D07 interaction).
**D12 (no-homeless dome policy) is DECIDED and speced (2026-07-30, BUGS.md
entry) — build owed, not a decision.** Origin: found in play — a nursery-only
child dome deadlocked itself. Vanilla's emigration tie rule
(`Colonist.lua:2675-2681`) never moves homeless colonists when every candidate
ties, so graduates evicted from nurseries strand in place; that pushes the dome
over `IsOverpopulated`, and D07's own `consider()` skips overpopulated
communities — so no new children arrive. D12 drains the homeless and the loop
unwinds without touching D07. **Its own module**, `Opt_ResidencyControl` as
donor pattern ONLY — the hard constraint is that the new flag must NOT route
through `CanAcceptNewColonists` (D03's gate), or it blocks the cohort delivery
it exists to protect. Never expel to the surface: best-effort via the shipped
emigration machinery, and if no destination qualifies the colonist stays.
**Sequencing:** D10 and D12 both touch colonist assignment — land them
separately with their own A/B, never entangled.
Release-time owner tasks from the audit (plan 2.5): preview image (PDX ≤2 MB
/ Steam ≤1 MB), screenshots, Paradox portal console-publishing rules.

**Session-start sequence (~2 min):**
1. `git log --oneline -5` + `git pull` (see above).
2. Verify the pack loaded clean: on-screen status loop (below) — all **68**
   default fixes `active` (69 before the 2026-07-30 F24 removal; incl.
   DroneStatDials, active-at-base), plus
   whichever opt-in toggles the user runs (account-persistent — READ the
   state, never assume it; all six ended OFF after the PT-55 closure cycle).
3. Fresh `SMRFixPack.DroneReport` baseline if D06 is on (counters reset
   every launch; the PT-52 passive watch continues every sitting).
4. Optional (only if a lander/cargo read is planned): re-arm
   `SMRTest.Log.AutoCargo(true)` + `SMRTest.Log.CargoReady(true)`
   (runtime-only, reset every launch).

---

You are continuing the Surviving Mars: Relaunched "Community Fix Pack" — this
session is **LIVE PLAYTEST STANDBY**: the user is (or is about to be) at the
keyboard in the retail game with both mods loaded, and you assist in real time.
Your jobs, in the order they usually come up:

1. **Set tests up** — for whichever PT item the user picks, walk them through
   setup using the checklist's own steps (`PLAYTEST_CHECKLIST.md`) and the
   verified command table (`PLAYTEST_HELP.md` — the reference half was split
   out 2026-07-30); hand them exact console lines to paste. The
   opt-in modules are enabled in **Options → Mod Options → Community Fix
   Pack** (main menu or pause menu; PT-51 verified the surface — but see the
   first-enable caveat above for the three affected modules).
2. **Process results as they arrive** — reporting protocol at the bottom of
   `PLAYTEST_CHECKLIST.md`: PASS → status flips in BOTH BUGS.md places (index
   row + heading tag; for D-entries flip the "built" wording to tested), the
   completed section moves to `PLAYTEST_ARCHIVE.md` (partially-passed tests
   stay in the checklist with their passed triggers recorded); FAIL →
   diagnose live if possible (console wrappers, timestamped logging — the
   F12 pattern), file the finding on the BUGS entry with the full forensic
   trail.
3. **Diagnose surprises** — anything odd the user reports mid-play gets the
   live-instrumentation treatment. New defects get a new F-number, entry, and
   severity call. Mechanical repairs may land same day WITH a re-verified A/B
   (F12 + ListFixes precedents); redesigns go to the user.
4. **Commit as you go** — every processed result or finding is a commit
   (identity below), pushed. Docs never lag play.

**First, read (in order) from `C:\Dev\SMR-BugFixPack`:**
1. `docs\ENGINE_FACTS.md` — the whole file (the engine behaviors that will
   otherwise mislead you; moved out of STATUS.md 2026-07-29). Then
   `docs\STATUS.md` — now a compact current-state doc: header (counts, open
   decisions, next gates) + reference sections. Session legs all live in
   `docs\archive\SESSION_LOG.md` (newest first) — read the newest ones (the
   2026-07-30 legs: checklist split, curiosity/D10-D12 spec legs, the
   playtest legs) down through the 2026-07-29 audit-remediation leg.
2. `docs\PLAYTEST_CHECKLIST.md` — **SPLIT 2026-07-30: the checklist now
   carries ONLY tests + the reporting protocol**; §1 standing watches (log
   hygiene, meteor watchdog, PT-52 passive), §2 owed halves, §3 wave-6
   PT-54, §4 fixture sittings, §5 cross-cutting (PT-20/21), **§6 the
   needs-eyes list (new 2026-07-30 — eleven single observations from the
   reachability audit; six ride along on PTs already scheduled)**. The PT-52
   section still carries the CAN/CANNOT lists — judge the module only on
   the CAN list. **All reference material — ground rules, external-validity
   rule, cheat discipline, console facts, the verified command table, Test
   Kit helpers + stress harness, save-fixture recipes — lives in
   `docs\PLAYTEST_HELP.md`.** Read the help doc's ground rules before
   handing the user any console line.
3. `docs\BUGS.md` — the entries the sitting touches (D06 + F77 for the PT-52
   watch; D07 for PT-53; F78/F81 for PT-54; **F76 before ANY depot-picker
   interaction**; F48 before PT-37). For any drone anomaly, the DroneControl
   bullet in "Not yet swept" carries the full assignment-machinery trace and
   the R1-R7 paste-ready console forensics.
4. `docs\FIX_POLICY.md` — binding rules for any code you write. **Its §4 has a
   drafted replacement awaiting the user's go-ahead** (end of
   `REACHABILITY_AUDIT.md`); until applied, §4 as written demands a proven
   defect but NOT a reachable one, and not an intended-vs-defective judgement
   — the two gaps that cost F24 and F49(c). Apply the spirit of the draft to
   anything you write in the meantime.
5. **`docs\REACHABILITY_AUDIT.md` — read the "Challenge review 2026-07-30" at
   the end before writing ANY new fix.** It carries the tier vocabulary
   (R1/R2/R3/R4/U plus `I` — Intentional), the hard tells that distinguish a
   defect from designed behaviour, the needs-eyes list, and the two standing
   rules earned the hard way: *a state producible only by console/debug
   injection is evidence AGAINST reachability*, and *re-read `git log` between
   assembling conclusions and publishing them*.
6. Only when relevant: `docsrchive\AUDIT_FINDINGS.md` (ARCHIVED — audit findings + the plan;
   Phases 1-3 implemented 2026-07-29, Phase 4 awaiting the user's
   go-decision); `docs\DRONE_OVERHAUL_OPTIONS.md` (only if D06 needs design
   iteration, not just knob tuning — the shipped core is the veto variant of
   option H + option A; upgrade paths H-v2/B/C and the DECISION section are
   there).

Game source (read-only, NEVER modify):
`A:\SteamLibrary\steamapps\common\Project Spark\ModTools\Src`.
Both mods load through junctions from `C:\Dev\SMR-BugFixPack` and
`C:\Dev\SMR-BugFixPack-TestKit`. **Check Mars.exe is NOT running before
touching loadable code** (`tasklist`) — edits to loaded Lua mid-session do
nothing until relaunch, and a baseline-metadata accident during play would be
silent.

## The board (user picks; suggested order)

- **⛔ FIRST — DO NOT WRITE ANY FIX BEFORE READING `FIX_POLICY.md` §4a.**
  Owner hard rule, 2026-07-30. The test is **who benefits**: could a PLAYER be
  harmed, now or after a future patch/DLC? Yes → real fix, ship it (invisible
  and latent are irrelevant). Only-a-mod-benefits → barred. Operationally the
  **R4/R3 boundary**: R4 needs new *calling code* (mod territory, barred), R3
  needs new *data* (ships with patches/DLC, allowed). Override is an explicit
  per-case ask to the owner, never inferred. **Judge by enumeration, never by an
  entry's own words** — F29 called itself "mod-facing / No shipped user" and had
  four live shipped callers.

- **⚠️ FIRST ACTION AT THE KEYBOARD, before any PT: set BOTH Mod Options dials
  to base, then run one A/B leg.** Two things ride on it: (1) it re-confirms the
  D09 dial probe goes green — its FAIL last leg was the off-base account dial,
  not the pack (TestKit defect, D09 entry); (2) **an A/B is genuinely OWED** —
  F28's deletion took its probe with it, so the numbers moved and no leg has run
  since. **Expect `67/73` default-config (or `73/73` all-toggles-on) and 76
  probes.** The last recorded leg (74/74, 77 probes, 66/1/10/0) predates F28.

- **DECISION OWED — the FIX_POLICY §4 amendment** (the *other* one; §4a is
  already applied). Drafted at the end of `REACHABILITY_AUDIT.md` and revised by
  its Challenge review: requires a reachability tier **plus** a positive intent
  statement backed by a hard tell, adds tier **`I` — Intentional**, and makes
  every lettered sub-item of a bundled fix its own audit subject.
  `FIX_POLICY.md` §4 is deliberately UNTOUCHED pending the owner.
  ⚠️ **Resolve this contradiction first:** as drafted it says "R4 does not
  ship", which would mandate stripping **F49(a)** — while the audit separately
  recommends keeping (a) as a cheap no-op rider on a module kept by (d). Three
  options are written up on the F49 entry; the recommended one is a narrow
  carve-out for an R4 item riding inside a module retained on other grounds.

- **Second-order, only if the owner wants a stricter line:** **F29** and
  **F57(a)** are R3 implemented as **§1.5 replacements** — the combination the
  amendment would put to the owner. Both are KEPT and correct today. F29 is
  explicitly NOT a §4a case (see its entry).

- **~~AUDIT_FIX_PROMPT~~ DONE 2026-07-29** — AUDIT_FINDINGS Phases 1-3 all
  landed (veto bypasses, opt-module first-enable repair, error-status
  checkbox, F78/F81 decoupling, upload blockers + ignore_files + ModItemCode,
  MOD_DESCRIPTION/README corrections, ENGINE_FACTS + STATUS/SESSION_LOG
  restructure). What it left for humans: **~~PT-55~~ (CLOSED IN FULL
  2026-07-30, archived — see the section above)** and the **Phase 4
  go-decision** (user).
- **~~PT-55~~ CLOSED IN FULL 2026-07-30** — archived; audit A2 caveat retired.
  The cheapest open item is now **PT-56** (D09 stat dials, ~5 min).
- **PT-52 STRESS A/B — re-run with the v2 harness (the v1 run's metric was
  invalid).** Protocol is Trigger B2 in the checklist (§2): quicksave →
  `Targets` dry run (check the `pure_only=true` cohort size too) → D06 OFF →
  `Break{scope="overlap", n=25, seed=1}` → reload → D06 ON → same call →
  `Compare()` → repeat seeds 2-3. Read the **GATE-DECIDED first claims** line
  (closest-hub % over FindTask-decided claims only) and the lifecycle deltas
  (haul queue vs exec vs claim wait vs travel — this is what gates the
  Track B structural choice). Do NOT read total clearance time as a D06
  score. Reload-based protocols do NOT re-poison a save (tested, F81).
- **PT-54 — wave-6 disaster fixes live gate** (checklist §3): stranded-flag
  reconcile, live-warning-never-cleared, wedge self-heal, reschedule-after-
  heal, rains survive collisions. The live 194-sol save is the fixture.
- **PT-53 — D07 CohortHousing, ONE trigger left** (checklist §2): Trigger A
  PASSED 2026-07-30 (Forever Young A/B — employed exempt, unemployed
  re-homed). **Only (E)** remains: manual assignment wins, toggle-off =
  instantly vanilla, save-ON/reload-OFF loads clean. Then it flips `tested`.
- **PT-52 Trigger B — controlled off/on CheatMalfunction A/B demo + F77
  extender-flap check** (checklist §2) — still un-run; cheap once hub A/B +
  extender geometry exists.
- **F82** — split-grid notification lingers ~a sol; machinery located,
  updater cadence still to trace (own entry). **F80** — trains skip valid
  waiting passengers; investigating, forensic tap on the entry.
- **F76 REPAIR — separate attended, game-free sitting** (vanilla P1,
  unfixed): fix belongs in/around `ResourceItems:UpdateLayout`
  (`ResourceItems.lua:45-71`); Init-time anchor conversion is a proven NO-OP;
  tier-2 fallback = bypass the picker. The F76 entry + section below are the
  whole brief.
- **~~PT-48~~ CLOSED IN FULL 2026-07-30 → D02 `tested`** (archived) — all five
  steps on console counters, opened with a positive control; acked buildings
  held 4.2 vanilla windows; the stamp survived save/reload. Left one vanilla
  curiosity on the D02 entry for a game-free look: `InsufficientResources`
  suppression resolves on **RealTime** while PT-38 measured
  `NotWorkingBuildings` on **GameTime**, despite both presets leaving
  `GameTime` at its default `true`.
- **~~PT-46 tail~~ CLOSED IN FULL 2026-07-30** (archived) — (d) PASSED by play
  (`els=43 cap=2` → `els=13 cap=1` across a salvage), (a) settled **R4** by the
  audit, (c) closed `wontfix` with its guard removed. F49 holds at `fixed*`
  carried by (d).
- **NEW — checklist §6 "Needs-eyes list"**: eleven single observations that
  settle verdicts currently believed on source-shaped evidence. Six ride along
  on PTs already scheduled; the genuinely new ones are **F34(d)**, **F74**,
  **F06** and F11's console read. **F74 and F53(a) need the pack DISABLED** —
  bundle them into the next PT-20 sitting.
- **PT-37 — the LAST decision gate** (attended): F48 — PASS = build the
  corrected fixup behind a one-shot flag; FAIL = `wontfix`.
- **Playtest-method rule (earned 2026-07-29, applies to every PT):** two tests
  in a row proved unrunnable as written (PT-29's trigger needed a colonist that
  could not exist yet; PT-11 compressed a scheduler const without re-arming the
  repeat, so it would have false-PASSed regardless of the fix). **Treat an
  un-run PT's procedure as unverified until it has been executed once**, and
  for any "nothing should happen" test insist on a positive control and an
  objective counter. Details in the checklist's ground rules.
- Un-run fixture PTs (checklist §4-5): PT-10, PT-15, PT-18 (fixtures
  A/D/E), PT-25, PT-27/28/30 (**PT-29 and PT-11 PASSED 2026-07-29 → F41 and F01
  `tested`, both archived**; PT-27's Biorobots grant is
  `ThePositronicBrain`; `CheatResearchAll()` SKIPS undiscovered
  breakthroughs — grant directly via `UIColony:SetTechResearched("<Id>")`),
  PT-35, PT-42, PT-44, PT-46 tail (F49(d) cap, F49(a) palette), PT-47,
  PT-20/21/22 (cross-cutting, last — PT-20's save should post-date wave 6 so
  the cycle covers the new persisted state).
- **PT-56 — D09 stat dials** (checklist §2, ~5 min): baseline reads → 2x/+1
  → Apply → stacked reads → base → Apply → baseline again → stale-save
  reconcile. PASS flips D09 to tested **and un-gates the D10 build** (the
  workshops module reuses the same label-modifier dial machinery).
- **D10 — workshops module BUILD (assistant, game-free, after PT-56 PASS):**
  speced + user-approved 2026-07-30, full spec on the BUGS.md D10 entry —
  T1 text repairs (workshop descriptions + Unemployed rollover gain the
  Relaunched faction-approval fact; ≥10% dome unemployment costs -900..-3000
  approval per faction clause) + T2 capacity dial (base/+50%/+100%, colony
  label modifiers on the three template labels, max_workers AND
  consumption_amount PAIRED — the pairing keeps per-worker cost vanilla).
  Adds PT-57 (~7 min) at build time. Seniors-in-workshops deliberately
  deferred (D07 interaction — own decision).
- **DECISIONS owed (user):** F79 D-item or not; audit Phase 4 go/no-go; D08;
  seniors-in-workshops (D10 deferral); **D11 shuttle same-pair passenger
  batching — feasibility is on the BUGS entry but it is NOT approved: ask
  fresh before any build (user's explicit instruction 2026-07-30); multi-hop
  passenger routing is REJECTED, do not re-propose.**
- Passive: PT-01 meteor silence-watch (the watchdog self-reports); F18
  savegame-sweep line on affected saves.

## PT-52 briefing notes (D06 + F77 — read WITH the checklist's PT-52 section)

The checklist section is the procedure; these are the assistant-side facts:
- **Setup check (each sitting):** the toggle persists, but confirm
  `DroneOverhaul [active]` AND `ExtenderFlapChurn [active]` via the
  on-screen loop or `SMRFixPack.fixes.DroneOverhaul.status` (bare
  expression). F77 rides along default-on — vetoable via
  `SMRFixPack_Disabled["ExtenderFlapChurn"] = true` pre-load if a confound
  is suspected. **Counters are NOT persisted** (zero-persisted-state design)
  — they restart at 0 each game launch, so take the sitting's baseline
  DroneReport right after load. Reference: three sittings healthy, peak
  `vetoed=10 / veto_expired=1 / moonlighted=0`, nine hubs integrated,
  `unclaimed=0` throughout including right after a marsquake mass-damage
  event.
- **`SMRFixPack.DroneReport` prints ON-SCREEN (ConsolePrint) AND to the log
  (ModLog)** — unlike ListFixes, no FlushLogFile dance needed live; the log
  copy is the evidence trail.
- **Counter interpretation** (the module's ground truth): `vetoed` climbing +
  `veto_expired` staying low = near fleets are taking the yielded work
  (healthy). `veto_expired` ≈ `vetoed` = strike window too short or near
  fleets can't respond → knob-tune or investigate. `moonlighted` > 0 near
  saturated hubs (it only fires for a neighbour hub with ZERO idle drones —
  0 is CORRECT when every hub has idle drones). All three flat at 0 with the
  toggle on = the module never intervenes — either no overlap contention this
  session (fine) or something is wrong (check status + log).
- **Starvation is the one theoretical risk the design accepts a window for**
  (max ~4 far-fleet polls ≈ 10-15s before the veto expires). If a wrench
  icon ever visibly outlives vanilla expectations: DroneReport + the R1/R2
  reads on the building IMMEDIATELY, then toggle off and watch whether
  vanilla clears it. That capture is a same-day knob/logic decision.
- **Iteration knobs** (top of `Code/Opt_DroneOverhaul.lua`, relaunch to take
  effect): STRIKES_MAX/STRIKE_TTL (veto patience), MOONLIGHT_MAX_HEXES (help
  radius), HUB_MISS_TTL/COVER_CACHE_TTL (scan cadence). Record every change
  + observed effect on the D06 entry. Knob changes are mechanical (assistant
  may land them same-day, committed); DESIGN changes (H-v2 demand filter,
  registration-H, balancer C) are user decisions per the options doc.
- **Scope guards to lean on when diagnosing:** the claim gate cannot touch
  player orders (FindTask is only called by auto-Idle); rockets, rovers,
  construction, and all hauling are exempt by class/type; toggling off is
  instant-and-complete vanilla. If a hauling or construction anomaly shows
  up, it is NOT this module — investigate it as its own finding.
- R1-R7 forensics (DroneControl bullet) double as the module debug kit; R7
  (hub A + hub B + extender + `CheatMalfunction`) is the cleanest off/on
  demonstration of the claim gate.

## F76 — READ THIS BEFORE THE USER TOUCHES AN RC TRANSPORT **OR DOZER** (vanilla P1, unfixed)

The resource picker (`ResourceItems`) renders far from the cursor and cannot
be clicked on the user's 4K/80%-scale setup — and interacting with it can
**HARD-LOCK the UI (Alt-F4, session lost)**. Full forensics on the F76 entry.
**Surface (widened 2026-07-27 late): ANY vehicle whose click-load reaches a
storage-depot-class object** — RC Transport depot LOAD, multi-type UNLOAD,
route resource choice, and the RC Terraformer ("RC Dozer") clicking a
waste-rock storage heap (confirmed by play, on-click). During play sessions:
- **Avoid the picker paths entirely.** Loose ground/rubble piles are safe (no
  picker — direct pickup, this includes the dozer's auto-gathering), and
  route-mode depot loading works for single-resource depots
  (`RCTransport.lua:466-476`).
- **Verified command workaround** (works for transports AND the dozer):
  `rc:SetCommand("TransferResources", depot, "load", "<Resource>", <amount*1000>, true)`
  (select the vehicle, `rc = SelectedObj`; depot via `~` inspector or
  selection).
- **NO live UI-internals prototyping in a play session** — hard rule since
  the lock-up. The F76 REPAIR is a separate attended, game-free sitting (see
  the board).
- It WILL draw false reports against the pack — the MOD_DESCRIPTION explainer
  note covers it.

## Live-session console facts (hard-won — do not re-derive)

- **`SMRFixPack.ListFixes()` prints to the LOG, not the console overlay**
  (ModLog path; the function returns nothing, so the console shows nothing —
  that is correct behavior, not a failure. The nil-detail CRASH it used to
  have is repaired). Read it via `FlushLogFile()` + the newest log, or use
  the on-screen variant:
  `*r for _, id in ipairs(SMRFixPack.order) do local f = SMRFixPack.fixes[id] ConsolePrint(id .. " [" .. f.status .. "]") end`
- The log buffer only flushes at exit — `FlushLogFile()` forces it
  mid-session (always do this before reading the log).
- **Mars↔asteroid map switches used to KILL the console** — TestKit repair
  BUILT and VALIDATED 2026-07-28 (`OnMsg.CurrentMapChangeDone` re-asserts
  gate + shortcuts; console opened normally across repeated switches; the
  quicksave+reload workaround is retired). If only the ECHO is gone but
  typing works, the lighter recovery is `ShowConsoleLog(true)` blind
  (uiConsoleLog.lua:88).
- **Runtime console wrappers must target the LEAF class** (engine-facts
  flattening corollary): wrapping a base class at runtime does nothing for
  already-built subclasses — e.g. lander taps go on `UniversalLanderRocket`,
  not `UniversalRocketBase`. (The same fact is why the opt-module
  first-enable defect existed — fixed by audit 1.3's file-scope installs;
  human re-verify PASSED — PT-55, closed 2026-07-30.)
- **CORRECTED 2026-07-29 — the earlier claim here was backwards.** Bare console
  expressions echo on-screen only (NOT logged), **and so does `print(...)`**:
  `print = CreatePrint{""}` (`lib.lua:202`) and `CreatePrint` defaults its
  output to **`ConsolePrint`** (`lib.lua:149`), which the engine documents as
  on-screen only. `print` therefore does NOT reach the log — the old advice to
  "use `print` when output must be retrievable" would have silently lost it.
  **`ModLog(...)` is the only path proven to reach the log file on disk**
  (ModLog → ModPrint → DebugPrint, `Mod.lua:109-132`), which is why the pack's
  own logging goes through it. Read the log with `FlushLogFile()` first.
- **`not understood` = the console could not COMPILE the line** (`console.lua:24`
  — no rule in `ConsoleRules` produced a loadable chunk). Overwhelmingly the
  cause is a `--` comment inside a `*r` / `*g` snippet: those rules splice your
  code into `CreateRealTimeThread(function() %s end) return` **on one line**
  (`uiConsole.lua:360-361`), so the comment eats the closing `end) return`.
  **Never write a console snippet with a trailing comment or a `--> value`
  annotation** — hand the user paste-safe lines, one command per line, because
  the console input is a SINGLE line and a pasted block silently concatenates
  (proven 2026-07-29: `--> nil` + the next line arrived as `--> nilUIColony:…`).
- For a simple read prefer a **bare expression** over `*r ConsolePrint(...)`:
  rule `{ "(.*)", "ConsolePrint(print_format(%s))" }` (`uiConsole.lua:363`)
  wraps anything that compiles as an expression, so `GetRareTraitChance()`
  prints itself. Reserve `*r`/`*g` for multi-statement snippets.
- Infopanel cheat buttons need `Platform.cheats = true` AND ride the
  game-time sync queue (dead while paused; fire on unpause). Direct
  `SelectedObj:Cheat*()` bypasses both.
- Console opens via Enter / Alt-Shift-C / Ctrl-Alt-C (TestKit auto-opens it
  in-colony; there is NO main-menu console — Mod Options replaced that need).
- Speed techs sanctioned for setup: `AdvancedDroneDrive`, `LowGDrive`,
  `MartianAerodynamics`. Hive Mind is NOT a drone tech in Relaunched.
- Cheat use is logged per save and blocks that save's achievements — fixture
  saves only.

## Harness facts (for any A/B pair / same-day repair)

- Launch: `& "c:\program files (x86)\steam\steam.exe" -applaunch 3215050 -smrautorun`.
  A leg takes ~75 s; Mars.exe may take minutes to appear. **Never kill on a
  short timeout** (25 min no-kill guard; harness watchdog 15 min).
- Arm the TestKit autorun by adding `"Code/96_AutoRunFlag.lua"` to the TestKit
  metadata `code` list; remove it to disarm (commented out at rest).
- Baseline = overwrite fix pack `metadata.lua` with an emptied `code` list —
  **keep the `default_options` block** (it is part of the mod def now).
  **Restore from a saved copy, NOT `git checkout`, while uncommitted metadata
  changes exist. NEVER `git commit -a` while that edit is in the working
  tree.**
- Opt-in leg mechanism (proven): temporary `Code/97_OptInLeg.lua` in the FIX
  PACK listed right after 00_Core, setting the `SMRFixPack_Optional` table
  (the OptionEnabled bridge ORs it with the saved Mod Options toggles).
  Delete it after the leg. **The bridge is one-way: it can only force a module
  ON, never off** (OptionEnabled ORs the table with the saved toggles), and the
  user's own Mod Options toggles are account-persistent and apply during legs.
  So ALWAYS read the leg's own `fix pack present: N/74 fixes active` line to
  learn which config you actually measured — and a true default-config leg
  (**67/73** since the F24 and F28 removals) requires the user to turn the six toggles
  off by hand first. Proven three times: 2026-07-29 a "default" leg came up
  74/74 with all six on; the post-D09 set needed the user's hand flip to
  produce its 69/75 leg; and the 2026-07-30 post-removal leg came up **74/74**
  because the playtest had left all six ON. **The dials are the same trap** —
  they are account-persistent too, and the carry dial was left at +1, which is
  what FAILed the D09 probe. Read both.
- **TestKit `Code/91_Stress.lua` (v2, lifecycle tracing)** — the drone stress
  harness. It registers NO probes; v2 installs permanent classdef-time wraps
  on `RequiresMaintenance` `StartDemandPhase`/`StartWorkPhase`/`Repair`, but
  they gate on an active stress run and pass straight through otherwise.
- **Expected numbers — CURRENT is the post-removal leg (2026-07-30 late, 77
  probes): all six toggles ON, `74/74`, `66 / 1 / 10 / 0`**, the one FAIL being
  the state-dependent D09 dial probe (set both dials to base and it should go
  green). A default-config leg should now read **`67/73`** and has NOT been run
  since the removals. The three legs below are HISTORICAL — measured before
  `Fix_DomePipeMoveInside` was deleted, so their `/75` and `/69` counts no
  longer apply: baseline (`code` list emptied) **1 / 61 / 15 / 0**;
  default config, six toggles OFF **62 / 0 / 15 / 0 at 69/75**; all six
  toggles ON + dials **67 / 0 / 10 / 0 at 75/75**. The D09 dial probe PASSes
  in BOTH fixed legs (DroneStatDials registers active-at-base, independent of
  the toggles). The 10 SKIPs are 9 `[install]`
  retail-sandbox probes + TechDescriptionBuilding; a default leg's extra 5 are
  the opt-module probes reporting `inactive (opt-in)` — **five, not six,
  because D06 has no probe of its own** (the stress harness covers it).
  Baseline's 1 PASS = FactionFundingCheck canary; the OptionsMenu probe (D05)
  asserts all six toggle wirings PLUS the two D09 dial wirings and FAILs
  baseline by design. The D09 dial probe writes `Mods[pack].options` (NOT its
  own env's CurrentModOptions — per-mod-env, see ENGINE_FACTS) and restores
  the leg's values through the same path. The rains probe does NOT skip on
  the synthetic map — the harness builds a colony, so `HasGame()` is true.
- **Probe-authoring trap (cost wave 6 its coverage, 2026-07-29):** a probe
  whose `run` falls off the end returns nil, and `SMRTest.Run` turns nil into
  **SKIP with an empty message** (`00_TestCore.lua:243`) — it looks like a
  deliberate skip, not a missing verdict. Baseline legs never catch it (the
  `FixMissing` guard returns FAIL before the tail runs), so only a FIXED leg
  can. Every probe needs an explicit `return "PASS", …`; grep
  `Register(` vs `return "PASS"` counts per wave file to audit this.
- **TestKit stand-in probe corollary (D07 leg):** WithGlobals stubs CANNOT
  reach a game file that localizes the global at load time
  (`local IsValid = IsValid`, Colonist.lua:5) — a probe driving shipped code
  with plain-table stand-ins must assert on the MODULE's own action, never on
  vanilla bookkeeping around the stand-ins; a fake colonist through the
  shipped FindEmigrationDome tail needs a PickEmigrationCommunity stub.
- Synthetic-map noise unchanged: ~49 Flight.lua `objects_to_mark` errors +
  a few GameInit nil-call lines in BOTH legs; a `[mod] Error in mod … Test
  Kit` line at quit is a shutdown artifact. The MultipleSuns
  "not found → lifted" line pair during load is the known benign transient.
- Parse sweep: python + luaparser, `ast.parse(open(f,encoding='utf-8-sig').read())`.
- Docs tooling: never round-trip a doc through PowerShell 5.1 `Get-Content`
  without `-Encoding UTF8` both ends; prefer the editor's file tools. Git
  commit messages via single-quoted here-strings or `git commit -F <file>`;
  **no embedded double quotes** (proven again 2026-07-27).

## Hard rules

`docs/ENGINE_FACTS.md` governs (the facts moved there from STATUS 2026-07-29):
sandbox on all platforms; `error()`/`assert()` report-and-continue;
self-checks read the DECLARING class; presets only after DataLoaded
(GlobalMaps exist EMPTY before it; DataChanged(false) re-fires right after;
DataLoaded can fire MORE THAN ONCE — a template can miss the first pass);
GameVars only inside patched functions; post-wrappers on command methods
never run; `IsValid()` is falsy for ALL pure-Lua objects; **the shipped build
IS Src** (full fpk extraction, 2250/2256 byte-identical, build 1.0.7.396349 —
keep apply-time self-checks anyway, they guard future patches); never modify
the game directory; only the playtest flips statuses to `tested`; mechanical
repairs land with a re-verified A/B, redesigns go to the user; **no live
UI-internals prototyping on the user's play sessions** (F76 lesson). Commit
with
`git -c user.name="SMR-BugFixPack" -c user.email="154917955+catt144@users.noreply.github.com"`,
push the fix pack (TestKit stays local-only).

**End of session:** update STATUS.md and this prompt (rewrite stale blocks —
no banner stacking), commit, push, summarize.
