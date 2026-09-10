# 04 — the skim: a fast pass over everything 03 did not own, with drill-downs where something looks odd

⛔ ONE-SHOT: this file `git rm`s itself on close-out (README rule 2).
Model: **Codex Sol Ultra — owner-assigned 2026-09-10** · owner needed: no · after
02; 03 and its continuations are all closed, so nothing runs beside you.

> ⚖️ **OWNER RULING 2026-09-10 — 04 IS A SKIM, NOT AN EXHAUSTIVE READ.** *"I want
> 04 to still fire but I want it to be more of a skim, and if it sees something
> that looks odd in the skim it can do a deeper check in that area."* The owner's
> original framing of the hunt was a **high-level sweep of the diff**, not an
> exhaustive search. The earlier design of this link (every untagged row read: ~10,450
> inventory rows + 25,409 preset rows + 2,435 callers, roughly 19× the whole 03b
> leg) is RETIRED — `git show e2b0e22:docs/agent/prompts/vanillahunt/04_HUNT.md`.
> Why: the 03 family read 2,955 items to exact receipts and filed 20 candidates,
> none yet observed in play; the cost did not buy proportionate yield. ⛔ Do not
> rebuild the exhaustive design by the back door (per-row ledgers, "every row
> assigned exactly once", `04b` for a remainder). **This link does not split** (owner,
> 09-10): it is sized to fit one orchestrator session.

⚠️ **Written tool-neutral.** "Agent" = your platform's judgement-capable
subagent (reads bodies and reasons), never a locate-only search agent. Where the
README's chain rules name Claude Code tools, use the git-visible equivalents in
README rules 1 and 15.

## 0 · Open in this order

`git log --oneline -10` · `git pull` · `ListAgents` (if your platform has it) ·
`README.md` §2 (taxonomy — the flag vocabulary), §2b (the three field reports),
§3 (the `C` entry contract), rules §5 · `STATE.md` · `TRIAGE.md` §1.3 (per-system
counts), §1.7 (FR tags), §3 "04 agent A…E" (your MAP: which files changed in each
system — not an assignment list) · `FIX_POLICY.md` §4 (the tells) · your inbox
(`## Notes from upstream` below — its leads are your first drill-downs). Pin check
(README §0: `appmanifest_3215050.acf` buildid still `24995074`).

## 1 · 🗒 Live todo list, from your first action

One item per skim agent, one for the leads pass, one per drill-down batch, one
per filing batch. Exactly one in progress; the owner reads it.

## 2 · What the skim is

**Unit = a changed FILE** (hand-written Lua), a **REGISTRY** (presets), or a
**LIST** (storage moves, removed/added files). Per unit the agent looks at the
DIFF — `git diff --no-index` of the two archived copies, or that file's
`INVENTORY.tagged.tsv` rows with both line ranges — reads the changed hunks and
just enough context to understand them, and writes **ONE line**: `nothing odd`
or `FLAG: <what looks odd, file:line both trees>`. No per-row verdicts, no
per-row coverage ledger, no full-body reads unless a hunk cannot be understood
without one.

**What counts as odd — flag it** (README §2's classes, as triggers, not a checklist):
- a `FIX_POLICY` §4 tell in a changed hunk: dead code or dead validation, a sibling
  that does it differently, a body contradicting itself, an explicit dev comment
  ("TODO", "should", "hack", "temporary") on changed lines;
- a signature or argument contract changed while a caller visibly kept the old
  shape (the F117/F115 shape) — or a same-signature body that starts needing an
  argument (R08311's shape);
- storage moved (GameVar → MapVar, `const` → `g_Consts`) with a reader in view
  still using the old address;
- a function, preset key or file removed while something visible still names it;
- a new call into an engine/native function on the new-game / map-entry path (FR-1);
- new or shortened periodic work — a new thread, hourly/daily handler, a scan in a
  loop (FR-3 `PERF`);
- a new preset key with no Lua reader in view, or a removed key still read;
- an old system meeting a new feature (the owner's thesis, README §2 class g).
**Not odd:** balance and number changes by themselves, renames carried
consistently, whitespace/churn, text changes.

**Drill-down = the deeper check, only on a FLAG.** Read the flagged function(s)
in full in both trees, their callers (one hop, counting inheritors — memory:
caller counts must count inheritors), siblings, and the consumer that matters.
Return one verdict: **FILE** (entry-ready text per README §3: route, both
citations, reach, falsifier, recipe with its vacuity condition, severity,
`DIFF-CAUSED` or `PASSING`) · **REJECT** (why it is fine, with the line that
shows it) · **LEAD** (plausible but needs a running game or a DLC read — a note,
not an entry). **Budget: about 25 drill-downs for the whole link.** Rank flags by
likely player harm and drill the top ones; every flag you do not drill is listed
by name as `flagged, not drilled` in your section — that list is a result, not a
failure.

## 3 · The plan — commit it to `TRIAGE.md` "04" before spawning

**Leads pass first (parent, or one agent): drill these directly, no skim needed.**
1. **FR-1 (Linux new-game crash, the highest-priority report):** the map-generation
   set — `CommonLua/Libs/MapGen/Data/MapGen/MapGen-Default.lua`, `MapGen-SubProc.lua`,
   `MapGen-Tools.lua`, `CommonLua/Libs/MapGen/Data/__const.lua`, and agent B21's
   lead that `MapGen:ApplyPass` calls `ResumePartialPassEdits("MapGen")` twice
   against one `Suspend` (`CommonLua/Libs/MapGen/MapGen.lua` 1.1.0 :1160-1161).
   Then skim README §2b's FR-1 render/config list. ⛔ The temporal upscaler is
   REFUTED as the trigger; the crash is almost certainly native — say what the Lua
   side can and cannot show, and point at `prompts/FR1_LINUX_SITTING.md`, the
   owner's machine test that beats any source read.
2. **The 8 F117-SHAPE caller sites** (TRIAGE §3: `ColonistTransport.lua:114/123/136/141`
   `GetTransportRoute`; `_fixup.lua:1335`, `ActionFX.lua:2052/2821/3967`
   `ActionFX.GetLocObj`) and R08311 (`RocketBase.lua:966` omits `res_id`).
3. **The carried leads in your inbox below:** the F95 note (`RefreshAstrogeologistExtractorBonus`
   on `Percent == 20` vs 1.0.7's 10), R09089 / R09475 research-cost migration (not
   C76's `DiscoverTech` route), C62's missing authored ScriptStatements instance,
   R11004's universal-storage Seeds route, the F118 question (does any vanilla
   `Deactivate` caller reset `s_ConstructionControllerDeleteOnLoad`?), and `EF-083`
   (what else assumed drones reach a landscaping site).

**Skim agents (5, waves as you like), each told the flag list above VERBATIM:**
- **A · turf** (trains, landscape, construction, drones, logistics, depots) — its
  changed files, biggest first; the 64 `SMELL` rows TRIAGE lists get a one-line
  keep/drop each.
- **B · colony** (colonists, domes, services, rockets, disasters, story, save/load) —
  `_fixup.lua` / `SavegameFixups*` / `PostLoad` / `OnMsg.LoadGame` bodies FIRST
  (what a 1.0.7-era fixup does to a colony started on 1.1.0); 90 `SMELL` rows keep/drop.
- **C · engine** (`CommonLua`, UI) — first a one-line-per-subtree loader note
  (`shipped-runtime` / `dev-only` / `not in fpk`; ⛔ by the loader's line, never by
  the directory name) so dev tooling is skipped honestly; then runtime files; the
  90 `NOROWS` text-diff files are skimmed here as plain diffs; 191 `SMELL` rows keep/drop.
- **D · storage + removed/added** — `STORAGE.tsv` moved/removed rows and `FILES.tsv`:
  flag only where a reader of the OLD address or name is still visible
  (calibrate on `Landscapes`, `bugs/F115.md`); the 36 removed files: moved or gone?
- **E · presets** — per REGISTRY, not per row: skim `PRESETS.tsv`'s changed keys
  for the registry (churn classes skipped), flag removed-but-read keys,
  new-but-unread keys, type changes. Split the 123 registries across 2–3 agents by
  size; `StoryBit`, `BuildingTemplate`, `TraitPreset`, `XDef` first.

Retired-module neighbourhoods (the (h) seeds in TRIAGE §3) are skimmed by their
system's agent: glance at the neighbours of each 1.1.0 target for anything the
developers' fix disturbed; flag, do not re-audit the fix.

## 4 · What every skim agent returns (committed verbatim)

1. The skim table: `unit · nothing odd | FLAG: …` — one line per unit.
2. Flags ranked by likely player harm, each with both-tree citations.
3. `SMELL` keep/drop lines (A, B, C).
4. NOT skimmed: units it did not reach, by name, with the reason.
Commit each to `reports/vanillahunt/agents/<A..E>[-n].md` (banner: brief hash,
units given, date) — 99 audits against these. Drill-down results go to
`agents/drill-<nn>.md` the same way.

## 5 · The control — kept, because it is cheap

The four seeded positives are in the pool, and the agents are NOT told:
`Lua/Units/Train.lua` `Train:UnloadAll` (F114), `Lua/Landscape/Landscaping.lua`
`LandscapeForEachUnit` (F115), `Lua/Buildings/TrackElement.lua`
`TrackGridElement:DemolishAndSplitTrack` (F116), `Lua/_GameUtils.lua` `ChooseDome`
(F117). Score whether the skim FLAGGED each file (a skim that walks past F115's
added `map` parameter is not a skim). Also re-open 2 random `nothing odd` units per
agent yourself; report both numbers in your section.

## 6 · Parent duties

- Verify every **FILE** verdict yourself from the two trees before writing an entry
  (re-derive the route — README rule 6); a verdict that does not hold is REJECT, noted.
- File surviving findings as `C` entries per README §3 and rule 15's filing protocol
  (pull, next free numbers, `--regen`, commit, push immediately).
- A runtime check that needs a fresh 1.1.0 colony → ONE combined checklist rider at
  the end, TAKEABLE WHEN, not one per entry.
- Write `TRIAGE.md` section "04": the plan, per-agent units skimmed / flagged /
  drilled, the control numbers, the `flagged, not drilled` list, and short
  **FR-1 / FR-2 / FR-3** subsections (what was skimmed and drilled for each, what
  was found, what the source cannot show).

## 7 · Scope fence and stops

**In:** the skim, the drill-downs, filing, `agents/` reports, `TRIAGE.md` "04".
**Out:** `DLC/**` (the DLC deep check's), any `Code/` edit or module, any tool edit,
metadata/version. A finding implying a KEEP module is wrong on 1.1.0 → a hotfix-3
checklist item, never repaired here. 03's closed receipts are not reopened; a seam
you find in your units is yours to file.
**Stop when** the skim is done and the drill budget is spent, or the context runs
short: commit what exists, list the unskimmed units and undrilled flags by name,
close out. ⛔ No `04b`.

## 8 · What may NOT be claimed

`tested`. That a system or file is clean or bug-free. Any row-level coverage (the
skim is file-level; say "skimmed N of M files, drilled K flags"). That `nothing odd`
means safe. That a `LEAD` is a finding. That an FR report is closed.

## 9 · Close-out

Outbox to 99 (every finding with route and `DIFF-CAUSED`/`PASSING`, the skim and
drill counts, the control numbers, the not-skimmed and not-drilled lists, drift).
Strike your README row. Explicit-path `git add` of `TRIAGE.md`, each
`reports/vanillahunt/agents/*.md` by name, `bugs/C##.md` + `bugs/INDEX.md`,
checklist if a rider, README, 99; `git rm` this file. doccheck GREEN, both
selftests GREEN, `git commit -F <msg> -- <paths>`, push, and verify the push landed
(`git log origin/main -1` shows your commit).

> ℹ️ **The notes below were written for the retired exhaustive design.** Their
> row counts and "~250 rows per agent" sizing are context and a map of where the
> leads are — not an assignment. Their specific leads are live and feed §3.

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

## From completed 03b — presets and generated consumers, 2026-09-10

03b is exact and closed: **1,984/1,984** assigned items read (1,618 PRESETS,
360 generated INVENTORY, 6 CALLERS), with zero missing/duplicate/extra rows and
no child queue. Use `reports/vanillahunt/SEAM_PRESETS_REPORT.md` and its six
named per-key ledgers; do not reopen the receipt.

Do not duplicate **C75** (The Incident no-explosion construction lock) or
**C76** (`DiscoverTech` authored Cost rejected by the initiative-only helper).
Your R09089 `Research.ChangeResearchCost` and R09475
`SA_RevealTech.SAExec` rows touch the broader research-cost migration: judge
their discarded caller cost/fixed 20% boost independently from C76's narrowly
owned `DiscoverTech` route. C62's concrete authored ScriptStatements-instance
search and R11004's universal-storage Seeds acceptance/availability route also
remain yours.

FR-1/2/3 remain open. 03b found no native-particle crash mechanism;
DeepScanning's Tech/effect/Exploration route is connected; its PERF-only leads
are unprofiled and cannot explain the pre-1.1 report. For dlccheck, TAKEABLE
WHEN a concrete owner is read: added AmbientLife programs/building
`prg_class`, cross-map WorkFarmSmall, InsectFarming task completion,
Sugar/Spices flight-list registration, and official DLC Techs' new data shape.
Base routes do not establish DLC clearance. Send back only a genuinely new
seam outside the completed receipt; 99 now waits for 04 and any child you
declare.
