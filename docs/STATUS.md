# Project Status — read this first in a new session

Rewritten in place every session (structure since 2026-07-29, audit
remediation 3.3). Session legs are append-only in
`docs/archive/SESSION_LOG.md` (newest first); engine facts live in
`docs/ENGINE_FACTS.md`; defect truth lives in `docs/BUGS.md`.

**Build state (authoritative counts — stated here and nowhere else):**
`Code/` = **74 files** (65 `Fix_` + 7 `Opt_` + `00_Core` +
`90_SaveSanitizer`) = **73 registered modules, 67 default-active** (the 6
toggle `Opt_` modules are opt-in via Mod Options; `Opt_DroneStatDials` (D09)
registers active but is byte-vanilla until a dial leaves base). Pinned game
build: **1.0.7.396349** (fpk parity proven — ENGINE_FACTS.md). BUGS.md index:
92 rows.
**⛔ NEW HARD RULE 2026-07-30 (owner) — FIX_POLICY §4a: this pack never fixes
other mods' problems.** Neither bugs caused by another mod, nor vanilla bugs
reachable only from mod code. "For modder benefit" is no longer a valid reason
to ship anything. Overridable ONLY by asking the owner explicitly, per case —
never inferred, never carried forward. **The test is WHO BENEFITS, not how visible the problem is** (owner's
clarification, same day): if a player could be harmed now or after a future
patch/DLC — even invisibly, even latently — it is a real fix and it ships; only
"the sole conceivable beneficiary is another mod" is barred. Operationally that
is the **R4/R3 boundary**: R4 needs new *calling code* (mod territory, barred),
R3 needs new *data* (ships with patches and DLC, so player territory, allowed).
It retired **F28** (R4, zero callers anywhere) and **nothing else** —
**F29 was briefly flagged and is KEPT**: its self-description as "mod-facing /
No shipped user" is factually wrong, the audit found four live shipped callers
in Mystery 2, making it R3 latent-by-data like F27/F31/F43. §4a now warns
explicitly: judge by enumeration, never by an entry's own words.

**Counts changed twice on 2026-07-30 — TWO modules deleted:**
**`Fix_ReplaceTechCount` (F28)** went under the new §4a rule: `Research:ReplaceTech`
has **zero callers in all of Src** (re-verified independently), so only mod code
could reach it, and it was carried as a §1.5 full replacement. Its TestKit probe
went with it (**probes 77 → 76**) — it asserted the fixed counter, so it would
have FAILed every leg. **A fresh A/B is therefore OWED** — unlike F24, the
numbers move. Earlier the same day:
**`Fix_DomePipeMoveInside` DELETED**
— F24 closed `wontfix` by user decision after the trigger was proven
unreachable in the shipped game (full proof on the F24 entry). No TestKit probe
existed for it, so the 77-probe suite is unchanged. **The owed A/B RAN the same
evening and the code gate is CLEAR** — see the post-removal row in the table
below. `Fix_TrainMinors` also lost its (c) guard the same day (F49(c)
`wontfix`, designed behaviour), which changes no counts.

**Just landed (2026-07-29 late, D09 build):** the drone stat dials DECISION is
BUILT — `Code/Opt_DroneStatDials.lua` + two Mod Options dropdowns: Drone
speed 1x/2x/3x/5x (range widened from the DECISION's 1.5x/2.0x by user call
after the live no-clamp probe: `SetMoveSpeed(10000)` read back exactly, clean
movement at ultra) and Drone carry +0/+1/+2. Techs' own label-modifier
machinery, reconciled on ApplyModOptions/CityStart/PostLoadGame, base =
modifiers removed = vanilla. D09 entry in BUGS.md; PT-56 owed. **The owed
post-D09 A/B pair RAN unattended the same night — see the probe-state table
below (code gate CLEAR).**

**Landed earlier the same day (audit-remediation session):** AUDIT_FINDINGS.md
Phases 1-3 implemented — code: veto re-check in the three data-patch fixes
(A1), DustSickness data-loaded latch (B3), file-scope install for the three
flattening-unsafe Opt_ hooks so a first mid-session enable works (A2),
reconciler "error" retry + skip logging (B1), MeteorStormWedge clears the
prediction flag itself (B2), logger escaping + build stamps (C4);
packaging: short_description / last_changes / optional_mod / ignore_files +
75 ModItemCode items (editor round-trip no longer wipes the mod) (A3);
description/README truthful: CohortHousing block, honest savegame claim,
console achievements + per-fix-disable disclosures (A4/B4/D1/D2). Docs
restructured (this header, ENGINE_FACTS, SESSION_LOG, archives). Details:
the newest SESSION_LOG leg.

**Open user decisions:** Phase 4 go/no-go (core helpers, module merges,
deactivation surface — AUDIT_FINDINGS.md PLAN); D01 standing-export half
(spec decided 2026-07-26, unwritten); F48 (parked section below); drone
overhaul structural choice (DRONE_OVERHAUL_OPTIONS.md — the stat dials are
BUILT (D09); the structural choice stays gated on the B2 re-run); F79
D-item or not; D08; seniors-in-workshops (deferred from D10, own decision);
**D11 shuttle same-pair passenger batching — candidate with feasibility on
file (BUGS.md entry), explicitly NOT green-lit: re-ask the user before any
build; multi-hop passenger routing REJECTED outright.**
**Decided, build queued:** D10 workshops module (speced + user-approved
2026-07-30, BUGS.md entry — text repairs + capacity dial; build gated on
PT-56 PASS). **D12 no-homeless dome policy** (speced + user-approved
2026-07-30, BUGS.md entry — own module, `Opt_ResidencyControl` as donor pattern
only; breaks vanilla's emigration tie for homeless colonists so specialist
domes stop stranding them, which also unwinds the D07 overpopulated deadlock
without touching D07). **D10 and D12 both touch colonist assignment — land them
separately, each with its own A/B.** Unfiled candidate: Universal Tunnel description omits its
life-support bridging (description drift, one-line text patch — user call).

**A/B probe state (FRESH — post-D09 unattended set, completed 2026-07-30
after the user flipped the six toggles OFF):** **77 probes** (the D09 dial
probe is new), all three legs clean.

| Leg | Active | Result |
|---|---|---|
| Baseline (`code` list emptied) | — | **1 PASS / 61 FAIL / 15 SKIP / 0 ERROR** |
| Fixed, default config (six toggles OFF) | 69/75 *(pre-F24-removal)* | **62 / 0 / 15 / 0** |
| Fixed, all six toggles ON + dials | 75/75 *(pre-F24-removal)* | **67 / 0 / 10 / 0** |
| **Post-removal re-verify, 2026-07-30 17.25 (unattended)** | **74/74** | **66 / 1 / 10 / 0** |

**Post-removal leg — the code gate for the F24 and F49(c) removals is CLEAR.**
Ran unattended after both removals; log
`Mars.exe-20260730-17.25.32`. `fix pack present: 74/74 fixes active` — exactly
one fewer than the pre-removal 75/75, which is the F24 deletion and nothing
else. **Zero `[CommunityFixPack]` error / inactive / disabled / FAILED lines**;
`DroneStatDials: applied`. Probe total still 77 (no probe was removed with
F24). The account had all six toggles ON, hence 74/74 rather than a
default-config 68/74 — read the state, never assume it.
**The single FAIL is a PROBE defect, not a pack regression.**
`DroneStatDials` reported `+1 carry dial: DroneResourceCarryAmount 3 → 2
(want 4)`. Cause: the probe captures its own baseline from the LIVE value —
`local base_carry = consts.DroneResourceCarryAmount`
(TestKit `60_Probes_Opt.lua:411`) — then asserts `base_carry + 1` at `:431`.
That is only valid when the account's carry dial is already at base. Today's
playtest left it off-base (the same account change that turned the six toggles
on), so the arithmetic is measured against an already-modified value. Neither
removal touches drones, modifiers or Mod Options, and the module logged
`applied`. **The probe is state-dependent and can FAIL — or false-PASS —
depending on account dial state; it should force base before measuring.**
Recorded as a TestKit defect, same family as the 2026-07-29
falls-off-the-end-returns-SKIP trap. **To confirm: set both dials to base in
Mod Options and re-run the leg** (2 min; also the natural moment to run PT-56).

Baseline's 1 PASS is the FactionFundingCheck canary; the D09 probe FAILs
baseline by design ("fix pack not loaded"). The 10 SKIPs are 9 `[install]`
retail-sandbox probes + TechDescriptionBuilding. Log clean in both legs: no
`[CommunityFixPack]` error/disabled lines, no error naming our `Code/`,
known synthetic-map noise only. **The pair caught two real defects en route**
(both fixed same-session, see the D09 entry): the module's file-scope
`Modifier.new` check tripped the F64 pre-flattening trap, and the probe's
first version wrote the TestKit env's own `CurrentModOptions` (per-mod-env —
new ENGINE_FACTS entry). **Account state as of the LAST leg (2026-07-30 late):
all six toggles ON (hence 74/74), and the CARRY DIAL IS AT +1, not base** — the
earlier "all six OFF after the PT-55 closure" note is superseded. **Read the
state, never assume it**, and read the DIALS too, not just the toggles: the
off-base dial is what FAILed the D09 probe.** The default leg's dial probe PASS also
proves the dials work independently of the toggles. Pre-D09 reference set
(76 probes): baseline 1/60/15/0 · default 61/0/15/0 at 68/74 · all-toggles
66/0/10/0 at 74/74.

**Next gates (owner playtests — PLAYTEST_CHECKLIST.md):** **PT-55 CLOSED IN
FULL 2026-07-30** (archived; audit A2 caveat retired; the D01 parked-rocket
limitation ACCEPTED by user call `4f5f61e` — a parked rocket picks the
behavior up on its next landing, `on_activate` enhancement on record but
unbuilt). **PT-48 CLOSED IN FULL 2026-07-30 → D02 `tested`** (archived; all
five steps on console counters, opened with a positive control; the acked
building held 4.2 vanilla windows and the stamp survived save/reload; a vanilla
GameTime-vs-RealTime curiosity on `InsufficientResources` was filed on the D02
entry for a game-free look). Cheapest open item now: **PT-56 D09 dials**
(~5 min; PASS un-gates the D10 workshops build). Then: PT-53 Trigger E (the
last thing between D07 and `tested`); PT-54 wedge watchdog; PT-52 Trigger B +
the B2 re-run on the v2 stress harness; PT-20 save/remove/load
incl. wave-6 persisted state; PT-21. **PT-46 tail: (d) PASSED 2026-07-30**
(cap follows length, `43/2`→`13/1` across a salvage); **(a) settled R4 by the
reachability audit** (no player-reachable entry into `place_track` — see the
audit's lead-pass block); **(c) closed `wontfix` 2026-07-30 (user decision,
tier I — designed behaviour), guard REMOVED (`d03417b`)**. F49 now holds at
`fixed*` on (a)+(d), carried by (d).

**Newest legs:** `docs/archive/SESSION_LOG.md` → the 2026-07-30 set, newest
first: the PT-55 closure leg, the PLAYTEST_CHECKLIST/PLAYTEST_HELP split leg,
the curiosity leg (tunnel water, workshop research → D10 spec, shuttle limits
→ D11 candidate), and the parallel playtest legs (PT-55/PT-53-A/D12); the
2026-07-29 D09-build and PT-11 legs sit below them.

**Playtest-method rule earned 2026-07-29 (applies beyond PT-11):** compressing a
scheduler's `g_Consts` interval does NOT shorten the sleep already in flight, so
a "nothing should happen" test must **re-arm the repeat**
(`RestartPeriodicRepeatThread`) and **carry a positive control**, or it
false-PASSes regardless of the fix. Full rule in PLAYTEST_HELP.md (the
checklist's reference half, split out 2026-07-30). Two tests have now been found unrunnable-as-written by actually running
them (PT-29, PT-11) — treat an un-run PT's procedure as unverified until it has
been executed once.

**Tech-gated fixes — coverage settled 2026-07-29, re-grounded by the
2026-07-30 reachability audit.** F41 is `tested` (PT-29). Of the other four,
**F28** (R4 — zero callers in all of Src; the audit's one DELETE candidate,
user decision pending), **F43** (R3 — corrected grounds: MoistureVaporator IS
tech-locked, but its `require_prefab`+unlocked cargo item routes it into the
branch the shipped code handles; the old "no tech-locked entry" wording was
wrong) and **F25** (R2 — pre-1.0.6 legacy saves; note the probe's SKIP label
may be mislabeled, see the entry) are correctly untestable in play. **F18** is
the only genuinely uncovered one: preset half probe-covered, play half needs
the Independence arc + a special project; judged not worth a PT for a
data-only P2.

**REACHABILITY AUDIT COMPLETE 2026-07-30 — `docs/REACHABILITY_AUDIT.md`.**
All 66 fix modules + both sanitizer passes audited for player reachability
(the F24 question, asked pack-wide): ~21 R1, ~38 R2, five R3 (kept — F27,
F29†, F31, F43, F57(a)†; † = §1.5-latent, flagged), one U (F11, settling
observation on the entry), two R4 — F49(a) (kept, lives inside a module with
two live halves) and **F28 (DELETE candidate, awaiting user decision)**. A
proposed FIX_POLICY §4 amendment (reachability tier required before a fix
ships) is drafted in the audit file, not applied. Eleven BUGS.md entries
carry new "Audit 2026-07-30" notes (evidence corrections: F06, F17, F22, F25,
F34, F37, F40, F43, F49, F74, F81 — plus F11's observation).
**CHALLENGED same day and one verdict fell: F49(c) was tabled "live R2"
unenumerated and was in fact designed behaviour** — closed `wontfix` by user
decision, guard removed. The "Challenge review 2026-07-30" appendix in the
audit file answers it: the three-part method failure (bundle inheritance;
grading reachability while inheriting defectiveness — source is decisive on
"can this path execute" and near-mute on "is it wrong", so UI-shaped
misreadings come back confident, not uncertain; evidence base going stale
mid-audit — `c3c4383`/`ba1e88b` landed during the run and were not re-read),
the two unenumerated verdicts (F49(c) wrong, F49(d) late-enumerated and
holding), the eleven-row source-blind-spot list with settling observations,
the new tier **I — Intentional**, and the REVISED §4 draft now requiring a
positive intent statement (hard tells: player report / dead code / sibling
contradiction / self-contradiction / dev comment; no tell → keyboard
observation before any fix is written). Still not applied — user go-ahead.

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

## Optional modules (6, off by default)

**Players enable them in Options → Mod Options (D05 — live toggles, both
directions, including a first mid-session enable since the 2026-07-29 audit
fix);** the pre-load `SMRFixPack_Optional = { <Id> = true }` table remains as
the override surface for other mods and the test harness.
`SMRFixPack.ListFixes()` reports them as `inactive` with the opt-in reason
until enabled. Files use an `Opt_` prefix instead of `Fix_` to mark them as
not-bug-fixes. Full detail: each module's BUGS.md D-entry and file header;
build history in SESSION_LOG.md.

- **ClassicRockets** (D01, `Code/Opt_ClassicRockets.lua`) — a player-controlled rocket
  parked at the colony keeps its launch ration requested even with no destination selected,
  so drones refuel it while it waits. Only the fuel half of D01; the standing Rare Metals
  export half is deliberately unwritten (see the D01 entry).
- **AcknowledgedWarnings** (D02, `Code/Opt_AcknowledgedWarnings.lua`, added 2026-07-27,
  **`tested` 2026-07-30 — PT-48 PASS in full**) — dismissing "Building Not Working"
  acknowledges the listed buildings until they recover; new breakages always warn
  immediately.
- **ResidencyControl** (D03, `Code/Opt_ResidencyControl.lua`, added 2026-07-27) —
  per-dome/habitat "closed to new residents" policy row; quarantine untouched.
- **MultipleSuns** (D04, `Code/Opt_MultipleSuns.lua`, added 2026-07-27) — lifts the
  Artificial Sun build-once limit and carries the absorbed F39 panel-binding fix.
  **This module is also where F56 would land** if the closed-`wontfix` auto-offload
  decision is ever reopened (user decision 2026-07-26): auto-offload and the export half
  are the same "rockets should load and unload themselves like they used to" request over
  the same machinery, so they ship together behind this one flag or not at all. Do not
  create an `Opt_AutoRocketOffload`.
- **DroneOverhaul** (D06, `Code/Opt_DroneOverhaul.lua`, added 2026-07-28, experimental) —
  closest-fleet-first claim gate on repair/clean work + idle-drone moonlighting for
  saturated neighbor hubs + `SMRFixPack.DroneReport()` telemetry. Stat dials and the
  structural choice are an open decision (DRONE_OVERHAUL_OPTIONS.md), gated on the
  B2 re-run with the v2 stress harness.
- **CohortHousing** (D07, `Code/Opt_CohortHousing.lua`, added 2026-07-28) — Seniors and
  Children in normal housing auto-move into free Retirement Home / Nursery slots (own
  dome first, reachable dome second); employed Seniors exempt, player orders win,
  quarantine/closed domes respected. PT-53 3-of-5 PASS; A/E halves owed.

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
| **F24** | **CLOSED `wontfix` 2026-07-30 (user decision) — fix DELETED.** Real defect (water grid passes `dome` where its electricity twin passes `self`), but **unreachable in the shipped game**: its only live call site can't reach the buggy line (`SpireBase` is not a life-support object), and the `Dome:OnLoad` sweep needs a state vanilla can't produce — domes refuse to place over buildings, no dome has an upgrade, interior shapes never change at runtime. Carried as a 34-line full-function replacement, so deletion beat latency. Counts 75→74 / 69→68. | — done. Rollback is one `git revert` if a counter-example appears. |
| **F49(c)** | **CLOSED `wontfix` 2026-07-30 (user decision) — guard REMOVED. It was fixing DESIGNED BEHAVIOUR**, a different and worse failure mode than F24's unreachable-but-real defect. Established at the keyboard: salvage mode targets objects not hexes, the cursor always names its target (red `Salvage` = no action permitted), the `Salvage Train Station`→`Salvage Track` handoff is seamless to the millimetre, and **no exposed control separates a station from its own connector track**. The propagation the item called a defect is what makes that boundary continuous; the guard would have carved a dead band into it. The module keeps (a) and (d) — counts unchanged. | — done. The reachability audit rated (c) "live R2" **without ever enumerating it**, and its R1-R4 vocabulary cannot express "reachable, but intended" — both ANSWERED in the audit's own "Challenge review 2026-07-30": new tier `I` — Intentional — with (c) reassigned to it. |
| **F28** | **CLOSED `wontfix` 2026-07-30 — barred by the new FIX_POLICY §4a hard rule.** Real defect, but `Research:ReplaceTech` has **zero callers in all of Src** — only mod code or the console can reach it, and it shipped as a §1.5 full replacement (37-line body copy) carrying per-update re-verification cost forever. Not an oversight: the entry said "No vanilla caller" the day it was filed and shipped anyway on a "modder benefit" rationale, which §4a now bars. Fix **and its probe** deleted; counts 74→73 / 68→67, probes 77→76. | — done. Rollback is one `git revert`. Optional later: rebuild the probe as a vanilla canary on the F10 precedent. |
| **F62** | ~~blocked~~ **CLOSED `wontfix` 2026-07-26 (user decision).** Verified identical to the original game (same one-hop algorithm, same two transitive-predicate callers): carried-forward dev vision in both games, breaks nothing. No opt-in module planned. | — done. |
| **F63** | ~~blocked~~ **CLOSED `wontfix` 2026-07-26 (user decision), same grounds** — no training term ever existed in either game's emigration score. | — done. |

Recorded on those entries but deliberately untouched (real inconsistencies, no action):
walkability says A↔C is walkable while services say C is invisible from A;
`CanWorkTrainHereDomeCheck` permits training at a train-reachable school that
`ChooseTraining` never offers; the `PlanetaryAsteroidVisitPossible` legacy branch's
`and`/`or` precedence slip; `IsDifferentAsteroidLocation` comparing a map to a
MapDescriptor. All are permissive failures — none blocks a player.

## Key technical facts — MOVED

The engine-facts section that lived here is now **docs/ENGINE_FACTS.md** (sole
authoritative home; moved verbatim 2026-07-29, audit remediation 3.2).

## Waiting on the user

1. DONE 2026-07-25/26 — retail A/B pairs clean AND the MarsDebug [install] pass is
   complete (49 PASS / 0 FAIL, F73 fully verified — see the QA session leg in
   SESSION_LOG.md).
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
10. **OPEN (2026-07-29): the F81/F78 disaster fix — scope decision.** F81 is
   CONFIRMED LIVE and the leak is unconditional (every completed meteor storm
   strands the flag and kills that colony's weather). Proposed package:
   (a) replace the global `MeteorsDisaster` with a **per-invocation** bounded
   drain loop + guaranteed notification removal on every exit path; (b) a
   one-shot `OnMsg.LoadGame` reconciliation clearing stranded predicted flags,
   which is what heals saves already poisoned; (c) a bounded `WaitMsg` in
   `RainsDisasterLoop`. **Gated on the `QA_REVIEW_PROMPT.md` review** — the open
   danger is how to distinguish a stranded flag from a legitimate warning in (b)
   without suppressing a real disaster warning, plus whether a watchdog (F02
   precedent) beats a full-body replacement that rots on game patches.
   *(Review since fired and both questions answered: `FindNotification` +
   Dismissable=false makes the stranded/legit test sound, and the watchdog DID
   beat the replacement — wave 6 built 2026-07-29 late, PT-54 gates it.)*
11. **OPEN (2026-07-29): D08 — the extender overhaul**, five layers speced in
   `DRONE_OVERHAUL_OPTIONS.md` with a risk table. Recommended order is
   dispatcher → Command Center tab + advisory → cluster scoping → adjustable
   radius → building (last, gated on PT-20). Also gated on the QA review.
9. **OPEN (2026-07-28): the F79 decision** — trains never carry service seekers
   (confirmed vanilla gap, entry has the fix sketch). Feature-completion D-item or
   leave as documented vanilla behavior? This is the only decision currently owed.
   (D07 was decided AND built 2026-07-28 — see the build leg in SESSION_LOG.md.)

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
Four `[DRAFT NOTE]` markers remain in `MOD_DESCRIPTION.md` (lines ~6, ~90 F76 explainer, ~390 ClassicRockets export half, ~448 final) and are
deleted before the text ships. The export-half one is load-bearing: do NOT promise the
ClassicRockets module's unwritten Rare Metals export half.
