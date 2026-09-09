# 07 · Test Kit — make the suite tell the truth about THIS build

Chain: `prompts/hotfix2/README.md` (its binding rules are yours). **Runs after
02, 03, 04 and 04b** — it needs the FINAL module set. Independent of 05 and 06.
**Before 99**: the audit's Pass A re-runs the instruments and Pass G lists what
was never exercised, and both are meaningless while ~40 of the kit's 100 probes
describe a pack that no longer exists.

⚖️ Authored 2026-09-08 by link 04's session (`smr-bugfixpack-ba`) on the
owner's call — *"Agreed, make the 07"* — after the chain was found to have **no
owner for the Test Kit at all**: every link's fence put it outside, 05's "In"
list is `sigcheck`/`logscan`/`GeneForging`, and 99 can only report. The kit is
`C:\Dev\SMR-BugFixPack-TestKit`, a **separate, local-only repo with no remote**
(settled; never raise a push as owed). Its `SMRTest.RunAll()` pack-off /
pack-on pair is the standard regression measurement (`WORKFLOW.md:309`), and
the post-99 sitting is where it will next be run.

## 0 · Start

`git log --oneline -10` · `git pull` in the PACK repo · `git log --oneline -5`
and `git status` in the KIT repo (no pull — no remote) · `ListAgents`. Staleness
anchor: pack `55b1d5e` (link 04 closed), kit `ec2cc52`. Todo list first, one
item per commit-and-verify unit (the units in §2 are a floor, not a ceiling —
expand the moment a unit turns out to be several).

**Read path:** kit `README.md` (the three-mod rule and "Known probe defects") ·
kit `Code/00_TestCore.lua` (`Register` `:375`, `FixMissing` `:315-327`, `RunAll`
`:417`, `FromFixPack` `:123`, `HasGame` `:172`, `WithGlobals` `:257-309`) ·
`agent/WORKFLOW.md` "Probe hygiene — HARD GATE" (`:138-175`) and element 7 of
"Authoring a prompt" (`:1067`) · `tools/doccheck.py:538-548` (the probe count
that feeds STATE's build-state block) and `:583-600` (the kit-tree rule: a dirty
kit tree is REPORTED on every pack run and is routed or committed, never
restored) · `prompts/hotfix2/README.md` rows 02, 03, 04, 04b (what changed in
the pack) · `reports/PACK_1_1_0_REVERIFICATION.md` §1b (why each REMOVE left —
you need the reason to know what a retired probe should now observe) ·
`99_TERMINAL_AUDIT.md` §4 Pass C and its Notes from upstream at `:643-660`
(link 03's two false-FAILs, with line numbers) and `:835` (link 04's) · your
inbox below · `agent/bugs/INDEX.md` for any status you cite.

## 1 · The census — what is wrong with the kit today (measured 2026-09-08)

100 registered probes (`doccheck` counts `SMRTest.Register(` occurrences minus
the definition). Against the pack at `55b1d5e`:

| probes | state | what a suite run shows |
|---|---|---|
| **37** | target a module link 02 DELETED (`2dc1dbe`) | `FixMissing` → FAIL "fix pack not loaded" for every one, or an install probe's "still the shipped one" FAIL |
| **3** | FALSE-FAIL on a LIVE module (03's two, 04's one) | FAIL that reads as a regression and is the probe being stale |
| **3** | pre-chain orphans (`FactionFundingCheck`, `ClassicRockets`, `DustSicknessBiorobots`) | already FAIL/SKIP before this chain; triage, do not assume |
| 2 | pack-wide sweeps whose target TABLES list deleted modules (`DispatchReach`, `LandscapeCostGuard`) | noise rows, not verdict changes |
| 1 | `SpaceYDroneCapBullet` (`fix = None`, module deleted as R-30) | stale |
| ~54 | live, believed current | ⚠️ "believed": nobody has run the suite on 1.1.0 |

⇒ the pack-on leg would print ~45 FAILs, of which zero are regressions. That is
a suite that trains the reader to ignore FAIL — the exact failure the kit's own
README warns about.

## 2 · The job — three units, each its own kit commit

### Unit A — the 37 orphans become a "vanilla fixed it" suite (kind `retired`)

⭐ **Do not delete them.** Every probe in the kit was built to run on an
UNPATCHED game — that is the pack-off leg of the A/B — so the 37 already know
how to observe the defect on vanilla. On 1.1.0 the REMOVE verdicts say vanilla
fixed those defects. So a retired probe run with no module present has a
meaning the pack has never had a machine check for:

* **PASS** = the fixed behaviour is observed on vanilla ⇒ the REMOVE verdict is
  confirmed **in-game**;
* **FAIL** = the defect is present ⇒ a REMOVE was WRONG (R-15's shape — the
  direction that costs players a fix) ⇒ a finding for 99, not a probe bug;
* **ERROR** = the probe's stubs are 1.0.7-shaped and 1.1.0 changed the
  function under them ⇒ the probe is stale, file it, and it is NOT evidence
  either way.

Mechanics:
1. Add `SMRTest.FixRetired(id)` to `00_TestCore.lua` beside `FixMissing`
   (`:315-327`): FAIL if `SMRFixPack.fixes[id]` (or whatever `FixStatus` reads)
   is registered — a retired module that came back is a real defect — and
   otherwise fall through to the probe body. Add `retired` to the kinds table in
   the README with the three-way reading above.
2. For each of the 37 (list in the inbox, with file and line): swap the
   `FixMissing` guard for `FixRetired`, set `kind = "retired"`, and **read the
   body** for anything that assumes the pack is present — `FromFixPack(fn)`
   asserts (the 4 `install` probes invert: FAIL if FromFixPack), `SMRFixPack_*`
   fields the probe expects the module to have written, `SMRFixPack.Log` hooks.
   A probe that only makes sense with the module present (an install probe
   with no behaviour half) is DELETED, named in the commit message.
3. ⛔ **A guard swap is not a re-derivation.** Where the body's stubs name a
   function 1.1.0 rewrote (§1b's rows say which — e.g. `Community:GetScoreFor`
   now takes the colonist, `TraitPreset:AddDomeColonistsModifier` resolves the
   label itself), expect ERROR and say so in the probe's header rather than
   patching the stub blind. A blind stub patch that happens to PASS is a false
   "vanilla fixed it" — the direction that retires a live fix.
4. `RunAll` prints its gate line `fix pack present: %d/%d fixes active`; the
   denominator must not count retired probes as expected fixes. Read `:417-465`
   before touching it.

### Unit B — the false-FAILs on live modules, rewritten against the NEW bodies

* **`PayloadTemplateRefill`** (`30_Probes_Wave3.lua:11-70`). It stubs
  `CreateRealTimeThread` to a no-op and expects `C.Apply(dialog)` to stamp the
  flag synchronously. Since `177c7b2` the stamp is INSIDE the thread's confirmed
  branch. Stub the thread to run its function immediately
  (`CreateRealTimeThread = function(fn, ...) fn(...) end`), give the dialog
  `GetCargoList = function() return {} end` and `PromptRocketCargoIssue =
  function() return nil end` (nil = confirmed), and the transporter a
  `SetCommand` capture and `command = "CmdWaitOrder"`. Then add the case the
  fix now guarantees: a prompt that returns `2` (cancel) with a `CancelFlight`
  capture must NOT stamp. ⚠️ Read `Code/Fix_PayloadTemplateRefill.lua`'s `Apply`
  copy first; the probe's stubs must match ITS calls, not your memory of them.
* **`SaintBlessing`** (`57_Probes_Wave8.lua:123`; the static half at
  `:139-143`). It asserts we rewrote `Saint.modify_trait`, which on 1.1.0 we
  deliberately no longer do (`3db4984`: a behaviour probe picks the branch).
  The truthful assertion is the OUTCOME on either branch — a Saint's dome
  modifier is filed under the label colonists actually carry — not our
  mechanism. Read the module's design first — the `Require` probe at
  `Fix_SaintBlessing.lua:192-195` and the two-probe pass that follows it (the
  header's STUB CONTRACT at `:156-190` explains both) — and 03's note in 99
  (`:649-654`) before writing.
* **`ShelterReflex`** (`20_Probes_Wave2.lua:182-196`). It tests half (a),
  deleted on purpose (`19b5aaa`). Drop the half-(a) assertions; keep half (b)
  (the `Idle` pre-wrapper). 03's note at 99 `:655-660` names the lines.
* **04b's three** — `VacuumWalks` (`20_Probes_Wave2.lua:472`),
  `LandscapeUnitFilter` (`30_Probes_Wave3.lua:276`), `TrainCargoDumping`
  (`30_Probes_Wave3.lua:1099`) — are re-copies with gates. Read 04b's outbox in
  99 for what each body now does and whether its gate DECLINES on the rig; a
  probe for a gated-off module must SKIP with the reason, not FAIL.
* **`GeneForging`** (`30_Probes_Wave3.lua:828`) — 05's A-1 edit changes how the
  module reads the map. If 05 has closed, re-read its outbox; if not, leave the
  probe and say so.

### Unit C — the sweeps, the counts, the surfaces

* `DispatchReach` (`64_Probes_Wave14.lua`): its `DISPATCH_TARGETS` table
  (`:91-197`) is a hand list of `{module, class, method}` Require targets. Rows
  for deleted modules go; rows for modules whose `Require` changed (F-1, F-3,
  F-6 gained/lost targets) are regenerated from the modules' `Require` blocks —
  `tools/harvest_wrap_targets.py:require_blocks` already parses them; reuse,
  do not re-implement. `LandscapeCostGuard` (`:501`) keys on
  `LandscapeCostRefresh`, deleted as R-26: retire it.
* `SpaceYDroneCapBullet` (`63_Probes_Wave13.lua:65`): module deleted (R-30);
  convert to `retired` or delete with the reason.
* ⛔ **`99_FixtureCarry.lua` is NOT yours.** Its field list
  (`SMRFixPack_payload_set` and the rest) is the SAVE FOOTPRINT — those fields
  exist in players' saves whether or not the module still ships, and the
  save-rescue mod is the cleaner. Do not "tidy" it to the live set.
* ⛔ The harness files (`95_AutoRun`, `96_AutoRunFlag`, `97_ForceInactive`,
  `98_EnablePathLeg`) are owner-armed legs. Never arm one; do not edit them.
* The pack's `doccheck --emit-counts` probe count WILL change. Re-emit STATE's
  build-state block in the pack commit (rule: never hand-typed), and the
  `TESTKIT TREE:` line must read `clean` at that commit — the kit commit lands
  FIRST.
* Kit `README.md`: the kinds table gains `retired`; "Known probe defects" gains
  the three false-FAIL shapes as a fourth trap ("a probe that asserts our
  MECHANISM breaks when the mechanism changes branch; assert the OUTCOME").
* `docs/PLAYTEST_CHECKLIST.md`: the LINK 03 and LINK 04 blocks each warn the
  owner that named probes FALSE-FAIL. Once repaired, replace those warnings with
  ONE line each pointing here and stating the new expected census (below) —
  the owner reads those blocks before the sitting.

## 3 · The expected census — write it down, it is the sitting's yardstick

Your close-out MUST state, for a 1.1.0 rig with the pack ON and with it OFF:
how many probes are `behavior`/`install`/`state`/`manual`/`retired`, and for
each kind the expected verdict distribution (which ones SKIP without a colony,
which are expected ERROR and why). Put it in 99's inbox (Pass G) and in the
checklist LINK 07 line. ⛔ Every number is a PREDICTION until the sitting runs
`RunAll` — say so in the same sentence.

## 4 · Scope fence

**In:** kit `Code/00_TestCore.lua`, the probe files `10_`–`64_`, kit
`README.md`; in the pack repo ONLY: STATE's emitted block, this chain's README
row, the two checklist lines named in Unit C, 99's inbox.
**Out:** every pack module and `items.lua`; `tools/*` (05 owns the tools tail;
`doccheck`'s count is derived and needs no edit); `60_Probes_Opt.lua` and
`65_Probes_Rescue.lua` (other mods, other registries); `99_FixtureCarry.lua`;
the four harness files; `90_Loggers.lua`/`91_Stress.lua` unless a deleted
module's logger throws on load — then the logger only, named.
Found something out of fence? **File it, do not fix it.**

## 5 · The hard gate (WORKFLOW "Probe hygiene", element 7)

`grep -rln "TEMPORARY" Code/ ../SMR-BugFixPack-TestKit/Code/` BEFORE you start
and before every commit; the sweep line goes in the todo list and every commit
message carries its result. Nothing here runs in a game, but you are editing the
instrument itself: a `TEMPORARY` marker you add for a local experiment leaves
with the same commit that answers it.

## 6 · Stop conditions

- A retired probe's body needs a real 1.1.0 re-derivation, not a guard swap ⇒
  mark it expected-ERROR in its header, file it, move on. Do not rewrite stubs
  you have not read the 1.1.0 function for.
- A probe would need a REAL game object instantiated to work ⇒ **STOP.** F49's
  PT-46 incident left orphan objects blocking grid hexes on a live colony; the
  kit's rule is plain tables with a class metatable, never `PlaceObject`.
- The kit's working tree is dirty with a STRANGER's changes ⇒ never restore
  (`doccheck.py:583` — uncommitted work has no reflog); message the peer.
- Unit A will not fit with B and C ⇒ split at a clean commit (`07b`), README
  row, full inbox. 37 body reads is the likely place.
- `RunAll`'s gate line or `FixMissing` semantics turn out to be load-bearing for
  the opt-in / rescue probes ⇒ **STOP AND ASK** before changing shared code;
  the README's three-mod rule exists because one kit serves three mods.

## 7 · What may NOT be claimed

- ⛔ Not "the REMOVE verdicts are confirmed" — retired probes are UNRUN until the
  sitting. This link makes the suite ABLE to confirm them, nothing more.
- ⛔ Not "the kit is verified" or "the suite is green" — nothing ran in a game.
  A parse sweep (`load()` under Lua 5.4 via `lupa`, see the inbox) is syntax.
- ⛔ No status word moves anywhere, and no bug entry gains "tested".
- ⛔ Not "the three false-FAILs are fixed" until the sitting's pack-on leg prints
  PASS for them — until then: "rewritten against the new bodies, unrun".

## 8 · Close-out

Kit commit(s) first (local; no push exists), then the pack commit: STATE block
re-emitted, README row struck, checklist lines replaced, outbox appended to
`99_TERMINAL_AUDIT.md`'s Notes from upstream — per Unit: what was converted /
rewritten / deleted (BY NAME, never a total — SKIPs by name is a standing rule),
the expected census (§3), the expected-ERROR list, and the drift you caught
(chain rule 5). `git rm` this file. Gates: `doccheck` GREEN with `TESTKIT TREE:
clean`, `TEMPORARY` sweep clean in both repos, parse sweep over kit `Code/`.
Commit with `git commit -F <file>`, push the PACK repo only.

## Notes from upstream

*(From the authoring session — link 04's, `smr-bugfixpack-ba`, 2026-09-08.
Nothing here ran in a game.)*

**1 · The census, re-derivable.** Classification = every `SMRTest.Register("X",
{ … fix = "Y" … })` in kit `Code/*.lua`, `Y` matched against (a) the file
names deleted in `2dc1dbe` and (b) the ids registered by any
`SMRFixPack.<Call>("Y"` in pack `Code/*.lua`. ⚠️ Two live modules register
through a variable (`90_SaveSanitizer.lua:254`, `FIX_ID`) or a data-patch call,
so a naive `Register("` regex undercounts live ids by three — my first count
said 50 orphans, the true figure is 37. Check the call, not the name.

**2 · The 37, by file and line** (`kind` as registered today):
`10_Probes_Wave1.lua` :10 CaveInsNoDisasters (install) · :39 MeteorFrequency ·
:132 UpgradeModifierLeak · :186 MilestoneCrash (install) · :276 TouristApplicants
· `20_Probes_Wave2.lua` :58 LanderCargoRatchet · :105 LanderReturnFuel · :617
DroneUnreachableForever · :740 TouristSatisfaction · :774 TrainPlatformWedge ·
:803 LowStorageWarning (install) · :833 CommandCenterNumbers ·
`30_Probes_Wave3.lua` :342 SmallLandscapeSites · :633 AsteroidLanderAvailable ·
:702 AutoExportPriority (fix=LanderCargoRatchet) · :884 DustSicknessDamage ·
:1041 UniversityOvertraining · `40_Probes_Wave4.lua` :341 GridGlobalStorage ·
:413 LastTransmissionStorage · :669 MoraleComfortTooltip · :767
StorageRateModifiers · :942 IndependenceTerraforming · `50_Probes_Wave5.lua`
:238 TrainMinors · :452 TechDescriptionBuilding · `55_Probes_Wave6.lua` :16
DisasterPredictionLeak · :64 MeteorStormWedge · :131 RainsDeadlock ·
`56_Probes_Wave7.lua` :39 FirstAsteroidPrefabs · `57_Probes_Wave8.lua` :182
DustDevilsDescrMap · :243 AsteroidVisitPrecedence (fix=AsteroidLanderAvailable)
· :315 AstrogeologistExtractors · :421 DustStormBreakMapFilter
(fix=DustStormUndergroundBreaks) · `58_Probes_Wave9.lua` :39 DustDevilSpawnGate
· `59_Probes_Wave10.lua` :54 AutomationLawCompensation · `62_Probes_Wave12.lua`
:61 LocalizedUIText · `64_Probes_Wave14.lua` :258 DispatchReach
(fix=SmallLandscapeSites — a SWEEP, Unit C, not a retirement) · :501
LandscapeCostGuard (fix=LandscapeCostRefresh — Unit C). ⚠️ Line numbers are as
of kit `ec2cc52`; they move as you edit — re-grep, do not trust these after the
first commit.

**3 · The pre-chain orphans, with provenance.** `FactionFundingCheck`
(`10_Probes_Wave1.lua:313`): the module was deleted at pack `86bddef` (F10
closed wontfix, PT-36) — a probe that outlived its module by weeks, and nobody
noticed because nobody ran the suite; an existing `retired`-shaped case.
`ClassicRockets` (`30_Probes_Wave3.lua:88`): the module moved to the opt-in pack
at `0efb87e`; its probe should be an `OptMissing` SKIP, not a `FixMissing`
FAIL — the README's three-mod rule. `DustSicknessBiorobots`
(`30_Probes_Wave3.lua:935`): no deletion under `Fix_`/`Opt_` names in the pack's
log; find where it went before deciding (grep the pack's `git log -S`).

**4 · The three false-FAIL causes are already diagnosed** — 99 `:643-660` (03's
two) and `:835` (04's). Do not re-derive them; read the new module bodies and
write the probe to the outcome.

**5 · There IS a Lua parser on this rig.** `python -c "import lupa"` — Lua 5.4
via `lupa 2.8`. Link 04's parse sweep is `load(src)` over every file with a
falsifier (a chunk missing an `end` must go RED); it lives in that session's
scratchpad, not in `tools/`. Rebuild it in ten lines and run it over kit
`Code/` before every commit — the kit has never had a syntax gate, and a probe
file that fails to load takes every probe after it in the file down silently.
⚠️ The engine's Lua carries `goto`/labels and `//`; Lua 5.4 parses both.

**6 · What the sitting will do with your census.** The owner's post-99 sitting
runs `RunAll` pack-off and pack-on on a 1.1.0 colony. Its readable output is
your prediction versus the print: every FAIL not in your expected list is either
a real regression or a probe you got wrong, and 99's Pass G will hold that line.
Make the prediction specific enough to be falsified.

**7 · Chain-rule 5 drift already on record, so you do not repeat it.** Link 03
and link 04 each filed their false-FAILs as "outside the fence" and routed them
to 05/99 — correct per their fences, but it left a 40-probe gap invisible to the
chain until the owner asked "what fixes the test kit?". The fence was right; the
chain's decomposition was missing this row. If you find another repo or surface
the chain assumes someone else owns, name it in 99's inbox rather than filing it
sideways.

### From link 04b — what the three group-C probes should now observe (2026-09-09)

*(Link 04b, `smr-bugfixpack-94`, 2026-09-09. Commits `799f145` F-8 · `3d4c933` F-10 ·
`7a401f1` F-9. ⛔ Nothing ran in a game. I did NOT touch the kit — this is read from its
source against the new module bodies.)*

⛔ **All three modules now APPLY on the rig** (their gates pass on 1.1.0 and decline on
1.0.7), so none of these probes may SKIP on "gated off" — they must run. Two will `ERROR`
as written, one should PASS:

* **`LandscapeUnitFilter`** (`30_Probes_Wave3.lua:276`) — **will ERROR.** It calls
  `LandscapeForEachUnit(MARK, cb)` (the 1.0.7 two-argument shape) with a stub `Landscapes`
  GLOBAL. Our body is now `(map, mark, callback, ...)` reading `map.Landscapes[mark]`
  (`Landscaping.lua:509-510`), so `map` binds to the number 4242 and `map.Landscapes`
  throws. Rewrite: build `local map = { Landscapes = { [MARK] = { mark = MARK, grid = ... } } }`
  and call `LandscapeForEachUnit(map, MARK, cb)`; drop the `Landscapes` entry from
  `WithGlobals`. Everything else (the `Landscape_ForEachObject` stand-in, `IsValid`, the
  {walker, boarder, walker} list) still fits: expect **1 unit reported, the boarder
  skipped** — the same PASS text as before. The desk harness got exactly that from the
  installed body.
* **`VacuumWalks`** (`20_Probes_Wave2.lua:472`) — **will ERROR.** The 1.1.0 body computes
  `need_work = self:CanWork() and not IsValid(self.workplace) and not self.user_forced_workplace`
  first (`Colonist.lua:1896`), and on the walk branch calls `self:DiscardTransportTicket()`
  (`:1918`) and, when `need_work`, `dest_dome:ReserveWorkplace(self)` or
  `self:CancelWorkReservation()`. The stub colonist has none of these ⇒ `attempt to call a
  nil value (method 'CanWork')`. Rewrite: add `CanWork = function() return false end`,
  `DiscardTransportTicket = function() end`, `CancelWorkReservation = function() end`,
  `workplace = false` to the colonist; keep `transport_task = false`. Note the walk branch
  is now also conditional on `not (self.transport_task and self.transport_task.shuttle)`
  (`:1898`) — `transport_task = false` satisfies it. The constants are read from
  `g_Consts` at call time; the suite runs in-game so that is fine, but a `WithGlobals`
  override of `const.ColonistMaxDomeWalkDist` would no longer reach the body. Expected on
  the fixed body: vacuum 300 m ⇒ `SetCommand("TransportByFoot", dest, fake_path)`, 1
  lookup; breathable ⇒ path `nil`, 0 lookups — the probe's existing PASS shape.
* **`TrainCargoDumping`** (`30_Probes_Wave3.lua:1099`) — **should PASS as written.** The
  fake stations carry `demand[res]` with `GetTargetAmount` and their own
  `IsResourceEnabled`, and `storable_resources = { res }` so the carried BlackCube hook
  (`res == "BlackCube"`) is never reached. `task_requests = {}` is now unread by our helper
  (harmless). All three cases (dump refused when elsewhere accepts; accepted when enabled;
  allowed when nowhere accepts) matched on the desk harness against the installed body.
  ⚠️ Its PASS is a statement about OUR guard on a stub that ASSERTS a positive target
  amount — it does not settle whether a suspended 1.1.0 request reports one (checklist row
  10). If you add a case, the F114 input is the valuable one: a storable resource with
  `demand[res] == nil` must NOT throw on the installed body.

**Census effect:** 2 more stale results (both `ERROR`, not `FAIL`) on top of the three
FALSE-FAILs from 03/04 — five named, until you rewrite. After the rewrite the predicted
suite reading for these three is 3 PASS. ⛔ None of that is evidence about a map.
