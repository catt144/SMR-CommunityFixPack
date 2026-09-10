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
