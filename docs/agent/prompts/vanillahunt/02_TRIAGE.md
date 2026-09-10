# 02 — triage: the parent orchestrating agents, not a session reading rows

⛔ ONE-SHOT: this file `git rm`s itself on close-out (README rule 2).
Model: Opus (recommendation; the owner assigns — README §1) · owner needed:
no · after 01, before 03 and 04.

> 🎯 You turn the raw inventory into a LEDGER the hunt links can work from:
> every row tagged with a system, the DLC-adjacent set built, body-changed
> rows in runtime files classified by a fan-out, the seeded-positive control
> SCORED, and per-link row lists written. **You do not hunt** — a row you
> find yourself chasing is a row you hand to 03 or 04 with a one-line note.
> ⭐ *"One session cannot hold 2444 files, but it can hold 2444 verdicts."*

## 0 · Open in this order

`git log --oneline -10` · `git pull` · `ListAgents` · `README.md` (binding, §2
and §4 especially) · `STATE.md` · `reports/vanillahunt/TRIAGE.md` §0 (01's
counts) · the four TSV banners · `bugs/F114.md`, `F115.md`, `F116.md`,
`F117.md` (so YOU know the seeds; the agents must not) · `facts/INDEX.md` ·
your `## Notes from upstream`. Pin check (README §0).

## 1 · 🗒 Live todo list, from your first action

One item per unit; the fan-out is several items (one per batch wave).

## 2 · Units

### A · System tags — mechanical, by path and by class prefix, in the parent

Add a `system` column to a working copy of `INVENTORY.tsv` (⛔ never edit 01's
generated file; write `INVENTORY.tagged.tsv` with its own banner). Systems, and
the 04 agent that owns each — this partition is BINDING on 03 and 04:

| system | what lands here | link |
|---|---|---|
| `trains` `landscape` `construction` `drones` `logistics` `depots` | `Lua/Buildings/Track*`, `Train*`, `Station*`; `Lua/Landscape/`; `Lua/Construction/`, `ConstructionSite`; `Drone*`, `Shuttle*`, `DroneControl`, `CommandCenter`; `*Depot*`, `Resource*`, `Storage*`, `Supply*` | 04 agent A (turf) |
| `colonists` `domes` `services` `rockets` `disasters` `story` `saveload` | `Colonist*`, `Trait*`, `Morale`; `Dome*`, `Residence*`, `Service*`, `Workplace*`; `*Rocket*`, `Cargo*`, `Trade*`, `Payload*`; `Disaster*`, `Meteor*`, `Dust*`, `ColdWave`; `Lua/Mysteries/`, `Lua/Scenario/`, `Sequences/`, `StoryBit*`; `_fixup.lua`, `SavegameFixups`, `Persist*` | 04 agent B (colony) |
| `commonlua` `ui` | `CommonLua/**` (all of it — 04's engine agent decides tooling by ROUTE, not you by path); `Lua/UI/`, `Lua/X/`, `Lua/XTemplates/` | 04 agent C (engine) |
| `removed-added` `storage` | every row from `FILES.tsv`; every row from `STORAGE.tsv` | 04 agent D |
| `preset:<registry>` | every `PRESETS.tsv` row with `churn-class = none`, tagged by the registry its `class` belongs to | 04 agents E, one per registry |
| `other` | whatever the rules above do not catch — ⛔ list them BY FILE in the ledger and assign each by hand with a reason; an `other` left unassigned is a row no link reads | you |

Rows tagged `dlc-adjacent` in unit B — Lua AND preset rows — leave every set
above and go to **03** instead. The partition 03 / 04-A / 04-B / 04-C / 04-D /
04-E is disjoint by construction; the ledger states each set's count.

A file may hold several systems' functions (`Building.lua`, `Dome.lua`,
`Colonist.lua` are 250–300 declarations each); tag by CLASS prefix where the
file is mixed, and say in the ledger which files you split.

### B · The DLC-adjacent tag — class (g)'s raw set, built in the parent

Tag `dlc-adjacent` every row — `INVENTORY` rows by 1.1.0 body or signature,
`PRESETS` rows by `class:id`, key, or value — that mentions any of:
`Food`, `Meal`, `Crop`, `Farm`, `Fungal`, `Bakery`, `Replicator`, `Restaurant`,
`Insect`, `Animal`, `Hunger`/`Starv`, `Consumption`, `FoodService`,
`norman`, `thomas`, `IsDlcAvailable`, `AssemblyOfPlanets`, `LawOffice`, `Law`,
`Policy`, `Tech` (preset injection), `Cargo`, `Resource` (new resources),
`ServiceBuilding`, plus every name declared in `DLC/norman/Code` or
`DLC/thomas/Code` (grep the declaration lines of those two trees ONCE, in the
parent, for the name list — that is the only read of `DLC/` this chain makes).
⚠️ A name match is not a dependency (`DLC_DEEP_CHECK` §1.2); the tag says
"03 looks", not "03 files". Count the set; it is 03's whole fence, and **03's
rows are removed from 04's lists** (disjoint by construction). Write the
tagged preset copy as `PRESETS.tagged.tsv`, own banner, 01's file untouched.

### C · The fan-out — classification of `body` and `body+sig` rows in `hand` files

⛔ Read README §4 again before spawning anything. Then:

1. **Batch by file, inside a system, ~150–300 changed rows per agent** (a big
   file alone, several small files together). One agent per batch,
   `general-purpose` type, run in parallel waves of 6–8. Each agent gets: the
   two archive roots, its row list (file · function · both line ranges), the
   taxonomy table from README §2 VERBATIM, the return format VERBATIM, and the
   instruction to read BOTH bodies with `python tools/luafn.py`-style spans (give
   it the `find_bodies` call, not a paraphrase). ⛔ It is NOT told which rows
   are seeds. ⛔ It does not write files.
2. **Required return, per row:** class (a)–(i) · what changed, one sentence ·
   seam flag (`old system × new feature`, or `none`) · a `GUARD` flag when the
   change adds or removes a nil-guard (class (i)) · a `WORTH-READING` flag with
   a one-clause reason, or `CHURN` with the reason (renamed local, reformat,
   moved helper, log string) · ⭐ **a `SMELL` field** — the surface sweep
   (owner, 2026-09-10): the agent has both bodies open, so if EITHER body
   meets a `FIX_POLICY` §4 tell (dead code or dead validation, a sibling
   contradiction, a self-contradiction, an explicit dev comment saying it is
   wrong) it names the tell and the line, diff-caused or not; `none`
   otherwise. A `SMELL` is not a finding — it is routed to 03/04 with the row
   as a `PASSING` candidate for the owning agent to derive. "Looks fine" ⇒
   reject the batch, re-issue with the rejection quoted.
3. **The control.** The four seeds are in ordinary batches. Score: did each
   come back with the right class and a sentence that names the real change
   (`map` prepended; the two nil-guards + `MultiResourceDepotBase`; the pre-sort
   `ProcessAllElements` + `skip_track_process`; the argument-type change)?
   **Hit rate, 0–4, into the ledger.** Below 4 ⇒ the pool read badly: re-issue
   the batches that held the misses AND a random 10 % of the others, and
   record both rounds. Then **re-run a random 20 rows yourself** from the raw
   bodies and score agreement — the second number in the ledger.
4. **Write verdicts as they arrive** into `INVENTORY.tagged.tsv` (parent
   writes; agents never do). Nothing is re-read from the agent's context.

### D · `CALLERS.tsv` — the (b′) pass, in the parent

For every `same`-call-line-against-changed-signature row: is the unchanged
caller REACHABLE (a `hand` file, not tooling) and does the signature change
alter what it receives (a prepended parameter shifts every argument; an
appended optional one may not)? Classify `F117-SHAPE` / `benign` / `unsure`
with one sentence each. ⛔ Every `F117-SHAPE` row is a **candidate**, filed to
the owning system's link with `TAKEABLE WHEN the link reads the caller's body`
— not filed as a `C` entry by you.

### E · The ledger — `TRIAGE.md` §1–§4

§1 counts: rows per class × system × bucket, `dlc-adjacent` count, `F117-SHAPE`
count, `F117-SHAPE` count, `GUARD` count, `SMELL` count, `WORTH-READING` vs
`CHURN`, preset readable-pile rows per registry. §2 the control: seeds hit
rate, self-sample agreement, batches re-issued and why. §3 **per-link row
lists** — "03" (the `dlc-adjacent` set, Lua + presets) and "04" broken down
per agent A–E — as file+function ranges pointing INTO the tagged TSVs (never
copied rows), (a)/(b)/(b′) first, then (h) seeds from the REMOVE bucket
(`PACK_1_1_0_REVERIFICATION.md` §1 — map each retired module's target
function to its system), then `SMELL` rows, then the `WORTH-READING` COUNT
per set — ⭐ 04 sizes its agents from these counts, so they must be exact.
§4 "NOT reached by triage": the `other` rows you could not place, the
`SPAN-SUSPECT` rows, the fpk-divergent rows, the churn-classed preset rows
(rule-classed and sampled by 01, unread here), anything an agent returned
`unsure`.

## 3 · Scope fence

**In:** A–E, `INVENTORY.tagged.tsv`, `PRESETS.tagged.tsv`, `TRIAGE.md` §1–§4.
**Out:** filing `C` entries (a classified row is not a finding — 03/04 derive
routes); reading any preset row for meaning (tagging is by name match);
reading `DLC/` beyond the one declaration-name grep; amending the taxonomy
(README §2 is set — if a row fits no class, `other` + a note to 99); touching
any tool.

## 4 · Stop conditions

Seeds hit rate ≤ 2 after the re-issue (the pool cannot classify — STOP AND ASK
before spending the rest of the budget) · 01's counts do not reproduce ·
more than ~40 batches needed (split: `02b_TRIAGE_COMMONLUA.md` takes the
`commonlua` system, full inbox, own row) · context half spent before unit D.

## 5 · What may NOT be claimed

That any row is a defect. That `CHURN` rows are safe (they are UNREAD, and
the ledger says so). That the seeds' hit rate covers `generated` or `DLC/`.
That a system with zero `WORTH-READING` rows is clean (name the agent count and
the row count instead).

## 6 · Close-out

Outbox to `03` and `04` (each: its §3 row list pointer, its (h) seeds, its
`F117-SHAPE` candidates, its `SMELL` rows, its `unsure` rows; 04's broken down
per agent with the counts) and to `99` (the control numbers, every re-issued
batch, every drift). Strike your row. Explicit-path `git add`:
`INVENTORY.tagged.tsv`, `PRESETS.tagged.tsv`, `TRIAGE.md`, README, 03, 04, 99;
`git rm` this file. doccheck GREEN, both selftests GREEN, commit `-F`, push.

## Notes from upstream

*(from the authoring session, 2026-09-09)* README §0's shape table is the size
argument for the batch counts above: ~807 hand-written changed files, of which
`CommonLua/**` is ~365 and `Lua/**` ~440. If the `body` row count for `hand`
files exceeds ~6,000, take the split in §4 up front rather than at batch 30.
