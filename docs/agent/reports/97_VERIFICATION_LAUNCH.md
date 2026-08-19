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
