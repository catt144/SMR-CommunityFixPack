# Session Log — append-only, newest first

Every session leg lives HERE (moved out of STATUS.md 2026-07-29, audit
remediation 3.3; new legs are PREPENDED below this preamble). Everything in
this file is **history**: counts, statuses and "next" claims were true when
written and are NOT maintained — the current state lives in `docs/STATUS.md`,
defect truth in `docs/BUGS.md`, engine facts in `docs/ENGINE_FACTS.md`.

---

## 🛑 PT-20 FAILED — WE LEAK EXECUTABLE CODE INTO PLAYER SAVES (F86, P1, blocks release) — 2026-07-31 late (live sitting, owner at the keyboard)

Started from `docs/FABLE_NEXT_PROMPT.md` at `84427e1`. The plan was PT-20 plus
the F74/F53(a) riders. PT-20's steps 1-4 passed; **step 5 — executed for the
first time — found a P1 defect in our own pack**, and the riders were dropped
because the leg proved they cannot be run on this colony at all.

### 1. Setting the trap (the part that made the answer interpretable)

`PT-20TEST` cut from the 288-sol `test 2i`. Positive-control reads with the pack
ON: `MeteorFrequency` `active`, `IsValidThread(Meteors)` `true`, heartbeat phase
`rolled`. Descriptor read: spawn 65 h (+0-25 h), warning **75 h — capped**, i.e.
this colony is tower-rich.

**Two dead ends, both killed by controls before they could produce a false pass:**
- `debug.getinfo` — proposed as an instant read of the thread's body. It is
  **unavailable in the mod sandbox**, which `ENGINE_FACTS.md:69` already recorded
  and the Test Kit logs on every boot (`no debug.getinfo … [install] probes will
  SKIP`). Should have come from the facts file; cost one console line.
- `Wakeup(Meteors)` — proposed to force the in-flight `Sleep` to resume. **It
  only wakes `WaitWakeup` sleepers** (`thread.lua:62-71`). The positive control
  (phase still `rolled` afterwards) caught it immediately.

**What worked:** compress the next roll to 2 h (`GetMeteorsDescr()` returns a
live preset table — `TerraformingDisasters.lua:54-99` returns `original` or a
sibling, no copy), `RestartGlobalGameTimeThread("Meteors")`, confirm the phase
advances to `long-sleep-done`, pause, save at sol 290. The next wake is then
bounded to ~2 game hours, so a null result would have been *interpretable*
rather than "maybe it hasn't woken yet".

### 2. The result — F86

Pack disabled in the Mod Manager, save reloaded:

```
[LUA ERROR] attempt to index a nil value (global 'SMRFixPack')
  Mod/SMR_CommunityFixPack/Code/Fix_MeteorFrequency.lua(106):   <>
Locals:  spawn_time | number 60000     <-- the value WE injected before saving
         hit_time   | number 60000
```

Our stack frame, with our local variables, came back out of the savegame. The
`Meteors` thread then died: **that colony gets no more meteors, permanently**,
and a save written afterwards carries the dead thread (`_fixup.lua:54-55` only
rebuilds when the save carries *nothing* for the name), so it does not self-heal.

Alongside it, **98** errors from `Opt_DroneOverhaul.lua(190)` via drone command
threads — **with its own opt-in toggle OFF**, because the wrapper installs at
file scope and only early-returns. Harm there is log-only: line 188 runs
vanilla's `Idle` to completion first, and drones were observed working normally.

**Mechanism:** a save captures every game-time thread **with its blocked stack**;
a mod function is serialised **by value** (not in `PersistGatherPermanents`), and
each mod env is a permanent (`Mod.lua:1642-1644`) which cannot resolve after
removal — `Unpersist missing permanent: Mod/SMR_CommunityFixPack | Fallback
permanent: table` — so the orphan runs with an empty `_ENV`.

**This voids an audit clearance.** The 2026-07-31 audit asked *where is the
function stored* and cleared class tables. `Drone.Idle` is a class-table write
and leaked anyway. The route is the stack, not the storage.

### 3. Controls (owner-directed escalation ladder)

Rung 1 — junction physically removed (`1 mods installed`, Test Kit only) —
**reproduced identically against the same save file**: 98 vs 98 drone errors, the
same single meteor error with the same locals; the only difference was the
engine's wording (`present, but not loaded` → `not present`). Rungs 2-3 (Steam
verify, reinstall) were stood down by agreement: no game-install state can invent
our injected `spawn_time 60000` inside our own frame. A repo backup was taken to
`B:\Dev mod backup\2026-07-31_pre-uninstall-test` (both mods, byte-verified)
before the junction was touched; junction restored afterwards.

**A false alarm worth keeping:** a `rawget` sweep found `GetPriorityForRequest`
on **192 buildings**. That is vanilla — `RequiresMaintenance.lua:94` flattens it
onto every instance that does not require maintenance (26 distinct per-class
functions, none equal to the base). Neither mod writes that member. Presence-based
orphan detection is useless here, and comparing against the class value
false-positived on all 192 — which hardens the cleanup mod's "leave identifiable
markers" condition with a failed attempt rather than a theory.

### 4. A second, independent finding — MODS DO GET A SAVE HOOK

`ModMsgBlacklist` (`Mod.lua:1430-1440`) blocks only `PersistSave`, `PersistLoad`,
`PersistGatherPermanents` and five non-save messages. A Test Kit probe
(`97_SaveHookProbe.lua`, temporary) proved it, with `OnMsg.LoadGame` as a
positive control:

```
[SMRTest][savehook] LoadGame FIRED (positive control)
[SMRTest][savehook] SaveGameStart FIRED — params=table: … SavingGame=true
[SMRTest][savehook] SaveGameDone FIRED — name=savesavetest.savegame.sav autosave=nil err=false
```

**This falsifies the recorded "mods get no save hook / tidying up on save is
unimplementable" fact** in `STATUS.md` and the D06 cleanup-mod argument, both now
corrected. Autosaves are the same path (`SaveAutosaveGame` sets one flag and
calls `DoSaveGame`, `Savegame.lua:1450-1453`) — so the hook covers them, and so
does the leak. ⚠️ Which is also the trap: autosaves fire ~once a sol, so a
tear-down that *restarts* a long loop would reset a 35–115 h timer forever,
recreating PT-01's silence from our own code. Re-arm from a persisted deadline.

### 5. F02's root cause, sharpened (owner asked)

Not "a dead `if`" — a **collapsed polling loop**. The fossil in
`Meteors.lua:280-283` is the loop that still exists intact 40 lines below in
`MeteorStorm` (`:319-341`): same `start_time`, same comparison, same `Sleep(5000)`,
but with the `while` removed and the loop body pulled inside the `if`.
`Min(spawn_time, warning_time)` is **not** the bug — it is the correct clamp, and
`DustDevils.lua:171` has it verbatim. Consequences: towers *accidentally repair*
the cadence (no towers → 6 h; several → 65-75 h), and sensor towers contribute
nothing to single-meteor warning because that comes from `Predict()` /
`prediction_time` (30 game seconds, tower-independent). **Owner decision: that 30
seconds is adequate; tower-scaled meteor warning is a feature and is declined.**

### 6. What this costs us

- **F86 blocks release** (FIX_POLICY §3 — the pack must never hold a save hostage).
- **12 modules exposed**, ~62 safe by construction (synchronous code cannot be
  captured — a save only captures *blocked* threads). Full list on the F86 entry.
- **`Fix_ShelterReflex` is the one to measure next**: it wraps `Colonist:Idle`
  like the drone leak but ends `return orig_idle(self, ...)`, a proper tail call,
  which should replace our frame. If that holds, it becomes a cheap coding rule
  for the whole wrapper class.
- **F74 and F53(a) are un-runnable on this colony** and the PT-20 bundling is
  retired: any save whose colony was ever played with the pack installed carries
  pack code, so switching the pack off does **not** produce a vanilla control.
  They need a colony that has never had the pack — a fresh 10-minute save.
- **Redesign proposed, nothing built, owner decision owed**: patch synchronous
  inputs instead of replacing blocking bodies (F02 then needs no body at all), a
  tail-call rule for wrappers, `SaveGameStart` tear-down for the remainder.

### 7. Housekeeping

Junction restored and verified (75 `Code/` files through the link) — **the pack
is still unticked in the Mod Manager and must be re-enabled**. The temporary
`97_SaveHookProbe.lua` is still armed in the Test Kit (local-only, never ships)
and should be removed once the autosave firing is confirmed on the keyboard.

---

## ALL FOUR DRONE RESEARCH GATES ANSWERED + F83 `tested` — 2026-07-31 (live playtest sitting, owner at the keyboard)

Started from `docs/FABLE_NEXT_PROMPT.md` at `4d0d453`. Two jobs came in ahead of
plan and a third emerged from a mistake.

### 1. PT-59 PASSED IN FULL → F83 `tested` (`8387aaf`)

- **(A) reload leg** — counters **1/1/1**, flag `true`, exactly one
  `recovered after a save/load (3 granted)` line; answering the re-shown popup
  left it at 1/1/1.
- **(B) healthy leg** — **1/1/1** with `SMRFixPack_FirstAsteroidPrefabs` still
  `false`. Vanilla granted; our code never ran. That is the double-grant guard.
- **(C)** — exceeded: the sitting logged **10 game loads against exactly 2
  grants**, 14 minutes apart, with **7 non-granting loads between them**.
- Unasked-for results: the heal **discriminated between two asteroid
  notifications** sitting in the corner list together, and **8 of 10 loads
  granted nothing** — the no-op path is the common one and it is silent.
- ⚠️ **The test's own procedure was WRONG and is corrected.** It never said which
  popup to answer; answering `ReconCenterDiscoveryAsteroid` yields `0/0/0`,
  indistinguishable from a fix failure, **and it was reported as a FAIL** before
  source settled it. Another instance of the standing rule that an un-run PT's
  procedure is unverified until executed once.

### 2. The four gates — ALL ANSWERED

- **Q3 + Q4 fell to SOURCE, not playtesting** (`cd37235`). **Q3a:** use the
  game's own class test `IsKindOf("AirProducer"/"WaterProducer")` — docstrings
  claim completeness — catching exactly five buildings; the property test the
  brief proposed would have **missed one**. **Q3b:** the Food-demand test alone
  catches six, two of which are *residences*; adding `ServiceWorkplace` gives
  exactly four. **Q4:** defaults are omitted from saves, five-step chain, and
  **no template in the game sets `priority`**. Live-confirmed both branches
  (`2708d24`): untouched `ShopsFood_Small` → `rawget` **nil**; after moving the
  arrow → **3**.
- **Q1 = HONOURED, both legs** (`add2d8a`, `663facf`). On a new game the hubs
  allocated `-1..5` natively. Two Stirling Generators at band 3 and band 4:
  band 4's work request ran `80000 → 50000 → 25000 → 0` and cleared. A **second,
  cheat-free symmetric pair** (equidistant, single hub, Polymers stocked) closed
  the **haul** leg — `demand_queues[4][Polymers]` inspected directly, both haul
  targets `1000 → 0` by drone delivery. **The band scheme survived the gate that
  could have killed it.**
- **Q2 = PERSISTED, answered by an accident** (`97a55fb`) — see below.

### 3. THE INCIDENT — the experiment module broke a live save (`d88dd11`)

v1 widened `const.TaskRequest.MaxBuildingPriority` at file scope and **asserted
in its own header that this was "inert"**. It was not. On an existing save every
`FindTask` threw, drones froze colony-wide while the UI reported "heavy load",
and the log took tens of millions of lines. **Nothing had been armed.**

Cause: `TaskRequestHub:Init()` allocates the queue tables at **construction** and
never again — so a restored hub carries `-1..3` while the widened const makes
vanilla's loops iterate `-1..5` and index nil. **That is the Q2 answer.**

**Three corrections to our own reference doc** fell out of it: the cited
`InitRequestQueues` **does not exist**; the claim that the game defines no
`const.TaskRequest` group is **false** (it exists and carries 3 — home not
determined, likely `Data.fpk`, which the parity extraction never covered); and
the hub population is **`DroneHubBase`, `RocketBase` and `RCRover`**.

v2 was rebuilt **safe by construction** — a queue top-up pre-wrapped onto all
seven entry points that index the queues — and ran clean.

### 4. The uninstall picture, and a NEW ENGINE FACT with pack-wide reach

- **Uninstall is safe, silent and LOSSY** (`6c05053`). A save with wide tables
  loading into narrow vanilla loops throws **nothing** — the mirror of the
  incident. But `demand keys: -1,0,1,2,3,4,5` persisted **with the module gone**,
  and 4 entries sat in a band vanilla never visits.
- **The heal path EXPIRES.** `DepositsSpawned` re-registers every hub, but fires
  only from a sector scan that places deposits, and sector status is a one-way
  ladder — **no re-scan on a fully-explored map**. Owner's framing, and it is
  right: clearing the map is an early act, removing a mod is a late one.
  **The hub UI toggle does NOT re-register** (measured).
- 🆕 **ENGINE FACT** (`988b0a8`): **a mod-authored closure stored on a persisted
  game object goes into the save, survives uninstall, and KEEPS RUNNING** —
  `rawget(obj, "GetPriorityForRequest")` returned `function: 000001E95D57A6B0`
  with the module uninstalled, and it re-filed queue entries using the vanished
  mod's logic, **with zero errors**. Pack audited: 5 of 6 sites cleared (UI
  windows, class tables); **`Fix_MeteorFrequency` is unresolved** and PT-20 now
  carries a mandatory step 5 naming it (`93bbf47`).
- 🆕 **The duplicate leak** (`93bbf47`, `DRONE_PRIORITY_SYSTEM.md` §10): a
  reconnect healed the building but took band 4 from **4 → 6**, because
  `DroneControl:RemoveBuilding` is bounded by a **file-local** pinned at 3.
  **This happens with the mod installed and working** — it is a defect of the
  band design, not of uninstall.

### 5. Owner decisions taken this session

- **A save-safety wall RELOCATES the overhaul, it does not kill it** (`1e19056`).
- **THE CLEANUP MOD** (`cae4eec`) — supersedes forced-standalone. Mods get **no
  save hook** (`PersistSave` blacklisted) and cannot run after their own removal;
  a second mod is the only thing that can occupy that window. Framed by the owner
  as a **beta response channel**, and as a capability rather than a backlog.
- **A possible PACK SPLIT is UNDECIDED and deliberately so** (`2ee9745`) — not
  owed, not scheduled, and may not gate anything.

### What this leaves for the next session

The band scheme **passed** its decisive gate but picked up **two constraints that
did not exist when it was drafted** (§9 uninstall, §10 duplicate leak), and the
`-1..3` fallback now has two independent arguments in its favour. Both are
written up neutrally; **no side has been picked. That is a design decision for a
fresh session.**

---

## PHASE 4 COMPLETE — C2 helpers + C4 deeper self-checks + C1 update report, CERTIFIED — 2026-07-31 (one-off PHASE4_REBUILD_PROMPT session, 11 unattended legs)

Executed `docs/PHASE4_REBUILD_PROMPT.md` (deleted on completion per its own
rule). Preflight design record: `docs/archive/PHASE4_PREFLIGHT.md`. Control
fingerprint: `docs/archive/fingerprint_before.txt`; end-state fingerprint:
`docs/archive/fingerprint_after.txt`.

### THE CERTIFICATION — every claim with its evidence

**What was measured, and what it read.**
- **Control** (before any edit): leg `Mars.exe-20260731-11.43.28` —
  all-six-toggles-ON + carry dial off base (read from the leg itself),
  `74/74 fixes active`, **67 PASS / 0 FAIL / 10 SKIP / 0 ERROR** at 77 probes.
- **Eight build stages, one commit + one leg each**, every leg diffed
  line-by-line against the control (verdicts, per-probe ids, all
  `[CommunityFixPack]` lines, reason strings):
  S1 helpers `67a744c` leg 11.47.23 · S2 log clones `eb06e31` leg 11.50.40 ·
  S3 SetGlobal `6b4a555` leg 11.53.21 (its commit message mis-cites the leg as
  "12.01" — written from memory; the fingerprint header carries the true name;
  the counts stated are correct) · S4 WhenActive `2e1bf88` leg 11.57.28 ·
  S5a DataPatch+Dust pair `6f90161` leg 12.00.22 · S5b donor+Independence
  `ad7f7e1` leg 12.03.14 · S6a-d Require waves `d28bf4c`/`b5f172c`/`7203a55`/
  `21a1a8d` legs 12.09.00/12.13.40/12.18.14/12.23.32 — **all EIGHT identical
  to the control**, modulo exactly four documented random-input probe messages
  (TouristApplicants roll counts, CrystalMysteryHang current mystery,
  FounderTraitNotification random trait, BombardmentSpread volley directions —
  verdicts always identical) and the log's own timing suffixes. · S7 C1
  surface `79a8e92` leg 12.28.05 — **68 / 0 / 10 / 0 at 78 probes**, the
  numbers predicted before the run; diff vs control is exactly the new
  `UpdateReport` PASS line + the summary counts.
- **Final fresh legs** (assembled result, from scratch):
  all-toggles-ON leg `Mars.exe-20260731-12.30.34` — `74/74`,
  **68 / 0 / 10 / 0** at 78 probes, identical to S7's fingerprint;
  baseline leg `Mars.exe-20260731-12.32.11` (`code` list emptied via the
  saved-copy discipline, restored and hash-verified `4dab1410…`, nothing
  committed while the edit was in the tree) — **1 / 62 / 15 / 0**, the 1 PASS
  is the FactionFundingCheck canary and the new `UpdateReport` probe **FAILs**
  as `fix pack not loaded (bug reproduces)`, proving it discriminates.
- **✅ The default-config leg RAN the same sitting** — the owner set the six
  toggles OFF + dials to base on request and leg `Mars.exe-20260731-12.44.39`
  read **`68/74`, 63 PASS / 0 FAIL / 15 SKIP / 0 ERROR** at 78 probes — the
  numbers predicted above before the run, landed exactly. Six
  `inactive (opt-in module …)` lines (the healthy default signature, six not
  five because DroneOverhaul reports status without a probe), zero
  error/disabled/FAILED lines, the D09 probe reporting the **carry dial AT
  BASE on entry** — the account is genuinely clean again. Fingerprint:
  `docs/archive/fingerprint_after_default.txt`. **Both shipping
  configurations are measured post-Phase-4; nothing is owed on the harness
  side.** (For the record: at certification-writing time this leg was owed —
  the account had been all-ON throughout the build, the account-state
  lesson's third earning in two days, and the opt-in bridge is one-way ON.)

**Invariants verified, and how.**
- Reason strings preserved byte-for-byte: legs cannot see a passing check's
  reason, so every wave carried a static extract-and-diff of string-return
  sites against HEAD (0 missing everywhere; the only flagged items were the
  checker's own em-dash decoding artifact — verified intact in the files —
  and concat-loop reasons the helper now generates identically).
- Declaring-class rule: every migrated method check re-verified; three
  suspicious sites resolved — ShelterReflex's Community.HasLifeSupport check
  is CORRECT (MicroGHabitat.lua:4 lists Community as a parent of the live
  class), MoraleComfortTooltip's dead Colonist.GetProperty limb became the
  real PropertyObject check, TrainWaitTime gained the two never-checked
  station-method checks (Station.RemoveColonist, Station.lua:770;
  TransportStatistics.AddSpentTime, TransportStatistics.lua:31).
- Handler gates: WhenActive carries BOTH FIX_POLICY §2 checks; no handler
  lost its gate; the by-design ungated handlers (MysteryEnd, the two watchdog
  state resets) and the probe-visible verdict functions were left untouched.
- `%` escaping: centralised in SMRFixPack.Log — the 12 clones and 5 inline
  variants are gone; output byte-identical.
- No `rawset(_G, …)` introduced anywhere; the two previously-unverified
  global installs gained the standard read-back.
- Packaging: metadata `code` (75) and items.lua `ModItemCode` (75) identical
  in content and order (script-verified after the final leg).
- Probe-authoring audit: 78 `Register(` across 8 files, every file with ≥ as
  many explicit `return "PASS"` sites (10/10, 20/21, 18/18, 12/12, 7/7, 3/3,
  2/3, 6/6).
- Mod-environment API: the helpers use only APIs the pack already used, plus
  three engine globals new to the pack — `GetPreGameMainMenu` (the TestKit
  autorun's proven poll target), `WaitMessage` (the engine's own mod-error
  dialog surface, Mod.lua:2229-2243) and `RealTime` — none on the
  ModEnvBlacklist (ENGINE_FACTS sandbox entry).

**What shipped.**
- **C2**: `SMRFixPack.Log` / `Require` / `SetGlobal` / `WhenActive` /
  `DataPatch` in 00_Core; 58 files migrated onto them (11 log clones, 12
  global installs, 16 handler gates, 4 DataPatch scaffolds, ~60 Require
  preflights). The F75/B3/A1 lessons and the PT-51 detail rule now live in
  the runner, not in per-file copies. A failing declaring-class check now
  gets a loud `__parents`-walk diagnosis naming the true declarer, so the F64
  failure mode can no longer masquerade as a game update.
- **C4**: the EXIST-only tier enumerated (42 modules, criterion in the
  preflight doc); bare-global indexing rawget-guarded through the helper
  everywhere; the IndependenceTerraforming missing-target latch added (it
  previously reported `active` forever if a future patch removed the tech —
  the B3 gap); the deepening items above.
- **C1**: `SMRFixPack.UpdateSuspects()` + a pregame-menu `WaitMessage` dialog
  shown ONLY when ≥1 fix deactivated over a game-code change (status
  `error`, the `update_suspect` mark, or the target-changed/install-failed
  detail conventions; opt-in / Mod-Options-off / verified-already-correct
  are never reported). This title never fires `Msg("PreGameMenuOpen")`
  (its init.lua replaces OpenPreGameMainMenu without it — the audit's cited
  engine precedent is dead code here), so the surface polls
  `GetPreGameMainMenu()` the way the TestKit autorun does. The dialog is the
  engine's own gamepad-native message surface, so it reaches console players
  — the pack's first failure surface that does (FIX_POLICY §7).
- **NOT shipped, by preflight decision** (`9f51f52`): the shared watchdog
  skeleton (F02 and F78 are different mechanisms — heartbeat-vs-signature —
  and consolidating them removed ~zero duplication at maximum risk); force-
  fitting the three divergent DataLoaded scaffolds (TechDescriptionBuilding,
  Opt_MultipleSuns, FirstAsteroid's latch); Require for the three
  partial-install applies (ShelterReflex, StorageRateModifiers,
  SequenceLatents — their per-target semantics are not gate-or-die). C3
  merges were never in scope (BARRED). The three drone modules
  (Opt_DroneOverhaul, Opt_DroneStatDials, Fix_ExtenderFlapChurn) are
  untouched per the carve-out and verified present in every fingerprint.

**What this certification does NOT claim.**
- **NOT "no behaviour changed."** Probes drive planted globals; a stand-in
  cannot reach a game file that localised a global at load time. What IS
  claimed: every fix still applies, still reports the same status, detail
  and reason string, and every probe returns the same verdict, in the
  all-toggles-ON and baseline configurations, across eleven legs.
- **Nothing here is playtested on a real colony or a real save.** Owed:
  the default-config leg (above) and normal play regression exposure.
- **C4's deeper checks are untestable against a future patch today, by
  construction.** They would catch a renamed/removed/reshaped target at the
  moment it happens; they would NOT catch a same-named function edited in
  place — and neither can C1's report, whose dialog text says so.
- **Residual risk, named plainly:** a consolidated code path whose behaviour
  differs only on a real colony state the harness cannot plant — the most
  exposed candidates are the WhenActive-gated LoadGame/PostLoadGame sweeps
  and the DataPatch-run preset passes (identical fingerprints prove their
  load-time behaviour, not their mid-colony behaviour). What would close it:
  one ordinary play session with the log checked afterwards (zero
  `[CommunityFixPack]` error lines, fixes still `applied`), plus the owed
  default-config leg. The after-every-patch extraction diff (WORKFLOW.md)
  remains the only true re-verification for the ~29 pinned replacement
  bodies.

**Deliberate deviations from strict preservation** (all fail-path-only,
invisible in every measured configuration, itemised for the record): the two
outlier installs' new read-back failure strings; AcknowledgedWarnings'
sequential (vs batch) install verification; the WhenActive veto re-read on 14
handlers that previously checked status only (newly effective only for a
mid-session console veto — FIX_POLICY §2's stated intent); DataPatch's heal
guarded against `"disabled"`/`"error"` where LastTransmission's was
unguarded (unreachable difference); Independence's new missing-target latch
reason; ClassicRockets' first-vs-last failing-name report when multiple
targets vanish at once.

---

## F83 BUILT — the First Asteroid prefabs are recovered on load — 2026-07-30 late (build session, unattended harness leg)

The headline task the previous session queued. Read the audit (§1-§3, §7), the
F83 entry and FIX_POLICY first, then verified **both** candidate shapes against
Src before writing anything, per the corrected brief.

**What Src confirmed (the trap is real).** `ShowPopupNotification` early-returns
on a `show_once` preset already shown (`PopupNotification.lua:249-251`) —
returning nothing — and `WaitPopupNotification` then takes neither `WaitMsg`
branch but still reaches `procall(callback, res)` (`:302-304`). So vanilla's
grant callback runs unconditionally, and a naive additive handler that also
grants would pay **2/2/2** on the healthy path. Both candidate shapes were
therefore judged on how they avoid that, not just on whether they heal.

**SHIPPED: shape (i), the load-time heal** —
`Code/Fix_FirstAsteroidPrefabs.lua`, Register id `FirstAsteroidPrefabs`
(FIX_POLICY §1.2 additive handler + §3's sanctioned one-shot sweep). On
`LoadGame`, if the FirstAsteroid popup notification is still in the persisted
`Notifications` table — the only state a dead real-time waiter can leave — the
sweep **removes** it, **grants** the three prefabs through the shipped
`ColonyAddPrefabs(..., 1, nil, MainCity)` calls in the shipped order,
**latches** a persistent flag, and **re-shows** the popup as pure display so the
player still gets the story text. The healthy path is never touched: no reload
means no `LoadGame`, so the trap is unreachable rather than merely guarded.
Removing the notification is load-bearing, not tidiness — its `PressFunc` is the
only thing that can re-queue the dead context, so exactly one grant path exists,
and that stays true even if a future patch moves the shipped waiter to a
game-time thread (where it would persist and still be listening).

**REJECTED: shape (ii), the `show_once` pre-mark.** The mechanism is real and
was confirmed in Src, but its correctness rests on OnMsg handler order **and**
on `CreateRealTimeThread` not running its body during the Msg dispatch — a C
export whose scheduling Src cannot settle, and losing that race shows the player
two corner notifications. It also moves the grant off the healthy path for every
player (prefabs at spawn instead of on answer) and cannot heal a save already
sitting stranded — which shape (i) does, including the owner's own PT-58
fixture. Reasoning recorded in the fix header, per the brief.

**Correction to the audit's own build note.** It advised matching the
notification by the preset's T loc-id via `text[1]`. That works only in a dev
build: `T()` returns **light userdata**, not a table, whenever the id is in the
translation table (`localization.lua:268`) — the retail case. The fix uses
`TGetID` (`:48-65`), which handles both forms, and reads the id from the **live**
preset rather than hardcoding it. (The related caveat the audit got right: the
preset id is genuinely absent from the instance — `ShowPopupNotification` nils
`instance.id` at `:286` because `AddNotification` asserts an id-less instance.)

**Savegame footprint** — one GameVar, `SMRFixPack_FirstAsteroidPrefabs`. Checked
end to end that a mod-declared GameVar is safe in the sandbox: `GameVar` writes
the real `_G` and `PersistableGlobals` (`lib.lua:1040-1055`) regardless of
caller, `ModEnvMeta.__newindex` explicitly permits writing a name registered
there (`Mod.lua:1559`), and `OnMsg.PersistLoad` only restores names still listed
in `PersistableGlobals` (`persist.lua:135-142`) — so a save made with the mod and
loaded **without** it simply ignores the stray value (§3).

**Probe + harness.** New TestKit wave file `56_Probes_Wave7.lua` (**probes
76 → 77**) driving the real sweep against planted globals over three legs:
stranded (must grant 1/1/1, remove once, re-show once, latch), already-healed
(must grant nothing — the no-double-grant assertion), and a decoy
non-FirstAsteroid popup (must grant nothing and must not latch). Unattended leg
`Mars.exe-20260730-23.29.22`: **`74/74` active, 67 PASS / 0 FAIL / 10 SKIP /
0 ERROR**, the predicted arithmetic exactly; zero `[CommunityFixPack]`
error/disabled/FAILED lines; no log line names our `Code/`. **Baseline leg**
`Mars.exe-20260730-23.46.39` (`code` list emptied, `default_options` kept):
**1 / 61 / 15 / 0**, with `FirstAsteroidPrefabs` **FAILing** as
`fix pack not loaded (bug reproduces)` — which is the whole point of running it,
since a probe that PASSes on baseline is measuring nothing (the wave-6
probe-authoring trap). metadata.lua restored from the saved copy and re-verified
against items.lua. **`items.lua` also needed its own `ModItemCode` entry** for
the new file, in the same order as the `code` list — without it an editor
round-trip would regenerate `code` without the fix (audit A3); `last_changes`
recounted 66 → 67.

**The account-state trap bit again, and then closed.** The 23.29 leg came up
`74/74`, i.e. **all six toggles were ON** — the previous prompt's "owner left
all six OFF" had gone stale during the PT-58 sitting, and the D09 probe reported
the carry dial off base too. That made 23.29 the all-toggles-ON configuration
and left the default-config leg owed, which the one-way opt-in bridge (ON only)
cannot supply. **The owner set everything back to base at the end of the night
and the leg ran immediately after** (`Mars.exe-20260731-01.37.22`): **`68/74`
active, 62 PASS / 0 FAIL / 15 SKIP / 0 ERROR** — predicted before the run and
landed exactly, with the D09 probe reporting the carry dial **AT BASE** on
entry. `FirstAsteroidPrefabs` PASSes in this configuration too, confirming the
fix is toggle-independent (it is default-on, not an opt module). Six
`inactive (opt-in module …)` lines = the expected healthy default signature.
**All three post-F83 legs are now on file and nothing is owed on the harness
side.** Standing lesson, unchanged and now twice-earned in one day: read the
account state from the leg's own `fix pack present: N/74` line, never from a
doc.

**Docs:** BUGS.md F83 → `fixed` in both places with a full build record;
**PT-59 filed** in the checklist (§3) with three triggers — reload leg 1/1/1,
healthy leg still 1/1/1 (the trap guard), and reload-twice still 1/1/1;
MOD_DESCRIPTION player line; STATUS counts to 75 files / 74 modules /
68 default-active / 77 probes.

---

## The popup/deferred-consequence audit — the storybit alarm OVERTURNED, F83's narrow decouple REINSTATED — 2026-07-30 (one-off session, unattended, game not launched)

Ran `docs/POPUP_AUDIT_PROMPT.md` (deleted on completion). Deliverable:
**`docs/POPUP_CONSEQUENCE_AUDIT.md`** — full enumeration of every path where a
player-visible consequence is applied after a wait, classified by save/load
survival. Headline: **the lead that stopped the F83 fix was wrong about the
engine.** A `CreateGameTimeThread` does NOT need `MakeThreadPersistable` —
**game-time threads persist by default with their full blocked stacks
(`WaitMsg`/`WaitWakeup`/`Sleep` are registered persist permanents "found in the
thread stack"); only real-time threads die on load.** Three source proofs
(XWindow clears the flag on a maybe-GT thread; `_fixup.lua` sets it only on the
RT twins and expects GT globals to arrive through the save;
Notifications.lua:214 flags only its RT variant) plus the everyday observed
fact that bare-GT unit command threads resume mid-command after every load.
Now an ENGINE_FACTS entry, alongside a second keystone: **every shipped popup
is async** — `ShowPopupNotification` opens with `assert(not bPersistable) --
we don't support these`, so the "persistable popup" branch the save handler
preserves is dead code and an OPEN popup's queue context never survives a load
(shielded in ordinary play because open popups are modal + game-pausing +
shortcut-eating; the shield is UI reachability, not the save system).

Consequences: **storybits, mysteries, anomaly sequences and challenges are
save-safe by design** (the storybit notification window even has a
forced-popup timeout backstop; no shipped scenario sequence is `real_time`;
the sequence system ships a watchdog that restarts abnormally-dead sequences).
**F06 is NOT an F83-family member** — one-shot `Msg` race, no save/load
involved, fix stands (entry note added). The real family is "consequence owned
by a REAL-TIME popup waiter": F83's two consequential sites + cosmetic
dead-View sites + a latent shielded class now filed as **F85** (breakthrough
choice popups ×3 grant `SetTechDiscovered` after an RT wait; the Assembly
"Colony Values" popup runs the ENTIRE politics init after one; all
open-immediately/modal, so tier **U** with a named settling observation — the
rebind-quicksave-to-F9 check, since `PopupPropagateShortcuts` lets F9/F11
through the modal layer and Quick Save is bindable). Also recorded: the one
`dont_pause` popup (distress call) admits sol-tick autosaves under it — the
popup itself is self-healing, but a second popup queued behind it at that tick
would be dropped with its GT waiter stranded (R3-edge, documented, no fix).

**F83: hold lifted, option 1 (narrow `OnMsg.SpawnedAsteroid` decouple)
REINSTATED as recommended — decision owed to the owner.** Entry corrections
from the audit: the eighth callback site (`ColonyViability.lua:260`) is GT +
open-immediately (safe, delisted); the `AnomalyAnalyzed` wait is commented out
in Src (dead site). **Needs-eyes list (4 items, audit §8):** (1) storybit
save/load in the notification window — the audit's one load-bearing inference,
~5 min console check; (2) Detailed Scan recoverability — grades F83's second
site; (3) the F85 rebind save vector; (4, optional) autosave under the
distress popup. No unattended game legs were run: the keystone fact has
observed corroboration, and every remaining question needs a keyboard.

**Rider repair:** the F84 filing commit (`21b92cb`) had spliced F84's last line
into the `### D06` heading, leaving D06's whole entry living under F84 —
heading restored in place, content untouched. Index 92 → **93 rows** (F85).

**Addendum, same evening — THE OWNER GAVE THE BUILD GO** (*"update the fable
next prompt to review and action on your findings"*), recorded on the F83
entry, STATUS and the next-prompt board. While writing the build brief the
session caught a **double-grant trap in option 1 as originally recorded**:
`WaitPopupNotification` procalls its callback even when `ShowPopupNotification`
early-returns on `show_once` (`PopupNotification.lua:249`, `:302-304`), and the
FirstAsteroid callback grants unconditionally — so "grant in our own additive
handler behind a flag" would pay 2/2/2 in the healthy no-reload path (the
entry's "the flag already stops a double grant" was wrong: the flag gates only
our handler). The brief now offers two corrected shapes — (i) a conservative
LoadGame sweep granting only when the stranded notification is detected
(matched by T loc-id, not T identity), or (ii) a show_once pre-mark that makes
vanilla's own always-run callback grant at spawn with the popup demoted to
display — build session verifies both against Src and picks one. PT-59 (the
kept fixture A/B) gains a second assertion: the no-reload leg must still read
1/1/1, not 2/2/2.

---

## Four PTs closed, two defects filed — and the F83 fix STOPPED by an owner question — 2026-07-30 (late evening, attended)

Continuation of the evening sitting below. **PT-58** (F83's consequence:
`1/1/1` vs `0/0/0`), **PT-44** (F23 → `tested`), **PT-25** (F38 → `tested`), on
top of **PT-56** (D09 → `tested`). Two new entries: **F83** (P2, proven) and
**F84** (P3, proven — the Universal Tunnel description is wrong twice).

**PT-25 is the one worth re-reading.** Its setup line said "SAVE-B / underground
access". The tester opened the underground build menu, found **no tunnel at all**,
and asked whether the premise was flawed — the same question that killed F24 and
F49(c). Half right: tunnels are a **surface** building (`UniversalTunnel` is the
only one in a player-facing category; `Tunnel` and `TrackTunnel` are `Hidden`),
so the underground reference was pure mis-specification — **fourth PT found
faulty by executing it**. But F38 itself held: the leaking sweep iterates
`TunnelBase`, and `UniversalTunnel` → `TrackTunnelBase` → `TunnelBase` with no
override. Corrected, run on the surface, passed all four steps including the
Rebuild over-reach guard. **SAVE-B retired** — its last consumer never needed it.
A free rider on that setup also disproved the tunnel's own description ("Rovers
cannot use this type of tunnel") → **F84**.

**Then the owner stopped a fix from shipping, and was right to.** F83's gate was
cleared and the narrow decouple was recommended and ready to build. He asked:
*are we 100% sure this is the only thing players can lose — what about anomaly
reports, mystery popups, story choices?* A first dive says the scope was drawn
too small:
- **`choiceN_func` is safe** — it runs in the UI action handler
  (`PopupNotification.lua:135`) before `host:Close(i)`, not in the waiting thread.
- **The return-value form of `WaitPopupNotification` is exposed exactly like the
  callback form.** The 8 callback sites are a subset of ~70 call sites; anything
  written after the wait dies with the thread.
- **Storybits are the likely real exposure**, and anomalies, planetary anomalies,
  mysteries and random events all route through them. `ActivateStoryBit`
  (`_StoryBits.lua:461`) spawns `run_thread = CreateGameTimeThread(RunWrapper)`;
  `Run()` posts a corner notification and waits; `OpenPopup()` then does reply →
  `StoryBitPayCost` → weighted outcome → `ProcessOutcomeEffects` → `Complete()`.
  Everything from the reply onward is after the waits. `g_StoryBitActive` is a
  persisted GameVar but `run_thread` has **no `MakeThreadPersistable`**,
  `OnMsg.LoadGame` only prunes dead presets, **no resume exists anywhere**, and
  `Unregister()` already ran so a stranded storybit cannot re-trigger.
  ActivationEffects run before the waits and are safe.
- **F06 was already an instance of this family** and nobody had connected it.

**The F83 narrow-decouple recommendation is RETRACTED and the fix is on hold.**
Fixing the asteroid grant alone would have papered over what looks like a general
defect — *player-facing consequences applied after a wait in a non-persisted
thread* — with the asteroid as its one proven symptom. A one-off audit prompt was
written (`docs/POPUP_AUDIT_PROMPT.md`): its own session, free to run unattended
A/B legs and add TestKit probes, explicitly barred from building any fix, and
required to separate observed from inferred. `FABLE_NEXT_PROMPT.md` now opens by
checking whether that file still exists.

**Lesson worth keeping:** the storybit exposure was reachable by grep the whole
time. It went unnoticed because F83 was scoped to the mechanism that produced the
*symptom* (a callback) rather than to the *shape* of the defect (consequences
after a wait). Scope a defect by its shape, not by the call form that surfaced it.

---

## PT-56 PASS IN FULL → D09 `tested`, D10 un-gated; and F83 filed from a surprise mid-setup — 2026-07-30 (evening, attended)

Live sitting with the tester at the keyboard, after the two unattended legs
below.

**PT-56 — PASS on all four steps**, on a one-speed-tech save (Low-G Drive only,
no Artificial Muscles), toggles off and dials at base going in. Baseline
`speed=1728 carry=1` · 2x/+1 → `speed=3168 carry=2` · back to base →
`1728/1` · **stale-save reconcile → `1728/1`**. The 3168 is the number worth
remembering: **+1440 exactly**, 100% of the 1440 BASE added additively beside
the tech — *not* a doubling of the live 1728. Log swept clean per PT-22 (zero
`[CommunityFixPack]` error lines; the only `Error` lines all session are the two
pre-existing `ResManager` `LawOfficeDoor` entries; four `MeteorFrequency
… restarting` lines are F02's watchdog across the sitting's four loads). D09 →
`tested`, section archived, **D10 workshops build un-gated**.

**Method lesson, paid for in this very test.** Step 4 was scored wrong first
time: it read `3168/2` and looked like a FAIL. The dials had simply not been set
back to base before the load, so the reading was correct behaviour. What caught
it was reading the **dial positions** alongside the values
(`Mods["SMR_CommunityFixPack"].options.DroneSpeedDial`) instead of the values
alone. Generalised onto the archived PT and the D09 entry: **for any dial test,
confirming the base state going INTO the load is its own step** — without it,
step 4 cannot distinguish a pass from a fail. Note this is the *third* time this
project has been bitten by account-persistent dial state in one day (the FAILed
probe, the 73/73-vs-67/73 leg, and now this).

**F83 filed — found by the tester mid-setup, and it grew.** A
`FirstFounderEnthusiast` popup arrived as a corner notification and its **View**
button did nothing. Chased live: the popup is a *scan* announcement of a founder
who already HAS the trait, so unrelated to F23/PT-44; the pack touches none of
this machinery; and `ViewAndSelectObject` called directly on the founder
**worked**, isolating the failure to callback delivery. A console repro of the
identical popup worked live, then the same repro left minimized across a
quicksave and load had its View die — tester verbatim: *"Correct view died after
a load."*

Mechanism: these popups always start minimized (`ShowPopupNotification` gates the
open-now branch on `start_minimized == false` and nothing ever sets it, so `nil`
takes the else branch); the waiter is a **real-time thread** blocking on
`WaitMsg(async_signal)`; neither the thread nor the async context survives a load
(`OnMsg.PersistSave` keeps only `sync_popup_id` entries) — **but the notification
does**. So after a reload it still opens, any choice signals nothing, and the
callback never runs.

**Eight call sites pass a callback; two are consequential.** `FirstAsteroid`
grants three Micro-G Auto Extractor prefabs its own popup text promises, is
`show_once`, and fires only at `asteroid_count == 1` — permanent silent loss.
`ReconCenterDiscoveryAsteroid` fires on *every* asteroid and its choice 2 is the
paid Detailed Scan, silently refused after a reload. The other six are dead View
buttons. Intent tell is self-contradiction (popup text vs delivery path);
reachability R1, reached organically before it was reproduced. **Honest caveat
recorded:** the mechanism is proven on the founder popup, the FirstAsteroid
consequence is *inferred* from identical code shape and is NOT observed —
**PT-58** added as the settling observation and gates any fix, per the F49(c)
rule. Nothing built; fix design is a user decision (recommended: decouple the
asteroid grant via an additive `OnMsg.SpawnedAsteroid`; a general popup-waiter
repair is not recommended). Family: same trap as F06.

The tester's current save had already met one asteroid, so it cannot serve as
PT-58's fixture — a fresh one is owed.

---

## The owed A/B ran and is CLEAR — and the D09 probe defect is repaired, not just recorded — 2026-07-30 (evening, unattended)

Session opened as playtest standby; the tester stepped away and released the
session for unattended work, so it took the two ⚠️ items at the top of the board
instead of waiting.

**The problem with the first item as written.** The board said: set both Mod
Options dials to base by hand, *then* run the owed A/B leg. That ordering exists
only because the D09 probe was broken — it read its baseline from the live
`g_Consts` value and asserted `base_carry + 1`, which is arithmetic against an
already-modified number whenever the account dial is off base. With nobody at the
keyboard the hand-flip was unavailable, and the leg would have FAILed again for
the same non-reason. **So the probe was repaired first and the precondition
disappeared.**

**TestKit repair** (`60_Probes_Opt.lua`, commits `ac30f54` + `e1d9bf1`). The probe
now reads the entry value, forces both dials to base through the real Apply path
(`rawset` on `Mods[pack].options` + `Msg("ApplyModOptions")`), takes its baseline
from *that* state, asserts that forcing base leaves no module modifier behind,
and restores the leg's entry values. Its tail cleanup check now compares the
restored const against the **entry** reading rather than against base, so it is
exact for any account dial state instead of speaking only when the account
happened to sit at base. STATUS had already written the remedy — *"it should
force base before measuring"* — this session just did it.

**Leg result (log `Mars.exe-20260730-19.20.24`, unattended via `-smrautorun`,
~70 s):** `fix pack present: 73/73 fixes active`, **76 probes, 66 PASS / 0 FAIL /
10 SKIP / 0 ERROR**.
- The counts land exactly where the F28 removal predicted (73 registered, 76
  probes), which is what the leg owed.
- **The dial probe went green with the account carry dial still at +1** — the
  exact state that FAILed it on the 17.25 leg — reporting `carry +1 over
  probe-forced base 1`. The repair is verified against the failing condition,
  not merely against a clean one.
- Zero `[CommunityFixPack]` error / inactive / disabled / FAILED lines; no log
  line names our `Code/`; noise profile identical to 17.25 (same 2 pre-existing
  `ResManager` `LawOfficeDoor` animation errors, same shutdown-artifact
  `[mod] Error in mod … Test Kit`, `objects_to_mark` 48→59 with the random map).
  The `LawOfficeDoor` pair was not previously on the documented noise list; it is
  now, having been shown present in both legs.
- The account still had all six toggles ON, hence `73/73` and not a
  default-config `67/73`. **A default-config leg has still not been run since
  the removals** — it needs the six turned off by hand, so it stays a keyboard
  item.

**Harness health check while the leg ran:** the falls-off-the-end-returns-SKIP
trap was re-audited across every probe file (`Register(` vs `return "PASS"`
counts). Clean — 10/10, 20/21, 18/18, 12/12, 7/7, 3/3, 6/6. Nothing is sitting
in that trap.

**What did NOT change.** D09 is still **not** `tested` — only the playtest flips
statuses, and PT-56's stale-save reconcile step is beyond any probe. **PT-56 also
still needs both dials set to base by hand**, because its step-1 baseline reads
come from the live game; the repair removed that precondition from *A/B legs*
only. The board's ⚠️ A/B item is now done and can come off; the ⚠️ dials-to-base
item survives as part of PT-56 itself.

### Second leg the same evening — the default configuration, and a self-inflicted blind spot found

The owner then set **all six toggles OFF and both dials to base** by hand — the
one thing the opt-in bridge cannot do, since it ORs with the saved toggles and
can only force a module ON. Leg run unattended immediately after, with the
expected result **stated before the run** so it could fail: log
`Mars.exe-20260730-19.32.16`, **`67/73` active, 76 probes, `61 PASS / 0 FAIL /
15 SKIP / 0 ERROR`.** It landed exactly. The five opt-module probes flip
PASS→SKIP as `inactive (opt-in)` — five, not six, because D06 has no probe of its
own — turning 66/10 into 61/15 with FAIL and ERROR still zero. `DroneStatDials`
and `OptionsMenu` both stay PASS, so the dials and the Mod Options wiring are
confirmed toggle-independent **in the shipping default configuration**, not just
with everything switched on. The six `[CommunityFixPack] … inactive (opt-in
module …)` log lines are the healthy default-config signature, not errors — six
here, not five, because DroneOverhaul reports its status despite having no probe.
Same noise profile a third time.

**The blind spot the leg exposed, in this session's own work.** Making the dial
probe immune to account dial state also made it *silent* about it — and that
silence costs something real, because the old broken probe's FAIL text
(`DroneResourceCarryAmount 3 → 2 (want 4)`) is precisely how the project learned
a playtest had left the carry dial at +1. A green leg now proves nothing either
way about the account, while **PT-56's own baseline reads still depend on it**.
Fixed the same evening (`e605ba6`): the probe compares its entry reading against
the base it forced and reports `account carry dial AT BASE on entry` or `OFF BASE
on entry (const N vs base M)`. Immunity for the verdict, visibility for the
human. General shape worth remembering: **when you make a check robust to some
ambient state, ask what the old fragility was accidentally reporting.**

Docs: STATUS A/B table + account-state block rewritten (17.25 compressed to
history), BUGS D09 entry item 2 flipped to repaired-and-verified with the new leg
recorded, PT-56's warning block corrected so it no longer tells the tester a
repaired defect is open, TestKit README's "Known probe defects" entry updated.

---

## HARD RULE: vanilla only, never other mods (FIX_POLICY §4a) — F28 retired under it — 2026-07-30 (late)

**The owner set a standing rule**, prompted by asking a simple question about
F28: *why did we build a "replace tech" fix when we have never replaced a tech?*

> *"This mod does not fix bugs caused from other mods. No agent should assume it
> does at any point going forward. The only way that should be able to be
> changed is if an agent specifically asks me to override as a one-off for
> something I specifically ask for."*

Recorded verbatim as **FIX_POLICY §4a**, with the corollary that actually occurs
in this tracker written out explicitly rather than left to interpretation: a
**vanilla bug reachable only from mod code is not a player fix and does not
ship**. The override procedure is the only one permitted — explicit ask, explicit
yes, one case, never inferred and never carried forward. Existing shipped fixes
are explicitly declared NOT precedent.

**Whole-tracker scan first, because setting the rule is only half of "don't slip
more in".** Exactly two shipped fixes rested on a mod-facing rationale: **F28**
and **F29**. (F34(b) is labelled mod-facing but was never actioned; F42 is
already `wontfix`.) Bounded blast radius.

**F28 retired under the rule.** The answer to the owner's question is that it was
**never an oversight** — the entry's second line said *"No vanilla caller; hits
mods/storybits/console"* the day it was filed, and it shipped anyway on a
"modder benefit" rationale. So F24 was an *error* (nobody knew it was
unreachable); **F28 was a decision, and the rule reversed it.** Independently
re-verified before deleting: the whole-tree grep over `Lua/`, `Data/`,
`CommonLua/` and `DLC/` returns exactly one `ReplaceTech` hit — the definition
at `Research.lua:684`.

Removed: `Code/Fix_ReplaceTechCount.lua`, its `metadata.lua` and `items.lua`
entries, the README row, and the `ReplaceTechCount` probe. **The probe had to go
too** — it drives the real method and asserts the *fixed* counter, so with the
fix gone it would FAIL in every leg. Recorded on the entry that it could later
be rebuilt as a vanilla canary on the **F10 precedent**, which is what
`FactionFundingCheck` became after F10's deletion; not done, because that is new
assertion code nobody asked for.

**Counts: 74 → 73 registered, 68 → 67 default-active, probes 77 → 76.** A fresh
A/B is **OWED** — unlike F24, this one moves the probe numbers. Also caught while
recounting: `metadata.lua`'s player-facing `last_changes` still advertised "68
bug fixes"; it derives as Fix_ files + the sanitizer and is now **66**, with the
derivation written into a comment so it stops drifting silently.

**F29 flagged — then UN-flagged the same evening, and the mistake is mine.** I
flagged it on the strength of its own words ("mod-facing bundle", "ship for
modder benefit", "No shipped user"). The owner asked the obvious question —
*what does F29 actually do?* — and reading the audit's enumeration to answer it
showed **the entry's self-description is false**: item 1 has **four shipped
callers**, all in Mystery 2 "Dredgers", all executing live in every playthrough;
item 3 runs for every digger that mystery spawns. Both are benign only because
the shipped *data* is benign (default sampling params; already-ordered timings).
That is **R3 latent-by-data**, not mod-only — same shape as F27/F31/F43. **KEPT.**

I made the exact error the audit made on F49(c): **trusted an entry's own
framing instead of the enumeration sitting right there.** There it was about
intent; here it was about provenance. §4a now carries the warning explicitly.

**The owner's clarification is what settled it**, and it is now the rule's
operative test: *"I don't want to fix things for other possible mods. But if
it's game code that could cause real problems for users now or in the future
even if they can't expressly see the issue, that is a real fix."* Ask **who
benefits**, not how visible the harm is. Invisible, latent and
nobody-has-complained are all irrelevant. Operationally it lands exactly on the
**R4/R3 boundary**: R4 needs new *calling code* to go live (only a mod can
supply that — barred); R3 needs new *data*, which ships with patches, DLC and
story content (player territory — allowed). So the rule retired **F28 alone**.

F29's one genuine open question is unrelated to §4a: it is R3 implemented as two
**§1.5 method replacements**, the combination the *pending* §4 amendment would
put to the owner. Paired with F57(a) in that bucket. No action unless a stricter
line is wanted.

---

## F49(c) removed; post-removal A/B leg run unattended — 2026-07-30 (late)

Owner away; work done to standing instruction, with two decisions deliberately
left untouched (below).

**F49(c) closed `wontfix`, guard removed (`d03417b`).** Full reasoning on the
F49 entry. The short version: the tester established at the keyboard that
salvage mode targets objects not hexes, the cursor always names its target
(bare red `Salvage` = no action permitted), the
`Salvage Train Station`→`Salvage Track` handoff is seamless to the millimetre,
and **no exposed control separates a station from its own connector track**.
The propagation item (c) called a defect is what makes that boundary
continuous — it is designed. Had the guard engaged it would have carved a dead
band into it. Removed the pre-guard, its apply-time self-check and the title
clause; (a) and (d) untouched; file parses; README never described (c).

**Post-removal A/B leg — code gate CLEAR.** Unattended, log
`Mars.exe-20260730-17.25.32`, 65 s. **74/74 fixes active** (exactly one fewer
than the pre-removal 75/75 = the F24 deletion), **zero `[CommunityFixPack]`
error/inactive/disabled lines**, probe total still 77. Result
**66 / 1 / 10 / 0**. The single FAIL is a **probe defect, not a pack
regression**: the D09 dial probe captures its baseline from the live value
(`60_Probes_Opt.lua:411`) and asserts `base_carry + 1` at `:431`, which only
holds if the account dial is already at base — today's playtest left it
off-base (same account change that produced 74/74 instead of 68/74). Neither
removal touches drones, modifiers or Mod Options, and the module logged
`applied`. **New TestKit defect recorded: the D09 probe is state-dependent and
can FAIL or false-PASS on account dial state; it must force base before
measuring.** Same family as the 2026-07-29 falls-off-the-end-returns-SKIP trap.
Confirmation is a 2-minute re-run with the dials at base — the natural moment
to run PT-56 as well. TestKit autorun armed and **disarmed** cleanly either
side.

**Challenge issued and answered the same evening.** The reachability audit
(`3398031`) had rated F49(c) "live R2" — the owner asked for it to be
challenged with our evidence rather than blind, on the grounds that catching
exactly this was the audit's premise. Prompt at `0d9435c`, answered `48d9edb`.
Its findings are worth more than the one corrected verdict: the method is
**decisive on reachability and near-mute on intent**, so a wrong
author-hypothesis sails through with full confidence; exactly **two** verdicts
in the whole table were unenumerated, both F49 items the lead kept for itself;
and the audit's own evidence base **went stale mid-run** — `c3c4383` and
`ba1e88b` landed while its sweeps ran and it never re-read `git log` before
publishing, so the falsifying evidence for (c) *and* the play-proof for (d)
were already in the repo. New tier **`I` (intended behaviour)** added, and (d)
late-enumerated and confirmed R2.

**Held for the owner, deliberately not actioned:** the **F28** delete decision
(the audit's sole DELETE candidate) and the **FIX_POLICY §4 amendment** (now
revised by the challenge to require a positive intent statement plus tier `I`).
Both were framed by the audit as the owner's call, and the project reserves fix
deletions and policy edits to them.

---

## PT-46 tail — F49(d) PASS; F49(a) parked on a reachability question — 2026-07-30

**(d) cap-follows-length: PASS.** Live 305-sol colony, read-only counter
printing actual vs shipped-formula expected per track. Track 3 went
`els=43 cap=2` → `els=13 cap=1` across a partial salvage — the surviving-track
case the fix exists for. All lines `OK` across four runs, including after a
reload and a second salvage on a freshly loaded track. The mid-track salvage
also split off a new track at `els=25 cap=1`, correct on its own, which
independently confirms the 2026-07-25 QA correction. Recorded honestly on the
entry: the `PostLoadGame` sweep's REPAIR of a stale cap is **not** proven and
cannot be from a healthy save — queued as a TestKit probe.

**(a) instant-track palette: parked, not run.** The attempt cost something and
is on record. Reaching `place_track` needed a `SetMode` injection with no
player-facing equivalent; it misbehaved and left an orphan `TrackBase` with
invisible elements blocking grid hexes on the live colony (cleared by reload).
That broke the project's own no-live-UI-internals rule (F76 lesson) — the
assistant handed it over, the rule existed, it was violated anyway.

**The user's response to that is the important output of this leg.** Their
question — *"are we forcing this to test something vanilla, or are we in a loop
of testing artifacts that aren't real bugs if you play the game correctly?"* —
reframed the whole thing. The debris was an artifact of an unreachable entry
path and is filed as nothing. And it exposed that F49(a) itself has never been
asked the F24 question: `place_track` serves "map setup, cheats, the
instant-build rule", and **none of the three is verified player-reachable**.

That became `docs/REACHABILITY_AUDIT_PROMPT.md` (commit `5b0ad35`) — a
game-free, read-only audit asking of every fix whether a player can reach the
defect at all, with F24 as the worked template, an R1-R4/U tier vocabulary,
decision rules keyed to patch cost, an explicit anti-over-pruning stance, and a
drafted FIX_POLICY §4 amendment (the policy demands a proven defect but has
never demanded proven reachability — which is exactly how F24 shipped).

**Gap noticed while writing this up:** F49**(c)** has no play coverage either —
PT-46's tail only ever covered (d) and (a). Cheap to close in salvage mode
(click a station-owned connector hex, confirm the station is not flagged).
F49 therefore stays `fixed*` on two items, not one.

---

## F24 CLOSED `wontfix` — fix DELETED, counts 75→74 / 69→68 — 2026-07-30

Came out of the user sitting down to run PT-44's F24 half and finding it
**impossible**: no dome will place over existing buildings ("Objects underneath
are blocking construction"), tried across dome types, sizes and angles. The
user's own read — "if this was ever a bug it needed a mod that breaks
boundaries or does upgrades" — turned out to be exactly right, and the question
they asked next is the one that settled it: *what are we really fixing here?*

**Reachability proof (now on the F24 entry, do not re-derive).** `MoveInside`
has two call sites in all of `Src`. `MartianAssembly.lua:60` is live in play but
cannot reach the buggy line — `SpireBase.__parents = { "Building" }` and the
template declares no water or air, so `LifeSupportGridObject:MoveInside` is not
in that chain. That leaves `Dome:OnLoad`'s repair sweep, which needs a
pipe-connected life-support building inside a dome's interior hexes with
`parent_dome ~= self` and live connections. Vanilla cannot produce that: domes
refuse to place over buildings, **no dome template carries any upgrade** (all
`*Dome*.lua` checked, zero `upgrade*_id`), and nothing mutates an interior shape
at runtime. The defect is real — it was never a player report, it was found by
diffing the water grid against its electricity twin — but it is unreachable.

**User decision: delete rather than carry as latent.** The F28/F43 precedent
(real-but-latent, keep) was offered and declined, on the reasonable grounds that
those are cheap patches while this one was a **34-line full-function replacement**
of `LifeSupportGridObject:MoveInside` that would rot on any future patch to it.
Removed: `Code/Fix_DomePipeMoveInside.lua`, its `metadata.lua` code entry, its
`items.lua` ModItemCode entry, and the README fix-table row.

**Verification of the removal:** both edited Lua files parse clean (luaparser);
`items.lua`'s CodeFileName list now diffs **identical** to `metadata.lua`'s code
list; 75 files = 66 `Fix_` + 7 `Opt_` + `00_Core` + `90_SaveSanitizer` → **74
registered / 68 default-active**. No TestKit probe existed for F24, so the suite
stays at 77 probes.

**OWED:** an A/B pair — every recorded leg predates this and was measured at
75/69; the default leg should now read **68/74**. Flagged in STATUS, the
continuation prompt, PLAYTEST_CHECKLIST (PT-22 item 4, PT-21 setup) and
PLAYTEST_HELP's ListFixes row. Rollback is one `git revert`.

**PT-44 consequence:** the F24 half is removed; PT-44 now covers F23 only. This
is the **third** PT procedure found unrunnable by executing it (PT-29, PT-11,
now PT-44's F24 half) — the standing rule earns another data point.

---

## PT-48 CLOSED IN FULL — D02 AcknowledgedWarnings → `tested` — 2026-07-30

Live playtest-standby sitting, parallel to the PT-55 closure session (that
agent held `PLAYTEST_CHECKLIST.md` / `PLAYTEST_ARCHIVE.md` dirty for most of
this leg; results were written only after `aac6798` landed and the tree went
clean — no collision).

**Why the item was open at all, since the user asked.** The D02 work everyone
remembers is **PT-38**, which is a *different test with a different job*: it was
the GATE that decided whether to build the module, and it corrected the premise
from "re-nags every 2 real minutes" to **120,000 GAME-ms = 4 game hours**.
Archived and done 2026-07-27. The module was BUILT the same day. **PT-48 — the
play verification — had never been run once**; its only coverage was the TestKit
stand-in probe, and probe-verified ≠ `tested`. Nothing had been lost.

**Method: counters, not eyes.** Steps 1-2 are "nothing should happen" tests, the
exact shape that has twice produced unrunnable procedures here (PT-29, PT-11).
So the sitting opened with a **positive control**: fixture built, module OFF,
dismissal armed `suppress_until = now + 120,000` to the millisecond, and the
notification RETURNED after the window — proving the no-power fixture generates
re-add attempts and that a later "it stayed quiet" could not be vacuous. Two
paste-safe console counters (per-building state + whole-ack-set enumeration) are
recorded verbatim in the archived section and are reusable for any future
notification work.

**Result: all five steps PASS.** Acked buildings held for 505,850 game-ms
(≈16.9 game hours = **4.2 vanilla windows**) with `shouldshow=true` proving they
actively qualified and were still excluded, and `suppress_until=nil` proving the
silence was the per-object filter rather than the shipped window. A new
building, placed while PAUSED, warned inside the interval vanilla would have
been silent. Repowering the original three cleared all three stamps
(`total_acked` 3 → 1) and re-breaking re-warned all three. The stamp survived
save/reload — flagged pre-run as the likeliest failure.

**Two findings worth carrying forward:**
1. **D02's blast radius is provably tiny.** Exactly **two** notification presets
   in the entire game are `Suppressable` — `InsufficientResources` and
   `NotWorkingBuildings` (`Data/NotificationPreset.lua:546/:646`). Since the
   module's guard is a literal `id == ID`, `InsufficientResources` is the only
   id in the game where it could differ from vanilla. It was forced (via
   `const.MinDaysFoodSupplyBeforeNotification`, restored after) and shown
   arming, expiring and re-nagging untouched. That reduces step 5 from a vague
   "check other warnings" to a single decisive observation.
2. **Vanilla curiosity, unexplained, filed on the D02 entry:**
   `InsufficientResources`' suppression resolved on **RealTime** while PT-38
   measured `NotWorkingBuildings` on **GameTime**, even though both presets
   leave `GameTime` at its default `true`
   (`NotificationPreset.lua:65-66/:126-128`). D02 never calls `GetTime()`, so
   the PASS is unaffected — but if the notification INSTANCE rather than the
   preset supplies `GameTime`, PT-38's recorded 4-game-hour fact may need
   scoping. Game-free item.

Also confirmed by reading before the sitting started: **D02 never had the
audit-1.3 first-enable defect.** Its three wrappers replace plain notification
GLOBALS rather than class methods, so runtime flattening never applies, and
`OnMsg.ApplyModOptions` re-runs `apply()` (`00_Core.lua:129`) on a first
mid-session enable. Verified in play — the module was enabled mid-session with
no relaunch and worked immediately.

**Docs:** D02 flipped in both BUGS.md places + full result block on the entry;
PT-48 section moved to PLAYTEST_ARCHIVE.md (37 sections) with the counters and
conditions; STATUS next-gates and optional-module list updated. MOD_DESCRIPTION
needed no change (it does not segregate tested/untested for opt-in modules).

---

## PT-55 CLOSED — step 3 run live, D01 limitation accepted — 2026-07-30

The bottleneck item is done, on the user's explicit "nothing else until it is
closed" directive. Two blockers resolved in order: (1) the D01 decision — the
parked-rocket first-enable limitation ACCEPTED as documented (user call,
`4f5f61e`), no `on_activate` refresh built, enhancement path recorded on the
D01 entry; (2) step 3 executed in the live sitting (log
`Mars.exe-20260730-12.03.01`): all six opt-ins `applied` → `deactivated` ×6 →
`re-activated` ×6 → `deactivated` ×6, with on-screen status reads AND full
`ListFixes` blocks agreeing at every step; log swept clean per PT-22 (zero
LUA ERRORs; Braze DNS + LawOfficeDoor ResManager noise only). Bonus capture:
`MultipleSuns: reconnected 1 solar panel(s)` on the mid-sitting reload — the
D04 self-heal visible in the log. PT-55 section archived (36 archived
sections now); audit A2 caveat retired in AUDIT_FINDINGS; STATUS + the
continuation prompt rewritten.

Tooling fact worth keeping: while Mars.exe holds the session log open, the
logs DIRECTORY reports a stale 0-byte size for it — NTFS directory metadata
only updates on handle close. `FlushLogFile()` works; open or copy the file
to read the flushed content instead of trusting the listing.

---

## PLAYTEST_CHECKLIST split: tests-only checklist + PLAYTEST_HELP.md — 2026-07-30

User call ("to the human eye its hard to find and organize play tests and then
find commands. its bloated"): the checklist now carries ONLY tests + the
reporting protocol; everything reference — ground rules, external-validity
rule, cheat discipline, console facts, the verified command table, Test Kit
helpers + stress harness, save-fixture recipes, the unverified-commands table —
moved verbatim to the new `docs/PLAYTEST_HELP.md`. Split executed by line-range
slice (python, utf-8, no round-trip); verified: all 46 headings survive, moved
content greps in exactly one of the two files. Cross-references updated:
checklist internal pointers, FABLE_NEXT read-list + jobs list, WORKFLOW.md
read-list, STATUS.md ground-rules pointer, TestKit README (own repo commit).
PLAYTEST_ARCHIVE and history docs untouched.

---

## Curiosity sitting → D10 speced: tunnel water, workshop research, unemployment truth — 2026-07-30

Assisted research session (game-free), three questions from the user, all
answered from Src with community cross-checks; ended in a new speced D-item.

- **"Can water reach an isolated mountain base?" — YES, through the Universal
  Tunnel, and the UI hides it.** `UniversalTunnel` → `TrackTunnelBase` →
  `TunnelBase` = `ElectricityGridObject` + `LifeSupportGridObject`;
  `GameInit` merges BOTH grids (Tunnel.lua:6,87-88; re-merged on track power
  reconnect, TrackTunnel.lua:12-17). Tracks/stations bridge electricity ONLY
  (Track.lua:112-123) — which is why players see power cross but never water.
  Recipe: pipes to both portals. The buildable Universal Tunnel's description
  says "tracks and power grids" — the hidden legacy Tunnel template still
  carries the correct "power and life support grids" text (description drift,
  F65 family). **Unfiled candidate** (user call): one-line description patch.
- **"What are 'workshops'?" — the three vocation buildings** (Art/VR/
  Biorobotics, build category "Workshops"), NOT factories: produce nothing,
  consume Polymers/Electronics/MachineParts per fraction-of-capacity, pay
  +10 Morale / +5 Comfort×performance. Community's three-camp unemployment
  argument adjudicated from code: no colonist-level penalty (icon-only
  status effect) — but **in Relaunched every faction def punishes ≥10% dome
  unemployment** (Workers' Party -900..-3000, WorkersParty.lua:103-121), so
  the inherited "ignore it, no penalty" advice is now wrong at colony level.
- **Design verdict on workshops** (user asked for honest): sound core loop,
  undersized (6-10 workers/shift), and illegible — the faction cost appears
  nowhere in workshop/unemployment UI text.
- **D10 SPECED + user-approved:** one Opt_ module — T1 text repairs
  (descriptions + Unemployed rollover state the faction cost) + T2 capacity
  dial (base/+50%/+100%, D09 label-modifier pattern, `max_workers` +
  `consumption_amount` PAIRED so per-worker cost stays vanilla —
  consumption is fraction-of-capacity × amount, ArtWorkshop.lua:35-39).
  **Build gated on PT-56 PASS** (same machinery, first live check first).
  Seniors-in-workshops deferred as its own decision (D07 employed-senior
  exemption interaction). Full spec: BUGS.md D10.
- **Shuttle-limits research (same sitting, follow-up curiosity):** three
  separate limits — cargo 3/shuttle (modifiable, +3 from HighPoweredJets =
  the game's only cargo buff), 10 shuttles/hub (+6 CompactHangars),
  passengers **1/trip structurally** (one vanilla task per colonist; the "1"
  is architecture, not a number). No breakthrough touches shuttles; fuel is
  the only shuttle law. Leftover cargo chains one extra hop or gets DUMPED
  as a ground pile (shipped comment: "noone wants this..dump it and go
  home"). Full reference on the new BUGS.md D11 entry.
- **D11 FILED AS CANDIDATE, NOT APPROVED (user's explicit framing):**
  same-pair passenger batching is feasible (task objects already carry the
  dome pair; hold fits 3-6 colonists; risks = boarding sync ×N, cancellation
  granularity, mod-removed-mid-flight landing). **The filing is for the
  record only — re-ask the user before any build. Multi-hop passenger
  routing REJECTED the same day.**

---

## D09 stat dials: decided → probed → range widened → BUILT → A/B clean, one evening — 2026-07-29 latest

**The whole D09 lifecycle ran in a single assisted evening.** During live play
the user asked where the planned speed/carry sliders were (answer: DECISION
recorded, build not started). Prep ran WHILE the user played (Mars.exe-running
rule respected: all drafting in scratchpad, zero repo writes); the user ran the
queued C-side clamp probe in-session (`SetMoveSpeed(10000)` → read back 10000,
movement clean at ultra — no C-side clamp, recorded on D09 + the DECISION
facts) and **widened the dial range 1.5x/2.0x → 2x/3x/5x on the strength of
it** (worst case 1440 × 5.6 = 8064 < 10000). On exit the build landed as
`9aae3de` (module + items/metadata + BUGS D09 + FIX_POLICY §5 dial addendum +
MOD_DESCRIPTION + PT-56 + STATUS/FABLE_NEXT), then the owed A/B pair ran
UNATTENDED (user pre-authorized):

- **Leg 1a FAIL — real catch #1:** the module's file-scope self-check read
  `Modifier.new` — the F64 pre-flattening trap (`new` is inherited, invisible
  on the classdef). Fixed `d8e309c` (presence-only at file scope, capability
  check in the reapply guard).
- **Leg 1b FAIL — real catch #2:** the new TestKit dial probe wrote its OWN
  env's `CurrentModOptions` — **per-mod-env** (each env aliases that mod's
  options object, Mod.lua:2128-2131/:679-683). New ENGINE_FACTS entry; probe
  now writes `Mods[pack].options` (TestKit `ed01ef7`).
- **Leg 1c: 67 PASS / 0 FAIL / 10 SKIP / 0 ERROR at 75/75** — dial probe
  PASSes both directions through the real Apply path. **Baseline:
  1/61/15/0** (D09 probe FAILs "fix pack not loaded" by design). Logs clean
  both legs; metadata baseline surgery restored from saved copy, tree clean.

**Account-state correction:** the legs read 75/75 — all six toggles were ON
again (re-enabled during the day's play). PT-55's all-OFF starting state must
be set by hand; the FABLE_NEXT/checklist notes claiming OFF were corrected.
D09 status: `built`, PT-56 owed (apply/stack reads, live removal, stale-save
reconcile — the clamp probe half is already done).

**Set completed 2026-07-30 (same assisted session):** the user flipped all six
toggles OFF and the default-config leg ran unattended — **62/0/15/0 at
69/75**, log clean, dial probe PASS (dials independent of the toggles; the
five opt-module probes back to `inactive (opt-in)` SKIPs). All three legs of
the post-D09 set now match expectations exactly. Side effect: the account is
in PT-55's required all-OFF starting state — PT-55 staged.

---

## PT-55 result + the D07 cohort-housing deadlock found in play — 2026-07-30

**PT-55 — the audit's A2 question is ANSWERED YES.** All three reworked hooks
install and run on a first mid-session enable, no relaunch. D03 clean ("no
issues at all"). D04 passes with an expected, self-healing timing limitation
(pre-existing panels can't be retro-bound because the wrap is on
`SolarPanelBase:GameInit`; a reload re-runs it and they snap to sun #2). D01's
hook is proven live — a rocket that LANDS after the flip fills immediately — but
**a rocket already parked does not begin refuelling and does not heal on
reload**, because `GetFuelResourceRequest` is only consulted when
`CargoTransporterNew:UpdateCargoResourceRequests` runs and nothing re-triggers
that for a parked rocket. PT-55 step 1's literal wording therefore fails for
D01. Open decision recorded on the D01 entry: an `on_activate` demand refresh.
The tester diagnosed the cause unaided ("my guess it's an on-land interaction")
and source confirmed it.

**D07 COHORT HOUSING — a self-reinforcing deadlock, found by deliberately
stressing homelessness.** Full chain, every link source-verified:

1. D07's cross-dome pass fills a nursery-only dome with Children.
2. They age up; the **Youth** trait's `apply_func` evicts them from the Nursery
   (`Data/TraitPreset.lua:760-764`) — so the tester's first hypothesis, that
   aged-up children clog the nursery, is WRONG; they are evicted correctly.
3. That dome has **no non-Child housing**, so they become homeless *there*.
4. `Dome:AddToLabel("Homeless", …)` sets
   `overpopulated = #Homeless >= g_Consts.OverpopulatedDome`
   (`Dome.lua:1026-1035`).
5. **D07's own `consider()` skips `community.overpopulated`**
   (`Opt_CohortHousing.lua:194`) — so the child dome is now permanently
   excluded as a destination.
6. New Children never migrate in. Observed live: nurseries at 5/26 and 3/26
   (68 free Child slots) with 28 homeless in the dome (**26 Youth, 2 Adult** —
   93% aged-out, the eviction signature), while a Child in a neighbouring dome
   commutes in to the school and goes home to a Smart Apartment.

`CanAcceptNewColonists()` is only `ui_working and accept_colonists`
(`Community.lua:61-63`) and read `true` live, so the quarantine is NOT involved
— `overpopulated` is the whole gate. **The module poisons its own destination**,
and the more children it delivers the more firmly it locks itself out.

**Separately established and NOT filed as a defect:** the homeless youths
themselves. `non-cohort free slots colony-wide: 0`, so total homelessness is set
by (population − housing capacity); D07 changes *which* colonist lacks a chair,
not how many. It arguably improves utilisation by freeing ordinary slots. A
caveat, not a bug — deliberately not given an F-number.

**RESOLVED SAME DAY → D12 SPECED AND APPROVED.** Four options were put to the
user (drop the `overpopulated` clause; refuse nursery-only domes; both;
document only) and **all four were rejected** in favour of a better direction
the user proposed: a per-dome **"no homeless residents"** policy that pushes
homeless colonists out to a dome that accepts them. It fixes the *cause* rather
than the symptom, is player-steerable rather than a hidden heuristic,
generalises to Retirement domes, and heals an already-poisoned dome — set the
flag, the homeless drain, `overpopulated` clears, D07 resumes unaided with no
change to D07 at all.

**Root cause reframed while speccing it.** The shipped eval *already* lets a
homeless colonist move to a dome with no free housing (`Colonist.lua:2676`,
comment: "if homeless, try changing community even if doesn't have living space
available"). What stops them is the gate above: candidates must score
**strictly better** unless home or work improves (`:2675`, `:2680-2681`). With
zero free slots colony-wide and unemployment saturated, every candidate **ties**
— and ties never move anyone. **This is the same tie rule D07's own header
cites as the reason cohort members never consolidate.** D12 is that same
tie-break applied to a different population.

**A design trap the user caught before it was written.** The first packaging
idea was to extend D03 ResidencyControl. The user asked whether that meant the
same UI control, and it would have been fatal: D03's row wraps
`Community:CanAcceptNewColonists`, which D07's `consider()` calls — so closing
the child dome to new residents would block the cohort delivery the feature
exists to protect. The two controls must act in **opposite directions on the
same dome simultaneously** (entry open, exit forced), so the new flag needs its
own field and its own gate. Packaging revised to a **separate module with D03 as
donor pattern only**, which also keeps D03's `tested` status intact.

**Chain confirmed end to end later the same sitting:**
`g_Consts.OverpopulatedDome` = **20**, dome read `overpopulated=true
homeless=20`. Step 4 is measured, not inferred. Note the threshold is `>=` and
the dome sat at **exactly** 20 (down from 28 as a few drained or died) — the
deadlock is genuine but marginal, so a future D12 test must show the drain
cleared it rather than attrition.

## PT-11 PASS → F01 `tested`, and the test that could not have worked — 2026-07-29 late

**PT-11 PASS → F01 `tested`** (P1, the first of the pack's fixes verified on the
SAVE-B no-disasters fixture). Preconditions live: `NoDisasters` true,
`Environment` Underground, fix `active`. Rubble baseline **27**; leg 1 (20 game
hours) **27**; save + reload, `g_Consts.MarsquakeSpawnTime` read back `1`, count
**27**; leg 2 (20 more) then the positive control
`CheatTriggerUndergroundMarsquake()` → **36**.

**Why +9 closes it:** `rubble_count = 10` (`Marsquake.lua:235`), so one quake
spawns at most ten cave-ins and nine landing (one `FindCaveInLocation` nil) is
the normal outcome. At most ONE quake occurred across the entire run, and the
control fired it. A single scheduler quake in leg 2 would have put the count
near 45; an unfixed pack, in the hundreds.

**THE TEST AS WRITTEN COULD NOT HAVE WORKED.** PT-11 said to set
`g_Consts.MarsquakeSpawnTime = 1` / `MarsquakeRandomTime = 1` and wait 20 game
hours. But a `MapGameTimeRepeat` computes its next interval at the END of each
tick and then sits in `Sleep(sleep)` (`CommonLua/Core/lib.lua:1590-1592`) — the
running thread keeps the interval it was handed *before* the edit. The defaults
are **384 and 96 hours** (`Lua/__const.lua:1085-1094`), i.e. **16 sols**, so the
prescribed 20-hour wait would have observed a thread still asleep on the old
interval and scored a PASS **whether or not the fix worked**. Every previous
reading of this test would have been vacuous.

Repaired by three additions, now in the checklist's ground rules as a general
rule (it applies to any scheduler-compression test, not just this one):
1. **`RestartPeriodicRepeatThread("<name>", CurrentMap)` after compressing**, so
   the fresh thread reads the new consts — verified with
   `IsValidThread(CurrentMap.RepeatThreads.<name>)`. It does not bypass a fix
   that wraps the repeat: the wrapper lives in `PeriodicRepeatInfo`, re-read
   every loop. **Must be repeated after each save/reload** — repeat threads are
   persistable (`MakeThreadPersistable`, `lib.lua:1595`), so a reload restores
   the old sleep.
2. **An objective counter** (`CurrentMap:MapGet("map", "CaveInRubble")`) instead
   of watching for damage. Also recorded: underground *buildings are irrelevant*
   to this test — `FindEpicentre` is `GetRandomPassable` →
   `GetPlayableAreaNearby` (`Marsquake.lua:237-241`), so quakes fire on a bare
   map and rubble lands near a random epicentre, not near the colony.
3. **A positive control at the end.** A negative test without one cannot
   distinguish "the fix worked" from "nothing would have happened anyway" —
   which was precisely this test's failure mode.

## PT-29 PASS + two documentation defects — 2026-07-29 late (live, on the SAVE-B fixture)

**PT-29 PASS → F41 `tested`** (index row + heading flipped, section moved to
PLAYTEST_ARCHIVE.md). Console read on a colony with both techs unresearched:
**`nil` → `50` → `150`**. Gene Forging alone now contributes its `param1 = 50`
where it contributed nothing before, and the two techs **add** — which is the
whole reason the fix is an additive sum rather than ChoGGi's GeneSelection
param1-bump (that approach pays out only when the *other* tech is also
researched, so Gene Forging alone would still have done nothing).

**Two documentation defects, both found by simply trying to run the test:**

1. **PT-29's trigger was unrunnable as written.** It read
   `MainCity.labels.Colonist[1]` while requiring the reading be taken "before
   researching anything" — you cannot have a colonist before the game
   auto-researches something. Neither constraint was real:
   `GetRareTraitChance(unit)` takes an **optional** unit
   (`local city = unit and unit.city or MainCity`, `Colonist.lua:3542`, a
   fallback the fix preserves verbatim), so a bare call works from sol 1; and
   the function consults **only** GeneSelection and GeneForging, so every other
   tech is irrelevant. Neither can arrive by accident either — GeneSelection is
   a **Breakthrough** (`CheatResearchAll` skips undiscovered ones) and
   GeneForging is a **Storybit** tech. PT-29 rewritten accordingly.
2. **`not understood` explained and written down.** The first attempt pasted the
   doc's `--> nil` annotations into the console and failed three times. Cause:
   the `*r` / `*g` rules splice the typed code into
   `CreateRealTimeThread(function() %s end) return` **on one line**
   (`uiConsole.lua:360-361`), so a `--` comment swallows the closing
   `end) return`, nothing compiles, no rule matches, and `console.lua:24`
   answers "not understood". Compounded by the console input being a SINGLE
   line — a pasted block concatenates, which is why `--> nil` and the next
   command arrived fused as `--> nilUIColony:SetTechResearched(...)`.
   **Never write a console snippet with a trailing comment or a `--> value`
   annotation.** Corollary also recorded: a bare expression is auto-wrapped in
   `ConsolePrint(print_format(...))` (`uiConsole.lua:363`), so a simple read
   needs neither `*r` nor `ConsolePrint`. Swept the rest of the checklist —
   PT-29 was the only instance of either trap.

**Coverage question raised and answered:** are any other playtests
research-sensitive? **No** — PT-29 was the only one, and the remaining un-run
items are gated on fixtures, mysteries and game rules, not research state (most
want *more* research, not less). But the check surfaced that **all four
tech-related fixes other than F41 have no playtest at all** — and three of them
correctly never will: **F28** is latent and mod-facing, **F43** is latent in the
shipped game (only one layout ships, `SelfSufficientDome`, and none of its
entries is tech-locked), and **F25** applies to pre-1.0.6 saves only, which is
also why its probe reports SKIP ("the tech has no description T") on a current
build — not a coverage hole, an unreachable defect. **F18** is the only
genuinely untested one; its preset half is already probe-covered
(`IndependenceTerraforming` PASSes), and the play half needs an Independence
sponsor plus a special project to observe `Consts.SpecialProjectResourcesModifier`
move 100 → 80 rather than → 90. Judged not worth a PT for a data-only P2;
recorded here so the question is not re-derived.

## Pre-flight A/B pair — 2026-07-29 late (unattended; the owed post-wave-6 re-baseline)

The A/B pair owed since wave 6 RAN, and it earned its keep: it caught a
TestKit defect that had made wave 6's automated coverage imaginary.

**Legs** (all unattended via `-smrautorun`, ~70 s each, logs in
`%AppData%\Surviving Mars Relaunched\logs`):

| Leg | Log | Result |
|---|---|---|
| Baseline (fix pack `code` list emptied) | 21.21.01 | **1 PASS, 60 FAIL, 15 SKIP, 0 ERROR** |
| Fixed, all six toggles ON | 21.22.35 | 63 PASS, 0 FAIL, **13** SKIP, 0 ERROR — 74/74 active |
| Fixed, re-verify after the probe repair | 21.25.56 | **66 PASS, 0 FAIL, 10 SKIP, 0 ERROR** — 74/74 active |
| Fixed, **default config** (six toggles OFF) | 21.36.51 | **61 PASS, 0 FAIL, 15 SKIP, 0 ERROR** — 68/74 active |

**76 probes now** (was 73). Baseline's 1 PASS is the FactionFundingCheck
canary, as always; all three wave-6 probes FAIL in baseline as designed —
including `RainsDeadlock`, which did NOT skip on the synthetic map (the
harness builds a colony, so `HasGame()` is true).

**THE FINDING — wave 6 had zero real probe coverage until this run.** The
middle leg showed PASS stuck at 63 while SKIP rose 10 → 13: the three wave-6
probes were reporting **SKIP with an empty message**. Cause: all three ran
every assertion and then fell off the end of `run()` without returning a
verdict, and `SMRTest.Run` turns a nil status into SKIP
(`00_TestCore.lua:243`). Every other wave file has exactly one `return "PASS"`
per probe; `55_Probes_Wave6.lua` had **none**. The file was written in the
post-QA build leg and never run against a *fixed* leg until now — baseline
FAILs come from the `FixMissing` guard and so never exercise the tail.

Repaired in the TestKit (local-only, commit `d701595`): explicit
`return "PASS", <what was verified>` in all three, and the two
`if x == nil then return end` holes now return an explicit FAIL — a bare
return read as an empty SKIP whether `WithGlobals` had deferred an ERROR or
the call simply answered nothing. Returning FAIL is safe for the deferred
case: `SMRTest.Run` overrides a FAIL with the pending ERROR
(`00_TestCore.lua:237-242`). Re-verified leg: 66/0/10/0. Reaching the tail
means every assertion had already passed, so the wave-6 *fixes* were correct
throughout — only the reporting was broken.

**Log hygiene, both legs:** zero `[CommunityFixPack]` inactive/error/disabled
lines, zero errors naming `SMR-BugFixPack\Code`. Four engine error signatures,
all present in BOTH legs and none ours: 48× `Flight.lua:465 objects_to_mark`,
1× `Flight.lua:479 objects_to_unmark`, plus the `GridObject:ApplyToGrids` /
`BuildWaypointChains` / `CreateResourceRequests` GameInit nil-calls (1× each in
baseline, 3× each in the fixed leg — each leg generates a different random map,
so per-signature counts vary; no new signature appeared).

**Account-state fact worth carrying:** the first fixed legs came up **74/74
active** — all six optional modules were already ON from the account's saved
Mod Options toggles (they are account-persistent, and no `SMRFixPack_Optional`
override was in play; the leg's temp file was never listed in metadata). So
those legs ARE the all-toggles leg. The user then turned all six OFF at the
main menu and the **default-config leg** ran: **68/74 active, 61/0/15/0**, with
the pack reporting all six `inactive (opt-in module, off by default)`. That
leg had to be done by hand because the pre-load override table can only force
modules ON, never off. **The A/B set is therefore complete — nothing is owed
to the harness.**

**Cross-leg arithmetic checks out exactly.** All-toggles 66/10 vs default
61/15: the difference is precisely the five opt-module probes
(ClassicRockets, AcknowledgedWarnings, ResidencyControl, MultipleSuns,
CohortHousing) moving PASS → SKIP. Five, not six, because **D06 has no probe
of its own by design** — the stress harness and PT-52 cover it. Against the
pre-wave-6 default leg (58/0/15/0 at 65/71): +3 PASS = the three repaired
wave-6 probes, SKIP identical at 15, active 65 → 68, total 71 → 74. The
toggles were left OFF afterwards, which is PT-55's required starting state.

**Harness discipline held:** `metadata.lua` was restored from a saved copy and
hash-verified byte-identical (`7C352189…`), the temporary `Code/97_OptInLeg.lua`
was deleted unused, nothing was committed while the baseline edit was in the
tree, and the TestKit autorun flag stayed commented out (the `-smrautorun`
command line armed the legs instead).

## Audit remediation session — 2026-07-29 (game-free, one-off AUDIT_FIX_PROMPT executed and deleted)

AUDIT_FINDINGS.md Phases 1-3 implemented in full, one commit per plan item
("Audit fix N.N" series, 88c2f08..HEAD). Parse sweep clean on every touched
Lua file; every patch target re-verified against Src before editing.

**Phase 1 (code):**
- 1.1 (A1) veto re-check in DustSicknessDamage / DustSicknessBiorobots /
  IndependenceTerraforming patch() (LastTransmissionStorage donor pattern);
  IndependenceTerraforming's status heal gated to never overwrite "disabled".
- 1.2 (B3) data_loaded latch in the DustSickness pair — absent targets after
  DataLoaded now latch `inactive` with a reason instead of reporting active
  forever.
- 1.3 (A2) file-scope install + per-call IsActive gate (Opt_DroneOverhaul
  donor) for Opt_ClassicRockets (whole fuel wrap), Opt_ResidencyControl
  (ONLY the CanAcceptNewColonists gate) and Opt_MultipleSuns (ONLY the
  GameInit binding wrap) — first mid-session enable now works; apply() keeps
  its self-checks and reason strings; headers tell the truth.
- 1.4 (B1) reconciler retries "error" entries on toggle-ON, logs every
  skip/failed retry and vetoed-toggle attempt, and surfaces
  on_activate/on_deactivate errors.
- 1.5 (B2) MeteorStormWedge's vanilla-release path clears
  g_DisastersPredicted.DisasterMeteorStorm itself (guarded on no live
  notification) — self-sufficient with F81 disabled, idempotent beside it.
- 1.6 (C4) %% escaping on all 6 remaining unescaped ModLog sites (the plan's
  "6 local + 4 inline" double-counted — grep proved exactly 6 existed);
  MoraleComfortTooltip's false returns-pass-through comment corrected
  (shipped UIStatUpdate verified to return nothing); build stamp
  1.0.7.396349 added to F05/F08/F07+F15/F29 headers.

**Phase 2 (packaging/storefront):**
- 2.1 metadata.lua: short_description (192 chars), last_changes,
  optional_mod=true, version 1.0, ignore_files (defaults + docs/.claude/
  README/.gitignore; LICENSE ships), description's per-fix-disable claim
  qualified. lua_revision confirmed and kept.
- 2.2 items.lua: 75 ModItemCode entries script-generated from metadata.lua
  and diff-verified identical order — the editor round-trip / upload flow no
  longer regenerates `code = false`. Toggles untouched.
- 2.3 MOD_DESCRIPTION.md: CohortHousing block (name verified in-game:
  "Retirement Home"); honest savegame-footprint wording replaces the false
  "stores nothing" claim; console achievements disclosure (Xbox/PS/MS Store
  blocked, Steam/PC not); PC-only per-fix-disable caveat; console
  bug-reporting variant.
- 2.4 README.md: 4 missing fixes + 2 missing modules added; findings count
  73 → 91. (2.5 preview image / screenshots / portal rules = owner tasks,
  still open.)

**Phase 3 (docs):**
- 3.1 F02 heading + RESOLUTION note (root cause pinned to F78/F81); D07
  heading matched to its index row; withdrawn fpk-divergence doctrine
  corrected in its last two live copies + BUGS/WORKFLOW framing now cites
  the 2,250/2,256 parity proof. (D06's index/heading already agreed.)
- 3.2 ENGINE_FACTS.md extracted verbatim from STATUS "Key technical facts"
  (sole authoritative home); pointers updated.
- 3.3 STATUS.md rebuilt as a ~225-line current-state doc (header with
  authoritative counts / open decisions / next gates + reference sections);
  all legs, wave records and superseded A/B tables moved verbatim to THIS
  file; stale "47 tracked defects" headline no longer styled as current.
- 3.4 sediment archived (ChatGPT report, RESEARCH, TESTING,
  CHEATS_INVENTORY) with promotions first: RESEARCH §3 leads → C03-C08,
  PLUS its three HIGH untraced leads → C09-C11 (small scope extension so
  archiving didn't bury them); CHEATS_INVENTORY's 11 missing commands +
  negative-knowledge list folded into the checklist's verified table (Src
  lines re-verified); TestKit README's probe table was already in place —
  its two stale pointers fixed (one docs-only TestKit commit, 39ecdba).
- 3.5 WORKFLOW.md rewritten (reading path, per-fix discipline, fpk
  extraction diff as an explicit release gate, post-audit release steps).
- 3.6 FIX_POLICY: global-replacement rank 4b, reconstruction sub-category,
  declaring-class rule, OnMsg status+veto rule, data_loaded-latch rule, new
  optional-modules / engine-semantics / console-platforms sections.
- 3.7 28 BUGS.md index rows slimmed to status + date + PT ref (prose
  verified present in entries first).

**Found beyond the audit:** nothing contradicting a finding; two counting
nits (the 1.6 "6+4" double-count; D06's 3.1 half already fixed pre-audit).
PT-55 added to the checklist for the owed human re-verify.

**Owed to humans:** PT-55 (three reworked opt-modules' live toggles, both
directions, mid-session FIRST enable); a PT-20-shaped save/remove/load cycle
covering wave-6 persisted state; the pre-flight A/B RunAll pair (still owed
since wave 6); owner tasks 2.5; the Phase 4 go-decision.

## Superseded rolling wrap (the pre-restructure STATUS header, through 2026-07-29)

Updated: **2026-07-29 LATE (QA-review session + wave-6 build): the
fresh-context QA review RAN and reported — every Track A/B claim verified at
source, the fpk-divergence doctrine WITHDRAWN (full `Lua.fpk` extraction:
2250/2256 files byte-identical to Src, build `1.0.7.396349` — see Key
technical facts), and the Track A plan was revised to an additive/watchdog
shape. That plan is now BUILT (user go, unattended leg): **F78 + F81 fixed** —
`Fix_DisasterPredictionLeak` (additive MeteorStormEnded removal + PostLoadGame
flag reconciliation), `Fix_MeteorStormWedge` (hourly wedge watchdog, heal via
RestartGlobalGameTimeThread + guarded stop pulse), `Fix_RainsDeadlock`
(bounded rains wait + persisted-loop refresh) — wave-6 probes in the TestKit
(`55_Probes_Wave6.lua`), **PT-54 is the live gate and an A/B RunAll pair is
QUEUED as the next session's pre-flight**. Track B decisions: claim gate
kept-but-demoted; the overhaul will ship Mod Options STAT DIALS (speed
×1.0/1.5/2.0, carry +0/+1/+2 — DECISION section in
`DRONE_OVERHAUL_OPTIONS.md`); the user's colony was measured at the vanilla
stat ceiling (2304 = +60% speed, 2× carry), so the structural choice (priority
escalation vs D08 dispatcher) is gated on the request-lifecycle
instrumentation — **BUILT 2026-07-29 (stress harness v2, TestKit
`91_Stress.lua`: per-request lifecycle tracing via RequestAssignUnit/
RequestUnitFulfill + StartDemandPhase/StartWorkPhase/Repair wrappers, gate
scored on the FindTask-decided cohort only, run-conditions header, stat-dial
legs first-class; `HARNESS_REVIEW_PROMPT.md` executed and deleted). Two new
Src facts recorded on D06: SetCommandKeepQueue preempts immediately (the ~57m
work→claim was NOT the deliverer handoff) and SHUTTLE deliveries misfire the
handoff (CargoShuttle has no Work method) so shuttle-hauled repairs DO go
through FindTask. The PT-52 B2 re-run with the v2 harness is the next live
gate.** Prior wrap: **2026-07-29 (live disaster leg — see the
section directly below): TWO P1 defects found. F81 CONFIRMED LIVE — a single
stranded `g_DisastersPredicted` flag was gating the colony's ENTIRE weather
system, and clearing it started rain instantly; the leak that strands it is
UNCONDITIONAL (every completed meteor storm does it). F78 reproduced on demand
and localized to the unbounded drain loop at `Meteors.lua:238-241`. F82 filed.
Drone stress harness built (TestKit, local-only) — its A/B has now RUN (null
result; see D06). D08 extender overhaul designed, nothing built.** Prior wrap: **2026-07-28 LATE (post-D07-build): D07 `Opt_CohortHousing` BUILT
(user-authorized unattended leg) with a FRESH A/B pair — 73 probes, baseline
1/57/15/0 · all-six-toggles 63/0/10/0 (71/71) — plus PT-23 → F46 and PT-09 →
F14 flips (twelve flips total on the day). See the "D07 build leg" section
directly below.** Prior wrap: **2026-07-28 session wrap — the PT-52 live sitting (D03 tested,
F71 tested, PT-52 telemetry healthy, F68 over-draw caught) + the same-day
game-free F68 repair leg with a FRESH A/B pair (baseline 1/57/14/0 ·
all-five-toggles 62/0/10/0, 70/70 — no pre-flight queued for the next
session). See the two 2026-07-28 leg sections below and the header
additions.** Prior wrap follows: 2026-07-27 night (**D05 SHIPPED AND TESTED same
night — optional modules enable in-game via Options → Mod Options, live both
directions, restart-persistent (PT-51 archived); PT-50 PASS in full → D04
tested; PT-49 core passing + row reposition verified; ListFixes crash found
by play and repaired; F76 surface widened to the dozer path; the drone
task-assignment investigate item is fully stocked and has its own kickoff
prompt.** 72 probes; last legs clean: baseline 1/57/14/0 · fixed 58/0/14/0
(64/68) · opt-in 61/0/11/0 (67/68); **an A/B re-verify is QUEUED as the next
session's pre-flight** (two mechanical repairs landed after the last pair —
expected numbers unchanged). See "Mod Options build leg" below; the earlier
same-day build leg and the playtest-marathon record follow). **2026-07-28:
the drone task-assignment static investigation leg is DONE (section below),
and the user-greenlit D06 overhaul core + F77 fix are BUILT the same day —
see the build-leg section directly below. PT-52 (attended, multi-iteration)
is the next sitting's centerpiece.** **2026-07-28 PT-52 sitting (live):
PT-49 COMPLETED in full → D03 `tested` (archived) — arrivals + tourists
proven against an adversarial pad-beside-the-closed-dome setup, an
unexpected child resident forensically cleared as in-dome birth, MicroG row
verified on an asteroid habitat and KEPT there by user decision (two real
auto-move-in paths exist: inter-habitat resettlement and stranded
re-homing).** **Same sitting, lander leg: PT-17 ratchet PASS (request pinned
at the hold across 4 automated cycles, no unload flip) and PT-32 PASS in
full → F71 `tested` (archived) — live two-resource priority inversion,
valuables first, nothing dropped. Capacity-edge leg: no wedge, BUT a NEW
FINDING on the F68 fix — request over-draws below the GET-WHEN-ABOVE
threshold under active mining (asteroid drained to 84 vs threshold 144);
root cause + repair sketch on the F68 entry (the fix double-implements the
anti-churn floor; delete the aboard-into-ground half). **BOTH queued repairs
LANDED the same evening (F68 over-draw + TestKit logger — see the repair-leg
section) with a fresh A/B pair; the build queue is EMPTY again.** PT-17
stays un-archived pending an attended capacity-edge re-run — **DONE 2026-07-28
next sitting: re-run PASS (ground settled AT the threshold, request tracked
instead of ratcheting) → F68 `tested`, PT-17 archived; PT-19 PASS same
sitting → F73 `tested`, archived (residence held through both gap shapes);
PT-33 PASS same sitting → F72 `tested`, archived (all three cases incl.
both not-over-broad negatives); PT-40 PASS same sitting → F65 `tested`,
archived (merge both geometries, clean salvage split, long-track control,
reload, log clean); PT-31 PASS same sitting → F70 `tested`, archived
(round trip held, prefill negative intact); PT-16 PASS same sitting →
F67 + F69 `tested`, archived — **the ASTEROID SECTION is COMPLETE.** PT-43
PASS in full same sitting → F19 + F20 + F21 `tested`, archived — **TEN
status flips in one sitting (F68, F73, F72, F65, F70, F67, F69, F19, F20,
F21), plus two NEW vanilla findings from the PT-43 setup (F79 trains-never-
serve-services, confirmed; F80 trains-skip-waiting-passengers,
investigating).**
Also proven this
sitting: the class-flattening runtime corollary (ENGINE_FACTS.md).**

## Disaster-system leg + drone stress harness + D08 design — 2026-07-29 (live, the project's biggest single-defect find)

One long attended session. **Two P1 defects found and one of them proven live,
end to end, with the recovery demonstrated on the user's save.** Full forensics
on the entries; this is the index.

- **F81 CONFIRMED LIVE (P1) — one stranded prediction flag was gating the
  colony's entire weather system.** `g_DisastersPredicted["DisasterMeteorStorm"]`
  sat `true` with no storm running; `IsDisasterPredicted()` therefore blocked
  rains (early-return in `RainsDisasterActivation`) and starved dust storms and
  cold waves (both scheduler loops push `wait_time` forward while it is true).
  `RemoveDisasterNotifications("DisasterMeteorStorm", MainMap)` → **rain started
  immediately**, then a toxic-rain warning, then a marsquake. 194 sols of "no
  weather ever" explained and fixed by one console line.
- **The leak is UNCONDITIONAL (grep-verified):** only three code paths ever
  remove that notification, and **the normal completion path of `MeteorsDisaster`
  is not one of them** (`Meteors.lua:242-251`). So on any map with storms
  enabled, the FIRST storm — wedged or perfectly healthy — permanently kills that
  colony's cold waves and rains. Highest-impact finding the project has made.
- **F78 REPRODUCED ON DEMAND AND LOCALIZED TO THREE LINES.** The stall is the
  unbounded drain loop `Meteors.lua:238-241`: `table.validate` works (73
  descriptors → 2) but two meteors never go invalid, so `#spawned` never reaches
  0. Hypothesis 1 was half right — not un-exitable, just unbounded. Controls:
  `single` completes cleanly; the spawn loop terminates normally.
- **New hazard for the repair: TWO storms wedged simultaneously**, and
  `g_MeteorStormStop` is a **shared global** consumed by whichever thread wakes
  first. Any bound must be per-invocation, and the fix must assume concurrency.
- **One confident theory DISPROVED by test** — we predicted a save/load inside a
  warning window would strand the flag; it does not (notification and thread both
  survive). `SavegameFixups.*` is a one-time legacy migration, not routine load
  behaviour. Recorded on the entry so it is not re-derived.
- **F82 filed (P3):** split power/life-support grid notification lingers ~a sol
  after the grid is rejoined; machinery located, updater cadence still to trace.
- ~~**Src ≠ shipped `Lua.fpk`, proven:** `GetCameraLookAtPassable` exists in Src and
  **not at runtime**, which is why bare `CheatMeteors("storm")` silently no-ops.
  Command table corrected. Treat all Src-only reasoning as provisional.~~
  **[WITHDRAWN 2026-07-29 — this was a misreading.** `GetCameraLookAtPassable`
  is a `local function` in Cheats.lua, invisible to the console *by design*,
  identical in Src and shipped. The full `Lua.fpk` extraction diff proved the
  shipped build IS Src: 2,250/2,256 files byte-identical, the 5 divergences
  engine/tooling only. The command-table correction stands on its own merits
  (always pass an explicit position). See ENGINE_FACTS.md → parity.]
- **Drone stress harness BUILT** (`TestKit/Code/91_Stress.lua`, local-only, no
  A/B owed): `SMRTest.Stress.Break/Targets/Report/Compare/HealAll/Stop`. Breaks a
  seeded deterministic set so the same save reloaded gives a true controlled A/B;
  captures every repair claim via a leaf-class pre-wrap on `Drone:Work` and
  reports **closest-hub first claims %** as the headline. *(That v1 metric was
  invalidated by the run below and the harness was REBUILT v2 on 2026-07-29 —
  see the header wrap and the D06 entry.)*
- **THE A/B RAN (2026-07-29) — NULL RESULT for D06's claim gate, and it exposed
  why.** Controlled: same quicksave reloaded, identical seeded set, both legs at
  normal speed, storages equalised. With the module ON the gate intervened
  **once** (`vetoed +1`) across 25 simultaneous malfunctions and the leg it
  arbitrates moved **58m → 57m**; the 34m total gain sits in the **hauling** leg
  D06 exempts by design, so it is variance. Cause: **0 of 25 targets were
  `no_resource` maintenance**, so `MaintenanceDroneUnload` → `StartWorkPhase(drone)`
  gave the first repair tick to the **delivering** drone every time, bypassing
  `FindTask` — **the metric measured which hub DELIVERED, not which won a
  claim** (the exact risk `HARNESS_REVIEW_PROMPT.md` §2 was written to catch).
  **Bigger finding: hauling is 3h03m of a 3h27m total — 88% of elapsed time**,
  which meets the options doc's own escalation condition and promotes D08's
  dispatcher (registration determines who can deliver) from speculation to
  evidence-backed. Full numbers and caveats on the D06 entry.
- **PT-52 sitting 3: healthy under real load** — DroneReport taken right after a
  marsquake damaged several buildings: nine hubs, `unclaimed=0` on every one,
  all laps `low`, `vetoed=3 / veto_expired=0 / moonlighted=0`.
- **D08 designed** (`DRONE_OVERHAUL_OPTIONS.md`) — extender overhaul in five
  layers with a risk table and five open questions. Origin: the user's live
  observation that extenders make the D06 problem worse. Nothing built.
- **`QA_REVIEW_PROMPT.md` written** — a one-off adversarial review prompt for a
  fresh session to QA both tracks before anything is implemented. *(Fired
  2026-07-29 late; verdict folded; file deleted per its own rule — see the
  newest wrap at the top of this document.)*
- **PT-53 PARTIAL PASS — D07 `Opt_CohortHousing` enabled live for the first time
  and works** ("it worked wonderfully"). Cross-dome consolidation confirmed from
  EVERY dome for both cohorts, over **trains, passages and shuttles chosen by
  distance**; graduation drain confirmed (with a transient homeless flicker that
  is the designed shape, recorded so it is not mistaken for a defect). Bonus:
  children reached services **via passages**, live corroboration of F79's
  passage-only service search. **No-churn also PASSED organically** — where
  cohort housing ran short those colonists simply stayed put with no hiccups,
  which is the "completely untouched when no slot exists" design confirmed at
  colony scale. **3 of 5 triggers pass; not flipped to `tested`** — the
  employed-senior exemption (A) and precedence/uninstall (E) are still owed.

## D07 build leg + two more flips — Fable, 2026-07-28 late (mixed live/game-free)

Same calendar day as the ten-flip sitting; a short live leg (user at keyboard)
followed by a user-authorized unattended build leg while they were away.

- **PT-23 PASS → F46 `tested` (archived), eleventh flip.** Both halves on the
  live 5-station network: forbidden Metals drained to 0/60 and STAYED; the
  all-five-stations-forbidden + drones-off leg proved trains dump rather than
  strand (zero loaded roamers). Isolated no-drone stations keeping stock =
  expected statics, recorded as an observation on the entry.
- **PT-09 PASS → F14 `tested` (archived), twelfth flip.** Red low-stat cell
  verified per-CELL both directions (red at Comfort 0, white on recovery).
  Two researched facts recorded: the peril statuses share a 12-36h
  per-colonist GRACE window before Health damage (StatusEffects.lua:93-98,
  then avg ~2x base rate, stacking); the fifth overview column is
  SATISFACTION (tourist-rating stat, ChangeSatisfaction zeroes gains past
  the tourist sol window) — its red 0 on every mature dome is CORRECT
  vanilla-intended rendering the F14 bug had been hiding.
- **D07 `Opt_CohortHousing` BUILT (user gave config + go the same evening:
  in-dome-first + cross-dome, Seniors+Children one toggle, then "start
  working on it" for the unattended window).** Colonist/housing-level rule,
  zero persisted state, all hooks per-call-gated: UpdateResidence post-wrap
  (in-dome move), FindEmigrationDome post-wrap (nearest-reachable cohort
  slot, tie rule bypassed; quarantine/D03/forced-dome/overpopulation
  respected), ColonistBecameYouth nudge. Mod Options toggle #6. Full notes
  on the D07 entry; PT-53 written into the checklist (5 triggers).
- **A/B pair FRESH (2026-07-28 late, 73 probes):** baseline **1/57/15/0** ·
  all-SIX-toggles **63/0/10/0 (71/71 applied)**, zero errors, both legs on
  predicted numbers. NO pre-flight owed. Two probe-side lessons from the
  leg (module itself never wrong): (a) **WithGlobals stubs cannot reach a
  game file that localizes the global at load time** — Colonist.lua:5 does
  `local IsValid = IsValid`, so stand-in probes must assert on the MODULE's
  action (absence/presence of its move), not on vanilla bookkeeping around
  plain-table stand-ins; (b) a fake colonist driven through the shipped
  FindEmigrationDome tail needs a PickEmigrationCommunity stub.
- Housekeeping: D07 config decision recorded on the entry when given
  (commit 6ca11a1); prompt un-run list updated (PT-09/PT-23 gone, PT-53
  added); Satisfaction/grace observations archived with their PTs.

## TEN-FLIP playtest sitting — Fable, 2026-07-28 evening (live, the project's most productive sitting)

One long attended session; full per-test evidence in `PLAYTEST_ARCHIVE.md`,
forensic trails on the entries. Zero pack code changed (no A/B owed).

- **Ten `tested` flips:** F68 (PT-17 capacity-edge re-run — ground settled AT
  the threshold), F73 (PT-19, both life-support gap shapes), F72 (PT-33, all
  three cases), F65 (PT-40 full procedure), F70 (PT-31 round trip), F67+F69
  (PT-16 — full-sol asteroid hold logged; manual-landing fuel ration kept and
  flown home), F19+F20+F21 (PT-43 in full). **The ASTEROID SECTION is
  COMPLETE.**
- **Validated live:** the map-switch console-death repair (workaround
  retired), the repaired AutoCargo logger (first live capture drove the F68
  re-run), the repaired CargoReady logger (leaf-class + change-only, repaired
  mid-session in a game-free break, first verdicts drove the F67 read).
- **F78:** hypothesis 1 (descriptor-validate infinite loop) REFUTED live
  (`table.validate` removes plain tables — `kept: 0`); on VeryLow the strike
  routine is statically seconds-bounded, so the 183h stall contradicts static
  analysis → on-demand repro plan banked on the entry (bracket taps +
  `CheatMeteors("single")` at empty ground).
- **NEW F79 (confirmed):** colonists never use trains for services —
  `Dome:GetService` is passage-only while the train-aware reachability serves
  only Workplace/Training/Residence. Fix = feature-completion, D-item, USER
  DECISION pending. **NEW F80 (investigating):** trains stopped 4+ times and
  skipped ~19 valid waiting passengers (full config-exonerating forensics on
  the entry; direction-blind-spot suspicion; mitigated by adding trains 2→5).
- **NEW D07 speced (user-commissioned, revised same day):
  `Opt_CohortHousing`** — colonist/housing-level rule, NO dome designation:
  cohort members in normal housing move to free Retirement Home/Nursery
  slots anywhere (in-dome reassignment first, cross-dome emigration
  second), completely untouched when no cohort slot exists; employed
  seniors exempt; graduation drains naturally; zero persisted state. Build
  awaits user go.
- **PT-52 sitting 2: healthy.** Readings `vetoed 1→9 / veto_expired 0→1 /
  moonlighted 0`, `unclaimed=0` on all seven hubs throughout (new hub 4230
  integrated); counters correctly survived a save reload and correctly reset
  on the mid-session relaunch. **Trigger B still un-run.** Log hygiene: the
  full session log swept — ZERO Lua/mod errors.
- New engine facts recorded on entries: `CheckAutoDepart` consults only the
  CURRENT side's rule set (empty side-set = designed collect-trip);
  `RoughTouchDown` storybit can strand a lander on a bare asteroid
  (`maintenance_request:SetAmount(0)` is the verified recovery);
  `Colonist:ChangeComfort(amount, reason)` is the clean stat-injection path;
  trains carry workers/trainees/migrants only (F79); the trip planner books
  tickets with no regard for actual train service.

## F68 over-draw repair leg — Fable, 2026-07-28 (game-free, post-playtest): same-day mechanical repair + fresh A/B pair

The PT-52 sitting's lander leg (PT-17 capacity edge) caught the pack's own
F68 fix over-exporting below the player's GET-WHEN-ABOVE threshold; the
repair landed the same evening once the user closed the game.

- **Root cause, live-proven before touching code:** the TAP2 console-tap
  arithmetic matched `ground + 2×aboard − threshold` EXACTLY at every
  recompute (52/72/98 at aboard 12/32/58; final ground 184−100=84) —
  **`GetTotalCargoAvailable` already counts a landed rocket's own hold**, so
  the v1 fix's aboard-into-ground addition double-counted every unit aboard
  and the request ratcheted monotonically to the hold cap. New engine fact,
  recorded here.
- **Repair (`Code/Fix_LanderCargoRatchet.lua`):** the addition
  (old :145-151) DELETED; the explicit request-floor block (never ask below
  aboard) now carries the whole F68 anti-churn fix. Header comment documents
  the discovery + repair. Parse clean.
- **TestKit AutoCargo logger repaired in the same leg** (local commit): two
  live-proven flaws — wraps the leaf class `UniversalLanderRocket` now (the
  flattening corollary made the old base-class runtime wrap structurally
  blind to real landers), and reads `self.cargo[res].requested` post-call
  (the return value it used to print is always nil).
- **A/B pair, fresh (also clears the queued pre-flight):** baseline
  1/57/14/0 · all-five-toggles 62/0/10/0 (**70/70 applied**, user's Mod
  Options toggles all on, zero pack errors, noise = the known synthetic-map
  set). The LanderCargoRatchet probe passes through the floor path
  (`request 300000 >= 300000 aboard`) — the probe needed no change, by
  design of the repair.
- **Validation debt: CLEARED 2026-07-28 (next sitting).** The attended
  capacity-edge re-run PASSed on the live colony: Concrete above 0 + Rare
  Metals above 140 with extractors replenishing mid-load; request tracked
  `aboard + surplus` (PreciousMetals 90000→92000, creeping only by the mined
  amount) instead of ratcheting; ground after departure 146 with miners
  running = settled AT the threshold. The repaired TestKit AutoCargo logger
  did the capture — its first live validation. **F68 → `tested`; PT-17
  archived.**

## D06 build leg — Fable, 2026-07-28: drone dispatch overhaul core v1 + F77 fix (user-greenlit, PT-52 pending)

Built same-day on the investigation verdict and the user's design review
(their proximity-cascade idea became option H in the study; the shipped claim
gate is its veto variant — reversible and orphan-proof, chosen for v1).

- **`Code/Opt_DroneOverhaul.lua`** (opt-in, off by default, Mod Options
  toggle "Drone dispatch overhaul (experimental)"; hooks installed at
  classdef time, gated per call on IsActive; NO persisted state):
  1. closest-fleet-first claim gate — chained wrapper on
     `TaskRequestHub:FindTask` (sole caller = drone auto-Idle, so player
     orders untouched): repair/clean work offered to a non-closest covering
     hub is withheld while the closest hub has idle drones; per-request
     strike cap (4 polls / 30s decay) makes starvation impossible;
  2. repair moonlighting — chained POST-wrapper on `Drone:Idle` (the body
     falls through exactly when workless — verified engine fact): workless
     drones take unclaimed repair/clean work of SATURATED neighbor hubs
     within 30 hexes and their own restrict area, vanilla-style SetCommand;
  3. `SMRFixPack.DroneReport()` telemetry (always on, read-only): per-hub
     state + module counters vetoed/veto_expired/moonlighted.
- **`Code/Fix_ExtenderFlapChurn.lua`** (F77, default-on fix): extender
  working-flaps now debounce+coalesce the whole-hub rebuild (2s, per root
  hub, chains resolved) instead of tearing it down twice per blip.
- Wire-up: items.lua toggle + metadata `default_options.DroneOverhaul` +
  code list. Parse sweep: all 4 touched files pass (python luaparser).
- Scope guards worth knowing when judging PT-52: rockets/rovers/construction/
  hauling all exempted by design; the claim gate cannot veto player orders
  structurally (FindTask is not on that path); toggling off restores vanilla
  instantly (registration layer untouched).
- Docs (full pass, same day): D06 entry + index row (BUGS), F77 flipped to
  `fixed` (row + tag), options doc carries the build note. **PT-52 is a full
  checklist procedure now** (PLAYTEST_CHECKLIST, optional-modules group):
  CAN/CANNOT-do lists, Trigger A passive watch, Trigger B controlled off/on
  A/B demo, Trigger C regression watch, result lines, knob log line.
  MOD_DESCRIPTION got the player-facing F77 bullet (Buildings & economy) and
  the "Drone dispatch overhaul — experimental" module block.
  FABLE_NEXT_PROMPT rewritten post-build (PT-52 centerpiece + assistant
  briefing notes, 65/70 module counts, D06 read-list pointers);
  DRONE_INVESTIGATION_PROMPT retired/deleted. `DroneReport` upgraded to
  print ON-SCREEN (ConsolePrint) AND to the log — the ListFixes lesson,
  applied before it bit.
- The user expects multiple iterations across sittings; knob changes get
  recorded on the D06 entry (mechanical, assistant may land same-day);
  design-level changes (H-v2, registration-H, balancer C) stay user
  decisions per the options doc.
- Testing debt, stated: no TestKit probes for the module yet (attended
  playtest is the v1 validation instrument; probes come with the iteration
  that stabilizes the design).

## Drone task-assignment investigation leg — Fable, 2026-07-28 (game-free, docs-only): verdict in

The `DRONE_INVESTIGATION_PROMPT.md` kickoff, executed as specced (no game, no
loadable-code edits, Src read-only). Full verdict + trace + instrumentation
plan live on the BUGS "Not yet swept" DroneControl bullet; **F77** filed
(index row + entry). Headlines:

- **Architecture verdict: working-as-coded, but with NO cross-hub locality
  anywhere.** Assignment is PULL and own-hub-only — `Drone:Idle`
  (`Drone.lua:564-641`) polls `command_center:FindTask(self)` (`:621`), the
  single FindTask call site in Src; the match itself is the C-side
  `Request_FindTask` over the hub's own queues (ordering/distance policy
  engine-internal — recorded as unverifiable from Lua). A building in overlap
  registers with EVERY covering hub and its (shared, C-side) request objects
  sit in every such hub's queues; the claim is first-poller-wins at command
  start and **held through the whole approach** (`Drone:Work`,
  `Drone.lua:898-924`); maintenance repair requests are **max_units = 1**
  (`RequiresMaintenance.lua:82`), so one far drone locks out a fleet parked
  next to the job. No handoff, stealing, or rebalancing exists anywhere.
- **Extender transparency CONFIRMED** (the user's hypothesis): both connect
  directions register the far HUB itself on the building
  (`DroneHubExtender.lua:156-160` building-side recursion;
  `DroneControl.lua:315-325` hub-side recursion) — extender-mediated coverage
  is indistinguishable from native in every match structure. Extenders do NOT
  extend drone movement: `const.DroneRestrictRadius` (100 hexes-worth) is
  anchored on the HUB position (`Drone.lua:227-230`, `_GameConst.lua:71`);
  post-SignalBoosters a 2-extender chain can register buildings a hub's
  drones can never legally reach (suspected F55-feeder, engine-side check —
  flagged for live).
- **NEW F77 (defect, provable):** every extender working transition (power
  blip, malfunction, repair, toggle — both edges) triggers a FULL
  disconnect+reconnect of the entire uplink hub's requester set
  (`DroneHubExtender.lua:171-178` → `DroneControl.lua:441-450`), Idle-kicking
  every drone en route to any connected building (`:720-729`) and burning
  O(B×D) + queue-rebuild work per flap. Reproduces both observed halves on
  its own. Fix sketch: debounce wrapper (user decision).
- **The live starvation stays two-hypothesis** until one attended sitting:
  (a) registration gap (starving buildings outside hub 2608's circle, inside
  the far hub's extender-stretched coverage — pure design) vs (b) claim
  lockout (in both queues, far fleet wins the claim race every chunk). The
  banked `target:0` read is consistent with both. **R1-R7 console reads** (on
  the bullet; sandbox-verified, incl. a `RequestAssignUnit` claim tap — no
  file-local alias in Drone.lua, so a console global wrapper is seen) settle
  it; R7 is the hub-A/hub-B/extender repro with `CheatMalfunction`.
- **Performance answer (the user's second observation):** per-idle-drone
  FindTask polls scan the hub's full queue set every ~3s and overlap
  multiplies queue content (k-hub overlap ≈ k× colony-wide scan work); the 1s
  empty-queue throttle can't engage while any drone holds unreachable-cache
  entries (`Drone.lua:630`); reconnect storms (radius change, F77 flaps, and
  `OnMsg.DepositsSpawned` reconnecting EVERY hub at once,
  `DroneHub.lua:188-199`) are O(B×D)-grade each. Range × drones × requests,
  exactly as reported.
- **Nothing was built** (per spec). Build decisions for the user: F77
  debounce (plain repair), and the locality levers — cross-hub idle-pull
  pre-wrap on `Drone:Idle` for (a) vs near-idle claim veto on
  `Drone:Work`/`PickUp` for (b) — which are assignment-POLICY changes
  (D-item territory). All sketches + risk statements on the bullet/F77 entry.
- **Follow-up same leg (user-commissioned): `docs/DRONE_OVERHAUL_OPTIONS.md`**
  — the D06-candidate feasibility study for an optional overhaul toggle.
  Options A-G with verified patch points; key new engine findings:
  `Drone:Idle` falls through (returns) exactly when no work was found, so a
  chained POST-wrapper is a legal dispatch hook (the F73 pre-wrap-only rule
  is for command bodies that always SetCommand); `Drone:Work`/
  `ApproachWrapper` never consult `command_center` (cross-hub execution is
  clean); `Drone:SetCommandCenterUser` (`Drone.lua:2687-2694`) is the
  vanilla migration path. Recommended order: telemetry → repair
  moonlighting → migration balancer; claim-veto/handoff gated on the R1/R3
  live answer. USER DECISION before any build.

## Mod Options build leg (D05) — Fable, 2026-07-27 late: in-game enable surface for the optional modules

Triggered live: the user sat down for Group 8 and had **no main-menu console**
— and the briefed console route was falsified outright (the Opt_ gates run at
mod code load during startup, BEFORE the main menu; that is why the A/B
harness always needed the `97_OptInLeg.lua` flag FILE). Release context made
it a blocker: Steam Workshop + Paradox Mods, and **Paradox delivers PS/Xbox,
which have no console at all**. User picked "build now" over "temp file for
tonight". Full spec + Src evidence on the **D05** BUGS entry; summary:

- **items.lua (new):** four `ModItemOptionToggle`s (names == registry ids) put
  the pack on **Options → Mod Options** (main menu and pause menu, gamepad
  capable). **metadata.lua** gains the matching `default_options` table (what
  `HasOptions()` reads — without it the page ignores the pack).
- **00_Core:** `SMRFixPack.OptionEnabled(id)` (pre-load `SMRFixPack_Optional`
  OR the saved toggle — the values load before mod code, `CurrentModOptions`),
  `SMRFixPack.IsActive(id)`, defs retained, and an `OnMsg.ApplyModOptions`
  reconciler: ON = re-arm installed hooks or apply now (+`on_activate`); OFF =
  registry status flip (+`on_deactivate`). **Every optional module's wrappers
  consult IsActive per call**, so toggles are live in both directions with no
  unhooking. D04 flips the `build_once` template flag in its callbacks
  (restore guarded so a third-party limit mod is never stomped).
- **D04 cosmetic repair (pre-existing, exposed by the leg):** the transient
  pre-DataLoaded "ArtificialSun not found" detail no longer sticks on
  `ListFixes`; miss only recorded post-DataLoaded, cleared when the template
  appears. Engine fact: **DataLoaded fires more than once during startup; a
  template can miss the first pass.**
- **TestKit:** new probe `OptionsMenu` (60_Probes_Opt.lua) asserts the wiring
  in EVERY leg — metadata defaults, the four toggle items, the 00_Core bridge
  — and FAILs discriminatingly in baseline (registry absent). **72 probes.**
- **Legs (2026-07-27, logs Mars.exe-20260727-…):** parse sweep 82 files/0
  failures; baseline 21.20.32 = 1/**57**/14/0; fixed 21.21.51 = **58/0/14/0**
  (64/68); opt-in 21.34.28 = **61/0/11/0** (67/68) — all module probes +
  OptionsMenu PASS; gates log the new "enable it in Options → Mod Options"
  reason.
- **Docs same-commit:** D05 entry + index row, **PT-51** (Mod Options page
  eyes-on — now the FIRST step of the Group 8 sitting, since it is the enable
  mechanism), Group 8 preamble rewritten, MOD_DESCRIPTION optional-modules
  enable text now points at Mod Options (console-only instructions removed
  from player-facing text).
- **PT-51 first sitting, same night: `ListFixes()` crash found live and
  repaired** — latent since the 2026-07-25 F75/F18 status repairs
  (`entry.detail = nil` writers vs a concat in ListFixes; full trail on the
  D05 entry). Both writers now use `""`, ListFixes nil-tolerant. Takes effect
  on the user's next relaunch; **A/B pair re-verify queued for the next
  game-free window** (cosmetic to the probes — nothing reads ListFixes).
- **PT-51 COMPLETE, same night → D05 `tested` (archived):** all four toggles
  + tooltips good; live both ways proven twice (ClassicRockets on
  mid-session, MultipleSuns off/on vs the build menu); full shutdown +
  relaunch kept every toggle and the startup log shows all four modules
  self-activating from saved values; ListFixes printed 2×68 clean lines
  post-repair; log swept clean twice. **The PT-49 row reposition is also
  verified** ("UI good for dome" — the policy row now sits with the toggle
  group).
- **PT-49 first sitting, same night: core behavior PASSing** (closed
  high-comfort dome: zero move-ins, commute/services normal — screenshots).
  Cosmetic finding repaired same day: the policy row now inserts directly
  after the shipped accept-colonists toggle instead of below the stat bars
  (array reposition; trail on the D03 entry). Position re-check + the
  remaining PT-49 steps (arrivals, manual relocation, tourists, quarantine
  independence, MicroG row, uninstall) continue after the next relaunch.
- **PT-50 PASS in full, same night (the Group 8 sitting, running on the new
  Mod Options toggles) → D04 `tested`, F39's absorbed fix play-verified:**
  sun #2 built through the normal menu multiple sectors from #1; night
  production beside a sun matched the banked PT-26 signature exactly (3.6/9 @
  −21%; other sector 10 @ 0% — no atmospheric penalty there); sunless panels
  closed to 0 at night (not over-broad); save/reload clean; limit off/on
  verified LIVE via the toggle (doubles as PT-51 live-toggle evidence).
  Section archived. PT-51 partials recorded (page + live both ways verified;
  persistence-across-restart + log check remain). **Also observed live: an RC
  Terraformer (dozer) + waste-rock heap showed the F76 detached-hex picker
  rendering — Load-on-WasteRock is vanilla dozer behavior (RCTerraformer.lua:33,
  :224-237; pack ruled out, F74 wrappers refuse-only), and the picker surface
  DOES extend to the dozer path (user confirmed: hex appeared on CLICK) — F76
  addendum filed: any vehicle whose click-load reaches a storage-depot-class
  object is affected; loose rubble piles safe; the same TransferResources
  command workaround applies.**

## Build leg — Fable, 2026-07-27 late: F61 deletion + D02/D03/D04 built, A/B renumbered

The queued game-free build leg, executed as speced (all specs were on the BUGS
entries). Game never touched a save; three unattended `-smrautorun` legs only.

- **F61 retirement mechanics DONE:** `Code/Fix_HomeDomeMigrationGate.lua` + its
  metadata line deleted (git history restores them); the TestKit
  `HomeDomeMigrationGate` probe deleted with it (it tested the removed behavior —
  not an F10-style canary).
- **D02 `Opt_AcknowledgedWarnings` BUILT** (opt-in, off by default): dismissal of
  `NotWorkingBuildings` stamps every listed building
  (`SMRFixPack_ack_notworking`, absent-tolerant) and SKIPS the shipped
  4-game-hour whole-id window; stamped buildings' re-adds are dropped until
  recovery clears the stamp. Three chained wrappers on the notification helper
  GLOBALS (`SuppressNotification` — sole caller runs only under `dismissed`, so
  it IS the dismissal hook; `AddObjectToNotification`;
  `RemoveObjectFromNotification` — none is file-local in Notifications.lua, F22
  precedent). Only that one id is touched.
- **D03 `Opt_ResidencyControl` BUILT** (opt-in): new per-dome/habitat "closed to
  new residents" policy (`SMRFixPack_closed_to_new_residents` on the Dome,
  absent-tolerant). Gates: post-wrap `Community:CanAcceptNewColonists`
  (voluntary resettlement — only Src caller is FindEmigrationDome's filter) +
  post-wrap the global **`ChooseDome`** for arrivals. Build-time survey
  refinement: `GetDomesReachableByColonists` was rejected as the arrival patch
  point — it also feeds construction range display and worker checks, which must
  keep seeing closed domes; `ChooseDome` is the single choose-a-new-home funnel
  (rockets ×3, landers ×3, factory androids, stranded re-homing). `safety_dome`
  passes through unfiltered (no suffocation), `traits.Tourist` exempt (hotels).
  UI: post-wraps on `sectionDome:Init`/`sectionMicroGHabitat:Init` append the
  row; the toggle rides shipped `Community:TogglePolicy`/`SetPolicyState`
  (FX, Ctrl+click broadcast, rogue-dome UI lock for free). Closed state styled
  yellow/limit so it cannot be read as the red quarantine row.
- **D04 `Opt_MultipleSuns` BUILT** (opt-in): lifts
  `BuildingTemplates.ArtificialSun.build_once` from OnMsg.DataLoaded/DataChanged
  (handlers gate on registry status = opt-in + veto covered, F75 lesson; menu
  re-reads `CanBuildOnlyOnce()` live) AND absorbs the F39 wrapper + LoadGame
  sweep unchanged. `Fix_SecondArtificialSun.lua` DELETED; its probe reworked to
  the ClassicRockets SKIP-unless-opted pattern.
- **TestKit:** new `Code/60_Probes_Opt.lua` carries the three module probes
  (each SKIPs with the opt-in reason unless active); the two retired probes
  removed in place with dated tombstone comments.
- **Parse sweep:** 81 Lua files across both mods, 0 failures.
- **A/B pair + opt-in leg (2026-07-27, all clean, NEW EXPECTED NUMBERS —
  71 probes total now):**

| Leg | Log (Mars.exe-20260727-…) | Result |
|-----|---------------------------|--------|
| Baseline (pack emptied) | 20.38.21 | 1 PASS, **56 FAIL**, 14 SKIP, 0 ERROR |
| Fixed (default config) | 20.39.59 | **57 PASS, 0 FAIL, 14 SKIP, 0 ERROR** — 64/68 active (4 opt-in inactive) |
| Opt-in (three new modules on via temp flag file) | 20.41.49 | **60 PASS, 0 FAIL, 11 SKIP, 0 ERROR** — 67/68 active; all three new probes PASS incl. the live template lift |

  Renumbering from the old 1/58/11 · 59/0/11 (70 probes): −1 armed probe (F61
  deleted), F39's probe moved to opt-in SKIP, +2 new opt-in SKIPs (D02, D03).
  The 14 default-leg SKIPs = 10 [install] + 4 opt-in modules. Baseline's 1 PASS
  is still the FactionFundingCheck canary. Log noise unchanged (synthetic-map
  Flight.lua blocks in both legs; the quit-time TestKit mod-error artifact).
  Opt-in mechanism for the leg: temporary `Code/97_OptInLeg.lua` in the FIX
  PACK's code list right after 00_Core (set `SMRFixPack_Optional` before the
  Opt_ files load) — deleted after the leg; TestKit autorun flag line reverted.
- **Registered modules now 68** (67 − 2 deleted + 3 new); 64 active by default.
- **Docs same-commit:** BUGS index rows + heading tags (F39, F61, D02, D03,
  D04), MOD_DESCRIPTION Optional-modules section rewritten with the three new
  module blurbs (feature framing; F39 bug-fix bullet removed, sweep-list phrase
  dropped, D02 draft note resolved), PLAYTEST_CHECKLIST gains **Group 8:
  PT-48 (D02), PT-49 (D03 — first added infopanel row, needs eyes-on),
  PT-50 (D04, reworked PT-26 vs the banked single-sun baseline)**.
- **F76 was deliberately NOT touched** — attended sitting only (hard-lock
  vector; see the F76 entry and the prompt).

## Playtest marathon — Fable, 2026-07-26/27: 12 PTs resolved, F10 retired, D02 unblocked

One long interactive run with the user at the keyboard and this session driving
console instrumentation. Full per-test evidence is in `docs/PLAYTEST_ARCHIVE.md`
(new file — completed checklist sections move there, reporting-protocol step 8);
one-line summary here:

- **Flipped `tested`:** F03 (PT-02), F05 (PT-05), F12 (PT-07), F13 (PT-08),
  F44+F45 (PT-03), F47 (PT-45), F50 (PT-04), F51 (PT-12), F54 (PT-34),
  F66 (PT-41); **F52 `tested*`** (PT-13). F49(b) resolved no-defect (PT-46).
- **F12 second defect — the session's big catch (PT-07 first run):** the fixed
  updater's maintenance loop and food branch share the `"Food"` object key on
  the SAME notification; the maintenance else-path deleted the food branch's
  entry hourly → notification destroyed/recreated with FX + voice every game
  hour (voice plays only on whole-notification creation; VoicePerObject false).
  Latent in vanilla (broken math meant nothing could ever be added). Diagnosed
  by live console wrappers after five falsified hypotheses (dismissal cycle,
  threshold flap, object validation, stale second body, cross-city removal —
  full trail on the F12 entry). Repair: maintenance loop skips `"Food"`.
  **A/B clean 2026-07-27:** baseline 11.45.34 = 1/58/11/0; fixed 11.47.09 =
  59/0/11/0, 66/67 active. Re-run PASSed all behaviors incl. silent organic
  clears on both branches.
- **F10 CLOSED `wontfix` + DELETED (PT-36):** the three funding calls returned
  0 cleanly over a maximally nil organic history, and later read a real
  $544.5M tourist payout correctly — premise dead both ways.
  `Fix_FactionFundingCheck.lua` and its commented metadata line removed
  (git history restores both); the TestKit probe stays as a canary (it is the
  baseline's expected "1 PASS" — documented A/B numbers unchanged).
- **D02 gate DONE with a premise CORRECTION (PT-38):** the dismiss window is
  **120,000 GAME-ms = 4 game hours**, not 2 real minutes (`GameTime` defaults
  true; three live timestamped dismissal→return pairs = 120,000 +
  time-to-next-attempt, every in-window re-add attempt observed BLOCKED;
  suppression is per notification id). At ultra the re-nag is every few REAL
  seconds — D02's case is STRONGER. `Opt_AcknowledgedWarnings` build unblocked.
- **PT-06 (F08) DONE 2026-07-27 (later) → F08 `tested`:** 5★ 10-tourist
  departure paid at Earth ARRIVAL "+23 applicants, $544.5M" (2.3/head =
  top-tier); the tanked half (a 25-tourist group into a stripped dome —
  homeless, services off, Earthsick early leavers) paid "+7 applicants,
  $94.5M" = **0.28 applicants/$3.78M per head — an 8× per-head split**.
  Mechanics confirmed from Src during the run: departure rewards walk every
  boarded Tourist with no sols/reason filter (early leavers count); any stat
  < 30 caps the rating at the 2★ tier (`HolidayStatCapRating`); 7-from-25 is
  in band for the corrected mostly-1★ roll (~10 expected) and ~3σ below the
  shipped inverted roll (~15 expected) — corroborating evidence, not noise.
  Two cosmetic vanilla quirks
  recorded in the archive entry (overstay-cycle button no-ops silently on an
  empty sol-10+ bucket and only cycles the current map; sols-based tooltip
  labels early-leavers "Enjoying their holiday").
- **PT-26 (2026-07-27, later): F39's premise UNREACHABLE in the unmodded game →
  D04 filed (user decision).** The Artificial Sun is a `build_once` wonder
  enforced colony-wide incl. construction sites (`BuildMenu.lua:711-719`
  counting `UIColony.labels`; the tester's build menu refused sun #2 with sun
  #1 standing) — two suns can never coexist, so the F39 fix is latent hardening
  vanilla can never exercise. Resolution: **D04 `Opt_MultipleSuns`** — opt-in
  module that lifts the limit (`BuildingTemplates.ArtificialSun.build_once =
  false`, read live by the menu — verified in-session) AND absorbs the F39
  binding fix, so the pack provides the condition its fix needs and spares
  players a third-party limit mod that would hit the vanilla `[1]` bug.
  Single-sun baseline banked (night production at −21% atmospheric beside the
  lit sun). Standalone fix file deletion + module build queued for the
  game-free leg. Spec on the D04 entry.
- **F76 NEW FINDING (2026-07-27, found live during PT-39 setup): the RC
  Transport depot resource picker renders far from the cursor and cannot be
  clicked** (vanilla, P1). "Load from depot" looks completely broken — icon +
  noise, nothing loads — while ground piles work (no picker on that path). Live
  instrumentation proved the `ResourceItems` dialog opens and STAYS ALIVE
  (`box=(886,13)-(1054,442)`, 1 item) but draws as a giant detached hex near
  the top of the screen, and clicks on it fall through to the map (selection
  churn then closes it via its own `OnMsg.SelectionChange`). Suspected
  `terminal:GetMousePos()` vs scaled-UI coordinate mismatch (~1.88 display
  scale maps the box back onto the true cursor position); 1080p error is small
  enough that it passed QA. Pack ruled out (all wrappers pass-through). Also
  affects the multi-resource unload and route pickers. Command-level workaround
  verified. **Wave-6 build candidate** (`Fix_ResourcePickerAnchor`); PT-39's
  depot control half is blocked on it (trade-rocket half unaffected).
  **User's release warning, recorded: this WILL draw false bug reports against
  the pack** — MOD_DESCRIPTION carries a draft-note for a "known vanilla
  issue" explainer (D02 precedent). Full forensics on the F76 entry.
  **Escalations (same day, later):** the multi-resource UNLOAD surface confirmed
  by play; environment pinned (fullscreen 3840×2160, UI Scale ~80-85%); and the
  broken picker can **HARD-LOCK the UI** (every MouseEvent erroring on a
  destroyed window in the modal/anim chain, `XWindow.lua:1154` — Alt-F4
  required, session lost). Live prototyping also established the dialog's own
  scale is applied AFTER Init (Init-time anchor conversion is a no-op — the
  repair belongs in/around UpdateLayout). **Process decision: no further live
  UI-internals prototyping on play sessions; F76 repair is an attended
  game-free leg task.**
- **PT-39 (2026-07-27, later): F74 → `tested`.** A landed TRADE rocket was
  fully refused by the RC Transport cursor ("treats it like normal terrain")
  AND by the route path — the route endpoint fell back to a ground position
  and the cargo was dumped at the pad, rocket untouched (the route handler
  only stores targets the guarded interaction check approves). Controls
  clean: ground-pile pickup + depot loading via route mode both work (the
  route path skips F76's broken picker for single-resource depots,
  `RCTransport.lua:466-476`). Cosmetic aside recorded: rovers clip through
  the landed event rocket's model.
- **Engine/tooling facts learned (also in the prompt + command table):**
  infopanel cheat buttons need `Platform.cheats = true` AND ride the game-time
  sync queue (dead while paused); tourists are 5% of applicants and the
  passenger filter EXCLUDES the Tourist trait by default (`initial_filter`);
  tourist stay is 5-10 sols; tourism rewards fire at Earth arrival; funding
  history is a 12-sol ring (`Funding.lua:86`); `CityStart` fires at
  map-generation time — use `InGameInterfaceCreated` for UI-ready work (TestKit
  console repair 2026-07-26); TestKit gained `SMRTest.Cls`.
- **Docs restructure:** completed playtests + evidence now live in
  `docs/PLAYTEST_ARCHIVE.md`; the checklist carries only un-run work
  (reporting protocol step 8 keeps it that way).
- **PT-14 (2026-07-27, after the session wrap): F61's premise FALSIFIED →
  CLOSED `wontfix` (user decision same day), community ask re-filed as D03.**
  The accept-colonists toggle is a **quarantine**: its OFF state is titled
  "Quarantined" and the rollover promises "Colonists are not allowed to enter
  or leave" (reused original-game T-ids — carried-forward wording);
  `Colonist:FindEmigrationDome` enforces it with the literal comment
  "quarantine, no one enters or leaves" (`Colonist.lua:2632-2634`). The lockdown
  the tester observed is designed behavior, and the shipped fix half-SUBVERTED
  it — worse, a use-case survey found scripted content that depends on the seal
  (Wildfire's dome-local infection spread `Traits.lua:1155-1173`; the RogueDome
  story bit FORCE-quarantines a renegade dome via `SetBuildingRogueState` →
  `Dome:SetUIInteractionState`; arrival routing's `is_welcoming_community`).
  **Resolution: `Fix_HomeDomeMigrationGate.lua` deletion STAGED (F10 precedent;
  needs a game-free leg, A/B numbers shift by one probe), and the real community
  ask — block move-ins WITHOUT locking commute/services — is filed as D03
  `Opt_ResidencyControl`:** a new per-dome "closed to new residents" policy row
  appended by post-wrapping `sectionDome:Init` (the infopanel section is a plain
  Lua class building rows imperatively — verified), gating
  `Community:CanAcceptNewColonists` + the arrival path, quarantine untouched.
  Full spec on the D03 entry; build queued for a game-free leg alongside D02.
- **PT-24 (2026-07-27, later): F36 → `tested`, both halves.** Geologist demand
  went **11 → 0 at the ExtractorAI grant with every other row identical**
  (before/after screenshots — the user reloaded a pre-tech save for the
  baseline, which also disproves over-exclusion since the pack was active both
  sides); multiple `CheatCompleteTraining` rounds across two universities
  graduated **38 engineers + 2 medics, zero geologists** (tallies from the
  universities' `trained_specialists`, captured in log
  Mars.exe-20260727-15.19.26). Setup gotcha found live and corrected in the
  checklist command table: **`CheatResearchAll()` skips undiscovered
  breakthroughs** (`Cheats.lua:84` discoverable-or-discovered gate) — grant
  directly via `UIColony:SetTechResearched("<Id>")`; PT-27's Biorobots route
  corrected to `ThePositronicBrain` in the same pass.
**ONE live prompt (updated 2026-07-28 — post-D06 build):**
- `docs/FABLE_NEXT_PROMPT.md` — playtest-standby assistance: the user plays,
  the session drives console instrumentation and processes results live.
  Rewritten 2026-07-28: PT-52 (D06 overhaul watch-and-judge) is the board
  centerpiece with assistant-side briefing notes; carries the queued A/B
  re-verify as pre-flight (module counts moved to 65/70 — probe numbers
  unchanged), the F76 avoidance rules, and the attended-sitting spec.
- Retired prompt files (each done and deleted/superseded):
  ~~OPUS_BUILD_PROMPT~~, ~~FABLE_QA_PROMPT~~ (2026-07-25),
  ~~FABLE_PLAYTEST_PROMPT~~ (merged into the one live prompt),
  ~~DRONE_INVESTIGATION_PROMPT~~ (2026-07-28 — its verdict, F77, and the
  D06 build all landed; the R1-R7 forensics it produced live on the BUGS
  DroneControl bullet, and PT-52 carries the live half).
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

**Open for the user after this session (updated 2026-07-26 late):** PT-01 longer
silence-watch only (cadence, tower warning lead AND necropsy all verified live;
the watchdog self-reports if the wedge recurs); rest of the merged-pack
checklist; PT-36/37/38 gates; MarsDebug attended [install] pass for wave-4/5.
**DONE since this record was written (commits 4310fb2..bc4e828, same day):**
PT-03 F45 retry PASS → F03/F44/F45/F50 `tested`; PT-45 PASS → F47 `tested`;
PT-46 PASS → F49(b) resolved no-defect; PT-01 tower-extended ~42h storm warning
banner verified live. Those commits flipped the BUGS.md detail headings but not
the index rows; the rows were synced in the follow-up doc-sync commit.
**PT-41 PASS (recorded 2026-07-26 later) → F66 `tested`:** shared hex stable, no
connector churn in the 11.48.31 log; demolishing one building left the survivor
connected ("became its own node but stayed connected … no weird visuals" — the
reclaim repair); plain-tile control clean.
**PT-07 first run FAILED the steadiness half (2026-07-27) → F12 second defect
found + repaired, A/B PENDING:** the Food warning fired correctly but the
notification was destroyed/recreated hourly (flash + voice replay). Live console
instrumentation attributed it to the surface city's own tick: the maintenance
loop and the food branch share the `"Food"` object key, and the maintenance
else-path deleted the food branch's entry each hour (voice plays only on
whole-notification creation — VoicePerObject false). Repair: maintenance loop
skips `"Food"` (the food branch owns the key). Full forensic record on the F12
entry. **A/B pair re-verified clean same day (2026-07-27):** baseline
Mars.exe-20260727-11.45.34 = 1 PASS / 58 FAIL / 11 SKIP / 0 ERROR; fixed
-11.47.09 = **59 PASS / 0 FAIL / 11 SKIP / 0 ERROR**, 66/67 active,
LowStorageWarning applied, zero errors from our files. Repair landed. **Open:
the user re-runs PT-07 on the repaired build (warning fires AND sits steady +
the Machine Parts half).** → **DONE 2026-07-27: PT-07 PASS in full, F12 `tested`**
(fires once / steady a sol / silent organic clear, both branches; see the
checklist archive).
**PT-38 DONE (2026-07-27) — D02's premise measured and CORRECTED; build
unblocked.** The dismissal window is **120,000 GAME-ms = 4 game hours**, NOT 2
real minutes: `GetTime()` = `GameTime()` because `GameTime` defaults true and
the NotWorkingBuildings preset doesn't override it (`NotificationPreset.lua:65-66,
:126-128`). Live timestamp wrappers measured three dismissal→return pairs at
148,805 / 161,755 / 132,056 game-ms — each 120,000 + time-to-next-attempt, every
in-window attempt observed BLOCKED. At ultra the re-nag is every few REAL
seconds — D02's case is stronger than premised. Suppression is per notification
id (fuel warnings independent — user-observed). **D02 (`Opt_AcknowledgedWarnings`
+ probe) is now buildable in the next build leg with the corrected spec.** Two
engine facts from the sitting: infopanel cheat buttons need `Platform.cheats =
true` (ObjCheat gate, `Network.lua:218-219`) AND their presses ride the
game-time sync queue — dead-looking while paused, firing on unpause.
**TestKit console repair (2026-07-26 later, user report: console dead on every
NEW save, fine on loads):** root cause — `Msg("CityStart")` fires from
`OnMsg.NewMap` DURING map generation (`Lua/_init.lua:18-26`), so the kit's fixed
2 s sleep auto-opened the console into a desktop the loading flow then replaced.
Repair in TestKit 00_TestCore.lua: also hook **`InGameInterfaceCreated`** (end
of `InGameInterface:Open`, `Lua/UI/InGameInterface.lua:388` — fires on BOTH new
games and loads, guarantees the UI exists), the open thread now waits on
`WaitLoadingScreenClose()` (`CommonLua/UI/LoadingScreen.lua:374`) instead of
guessing, and auto-open arms once per session entry so mid-session interface
reopens re-assert enable+shortcut without popping the console again. **Engine
fact: CityStart is a map-generation-time message, NOT a UI-ready message — use
InGameInterfaceCreated for anything that needs the in-game UI.**

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
