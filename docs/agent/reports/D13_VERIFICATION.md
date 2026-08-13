# D13 — the Save Rescue verification matrix (junction-pull configs)

**What this is.** The unattended verification of the standalone save-rescue
artifact (`C:\Dev\SMR-CommunitySaveRescue`) against the frozen spec, §10 of
`D13_EXPOSED_SET.md`, whose §10.9 is this matrix's contract. Chain
`d13-rescue` prompt 4. Precedent floor: the `split-optins` matrix
(SESSION_LOG 2026-08-12) — cell banners as identity, an ARM gate that reads
everything back off disk, config gates BEFORE any load, **predictions written
before the run**, deviations chased to ground before filing.

⛔ **§1 (predictions) was committed BEFORE the first launch.** That commit is
the proof; `git log` this file. §2 is written after, and every row carries its
own provenance tag (MEASURED / SOURCE / INFERRED) — R3 bans a blanket claim
over a table.

## 0. Conditions of the run

| | |
|---|---|
| staleness | fix-pack `2fee4be` · opt-pack `98c37ea` · TestKit `da432f8` · rescue `aaff837` — all four clean, all synced to their remotes |
| ⛔ item 26 | **MEASURED DONE.** The owner ticked "Save Rescue" and restarted at 11:16 today: `Mars.exe-20260813-11.16.44` line 302 `[CommunitySaveRescue] SaveRescue: ready`, line 313 `Loaded mod items for: … SMR_CommunitySaveRescue`. The checklist line was still open; the log is the measurement |
| PROBE SWEEP | `clean` at open over all four `Code/` trees (fix, opt-in, TestKit, rescue) |
| owner cost | predicted **zero minutes** — nobody at the keyboard; game closed at open, Steam client up (it is the launcher) |
| ⚠️ cheats | the rig has cheats enabled and the fixture lineage (`PT35FIXTURE` → `SPSTAGE` → `SPCONRT`) was built on cheated playtest colonies. **Intersection with these readings: NAMED per cell in §2** |
| EF-056 | both autosaves byte-copied by name before launch 1 — `Autosave Sol 311.savegame.sav` (MD5 `D5BCCF2CB758D5E5EA0706D671602AF5`) and `Autosave Sol 311(2).savegame.sav` (MD5 `98F55E5C4F37A074CBA7671ED30E9EBD`), each verified identical after copying |
| EF-051 | **HOLD stands** (Steam Cloud ON). Staged saves close out as "deleted, listing verified", never "gone" |
| protected four | `CP15PT15` `D2887D754C44134141B6CCC4C9020446` · `CP60RT` `7467573DB43EF0D61ED36FE50A131EE6` · `PT35FIXTURE` `D721329D1EE18604B3D6C89401F74738` · `Autosave Sol 311` `D5BCCF2CB758D5E5EA0706D671602AF5` — re-read at close-out |

## 1. The fixtures, and which witness is native and which is manufactured

⛔ **The derivation's claim is only that the pre-rewrite population exists in
the wild — never that we hold one.** Both halves are named here so §2 can never
be read as though a synthetic witness were a native one.

**`RESCUESTAGE.savegame.sav`** — byte copy of `PT35FIXTURE.savegame.sav`.
MEASURED byte-identical to `SPSTAGE` (`D721329D1EE18604B3D6C89401F74738`), so
the suite tally is comparable with the audit-recounted baseline, which was taken
on exactly these bytes. The suite world is FIXED across the tally cells: the
`[state]` probes read the colony and a tally on another world is not comparable.

**`RESCUEWIT.savegame.sav`** — byte copy of `SPCONRT.savegame.sav`, the
`split-optins` cell-(e) contract round-trip save (MD5
`8A7639341C536816BFE18E35150AEDDE`). ⭐ **It is the strongest native witness
this project holds**, and its contents are already MEASURED — the FixtureCarry
dump at `archive/spe_Mars.exe-20260812-18.53.42.log:536-593` and the INVROW
block at `:342-407` describe these exact bytes:

| row | name | NATIVE in `RESCUEWIT` | source |
|---|---|---|---|
| D15a | `SMRFixPack_DroneSpeedDial` | ⭐ PRESENT on label **Drone**, `prop=move_speed percent=200` — written by the real `Opt_DroneStatDials` through its own Apply path at a non-base dial | spe `:502` |
| D15b | `SMRFixPack_DroneCarryDial` | ⭐ PRESENT on label **Consts**, `prop=DroneResourceCarryAmount amount=2` | spe `:504` |
| D5 | `SMRFixPack_reserved_at` | **1336 objects** of 3411 scanned | spe `:573` |
| D7 | `SMRFixPack_payload_set` | 3 objects | spe `:577` |
| D12 | `SMRFixPack_ack_notworking` | 4 objects (1 native + 3 forced by cell (e)) | spe `:583` |
| D13 | `SMRFixPack_closed_to_new_residents` | 11 domes (4 native + 7 forced) | spe `:581` |
| D14 | `SMRFixPack_no_homeless` | 11 domes (2 native + 9 forced) | spe `:585` |
| D3 | `SMRFixPack_loop_version` | `= "1.0.1"` on the **normal** rains entry, whose `activation_thread` is ALIVE | spe `:550` |
| D11 | `SMRFixPack_F48_StationConnectors` | ⛔ KEEP witness — `= true` on `UIColony` | spe `:506` |

⇒ **8 of the 11 REMOVE names and 1 of the 2 KEEP names are NATIVE.** Three
REMOVE rows and one KEEP row are not, and are **MANUFACTURED by a declared
probe** on the byte copy, then saved as `RESCUEDMG.savegame.sav` and reloaded
before anything is claimed (R4 — the manufacture is only real if it survives
the round trip):

| row | name | why it must be manufactured | how |
|---|---|---|---|
| D6 | `SMRFixPack_shelter_try` | reads 0 in every save we hold | write the timestamp onto N labelled `Colonist`s |
| D8 | `SMRFixPack_rocket_fuel_key` | legacy — the current pack deletes it itself, so only a save that never loaded under it carries one | write onto the `DroneControl`s |
| D4 | `SMRFixPack_fixed_loop` | ⭐ **the pre-rewrite-lineage row.** No save in the folder carries it: every save the current pack has loaded was migrated and latched by the pack | set `= true` on the **normal** entry, which is the one with a LIVE `activation_thread` — the exact shape §10.4's legacy-loop heal detects |
| — | dead `Meteors` thread | `Meteors` is ALIVE in every save we hold (spe `:564`) | `DeleteThread` it before the save. ⚠️ **Whether deadness survives the round trip is UNKNOWN and is itself a measurement** — if it comes back alive, the meteor restart is UNSAMPLED and §2 says so rather than claiming it |
| D10 | `SMRFixPack_F35_<label>` | ⛔ **UNSAMPLED — the KEEP headline has never been observed.** `label_modifiers` was NOT INSPECTABLE to the FixtureCarry probe (spe `:591`), so its presence in `RESCUEWIT` is genuinely unknown | the instrument **censuses first**. Native → used as-is and said so. Absent → planted with the exact id shape `90_SaveSanitizer:84` writes and declared SYNTHETIC. **Either way the condition is SAMPLED** — absent ≠ refuted |

## 2. The matrix — predictions, written before the run

Eight launches. Every cell's configuration is set by JUNCTION presence
(`EF-055`: a pull is a real uninstall, D13 state (4); the account and the
owner's ticks are untouched). ⛔ **Every cell's gate line reads the pack
registries — `n/n` or REGISTRY ABSENT — before anything else is believed**
(four-OFF-states doctrine), and the config gate STOPS the run on a mismatch.

| # | cell | junctions | save | what it settles |
|---|---|---|---|---|
| 1 | **r0** | fix + opt + kit | `RESCUESTAGE` | the standing-config control |
| 2 | **r1** | fix + opt + kit + **rescue** | `RESCUESTAGE` | the artifact beside both packs — the measurable no-op |
| 3 | **r2pre** | **kit only** | `RESCUEWIT` | the before-inventory and the manufacture |
| 4 | **r2** | kit + **rescue** | `RESCUEDMG` | ⭐ the rescue case |
| 5 | **r2b** | kit + rescue | `RESCUECLEAN` | idempotence, in a FRESH process |
| 6 | **r3** | **kit only** | `RESCUECLEAN` | the artifact leaves nothing |
| 7 | **r3z** | **none** | — | the zero-mods log-clean read |
| 8 | **r-restore** | fix + opt + kit | — | the close-out control |

### (r0) standing-config control — the artifact is not installed yet

* **P0.1** `fix pack present: 74/74` · `opt-in pack present: 8/8` · save-rescue
  **REGISTRY ABSENT**, and `rawget(_G, "SMRSaveRescue") == nil`.
* **P0.2** load order `1:SMR_CommunityFixPackTestKit 2:SMR_CommunityFixPack
  3:SMR_CommunityOptInPack` (`EF-054` — opt-in wrappers OUTERMOST).
* **P0.3** ⭐ **the suite re-measurement STATE records as PENDING: 78 PASS /
  0 FAIL / 16 SKIP / 0 ERROR of 94.** The audit-recounted 78/0/10/0 of 88 plus
  the six new rescue probes SKIPping `save-rescue mod not installed (separate
  mod — not a failure)`. ⚠️ The queued `FactionFundingCheck` PASS→SKIP repair
  was deliberately NOT taken, so it should still read PASS.
* **P0.4** the residue inventory of the baseline world, by name — the control
  that proves the artifact's install and removal leave the rig's normal state
  untouched (re-read identically at r-restore).
* **P0.5** ⚠️ **a `Couldn't find mod SMR_CommunitySaveRescue from your account
  storage.` line is predicted PRESENT** — `EF-055`'s measured route: the id
  stays in the account, the folder is gone, `ModMessage` appends non-modally.
  It is the standing cost of "the artifact is not a standing rig mod", and it
  is routed to the owner rather than absorbed.

### (r1) the artifact beside both packs — per spec, a measurable no-op

* **P1.1** `74/74` · `8/8` · `save-rescue present: 1/1`.
* **P1.2** four mods loaded; the rescue's position in the load order is
  RECORDED, not predicted (it is the account's enable order, `EF-054`).
* **P1.3** ⭐ **the automatic `PostLoadGame` pass prints its zero:**
  `pass: removed 0 entries | heals: meteors 0, rains restarted 0, rains ended 0`.
  §10.9(3): an absence of lines cannot be told from an absence of the pass, so
  the zero must be printed, not inferred.
* **P1.4** the stand-down is recorded for BOTH packs, and the stand-down dialog
  is raised **once per session, not per load** (§10.1). ⚠️ **This is untested
  UI** — `WaitMessage` on an RT thread after a 2 s settle. Predicted: it raises,
  and no `[LUA ERROR]` names any of the three mods.
* **P1.5** suite **84 PASS / 0 FAIL / 10 SKIP / 0 ERROR of 94** — the six
  rescue probes all PASS.
* **P1.6** ⛔ **the interlock test.** The six probes drive forced passes; they
  are supposed to touch only synthetic state (`WithGlobals`, `g_RainDisaster`
  stubbed false, `MainMap = false`). **Prediction: the residue inventory taken
  before `RunAll` and after it is IDENTICAL — handle sets, not counts.** A
  moved handle set means a probe reached the live colony.
* **P1.7** the version-skew witness is quoted verbatim from the log rather than
  asserted: `list derived over Community Fix Pack cdbcd9d / Opt-In Modules
  e17586b (2026-08-13)`.

### (r2pre) kit only — the before-inventory and the manufacture

* **P2p.1** all three registries **ABSENT**.
* **P2p.2** the before-inventory reproduces §1's native table **by handle set**,
  not by count. ⭐ **Two rows are a real first measurement, not bookkeeping:**
  `SMRFixPack_MeteorLatch` and `SMRFixPack_FirstAsteroidPrefabs` are predicted
  **ABSENT** — §10.2 calls D1/D2 unreachable because a mod-registered GameVar is
  dropped on any load without its registering mod (`persist.lua:136-142`), and
  that has only ever been argued from source. This load is the pack-absent load
  that tests it. ⚠️ **A `MeteorLatch` absence here is NOT evidence the artifact
  removed anything** — the artifact never looks at it.
* **P2p.3** D10 census answers a question nothing has answered: how many
  `SMRFixPack_F35_*` modifiers this save carries. Native → used. Zero → planted
  and DECLARED synthetic.
* **P2p.4** after `SaveGame` → `LoadGame` of `RESCUEDMG`, every manufactured row
  reads back identically. ⚠️ **`IsValidThread(Meteors)` after the round trip is
  the open one** — predicted FALSE (the manufacture holds), and if it reads TRUE
  the meteor restart is recorded UNSAMPLED.

### (r2) the rescue case — packs pulled, artifact + kit, the AUTOMATIC path

⛔ The pass is sampled through `OnMsg.PostLoadGame`, **not** through
`force = true`. The probe surface exists because the rig's normal config stands
the pass down; here the packs are genuinely absent, so the real trigger fires
and the forced call would be the weaker evidence.

* **P2.1** fix ABSENT · opt ABSENT · `save-rescue present: 1/1`.
* **P2.2** the pass's `by_name` counts match the before-inventory row for row —
  `reserved_at` ≈1336 · `payload_set` 3 · `ack_notworking` 4 ·
  `closed_to_new_residents` 11 · `no_homeless` 11 · `shelter_try` and
  `rocket_fuel_key` as manufactured · `DroneSpeedDial` 1 · `DroneCarryDial` 1 ·
  `loop_version` 1 · `fixed_loop` 1.
* **P2.3** heals: `rains_restarted = 1` (the normal entry — its live
  `activation_thread` plus the D4 stamp is exactly the legacy-body shape),
  `rains_finished = 0` (`g_RainDisaster` is falsy in this save),
  `meteors = 1` **if and only if** P2p.4 held the thread dead.
  **Cost, stated: one rain re-roll and one meteor re-roll on a fixture copy.**
* **P2.4** ⛔ **read back BY NAME: every REMOVE name ABSENT.** ⚠️ §10.2's
  disclosed incompleteness says an object in no label is not visited — a
  colonist riding a rocket. **If `reserved_at` survivors appear, they are
  checked for cargo membership BEFORE anything is filed as a defect.**
* **P2.5** ⛔ **KEEP survives: the `SMRFixPack_F35_*` modifiers are present and
  unchanged by id, and `SMRFixPack_F48_StationConnectors` is still `true`.** A
  missing KEEP name stops the leg (README).
* **P2.6** restarted threads are VALID: the normal entry's new
  `activation_thread`, and `Meteors` if it was restarted.
* **P2.7** the report dialog raises with the removal text (the second half of
  the untested UI), and `RESCUECLEAN.savegame.sav` is written.

### (r2b) idempotence, in a fresh process

* **P2b.1** the automatic pass over the cleaned save finds **nothing**:
  `removed 0 | heals: meteors 0, rains restarted 0, rains ended 0`. ⭐ This is
  what replaces a latch, and the mechanism is that step 4 of the previous pass
  removed the detector (D4) the rain heal reads. A fresh process also resets
  `stand_down_told`, so nothing is carried over from r2.
* **P2b.2** **no dialog** — a load that finds nothing is silent.
* **P2b.3** every REMOVE name still absent, both KEEP names still present.

### (r3) the artifact leaves nothing

* **P3.1** all three registries ABSENT; `rawget(_G,"SMRSaveRescue") == nil`.
* **P3.2** ⛔ **residue-zero, first half:** the field/modifier/global inventory
  finds **zero names containing `SaveRescue`** anywhere — no object field, no
  label-modifier id, no entry field, and no `SMRSaveRescue*` key in
  `PersistableGlobals`.
* **P3.3** the cleaned state is unchanged by the artifact's own removal: every
  REMOVE name absent, both KEEP names present.
* **P3.4** ⛔ **residue-zero, second half** (`EF-047` — absence only from the
  archived file): **zero `[CommunitySaveRescue]` lines** in this cell's log
  after archiving.

### (r3z) the zero-mods read

* **P3z.1** no `Loaded mod def` line for any of the four mods; **zero**
  `[CommunitySaveRescue]`, `[CommunityFixPack]`, `[CommunityOptInPack]` and
  `[SMRTest]` lines; zero `[LUA ERROR]`.
* **P3z.2** four `Couldn't find mod … from your account storage.` lines — the
  same `EF-055` route as P0.5, now for all four ids. ⚠️ The process is closed
  gracefully (`taskkill` without `/F`) so the tail flushes; if it does not, the
  cell reports what the log actually contains and the absence claim leans on
  (r3) instead.

### (r-restore) the close-out control

* **PR.1** `74/74` · `8/8` · save-rescue ABSENT; load order back to the three.
* **PR.2** the owner's dials and toggles exactly as they left them —
  `DroneSpeedDial=5x`, `DroneCarryDial=+2`, all seven toggles `true`
  (`archive/sprestore_Mars.exe-20260812-19.02.50.log:240-242`).
* **PR.3** the r0 residue inventory of the baseline world re-reads identically.

## 3. What may NOT be claimed out of this matrix

* Not **"clean after uninstall"** without the registry-absent gate line beside
  the reading (four-OFF-states doctrine).
* Not **"residue-zero"** without (r3) BOTH halves — the kit-instrumented
  inventory AND the archived-log read.
* Not **"the save is repaired"** beyond what (r2) read back BY NAME. "Vanilla
  threads alive" means the handle-valid read plus the one-shot bound, not a
  feeling.
* Not **"gone"** for any staged save while the `EF-051` hold stands.
* Not **"the meteor restart works"** unless P2p.4 actually held the thread dead
  across the round trip. An unsampled condition is not a negative result.
* Not **"D1/D2 are removed"** — the artifact never touches them; their absence
  is the engine's GameVar mechanism and is attributed to it.

## 4. Measured results

*(written after the run — see §2 of the same name in the commit that carries the
archived logs)*
