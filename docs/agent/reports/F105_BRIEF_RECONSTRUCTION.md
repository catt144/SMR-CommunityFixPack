# The F105 brief, reconstructed — and why its structure worked

**What this is.** The owner asked (2026-08-24, after the fix shipped) for the
prompt that drove the F105 session to be regenerated as a report so its
STRUCTURE can be reviewed — it accomplished something the project had tried and
failed at for a long time. The brief, `docs/agent/prompts/F105_LANDSCAPE_COSTS.md`,
was authored 2026-08-23, was never tracked (it sat untracked in the working
tree), and was consumed and deleted by the session it drove (commit `78619f6`),
so git holds no copy. **Part 2 below is reconstructed from that session's own
verbatim read of the file at its start** — faithful in every section, heading,
table and rule; a phrase here or there may have drifted. Part 1 is the
structural analysis, written with the benefit of what happened AFTER the
session too (F106 refuted, F107 found and repaired, the attended A/B repro,
the 1.0.x upload).

---

## Part 1 — What the structure did, mapped to what actually happened

### 1. One issue, one session, an explicit fence — and "file, do not fix"

The brief opened with *"Your whole job is F105"* and closed the scope in §5 with
a rule that had teeth: *"Something interesting out of scope → FILE IT, DO NOT
FIX IT."* That single rule is what contained the session's one serious error.
The class-builder derivation (F106) was WRONG in its premise, and it implicated
a shipped module (F33). Because the fence forbade touching any other module,
the wrong derivation became an ENTRY with a one-line settling probe, not a
"repair" of a working fix. F106 was filed and refuted by measurement the same
day; nothing shipped on it. A brief without that fence would have let the
session "fix" `Fix_SmallLandscapeSites` on a false premise.

### 2. "Re-derive the ROUTE, not the citations" — and "overturning this brief is a success"

§2 presented the mechanism as numbered steps with line cites, then said:
*"If a line number below is right but the path to it is wrong, the finding is
wrong. Say so loudly."* Walking the route (not checking the cites) is what
found that the Efficiency laws were NOT triggers (every cited line was correct;
the path from a law to the sweep did not exist), that
`ClearWasteRockConstructionSite` shares the crash, that `TerrainPaint` is
latent-only, and which milestone it was. Framing a correction as the BEST
outcome removed the pull to confirm the filed entry.

### 3. A ranked clue list with ONE decisive clue and a pre-stated decision rule

§6 was ordered by value, and the top of the brief said: *"the single most
valuable thing you can settle is clue 1 … If it goes the way I suspect, the fix
shape currently recommended is the WRONG one."* Then it gave the rule in
advance: *"if two or more unguarded readers are reachable, guarding one is the
wrong fix"* → flip to the writer. That turns an open-ended investigation into a
decision procedure with a known output. The session ran exactly that: nine
reader sites, each read in its enclosing function, one verdict each, and the
shape question answered by the rule rather than by taste.

### 4. "What this does NOT establish" as a task list

§3 listed, item by item, what the evidence could not support (never
reproduced; which tech; other subclasses; other readers; what the site was).
Every one of those became a task with a recorded verdict. The list was more
useful than the evidence section it followed, because it told the session where
the truth was thin.

### 5. Hunches labelled as hunches, with a return on refuting them

*"A hunch you refute is a result; record it either way."* The story-bit hunch
(different effect class?) was refuted with the class body cited; the
construction-group hunch was settled. Labelling protects the reader from
inheriting a guess as a fact — the same lesson `recorded facts are claims too`
encodes.

### 6. Stop conditions framed as PERMISSION, not failure

§9: *"Report and stop rather than pushing through, if …"* with five concrete
triggers, and §7's *"If your findings change what 72 should decide — say so at
the top and stop."* Owner decisions stayed the owner's. It also made the
mid-session ruling easy to absorb: §0 already said *"If checklist 72 has been
answered since this was written, the owner's ruling overrides §7,"* so when the
ruling arrived by message the session had a rule for it instead of a dilemma.

### 7. The vocabulary fence — "What you may NOT claim"

§10 fixed the words: never "reproduced" without your own log line, never
"guarded" from a grep line (read the function), "refuted" requires the
condition was SAMPLED, never a count you did not compute, never dismiss a log
line as "not ours." Those rules shaped the entry's language directly — the
session wrote "tested-unattended, menu-only" and "⛔ never reproduced on the
rig," which is exactly what let the NEXT session know what was still owed and
go do it (the attended A/B legs).

### 8. A read path with file granularity and a WHY column

§0's table gave each required file a reason to read it. That is cheaper than a
reading list and better than a summary: it front-loads context without
pre-digesting it. The one line of path trivia (*"the installdir is literally
`Project Spark`"*) saved a search that had cost earlier sessions a session.

### 9. The live todo requirement

§1 demanded a todo list before any reading, one item per commit-and-verify
unit, updated the moment each completes, *"because the owner reads this list to
decide when to step in."* The harness had no todo tool that session; the list
lived in a repo-root file. It still did its job: the owner's ruling arrived
while clue 1 was in progress, and the list let the session re-plan in place.

### 10. Enumerated deliverables, including self-consumption

§11 named six outputs, the last being *"`git rm` this file in the closing
commit."* A brief that deletes itself cannot go stale, cannot be re-run by
accident, and forces everything it carried to be written into durable records
(entry, report, facts, checklist) before it disappears.

### What the structure did NOT catch — for the next brief

* **Verification was priced as a boot `applied` line.** That price cannot see a
  dead branch: the shipped module's per-leaf `prev` capture was `nil` (F107),
  the guard branch worked, and `applied` printed. A brief that ships code should
  ask for one DISPATCH reading (call the wrapped path and read the effect —
  WORKFLOW's R7), not just the install line.
* **"Recorded facts are claims too" was written about inherited facts; it
  needed to say the same about derivations made THIS session.** F106 came from
  reading the class builder — outside the brief's map — and treating that read
  as settled enough to shape the fix. The refutation came from a measurement a
  day later. A line like *"a derivation you make today is a claim until one
  read of the running game agrees with it; if the fix's SHAPE depends on it,
  measure first"* would have caught both F106 and F107 before they shipped.
* **The §2 mechanism was numbered and cited, which invites re-derivation; the
  fix-shape reasoning in §6 was prose, which does not.** Making the shape
  argument a numbered chain with its own "what this does not establish" would
  have exposed that "one wrap covers every subclass" rested on an unverified
  assumption about WHEN the pack applies.

---

## Part 2 — The brief, reconstructed

> Reconstructed 2026-08-24 from the consuming session's verbatim read.
> Structure, headings, tables and rules are exact; a phrase may have drifted.

# F105 — the landscaping construction-cost crash. One issue, one session, dig.

♻️ **SELF-CONSUMING.** `git rm` this file in your closing commit, naming its grave.

**Your whole job is F105.** A field-reported crash we derived from a reporter's
log and **have never reproduced.** You have one issue, no deadline pressure, and
permission to read as widely around it as you like. The owner's words for what
they want from you: *"examine the code around it, nearby it and anything that
could be linked to it and see if it can shake something loose."*

⚠️ **The single most valuable thing you can settle is in §6, clue 1.** If it goes
the way I suspect, the fix shape currently recommended on checklist 72 is the
WRONG one and you will have saved us shipping a repair that covers one crash site
out of several. Read that clue before you plan.

---

## 0 · Read path — file granularity, per `WORKFLOW.md` §8

**Staleness check first.** This brief was written at commit `HEAD` of 2026-08-23.
Another session may have moved F105 since:

```
git log --oneline -15 && git pull
git log --oneline -- docs/agent/bugs/F105.md docs/PLAYTEST_CHECKLIST.md
python tools/doccheck.py
```

⛔ If checklist **72** has been answered since this was written, the owner's
ruling overrides §7 below. Read it before planning.

**Required reads, in this order:**

| File | Why |
|---|---|
| `docs/agent/STATE.md` | Mandatory every session. Note the `## Post-launch issues` block at the top. |
| `docs/agent/bugs/F105.md` | The entry. Everything below is its expansion, not a replacement. |
| `docs/agent/bugs/F104.md` | The same day's other report. Same misattribution, unrelated cause — read it so you do not re-derive it. |
| `docs/agent/facts/EF-014.md` | ⭐ Where the game source is, and the proof that shipped Lua **is** `Src`. |
| `docs/agent/facts/EF-065.md` | Why our name is on the player's warning box. Not your job to fix, but you need it to reason about the report. |
| `docs/agent/facts/EF-066.md` | Its unswept question is **the same shape as this defect**. See §6 clue 6. |
| `docs/agent/bugs/F49.md` | Search it for `construction_costs_at_start` — this project has met that field's lifecycle before, in the "Recorded latent" block. |
| `docs/agent/FIX_POLICY.md` | §3a save safety, §4 intent-and-reachability. Binding on anything you propose. |
| `Code/Fix_MilestoneCrash.lua` | The module whose frame put our name on the box. |
| `Code/Fix_SmallLandscapeSites.lua`, `Code/Fix_LandscapeUnitFilter.lua` | Our only two landscape-touching modules. Clear them or implicate them (§6 clue 5). |

**Game source** (`EF-014`, and the path is not guessable):

```
A:\SteamLibrary\steamapps\common\Project Spark\ModTools\Src
```

⚠️ The Relaunched Steam `installdir` is literally **`Project Spark`**. Any search
under a "Surviving Mars Relaunched" folder name finds nothing. The old 2018 game
at `...\common\Surviving Mars` is a decoy with a `ModTools` folder and no `Src`.

**Attached by the owner:** the reporter's log
`Mars.exe-20260824-00.01.27-6a22b86d.log`. Read it yourself; §3 quotes it but
quotes are not evidence.

---

## 1 · 🗒 Live todo list — REQUIRED, and required to stay current

**Create it before you start any reading**, covering the whole job.

⚠️ **One item per commit-and-verify unit.** If a stage produces its own commit or
its own verification run, it is its own item. Never bundle. If a stage turns out
to contain more units than this brief anticipated, **expand it in the list at
that moment.**

- Mark each item complete **the moment it completes**, never as a batch.
- Exactly one item in progress at a time.
- Rewrite the list when reality diverges.
- Put useful state in the item text — which sweep, what the last read said — so
  the list answers "where are we" without reading the transcript.

**The owner reads this list to decide when to step in.** A stale list is a wrong
answer to that question, and this job is long enough that they will look.

---

## 2 · What is established — but ⛔ re-derive it, do not inherit it

⛔⛔ **`recorded facts are claims too`.** This project has been wrong in both
directions inside one week with every cited line correct both times. So:
**re-walk the ROUTE, not just the citations.** If a line number below is right
but the path to it is wrong, the finding is wrong. Say so loudly if you find that
— overturning this brief is a success, not a failure.

The mechanism as currently understood, all at `ModTools\Src`, game **1.0.7.396349**:

1. `ConstructionSite` declares `construction_costs_at_start = false` as its
   **class default** — `Lua/Buildings/ConstructionSite.lua:32`, commented
   *"for ui, since requests don't keep total and total may change due to modifiers."*
2. The only thing that makes it a table is
   `ConstructionSite:GatherConstructionResources`, at `:640` (`= {}`), filling it
   per-resource at `:653`.
3. `LandscapeConstructionSite:GatherConstructionResources`
   (`Lua/Landscape/LandscapeConstructionSite.lua:105-155`) **overrides** that
   method. It sets `self.construction_resources = {}` at `:146` and chains only to
   `ClearWasteRockConstructionSite.GatherConstructionResources` at `:154` — which
   (`Lua/Landscape/ClearWasteRockConstructionSite.lua:140-170`) also never touches
   the field. **The parent's initialiser never runs.**
4. `construction_resources.WasteRock` *is* populated — `:203`, `:216`, `:220` —
   so the site carries a truthy `construction_resources[res]` beside a
   `construction_costs_at_start` that is still the boolean `false`.
5. `ConstructionSite:RefreshConstructionResources` (`:665-684`) guards on
   `construction_resources[resource]` and then indexes the boolean at **`:673`**.
6. Class chain: `LandscapeConstructionSite` → `ClearWasteRockConstructionSite` →
   `LandscapeConstructionSiteBase` → `ConstructionSite`, so the
   `AllMapsForEach(true, "ConstructionSite", …)` sweep reaches it.
7. **Trigger:** `Effect_ModifyLabel:OnApplyEffect`
   (`Lua/MarsGameEffects.lua:174-176`) — any label matching `_Construction$` runs
   `RefreshConstructionResources` over every construction site on every map.

**Believed carriers of such effects** (⚠️ **enumerate this properly yourself — my
grep was not exhaustive and I said so**): techs at `Data/TechPreset.lua:685`,
`:1004`, `:2366+`; laws at `Data/LawDef/LawDef-Efficiency.lua:315-371`. Files
containing `Effect_ModifyLabel` at all: `TechPreset.lua`, `GameRuleDef.lua`,
`MissionSponsorPreset.lua`, `CommanderProfilePreset.lua`. ⚠️ `Data/StoryBit/FoodFight.lua`
carries `_Construction` **labels** but appeared to use a different effect class —
**verify, do not trust that.** A story bit would be a far more common trigger than
a tech.

---

## 3 · The evidence, and exactly how far it reaches

From the reporter's log, quoted so you can check my reading against the file:

```
[LUA ERROR] Lua/Buildings/ConstructionSite.lua:673: attempt to index a boolean value (field 'construction_costs_at_start')
  Lua/Buildings/ConstructionSite.lua(673):  method RefreshConstructionResources
  Lua/MarsGameEffects.lua(175):   <>
  [C](-1):  method MapForEach
  CommonLua/Core/map.lua(1049):  global AllMapsForEach
  Lua/MarsGameEffects.lua(174):   <>
  CommonLua/Classes/GameEffect.lua(38):  method EffectsApply
  Lua/Research.lua(313):  method SetTechResearched
  Lua/Research.lua(841):   <>
  Lua/Tech.lua(457):  global GrantResearchPoints
  Lua/Milestones.lua(180):   <>
  Mod/SMR_CommunityFixPack/Code/Fix_MilestoneCrash.lua(73):  global CompleteMilestone
  Data/Milestone.lua(340):   <>
Locals:
  self | LandscapeConstructionSite at (189500, 167138, 10000) on map 1
  resource | string WasteRock
  construction_resource | userdata …
  cost | number 0
```

Session config from the same log: rules `UnlockedPolicies, ColonyPrefab,
NoPassagePenalty, DiscoverBreakthroughs` (**no `FreeConstruction`**, so the `:667`
guard does not spare it); sponsor IMM; map `BlankBig_03`; 6 mods.

**⛔ What this does NOT establish, and you must not write as if it does:**

- **We have never reproduced it.** Zero rig captures. Everything is source-reading
  over one stranger's log.
- **Which tech completed** is unknown. Only that its effects carry a
  `*_Construction` label.
- **Whether other `ConstructionSite` subclasses share the gap** — unswept.
- **Whether other readers of the field crash the same way** — see §6 clue 1. This
  is the big one and it is open.
- **What that particular levelling job was** — a player levelling job, a mystery
  set-piece, a mod-created site? Unidentified. `Fix_SmallLandscapeSites` exists in
  this pack for a reason; see clue 5.

---

## 4 · Why the pack was named (context only — ⛔ NOT your job)

`Fix_MilestoneCrash.lua(73)` is our copy's `Msg("MilestoneCompleted", id)` — the
line vanilla has in the same place (`Lua/Milestones.lua:134`). Our replacement is
byte-equivalent on this path, so **vanilla throws identically, log-only, with no
popup.** The box exists only because `OnMsg.OnLuaError` (`Mod.lua:3001-3013`)
matches any loaded mod's `content_path` anywhere in the crash text — its own
comment calls it a *"rough estimation based on call stack"*. `EF-065`(a).

⛔ **The attribution problem is checklist 73 and is NOT in your scope.** Do not
redesign `Fix_MilestoneCrash`, do not touch `ReportModLuaError`, do not implement
trampolines. If your work turns up something that bears on 73, **write it in your
report and leave it.**

---

## 5 · Scope fence

**In scope:** the `construction_costs_at_start` contract and everything that
reads or writes it; `ConstructionSite` and every subclass of it; the
`Effect_ModifyLabel` `_Construction` sweep and its trigger set; reproducing the
crash; specifying the fix.

**Out of scope:** F104 / Passage Network (closed, not ours). Checklist 73 and the
blame surface. Any other module in the pack. The opt-in pack.

**Something interesting out of scope → FILE IT, DO NOT FIX IT.** A new entry in
`docs/agent/bugs/` (or a fact in `docs/agent/facts/`) and a line in your report.
That is the rule and it has teeth: `F10` is this project's monument to fixing
something nobody could reach.

---

## 6 · Clues, leads, and everything we ever thought about this

Ordered by what I think is worth most. Some of these are hunches — they are
labelled. **A hunch you refute is a result; record it either way.**

### Clue 1 ⭐⭐⭐ — THE ONE THAT MATTERS. Are there other unguarded readers?

The checklist currently recommends **guarding the reader** in
`RefreshConstructionResources`. That recommendation assumes `:673` is the *only*
place a landscape site can reach an unguarded read of this field. **I did not
verify that, and the raw grep says it is probably false.** Every reader I found:

| Site | Guarded? |
|---|---|
| `ConstructionSite.lua:1084` `local costs_at_start = self.construction_costs_at_start` | unknown — read the use |
| `ConstructionSite.lua:1491` `if self.construction_costs_at_start and …BlackCube` | ✅ guarded |
| `ConstructionSite.lua:1615` `assert(self.construction_costs_at_start)` | ⚠️ **an assert** |
| `ConstructionSite.lua:1616` `for r_n, amount in pairs(self.construction_costs_at_start)` | ⛔ `pairs(false)` throws |
| `ConstructionSite.lua:1628` `self.construction_costs_at_start and …[resource] or 0` | ✅ guarded |
| `ConstructionSite.lua:2711` `local res_amount = (self.construction_costs_at_start[res] or 0)` | ⛔ **unguarded index** |
| `ResourceOverview.lua:812` `local target = site.construction_costs_at_start[resource_type]` | ⛔ **unguarded index** |
| `TrainDisasterHandling.lua:139` `local total = cgl.construction_costs_at_start[res] or 0` | ⛔ unguarded (track group, may not apply) |
| `Track.lua:646-651` | reads then **assigns** — tracks have their own writer |
| `BlackCubesBuildingInteractionsModFriendly.lua:28` | ✅ guarded |

**The question to answer:** can a `LandscapeConstructionSite` reach `:1616`,
`:2711`, or `ResourceOverview.lua:812`? `ResourceOverview` is a UI path — if a
levelling site appears in the resource overview, that is a crash a player could
hit by *opening a panel*, with no tech involved at all, and it would be far more
common than the reported one.

⇒ **If two or more unguarded readers are reachable, guarding one is the wrong
fix** and the recommendation flips to initialising the field at the writer
(giving `LandscapeConstructionSiteBase` the `= {}` its parent sets), which repairs
every reader at once. **Settle this before you spec anything.**

⚠️ Note `:1615`'s `assert`. The developers believed the field was always a table
by that point. That is evidence the **override is the anomaly and the readers are
written to a contract** — which argues for fixing the writer. Weigh it.

### Clue 2 ⭐⭐ — sweep every `ConstructionSite` subclass for the same gap

The defect class is *"a subclass overrides `GatherConstructionResources` without
running the parent's initialiser."* Enumerate every subclass and check each.
Known neighbours: `ClearWasteRockConstructionSite`,
`LandscapeConstructionSiteBase`, `TerrainPaintConstructionSite`. There will be
more. ⚠️ **`MicroGHabitatBase` is a known precedent for exactly this kind of
copied-omission** — `Fix_DomeFreeSpaceMismatch`'s header records it having the
identical omission as `Dome:RefreshFreeLivingSpaces`. Same author habit, different
file. Look for it here.

### Clue 3 ⭐⭐ — `cost = 0` in the locals tells you the fix is safe

`GetConstructionCost("WasteRock", mod_o)` returned **0** for that site. Landscape
sites do not use the normal construction-cost system at all — their work is
volume-based (`wr_required` / `wr_produced`, `LandscapeConstructionSite.lua:105-145`).
⇒ There is genuinely **nothing for `RefreshConstructionResources` to refresh** on
such a site, which is why skipping is correct rather than merely convenient. If
you take the writer fix instead, confirm an empty `{}` produces the same no-op.

### Clue 4 ⭐ — this project has met this field before

`F49`'s **"Recorded latent (wave-5 screening, no fix)"** block, on
`BreakTrackElement` (`Track.lua:643-652`). It documents that
`cgl.construction_costs_at_start` is **`false` at group creation** and gets
assigned `{}` on first touch, and that a `DivRound(cost, res)` typo there is
unreachable *because* of that lifecycle. Read it: it is the same field, a
different call site, and a prior careful reading of when it is and is not a table.
⚠️ It also records that the reachability analysis there was **wrong once and
corrected**. Do not inherit its conclusion; use it as a map.

### Clue 5 ⭐ — clear our own two landscape modules, or implicate them

`Fix_SmallLandscapeSites` wraps `L:GetClosestDests`; `Fix_LandscapeUnitFilter`
replaces `LandscapeForEachUnit`. Neither should touch this field. **Confirm it
rather than assume it** — and check whether either can cause a landscape site to
exist in a state vanilla would not produce. If one can, this stops being purely
a vanilla defect and the entry needs rewriting.

### Clue 6 — the same shape as `EF-066`'s open question

`EF-066` carries an unswept worry about our own pack: we wrap ~60 (class, method)
targets and nobody has enumerated which have **shipped subclass overrides the
wrap never reaches**. F105 is *vanilla's own instance of that exact pattern*. If
your subclass sweep produces a reusable method, say so — it is directly
transferable, and it would retire a standing watch.

### Clue 7 — the trigger set decides how bad this is

A tech is rare and one-way. A **law** can be enacted and repealed repeatedly. A
**story bit** fires unpredictably. A **game rule / sponsor / commander** applies
at game start, when no levelling site can exist — probably harmless. Enumerating
which effect carriers are reachable *while a levelling site is on the map* is what
turns this from "one reporter's crash" into a priority. Do that enumeration.

### Clue 8 — hunches, explicitly labelled as such

- **HUNCH:** `:666`'s `if self.construction_group and self.construction_group[1] ~= self then return end`
  means only the group leader refreshes. A landscape site in a group might be
  spared, which would change what a repro needs. Unverified.
- **HUNCH:** the reporter's site at `z = 10000` and the `GeoscapeDome`/`DomeBasic`
  vocabulary in the *other* log suggest a mature colony. Irrelevant unless a repro
  fails on a fresh map, in which case revisit.
- **NOT CHECKED AT ALL:** whether `RefreshConstructionResources` has callers other
  than `MarsGameEffects.lua:175`. Sweep it. Another caller is another trigger.

---

## 7 · What you may build, and what you may not

⛔⛔ **DO NOT ship module code unless checklist 72 has been answered.** The owner
holds the fix-or-not ruling. Your deliverable is a **fix-ready spec**, not a
module — unless §0's staleness check shows 72 already answered, in which case
build the shape it names and nothing else.

⚠️ **If your findings change what 72 should decide** — and clue 1 could —
**say so at the top of your report and stop.** Re-routing a live owner decision
because the ground moved is the correct outcome, not a failure to finish.

**If you do build (72 answered only):** post-release cost rules apply — an
`items.lua` entry (`H-10` — a module absent from `items.lua` **ships absent**),
one boot `applied` line, doccheck counts. ⛔ Never quote `FIX_POLICY` §3a's
per-module cost for a single added fix (owner 2026-08-20, checklist 57).

---

## 8 · Reproducing it

Worth real effort — it is the one gap nothing else closes.

**Recipe to try:** a colony with no `FreeConstruction` rule → place a terrain
levelling job and let it sit unbuilt → research a tech carrying a
`*_Construction` cost modifier (or enact an Efficiency law that does) → watch for
`ConstructionSite.lua:673`.

⚠️ **Stale-probe gate — `WORKFLOW.md` §7 — binding if you record any test
result.** Run the probe sweep BEFORE testing, put the sweep line in your todo
list, and **refuse to record results without it.**

⚠️ `EF-056`: loading a **copy** of a campaign still runs that campaign's autosave
rotation and deletes the owner's autosaves. Pre-copy every autosave first.
⚠️ Cheats are normal on the playtest saves and are only a confound where a reading
intersects what they changed.

**If you cannot reproduce it, that is a result** — record what you tried and what
the negative rules out. ⛔ "Could not reproduce" does **not** downgrade the
entry: the log is a measurement and the derivation stands on its own.

---

## 9 · Stop conditions — permission, not failure

Report and stop rather than pushing through, if:

- Clue 1 shows multiple reachable unguarded readers ⇒ **checklist 72's question
  changed**; route it, do not answer it yourself.
- The subclass sweep turns up more than ~3 affected classes ⇒ this is a defect
  *class*, not an entry, and wants an owner decision on scope.
- You find the mechanism is **not** what §2 says ⇒ stop, rewrite the entry, report.
  Overturning this brief is the best outcome available to you.
- Any fix shape you can find would need to change persisted state ⇒ `FIX_POLICY`
  §3a, and that is an owner call.
- A repro requires anything destructive to the owner's saves ⇒ ask.

---

## 10 · What you may NOT claim

- ⛔ **Never `tested-attended` without a human at the keyboard**, and never a
  screen claim without an attended witness. `tested-unattended` for real launches
  with nobody watching. Bare `tested` is legacy and closed to new work.
- ⛔ **Never write "reproduced" without a log line you produced yourself**, quoted
  with its file name.
- ⛔ **Never write a count, md5 or byte figure you did not compute.**
- ⛔ **Never call a reader "guarded" from a grep line** — read the enclosing
  function. That is exactly the mistake that would make clue 1 come out wrong.
- ⛔ **"Refuted" requires the condition was SAMPLED**, not merely that a count
  came back zero.
- ⛔ Do not report a log line you cannot explain as "not caused by our leg" and
  move on. Report it with its age. Every pushback on that habit in this project
  has found a real defect.

---

## 11 · Deliverables

1. **`docs/agent/bugs/F105.md` updated** — front matter `updated:`, and the body
   carrying what you established, what you refuted, and what stays open. If the
   mechanism changed, rewrite it; do not append a correction to a wrong body.
2. **A report** in `docs/agent/reports/` — the sweeps, the enumerations, the
   negative results. Reports are not authority: where a report and the entry
   disagree, the entry wins or the report is corrected in the same change.
3. **New entries/facts** for anything filed out of scope.
4. **Checklist 72 updated** if your findings change the question — in
   `docs/PLAYTEST_CHECKLIST.md` under "Decisions waiting on you", never only in an
   agent doc.
5. **`python tools/doccheck.py` GREEN** before you commit. It is a pre-commit hook
   (`git config core.hooksPath tools/hooks`) and red blocks.
6. **`git rm` this file** in the closing commit.

⚠️ PowerShell 5.1 traps that have cost this project time: `git commit -m` with
embedded double quotes splits arguments — use `-F <file>`. `Get-Content` /
`Set-Content` mangle this repo's no-BOM UTF-8 docs — use the Edit tool, or
`[System.IO.File]` with `UTF8Encoding($false)`.
