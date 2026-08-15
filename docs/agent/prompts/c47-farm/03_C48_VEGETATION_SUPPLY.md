# C48 — measure the vegetation seed-supply routing (UNATTENDED, owner cost zero)

**Authored 2026-08-15**, at the close of the `C47` attended sitting, by the
session that ran it. Paste into a fresh session. ⛔ **This prompt DELETES ITSELF
at close-out**; `02_AUDIT.md` remains the terminal audit for the whole folder and
burns it.

**Start with `git log --oneline -10` and `git pull` in all four repos.**
⭐ **FIRST ACTION: create a live todo list**, one item per Job, updated the moment
each changes state. The owner reads it to decide when to step in.

---

## 0. Read these first, in this order

| # | file | why |
|---|---|---|
| 1 | `docs/agent/STATE.md` | mandatory every session |
| 2 | **`docs/agent/bugs/C48.md`** | the case you are measuring — mechanism, the asymmetry, and what is NOT established |
| 3 | `docs/agent/bugs/C47.md` | the parent case, incl. the 2026-08-15 readings and **four agent corrections** |
| 4 | `docs/agent/WORKFLOW.md` — "Log review", "Co-runs" close-out, "Probe hygiene" | never-discount, the directory reconcile, arming rules |
| 5 | `docs/agent/facts/EF-051.md`, `EF-056.md`, `EF-014.md` | save hygiene, the autosave-rotation hazard (**it FIRED on 2026-08-15 — see below**), the pinned build |

⛔ **`C48` is a CANDIDATE. This leg measures. It does not fix, and it does not
decide whether anything should be fixed.**

---

## 1. What already exists — do not rebuild any of it

Everything below is committed and working. **Resurrect, do not rewrite**
(CHAIN_METHOD rule).

* **`97_C47Common.lua.txt`** — the shared harness (say/Try/Applicable/Load/
  ReadConditions/Guard/FreezeDiagnostic/ErrorWatchNote). `C47.Load(save, speed)`
  loads and **aborts if the speed does not take**.
* **`98_C48Veg.lua.txt`** — ⭐ **the instrument for this leg, already written,
  parse-swept and gate-proven.** Read it before changing a line of it.
* **`C47_ARM.ps1.txt`** — arming, with four modes and gates that point in
  different directions on purpose:
  * `arm-suite` — the probe suite only
  * `arm-sampler` — the unattended C47 sampler (5x, 2 s polling)
  * `arm-ride` — the ATTENDED ride-along; its gate **rejects** any payload that
    calls `LoadGame`/`SetGameSpeed`/`quit`/`SaveGame`
  * `arm-veg` — ⭐ **this leg**; unattended gate, plus a read-only check and a
    check that the payload actually scans `VegetationTaskRequester`
  * `disarm` — removes everything; **protects the permanent wave-11 probe**
* **`Code/61_Probes_Wave11.lua`** in the TestKit — PERMANENT, ships, tests no fix.
  ⛔ Never delete it. It asserts the C47 template pair as RATIOS.

**Run it:** copy `C47_ARM.ps1.txt` to a scratch `.ps1` and run
`.\C47_ARM.ps1 arm-veg`. Launch with
`& "c:\program files (x86)\steam\steam.exe" -applaunch 3215050`.
Logs land in `%APPDATA%\Surviving Mars Relaunched\logs`.

---

## Job 1 — stage, and protect the fixture

1. ⛔ **Stage a COPY.** `98_C48Veg.lua` expects **`C48STAGE.savegame.sav`**.
   Copy it from `C47FARM.savegame.sav` (MD5 `1B06B9BFAE8922562F5B8B64766F8584`,
   56,382,611 bytes — verify before and after; it must not change).
2. ⛔⛔ **`EF-056` FIRED ON 2026-08-15 AND THIS IS NOT THEORETICAL.** The attended
   sitting's autosave rotation **deleted the owner's `Autosave Sol 376`**. It was
   recovered only because the leg had byte-copied it first
   (MD5 `5175623063E4D02F332EBD485D67F043`, restored and verified).
   ⇒ **Byte-copy EVERY autosave out of the save directory before you launch**, and
   reconcile by name afterwards. The directory listing must enumerate the
   **directory**, not the `*.sav` glob (`EF-051`, the extensionless-file trap).
3. Record the full directory listing BY NAME before and after.

---

## Job 2 — the run

`arm-veg`, launch, wait, archive. The payload self-drives and quits.

⚠️ **Known constraints, all MEASURED on 2026-08-15 — do not re-derive them the
hard way:**

* ⛔⛔ **The colony's clock STOPS at `UIColony.day=385 hour=0`.** `IsPaused()=1`
  while `GetTimeFactor()` still reads the set speed; `PauseReasons` holds one
  entry rendering as **`XPauseLayer`**; `PopupNotification` is in the open-dialog
  registry. A popup opens at the sol boundary and nobody is there to close it.
  **No unattended run can pass day 385.** `C47.FreezeDiagnostic` detects it and
  closes the window; the usable span is **~15 game hours (0.64 sol)**.
* The payload runs at **1x** deliberately — the owner's attended session was at 1x
  and produced 13x the flap rate of the 5x unattended runs. ⭐ **Whether that gap
  is speed or something else is UNRESOLVED and is a named side-question**
  (see Job 4).
* Sampling is **200 ms**, not 2 s. The 2 s polling of every earlier leg smeared
  individual deliveries together, which is why delivery SIZE is still unknown.

Archive with **`git add -f`** — `.gitignore` line 2 is `*.log` and a plain
`git add` drops it silently. Name it `c48veg_Mars.exe-<stamp>.log`.

⭐ **Read the WHOLE log.** Report the `[LUA ERROR]` count explicitly even at zero.
⚠️ The suite launches carry ~48-60 lines of a pre-existing vanilla
`Flight.lua:465 objects_to_mark` signature in the synthetic autorun colony; the
three C47 sampler runs and the attended sitting carried **0**. Never discount a
line — report it with its age (owner rule 2026-08-01).

---

## Job 3 — predictions, COMMITTED BEFORE THE RUN

⛔ Non-negotiable, and the commit order is the evidence. Derive each, showing your
working, into `C48.md`, and commit **before** launching.

At minimum:

* **The headline.** Count of live `VegetationTaskRequester` objects inside each
  farm's serving radius. Predict the complaining farm (`OpenFarm#15779`, Potato ·
  Cover Crops · Wheat) holds **many** and the silent one (`OpenFarm#15974`) holds
  **few**. ⛔ If they are equal, the owner's density explanation is refuted and
  the `C47` A/B difference is unexplained again — say so, do not patch it.
* **The depots stay flat.** Predict both Seeds depots' stored amounts barely move
  while the farm's buffer sawtooths. ⛔ If a depot drains in step with the farm,
  the farm IS being fed from storage and `C48`'s premise is wrong.
* **The delivery-size distribution.** With the rig's carry dial at +2 a full trip
  is **3000**. Predict a wall of small values instead. State the number you
  expect and why.
* ⛔ **State what would REFUTE each**, and remember: a zero is `UNSAMPLED` unless
  the condition was sampled.

---

## Job 4 — ⭐⭐ THE SPEED LADDER. Co-equal deliverable with Job 3, not optional.

**Why did the owner's 1x attended session stall the farm 52% of samples while the
5x unattended runs stalled it 3.6% on the same save?** Four causes are already
**refuted**:

1. drone contention from player construction — owner: *"nothing but normal
   maintenance"*
2. run-to-run variance — the gap is far outside the 2/0/4 spread
3. crop cost per hex — the two farms **spent almost identically** (9,425 vs 9,520)
4. request disconnection while stalled — `UpdateRequestConnectivity` tests
   `ui_working`, the **player's on/off switch**, not the stall state

⭐ **The owner named the fifth and designed the test** (2026-08-15):

> *"my guess is the speed… do a variable speed test, fire at 1x speed for X min
> poll, then repeat for each speed level. I noticed that the frequencys would
> change on how often it ran out of stock depending on the speed I was on, it
> seems like the faster the speed is the less it runs out of stock."*

**It is already built** — `98_C48Veg.lua.txt` runs the ladder `1x → 3x → 5x → 20x`
in ONE process, on ONE colony, with the same drones and the same vegetation
offers, so the only variable between segments is the time factor. Two separate
launches would have carried every cross-run confound; this does not.

⛔ **Segments are equal in GAME time (3.5 game hours each), not real time**, and
that is forced: the colony's clock stops at day 385 hour 0 and starts at day 384
hour 8, so the whole budget is ~16 game hours regardless of speed. Equal
real-time segments would give 20x eight times the simulated exposure of 1x.
⇒ ⛔ **Read the per-game-hour columns in the `LADDER ROW` lines, never the raw
counts.** A rung with `took=false` is VOID; `complete=false` is PARTIAL; a rung
that never ran is UNSAMPLED, never zero.

**Commit the owner's prediction as theirs before running:** stalled-% falls
monotonically as speed rises. ⭐ **A refutation is worth more than a
confirmation** — it would mean the 52%-vs-3.6% gap has a cause still unfound.

⛔ Do not offer a sixth cause without a control. The owner pushes back on stated
root causes and has been right every time so far.

---

## Job 5 — record

* Append a dated section to `C48.md`: predictions **as committed**, then the
  readings, then the verdict per prediction (HELD / FAILED / UNSAMPLED).
* Re-emit every count from the archived log; **never inherit a tally**.
* Update `STATE.md`. **`docs/PLAYTEST_CHECKLIST.md` only if something needs the
  owner's call** — item 33 is currently answered and struck; do not invent a new
  one.
* ⭐ **Credit is owner's.** `C48` exists because the owner watched drones while
  the agent watched counters. Keep that on the entry.

---

## ⛔ What may NOT be claimed out of this leg

1. **That a drone CHOSE a vegetation offer over a depot.** This measures offer
   counts, depot stock and delivery sizes. Flat depots plus small deliveries is
   strong circumstantial evidence; it is not a read of the drone's decision.
2. **That anything is a defect.** "Colonists sweep the landscape for free seeds"
   is defensible design.
3. **Any rate without the confounds beside it** — cheats enabled, oversized
   terraforming speed-run, drone carry dial at **+2** (a trip is 3000, not 1000).
4. **Any screen or audio claim.** `tested-unattended` never covers those.

---

## Close-out

* `python tools/doccheck.py` GREEN; `--emit-counts` into STATE's build block.
* ⛔ **Disarm** (`C47_ARM.ps1 disarm`) — the probe-hygiene rule says the file
  lives in `Code/` only while its run is happening, and doccheck goes RED while
  armed, so you cannot commit until you disarm.
* ⭐ **`EF-051` reconcile: list the save directory BY NAME**, and account for
  every difference. **Restore any autosave the rotation ate**, as this session did.
* `git status` in BOTH repos. Commit, push (standing owner permission).
* **Delete this file.** `02_AUDIT.md` then audits the whole folder and burns it.
