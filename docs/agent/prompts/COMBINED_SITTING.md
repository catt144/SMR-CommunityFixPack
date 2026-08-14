# The ONE combined sitting — PT-20 redo (state 3) + D13 attended after-sweep + F102's minute

## ✅✅✅ IT RAN 2026-08-14. ALL THREE MOMENTS PASSED; D13 IS `tested`.

⛔ **The moments below are TAKEN.** This brief does not delete itself — PT-20 is a
standing per-era re-check and this is now its measured recipe — but nothing in it
is owed. **Results:** `agent/bugs/D13.md` (the 2026-08-14 block) ·
`agent/bugs/F102.md` · the PT-20 block in `PLAYTEST_CHECKLIST.md` ·
`archive/SESSION_LOG.md` 2026-08-14. **Logs:** `archive/cs_c1_*` · `cs_a1_*` ·
`cs_b1void_*` · `cs_b1_*` · `cs_b2_*` · `cs_zrestore_*` (+ prep `archive/csprep_*`).

**What a re-run must NOT inherit from the §5 predictions below** — they were
written for *these* fixtures and are now history, not a template: `removed 1566` is
`SPCONRT`'s number, and the F102 census is `SPWITCRT`'s one deposit. Re-derive
both. ⚠️ And read the three findings first: `EF-055`'s measured limit (a restored
junction may come back **not enabled** — verify the registry in-game before
measuring), the §10.5-vs-`report_text()` gap, and the two instrument defects
recorded on the D13 entry.

---

**Owner kickoff: open a session on this file and say "run the combined sitting".**
⭐ **PREP IS DONE AND MEASURED (2026-08-13, this file rewritten from it).** Two
unattended dry-run launches have already happened with the game closed and
nobody at the keyboard; everything in §1 and §2 below is a reading off their
archived logs, not a plan. **What is left is your ~30–45 attended minutes and
nothing else.**

This is a CO-RUN (WORKFLOW co-run protocol binds in full: live todo list updated
per item — the owner reads it to decide when to step in; R2 execution markers;
EF-050 verbatim savenames; EF-051 hold wording — "deleted, listing verified",
never "gone"; ⛔ EF-056 — byte-copy EVERY autosave BY NAME before any launch that
loads a copy of a real campaign; cheats are expected on playtest saves and
attributed, never re-litigated).

**Why one sitting:** STATE ② — these three owe owner-attended minutes and nothing
else on the release line does.

---

## 1. Conditions of the prep — MEASURED, all four gates GREEN

| | |
|---|---|
| staleness | fix-pack `8baac2f` · opt-pack `6170708` · TestKit `da432f8` · rescue `eb4cbd1` — all four clean working trees; the three with remotes are in sync (TestKit is local-only by decision) |
| PROBE SWEEP | `clean` at prep open over all four `Code/` trees (fix, opt-in, TestKit, rescue) |
| doccheck | GREEN — 74 modules / 75 `Code/*.lua` / 94 probes / 161 index rows |
| rig at open | game CLOSED · junctions on disk: fix pack, Test Kit, opt-in pack · ⛔ **rescue junction ABSENT** (pulled at the d13-rescue close-out, as designed — it is not a standing rig mod) |
| ⚠️ cheats | the rig has cheats enabled and every save here is a heavily-loaded playtest colony. **Intersection with these readings: NONE** — everything measured is a mod-authored persisted name, a label modifier, a registry count, a thread handle or an entity string, and no cheat writes or clears any of them |
| gate read at prep | `pack=74/74` · `opt-in=8/8` · `save-rescue=REGISTRY ABSENT` · load order `1:TestKit 2:FixPack 3:OptInPack` (EF-054) · dials `DroneSpeedDial=5x` `DroneCarryDial=+2` · all 7 toggles `true` |

**EF-056 — every autosave byte-copied BY NAME before the first launch**, each
verified identical after copying, and both MD5s match the values the d13-rescue
close-out recorded yesterday:

| autosave | bytes | MD5 |
|---|---|---|
| `Autosave Sol 311.savegame.sav` | 54,885,560 | `D5BCCF2CB758D5E5EA0706D671602AF5` |
| `Autosave Sol 311(2).savegame.sav` | 55,260,969 | `98F55E5C4F37A074CBA7671ED30E9EBD` |

Protected four re-hashed at prep open, all four unchanged: `CP15PT15`
`D2887D754C44134141B6CCC4C9020446` · `CP60RT` `7467573DB43EF0D61ED36FE50A131EE6`
· `PT35FIXTURE` `D721329D1EE18604B3D6C89401F74738` · `Autosave Sol 311`
`D5BCC…`. Save directory at prep open: **92 entries, 88 `.sav`**, listed by name.

### The two staged copies (byte copies, never an original)

| staged as | copy of | MD5 | why this save |
|---|---|---|---|
| **`CSHOST.savegame.sav`** | `SPWITCRT` (sol 311, 53.9 MB) | `14221BC2ABE9734ADE7EF9FAEC3085C4` | both packs, the campaign's own already-generated asteroid maps, and ⛔ **no `autosave` key in its header** — see §2.3. Serves moment **C** and moment **A** |
| **`CSSWEEP.savegame.sav`** | `SPCONRT` (sol 335, 54.4 MB) | `8A7639341C536816BFE18E35150AEDDE` | ⭐ **byte-identical to the witness the D13 verification matrix itself used**, so its native residue inventory is already a measured fact rather than a hope. Also no `autosave` key. Serves moment **B** |

---

## 2. ⛔ Three things prep found that this brief used to say wrongly

### 2.1 The rescue mod must be OUT for moments C and A, or PT-20 measures nothing

The earlier draft restored the rescue junction during prep and left it in for the
whole sitting. **That would have voided the PT-20 redo.** In state 3 both packs
are absent, so Save Rescue's per-pack stand-down does *not* fire — it would run
its full pass on the PT-20 host save about two seconds into the load and strip
the very residue PT-20 exists to prove is harmless, then put a dialog over the
owner's ten minutes of ordinary play.

⇒ **The rescue junction is restored BETWEEN moment A and moment B**, agent-side,
game closed, zero owner cost (EF-055 — a junction round trip does not cost the
owner their tick; measured a third time yesterday). This is one extra junction
operation and it buys back the whole point of the redo.

### 2.2 F102's fixture: there is **ONE** deposit, not three — and it is better than three

⛔ **There is no save called `Sylmacaink BH25`, and no save on disk carries the
`BlankAsteroidSlim_02` map** of the 2026-08-12 leg (all 88 `.sav` read at their
metadata headers). The earlier fallback was to respawn a D-type from the console.
**Prep found something strictly better and it is already in the owner's
campaign:** `CSHOST` loads **four** map slots, two of them asteroids
(`BlankAsteroidDonut_01`, `BlankAsteroidBranchOut_01`), and slot 3 carries **one**
subsurface Exotic Minerals deposit — `SubsurfaceDepositPreciousMinerals#2000010866`,
`revealed=true`, amount 14,935,000.

⭐ **Why one already-placed deposit beats three freshly spawned ones.** F102's fix
has two halves (`Code/Fix_ExoticDepositSign.lua`): a class-default retarget that
covers deposits placed *after* load, and an `OnMsg.LoadGame` `UpdateEntity` sweep
that covers deposits *already in the save*. The 2026-08-12 console-spawn leg
tested only the first half. This save tests the second, and prep measured it
firing:

```
[CommunityFixPack] ExoticDepositSign: 1 Exotic Minerals deposit(s) re-signed onto the clean entity
```

…with the deposit then reading `entity=SignRareMineralsDeposit`, and
`SMRFixPack.ListFixes()` printing `ExoticDepositSign [active]` verbatim into the
same log. ⇒ **Everything except "does the art actually render on screen" is
already measured.** The owner's minute is genuinely one minute: the rig parks the
camera on the deposit and selects it for them (measured: `ViewObjectAndChangeMap`
switched to `BlankAsteroidDonut_01` and left `SelectedObj` = that deposit).

⇒ **Checklist item 11's wording is corrected by this brief: one sign, not three.**

### 2.3 ⛔⛔ The dry runs deleted this sitting's own fixture, and EF-056 now says why

The first `CSHOST` was a byte copy of `Autosave Sol 311(2)`. Two dry-run loads
later it was **gone** — and so was the owner's held `Autosave Sol 311`, and so was
`SPWITC`.

**The mechanism, read out of the file rather than reasoned:** `autosave = true`
lives in the savegame's plain-text metadata header, `Copy-Item` carries it
verbatim, and `Autosave()`'s rotation enumerates *"every entry whose full metadata
says `v.autosave`"* — tag-driven, name-blind. Four autosave-tagged files were on
disk; the rotation wrote `Autosave Sol 311(3)` and deleted indices 2, 3 and 4.
⇒ **A byte copy of an autosave IS an autosave to the rotation.** EF-056 told this
project to pre-copy autosaves; it did not say that *staging a fixture FROM one
puts the fixture in the same firing line*. It does now (`EF-056`, amended
2026-08-13 with the header read and the arithmetic).

* ✅ **`Autosave Sol 311` restored byte-exact** from the pre-copy, MD5 `D5BCC…`
  re-verified. First time the pre-copy rule has been the thing that saved a file
  rather than a precaution nobody needed.
* ⚠️ **`SPWITC` was not pre-copied and is not recoverable** — a split-optins
  artifact, on no protected list. Inventoried, attributed, not filed.
* ⛔ **`CSHOST` was therefore re-staged from `SPWITCRT`**, which carries no
  `autosave` key, and a third dry run confirmed the F102 fixture is identical on
  it (same deposit handle, same re-sign line, same camera park).
* ⚠️ **Firing is NOT per-launch and must not be predicted.** The third launch, the
  same shape minutes later, wrote no autosave and deleted nothing. ⇒ **the
  runbook reconciles every autosave BY NAME after every launch** and restores from
  the pre-copies at `…/scratchpad/ef056/` (all three now held: `Sol 311`,
  `Sol 311(2)`, `Sol 311(3)`).
* ⭐ **Had this been found at the sitting instead of in prep, the owner would have
  been in the chair when moment C's save turned out not to exist** — the
  corun-batch-1 M1 failure, exactly.

### 2.4 A harness defect the dry run caught before the owner could pay for it

`CS.Flow()` decides whether to arm the watchdog and runs **before** `CS.Payload()`
sets `CS.attended` — so the unattended prep cell ran with **no watchdog** while
every gate line read GREEN. Same class as the `r1`-void ARM defect
(`D13_VERIFICATION.md` §4.6): a guard read earlier than it is written. Fixed at
file scope in `98_CSRun.lua.txt`, default flipped to `false` in
`97_CSCommon.lua.txt`, re-parsed GREEN. ⛔ It cost nothing because it was found
unattended; that is what the dry run is for.

---

## 3. The launch order — 4 attended launches, 2 Mod-Manager visits, 1 unattended close-out

⛔ **A Mod-Manager disable does NOT take effect until a FULL PROCESS RESTART**
(D13, measured 2026-08-10). Every quit below is a real quit to desktop, not a
return to the main menu — the half-disabled state (2) is what made the old
98-vs-98 comparison unreadable in the first place.

| # | cell | packs (Mod Manager) | rescue junction | payload loads | the moment | what the owner does |
|---|---|---|---|---|---|---|
| 1 | `c1` | **ON** | OUT | `CSHOST` | ⭐ **C — F102's minute** | look at the deposit the camera is parked on → then **Mod Manager: turn BOTH packs OFF** (Test Kit stays ON) → **quit to desktop** |
| — | *agent* | — | — | — | — | nothing to do; the junction stays out |
| 2 | `a1` | **OFF** (state 3) | OUT | `CSHOST` | ⭐ **A — the PT-20 redo, done RIGHT** | ~10 min ordinary play → in-game save as **`PT20REDO`** → load it back → **quit to desktop** (do NOT touch the Mod Manager) |
| — | *agent* | — | → **IN** | — | — | `CS_ARM.ps1 config rescue-in` — game closed, ~0.2 s, zero owner cost |
| 3 | `b1` | **OFF** (state 3) | **IN** | `CSSWEEP` | ⭐⭐ **B ①②③ — the D13 after-sweep** | **watch the screen from the launch** → read the report dialog → save as **`D13SWEEP`** → load it back (expect silence) → **Mod Manager: turn BOTH packs back ON** → **quit to desktop** |
| 4 | `b2` | **ON** | **IN** | `D13SWEEP` | ⭐ **B ④ — the stand-down** | one dialog, one look, **quit** |
| — | *agent* | — | → **OUT** | — | — | `config rescue-out`, then cell `zrestore` unattended — the close-out control |

⚠️ **Moments B and B④ need the owner watching from the launch**, because the
dialog arrives about 2 s after the load completes (~30 s after the launch) and
`WaitMessage` writes **no log line in either direction**. The agent fires each
launch only when the owner says they are looking.

⛔ **If a cell's configuration is wrong, the game closes itself within seconds of
reaching the menu and before anything is measured.** That is the config gate, not
a crash. It happens because a reading taken in the wrong mod state is worse than
no reading (`unattended-2` run 1 took six of them). Call the agent; nothing is
broken.

---

## 4. The measure-moments — instrument · verdict words

| # | moment | instrument | verdict words | what it closes |
|---|---|---|---|---|
| **C** | F102's minute (packs ON, rescue OUT) | the owner's **eyes** on a deposit the rig has already located, switched maps to and selected — plus, already in the log, the `re-signed` sweep count, `entity=SignRareMineralsDeposit`, and `ExoticDepositSign [active]` | **"sign renders: yes / no"** · **"deposit selectable: yes / no"** | checklist item 11's local (safety) half. ⛔ It closes the SAFE half only — the cure stays unverified and ships disclaimered by the owner's 2026-08-12 ruling |
| **A** | PT-20 redo, state 3 (both packs off **and** restarted) | rig-side loads/saves/log reads; ⛔ the `pack=0/0 opt-in=0/0` gate line printed BESIDE every reading, and again on each of the owner's own loads | the PT-20 block's re-check re-run, its result stated as **"supersedes / confirms the old 98-vs-98"**; **0 `[LUA ERROR]`**; every pack-naming log line accounted (the state-3 six-line inventory, D13 entry 2026-08-10, is the template) | PT-20's standing per-era re-check, and the owner's decision 6 of 2026-08-10 |
| **B** | ⭐⭐ D13 attended after-sweep, same state-3 window, rescue IN | **eyes** — the one instrument unattended mode cannot have (the terminal audit ruled both dialogs permanently unsampleable unattended) — plus the pass's own log line and a full by-name residue read 5 s after every load | ① **"report dialog RAISED: yes / no"** + its text vs the frozen spec §10.5 · ② the `pass: removed N …` line quoted verbatim · ③ after save+reload: **"removed 0 AND no dialog: yes / no"** · ④ after re-enable+restart: **"stand-down dialog ONCE: yes / no"** + `removed 0` | ⛔ **a clean run here is what finally grants D13 `tested`** — the last thing blocking the release line. Any KEEP name missing or REMOVE survivor ⇒ stop the leg, record verbatim, route |
| **D** | optional capture passes that ride these same launches — see §6 | per `CAPTURE_SITTING.md` | per that brief | checklist item 24, in part |

---

## 5. Predictions — written BEFORE the sitting, off the prep runs

⛔ Committed in this file's own commit; `git log` it. Provenance per row (R3 bans
a blanket claim over a table).

### Cell `c1` — F102

* **P-C1** MEASURED-in-prep, expected to repeat: `pack=74/74` · `opt-in=8/8` ·
  save-rescue **REGISTRY ABSENT**; load order `1:TestKit 2:FixPack 3:OptInPack`.
* **P-C2** MEASURED-in-prep: exactly **1** subsurface Exotic Minerals deposit,
  on map slot 3 (`BlankAsteroidDonut_01`), handle `2000010866`, reading
  `entity=SignRareMineralsDeposit`.
* **P-C3** MEASURED-in-prep: `ExoticDepositSign: 1 … re-signed onto the clean
  entity` and `ExoticDepositSign [active]` both in the log.
* **P-C4** ⛔ **UNSAMPLED AND ONLY THE OWNER CAN SAMPLE IT: does the new sign
  RENDER.** No log line exists for this in either direction. "It did not render"
  is a result, and it would be a genuine F102 finding.
* **P-C5** INFERRED: no Save Rescue dialog of any kind at this moment — the mod's
  code is not in this process at all.

### Cell `a1` — PT-20 redo

* **P-A1** the gate reads `pack=0/0` **and** `opt-in=0/0` with both registries
  reported ABSENT, and `MODORDER` shows the Test Kit alone. If it does not, the
  restart did not happen and the cell stops itself.
* **P-A2** SOURCE (D13 entry, 2026-08-10 state-3 inventory): the pack-naming
  lines in this log are accounted for by mod-def loads, the items load, the
  save's own recorded mod list, one `Unpersist missing permanent:
  Mod/SMR_CommunityFixPack`, and `This savegame tries to load Mod Community Fix
  Pack … which is present, but not loaded`. ⚠️ The `Unpersist` line is **NOT**
  diagnostic of an uninstall — it also occurs in state (2) with the pack fully
  loaded. It is only readable next to the `pack=0/0` gate line.
* **P-A3** **0 `[LUA ERROR]`** across the whole process, including the owner's
  save and reload. This is PT-20's actual verdict.
* **P-A4** INHERITED-then-MEASURED: the save still carries its leftovers while
  all this happens — prep read `CSHOST` at **reserved_at 1260 · payload_set 4 ·
  closed_to_new_residents 4 · both Drone dial modifiers present · F48 latch true
  · F35 modifiers 0**. ⭐ That is the point of the leg: *the residue is present
  and the save behaves normally anyway.*
* **P-A5** ⚠️ **What this cell CANNOT settle:** the old 98-vs-98 was an error
  **count** comparison from the F86 era, and F86 is repaired (PT-58 measured the
  same shape at zero). A clean state-3 run **supersedes** that comparison; it
  does not reproduce it. Say "supersedes", not "confirms", unless errors appear.

### Cell `b1` — ⭐⭐ the D13 after-sweep, on a NATIVE witness

⛔ **This is not a re-run of the `r2` matrix cell and its numbers will not match
it.** `r2` ran on `RESCUEDMG`, which had three REMOVE rows, a dead `Meteors`
thread and the D10 KEEP witness **manufactured** into it. `CSSWEEP` is untouched:
it carries only what the shipped packs really wrote. **That makes this the first
run of the artifact against exactly what a real player's save looks like**, and
it is why the predicted heals are zero.

* **P-B1** gate: fix **ABSENT** · opt-in **ABSENT** · `save-rescue 1/1 active`;
  four mods in `MODORDER`.
* **P-B2** the automatic `OnMsg.PostLoadGame` pass fires — **not** `force = true`
  — and prints:
  ```
  pass: removed 1566 entries (SMRFixPack_DroneCarryDial=1, SMRFixPack_DroneSpeedDial=1,
    SMRFixPack_ack_notworking=4, SMRFixPack_closed_to_new_residents=11,
    SMRFixPack_loop_version=1, SMRFixPack_no_homeless=11, SMRFixPack_payload_set=4,
    SMRFixPack_reserved_at=1533)
    | kept 1 track re-order latch
    | heals: meteors 0, rains restarted 0, rains ended 0 | skipped 1
  ```
  ⚠️ **`reserved_at` may read 1534 and the total 1567**, and either is a pass.
  Prep read this save with the pack RUNNING, and the live pack writes that field
  during play — the exact mechanism `D13_VERIFICATION.md` §5 correction 1 records
  (a live 1336 against a pack-absent 1335 on the sibling witness). ⛔ **This is
  why the reads are handle sets and not counts.**
  ⭐ **The arithmetic reconciles to the archived `r2` line to the unit**, which is
  the strongest evidence that this prediction is derived and not guessed:
  `1533+4+4+11+11+1+1+1 = 1566`, and `r2`'s `1617` is exactly that plus its three
  manufactured rows (`shelter_try=25`, `rocket_fuel_key=25`, `fixed_loop=1`).
* **P-B3** ⭐ **heals: `meteors 0, rains restarted 0, rains ended 0`.** MEASURED
  basis: the `Meteors` thread is ALIVE in this save, so the ambiguity rule
  declines to touch it (spec §10.4 — a live thread whose body may be a captured
  pack-era body is not detectable from Lua, and restarting a healthy thread would
  re-roll its timer forever); and the rains entry carries `loop_version` **without**
  `fixed_loop`, which the spec calls "already migrated by the pack: thread
  untouched, stamp removed". ⛔ **A meteor or rain re-roll here would be the
  finding**, not the pass.
* **P-B4** **KEEP survives:** `SMRFixPack_F48_StationConnectors` still `true`.
  ⚠️ **D10 (`SMRFixPack_F35_*`) is expected ABSENT on this save and that is not a
  failure** — prep measured zero F35 modifiers, exactly as the D13 matrix found
  before it planted a synthetic one. The condition was SAMPLED there, on a
  declared-synthetic witness; it is not re-sampled here and this brief does not
  claim it is.
* **P-B5** ⛔ **the dialog RAISES with the removal text** (frozen spec §10.5:
  "Removed …", "Kept on purpose …", "You can remove Save Rescue whenever you like
  — it stores nothing in your save"). **UNTESTED UI, and the owner's eyes are the
  only instrument that will ever adjudicate it.**
* **P-B6** after the owner saves `D13SWEEP` and loads it back **in the same
  process**: `removed 0`, heals `0,0,0`, and ⛔ **NO DIALOG AT ALL** — with both
  packs absent nothing stands down, and a load that finds nothing is silent by
  design (this is what replaces the latch the spec rejected).
* **P-B7** **0 `[LUA ERROR]`**, as in all nine of yesterday's launches.

### Cell `b2` — the stand-down

* **P-B8** gate: `pack=74/74` · `opt-in=8/8` · `save-rescue 1/1`.
* **P-B9** `pass: removed 0 …`, preceded by `thread heals skipped — the Community
  Fix Pack is installed and heals its own`.
* **P-B10** ⛔ **exactly ONE stand-down dialog, once per session and not per
  load** (`stand_down_told`, `10_SaveRescue.lua:542`). A second dialog on a second
  load is a defect; so is none at all.

### Cell `zrestore` — the close-out control

* **P-Z1** `74/74` · `8/8` · save-rescue ABSENT; `DroneSpeedDial=5x`,
  `DroneCarryDial=+2`, all seven toggles `true` — the owner's account exactly as
  they left it after four junction round trips.

### 5.1 The two fixtures' residue, read in prep — MEASURED, packs loaded

⚠️ Provenance on the whole block: read with **both packs running**, so
`reserved_at` is a live number and may drift by one or two against a pack-absent
read. Every other row is static. Logs archived this commit.

| row | name | `CSSWEEP` (moment B) | `CSHOST` (moments C+A) |
|---|---|---|---|
| — | objects scanned | 4516 | 3911 |
| D5 | `SMRFixPack_reserved_at` | **1534** | 1260 |
| D6 | `SMRFixPack_shelter_try` | 0 | 0 |
| D7 | `SMRFixPack_payload_set` | 4 | 4 |
| D8 | `SMRFixPack_rocket_fuel_key` | 0 | 0 |
| D12 | `SMRFixPack_ack_notworking` | 4 | 0 |
| D13 | `SMRFixPack_closed_to_new_residents` | 11 | 4 |
| D14 | `SMRFixPack_no_homeless` | 11 | 0 |
| D15a | `SMRFixPack_DroneSpeedDial` | ⭐ present, label `Drone` | present |
| D15b | `SMRFixPack_DroneCarryDial` | ⭐ present, label `Consts` | present |
| D3 | `SMRFixPack_loop_version` | `1.0.1` on `rains['normal']`, `activation_thread` VALID | same |
| D4 | `SMRFixPack_fixed_loop` | **nil** — already migrated by the pack ⇒ no rain restart | same |
| — | `Meteors` thread | **valid** ⇒ no meteor restart, one `skipped` instead | valid |
| D10 | `SMRFixPack_F35_*` (KEEP) | ⚠️ **0 — absent, as on every save we hold** | 0 |
| D11 | `SMRFixPack_F48_StationConnectors` (KEEP) | ⭐ `true` | `true` |
| D1/D2 | `MeteorLatch` / `FirstAsteroidPrefabs` | `1.0.1` / `false` with the packs on — ⛔ the ENGINE drops these on any pack-less load; never report their absence as a removal | same |

⇒ **The two Drone dial modifiers are the headline and they are NATIVE here.**
They are the only residue that keeps *changing the game* after an uninstall, and
moment B is the first time the artifact will be seen taking them off a save that
really acquired them, with a human watching.

---

## 6. What rides along free — the capture passes (OPTIONAL, drop any of them)

Checklist item 24 wants most of `CAPTURE_SITTING.md` on this sitting, and the
fold-in really is free: that brief's ordering exists to buy a both-mods-OFF frame
and a both-mods-ON frame **without** paying a restart per pair, and this sitting
already contains both, on the same save.

| capture pass | rides | note |
|---|---|---|
| **A** (`F13-before`, `F14-before`) — both mods OFF | cell `a1` | same save (`CSHOST`) as the "after" below, which is what makes the pair a pair |
| **B** (`F13-after`, `F14-after`, `F19-after`) — both mods ON | cell `c1` | ⚠️ chronologically first; the pair is still a pair |
| **C** (opt-in Mod Options surfaces + ⭐ the free "does a toggle take effect without a restart" measurement) | cell `b2` | the strongest material the project has; `CAPTURE_SITTING` says take your time |
| **D** (`multiplesuns`, `modmanager`) | `c1` or `b2` | ⛔ if a second Artificial Sun is not already standing, **drop the shot** |
| **E** (`F102-signs`) | ⭐ cell `c1`, **already framed** | the camera is parked and the deposit selected before the owner looks. ⛔ Not a before/after: the "before" is a hard freeze on hardware we do not own |
| **F** (`listfixes-*`) | `c1` or `b2` | ⚠️ **prep narrowed this but did not answer it.** `ListFixes()` output reaches the LOG (measured, §2.2). Whether anything appears on the in-game CONSOLE is still the open question, and it is what `MOD_DESCRIPTION.md:487-488` claims. If nothing appears: record "no visible output", do not hunt |
| **G** (preview backdrops) | any cell | 4–6 wide vistas, no UI, leave dead space |

⛔ **Every one of these is droppable and none of them may push a measure moment.**
If the sitting is running long, the three moments finish and the capture passes go
to a second sitting — that is what `CAPTURE_SITTING.md` is still for.

---

## 7. What may NOT be claimed out of this sitting

* Not **"F102 is cured"** — never. Two clean local runs and a third verify SAFETY
  only; the freeze has never reproduced on hardware we own, and only an affected
  player's report moves that entry (F102 "What a future session must not
  conclude").
* Not **"the three signs render"** — there is **one** deposit on this fixture.
* Not **"clean after uninstall"** without the registry-absent gate line beside the
  reading (four-OFF-states doctrine).
* Not **"D13 is `tested`"** unless the dialogs were actually seen and said so —
  that grant is the whole point of the attended half, and `tested` still means a
  pass at the keyboard (WORKFLOW).
* Not **"D10's KEEP condition was sampled here"** — it was not; §P-B4.
* Not **"the meteor / rains heals work"** — this fixture cannot exercise them and
  predicts zero. The manufactured-witness run of 2026-08-13 remains the only
  evidence for those two, and it says so.
* Not **"gone"** for any staged save while the `EF-051` hold stands (Steam Cloud
  is ON by the owner's deliberate, temporary choice): **"deleted, listing
  verified"**.
* Not a **cost figure** the log cannot support. The heartbeat line measures the
  attended minutes; report cost **against promise**, never as an achievement.

---

## 8. Close-out (rig-side, same session)

1. `config rescue-out`, then cell `zrestore` unattended — restore the standing
   config (both packs + kit junctions IN, rescue junction OUT) and read it back:
   gates `74/74` + `8/8`, dials `5x`/`+2`, seven toggles.
2. **DISARM GATE** — both instruments deleted, both `metadata.lua` lines removed,
   `PROBE SWEEP: clean` over all four `Code/` trees, `git status` in **both**
   repos (a stranded TestKit edit is a finding to route, never something to
   quietly commit).
3. Staged saves **deleted, listing verified BY NAME** — `CSHOST`, `CSSWEEP`,
   `PT20REDO`, `D13SWEEP` — and the save directory reconciled by NAME against the
   92-entry prep baseline, never against a count.
4. ⛔ **EF-056 reconciliation AFTER EVERY LAUNCH, not only at the end** (§2.3):
   every autosave re-hashed by name against the three pre-copies at
   `…/scratchpad/ef056/`; anything the rotation ate is restored byte-exact and
   said so. Firing is timer-driven and unpredictable — reconcile, never reason.
5. Whole-log sweep of every archived log (F99 `:805` and C45 `Quantum Comet`
   watches; ⛔ every unexplained line reported VERBATIM with its age — "not caused
   by our leg" is an attribution verdict, never a dismissal).
6. Archive every cited log with `git add -f` in the **same commit** as the claims
   (`.gitignore` line 2 is `*.log`; a plain `git add` drops it silently).
7. `SESSION_LOG`; checklist items ticked (11 local half; PT-20; D13 → `tested`
   **if earned**); STATE ② cleared and ③ (MOD_DESCRIPTION ×2(+1)) promoted to NEXT.

## 9. Agent runbook

Parked instruments — `docs/agent/prompts/combined-sitting/`: `97_CSCommon.lua.txt`
· `98_CSRun.lua.txt` · `CS_ARM.ps1.txt`. ⛔ They live in `Code/` only while a
launch is happening (probe hygiene rule 5) and die in the commit that records the
answers.

```
# once: materialise the arm script WITH A BOM (PS 5.1 reads a no-BOM .ps1 as ANSI)
# then, per launch:
CS_ARM.ps1 config rescue-out|rescue-in     # only the RESCUE junction ever moves
CS_ARM.ps1 arm <cell> [savefile]           # cells: dry c1 a1 b1 b2 zrestore
& "c:\program files (x86)\steam\steam.exe" -applaunch 3215050
# ... the owner's moment ...
CS_ARM.ps1 disarm
```

The ARM gate reads everything back off disk, **counts** each `metadata.lua`
listing and fails on anything but exactly one (the `r1`-void lesson), cross-checks
every `CS.*` the payload calls against the harness definitions, refuses to launch
if a pack junction has been pulled (that would take the mod out of the Mod
Manager list entirely and the owner could not turn it back on), and checks the
staged save exists — which for cell `b2` is also the typo check on the name the
owner typed into the in-game save dialog. If `D13SWEEP` is missing, **list the
directory and re-arm with the real name**; do not guess.

**This brief does NOT delete itself** — PT-20 is a standing per-era re-check and
this is now its measured recipe. Strike the moments as they are taken.
