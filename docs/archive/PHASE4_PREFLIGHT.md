# Phase 4 preflight — C1 + C2 + C4 rebuild (2026-07-31)

Product of `docs/PHASE4_REBUILD_PROMPT.md` Phase 0. Written BEFORE any code was
touched. The behavioural fingerprint (Phase 0a) is captured separately in
`docs/archive/fingerprint_before.txt` — at the time of writing Mars.exe was in
use by the owner (live play session since 09:52), so the fingerprint leg is
queued behind that session's end; no code will be touched before it runs.

Evidence base: the mandated read list in full; complete fresh surveys of all 75
`Code/` files (every apply()/file-scope self-check with depth classification;
every OnMsg handler with status/veto/status-write classification; all seven
DataLoaded scaffolds; all 17 LoadGame/PostLoadGame sweeps; all global-install
verifier sites; both watchdogs); TestKit probe-dependency inventory; Src
verification of the classdef `__parents` layout (classes.lua:61,:567) and of
the PreGameMenuOpen message (dead in this title — see Q7).

## Measured landscape (fresh, 2026-07-31 — the audit's counts were stale)

- 75 files, 74 registered modules, 68 default-active. Pinned build 1.0.7.396349.
- **12 cloned `log()` helpers** (00_Core, 90_SaveSanitizer, DisasterPredictionLeak,
  DustSicknessBiorobots, DustSicknessDamage, FirstAsteroidPrefabs,
  IndependenceTerraforming, LastTransmissionStorage, MeteorFrequency,
  MeteorStormWedge, RainsDeadlock, Opt_MultipleSuns) — all byte-equivalent in
  behaviour (same prefix, same `%%` escaping).
- **194 literal `return "…"` sites**, of which **~155 are real apply()/install
  self-check reasons**; the rest are watchdog verdicts (F02: 9, F78: 11),
  sweep verdicts (IndependenceTerraforming: 9), and non-reason strings
  (`"Child"`, `"Senior"`, `"patched"`, `"bridged"`). **Plus 13 concatenated
  reason sites** (`return name .. " not found …"`) the literal grep undercounts
  — true reason total ≈ 168 across ≈ 207 string-return sites. Any mechanical
  pass keyed on `return "` alone would miscount; migration works file-by-file,
  not by grep.
- **43 OnMsg handlers in 24 files**: 31 status-gated; only 5 files add the
  separate veto re-read FIX_POLICY §2 asks for; 7 files write status/detail,
  and only 2 of those guard the `"disabled"` status at the write itself (the
  others are protected by an early veto return instead).
- **Seven DataLoaded/DataChanged scaffolds**, four of one family
  (DustSicknessDamage, DustSicknessBiorobots, IndependenceTerraforming,
  LastTransmissionStorage — preset mutators with patched/data_loaded/
  ever_changed flags in varying subsets) and three divergent
  (TechDescriptionBuilding — handlers installed inside apply, no latch;
  Opt_MultipleSuns — detail-only writes plus a reverse operation;
  FirstAsteroidPrefabs — DataLoaded-only existence latch, no mutation).
- **17 LoadGame/PostLoadGame files** in four shapes: 6 AllMapsForEach sweeps,
  2 Cities-label sweeps, 6 one-shot heals/delegates, 3 thread/state resets.
- **10 global-install verify sites in 7 files** (assign + `rawget` read-back +
  bespoke failure string); **2 unverified outliers**
  (Fix_AsteroidLanderAvailable `PlanetaryAsteroidVisitPossible`,
  Fix_MilestoneCrash `CompleteMilestone`).
- **2 hand-rolled watchdogs** (F02 heartbeat-driven via NewDay; F78
  signature-confirmation via NewHour) — structurally different mechanisms, not
  two copies of one shape.
- **EXIST-only self-check tier: 42 of 74 modules (~57%)** — the C4 target list
  (enumerated under Q8).
- TestKit probes reach into 18 named `SMRFixPack.*` internals (publish tables,
  watchdog check functions, sweep entry points, `order`/`fixes`/
  `OptionEnabled`). All are frozen interfaces for this refactor.

---

## Q1 — the declaring-class hazard

**How the design makes the right thing the easy thing (and the wrong thing
loud):**

1. **A passing check is declaring-class-correct by construction.** Mod code
   runs before class flattening, so a class global is a plain classdef table
   exposing ONLY self-declared members (ENGINE_FACTS). If
   `Require`'s `rawget(classdef, method)` finds the method, that class declares
   it — there is no way to "accidentally pass" via inheritance. The hazard
   exists only on the FAILURE path: a check against the wrong class reads nil
   and today masquerades as "game update changed it" (exactly how F64 shipped
   broken).
2. **The failure path gets differential diagnosis.** Classdefs carry
   `__parents` (verified: classes.lua:61 `class_def = { __parents = { … } }`,
   consumed at :567/:694). When a method check fails, `Require` walks
   `__parents` recursively; if any ancestor declares the method, it logs a LOUD
   line naming the ancestor — "check targets X but Y declares it; this is an
   authoring error, not a game update (FIX_POLICY §2)" — and still returns the
   site's reason string so the fix deactivates safely. A wrong-class check can
   no longer masquerade as patch rot. **No auto-heal**: the helper never
   silently substitutes the ancestor, because behaviour preservation forbids a
   check passing today that didn't pass yesterday (and vice versa) without a
   human deciding it.
3. **Migration re-verifies every class choice once.** The survey flagged three
   suspicious sites (Fix_MoraleComfortTooltip's dead `Colonist.GetProperty`
   limb; Fix_ShelterReflex checking `Community.HasLifeSupport` but invoking it
   on a MicroGHabitatAutoResolve receiver; Fix_TrainWaitTime checking only the
   `Station` class table while calling two unchecked methods). Each gets its
   class verified against Src during its migration wave, and 13 sites with
   explicit correct-declaring-class comments become the codified precedent.
   Any current-behaviour defect found this way is FILED, not fixed (brief rule).

"The caller passes the right class" is indeed not an answer; the answer is
that wrong classes are caught at first run (loudly, distinguishably) instead of
silently producing a plausible reason string.

## Q2 — reason strings are an interface

The helper **preserves every reason string byte-for-byte**. Mechanism:

- `Require` spec entries generate the conventional string
  (`<name> not found (game update changed it?)`) from the checked name; any
  site whose current string differs in ANY way (the `changed them?` plurals,
  the `machinery is gone` bespokes, install-verify failures, opt-in gates)
  passes its existing string explicitly. First-failure order is the spec list
  order = the original check order, so the FIRST reason returned is unchanged
  too.
- **The fingerprint legs cannot verify this** — a passing check's reason string
  never appears in any log. So string preservation is verified statically: per
  migrated file, extract the before/after set of reason strings (including the
  13 concat sites) and diff them; the per-stage invariant checklist records
  "reason-string diff: empty" per wave. No generated-instead-of-preserved
  divergence is accepted at all; nobody has approved one.

## Q3 — the two DataPatch lessons

The `DataPatch` runner carries both, structurally:

- **F75 (false-inactive):** the runner owns a `data_loaded` flag per id, set
  only by its own `OnMsg.DataLoaded`. A missing target is a silent return
  before `data_loaded`; the `inactive` latch is only reachable after it. This
  lives in the runner's single latch path — sites cannot forget it because
  sites no longer write it.
- **B3 (re-fire is SUCCESS):** the runner owns `ever_changed`. The engine's
  `Msg("DataChanged", false)` right after every DataLoaded re-runs the pass
  over already-corrected presets; the runner treats "nothing to do after a
  session that changed something" as success and returns without relabeling —
  the exact branch at Fix_LastTransmissionStorage.lua:168-174, hoisted.
- Also hoisted: the veto re-read at the top of every pass (the A1 pattern),
  `detail = ""` never nil (the PT-51 crash), and the DataChanged class filter
  per site.

## Q4 — veto semantics

Verified (fresh survey, matches the brief's 2026-07-31 verification): 13 files
gate handlers on `status == "active"` with no separate veto read, and none of
them heal status — so Register's `"disabled"` latch already makes the status
read honour a pre-load veto. **No live gap.**

- `WhenActive(id, fn)` preserves that AND adds the separate
  `SMRFixPack_Disabled` re-read FIX_POLICY §2 literally requires. For a
  pre-load veto this is redundant by construction (status is `"disabled"`, so
  the gate already refuses); the only behaviour delta is that a MID-Session
  console veto now also stops handlers — which is §2's stated intent and the
  A1-fix donors' existing behaviour. No leg, probe, or shipped surface can
  observe a difference (nothing sets the veto mid-session in any measured
  configuration).
- Status healing: only the DataPatch scaffolds and FirstAsteroidPrefabs heal.
  The runner's heal path refuses to overwrite `"disabled"` (the
  IndependenceTerraforming guard, hoisted). Today that guard is unreachable
  when vetoed (the pass returns early on the veto re-read), so hoisting it
  changes nothing measurable — it just makes the invariant structural.

## Q5 — file-scope ordering

Verified directly: `metadata.lua` `code` list has `Code/00_Core.lua` first
(line 49) and `items.lua` mirrors it; the engine loads code in list order
(FIX_POLICY §8; Mod.lua LoadCode iterates the list). Existing files already
consume `SMRFixPack.*` at file scope (Opt_DroneOverhaul's Register call,
Fix_MeteorFrequency's `SMRFixPack.MeteorsNote` assignment, every file-scope
`OnMsg` handler reading `SMRFixPack.fixes`), so the pattern is already proven
in every leg ever run. All new helpers live in 00_Core; no file gains a
dependency it doesn't already structurally have.

## Q6 — can C1 honestly deliver what its name promises?

**The honest claim is narrower than "N fixes deactivated after game update",
and the narrow version is still worth shipping.**

What the self-checks can notice: a target that was **renamed, removed, or
reshaped** (missing method, changed table layout, missing const). What they
cannot notice — by construction, sandbox has no introspection: a function
**edited in place under the same name**. In that case the pack keeps applying
its 1.0.7.396349 bodies to moved game code and no runtime surface can know.
The dialog therefore must never say "the rest of the pack is fine".

**What ships:** a pregame-menu notice shown ONLY when at least one
default-active fix is `inactive`-with-target-suspect-reason or `error`:
"N fixes in the Community Fix Pack found that the game code they patch has
changed — usually after a game update — and switched themselves off for
safety. Fixes that cannot detect such changes may still need an update: if the
game was recently updated, check for a new version of the Fix Pack." (exact
text at build time, via `Untranslated()`). It reports what was noticed, warns
that noticing is partial, and never implies coverage it does not have. The
after-every-patch extraction diff (WORKFLOW release gate) remains the real
mitigation for the edited-in-place case; the surface's value is that today the
information is log-only — invisible to every console player and most PC
players.

Classification plumbing: helpers mark the registry entry
(`entry.update_suspect = true`) when a target-shape check fails or a DataPatch
latch fires after DataLoaded; `status == "error"` counts too. Reasons that are
NOT suspect: opt-in gates, "turned off in Mod Options", "already
fixed/corrected" verdicts, veto. Unmigrated/bespoke stragglers are covered by
the reason-string convention (`game update changed`) as a fallback classifier.

## Q7 — C1 on consoles

**The report appears at the pregame main menu on every platform, including
Xbox/PlayStation/MS Store.** Mechanism: a standard modal message dialog
(`WaitMessage` — the engine's own surface for "Mod Loaded with Errors",
Mod.lua:2229-2243; dialogs are the universal, gamepad-native UI). One
correction to the audit's precedent, verified in Src: **this title never fires
`Msg("PreGameMenuOpen")`** — the game's `Lua\init.lua:1` replaces
`OpenPreGameMainMenu` and drops the Msg, so the engine's own error dialog
trigger is dead code here. The TestKit already solved this exact problem: poll
`GetPreGameMainMenu()` from a bounded real-time thread (95_AutoRun.lua:191-202,
proven in every unattended leg). The surface does the same — file-scope RT
thread, poll until the menu dialog exists (bounded), then show the dialog once
per session if N > 0. Threads and dialogs at menu time have no savegame
footprint. Mod Options remains where the six toggles live; this notice needs
no player steering, so a read-only dialog is sufficient and universal.

## Q8 — C4 scope: which files, what criterion

**Criterion:** a module is "shallow" if its apply()/install preflight contains
no LAYOUT or CONTENT check — nothing beyond "the global/class/method exists" —
per the full-file survey (not filename age; several "early" files are already
deep, e.g. F01's slot-layout check, and several late files are shallow).

**The EXIST-only tier — 42 modules:** AnomalyCaveInMap,
AsteroidLanderAvailable, CrystalMysteryHang, DestroyedTunnels,
DisasterPredictionLeak, DomeFreeSpaceMismatch, DomeOverviewHighlight,
ExtenderFlapChurn†, FirstAsteroidPrefabs, FounderTraitNotification,
FreedHousingNotice, GeneForging, GhostFarmOxygen, GraphConsumedCaption,
GridGlobalStorage, LakeEntombment, LandscapeUnitFilter, LayoutTechLock,
MilestoneCrash, NightShiftWork, PayloadTemplateRefill, RainsDeadlock,
RocketDroneChurn, ShuttleHubOffAvailable, ShuttleTransportCache,
StaleReservations, TouristApplicants, TrackConnectorPingPong, TrackSalvageWipe,
TrackTunnelPowerBridge, TrainCargoDumping, TrainMinors, TrainWaitTime,
TrainsToVoid, UpgradeModifierLeak, WispRewards, SaveSanitizer,
AcknowledgedWarnings, ClassicRockets, CohortHousing, MultipleSuns,
ResidencyControl. († ExtenderFlapChurn is carved out — drone module; it stays
as-is and is listed only for completeness.)

**What "deepening" concretely means, bounded:** (i) every method call the
patch/replacement makes on a checked class gets a declaring-class Require
entry (the TrainWaitTime gap: `Station` table checked, `AddSpentTime`/
`RemoveColonist` not); (ii) consts and table fields the patched body reads get
LAYOUT entries; (iii) the two unverified global installs gain the standard
read-back; (iv) bare-global indexing (`type(Colonist.X)` with no
`rawget(_G,"Colonist")` guard — NightShiftWork, UpgradeModifierLeak,
MilestoneCrash, TouristApplicants, WispRewards, TrainPlatformWedge) becomes
rawget-guarded so a vanished class reports `inactive (reason)` instead of
`error`. NOT in scope: content signatures of copied bodies (impossible —
sandbox), new behaviour, new messages. Every added check must PASS against the
current build — a deepened check that fails today is a migration bug by
definition and the leg catches it as a status flip.

## Q9 — staging

Principles: one helper family or one wave of call sites per stage; every
intermediate state shippable (helpers are additive; migration never leaves a
file half-cut); an A/B leg + fingerprint diff after every stage; one commit
per stage, pushed; never batch.

- **S1** — 00_Core: add `SMRFixPack.Log`, `Require`, `WhenActive`,
  `SetGlobal`, `DataPatch`, the `update_suspect` plumbing. No call site
  changes, no visible surface. Leg expectation: identical.
- **S2** — migrate the 11 non-core `log()` clones to `SMRFixPack.Log`
  (each becomes `local log = SMRFixPack.Log`). Leg: identical.
- **S3** — migrate the 10 verified global-install sites to `SetGlobal`;
  add read-backs to the 2 outliers (deliberate C4 item, noted). Leg: identical.
- **S4** — migrate the simple status-gate prologues (the plain OnMsg handlers
  from the survey; NOT the watchdog-internal gates whose verdict strings are
  probe-visible, NOT the drone carve-outs) to `WhenActive`. Leg: identical.
- **S5** — migrate the four same-family DataPatch scaffolds
  (DustSicknessDamage, DustSicknessBiorobots, IndependenceTerraforming,
  LastTransmissionStorage) onto the runner, two files per sub-stage with a leg
  each. The three divergent scaffolds (TechDescriptionBuilding, MultipleSuns,
  FirstAsteroidPrefabs) are NOT force-fitted — see scope reductions.
- **S6a-S6d** — `Require` migration of apply()/install preflights in four
  waves of ~13-15 files, metadata order, drone carve-outs excluded; per wave:
  reason-string extract-diff (empty), declaring-class re-verify against Src for
  every method entry, parse sweep, leg. C4 deepening items (i)/(ii)/(iv) land
  WITH each file's wave — one edit per file, not two.
- **S7** — C1 surface in 00_Core (menu poll thread + dialog + log line) + its
  TestKit probe (drives the classifier + dialog-eligibility function directly;
  probe count 77 → 78, deliberate). Leg: identical except the one added probe
  PASS (78-probe totals predicted before the run).
- **S8** — final phase per the brief: three fresh legs, full fingerprint diff,
  packaging invariant, probe-authoring audit, ENGINE_FACTS API re-check,
  certification, docs, delete the brief.

Estimated 10-12 legs at ~90 s unattended each. Every stage is bisectable and
individually revertable.

## Q10 — everything else that worries me (and the scope reductions)

1. **Watchdog consolidation is DROPPED from C2 (scope reduction, preflight
   authority).** The survey shows F02 and F78 are different mechanisms
   (heartbeat-vs-signature, NewDay-vs-NewHour, restart-vs-heal-thread), both
   with probe-visible verdict strings and persisted-thread interactions
   (zero-upvalue discipline). A shared skeleton would be a third mechanism both
   would be force-fitted into — maximum risk, ~zero duplication removed. They
   stay as-is.
2. **The three divergent DataLoaded scaffolds stay custom** (TechDescription's
   inside-apply install, MultipleSuns' detail-only + reverse-op, FirstAsteroid's
   existence latch). Force-fitting them into the runner buys ~40 lines and
   risks three hand-tuned semantics; the runner serves the four-file family it
   actually fits. FirstAsteroidPrefabs' LoadGame gate (not its DataLoaded
   latch) migrates to `WhenActive` in S4 — that part is the standard shape.
3. **Persisted-closure discipline:** helpers must never end up in a persisted
   thread's upvalue chain. `WhenActive` wraps OnMsg handlers (not persisted)
   and the wrapped fn lives at file scope — same persistence surface as today.
   The F02/F78 zero-upvalue bodies are untouched (see 1).
4. **Probe-visible internals are frozen:** the 18 `SMRFixPack.*` names the
   TestKit reads (publish tables, `MeteorsWatchdogCheck`, `StormWedgeCheck`,
   sweep entry points, `HealFirstAsteroidPrefabs`, `order`, `fixes`,
   `OptionEnabled`, `IsEventRocket`, `DescribeDroneDials`) keep their names,
   shapes and verdict strings exactly.
5. **Mod-env API surface:** the helpers use only what the pack already uses —
   `rawget`, plain-assignment global writes, `CreateRealTimeThread`,
   `GetPreGameMainMenu`/`GetDialog`, `OnMsg`, string ops. The one genuinely
   NEW call is `WaitMessage` for the C1 dialog — engine-global UI, used by the
   engine's own mod-error path, not on the ModEnvBlacklist; flagged here per
   the brief ("a helper needing something the pack has never used is a design
   question"): it is the entire point of C1, and the alternative (log-only) is
   the status quo C1 exists to fix. Final API re-check happens in S8 against
   ENGINE_FACTS.
6. **The A/B legs cannot see reason strings of passing checks** (Q2) — static
   extract-diff is the control for the single largest class of migrated text.
   Named here so the certification doesn't overclaim what legs proved.
7. **Fingerprint configuration:** the account is currently in the shipping
   default (six toggles OFF, dials base — read from the live session's own
   log, 68/74 signature). Per-stage legs therefore measure the default
   configuration; the all-toggles-ON fingerprint is captured up front too, via
   the one-way opt-in bridge (temporary `Code/97_OptInLeg.lua`, the
   2026-07-27 precedent, deleted after each use, never committed). The final
   phase's default leg then needs nothing from the owner UNLESS the account
   state changes mid-job — if it does, the brief's rule applies (ask, never
   fake).
8. **Defects noticed en route** (candidates so far: the MoraleComfortTooltip
   dead check limb; ShelterReflex's receiver-class mismatch) are check-quality
   items INSIDE C4's remit — they get correct Require entries in their waves,
   with the class verified against Src, and anything that turns out to be a
   live behaviour defect is filed in BUGS.md instead of fixed (brief rule).
9. **PowerShell/encoding discipline** per ENGINE_FACTS tooling note and the
   memory on commit quoting (`git commit -F`); parse sweep via python +
   luaparser before every commit.

## Verdict (0c)

The plan is sound with the two scope reductions above (no watchdog skeleton;
no force-fit of the three divergent scaffolds). Q6's honest-narrow C1 is worth
shipping. No stop condition is met; no owner input is required until the final
phase's default-config leg (and none even then unless the account state has
moved). Proceeding: fingerprint capture (0a) as soon as Mars.exe is free, then
S1.
