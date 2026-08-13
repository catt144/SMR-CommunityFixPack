# Chain prompt 4 — the unattended verification matrix (junction-pull configs)

**Read `README.md` first — binding chain rules apply.** Staleness check (all
repos incl. the artifact's), todo list. **Owner NOT needed at the keyboard;
the game and Steam must be FREE** — if a process is up, stop and report.
Precedent floor: the split-optins matrix (SESSION_LOG 2026-08-12) — cell
banners as identity, ARM gate reading everything back off disk, config gates
BEFORE any load, predictions written before the run, deviations chased to
ground before filing.

## Preconditions, in order, none skippable

1. **PROBE SWEEP** over all Code/ trees — clean or declared.
2. ⛔ **EF-056:** byte-copy EVERY autosave in the save folder, BY NAME, before
   the first launch that loads any save. List them in the log and the record.
3. **EF-051 HOLD stands** unless STATE says the owner re-unticked: staged
   saves close out as "deleted, listing verified", never "gone".
4. Instruments arrive as parked `.txt` in this folder → copied live by a
   script FILE (C11), ARM gate reads mode + files back OFF DISK, refuses to
   launch unarmed. Watchdog on every launch.
5. Every cell's config is set by JUNCTION presence (EF-055: pull = real
   uninstall, state 4; restore = clean reinstall; account untouched). ⛔ The
   four-OFF-states doctrine: every cell's gate line reads pack registries
   (`n/n` or REGISTRY ABSENT) before anything else is believed.

## The matrix (prompt 3's Notes refine cells; predictions written FIRST)

Design the cells against the spec's promises; the floor is:

* **(r0) standing-config control** — both packs + kit, artifact junction
  ABSENT: baseline `74/74` + `8/8` and the suite tally re-read (quote the
  audit-measured 78/0/10/0 of 88 unless prompt 3 re-baselined — then quote
  ITS number); proves the artifact's install/remove leaves the rig's normal
  state untouched before anything else runs.
* **(r1) artifact beside both packs** — per spec (no-op or report-only;
  whatever the spec promises is the prediction). Suite unchanged.
* **(r2) the rescue case** — a DAMAGED/residue-carrying witness (per prompt
  3's fixture notes: a byte copy of a pre-rewrite-lineage save if one exists
  BY NAME, else synthetic residue written by the declared probe on a
  PT35FIXTURE copy — say which, and what each witnesses) loaded with BOTH
  packs' junctions PULLED, artifact + kit only: clean pass runs, then read
  back — every REMOVE name gone, every KEEP name intact BY NAME, restarted
  threads valid, one-shot bound held (R4: save → reload → re-read; a second
  artifact pass must find nothing to do).
* **(r3) the artifact leaves nothing** — pull the artifact's junction too;
  load (r2)'s cleaned save with the KIT ONLY: registry-absent gates for all
  three mods, field/GameVar inventory reads zero artifact names; then ONE
  true zero-mods launch (kit junction pulled as well) for the log-clean
  read — that log answers ABSENCE claims per EF-047 after archiving.
* **(r-restore) control** — all standing junctions back (both packs + kit;
  artifact stays out — it is not a standing rig mod), gates re-read, dials
  and toggles as the owner left them.

Every load: EF-050 verbatim savenames; speed set/read-back; INVDIFF-style
before/after comparisons on HANDLE SETS, not counts, for every name the spec
promises to touch or spare.

## Close-out, all of it verifiable

Archive EVERY log in the SAME commit as the claims it backs (`git add -f`,
R8 — including any log another actor produced that you cite). Staged saves:
deleted, listing verified BY NAME; autosave pre-copies reconciled BY NAME;
protected-save MD5s re-read (`CP15PT15`, `CP60RT`, `PT35FIXTURE`,
`Autosave Sol 311` — the standing four). DISARM: instruments out of Code/,
junctions restored, TestKit tree clean, `git status` in ALL repos. Whole-log
sweep per WORKFLOW: unexplained lines verbatim with age; F99
`TrackElement.lua:805` and C45 `invalid pos` watches; a missing archived log
is an automatic finding. Update the D13 entry + STATE to the measured truth.
Append your outbox to `05_FABLE_AUDIT.md` `## Notes from upstream`: the
matrix table (predicted vs measured, log per cell), every deviation with its
chased mechanism, the fixture provenance, close-out inventory, owner-minutes
actually consumed (predicted zero). Delete this file in the same commit.

## Stop conditions

- Artifact residue of its own, a KEEP name missing, a REMOVE name surviving,
  any `[LUA ERROR]` naming any of the three mods → stop that leg, record
  verbatim, keep independent legs, route.
- A cell's config gate reads other than predicted → do not proceed on that
  cell; diagnose junction-side first (the gate exists so a wrong world is
  never measured).

## ⛔ What you may not claim

- Not "clean after uninstall" without the registry-absent gate line beside
  the reading (four-OFF-states doctrine).
- Not "residue-zero" without (r3) BOTH halves: the kit-instrumented inventory
  AND the zero-mods archived-log read.
- Not "the save is repaired" beyond what (r2) read back BY NAME; "vanilla
  threads alive" means the handle-valid read plus the one-shot bound, not a
  feeling.
- Not "gone" for any staged save while the EF-051 hold stands.

## Notes from upstream (prompt 3 appends here)

**From prompt 3 (Opus, the build — 2026-08-13). The spec is FROZEN, the
artifact EXISTS, and ⛔ NOTHING WAS LAUNCHED — every claim below is
source/design tier.** Staleness at my run: fix-pack `cdbcd9d`, opt-pack
`e17586b`, TestKit `62f03da`, all clean. Rule-7 gate CHECKED and PASSED before
any work: prompt 2's verdict is BUILD, checklist item 17 records Q-A = (c) and
item 18 records Q-B = mod-shaped.

### ⛔ ONE OWNER ACTION BLOCKS YOU, and it is not optional

**The rescue mod is installed but NOT ENABLED** (junction in
`%AppData%\Surviving Mars Relaunched\Mods\SMR-CommunitySaveRescue`, target
`C:\Dev\SMR-CommunitySaveRescue`). Enabling is a Mod-Manager tick **plus a full
process restart** — this entry's own measured finding — and re-enable is
owner-only by standing rule. **Checklist item 26 asks for it.** ⇒ At your
staleness check, read the checklist: if item 26 is not ticked, cells (r1)/(r2)
cannot load the artifact at all and every rescue probe SKIPs with
"save-rescue mod not installed". Report and hold rather than inventing a route
around it. (r0) and (r-restore) still run.

### What shipped, where

| repo | sha | what |
|---|---|---|
| **`C:\Dev\SMR-CommunitySaveRescue`** (NEW) | `1b88a47` + `aaff837` | the artifact. `metadata.lua` · `Code/00_Core.lua` · `Code/10_SaveRescue.lua` · `README.md` · `CLAUDE.md` · `docs/PROVENANCE.md` · MIT `LICENSE`. Public remote `catt144/SMR-CommunitySaveRescue`, **pushed**. Parse sweep 3/3 OK |
| `C:\Dev\SMR-BugFixPack-TestKit` | `b0c9d91` + `da432f8` | `Code/65_Probes_Rescue.lua` (6 probes) · `RescueStatus`/`RescueMissing` · the third `RunAll` gate line · README. **PARSE SWEEP: 19/19 OK, 0 FAIL** |
| `C:\Dev\SMR-BugFixPack` | this commit | `agent/reports/D13_EXPOSED_SET.md` (promoted + §10 spec) · the count sweep · D13/F86/EF-023/FIX_POLICY · STATE · checklist 26 |

Ids, all owner-ratified: `SMR_CommunitySaveRescue` · global `SMRSaveRescue` ·
log tag `[CommunitySaveRescue]` · display **"Save Rescue"** · veto global
`SMRSaveRescue_Disabled` (accepts `true` or `{ SaveRescue = true }`).

### The spec's verification-relevant promises — §10 of `agent/reports/D13_EXPOSED_SET.md`

⛔ **Read §10 whole before designing a cell; §10.9 is written as your contract.**
The short form:

**REMOVE — 11 names your matrix must read as ABSENT after a pass:**
`SMRFixPack_DroneSpeedDial` (label "Drone") · `SMRFixPack_DroneCarryDial`
(label "Consts") · `SMRFixPack_reserved_at` · `SMRFixPack_shelter_try` ·
`SMRFixPack_payload_set` · `SMRFixPack_rocket_fuel_key` ·
`SMRFixPack_ack_notworking` · `SMRFixPack_closed_to_new_residents` ·
`SMRFixPack_no_homeless` · `SMRFixPack_loop_version` · `SMRFixPack_fixed_loop`.

**KEEP — 2 names that must SURVIVE (a missing one is a stop-the-leg
condition):** `SMRFixPack_F35_<label>` modifiers (⭐ the residue IS the repair)
and `SMRFixPack_F48_StationConnectors`.

**NO ACTION, and the reason is mechanical, not a shrug:** `SMRFixPack_MeteorLatch`
and `SMRFixPack_FirstAsteroidPrefabs` are mod-registered GameVars, dropped on any
load without the registering mod — the artifact can never see them and must never
register a name to try. `SMRFixPack_spawn_gate` is deliberately not hunted.
⚠️ **So do not read "MeteorLatch absent" as evidence the artifact removed it.**

**The thread set — two heals, both one-shot, both vanilla-bodied:**

1. **Rains.** (a) stale-ACTIVE (`g_RainDisaster` truthy, entry's `main_thread`
   dead) → vanilla `FinishRainProcedure`; (b) an entry with a VALID
   `activation_thread` **and** `SMRFixPack_fixed_loop == true` → `DeleteThread` +
   `CreateGameTimeThread(RainsDisasterLoop, settings)`. Cost: **one rain
   re-roll** per entry. ⭐ **The detector is D4, and step 4 of the same pass
   REMOVES it** — that is what makes the heal one-shot with no latch. Your
   idempotence cell rests on exactly this: a second pass must find nothing.
2. **Meteors.** `RestartGlobalGameTimeThread("Meteors")` **only** when the
   thread is dead/absent AND `GlobalGameTimeThreadFuncs.Meteors` is a function
   AND a map is loaded AND `NoDisasters` is off AND the descriptor is present and
   not `forbidden`. Cost: **one re-roll of the 35-115 h window**, stated to the
   player. ⛔ **A LIVE thread is left alone and the skip is REPORTED** — a
   captured foreign body is not readable from Lua, so "alive" is ambiguity, and
   ambiguity is reported, never guessed. Predict the skip, do not predict a
   restart.

**The stand-down, which is the cheapest cell you have (§10.1).** Rows act only
while the mod that WROTE them is absent — **per mod, not globally**, because a
player who removed only the opt-in pack still has permanent dial residue. So in
the rig's normal config (r1) the automatic pass is a **measurable no-op** and
logs its zero; a stand-down dialog appears **once per session**, not per load.

**Version skew is answered by DISCLOSURE, not detection (§10.6)** — the artifact
cannot know which pack version wrote a save (the only versioned stamp is a
mod-registered GameVar and is already gone). It logs its own version and the
derivation stamp on every run: *"list derived over Community Fix Pack cdbcd9d /
Opt-In Modules e17586b (2026-08-13)"*. **That line is your version-skew
witness** — quote it from the log rather than asserting coverage.

**Self-cleanliness (§10.7)** — no `GameVar` call anywhere, no name write of any
kind (every mutation is `= nil` or a vanilla removal call), no GT thread of its
own, no Mod Options machinery. The one thread it creates is the report's
REAL-TIME thread (`persist.lua:128-131` — RT threads persist only when flagged
`threadPersist`, and nothing here flags one). Probe `SaveRescueSelfClean` checks
the mechanical version of this at runtime: no `SMRSaveRescue*` key in
`PersistableGlobals`.

### The probe surface, and why it exists

The automatic path stands down whenever a pack is loaded, so a probe that waited
for `PostLoadGame` could never sample the pass. Drive it directly:

* `SMRSaveRescue.RunPass{ force = true }` — `force` bypasses **only** the
  stand-down gate. Never the KEEP list, never an ambiguity skip.
* `SMRSaveRescue.Scan()` — read-only census. `SMRSaveRescue.HealThreads{}` —
  the heals alone. `SMRSaveRescue.ListResidue()` / `.ResidueNames()` — the table.
* Returns `{ removed, by_name, by_noun, kept, heals{meteors, rains_restarted,
  rains_finished}, skipped, stood_down }`. **`by_name` is your INVDIFF surface.**

⚠️ **The six new probes never touch the real save** — they stub a synthetic city
and colony through `WithGlobals` first, because a forced pass on a live colony
would really strip its timestamps and really take a Drone dial's boost off the
session in progress. ⛔ **Keep that property in any probe you add**, and note
**both interlocks** (`da432f8` — one of them was missing on the first cut, found
by re-reading rather than by running):

* `g_RainDisaster = false` is stubbed by a `stubs()` helper **no probe may
  bypass**. The rain heal reads that global from the REAL session and then looks
  its entry up in the stubbed `RainsDisasterThreads` — a rain actually falling
  resolves to "no entry, known type", the exact stale-ACTIVE shape, and the heal
  would fire vanilla's `FinishRainProcedure` at the live weather.
* `MainMap = false` is passed wherever the meteor half is not the subject, so
  its designed-silence guard declines.

In particular the dead-meteor restart is deliberately NOT exercised by the suite:
proving it costs a real 35-115 h re-roll. **That leg is yours, on a fixture.**

### Fixtures — one class exists, one must be manufactured

* **Exists BY NAME:** `PT35FIXTURE.savegame.sav` carries `SMRFixPack_*` instance
  fields and `MeteorLatch` (split-matrix FixtureCarry dumps). It is a fine (r2)
  witness for the **object-field** rows, and it is the natural place to plant a
  D10 witness. ⛔ Do not delete it (STATE).
* **Does NOT exist:** no save in the folder is known to carry
  **PRE-REWRITE-lineage** residue — a live `activation_thread` stamped
  `SMRFixPack_fixed_loop`, or a dead `Meteors` thread. Every save the current
  pack has loaded was migrated and latched by the pack itself. ⇒ **Manufacture
  it:** a declared probe writes `SMRFixPack_fixed_loop = true` onto a real
  `RainsDisasterThreads` entry (and/or `DeleteThread`s the `Meteors` thread) on a
  BYTE COPY, saves, reloads. Say in the record which witness is synthetic and
  which is native — the derivation's own claim is only that this population
  exists in the wild, never that we have one.
* ⛔ **D10 is still UNSAMPLED** (§6 doubt 3): the KEEP headline has never been
  observed. **Plant or manufacture an F35-affected witness and read the modifier
  back** — absent ≠ refuted, the condition must be SAMPLED. This is routed to
  you by name.

### Suite baseline — changed, and NOT re-measured

⛔ **Probe count 88 → 94.** The audit-measured `78/0/10/0 of 88` is **PENDING
RE-MEASUREMENT** and (r0) should quote it as such: the six new probes have never
run anywhere. Expected shape once the artifact is enabled and a game is loaded:
they PASS or SKIP; with the artifact absent all six SKIP with
"save-rescue mod not installed". ⚠️ The queued `FactionFundingCheck` PASS→SKIP
repair (TestKit `62f03da`) was **NOT** taken here and stays queued — I did not
want two unmeasured changes in one baseline.

### Uncertainties I am handing you, stated rather than buried

1. **Nothing has been run.** The pass has never executed. A syntax-clean parse
   sweep is not a run — treat every cell as a first execution, watchdogged.
2. **The label walk misses unlabelled objects** (§10.2) — the real case is a
   colonist riding a rocket (`keep_cargo_in_labels = false`). Their timestamps
   survive that one load and clear on a later one. If your (r2) read finds a
   handful of `reserved_at` survivors, check whether they are in cargo BEFORE
   filing it as a defect.
3. **The stand-down is `pack=n/n`-shaped** — off-states (1) and (2) read as
   PRESENT, so a toggled-off or restart-less-disabled pack still stands the
   rescue down. Correct, but it means (r1) must set its config by JUNCTION, not
   by toggle, or it measures the wrong thing.
4. **The report dialog is untested UI.** `WaitMessage` on an RT thread with a
   2 s settle `Sleep` — I have read the precedent, not seen it fire. A cell that
   loads a residue-carrying save WILL raise a dialog; expect it in the watchdog.
5. **`Consts`-label removal.** Removing the carry dial calls
   `SetLabelModifier("Consts", id, nil)`; the const rebuild rides vanilla's
   `OnMsg.ConstValueChanged`. I am confident by construction (it is the module's
   own base-position call) but it is unmeasured — **read `DroneResourceCarryAmount`
   back**, do not assume.
6. **One live-path observation inherited from prompt 2b and still unowned:** with
   the pack INSTALLED, a save taken during an active Crystals mystery restores a
   repeater the LoadGame handler cannot stop, so hourly `CrystalFlyAway`
   broadcasts can double per save/load cycle. Source-derived, unmeasured, inert
   as far as anyone can tell. I did NOT file it as a bug entry (that changes the
   index row counts, and I had no mandate) — **it is still routed, now to prompt
   5 or the owner.** It is also the cheapest available witness for the corrected
   persistence model, if a cell is ever cheap.
7. **The QA sweep's "opt-pack docs clean" was wrong** — that repo carries its own
   `EF-023` and `FIX_POLICY`, both stating the superseded 13. Corrected in both
   repos here. Recorded because it is the house pattern: a recorded fact is a
   claim, including a QA verdict about completeness.
