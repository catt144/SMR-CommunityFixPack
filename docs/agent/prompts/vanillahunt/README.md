# vanillahunt — the chain manifest

Effort: find what game **1.1.0.403908** BROKE in the game itself, by diffing the
archived 1.0.7 tree against the archived 1.1.0 tree at function granularity and
reading the changes by risk class. Authored 2026-09-09 by `smr-bugfixpack-c3`
under `prompts/VANILLA_DIFF_HUNT.md` (consumed by the authoring commit; find it
with `git log --diff-filter=D --format=%h -- docs/agent/prompts/VANILLA_DIFF_HUNT.md`
and read `git show <that-sha>^:docs/agent/prompts/VANILLA_DIFF_HUNT.md`).
Method: `agent/reports/CHAIN_METHOD.md`. Authoring mechanics: `agent/WORKFLOW.md`
"Authoring a prompt" elements 1–8.

> ⚖️ **THE THESIS, in the owner's words:** *"when they patch things they usually
> create 2 new bugs for every one they fix … they are famous for not correctly
> judging how old features will interact with new ones."*
> ⭐ The target is **the unannounced change and the interaction seam**, never
> "read the changelog and check it". A patch note is a claim about intent; the
> diff is what actually happened. ⚖️ Owner rule 09-08: a patch note saying
> "Fixed" is a CLAIM, false until we confirm it.

⛔ **SCOPE: VANILLA DEFECTS, NOT OUR MODULES.** The pack's own re-verification is
`reports/PACK_1_1_0_REVERIFICATION.md` and it is done. A finding here is a
**candidate defect, FILED** (`bugs/C##.md`); it is never automatically a module.
`FIX_POLICY` §4 and the owner decide what becomes a fix — the pack has just shed
36 modules for good reasons. ⛔ No link in this chain adds a module.

## ⛔ What this hunt CANNOT see — stated first, not buried

Every link inherits this list and repeats it in its close-out. A "nothing found"
inside a blind spot is not a result.

1. **Anything not in `ModTools\Src`.** Entities, maps, textures, sounds, the
   localisation packs (`Local\<Language>.fpk`, `EF-063`), and any content that
   ships only inside an `.fpk` with no Src counterpart.
2. **The engine.** `Mars.exe` changed between builds `23584660` and `24995074`;
   every native function the Lua calls (`Landscape_ForEachObject`, hex grids,
   pathfinding, the serializer) may behave differently with no Lua diff at all.
3. **⚠️ Whether the game EXECUTES the Src we read.** Parity between Src and the
   executed `Packs\Lua.fpk` was proven for **1.0.7 only** (2,250/2,256 files,
   `WORKFLOW.md` "fpk verification"). ⛔ **It has NOT been re-run for 1.1.0.**
   Link 01 runs it first; until then every citation is a citation of the
   ModTools tree, not of the game. `EF-078`: trust runtime over source.
4. **Runtime-only behaviour.** Timing, thread interleaving, real-time vs
   game-time, UI hit-testing and input modes (FIX_POLICY §4: source reading has
   no validity there), balance, progression, console platforms (§7).
5. **The 1.0.7 archive's `DLC/` subtree** — 12 files against 1.1.0's 151, a
   Steam artefact of the branch switch. Excluded from every diff here; DLC-vs-
   DLC facts come from `prompts/DLC_DEEP_CHECK.md`'s chain.
6. **Generated data at function granularity.** `Data/`, `Lua/BuildingTemplate/`,
   `Lua/XDef/`, `Lua/ClassDefs/` are editor exports; a function-level differ
   reads them as noise. Link 01's second instrument diffs them at FIELD level
   instead, with its own falsifier and its own blind spots (a preset consumed
   by C-side code has no Lua reader to find).
7. **Semantics moving under an UNCHANGED body** — the F117 shape (see class
   (b′) below). The inventory sees the callee's signature change; it cannot see
   that a caller two calls away silently kept the old contract unless that
   caller is enumerated. Class (b′) is the mechanical pass that tries; a callee
   reached through a dynamic dispatch (`self[name]`, a preset's `func` field,
   `Msg` handlers) is outside it.

## 0 · Preconditions — all DONE at authoring; every link RE-CHECKS the pin

| what | state | how a link re-checks |
|---|---|---|
| 1.1.0 tree archived | ✅ `C:\Dev\SMR-SrcArchive\1.1.0.403908\Src`, 4717 files, digest `a4577da2…45b2`, Steam build `24995074` | `MANIFEST.sha256` beside it; README in `C:\Dev\SMR-SrcArchive\` |
| 1.0.7 tree archived | ✅ `C:\Dev\SMR-SrcArchive\1.0.7.396349\Src`, 4448 files, digest `09d95e34…9921`, Steam build `23584660` (`EF-083`) | same |
| installed build = archived 1.1.0 | ✅ `appmanifest_3215050.acf` `buildid 24995074` (checked 2026-09-09 by this session and by `smr-bugfixpack-05`) | ⛔ **re-read the appmanifest at link top.** A different buildid ⇒ ARCHIVE THE NEW TREE FIRST (standing rule), then STOP AND ASK — the inventory's 1.1.x side is pinned to `24995074` and a re-pin is a chain decision, not a link's |
| the diff is measured | ✅ from the two manifests, excluding nothing: **2444 changed**, 1968 identical, **305 added**, 36 removed | link 01 re-derives these from the manifests as its first control — the numbers must match or the archive moved |
| fpk parity on 1.1.0 | ✅ **DONE 2026-09-10, and PERFECT** — `EF-085`: 4,564/4,564 non-DLC Src files ship byte-identical in `Packs\Lua.fpk`/`Data.fpk`, **0 divergent, 0 absent** (against 1.0.7's 2250/2256-with-5). ⇒ blind spot 3 above is CLOSED for the bytes: every `1.1.0 file:line` this chain writes cites bytes the install ships. ⛔ Still not proof the game EXECUTES them (`EF-078`), and it says nothing about `Mars.exe` | `python tools/flpk_extract.py`-based re-run; `EF-085` carries the route. Re-run after any buildid change |

⭐ **MEASURED 2026-09-09 (authoring session), the shape that sized this chain**
— re-derive in 01, do not inherit:

| bucket | files | note |
|---|---|---|
| changed, `DLC/` excluded | 2437 | all `.lua` |
| of which generated/data (`Data/`, `Lua/BuildingTemplate/`, `Lua/XDef/`, `Lua/ClassDefs/`) | 1630 | `Data/StoryBit` alone is 514 — `presetdiff`'s rows, read by 04's registry agents |
| of which hand-written | 807 | `Lua/` 155 · `Lua/Buildings` 139 · `CommonLua/Classes` 76 · `CommonLua/Libs` 71 · `CommonLua/` 59 · `CommonLua/Data` 30 · `CommonLua/X` 30 · `CommonLua/Editor` 28 · `Lua/Scenario` 26 · `CommonLua/Core` 25 · `Lua/Units` 22 · `CommonLua/Ged` 20 · `Lua/X` 20 · `CommonLua/UI` 18 · `Lua/UI` 17 · `Lua/Mysteries` 11 · `Lua/Landscape` 10 · `Lua/Construction` 8 · the rest under 8 each |
| function-declaration lines across the 807 (max of the two trees) | ~28,250 | the inventory's upper bound on rows; the changed subset is what the links read |
| removed files | 36 | tutorials 1–5, `CommonLua/Classes/Mod*.lua` (the old modding backend), `Flight.lua`, `Notifier.lua`, five `XDef` dialogs incl. `ResearchDlg` and `CommandCenterLifeSupportGridsOverview`, `ClassDef-Conditions`/`-Factions`, `InteriorAmbientLife.lua` — ⛔ each is a class (d)-or-(e) question, 04's agent D |
| added files | 305 | 138 are `DLC/norman`; 31+31 `XDef` pairs; 20 `CommonLua/Libs`; 17 `Lua/`; 8 `Lua/Buildings`; 7 `Lua/AmbientLife` — class (f), 04's agents by system |

## 1 · The queue

| # | file | model | owner needed? | what it drains |
|---|---|---|---|---|
| ~~01~~ | ~~`01_INVENTORY.md`~~ | Opus | no | ✅ **DONE 2026-09-10** (`smr-bugfixpack-04`). fpk parity **PERFECT, 0 divergent** (`EF-085`) ⇒ no row carries `FPK-DIVERGENT`. `tools/treediff.py` + `tools/presetdiff.py`, both importing `luafn.find_bodies`, both `--selftest` 16 PASS / 0 FAIL and broken-on-purpose once each. Five TSVs in `reports/vanillahunt/`: INVENTORY 9,832 · PRESETS 37,512 · CALLERS 4,096 · STORAGE 1,155 · FILES 202. `TRIAGE.md` §0 written and CLOSED. Manifest re-derivation MATCHES §0 (2437+7 / 1963+5 / 166+139 / 36+0). **Seeded positives 4/4 by the tool.** ⭐ 2,465 `same`-against-changed-sig call lines (9 against a pure-`sig` callee); `Landscapes` GameVar→MapVar found mechanically; the "removed" modding backend was MOVED. ⛔ Known holes: 8,473 indented declarations (4,883 in `hand` files) covered by neither instrument; 133 `SPAN-SUSPECT` rows; delimiter fix routed as checklist **135**. ⭐ **Amended 2026-09-10 (authoring session, on the owner's ask):** the indented hole was MEASURED — 2,033 of the 4,142 in changed hand files were always covered by their outer body's hash, 2,109 were not — and `treediff` **v1.1** now enumerates those orphans (`INDENTED` / `ONE-LINE` flags, hash-matched so insertions cannot cascade). `INVENTORY.tsv` re-emitted 9,832 → **11,742** rows, other TSVs banner-only; selftest 22 PASS, broken on purpose once; seeds still 4/4. `TRIAGE.md` **§0.13** has the numbers. Still uncovered: anonymous `function(` literals |
| ~~02~~ | ~~`02_TRIAGE.md`~~ | Opus | no | ✅ **DONE 2026-09-10** (`smr-bugfixpack-b6`). Every INVENTORY/PRESETS/CALLERS row carries a system and ONE link (03 / 04-A…E), 0 UNASSIGNED, 289 files placed by hand with reasons; three `*.tagged.tsv` (01's files untouched); `TRIAGE.md` §1–§4. dlc-adjacent tag TWO-TIER (stated deviation: the literal list would have fenced 2,918 Lua + 8,209 preset rows off from 04). **3,699 hand body rows classified by 24 judgement agents, 0 without a verdict**; seeds **4/4 by content, 2/4 by strict label** (parent ruling in §2.1); blind 20-row self-sample WR/CHURN 20/20; round 2 on 295 rows WR/CHURN 99 %. Unit D: 8 F117-SHAPE candidates (`GetTransportRoute` ×4, `ActionFX:GetLocObj` ×4), 2 unsure — three parent rulings were CORRECTED by agents (drift to 99). README §2b FR tags by function; NOROWS.tsv's 123 row-less hand files bucketed as text-diff items. ⚠️ B01–B15 briefed before §2b (no PERF tell); B12.r2 issued, not ingested |
| ~~03~~ | ~~`03_SEAM.md`~~ | Fable (rec); run by Codex | no | DONE2026-09-10:396 complete present-span reads,6 complete caller contracts; C56-C62 cand/source-read; desk C56/C57/C59. Required split below; original seam set is NOT cleared. SEAM_REPORT/SEAM_COVERAGE, TRIAGE §03. Parent random sample6/6 changes,5/6 initial route precision; zero eligible seeds |
| 03b | `03b_SEAM_PRESETS.md` | Fable (rec) | no |360 generated INVENTORY +1,618 PRESETS across49 registries +6 CALLERS; field/consumer and generated-twin seams |
| ~~03c~~ | ~~`03c_PROGRESS_SEAM.md`~~ | Fable (rec) | no | **DONE 2026-09-10:** 286/286 read; C63-C65 filed; DeepScanning route connected; no child queue |
| ~~03d~~ | ~~`03d_CALLER_SEAM.md`~~ | Fable (rec) | no | **DONE 2026-09-10:** 283/283 read (249 INVENTORY + 16 CALLERS + 18 NOROWS); C66-C73 filed; no child queue |
| 04 | `04_HUNT.md` | **Codex Sol Ultra** (owner-assigned 09-10) | no | the second parent-orchestrates-agents link, everything not tagged (g): one agent per system (turf · colony · engine · storage+removed/added) and one per preset registry, each under its own binding reading order; the parent verifies one finding per agent from the trees, files, and commits every agent report verbatim to `reports/vanillahunt/agents/`. ⚖️ **Does NOT split** (owner, 09-10) — the whole plan runs in one orchestrator, committed as it goes |
| 99 | `99_TERMINAL_AUDIT.md` | **Fable** (rec) | ✅ raises the kickoff | adversarial backward QA: re-derive a sample of findings from scratch against the agent reports, re-falsify both instruments by planting fresh changes, rule on whether the inventory was SOUND, score the controls, measure the surface sweep's real reach, sweep the not-reached lists, empty the folder, end with the `DLC_DEEP_CHECK.md` kickoff line |

**03 split,2026-09-10:** 03b/03c/03d are first-class continuations of03's
required ~400-row stop. Their rows are disjoint per SEAM_COVERAGE.tsv; they may
run independently of one another and04, coordinating shared-file writes.99
waits for ALL of them and any declared children. No04 split rule was changed.

**Ordering.** 01 → 02 strictly (02 reads 01's TSVs). **03 and 04 are
independent of each other** — either order, or in parallel by two sessions;
they share no rows (02's partition is disjoint by construction) and no files
except the ledger, which each appends to under its own named section. 99 last,
on a folder holding `99` + this file. ⛔ **Choose the shape before link 1, not
after link 5** (`CHAIN_METHOD` §5a): inside 04 each agent compounds within its
own system (the question "what did every changed function in this system
assume?" is the yield), and systems do not compound across each other enough to
pay for serialising them — which is what makes them agents rather than links.

⭐ **Deviations from the brief's suggested split, stated per `CHAIN_METHOD` §3.**
(1) The brief proposed *"classes (a)/(b) their own link; the rest by system."*
Class (a) is **most of the inventory** and cannot be one context, and a reader of
"all class (a) rows" has no system in its head. So the reading partitions by
SYSTEM (disjoint), with CLASS as the sort order inside each, (a)/(b)/(b′) first.
Class (g) stays its own link because it is a TAG across systems, not a system,
and it is the owner's thesis — the one judgement a per-system agent cannot make.
(2) The generated data is read: the brief's blind-spot list would have written
off 1630 of the 2444 changed files; they are Lua-form preset data and a
field-level differ reads them, so 01 builds that second instrument beside the
first — same author, same falsifier discipline. (3) **Consolidated 8 → 5 links
on the owner's question of 2026-09-10** (*"do some of these do similar things
where multiple could be one leg that utilises sub agents?"*). The four
per-system reading links were the same job on disjoint row sets, and the
preset-reading link was that job on presets; they are now 04's agents, and
their reading orders survive verbatim as per-agent briefs. What the
consolidation costs, said plainly: 04's parent must plan its agents from 02's
counts BEFORE spawning and commit that plan, it files every surviving entry
itself, and 99 can only audit 04 through the agent reports — so committing
those verbatim is a chain rule, not hygiene. ⚖️ **The owner then ruled (same
day) that 04 does not split and runs on Codex Sol Ultra**, whose specialty is
large subagent coordination; the pre-split clause was removed from 04 and its
stop condition became "commit the plan and the reports, mark the unrun agents,
stop" — so a resumed orchestrator picks up from committed state. (4) **The
surface sweep** (owner, same day): every body an agent opens for any reason is
also read for a `FIX_POLICY` §4 tell, and a hit is filed `PASSING` whether or
not the diff caused it (§3 below). It widens the read only to bodies someone
was opening anyway; 99 measures that reach so nobody mistakes it for a sweep of
the unchanged tree.

⭐ **Model placement — the OWNER's at five links (`CHAIN_METHOD` §4.0: five or
fewer, the owner assigns; "(rec)" in the table is this Fable session's
recommendation, bodies are model-neutral).** ✅ **04 is ASSIGNED: Codex Sol
Ultra** (owner, 2026-09-10) — the heaviest session, handed to the model built
for large subagent coordination; its brief is written tool-neutral for that
reason. Recommended for the rest: 03 and 99 on the top tier. 03 because the
seam is the thesis's home and a thin read there yields nothing an audit can
recover; 99 because it is the fresh-context adversary. 01 is NOT recommended
top-tier despite being load-bearing: it ships with falsifiers that 99 re-runs
and a seeded control that 02 scores — its errors are CAUGHT downstream, which
is the placement rule. ⚠️ Cross-vendor: 99 audits 04's work through the
committed `agents/` reports and the filed entries, never through a session
transcript — the same discipline a Claude 04 would have been held to, and the
reason those reports are a chain rule. Routed as checklist **134** for the
remaining three.

## 2 · The risk taxonomy — binding sort order for every row

Every class is one this project has **already been bitten by in a single
update**. That is the whole argument for using them as the sort order.

| class | shape | our scar |
|---|---|---|
| **(a) body changed, name + arity identical** | invisible to every instrument we own but `bodycheck` | `F114` (157 throws, a player found it), `F116` |
| **(b) signature changed** | a parameter added, usually leading | `F115` (`map` prepended to `LandscapeForEachUnit`) |
| **(b′) callee contract changed, a CALLER kept the old one** | the callee's signature or argument meaning moved; a call site in the SAME tree still passes the old shape — the developers' own F117 | `F117` (`ChooseDome(traits…)` → `ChooseDome(colonist…)`; our caller kept `traits`; **a vanilla caller could have too**). Added 2026-09-09 from `smr-bugfixpack-0f`'s handoff: *"what found it was diffing the CALLERS of functions we call, not the functions themselves"* |
| **(c) storage moved** | same concept, new home | `Landscapes` GameVar → MapVar; walk consts `const.` → `g_Consts` |
| **(d) RENAMED, not removed** | the name is gone, the feature is not | low-Food warning → `StarvingColonists`; `daily_update_func` → `DailyUpdate` |
| **(e) removed outright** | genuinely gone | 36 of our modules retired against this |
| **(f) new function / new call site** | new code, least-tested code | — |
| **(g) ⭐ OLD × NEW SEAM** | existing system meets new feature | **the owner's thesis — weight this highest** |

Two derived shapes the links must also sort for, because they are where the
thesis predicts yield and no class above names them:

- **(h) "they fixed it — what did the fix touch?"** The 36 retired modules
  (`PACK_1_1_0_REVERIFICATION.md` §1 REMOVE bucket, `VANILLA_FIX_QA.md` §0,
  headers at `git show 2dc1dbe^:Code/<module>.lua`) name 36 functions the
  developers changed ON PURPOSE. Two-new-bugs-per-fix predicts the neighbourhood
  of each — the callers, the siblings, the state the fix now writes. Links 05/06
  read those neighbourhoods FIRST.
- **(i) a guard added or removed.** A new `if x then` in 1.1.0 is a claim that
  `x` can be nil where it could not before — ask what else reads `x` unguarded
  (`C54`'s lesson in the other direction: before filing an unguarded read as a
  defect, count the unguarded siblings; `EF-005`).

⛔ **THE METHOD RULE, learned three separate times on 2026-09-08; it governs every
row you triage:**

> **A claim about what is ABSENT needs the presence side ENUMERATED.**
> *"grep found 0 hits"* can only prove the old **NAME** is gone — never that the
> **FEATURE** was removed. Search for the capability (the preset, the UI string,
> the voiced line, the overriding subclass, the inheriting class), not the
> identifier. The three instances: a "deleted low-Food warning" that was a rename
> (`C54`/ck121); a "class X no longer defines Y" where Y was inherited intact
> (F-8, `caller-count-must-count-inheritors`); an asymmetry argument counting 36
> guarded sites and never the 46 unguarded ones (`C54`, refuted same day).

⚠️ **Check `docs/agent/facts/INDEX.md` BEFORE filing any engine-semantics claim.**
`EF-005` already answered one of the above and two sessions derived past it.

## 2b · ⭐ Field-report surfaces — read these rows FIRST (owner, 2026-09-10)

Three player reports the owner put in front of the chain (Steam discussions,
posted as screenshots in the owner's session of 2026-09-10; the Linux one is
*"widely reported by users on Steam and Reddit and leaving them completely
unplayable"*). ⛔ A field report is a CLAIM about a SYMPTOM, not a cause. The
chain's job is to enumerate every diff-visible surface that could produce the
symptom, read those rows before any other, and say plainly which surfaces it
read and which it could not. **A report is never closed by a chain that found
nothing — only by a witness.**

**Tagging (link 02).** Tag rows `FR-1` / `FR-2` / `FR-3` (a row may carry
several) **by FUNCTION, not by file**: measured by link 01's session, a
file-level match over-tags 800–1,400 inventory rows per report and would bury
the signal. Tag the entry functions named below, then one hop of their changed
callees (`CALLERS.tsv` style). State the tagging rule and the counts in the
ledger. FR rows go to the TOP of every row list handed to 03 and 04; an FR tag
does not move a row out of its system — the owning reader reads it, first.

**FR-1 · ⚖️ HIGHEST — "Feeding the Future — doesn't work on Linux": every new
game crashes under Proton since the update.** (Steam, 2026-09-08; Linux Mint
22.2; every Proton from 9.0 to 11.02 plus experimental; the same regardless of
settings; the menu loads, starting a new game crashes.)
- ⛔ **What the chain cannot see:** the crash itself is almost certainly NATIVE
  — `Mars.exe`, D3D12 → vkd3d, the shader cache, a DLL (blind spots 1, 2, 4).
  Precedent **`F102`**: the last Proton-only failure was a hand-hacked material
  hanging the NVIDIA-under-Proton shader path, below Lua; the only Lua-visible
  part was WHICH entity got spawned. ⭐ **OBSERVED in one player's log**
  (posted in the Linux thread 2026-09-08; it is `MarsDebug.exe` running the
  mod editor's Preset Editor for 8 s and quitting normally, so it is NOT a
  crash log): the ENGINE detects Proton (`Proton/Wine: 11.0`), yet Lua's
  platform flags read `asserts, cheats, debug, desktop, editor, ged,
  goldmaster, paradox, pc, steam` — no `linux`. ⇒ a `Platform.linux` branch
  does not fire under Proton; a Lua-side cause must be code that runs on every
  Windows machine and hits a Wine/vkd3d gap, OR engine code that branches on
  the Wine detection Lua cannot see. Same log: NVIDIA GPU (as in `F102`, whose
  AMD Steam Deck control was negative) and `Failed activating D3D12 Dred` —
  D3D12's crash diagnostics are unavailable under vkd3d, so a device-removal
  crash would leave no reason behind.
- **What it CAN see — read in this order:** (a) every changed or new row on
  the path from "New Game" to the first sol — the `OnMsg.NewGame`,
  `NewMapLoaded`, `NewMapGenerated`, `PostNewMapLoaded` handlers, map
  generation (`MapGen`, `GenerateMap*`), `PreGameMission`, colony/city init,
  and the multi-map setup the `map` parameter and the `Landscapes` MapVar move
  point at; ⭐ any NEW call from those bodies into an engine/native function
  1.0.7 never made there is the prime Lua-visible suspect. (b) base-game code
  on that path that branches on the DLC (`IsDlcAvailable`, `norman`) — the
  thread title names the DLC; ⭐ does a NON-owner crash too? **03 owns (b).**
  (c) assets first spawned at new game that are new or changed in 1.1.0:
  `PRESETS.tsv` `none` / `added-preset` rows in `ParticleSystemPreset`,
  `ActionFX*`, lightmodel and entity registries, plus the render-setup Lua
  (`CommonLua/Classes/Lightmodel.lua`, `RenderFeaturesParams.lua`, option
  DEFAULTS such as the upscaler / DLSS / XeSS choice) — `F102`'s mechanism
  class. (d) `hr.*` engine settings applied at new game or on option apply.
- **Deliverable:** subsection **FR-1** in 04's `TRIAGE.md` section (a, c, d)
  and **FR-1(b)** in 03's — every FR-1 row read, its verdict, candidates
  ranked, a NOT-reached list. ⛔ "No Lua cause found" is written as the
  surfaces read, never as "not a Lua bug". ⭐ The falsifier that beats every
  source read is **evidence from one affected machine** (the owner's to obtain,
  checklist 136): Proton's own log (`PROTON_LOG=1 %command%` as a Steam launch
  option — Valve's documented switch, writing `steam-3215050.log` in the home
  folder; ⛔ route-check before any player is told) records the fault on the
  Wine side, where the game cannot; plus the game's own `Mars.exe` log. ⚠️
  **`EF-047`: the engine flushes a large log tail only at process EXIT**, so a
  hard crash can lose the game log's last lines entirely — quote that log for
  what is PRESENT (GPU, driver, Proton version, DLC load, how far startup got),
  never for where it stopped.
- ⭐ **Second report (Steam, relayed by the owner 2026-09-10): an INSTANT crash
  to desktop, persisting through uninstall/reinstall, on a confirmed clean
  no-mod install, with no crash report or popup of any kind.** What it settles
  and what it does not:
  - ⇒ **Not a mod, and not our pack** — vanilla.
  - ⇒ **Points further below Lua.** MEASURED here: vanilla Lua errors do not
    end the process — `F114`'s thread threw 157 times, every 6 s of game time,
    across a ~42-minute session, and the game kept running. A crash to desktop
    is the PROCESS dying, which a Lua error, on everything this project has
    watched, does not do. So the Lua-visible levers are the ones that can kill
    a process FROM Lua — (a)'s NEW engine/native calls (a C function handed a
    value it does not check), (c)'s new assets, (d)'s engine settings. **Read
    those rows ahead of the rest of FR-1.**
  - ⛔ **"No popup" does NOT discriminate.** The engine's Lua-error message box
    fires only when a MOD's path is in the error's stack (`EF-065`), so on a
    clean install a vanilla Lua error shows no popup either.
  - ⚠️ "Persists through reinstall" rules out damaged game files. Whether a
    reinstall also clears the Proton prefix and Steam's shader pre-cache for
    app `3215050` is UNVERIFIED here — route-check before anyone is advised to
    delete them.
  - ⭐ **The cheapest discriminators, for the owner to ask reporters**
    (checklist 136): does LOADING a save also crash, or only a new game
    (only-new-game ⇒ new-game / map-generation code, surface (a); both ⇒ the
    shared map-entry and render path, (c)/(d)); at WHICH moment (clicking New
    Game, the mission setup screen, the loading screen, the first frame of the
    map); does it stop with the DLC disabled in Steam (⇒ FR-1(b)); GPU vendor
    and driver.
- ⭐ **Third report + the DLC-off result (relayed by the owner 2026-09-10) —
  what is now ESTABLISHED, and it re-ranks FR-1.** The OP adds *"it keeps
  crashing even when all DLC content is disabled"*; a second player (Manjaro,
  KDE on Wayland, kernel 6.18, NVIDIA **GTX 1070**) crashes on new game in
  normal, sandbox AND challenge, after validating files, with no crash-report
  popup on relaunch.

  | varies across reports ⇒ not the cause | constant |
  |---|---|
  | distro (Mint 22.2, Manjaro) · display server (X11 Cinnamon, Wayland KDE) · kernel (7.0, 6.18) · Proton 9.0–11.02 + hotfix/experimental · in-game settings · game mode · DLC content on/off · mods (none) · file integrity (validated, reinstalled) | **1.1.0 · Proton · the moment a new game starts · NVIDIA on every GPU named** (RTX 3060 Laptop, GTX 1070; `F102`'s earlier Proton freeze was NVIDIA too) |

  - ✅ **CONTROL, MEASURED 2026-09-10: a new game on 1.1.0 WORKS on Windows +
    NVIDIA.** The owner's rig (RTX 4080, D3D12, per `F102`) started colony
    `BlankBig_02`; every save of it, its Sol-1 start included, carries
    `orig_lua_revision=403908` (headers read from
    `C:\Dev\SMR-SaveBackup\20260909-hotfix2-sitting\`). ⭐ **And it ran on the
    upscaler under suspicion — OBSERVED (owner's screenshots, 2026-09-10):**
    `OPTIONS / VIDEO` shows `Antialiasing: TAA`, `Upscaling: NVIDIA DLSS 4`,
    `Resolution Percent: Native (100%)`, `Graphics Adapter: NVIDIA GeForce RTX
    4080`, 3840×2160 fullscreen; the owner states all 1.1.0 testing ran this
    way. That also OBSERVES what was only read in source: on an RTX card the
    default TAA auto-picks DLSS 4. ⇒ **DLSS 4 itself works on NVIDIA; not
    "NVIDIA", not "DLSS 4", but NVIDIA × Proton** — vkd3d-proton / dxvk-nvapi on
    NVIDIA's Linux driver — meeting something 1.1.0 does at new game, of which
    the upscaler's initialisation under Proton was the leading Lua-visible
    candidate (⛔ refuted as the trigger 2026-09-10 — the falsifier bullet below).
  - ⚠️ **The AMD side, partly filled (owner, 2026-09-10): Steam Deck players
    report NO problem.** That is consistent with NVIDIA × Proton — the Deck is
    AMD (RADV) — but `F102` warns a Deck negative is weaker than it looks:
    Valve pre-distributes the Deck's shader caches, and SteamOS pairs its own
    Proton with RADV. So a Deck "works" cannot separate "NVIDIA-specific" from
    "shader-cache or SteamOS-specific". ⭐ **The datum still missing is DESKTOP
    Linux on AMD** — one such report, working or crashing, splits the two
    (checklist 136). The project's own Deck test was dropped: it would only
    repeat what players already report.
  - ⇒ **FR-1(b) drops in rank:** a DLC-DEPENDENT branch is unlikely when DLC-off
    still crashes. ⛔ It does NOT clear 03's seam — base-game code changed to
    accommodate the DLC ships to everyone and runs with the DLC off. (How the
    DLC was "disabled" — the in-game content toggle or Steam — is unstated.)
  - ⛔ **REFUTED AS THE TRIGGER 2026-09-10 (falsifier bullet below); kept as the
    record of why it led. The lead the diff showed (surfaces c, d): the
    temporal upscaler.** 1.1.0 upgraded **NVIDIA DLSS 2 → DLSS 4**
    (`CommonLua/Core/options.lua`, the `Antialiasing` and `Upscaling` tables).
    The DEFAULT anti-aliasing is `"TAA"` (`CommonLua/Core/GlobalStorageTables.lua:114`),
    which *"automatically picks a temporal anti-aliasing technique based on the
    machine's GPU"* — `options.lua:210-228` hands TAA the DLSS, XeSS or FSR 2
    settings (read its conditions), and the DLSS entry is selectable only when
    `hr.TemporalIsTypeSupported("dlss")`. So every NVIDIA player on default
    settings initialises an upscaler at the first 3D frame. ⚠️ **The GTX 1070
    cuts against "DLSS 4 alone":** it cannot run DLSS (the game's own help text
    says it "requires an NVIDIA RTX graphics card"), so its TAA falls back — the
    honest surface is **the auto-pick, the capability probe, and whichever
    upscaler they initialise**. Also new in 1.1.0: NVIDIA's **REBLUR / NRD
    denoiser** (59 `REBLUR*` parameter lines in
    `CommonLua/Classes/RenderFeaturesParams.lua`, 0 in 1.0.7; `NRD` 0 → 2
    files) — whether any new-game code path writes those `hr` values is a
    question for (d). Minor: a new `FilmGrain` option whose values set no `hr`
    key.
  - ⛔ **COVERAGE HOLE this exposes — measured, and now a generated list.** The
    DLSS 2 → 4 change sits in a top-level DATA TABLE in a `hand` file:
    `treediff` emits functions and `presetdiff` reads only the `generated`
    bucket, so **neither instrument lists it**. Measured (`treediff` v1.2,
    2026-09-10): **123 changed / added hand files have ZERO inventory rows
    with real content** — top-level option / config / const tables, and preset
    data stored OUTSIDE the four `generated` prefixes (`CommonLua/Data/` 28
    files, `CommonLua/Libs/` 26, mostly their `Data/` and `ClassDefs/`
    folders). They are listed in **`NOROWS.tsv`** (`reader=NONE`,
    `content=yes`); link 02 hands them to 04 as TEXT-DIFF items, because no row
    exists to tag. **FR-relevant files in that list — read AS TEXT first**
    (normalised changed lines in brackets):
    FR-1 — new-game map generation: `CommonLua/Libs/MapGen/Data/MapGen/MapGen-Default.lua`
    (12), `MapGen-SubProc.lua` (42), `MapGen-Tools.lua` (2),
    `CommonLua/Libs/MapGen/Data/__const.lua` (6); render and scene:
    `CommonLua/Data/LightmodelFeaturePreset.lua` (**new**, 37),
    `CommonLua/Data/PersistedRenderVars.lua` (11), `CommonLua/Data/__SceneParamDef.lua`
    (29), `Lua/Config/render.lua` (10), `CommonLua/Core/ProceduralMeshShaders.lua`
    (2), `CommonLua/X/XShaderEffect.lua` (1); config and consts:
    `Lua/Config/config.lua` (40), `CommonLua/Core/config.lua` (6),
    `Lua/__const.lua` (347); the path to a new game: `Lua/XTemplates/PGMainMenu.lua`
    (2, the pre-game menu), `Lua/UI/LoadingScreen.lua` (2). Plus the TABLE
    parts of files that do have rows: `CommonLua/Core/options.lua` (the DLSS
    pick, 1.1.0 `:210-228`), `CommonLua/Core/GlobalStorageTables.lua`,
    `CommonLua/Classes/RenderFeaturesParams.lua`, `CommonLua/Core/Postprocessing.lua`,
    `Lua/ProjectOptions.lua`.
    FR-2 — `Lua/Units/RCSensor.lua` (4), `Lua/Buildings/SurfaceDeposit.lua` (2).
    FR-3 — `Lua/Config/pathfind.lua` (55), `Lua/Config/_pfclasses.lua`
    (**new**, 63).
  - ⭐ **Player-side falsifier AND candidate workaround (checklist 136):** before
    New Game, change anti-aliasing from the default `TAA` to the non-temporal
    `SMAA` or `FXAA` — `NotSelectableTemporalUpscalingOption` then rules DLSS,
    XeSS and FSR 2 out. If new games then start, the temporal upscaler path is
    the trigger and there is a workaround to publish; if they still crash, the
    upscaler is cleared and (a)'s native calls lead. ⛔ Untested. Route half
    walked (owner's screenshots): the setting is `OPTIONS / VIDEO →
    Antialiasing`, and `Upscaling` shows the upscaler TAA picked. Still to walk
    before any player is told: that `SMAA` / `FXAA` is selectable there and that
    `Upscaling` then stops showing DLSS.
  - ⛔ **FALSIFIER FIRED 2026-09-10 — the temporal upscaler is REFUTED as the
    trigger.** Two Steam replies relayed by the owner (whether two players or
    one is not established): *"Tried FXAA and also just setting
    antialiasing/upscaling off entirely. Still crashes on "New Game", no
    change."* (thread post #13), and a player on NVIDIA already launching with
    *"anti-aliasing completely off (all graphics minimum, everything off that
    can be off)"*, still crashing. Source confirms the setting takes effect
    (1.1.0 `CommonLua/OptionsObject.lua:348-370`, `SyncUpscaling`): with `Off` /
    `FXAA`, `IsTemporalAntialiasingOption` is false, so at Native 100% the
    `Upscaling` option is forced `Off` (`ResolutionUpscale = "none"`) and below
    100% DLSS / FSR 2 / XeSS are `not_selectable` (`options.lua:668-685`) — no
    temporal upscaler is APPLIED. ⚠️ What survives, weakly: the capability
    probe `hr.TemporalIsTypeSupported` runs at every PC boot whatever the
    setting (`options.lua:209-230`, `OnMsg.Autorun`), but it ran identically on
    1.0.7 (archive `:216-218`) and runs at startup while the menu works, so it
    is no lead for a New-Game-moment crash; the engine's native DLSS 4 library
    load is below Lua and a menu setting cannot exclude it. ⇒ **As
    pre-registered above: (a)'s NEW engine/native calls on the New-Game path
    now lead** — map generation first (the `MapGen` NOROWS files in the list
    above; agent B21's double `ResumePartialPassEdits` note in 04's inbox),
    then (c) new assets / lightmodel (`LightmodelFeaturePreset.lua`, new) and
    (d) `hr.*` settings. There is no settings workaround to publish.
  - ⭐ **A reporter's `Mars.exe` log, OBSERVED 2026-09-10 (pasted in the thread):**
    the same executable as ours (`Timestamp 6a91a190`, cf.
    `archive/logs/first110_Mars.exe-20260908-15.20.28-6a91a190.log`),
    `Proton/Wine: 9.0`, Wine-reported `Windows 10 10.0.19043`, i7-6700K 4/8,
    32 GB — and it ENDS at `*** Debug::Init()`. Ours continues 0.1 s later
    (`Steam initialized`, the GPU block at 2.07 s, Lua at 4.6 s; `:24-52`).
    That game reached the menu and New Game, so this is `EF-047` seen in the
    field: after the hard crash only the first flushed block survived, not even
    the GPU line. ⇒ the game log carries NO crash location; **`PROTON_LOG=1` is
    now the only player-side instrument that can.**
  - ⚠️ **"Does loading a save also crash?" cannot be answered as asked:** a
    Linux player's saves are 1.0.7, which 1.1.0 on Steam refuses (`EF-079`),
    and a player whose every new game crashes has never made a 1.1.0 save. The
    discriminator needs a SUPPLIED save — a vanilla (no-mod) 1.1.0 Sol-1 save
    from the owner: loads and runs ⇒ the fault is in new-game map GENERATION
    (surface (a)); crashes too ⇒ the shared map-entry / render path. ⛔ The
    Proton save-folder location is unverified — route-check it before any
    player is told where to put the file (checklist 136).

**FR-2 · "Deep scanning with probes reveals no deep resources."** (Steam,
2026-09-08, two players; intermittent; one says a clean reinstall fixed it,
the other that it worked after more scanning.) Fully diff-visible — Lua and
presets.
- ⭐ **The route question, answered from BOTH trees:** on 1.1.0, does an
  orbital probe, and does sector scanning after the deep-scan tech, reveal
  deep deposits the way it did on 1.0.7? Name the tech, its effect, the reveal
  function and the state it writes, in both trees.
- **Read in this order:** the deep-scan tech preset — ⚠️ link 01 found the tech
  registry exists TWICE in 1.1.0 (274 `TechPreset` + 441 `Tech`, 258 ids under
  both classes, `TRIAGE.md` §0.10): is the deep-scan tech one of them, and whose
  effect is live? A tech defined twice is exactly how a feature silently stops;
  then the probe / exploration / sector-scan / deposit-reveal hand code; then
  class (c) — reveal state that became per-MAP (the `map` parameter, `Landscapes`
  GameVar → MapVar): "intermittent" and "a reinstall fixed it" read like state
  or ordering, not a deleted feature; then the `UndergroundDeepScanning*`
  storybits and the `DeepScan*` rows in `PRESETS.tsv`.
- **Deliverable:** subsection **FR-2** in 04's section: the route answer (yes /
  no / conditional, both-tree citations) and any candidate filed per §3.

**FR-3 · "Frame skip and stuttering", the same at lowest and highest graphics
settings.** (Steam, posted **2025-11-10 — before 1.1.0**; 16 comments.) ⚖️
**Owner, 2026-09-10: code-side causes are in scope.** A stutter that does not
move with graphics settings points at the CPU side — simulation, Lua threads,
garbage collection — which is code, not only engine.
- **What the diff can see:** 1.1.0 changes that ADD or SHORTEN periodic work —
  a new `CreateGameTimeThread` / `CreateRealTimeThread`, a shorter `Sleep` /
  `WaitMsg` interval, a new per-tick or per-frame loop over all units /
  buildings / grids, a new high-frequency `OnMsg` handler, a new UI rollover /
  infopanel update loop, new table allocation on a hot path. Any of those can
  WORSEN a stutter that already existed.
- ⛔ **What it cannot:** the ORIGINAL cause of a stutter reported ten months
  before 1.1.0 lives in code both trees share, or in the engine; no diff lists
  it and the surface sweep reaches only bodies someone opened. The whole-tree
  pass is routed to the owner as checklist 136; the chain must not report FR-3
  "not found" as "no code cause".
- Every agent that opens a body adds a **`PERF`** tell to its `SMELL` field when
  it sees one of the shapes above, changed or not. ⛔ A source read never
  measures frame time (`FIX_POLICY` §4, runtime-only): every FR-3 candidate is
  filed with a profiling falsifier and stays `cand`.
- **Deliverable:** subsection **FR-3** in 04's section: the added / shortened
  periodic work, with both-tree citations, and the `PERF` tells reached.

**99** answers each report in one plain-language paragraph in `HUNT_AUDIT.md`.

## 3 · What a finding must contain — the filing contract

A candidate defect entry `docs/agent/bugs/C##.md` (C-series; F-series only when
it is clearly player-visible AND the route is complete), carrying:

- the **route, re-derived** — ⛔ not the citation, the reasoning above it, with
  the ROUTE sentence tagged separately from its citations (`WORKFLOW` rule 2:
  MEASURED / SOURCE / INFERRED / INHERITED / GUESS, per row, never blanket);
- **1.1.0 `file:line` AND the 1.0.7 counterpart** — both trees are on disk, so
  a one-sided citation is a choice, and the wrong one;
- **who reaches it** — a real player action, or "no reachable caller found"
  with the search that proved it (`FIX_POLICY` §4 tiers R1–R4/U);
- ⛔ **the falsifier**: what observation would prove this is NOT a bug. A finding
  with no falsifier is a hunch with citations. ⭐ Prefer an EXECUTING falsifier:
  `tools/deskbench.py` and the `desk_*.py` pattern extract shipped bodies from
  BOTH trees with `luafn.find_bodies` and run them in real Lua (shims per memory
  `desk-harness-engine-shims`) — that is what settled F117 in both directions,
  including showing the obvious repair mis-scoring silently on 1.0.7;
- ⚠️ **the repro recipe derived SEPARATELY from the diagnosis.** F117's first
  control ("land beyond walking distance") was refuted by 99b — the far landing
  never reached the defective line. Fixing a defect exercises the code path and
  never the trigger; a control must make the TRIGGER fire, and its own
  vacuity condition must be named;
- **severity in player terms**, honestly: *"silent, no throw"*, *"cosmetic"* and
  *"only with the DLC installed"* are real and common answers; and for every
  DLC-adjacent finding, ⭐ **does it affect players who do NOT own the DLC?**

⛔ **Nothing is `tested`. A source read is never `tested`.** Every entry this
chain files is `cand` + `source-read` until something is reproduced in a game,
and most never will be. ⛔ Never move a status you did not witness.

⭐ **`DIFF-CAUSED` or `PASSING` — every entry says which (owner, 2026-09-10).**
The chain is diff-anchored, but every reader has bodies open: the two versions
of a changed function, its callers, its siblings, the consumer of a changed
preset. **A body opened for any reason is also read for a `FIX_POLICY` §4
tell** — dead code or dead validation (a computed value discarded, a guard that
cannot fire, a message nothing emits), a sibling contradiction, a self-
contradiction within one function or preset, an explicit dev comment saying it
is wrong. A tell is filed as a `PASSING` candidate with the tell named, whether
or not 1.1.0 caused it; no tell, no filing — the surface sweep is for tells,
not hunches. ⛔ It reaches only bodies someone opened; 99 counts that reach.
What it does NOT do: read the unchanged tree on its own account.

**Filing mechanics (route watched working 2026-09-09):** copy the front-matter
shape of `bugs/C55.md`; `seq` and `row` are the next free numbers READ FROM THE
INDEX AT FILING TIME (150/185 at authoring — peers file too); `status: "cand"`,
`status_source: "tag"`, heading tag `[cand <date> …]`; then regenerate the
generated index (never hand-edit it):

```
python tools/doccheck.py --regen
```

⚠️ **CORRECTED BY LINK 01, 2026-09-10.** This block used to hand-drive
`split_bugs.write_lines(...)` and say "a fact goes the same way with
`split_facts`". **It does not** — `split_facts` has no `write_lines`, so that
recipe fails on any fact. `--regen` is the one route: it rewrites
`bugs/INDEX.md`, `facts/INDEX.md` and `AGENTS.md` together, it is what
`doccheck`'s own RED tells you to run, and ⛔ it is never
`split_bugs.py --write` / `split_facts.py --write` (those re-run the retired
one-time migration).

`python tools/doccheck.py` must then read `BUGS INDEX: fresh` and `FACTS INDEX:
fresh`; red means the front matter and the heading tag disagree. For a fact,
keep `lines:` equal to the body length.

## 4 · Subagents — fan out the READING, keep the JUDGEMENT central

⚖️ Owner, 2026-09-08: where the work is large enough to warrant it, the hunts
split it across subagents. Rules, binding on every link that fans out:

- ✅ **Fans out freely:** classifying rows (read both bodies, return the row);
  one agent per FILE BATCH inside a system, never one per function; chasing one
  candidate to ground (callers, reachability, falsifier — returns a paragraph).
- ⛔ **Never delegated:** building or amending an instrument; setting or amending
  the taxonomy; synthesis, ranking, the verdict; ⛔ **ANY WRITE TO A SHARED
  FILE — subagents READ and REPORT, the parent writes.**
- ⛔ **`Explore` is the WRONG agent type for classification** — it locates, it
  does not review. Use `general-purpose` (or `claude`) for every judgement task;
  `Explore` only to find call sites.
- **What an agent MUST return, per row:** `file:function` · class · the 1.0.7
  and 1.1.0 line numbers · what actually changed, one sentence · who reaches it
  · the falsifier · the seam flag (which existing system, which new feature) ·
  **`SMELL`** — a `FIX_POLICY` §4 tell in EITHER body it opened, with the line,
  or `none` (the surface sweep, §3). ⛔ "Looks fine" and "no issues found" with
  nothing behind them are REJECTED results — re-issue the batch.
- **A hunt agent (04) additionally returns** entry-ready findings tagged
  `DIFF-CAUSED`/`PASSING`, a coverage section (rows given / read / NOT reached
  with reasons) and its `CHURN` spot check; **the parent commits the report
  verbatim** to `reports/vanillahunt/agents/` — 99's primary evidence.
- ⛔ **THE CONTROL.** *"Twelve agents found nothing"* is indistinguishable from
  *"twelve agents read badly."* Seeded positives are in the pool WITHOUT the
  agent being told: **`Lua/Units/Train.lua Train:UnloadAll`** (F114, class (a)),
  **`Lua/Landscape/Landscaping.lua LandscapeForEachUnit`** (F115, class (b)),
  **`Lua/Buildings/TrackElement.lua TrackGridElement:DemolishAndSplitTrack`**
  (F116, class (a)), and **`Lua/_GameUtils.lua ChooseDome`** (F117, class (b′) —
  its callers must come back enumerated). The parent scores the hit rate,
  re-runs a random sample of rows itself, and **reports both numbers in the
  ledger**. An agent pool that misses F115's added `map` parameter is not
  reporting on the other rows either.
- Subagents are parallelism WITHIN a link — ⛔ not a substitute for splitting the
  chain (rule 4 below) and not a substitute for the terminal audit.

## 5 · Binding chain rules — every prompt inherits these

1. **Staleness check first.** `git log --oneline -10`, `git pull`, `git status
   --short`, and `ListAgents` where your platform has it. Several sessions —
   Claude and Codex — edit this tree at once; a peer's unstaged file in `git
   status` is a lane you do not enter, and a peer's commit in `git log` since
   your prompt was written is a staleness check you run before acting on the
   prompt. Where a messaging tool exists, message the peer whose lane you are
   about to enter; where it does not, the git-visible claim in rule 15 IS the
   coordination. ⛔ Explicit FILE paths on every `git add` — never `add -A`, never a
   directory pathspec (both swept a peer's work on 2026-09-08) — **and on
   every `git commit`: `git commit -F <msg> -- <paths>`.** The index is shared
   between sessions and a bare `git commit` commits the WHOLE index: on
   2026-09-10 a peer's `6ad619a` carried this chain's staged rename and four
   deletions under its own message, minutes after they were staged. Explicit
   paths on `add` alone do not close that race; paths on `commit` do.
2. **Inbox / outbox.** Read `## Notes from upstream` at the bottom of your
   prompt before you start. On close-out, append your outbox to the NEXT
   prompt's `## Notes from upstream` **and** to `99_TERMINAL_AUDIT.md`'s, strike
   your row in this README, `git rm` your own prompt file, commit all of it
   together, push.
3. **Route, do not drop.** Anything out of your fence gets FILED (a `C` entry, a
   fact, a checklist item, a ledger "NOT reached" line), never fixed and never
   dropped. Unsure whose it is? **STOP AND ASK.** Every routed item carries
   **TAKEABLE WHEN <condition>**.
4. **Self-split at a clean commit boundary.** If the job will not finish
   comfortably in this context, commit what is done, write `NNb_*.md` as a
   first-class chain member with a FULL inbox, add its row here. Never push a
   job to the edge of a window — *"a chain cannot tell what its current context
   is"* (owner, 2026-09-08), which is why the splits below were made up front.
5. **Capture drift as evidence, not shame.** Every mistake you catch in your own
   or an upstream link's work — ten-second fixes included — goes to 99's inbox.
6. **Re-derive the ROUTE, always.** The recorded facts and the brief's numbers
   are design, not permission to skip verification. Every route failure this
   project has had sat on individually-correct citations.
7. **⛔ No instrument here is a clearance.** `treediff` sees text; `sigcheck`
   sees arity; a name sweep sees names; a field differ sees fields. Only a body
   read clears a body, and only a running game clears a behaviour.
8. **Live todo list, one item per commit-and-verify unit**, marked complete the
   moment it completes; exactly one in progress. The owner reads it to decide
   when to step in.
9. **Green gates before every commit:** `python tools/doccheck.py` GREEN, plus
   `python tools/treediff.py --selftest` and `python tools/presetdiff.py
   --selftest` from 01 onward; a WARN goes VERBATIM
   into your summary. `git commit -F <file> -- <your paths>` (embedded quotes
   split args under PS 5.1; the path list is rule 1's race guard), then push.
10. **⛔ Read-only on the game directory and on both archives. Always.** Nothing
    here needs `Mars.exe` running; nothing here writes under `Project Spark\`
    or `SMR-SrcArchive\` except a NEW archive folder when a newer build lands.
11. **⛔ Never move a status you did not witness.** A source read is never
    `tested`; a patch note saying "Fixed" is a claim.
12. **Bindings in force:** `H-02` (no Mod Editor, no `version` edit, no upload),
    `H-03`, `H-04`, `H-08`, `H-09`, `H-10`. ⛔ Never "correct" a 1.0.7 citation in
    an existing entry (`EF-075`): an entry records a defect in a STATED version.
    Owner decisions go to `docs/PLAYTEST_CHECKLIST.md` → "Decisions waiting on
    you", never only into an agent doc.
13. **STATE.md is byte-capped** (warn 12288, hard 18432; ⛔ never raise it — ck132
    is the owner's open call). Measure with `python tools/doccheck.py` (the
    `STATE + STUBS` line), never quote a number from here; add facts not
    stories; expect the WARN and evict per `prompts/STATE_EVICTION.md`.
14. **⛔ A subagent's result is a claim.** The parent verifies a sample from the
    primary artefact before writing it anywhere (memory: *a peer session's
    finding is a claim and so is your own*).
15. **Running 03 and 04 at the same time is designed for — on two shared
    surfaces it needs a protocol.** (a) `TRIAGE.md`: write ONLY inside your own
    named section, never reflow the file. (b) `bugs/INDEX.md` and the `seq`/
    `row` numbers: two sessions filing in the same minute can pick the same
    "next free" numbers. So, per filing batch: `git pull` FIRST, re-read the
    next free numbers from the index, create the entries, regenerate the
    index, commit `-- <paths>` and **push immediately — the push IS the
    claim** (tool-neutral: it works across vendors). A rejected push means the
    peer claimed first: pull, renumber your new entries to the next free
    numbers, regenerate, commit, push again. On a rebase conflict in
    `INDEX.md`, resolve it by regenerating (never by hand-merging) and re-run
    doccheck. Everything else the two links touch is disjoint by construction
    (02's partition).

## 6 · Artefacts

```
docs/agent/reports/vanillahunt/
  INVENTORY.tsv   01  one row per added/removed/body-changed/signature-changed top-level function (identical ones COUNTED, not listed)
  STORAGE.tsv     01  GameVar/MapVar/GlobalVar/PersistableGlobals/const-table declarations, both trees, moved/added/removed
  FILES.tsv       01  the 305 added + 36 removed files with a one-word bucket each
  CALLERS.tsv     01  for every class (b) row: its call sites in BOTH trees, each marked updated / unchanged / new
  PRESETS.tsv     01  field-level preset diff (PlaceObj id → key → 1.0.7 value → 1.1.0 value), churn RULE-classed and sampled
  NOROWS.tsv      01  (treediff v1.2, added 2026-09-10) every changed .lua file with NO inventory row — reader NONE/presetdiff, content yes/ws-only, normalised lines changed. The NONE+yes rows (123) are changed code no instrument lists; 04 reads them as text
  *.tagged.tsv    02  the two working copies with system / dlc-adjacent / class / SMELL columns (01's files untouched)
  TRIAGE.md       01 §0 counts · 02 §1–§4 ledger (counts, control scores, row lists per link and per 04 agent) · 03 and 04 APPEND a named coverage section each (reached / NOT reached; 04's per agent, plus its tooling gate table) · 03 writes "For dlccheck"
  agents/*.md     04  every hunt agent's report, verbatim, bannered (brief hash, wave, rows given) — the primary evidence 99 audits
  HUNT_AUDIT.md   99  the verdict
```

Findings live in `docs/agent/bugs/` as `C` entries (§3), never in the ledger.
The TSVs are generated: line 1 is a banner naming the tool, both tree digests and
the command; regenerate, never hand-edit. Commit them — the archives are not in
git, so the inventory is the only portable record of the diff.

## 7 · Chain-to-chain

`prompts/DLC_DEEP_CHECK.md` is the next authoring brief and it **shares the base-
game diff with this chain by design** (its §1.1: DLC-integration bugs surface in
the BASE-GAME diff). Link 03 writes the handoff section `dlccheck` consumes
(`TRIAGE.md` → "For dlccheck"), and 99's owner report ends with the kickoff line
for `DLC_DEEP_CHECK.md`. ⛔ The DLC chain must not redo 03's rows; this chain
must not read `DLC/norman` beyond what a base-game row calls into.

## Read path — declared

`docs/agent/STATE.md` (mandatory) · this README · `agent/FIX_POLICY.md` §2b, §4
· `agent/reports/CHAIN_METHOD.md` §3–§5a · `C:\Dev\SMR-SrcArchive\README.md` ·
`tools/luafn.py` (whole; 69 lines) · `tools/bodycheck.py` header (how a body is
hashed) · `docs/agent/facts/INDEX.md` (at minimum `EF-005`, `EF-075`, `EF-078`,
`EF-079`, `EF-083`) · `docs/agent/bugs/F114.md`, `F115.md`, `F116.md`, `F117.md`,
`C54.md`, `C55.md` · `agent/reports/PACK_1_1_0_REVERIFICATION.md` §1, §3 ·
`agent/reports/VANILLA_FIX_QA.md` §0 · your own prompt's inbox. Game source: the
two ARCHIVED trees, never the live install (which is byte-identical to the 1.1.0
archive while the buildid is `24995074` — re-check, rule 0).
