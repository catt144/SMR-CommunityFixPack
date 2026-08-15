# C47 — build the probe set and measure the Open Farm seed starvation (UNATTENDED, owner cost zero)

**Authored 2026-08-15.** Paste into a fresh session. ⛔ **This prompt DELETES
ITSELF at close-out** (chain rule); prompt `02_AUDIT.md` is the terminal audit
and deletes the folder.

**Start with `git log --oneline -10` and `git pull` in all four repos.** This
file goes stale the moment another session commits. **Staleness anchor: the
2026-08-15 evening session that filed `C47` and deleted `Fix_DistressPopupPause`.**

⭐ **FIRST ACTION, before any work: create a live todo list** (one item per Job
below) and **update it the moment each item changes state**. The owner reads
that list to decide when to step in. A stale list is a defect in this leg.

---

## 0. Read these first, in this order

| # | file | why |
|---|---|---|
| 1 | `docs/agent/STATE.md` | mandatory every session |
| 2 | `docs/agent/bugs/C47.md` | **the whole case** — the two numbers, the sibling comparison, and §2026-08-15 "HOW TO MEASURE IT" which this prompt implements |
| 3 | `docs/agent/FIX_POLICY.md` §1.4, §2, §3a | only if you end up proposing code — **you are NOT authorised to build a fix in this leg** |
| 4 | `docs/agent/WORKFLOW.md` — "Log review", "Co-runs" close-out | the never-discount rule and the directory reconcile |
| 5 | `docs/agent/facts/EF-051.md`, `EF-056.md`, `EF-014.md` | save hygiene, the autosave-rotation hazard, the pinned build |

⛔ **`C47` is a CANDIDATE, not a ruled defect.** This leg measures. It does not
fix, and it does not decide whether anything should be fixed.

---

## 1. What the owner has already done

They were playing when this was commissioned and were asked to leave a fixture:

* ⭐ **The named manual save is `C47FARM`** (owner, 2026-08-15), taken **while
  the symptom was live** — so the staged copy carries the state to be measured.
  Verify it exists by name before anything else; ⛔ do not substitute another.
* ⭐ **The fixture is TWO Open Farms**, and their crop selections are known:
  * **farm A** — Potato · Cover Crops · Wheat ⇒ mean **367** seeds/hex
  * **farm B** — Cover Crops · Leaf Crops · Wheat ⇒ mean **233** seeds/hex,
    photographed at `Stored Seeds` **3.7/5** (partial, mid-drain)
  ⛔ Crops ROTATE round-robin per placement
  (`ThreeHarvestTypesBuilding.lua:40-60`), so **use the MEAN of the selected
  crops, never the dearest** — see the correction section at the end of `C47`,
  which fixes this entry's own first arithmetic. Expected runway: **~3.4 ticks
  (≈1.0 h) for farm A, ~5.4 ticks (≈1.6 h) for farm B**.
* ⭐ **The owner could not tell which farm triggers the voice line** — they
  cycle fast, especially at high game speed. **Answering that is a named
  deliverable of this leg**, and it is free: the counters are per object.
* ⛔ **A named save, deliberately NOT an autosave** — `EF-056`: a byte copy of
  an autosave is still an autosave to the game's rotation and has destroyed
  owner autosaves twice. Working from a named save removes that hazard entirely.
* The game is **closed**.

⚠️ **Still do the `EF-051` close-out reconcile** at the end (directory listing
by NAME, before and after), and **still pre-copy any autosave you touch**.

---

## Job 1 — the STATIC probe: does the live game agree with our source read?

**Where:** the Test Kit repo, `C:\Dev\SMR-BugFixPack-TestKit`, a new wave file
(`Code/61_Probes_Wave11.lua`) registered the same way as `59_Probes_Wave10.lua`.
Add it to that repo's `metadata.lua` `code` list. ⚠️ Probe count moves 95 → 96;
re-emit with `--emit-counts`, never hand-type.

**What it asserts** — that the four numbers `C47` derived from source are the
numbers the running game actually has. This is the cheap, permanent half: it
turns the entry's table into something the suite re-checks on every future run,
and it FAILS loudly if a patch ever changes them.

Read from the **class defaults / templates at runtime**, not from an instance
(so it passes on any save, including the synthetic autorun colony):

| assert | expected | source it is checking |
|---|---|---|
| `OpenFarm` template `consumption_max_storage` | **5000** | never set ⇒ `HasConsumption.lua:44` default |
| `OpenFarm` template `vegetation_interval` | **3** | `Data/BuildingTemplate/OpenFarm.lua` |
| `ForestationPlant` template `consumption_max_storage` | **10000** | set explicitly |
| `ForestationPlant` template `vegetation_interval` | **20 or absent** | class default `TerraformingBuilding.lua:365` |
| `const.ResourceScale` | **1000** | `ResourcesFormatting.lua:6` |
| `g_Consts.DroneResourceCarryAmount` | **1** | `__const.lua:639-640` |
| Vegetable presets' `placement_consumption_amount` | Herbs 100 · Rapeseed 100 · Spinach 200 · Wheat 400 · **Potato 600** | `Data/Vegetation.lua` |

⭐ **Derive the tick length in the probe rather than asserting a literal**:
`MulDivRound(vegetation_interval, const.HourDuration, 10)` — and assert the
**ratio** OpenFarm:Forestation is 1:6.67 and the storage ratio is 1:2. A ratio
survives a rebalance patch that moves both; a literal does not.

⛔ **PASS text must state what it does NOT prove**: that these are template
numbers, not evidence of any player experience.

---

## Job 2 — the SAMPLER: what actually happens over time

**Where:** the same Test Kit repo, but a **separate, non-suite file** — it is a
long-running instrument, not a pass/fail probe. Follow the payload pattern the
`unattended-3` C39 leg used (log tag in brackets, e.g. `[C47]`, staged-save name
printed on load — see `docs/archive/u3c39_Mars.exe-20260815-01.36.41.log:188`
for the shape). ⛔ Do **not** add it to the shipped Test Kit `code` list
permanently; it is armed for this leg and disarmed at close-out.

**What it must collect:**

1. **Census at load** — every `OpenFarmBase` and every `ForestationPlantBase` on
   the map, by handle: selected crop(s), `consumption_amount`,
   `consumption_max_storage`, `building_update_time`, initial
   `consumption_stored_resources`, and whether it is `working`.
2. ⭐ **Event counters via `OnMsg`, not via wrappers** — this is the whole point
   of the method and it patches nothing:
   ```lua
   function OnMsg.AddNotificationObject(notification, obj)
       -- filter: notification.id == "NotWorkingBuildings"
   end
   function OnMsg.RemoveNotificationObject(notification, obj)
   end
   ```
   Count **adds** and **removes** per object. The add/remove pair IS the flap
   count, which is the number the owner's complaint is about.
   (Route: `BaseBuilding.lua:137-139` → `UpdateObjectInNotification` →
   `NotificationUI.lua:209` / `:220`.)
3. **Voice-eligible adds** — apply the preset's own rule yourself rather than
   guessing: `VoicePerObject = true` and `VoiceCooldown = 60000`
   (`Data/NotificationPreset.lua:638-655`), so an add produces a queued voice
   for **that object** at most once per 60 **real** seconds. Report both raw
   adds and voice-eligible adds.
4. **Buffer sampling** — `consumption_stored_resources` on a fixed cadence, per
   farm. Enough resolution to see it hit zero between ticks.
5. **A report function** (`C47.Report()`) that emits the whole table through the
   Test Kit's `Note`/ModLog path. ⛔ Bare `print()` does **NOT** reach the log
   — recorded harness fact, and it has cost this project a leg before.

---

## Job 3 — PREDICTIONS, written and committed BEFORE the run

⛔ **Non-negotiable, and it is the house rule that makes a result mean
anything.** Write these into the entry (or a scratch file committed first), then
run. A prediction written after the fact is worthless.

Derive each from `C47`'s arithmetic, showing your working:

* Buffer **5000** against a mean tick cost of **~1467** (farm A) and **~933**
  (farm B) ⇒ predict the sampled minimum reaches **0** on both, and that
  **farm A empties measurably sooner than farm B**. ⭐ That A-vs-B ordering is a
  free internal control — same building type, same colony, same drones, only
  the crop mix differs — and if it does NOT hold, the drain model is wrong.
* ⛔ Do **not** predict off the all-Potato worst case (5×600); no farm here is
  configured that way.
* Predict roughly **how many adds per sol** per farm from the tick rate
  (0.3 h tick ⇒ 80 ticks/sol at 24 h) and the drone refill rate (1000/trip).
  ⚠️ State the assumption you are making about drone travel time and mark it
  **INFERRED** — you do not know it, and the run measures it.
* ⭐ **Separate the banner from the voice.** With only **two** farms the
  `VoicePerObject` amplifier caps at **2 queued voices per 60 real seconds**, so
  voice volume alone cannot explain "endless". Predict that the **banner**
  add/remove churn (no per-object cooldown) is the dominant term, and report the
  two counts separately. ⚠️ Check whether `QueueVoice`'s cooldown is real or
  game time and use the right clock — at high game speed the two diverge wildly,
  which is exactly the owner's observed condition.
* ⭐ **The control prediction:** the `ForestationPlant` in the same colony,
  same instrument, should show **near-zero adds** and a buffer that stays well
  off the floor. **If the control also flaps, the whole C47 story is wrong** and
  that is the single most valuable outcome this leg can produce. Say so in
  writing beforehand.

---

## Job 4 — run the leg

Reuse the established unattended harness — `Code/95_AutoRun.lua` +
`Code/96_AutoRunFlag.lua` in the Test Kit (arm by adding the flag file to the
`code` list; the file's own header documents both opt-in routes), and the
staged-save load pattern from the C39 leg.

1. ⛔ **Stage a COPY** of the owner's named save (never the original). Record
   the copy's name and its MD5 before and after — the C39 leg proved
   byte-identical either side because it never saves; this leg must do the same.
2. Load the copy, let it settle, run the sampler for a real span of game time.
   **Run long enough to cross several sols** — the flap rate per sol is the
   headline number.
3. Emit the report, quit. Archive the log into `docs/archive/` with
   `git add -f` — ⛔ `.gitignore` line 2 is `*.log`, so a plain `git add` drops
   it silently and the commit still looks complete.
4. ⭐ **Read the WHOLE log**, not just your own lines. Never silently discount a
   line (owner rule, 2026-08-01): report unexplained lines with their age.
   Report the `[LUA ERROR]` count explicitly, even when it is zero.

---

## Job 5 — record

Append a dated section to `docs/agent/bugs/C47.md` with:

* the predictions **as committed**, then the readings, then the verdict per
  prediction (HELD / FAILED / UNSAMPLED — `UNSAMPLED` if the condition never
  occurred; ⛔ "refuted" requires the condition was **sampled**, not merely that
  a count was zero);
* the control's numbers beside the subject's, always;
* every count re-emitted, never inherited;
* whether the entry's `~80×` source ratio survived contact with the game.

Then update `STATE.md`, and **`docs/PLAYTEST_CHECKLIST.md` if — and only if —
something needs the owner's call.** ⛔ Owner decisions never live only in agent
docs. If the leg produces no decision, say so; do not invent one.

---

## ⛔ What may NOT be claimed out of this leg

1. **That a player sees a banner or hears a voice line.** Counting
   `AddNotificationObject` measures *that the game raised the event and queued a
   voice*. It does not measure a screen or a speaker. That half needs the
   owner's eyes and ears — the difference between `tested-unattended` and
   `tested-attended` under the vocabulary the owner set on 2026-08-15.
2. **That this is a defect.** No code comment ties the two fields; it is an
   unset field, not a self-contradiction. "Farms are meant to be supply-hungry"
   remains a defensible reading and the leg may support it.
3. **That the flap rate generalises.** ⚠️ **Cheats are enabled on this rig** and
   the colony is an oversized terraforming speed-run. The template numbers are
   playstyle-independent; the *rate* is not. Name the confound beside the number.
4. **Anything about other buildings** from a farm sample. Ten templates leave
   the storage at default; only Open Farm also tuned its cadence. Do not widen.

---

## Close-out

* `python tools/doccheck.py` GREEN before any doc commit; `--emit-counts` into
  STATE's build-state block.
* Disarm the sampler (remove it from the `code` list); leave the Job 1 probe in.
* ⭐ **`EF-051` reconcile: list the save directory BY NAME** before and after,
  and account for every difference. The owner's own saves are the contract.
* Commit across the repos that changed; push (standing owner permission).
* **Delete this file** and hand to `02_AUDIT.md`.
