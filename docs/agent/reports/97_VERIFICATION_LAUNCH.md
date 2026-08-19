# 97 — verification launch (interlude, no lens): PRE-REGISTERED PREDICTIONS

**Written and pushed BEFORE the game opens** (`00_CHAIN_SPEC.md` §7,
`97_VERIFICATION_LAUNCH.md` §3.3; precedents `3f1856f`, `94eb508`, `d762964`).
Results are appended BELOW this block at close-out, never edited into it.

⛔ **This leg is RECORD-ONLY** (spec §4, links 3+) except a launch-blocking find.

---

## 0 · What this leg can and cannot reach, decided before it starts

The brief's five jobs split cleanly on one line: **the console**. Mod code runs in
a `LuaModEnv` whose blacklist removes `ConsoleExec` and `debug`
(`Mod.lua:1285`), and an unattended process has nobody at the keyboard — so
`DbgPackMod`, a forced `ReloadLua`, and a planted suspect mark **cannot be
driven from this session at all**. What *is* fully unattended is the TestKit's
own autorun harness (`95_AutoRun.lua`), which boots, builds a colony, runs
`SMRTest.RunAll()` and quits.

| job | reachable here? | why |
|---|---|---|
| 1 · core fix ①  (stale `update_suspect`) | ⭐ **yes, by falsifier** | see §2 — the suite already drives the live registry |
| 1 · core fix ② (`order` double-append) | ⛔ **no** | needs a SECOND Lua load in ONE process → `DbgPackMod`/Mod Manager → console or hands |
| 2 · suite by name, opt-in off | ✅ **yes** | junction pull (`EF-055`) reaches "opt-in absent" with no account-state edit |
| 3 · L2 reload prediction | ⛔ **no** | same second-load problem |
| 4 · the dialog | ⛔ **no**, and by rule | needs a planted mark from the console, **and** a screen event needs an attended witness (spec §7) |
| 5 · harvest | partial | §5 |

⇒ **Two legs, both unattended, and they are a designed PAIR:**

| leg | configuration | what only this leg gives |
|---|---|---|
| **L-A** | fix pack + TestKit, **opt-in junction pulled**, unpacked, cold boot | the suite with the opt-in absent — never measured |
| **L-B** | fix pack + TestKit + opt-in, unpacked, cold boot | a **by-name control** against `c47suite4` (2026-08-15, `80/0/16/0`), the last suite taken before `2f077e8` — and it **re-proves the junction restore** (`EF-055`'s measured failure mode) inside this sitting |

⚠️ **Labelling.** L-B's configuration matches the recorded baseline **and the
baseline is itself an autorun new-colony leg** (`c47suite1..4` all carry
`[SMRAUTO]`), so this one comparison is legitimate. L-A is **re-derived, not
compared** — its diff against L-B is the answer, not its diff against history.

---

## 1 · Configuration, recorded before the launch

- Rig: `A:\SteamLibrary\steamapps\common\Project Spark`, game **1.0.7.396349**.
- Mods present as junctions in `%AppData%\Surviving Mars Relaunched\Mods`:
  `SMR-BugFixPack`, `SMR-BugFixPack-TestKit`, `SMR-OptInPack`.
- Account state carries **all three enabled** (last launch, `MarsDebug…19.29.48`,
  ran `[CommunityOptInPack]` module lines). ⛔ Account state is **not touched** —
  `AccountStorage` is blacklisted and a Mod-Manager visit is owner time.
- Probe hygiene gate: `grep -rln "TEMPORARY" Code/ ../SMR-BugFixPack-TestKit/Code/`
  → **0 hits**, `doccheck` GREEN, `TESTKIT TREE: clean`.
- Harness arming: `Code/96_AutoRunFlag.lua` added to the **TestKit's** code list
  for the duration and removed at close-out. ⛔ Nothing is added to `Code/` of
  the pack under audit, and `metadata.lua` of the pack is not opened (**H-02**).
- `EF-056` pre-copy: **2** autosave-tagged files (header `autosave = true`, the
  tag-driven test, not the name) copied to `C:\Dev\_ref\EF056_precopy_20260819_97leg\`,
  **outside** the save directory:
  `Autosave Sol 406` `392cbaaa8cddd4a80d988a779791f3bc` ·
  `Autosave Sol 411` `2c645da1ab9fa0a070fd40028b3800b9`.
  Directory snapshot by name: **78** `.savegame.sav`. Reconciled after EVERY leg.

## 2 · ⭐ Job 1, fix ① — the falsifier this leg actually owns

`UpdateReport` (`TestKit/Code/56_Probes_Wave7.lua:140-153`) calls
`SMRFixPack.UpdateSuspects()` **against the live registry** and returns
`FAIL, "healthy build reports suspects: …"` if it is non-empty. The suite runs
~30 s after the city is live — **later than the report thread's single sample**,
which is why the defect could sit in the tree with the dialog never firing.

**Pre-fix, SaintBlessing's documented end state is `inactive` + a stale
`update_suspect`** (`2f077e8`, measured in `rs_ownertick` and `spowner`). So:

- **PREDICT: `PASS UpdateReport … healthy registry clean` in both legs.**
- ⛔ **A `FAIL` naming SaintBlessing (or any id) is LAUNCH-BLOCKING** and says
  core fix ① does not work.
- **PREDICT: zero occurrences of `update report:` in either log**, and no modal
  box. If one draws, an unattended leg has nobody to close it — that is itself
  the reading.
- **PREDICT: the SaintBlessing cycle appears in full** — `applied` →
  `inactive (no dome-colonists trait presets)` → `corrected N … of M`.

⚠️ **What this does NOT prove, stated in advance:** it proves the mark is clear
**at suite time**, not that it is clear at every instant, and it does not
exercise `ctx.heal`'s clearing site separately from `run_apply`'s. Naming the
path that ran is required (`97` §11).

## 3 · Job 2 — the suite, by name

**L-B (control, all three mods) — PREDICT identical to `c47suite4` by name:**

- `fix pack present: 75/75 fixes active` · `opt-in pack present: 8/8 modules active`
  · `save-rescue NOT loaded`.
- **80 PASS / 0 FAIL / 16 SKIP / 0 ERROR of 96.**
- The 16 SKIPs, by name: 8 `[install]` probes on `introspection unavailable
  (retail sandbox)` — `CaveInsNoDisasters`, `MilestoneCrash`, `TrainsToVoid`,
  `BrokenTrackSalvage`, `TrackSalvageWipe`, `LakeEntombment`, `GhostFarmOxygen`,
  `LowStorageWarning`; 2 behaviour SKIPs — `AnomalyCaveInMap`,
  `TechDescriptionBuilding`; 6 rescue probes — `SaveRescueCleanPass`,
  `SaveRescueStandDown`, `SaveRescueIdempotent`, `SaveRescueHealBounds`,
  `SaveRescueSelfClean`, `SaveRescueResidueTable`.
- ⇒ **Any FAIL here is a regression from `2f077e8` and is launch-blocking.**

**L-A (opt-in absent) — PREDICT:**

- `fix pack present: 75/75` · `opt-in pack NOT loaded — its probes SKIP (a
  separate, optional mod)` · `save-rescue NOT loaded`.
- The **8** probes of `60_Probes_Opt.lua` move `PASS → SKIP`:
  `AcknowledgedWarnings`, `ResidencyControl`, `MultipleSuns`, `CohortHousing`,
  `NoHomeless`, `DroneStatDials`, `OptionsMenuOptIn`, `OptionsMenuFixPack`.
- ⇒ **72 PASS / 0 FAIL / 24 SKIP / 0 ERROR of 96.**
- ⚠️ **The two `OptionsMenu*` probes are the ones to watch.** `OptionsMenuFixPack`
  reads THIS pack's options page, not the opt-in's — if it SKIPs on the other
  mod's absence it is over-guarded, and if it **FAILs** the pack's own options
  surface depends on a mod that will not be installed. Either outcome is a
  finding; a clean SKIP-because-opt-in-absent is the boring case.
- ⛔ **A FAIL in any of the other 88 is a finding about the SHIPPING
  configuration** and matters more than anything else in this sitting.

## 4 · Load-time predictions common to both legs

- **75 `applied` lines exactly**, one Lua load, no `148 = 2×74` shape (L2's
  two-load signature). ⛔ This is NOT the fix-② falsifier — one load cannot
  double-append. It is only a control that these legs are single-load.
- **0 `[LUA ERROR]`** (stop condition).
- `[SMRAUTO] armed` → `BEGIN` → `END` → `done`; no `TIMEOUT`, no `ERROR <stage>`.
- L-A additionally: **no `[CommunityOptInPack]` line anywhere**, and a
  `[mod] Loaded mod def` list of **2**, not 3 — that is the junction pull proving
  itself. L-B: the opt-in def and its 8 module lines are **back** — that is the
  restore proving itself (`EF-055`).

## 5 · Job 5 — what the pair can honestly harvest

Reachable: aggregate log volume per load in the shipping configuration (L4 owed
this a running number, not an archive count) · whether the pack emits anything a
player would see during a first-run boot · `0` vs non-zero error spam · the
per-leg wall clock as a first, crude aggregate cost signal for 75 modules.

⛔ **Declared out of reach and NOT attempted:** the shelter-precondition
co-occurrence (needs a colonist in that state) · the contended two-damage save ·
any console platform · any non-English run · packed-vs-unpacked (that is run B)
· anything needing the Mod Manager, Mod Options, or a second Lua load.

## 6 · Stop conditions carried from the brief

Any `[LUA ERROR]` → stop launching. `UpdateReport` FAIL → stop, launch-blocking.
Save directory not reconciling by name → restore from the pre-copy FIRST.
`doccheck` red → fix before committing.

---

# RESULTS — three launches, 2026-08-19 00:26–00:33

⭐ **The chain has opened the game.** Links 1–4 swept a tree that had never run;
`2f077e8`'s core file has now executed **three times** in retail Surviving Mars.

| leg | log | config | wall | verdict set |
|---|---|---|---|---|
| **L-A** | `archive/vl97a_Mars.exe-20260819-00.26.43.log` | fix pack + TestKit, **opt-in junction pulled** | 69.3 s | `72 PASS / 0 FAIL / 24 SKIP / 0 ERROR` |
| **L-B** | `archive/vl97b_…00.30.17.log` | junction **restored** — and see §R4 | 68.0 s | identical, probe for probe |
| **L-C** | `archive/vl97c_…00.32.17.log` | same, repeat | 66.3 s | identical, probe for probe |

All three: `[SMRAUTO] armed → BEGIN → END → done`, no `TIMEOUT`, no
`ERROR <stage>`. Save directory reconciled **by name after every launch**: 78
files before, 78 after, three times; both pre-copied autosaves still
MD5-identical (`392cbaa…`, `2c645da…`). Nothing was written, nothing deleted.

## R1 · ⭐ Job 1 — do the two core fixes work? **NOT YET, and the reason is precise**

⛔ **Neither fix is verified. The honest statement is not "no evidence" — it is
that this leg RAN one of the two fixed sites and cannot READ its result.**

**Fix ① (stale `update_suspect`).** The failing sequence **did execute**, and the
log proves it line by line (`vl97a`, lines 154 and 167):

```
[CommunityFixPack] SaintBlessing: inactive (no dome-colonists trait presets)
[CommunityFixPack] SaintBlessing: corrected 1 dome-colonists trait modifier label(s) of 2
```

That is `Fix_SaintBlessing.lua:121` — the **non-benign** latch, which sets
`entry.update_suspect = true` (`00_Core.lua:277`) — followed by `:113`
`ctx.heal()`, which is **one of the exact two sites `2f077e8` added a clear to**
(`00_Core.lua:292`). The gate then reads `fix pack present: 75/75 fixes active`,
so the heal restored the entry. ⇒ **The fixed line ran, in retail, and left the
module active.**

⛔ **But the mark itself is unreadable from here.** `UpdateSuspects` inspects
only entries whose status is `error` or `inactive` (`:527-536`), and this entry
ends **`active`** — so a stale mark would be **invisible to the very probe that
would report it**. `PASS UpdateReport … healthy registry clean` is therefore
**true and uninformative for fix ①**. The pre-registration (§2) expected that
probe to discriminate; it does not, and that is the correction this leg owes.

⇒ ⭐ **One console line settles it, and nothing else in this project can:**
`print(SMRFixPack.fixes.SaintBlessing.update_suspect)` → **expect `nil`**.

**Fix ② (`order` double-append)** needs a **second Lua load in one process**. The
`75 applied` lines and `75/75` prove these legs were single-load — a control, not
the falsifier. ⛔ Unreachable unattended: `ConsoleExec` and `debug` are
blacklisted from mod code (`Mod.lua:1285`) and nobody is at the keyboard.

⚠️ ⭐ **And the same reload is now known to test a third thing.** With link 2's
`data_edited` memo in place, a second load should take
`Fix_SaintBlessing.lua:116`'s early return — so the **benign latch that made the
mark visible in `rs_ownertick`/`spowner` should no longer happen at all**. Both
2026-08-17 core fixes and link 2's fix converge on the **same one reload**, which
is why the console leg below is worth its minute.

## R2 · Job 2 — the suite with the opt-in absent, BY NAME

`fix pack present: 75/75 fixes active` · `opt-in pack NOT loaded — its probes
SKIP` · `save-rescue NOT loaded`. **72 PASS / 0 FAIL / 24 SKIP / 0 ERROR of 96**
— the pre-registered figure, hit exactly.

⭐ **The by-name control is clean.** Diffed probe for probe against
`c47suite4_Mars.exe-20260815-15.20.44.log` — the last suite before `2f077e8`, and
itself an autorun new-colony leg on this build, so the comparison is legitimate
and **the only configuration difference is the opt-in**. Across all 96 probes:
**8 verdict changes, every one of them PASS → SKIP**:

`AcknowledgedWarnings` · `ClassicRockets` · `CohortHousing` · `DroneStatDials` ·
`MultipleSuns` · `NoHomeless` · `OptionsMenuOptIn` · `ResidencyControl`

⇒ **The other 88 probes hold their exact verdict across `2f077e8`.** No
regression from the core fixes is visible in the suite.

⚠️ **Two corrections to the pre-registration, both in the naming, neither in the
count.** §3 predicted those 8 would be the contents of `60_Probes_Opt.lua`.
**`ClassicRockets` skips and lives elsewhere**, and ⭐ **`OptionsMenuFixPack`
PASSES** — the pack's own options page stands up with the opt-in mod absent,
which was named in advance as the outcome that would matter. The opt-in-absent
SKIP set is these 8 names, not that file's list.

The other 16 SKIPs are the pre-existing set, unchanged: 8 `[install]`
introspection SKIPs, `AnomalyCaveInMap`, `TechDescriptionBuilding`, and the 6
`SaveRescue*` probes.

## R3 · What the pack does at load, measured rather than counted from an archive

- **All 75 modules register and apply in ≈0.57 s** (`Lua 0:00:18:418` →
  `:18:992` — markers that survive a loading screen, `EF-045`); the data-patch
  and heal work finishes by `:19:737`, so the pack's whole load-time footprint is
  **≈1.3 s**. ⭐ Every link recorded *"runtime cost of 75 modules together —
  never measured by anything."* This is that number, for the apply phase, in
  configuration A.
- **Log volume:** the pack writes **81 lines at load** (75 `applied` + 6 outcome
  lines) and **90 across the session**; the TestKit writes 225; the whole log is
  1,070 lines. ⇒ In the shipping configuration the pack is ~81 lines of a boot.
- **Player-visible surfaces: none fired.** `update report:` has **0** occurrences
  in all three logs and no dialog drew. ⚠️ ⛔ That is NOT the claim that nothing
  appears to a player (§11) — it is one configuration, one save-less boot.
- **The pack's non-`applied` line set is identical to the 08-15 baseline**, with
  exactly one difference, and it is the right one: `RainsDeadlock: … version
  1.0.1` then, **`version 1.0.0` now.** ⇒ The running game reports the frozen
  release version — a positive control on **H-02**.

## R4 · ⛔ THE COST THIS LEG INCURRED, AND IT IS AN OWNER ITEM

**Pulling the opt-in junction disabled that mod in account state, and restoring
the junction did not bring it back.** L-B and L-C both load its **def** (3 defs)
and run **0** of its module code; the gate line reads `opt-in pack NOT loaded`
across **two** relaunches. It is sticky and needs **an owner Mod-Manager tick +
restart**. On the checklist.

⭐ **This is `EF-055`'s measured limit reproducing — and it refines it twice.**
That fact attributed the failure to a round trip that *"spanned an owner
Mod-Manager visit"*; **there was no Mod-Manager visit here at all**, so the visit
is not the cause. And `EF-055` says a mod whose folder is missing is *"skipped
with a non-modal log line"* — ⛔ **`vl97a` carries no such line**: it vanished
**silently**, `Account storage loaded successfully` followed straight by two defs
instead of three. `account.dat` was rewritten at 00:30. The fact is amended.

⚠️⚠️ **This bears directly on the terminal gate.** `98_LAUNCH_REHEARSAL.md` runs
**run B by pulling the fix pack's junction** and installing the packed build. If
that pull drops `SMR_CommunityFixPack` out of `AccountStorage.LoadMods` the same
way, **the packed install will sit there loaded-as-def and never run**, and B
will read as a catastrophic failure that is really an account-state artifact.
⇒ **B must plan an owner tick after the swap, and must read the gate line before
believing any other number.** Not a defect in the pack — a defect in the planned
procedure, found before it cost the gate.

## R5 · Log lines this leg did not cause, reported rather than dismissed

`[LUA ERROR] Lua/Flight.lua:465 objects_to_mark` ×48 and `:479
objects_to_unmark` ×1 in L-A (×59 / ×1 in L-B). ⚠️ **The 48/1 split is identical
to the 08-15 baseline leg's**, and `PLAYTEST_HELP` records the same two lines
from **2026-08-03** as vanilla synthetic-map noise that retail swallows silently.
⇒ **Attribution: vanilla, aged ≥16 days, count reproduced.** ⛔ Not a dismissal
— they are `[LUA ERROR]` lines in a shipping-configuration boot and are stated
here with their age. The brief's stop condition (§10) was weighed and **not**
triggered: it exists to stop launching into a NEW broken state, and this is a
constant that predates the tree under test.

`MeteorFrequency: WATCHDOG — no meteor resolved for 99 game hours (thread ALIVE
but stuck); restarting onto vanilla's body` — present, **and present identically
in the 08-15 baseline**; it fires inside the suite window, i.e. probe-driven.
Unchanged, not new, not silently discounted.

## R6 · ⛔ Still unreached, and what each one needs

| item | what it needs |
|---|---|
| ⭐ **fix ①'s mark is clear** | ONE console read: `print(SMRFixPack.fixes.SaintBlessing.update_suspect)` → `nil`. Any launched game, ~10 s |
| ⭐ **fix ② (`order` dupes)** | a second Lua load in one process — `DbgPackMod(Mods.SMR_CommunityFixPack, false)` at the console, then `#SMRFixPack.order` |
| **L2's 2-false-FAIL reload prediction** | the same reload, with `SMRTest.RunAll()` either side |
| **link 2's `data_edited` fix** | the same reload — the 4 modules that went `inactive` on load 2 should now stay `active` |
| **the update-report dialog** | a planted mark from the console **and** an attended witness (spec §7 — a screen event may never be `tested-unattended`) |
| **the opt-in pack's own behaviour** | the owner's Mod-Manager tick (R4) |
| shelter-precondition co-occurrence · contended two-damage save · autosave-path load passes · uninstall/reinstall walk | bespoke saves; untouched, as declared |
| console platforms · non-English · packed vs unpacked | out of scope here; the last one is run B |

⚠️ **What no leg here can speak to:** this was TestKit-on and unpacked. It is run
**A** — information. **Run B remains the gate and remains unrun.**
