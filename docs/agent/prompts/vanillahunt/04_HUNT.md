# 04 — the hunt: one parent, one agent per system and per preset registry

⛔ ONE-SHOT: this file `git rm`s itself on close-out (README rule 2).
Model: **Codex Sol Ultra — owner-assigned 2026-09-10** (*"its specialty is
massive subagent coordination; it is specifically designed for this sort of
task"*) · owner needed: no · after 02; **independent of 03** (the seam) — the
two may run at once in separate sessions, they share no rows. ⚖️ **Owner
ruling, same date: this link does NOT split.** The whole hunt is one
orchestrator; rule 4 of the README does not apply here. What still binds is
everything below about verification and evidence — a bigger fan-out raises
the bar on those, it does not lower it.

⚠️ **Written tool-neutral.** Where this brief says "agent" it means your
platform's judgement-capable subagent (one that reads whole bodies and
reasons), never a locate-only search agent. Where the README's chain rules
name Claude Code tools (`ListAgents`, `SendMessage`), use the git-visible
equivalents in README rule 1 and rule 15 — they were rewritten for this.

> 🎯 Every row 02 did not tag `dlc-adjacent` is read here: the hand-written
> Lua by SYSTEM, the preset data by REGISTRY, the storage moves and the
> removed/added files. **You are the parent.** You do not read rows; you brief
> agents, verify a sample of what each returns from the two trees, file the
> findings that survive, and commit every agent report verbatim as primary
> evidence for 99. ⭐ Consolidated from four links on the owner's question of
> 2026-09-10 — same job on disjoint row sets, so one orchestrator; the reading
> orders below are what those four links were going to enforce, now enforced
> per agent brief.

## 0 · Open in this order

`git log --oneline -10` · `git pull` · `ListAgents` · `README.md` (§2, §3, §4
— binding, and §4's return format goes into every brief VERBATIM) · `STATE.md`
· `TRIAGE.md` §1–§4 (your row lists are §3 "04": per system and per registry,
with (h) seeds, `F117-SHAPE` candidates, `unsure` rows, and the preset readable
pile after 01's churn rules) · the TSV banners · 01's fpk-parity fact ·
`PACK_1_1_0_REVERIFICATION.md` §1 (REMOVE bucket) · `VANILLA_FIX_QA.md` §0 ·
`bugs/F95.md`, `F114.md`, `F116.md`, `F117.md`, `F118.md`, `C54.md`, `C55.md` ·
`facts/INDEX.md` (`EF-005`, `EF-008`, `EF-009`, `EF-017`, `EF-066`, `EF-079`,
`EF-080`, `EF-083`) · `FIX_POLICY.md` §4, §6 · your inbox. Pin check (README §0).

## 1 · 🗒 Live todo list, from your first action

One item per agent wave, one per verification pass, one per filing batch.

## 2 · The design — decide the split BEFORE spawning anything

1. **Size from the ledger, not from hope.** Per system and per registry, take
   02's `WORTH-READING` row count. **~250 rows is one agent.** A system above
   that is cut into file-group agents (e.g. `turf` → tracks+trains /
   landscaping+construction / drones+logistics+depots). Write the full agent
   plan (agent · rows · files) into `TRIAGE.md` "04" BEFORE the first spawn,
   so 99 can check that every row was assigned to exactly one agent. ⛔ No
   `04b` — the owner ruled this link does not split; the whole plan runs
   here, in as many waves as it takes. What the parent must hold is the
   VERDICTS, never the reading: keep per-agent results in the committed
   `agents/` reports (§2.5) and work from those files, not from memory.
2. **One brief per agent**, a judgement-capable subagent (⛔ never a
   locate-only one), holding: the two archive roots; its row list (file · function ·
   both line ranges, or `class:id · key` for presets); README §2's taxonomy
   VERBATIM; the system's reading order from §3 below; README §4's return
   format VERBATIM plus the surface-sweep clause; the `find_bodies` call it
   must use for spans; ⛔ no seeds named; ⛔ no file writes; ⛔ "looks fine"
   rejected. Waves of 6–8 in parallel.
3. **Verify before you write.** For every agent: re-derive at least ONE of its
   findings from the two trees yourself (the highest-severity one), and re-read
   any agent whose "rows reached" exceeds the rows it was given or whose report
   carries no NOT-reached list. An agent whose verified finding does not hold is
   re-issued with the failure quoted; both reports are kept.
4. **File what survives** as `C` entries per README §3 — the agent returns
   entry-ready text (route, both citations, reach, falsifier, recipe, severity,
   `DIFF-CAUSED` or `PASSING`); you check it, you write it. Batch the index
   regeneration per wave.
5. **Commit every agent report verbatim** to
   `reports/vanillahunt/agents/<system-or-registry>[-<n>].md` (banner: brief
   hash, wave, rows given, date). ⛔ Not optional — 99 audits verdict-by-verdict
   against these, and evidence living only in a session transcript is the
   failure `CHAIN_METHOD` §3 records twice.
6. **⭐ Field-report rows FIRST (README §2b, owner 2026-09-10).** Every row 02
   tagged `FR-1` / `FR-2` / `FR-3` goes to the agent that owns its system, at
   the TOP of that agent's list, and the agent's brief carries README §2b's
   paragraph for that report VERBATIM, plus the `PERF` tell for its `SMELL`
   field. Record in the agent plan which agent took which FR rows. From the
   verified returns, write subsections **FR-1** (surfaces a, c, d), **FR-2**
   (the route answer) and **FR-3** into your `TRIAGE.md` section — each with
   rows read, candidates and a NOT-reached list. ⛔ An agent's "nothing" on an
   FR row is re-read by you from the trees before it is written; FR-1 is the
   report players say leaves the game unplayable.
7. **⭐ `NOROWS.tsv` — the changed code that has no rows (added 2026-09-10).**
   Every `reader=NONE`, `content=yes` file in `NOROWS.tsv` (123 on these
   trees) is changed hand code with no inventory row, so no row list can carry
   it: top-level option / config / const tables, and preset data stored outside
   the `generated` prefixes. Assign each to the agent that owns its system as a
   TEXT-DIFF item (both trees, compared after trailing-whitespace
   normalisation), the FR-relevant ones first (README §2b names them), and
   record the assignment in the agent plan. The agent reports what changed and
   applies the same taxonomy and `SMELL` / `PERF` tells as for rows. ⛔ A
   `NONE`+`yes` file that no agent was given is a coverage defect, and 99
   checks for it.

## 3 · Per-system reading orders — go into the briefs, binding

**A · turf** (`trains` `landscape` `construction` `drones` `logistics`
`depots`). (h) FIRST — for each retired module in these systems (`git show
2dc1dbe^:Code/<module>.lua` for its header, target and stated defect) read the
1.1.0 target body, confirm the developers' fix is what the re-verification
said (`VANILLA_FIX_QA` §0 corrects the main report in four places), then the
NEIGHBOURHOOD: every caller, every sibling, every field the fix now writes.
Then (b′) rows (write the argument positions out), then (a)/(b)
`WORTH-READING` biggest files first (`Track*`, `Train*`, `Station*`,
`Landscaping.lua`, `LandscapeConstructionSite*`, `ConstructionSite.lua`,
`Construction/Construction.lua`, `Drone.lua`, `DroneControl.lua`,
`ShuttleHub.lua`, `*Depot*`, `Resources.lua`), then (i), (f), then a 30-row
`CHURN` spot check. ⭐ Extend `EF-083`: landscaping is rover-only and
research-gated on 1.1.0 — enumerate what else assumed drones reach a
landscaping site (`ShouldAddRequestToCommandCenter` readers, the research
flag readers). `C55` is filed — extend, never duplicate.

**B · colony** (`colonists` `domes` `services` `rockets` `disasters` `story`
`saveload`). **Save/load FIRST**: every changed/added function in
`_fixup.lua`, `SavegameFixups.*`, `Persist*`, every `PersistGatherPermanents`
/ `OnMsg.LoadGame` / `PostLoad` body — what state it rewrites, what 1.0.7
wrote there, idempotent or not, once-per-save (cite the versioning mechanism
in `CommonLua`) or every load, and what it does to a colony STARTED on 1.1.0.
The `RefreshAstrogeologistExtractorBonus` fixup narrowing on `Percent == 20`
where 1.0.7 pays 10 is noted inside `bugs/F95.md` and never filed — file it
with the route or refute it, first. Then (h), then (b′) — `ChooseDome`'s own
vanilla callers from `CALLERS.tsv` — then (a)/(b) biggest first
(`Colonist.lua` ~298 declarations, `Dome.lua` ~281, `Building.lua` ~254 by
class prefix, `UniversalRocket.lua` ~239, `SA_Gameplay.lua` ~182), then (i),
(f), spot check. Story/scenario/mystery Lua last (`Lua/Mysteries` 11,
`Lua/Scenario` 26); the `StoryBit` presets are a registry agent's. ⛔ `C54`'s
lesson before any unguarded-read filing: count the unguarded siblings, check
`EF-005`. The F118 mechanism (1.1.0 registering the layout controller in
`s_ConstructionControllerDeleteOnLoad`) raises the vanilla question of whether
any VANILLA `Deactivate` caller resets that flag — this agent's.

**C · engine** (`commonlua` `ui`). **The tooling gate first, by ROUTE:** for
every `CommonLua` subtree, cite the loader (`dofile`/`require` and the
platform flag) and verdict `shipped-runtime` (read in full) /
`shipped-dev-only` (read the gate, sample 10 rows for leaks past it) /
`not-in-fpk` (01's parity list — not read, counted). ⛔ A verdict by directory
name is a label check; `CommonLua/Libs/MapGen` and `Lua/RandomMap` are RUNTIME
until the loader says otherwise. The parent keeps the gate table in
`TRIAGE.md` "04". Then (b′), (a)/(b) in `shipped-runtime` files
(`CommonLua/Classes` 76, `Core` 25, `Libs` runtime part, `X` 30, `UI` 18,
`Lua/UI` 17, `Lua/X` 20, `XTemplates` 5), (i), (f), spot check. ⚠️ A
`CommonLua` change is felt above it: for every real change name ONE consumer
in `Lua/**` and read whether it still holds (`EF-066`: a `classes.lua` change
reaches every descendant). UI wrongness is a hypothesis until a keyboard sees
it (`FIX_POLICY` §4) — file `cand`, tier U, observation named.

**D · storage + removed/added** (one agent). Class (c) from `STORAGE.tsv`:
every `moved-file` / `kind-changed` / `removed` row, grep both trees for every
READER, classify `updated / still-old-address / dynamic`; a `still-old-address`
reader in shipped runtime code is a finding naming what it now reads. Calibrate
on the `Landscapes` move first (1.1.0 `MapVar("Landscapes", {})`,
`Landscaping.lua:21`; `bugs/F115.md` line ~46) and check against the entry.
Then `FILES.tsv`: the 36 removed — a nonzero still-present-names count is a
MOVE (find where: `CommonLua/Classes/Mod.lua` → `CommonLua/Modding/Mod.lua` is
the known case), zero is a candidate (e) that still needs the CAPABILITY
searched (UI string, preset, `XTemplate`); the five removed `XDef` dialogs and
the five tutorial files are the obvious (d)-or-(e) cases; the old modding
backend (`Mod*.lua`, `ModsBackend.lua`) has the widest reach. The 305 added
minus `DLC/norman`: class (f) grouped by what they plug into; zero callers ⇒
dead-on-arrival (tell 2) or a hook by name — say which, with the search.

**E · presets, one agent per registry** (`CropPreset`, `Meal`, `Resource`,
`LawDef`, `PolicyDef`, `Tech`, `Cargo` are 03's where `dlc-adjacent`; yours
are the remainder plus `BuildingTemplate`, `TraitPreset`, `StoryBit`, `XDef`,
`FactionDef`, `Scenario`, `PopupNotifications`). Rows are the readable pile
after 01's churn rules (`PRESETS.tsv` `churn-class = none`). ⛔ Field-level:
the deliverable per row is **which key, what value, which base-game CONSUMER
reads it (`file:line`)**, or `no Lua reader found` with the grep. The question
is the thesis's: does the old consumer still read the new value correctly? A
new key nobody reads is tell 2; a removed key someone still reads is a nil
where a value was. No balance opinions. Removed data files worth a presence
check: `TutorialPreset`, `DiscoveryGenericPreset`,
`FactionDef/TransHumanistMovement`, `PopupNotificationPreset-Tutorial`.

## 4 · What every agent returns — README §4's list, plus

- **`DIFF-CAUSED` or `PASSING`** on every finding. ⭐ **The surface sweep
  (owner, 2026-09-10):** a body opened for any reason — a changed row, a
  caller, a sibling, a consumer — that meets a `FIX_POLICY` §4 tell (dead code
  or dead validation, sibling contradiction, self-contradiction, an explicit
  dev comment) is returned as a `PASSING` finding with the tell named, whether
  or not 1.1.0 caused it. Not a hunch: a tell, or nothing.
- **coverage**: rows given, rows read, rows NOT reached with the reason; the
  30-row `CHURN` spot check (hits reopen that file's churn).
- **for each finding**: entry-ready text per README §3, both trees cited, the
  recipe derived separately from the diagnosis, the falsifier's form
  (executing via the `tools/desk_*.py` pattern where the body allows;
  `desk_probes_f67_f59.py` for building/unit bodies, `desk_f117_argshape.py`
  for scoring/choice bodies).

## 5 · Scope fence

**In:** §2–§4, filing, `agents/` reports, `TRIAGE.md` "04" (the gate table,
coverage per agent, spot checks). **Out:** every `dlc-adjacent` row (03's —
a seam an agent finds in an untagged row is a one-line note to 03 and a triage
drift for 99); `DLC/**`; any `Code/` edit or module; any tool edit; ⛔ a
finding that implies a KEEP module is now wrong on 1.1.0 is a hotfix-3
checklist item, TAKEABLE WHEN the owner rules — never repaired here.

## 6 · Stop conditions

An agent's verified finding fails twice (the brief is wrong — fix the brief,
record the drift, re-issue) · a falsifier needs a running game (checklist
rider, TAKEABLE IN the post-upload sitting or the next organic play) · ⚠️ if
the session cannot complete the plan: commit every report and filing so far,
mark the unrun agents in the `TRIAGE.md` "04" plan as NOT RUN with the
reason, and STOP — ⛔ do not author `04b`; the owner decides how the remainder
runs (the same orchestrator resumed on the committed plan is the designed
recovery, which is why the plan and the reports are committed as you go).

## 7 · What may NOT be claimed

`tested`. That a system with no findings is clean (report rows and agent
count). That an unread `CHURN` row is safe. That a retired module's vanilla
fix is COMPLETE (the re-verification's claim; yours is whether it broke a
neighbour). That a subtree is tooling by its name. That "no caller found"
means unreachable without the inheritor count and the search string on the
entry. That an agent's report is evidence until you re-derived one finding
from it.

## 8 · Close-out

Outbox to 03 (seams found in untagged rows, if 03 has not closed) and to 99
(every finding with its route and `DIFF-CAUSED`/`PASSING`, the agent count,
verification results per agent, every re-issue, NOT-reached lists, spot
checks, drift). Strike your row. Explicit-path `git add`: `TRIAGE.md`,
`reports/vanillahunt/agents/*.md` by name, `bugs/C##.md` + `bugs/INDEX.md`,
`facts/EF-###.md` + `facts/INDEX.md` if any, README, 03 (if open), 99; `git rm`
this file. doccheck GREEN, both selftests GREEN, commit `-F`, push.

## Notes from upstream

*(authoring session, 2026-09-10)* The three re-copies in the turf systems
(`LandscapeUnitFilter`, `TrainCargoDumping`, `VacuumWalks`) had their 1.1.0
bodies read line by line on 2026-09-09 (`prompts/hotfix2/README.md` row 04b);
their entries carry the two-sided diff — start from those reads. `F45` is
still live on 1.1.0 (KEEP). The `Data/` twins: `Lua/BuildingTemplate` and
`Lua/XDef` are generated from the `Data/` side — 01 diffs `Data/`; the
`BuildingTemplate` registry agent confirms on a sample that the twin carries
nothing the `Data/` side does not.

---

*(from link 02, `smr-bugfixpack-b6`, 2026-09-10 — TRIAGE.md §1–§4 is WRITTEN. ⛔ A class is a sort key, `WORTH-READING` a routing flag, a `SMELL` a PASSING candidate to derive; no row here is a finding.)*

**Size your agents from TRIAGE.md §3 "04's sizing line"** — the WORTH-READING counts there are exact (the files' own). Per agent:

**A · turf**
- **Row lists:** `TRIAGE.md` §3 "04-A" — pointers into `INVENTORY.tagged.tsv` (`link` column == `04-A`: 1199 rows, 696 fan-out classified, **596 WORTH-READING**)  and `CALLERS.tagged.tsv` (`caller_link` == `04-A`).
- ⭐ **FR rows FIRST (README §2b): 57** — FR-3 35, FR-2 17, FR-1(a) 6, FR-1(d) 1.
- **NOROWS text-diff items: 9 files** (changed hand code no instrument lists; `diff` both trees; list in TRIAGE.md §3 "04-A").
- **(h) seeds: 9** — R-1 `LowStorageWarning`; R-6 `SmallLandscapeSites`; R-7 `DroneTransportMinors (b)`; R-8 `DroneUnreachableForever`; R-23 `DustStormUndergroundBreaks`; R-26 `LandscapeCostRefresh`; R-31 `StorageRateModifiers`; R-34 `TrainMinors`; R-35 `TrainPlatformWedge`.
- **F117-SHAPE candidates (0)** — TAKEABLE WHEN you read the caller's body: —.
- **SMELL rows: 64** (PASSING candidates; the list is in §3) · **agent `unsure`: 0** · **CALLERS `unsure`: 0**.

**B · colony**
- **Row lists:** `TRIAGE.md` §3 "04-B" — pointers into `INVENTORY.tagged.tsv` (`link` column == `04-B`: 2408 rows, 1230 fan-out classified, **1074 WORTH-READING**)  and `CALLERS.tagged.tsv` (`caller_link` == `04-B`).
- ⭐ **FR rows FIRST (README §2b): 199** — FR-3 122, FR-2 53, FR-1(a) 33.
- **NOROWS text-diff items: 6 files** (changed hand code no instrument lists; `diff` both trees; list in TRIAGE.md §3 "04-B").
- **(h) seeds: 21** — R-2 `LanderCargoRatchet`; R-3 `TouristSatisfaction`; R-4 `AutomationLawCompensation`; R-5 `UpgradeModifierLeak`; R-9 `MeteorFrequency`; R-10 `MeteorStormWedge`; R-11 `AsteroidLanderAvailable`; R-12 `GridGlobalStorage`; R-14 `RainsDeadlock`; R-15 `DustSicknessDamage`; R-17 `UniversityOvertraining`; R-18 `CaveInsNoDisasters`; R-20 `DisasterPredictionLeak`; R-21 `DustDevilSpawnGate`; R-22 `DustDevilsDescrMap`; R-24 `ExtractorStaffedPerformance`; R-25 `LanderReturnFuel`; R-28 `MilestoneCrash`; R-29 `MoraleComfortTooltip`; R-33 `TouristApplicants`; R-36 `90_SaveSanitizer`.
- **F117-SHAPE candidates (5)** — TAKEABLE WHEN you read the caller's body: `Lua/_fixup.lua:1335` (ActionFX.GetLocObj); `Lua/Units/ColonistTransport.lua:114` (GetTransportRoute); `Lua/Units/ColonistTransport.lua:123` (GetTransportRoute); `Lua/Units/ColonistTransport.lua:136` (GetTransportRoute); `Lua/Units/ColonistTransport.lua:141` (GetTransportRoute).
- **SMELL rows: 90** (PASSING candidates; the list is in §3) · **agent `unsure`: 0** · **CALLERS `unsure`: 0**.

**C · engine**
- **Row lists:** `TRIAGE.md` §3 "04-C" — pointers into `INVENTORY.tagged.tsv` (`link` column == `04-C`: 2871 rows, 1453 fan-out classified, **1255 WORTH-READING**)  and `CALLERS.tagged.tsv` (`caller_link` == `04-C`).
- ⭐ **FR rows FIRST (README §2b): 214** — FR-1(a) 78, FR-1(c) 61, FR-3 59, FR-2 21, FR-1(d) 12.
- **NOROWS text-diff items: 90 files** (changed hand code no instrument lists; `diff` both trees; list in TRIAGE.md §3 "04-C").
- **(h) seeds: 0** — —.
- **F117-SHAPE candidates (3)** — TAKEABLE WHEN you read the caller's body: `CommonLua/Classes/ActionFX.lua:2052` (ActionFX.GetLocObj); `CommonLua/Classes/ActionFX.lua:2821` (ActionFX.GetLocObj); `CommonLua/Classes/ActionFX.lua:3967` (ActionFX.GetLocObj).
- **SMELL rows: 191** (PASSING candidates; the list is in §3) · **agent `unsure`: 1** · **CALLERS `unsure`: 2** — `CommonLua/Camera.lua:801` LuaExportedDocs stub of a C function: the documented contract shrank to (map, ..; `Lua/X/Infobar.lua:582` this caller passes a CITY (Infobar.lua:582, reached with UICity from :661 — agen.

**D · storage + removed/added**
- **Row lists:** `TRIAGE.md` §3 "04-D" — pointers into `INVENTORY.tagged.tsv` (`link` column == `04-D`: 2003 rows, 0 fan-out classified, **0 WORTH-READING**)  and `CALLERS.tagged.tsv` (`caller_link` == `04-D`).
- ⭐ **FR rows FIRST (README §2b): 95** — FR-3 71, FR-1(a) 15, FR-2 9, FR-1(d) 2.
- **NOROWS text-diff items: 0 files** (changed hand code no instrument lists; `diff` both trees; list in TRIAGE.md §3 "04-D").
- **(h) seeds: 0** — —.
- **F117-SHAPE candidates (0)** — TAKEABLE WHEN you read the caller's body: —.
- **SMELL rows: 0** (PASSING candidates; the list is in §3) · **agent `unsure`: 0** · **CALLERS `unsure`: 0**.

**E · presets**
- **Row lists:** `TRIAGE.md` §3 "04-E" — pointers into `INVENTORY.tagged.tsv` (`link` column == `04-E`: 1972 rows, 0 fan-out classified, **0 WORTH-READING**) + `PRESETS.tagged.tsv` (25409 rows) and `CALLERS.tagged.tsv` (`caller_link` == `04-E`).
- ⭐ **FR rows FIRST (README §2b): 0** — .
- **NOROWS text-diff items: 0 files** (changed hand code no instrument lists; `diff` both trees; list in TRIAGE.md §3 "04-E").
- **(h) seeds: 6** — R-13 `LastTransmissionStorage`; R-16 `IndependenceTerraforming`; R-19 `CommandCenterNumbers`; R-27 `LocalizedUIText`; R-30 `SpaceYDroneCapBullet`; R-32 `TechDescriptionBuilding`.
- **F117-SHAPE candidates (0)** — TAKEABLE WHEN you read the caller's body: —.
- **SMELL rows: 0** (PASSING candidates; the list is in §3) · **agent `unsure`: 0** · **CALLERS `unsure`: 0**.

- ⛔ **FR-1 TEXT-DIFF ITEM for agent C — RE-RANKED 2026-09-10, no longer first (not rows — no instrument emits them):** players with anti-aliasing Off / FXAA still crash, so the temporal upscaler is REFUTED as the trigger (README §2b, the falsifier bullet). Read the map-generation / new-game native-call set FIRST (the next bullet, and README §2b's FR-1 `MapGen` NOROWS files); these tables stay a read item because the native DLSS 4 load is not excluded. The upscaler tables (README §2b, ce06307) live in top-level data tables. `diff` both trees of: `CommonLua/Core/options.lua` (35 lines; `OptionsData`, DLSS pick at 1.1.0 :219-224), `CommonLua/Core/GlobalStorageTables.lua` (4), `CommonLua/Classes/RenderFeaturesParams.lua` (410), `CommonLua/Core/Postprocessing.lua` (25), `Lua/ProjectOptions.lua` (24), and `Lua/Config/` (`_config.lua`, `_libs.lua`, `config.lua`, `pathfind.lua`, `render.lua` changed with 0 rows; `_pfclasses.lua`, `Libs/` new). TRIAGE.md §1.7 has the measurement.
- ⭐ **FR-1 lead from the fan-out (agent B21's NOTES, a claim, not re-read by the parent):** `MapGen:ApplyPass` calls `ResumePartialPassEdits("MapGen")` TWICE (`CommonLua/Libs/MapGen/MapGen.lua` 1.1.0 :1160-1161) against ONE `Suspend` in `RunInit` — a self-contradiction tell on the map-generation path FR-1(a) tags. Agent C: read it with the FR-1 set.
- ⚠️ **FR-3 `PERF` gap:** fan-out batches **B01–B15** were briefed before README §2b and carry no PERF tells; your agents re-open those WORTH-READING bodies with PERF in their briefs — 99 checks that you did.
- ⚠️ **Appended-parameter callers are benign BY SHAPE only** (TRIAGE.md 1.5): the heuristic was falsified once (`ActionFX:GetLocObj`); a same-signature body that starts needing an argument (R08311) is invisible to CALLERS — read the agent (b′) row verdicts.
- The agents' verbatim cross-row NOTES are TRIAGE.md §3.x — several are tree-wide contract shifts (`table.ifilter` callback, `OnSetWorking` → `RecursiveCallMethods`, `IsInWalkingDist` −1).


### From 03 · core food seam close-out, 2026-09-10

03 consumed after 396 complete present-span reads; its required split is now
03b_SEAM_PRESETS.md (360 generated + 1,618 fields),03c_PROGRESS_SEAM.md (284 hand),
03d_CALLER_SEAM.md (249 hand + 18NOROWS). Callers are partitioned too. Your original
04 rows are unchanged; no new untagged seam was reassigned away from you.
SEAM_COVERAGE.tsv and SEAM_REPORT.md give exact ownership and evidence.

Avoid duplicates C56-C62, all cand/source-read. Five DIFF-CAUSED; C59 bounded
next-slot loop and C62 discarded explosion list are PASSING. C56/C57/C59 desk
controls discriminate; no runtime/native proof. Untagged support/caller bodies
were opened for routes (e.g. producer callbacks, MicroGHabitat, death handlers),
not counted as draining your rows. Read your own full bodies as planned.

For FR-1: three03 new-game-tagged base bodies read, seven pending03c/03d;
Lua guard3/1 vs Lua + Data10/1, no crash ruling. Temporal-upscaler lead stays yours.
Lua/Config/config.lua belongs to 03d's18NOROWS but is also in your explicit
FR-1 support list: coordinate the finding;03d owns whole-file coverage.
FR-2 none read by03. FR-3 hard C60 allocation plus unmeasured Community hourly
resident scans, farm synchronization, widened pet enumeration and recipe loops;
no claim about the original 2025 stutter. SEAM_REPORT has old/new counterevidence.

C62's four wrappers still lack a concrete instantiated scenario.03b/03d may
consult generated effects/ScriptStatements; an original 04-E preset stays yours.
No absence search proves a dynamic/native caller cannot exist. For all non-owner
claims, base class existence does not prove a constructible building/preset route.
Send new seam handoffs to the open03b/03c/03d owner;99 waits for all. Detailed
drift and corrected source names/recipes are in SEAM_REPORT, not hidden by the split.

## From completed 03c — progression seams, 2026-09-10

03c consumed 286/286 (284 INVENTORY + C03016/C03021), filed C63-C65, and has no
child queue. Avoid duplicates: C63 is the new zero-seat disaster guard bypassing
duration/ShouldStop while daily updates continue; C64 is the pre-existing
completed-opportunity expiry loop gated on another active opportunity; C65 is
the Earth Council intro wrapper orphaned when BeginSession was removed. All are
source-read/runtime-unobserved; archived-body/source controls discriminate.

Your `GameRules.lua` R08351-adjacent lead is refuted: PersistLoad calls
`LoadGameSettingFixup` and copies `idGameRules` into `Game` before the later
save-fixup phase, so `MoveGamerulesToGame`'s now-false global is redundant rather
than a lost setting. Do not file it. DeepScanning's live Tech has both effects
and its Exploration consumer is connected; probes independently require
AdaptedProbes. EasyResearch's initiative selection is intent/runtime-ambiguous,
not filed. R08012's missing stale-disaster cleanup is conditional on an official
removable-faction save route and belongs to dlccheck. R09822 is an unprofiled
700 ms Tech Tree UI waiter, not evidence for the pre-1.1 stutter.

Exact receipt, FR-1/2/3 outcomes, random sample 6/6+6/6, drift and scope limits:
`PROGRESS_SEAM_REPORT.md`; controls: `PROGRESS_SEAM_DESK.txt`. A delegated Norman
instance search exceeded 03c's fence and is disclosed only as an outbox lead,
not DLC coverage.

## From completed 03d — caller, service and rowless seams, 2026-09-10

03d consumed **283/283** (249 INVENTORY + 16 CALLERS + 18 whole-file NOROWS),
NOT-REACHED 0, and has no child queue. Exact keys, limits, rejected leads and
the random 6/6 change + 6/6 route sample are in `CALLER_SEAM_REPORT.md`; archived-
body controls are `CALLER_SEAM_DESK.txt`. The tagged inputs and
`SEAM_COVERAGE.tsv` remain unchanged.

Avoid duplicates C66-C73, all cand/source-read and runtime-unobserved: C66
ground RC Transport group-All unloads all cargo; C67 returns an old-shift meal
against the reset current-shift counter; C68 fulfills/eats after failed service
entry; C69 treats an active AI-mystery research wait as Researched; C70 can
rebind a destroyed St. Elmo experiment to a pre-existing tank; C71 retains an
Explorer-malfunction message after the rover effect/register were removed; C72
adds 40/50 ms Basics tutorial polling; C73 overwrites a just-computed Food
availability value. C67-C69 desks discriminate; C72/C73 require profiling.
Checklist 138 owns all fresh-fixture/runtime choices.

For FR-1, 03d's whole-file read of `Lua/Config/config.lua` found broad new
native/all-player workers and settings but no entitlement branch or Proton
crash mechanism. Do not double-claim that file; your temporal-upscaler result
remains yours. FR-2 remains unexplained: the DeepScanning definition/effect and
Exploration route are connected, while probes separately require AdaptedProbes.
FR-3 remains open: R07155 keeps its old bounded 500 ms wait; the new short-
cadence/tutorial and hourly work is unprofiled and cannot cause the pre-1.1
report. No field report was closed.

C69's route reaches the generated `SA_WaitResearch`/research-effect surface in
your 04-B queue; use the 03d direct-callee read as supporting evidence, not as
drainage of your assigned row/preset. C62's ScriptStatements wrappers were
confirmed to validate and call `BlowUp` with StoryBit provenance, but no
concrete authored instance was found; your original 04-E preset search remains
the owner. R11004's absent universal-storage Seeds gate remains unresolved
until a concrete acceptance/availability route is read.

For dlccheck only, TAKEABLE WHEN it reads a concrete owning class/preset:
WorkFarmInsect/WorkFarmSmall's `Maps[1]` temporary-tablet assumption and the
prior recipe-input double-consumption route. Base routes do not clear DLC
overrides; anonymous/dynamic/native callers, assets absent from Src, consoles,
timing and incomplete old DLC remain blind spots. Send any new seam back only
if it is outside this completed exact receipt; 99 still waits for 03b, 04 and
any child 04 declares.
