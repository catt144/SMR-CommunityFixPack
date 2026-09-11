# MIGRATION CLUSTER CHECK — are our colonist-migration fixes still right on 1.1.0, and what do we tell Paradox?

Paste into a fresh session (any model; the owner picks). Written **2026-09-11** by `smr-bugfixpack-e6`.
**Staleness anchor: HEAD was `3b880dc` when this was written.** Start with `git pull` + `git log --oneline -15`
and read what landed since; the records win over every specific below.

> ⚖️ **WHY THIS EXISTS — the owner's framing.** A Paradox developer (`ivanassen`) is going through the pack's
> fix list and merging what they can into the game. Their words, Steam, 2026-09-11:
> *"I've found most to be valid, a very small minority I couldn't reproduce (e.g. the farms's oxygen bonus to the
> dome leaking after the farm is destroyed), and some are quite broad and are probably fixed in many but not all
> cases, and not trivial to test (everything to do with colonist migration, for example)."*
> They are right to be cautious, and our own evidence says so (§1). **This job produces two things: our own
> corrected truth, and a report written FOR THEM** — per defect: what is broken, where in their code, how to
> reproduce it, what our fix does, and how sure we are.
>
> ⛔ **A wrong claim here is expensive.** It goes to the developers of the game under our name, after they have
> already caught one entry of ours that 1.1.0 had fixed (F37). **Prefer the narrower true sentence every time.**

## 0 · Orient (before touching anything)

1. `git pull` · `git log --oneline -15` · `git status --short` · `ListAgents`. **Several sessions edit this tree
   at once** and a peer's unstaged file is a lane you do not enter. As of writing, `items.lua` + `metadata.lua`
   are the owner's uncommitted Mod Editor pack (v8) and belong to the release session — **never touch them**,
   nor `perma/RELEASE_OUTBOX.md`.
2. **Read `docs/agent/STATE.md`** (mandatory kernel), then `docs/agent/FIX_POLICY.md` §2, §2a, §2b, §4, §4a.
3. Open a **live todo list** before starting — see §7.
4. ⛔ **This brief launches no game.** The in-play half is written as recipes for the owner's owed sitting
   (checklist 144 a). If you do end up recording a test, the STALE-PROBE GATE binds first:
   `grep -rln "TEMPORARY" Code/ ../SMR-BugFixPack-TestKit/Code/` must be zero, in the todo list, before results.

## 1 · What is already known — inherit this, do not redo it

Measured 2026-09-11 (`smr-bugfixpack-e6`), all re-checkable:

- **Mechanically current.** `python tools/bodycheck.py --all` reads OK on all 21 pinned rows across the eight
  modules; `python tools/sigcheck.py` reads 0 MISMATCH over 47 sites. ⚠️ The tools print their own caveat: an OK
  is **not** a clearance — a same-name, same-arity function with a changed BODY is invisible to both, and 13
  sites carry no pin at all (`sigcheck --coverage`).
- **The hotfix-2 re-read (2026-09-08/09) covered every module in this cluster** and changed five of them:
  `reports/PACK_1_1_0_REVERIFICATION.md` rows **K-2** (DomeFreeSpaceMismatch), **K-5** (ShuttleHubOffAvailable),
  **K-6** (ShuttleTransportCache), **K-13** (ArrivalDeaths), **K-21** (FreedHousingNotice); and
  `reports/HOTFIX_2_AUDIT.md` findings **F-1** (ArrivalDeaths threw on 1.1.0 → F117), **F-2** (StaleReservations
  had become an applies-today HARM to expedition crews), **F-3** (ShelterReflex half (a) dropped), **F-4**
  (DomeFreeSpaceMismatch no longer reaches its gate), **F-9** (VacuumWalks re-armed on a rewritten body).
- **THE GAP THIS BRIEF EXISTS TO CLOSE.** 1.1.0 changed the migration functions themselves, and **no
  function-level read of them exists**. `reports/vanillahunt/INVENTORY.tsv` rows:
  `Colonist.FindEmigrationDome` (**body AND signature** — new `force_leave` argument), `Colonist.TryToEmigrateToDome`,
  `Colonist.UpdateResidence`, `ChooseResidence`, `Residence.CanReserveResidence`,
  `Residence.CancelResidenceReservation`, `GatherFreeLivingSpaces`. **None appears in
  `reports/vanillahunt/SEAM_COVERAGE.tsv`** — the seam readers covered food/farms/resources, and the Colonist rows
  they read were the food ones. `Colonist.lua`, `Residence.lua` and `ShuttleHub.lua` got only a file-level
  changed-hunk skim (`reports/vanillahunt/agents/04-B_COLONY.md`), which that report says is **not** a coverage claim.
- **In-play evidence since 1.1.0 is almost nil.** The first `RunAll()` on 1.1.0 is still OWED (STATE), so every kit
  verdict in this cluster is a PREDICTION. `ShelterReflex`'s probe is `install` kind and SKIPs on retail
  (`00_TestCore.lua:77-80`). `VacuumWalks` and `ShelterReflex` are marked rewritten-but-never-run. The July PT
  passes (PT-12/13/19/34) are **1.0.7** and their colonies cannot be loaded (`EF-079`). The one real 1.1.0 in-play
  confirmation in this cluster is **C83** (tested-attended 2026-09-10).

## 2 · Scope fence

**IN.**
- The eight shipped modules: `Fix_ShuttleTransportCache` (F51), `Fix_VacuumWalks` (F52), `Fix_ArrivalDeaths`
  (F53 + C83 + F117), `Fix_ShuttleHubOffAvailable` (F54), `Fix_StaleReservations` (F58),
  `Fix_FreedHousingNotice` (F59), `Fix_DomeFreeSpaceMismatch` (F60), `Fix_ShelterReflex` (F73).
- The seven changed 1.1.0 functions in §1, read function-level against the archived 1.0.7 tree.
- The four declined entries in the same area — **F61** (the toggle is the designed quarantine), **F62** (services
  reach one passage hop), **F63** (universities invisible to emigration), **F79** (no trains for services) — and
  **F80** (a ticketed colonist not boarding for 17+ game hours; unexplained, vanilla).
- C40, C42, C45, C84 if and only if the read touches them; otherwise leave them.

**OUT.**
- ⛔ **Building or changing any fix.** A finding is FILED (entry + checklist), never built here. If the read says a
  module is now wrong or harmful, that is a finding and a checklist decision, not a patch — **except** a change the
  owner explicitly orders during the session, flagged in one line.
- The opt-in mod's modules (D03/D07/D12) — name them in the report as "in a separate optional mod", nothing more.
- FR-1/Linux (→ `perma/LINUX_DISPATCH.md`), the release lane, `items.lua`, `metadata.lua`, `RELEASE_OUTBOX.md`.
- Anything interesting found outside this list: **file it, do not chase it.**

## 3 · The work

**S1 — read what 1.1.0 changed (the gap).** For each of the seven functions: extract both bodies with
`tools/luafn.py` / `tools/treediff.py` (live 1.1.0 tree vs `C:\Dev\SMR-SrcArchive\1.0.7.396349\Src`) and read them.
Answer per function: what changed, does it change the defect one of our modules corrects, does it change the
*premise* of an entry, and does it create a new defect. **`FindEmigrationDome`'s new `force_leave` parameter is
the first thing to read** — a signature change at the centre of migration is the shape that produced F115 and F117.

**S2 — a verdict per module.** For each of the eight: **STILL NEEDED** · **REDUNDANT** (1.1.0 fixes it — then trace
the replacement body and name residuals, never a name proxy) · **HARMFUL** (like F-2 was) · **PARTIAL** (works for
some cases; say which are NOT covered). Cite `file:line` on **1.1.0.403908** for every claim. Run
`python tools/bodycheck.py --module <name>` and use `tools/deskbench.py` where a desk harness is cheap; a harness
without a leg that can fail is not evidence.

**S3 — reproduction recipes.** For every defect still live, write numbered in-game steps someone else can follow,
each with (a) a control that would fail if the defect were absent, and (b) what to look at. Mark each recipe
**CHEAP** (can ride the owner's owed v7 sitting, checklist 144 a) or **EXPENSIVE** (needs a provisioned colony).
⛔ Trace every recipe to the shipped body first and ask "what makes this vacuous?" — a recipe that cannot fail
banks a FALSE PASS. Where no recipe exists, say so plainly; "not reproducible at the desk" is a result.

**S4 — the declined four, and F80.** Decide what, if anything, is worth telling the developers about each: F61 is
their designed behaviour (say so, and that we withdrew it); F62/F63 are consistent carried-forward design with one
recorded internal inconsistency each (offer as observations, never as bugs); F79 is our own decision, not a defect;
**F80 is an unexplained vanilla defect and is probably the most valuable single thing we can hand them.**

**S5 — the deliverable: `docs/agent/reports/MIGRATION_DEV_REPORT.md`.** Written FOR a Paradox developer, in their
terms, not ours. One section per defect:
1. **Symptom** a player sees, in one sentence.
2. **Where**, `file:line` on 1.1.0.403908, with the mechanism in two or three sentences.
3. **Reproduce**, numbered steps, or an explicit "we have not reproduced this on 1.1.0".
4. **What our fix does**, one paragraph, and the module name.
5. **Confidence**, one of: `CONFIRMED IN PLAY` (name the date and who watched) · `DESK-CONTROLLED` (name the
   harness) · `SOURCE-READ ONLY` · `UNVERIFIED ON 1.1.0`.
6. **What we are unsure about** — the cases our fix does NOT cover. This section is required and may not be empty
   where §1 or S2 found a gap (F52's no-passage surface walk and F59's un-hooked reservation-cancel site are two
   we already know).
Open the report with a short honest preamble: how we find and check bugs, that the list's wording is
player-facing and deliberately broad, and that we will correct anything they disprove — as we did for F37.

**S6 — record and route.** Entry updates for anything the read changed (`row_status`, a dated 1.1.0 section;
⛔ never edit an entry's original 1.0.7 body). Then `python tools/doccheck.py --regen` (check
`git status docs/agent/bugs/` for a peer's files first) and `python tools/doccheck.py` GREEN. Add ONE checklist
item carrying the owner's decisions: which sections may be sent to the developers, whether any module needs a
build, and which recipes ride the owed sitting. **Claim your checklist number by message to the other sessions
before writing it** (150 is taken). Commit with `git commit -F <file> -- <explicit paths>`, then push.

## 4 · What may NOT be claimed

- **"Reproduced" requires a run.** A desk harness proves a branch, not that a colony reaches it — say
  "desk-controlled". A source read is "source-read only".
- **"Vanilla fixed it" requires the replacement body traced** and its residuals named. A missing name is not a
  deleted feature; grep where it went.
- **No in-play claim may rest on a 1.0.7 playtest.** Those colonies cannot be loaded on 1.1.0 (`EF-079`).
- **Kit verdicts are predictions** until the owed `RunAll()` runs; `install`-kind probes SKIP on retail entirely.
- **Never quote the public fix list as evidence** — it is player-facing wording, and its breadth is exactly what
  the developer questioned.
- Label every claim **SOURCE** (you read the line) or **INFERRED**. An unexplained log line is reported verbatim
  with its age, never discounted.

## 5 · Stop conditions — reporting beats pushing through

- A function's 1.1.0 rewrite is large enough that reading it properly exceeds the session → report what you read,
  name what you did not, and propose a chain (`reports/CHAIN_METHOD.md`).
- A module looks **harmful** on 1.1.0 → stop, write it up, and put it in front of the owner immediately. Do not
  fix it quietly. (F-2 is the precedent: our sweep was cancelling real expedition reservations.)
- The read contradicts a recorded entry → say so; entries are claims too. Do not "correct" an entry's 1.0.7
  citations to the live tree.
- You need the game launched → write the recipe for the owner's sitting instead.

## 6 · Read path (file granularity)

`docs/agent/STATE.md` · `docs/agent/FIX_POLICY.md` · `docs/agent/bugs/INDEX.md` (finds more) ·
entries `F51 F52 F53 F54 F58 F59 F60 F61 F62 F63 F73 F79 F80 F117 C83 C84` ·
`docs/agent/reports/PACK_1_1_0_REVERIFICATION.md` (rows K-2/K-5/K-6/K-13/K-21) ·
`docs/agent/reports/HOTFIX_2_AUDIT.md` (F-1/F-2/F-3/F-4/F-9) ·
`docs/agent/reports/vanillahunt/INVENTORY.tsv` + `SEAM_COVERAGE.tsv` + `agents/04-B_COLONY.md` ·
`docs/FIELD_REPORT_REPLIES.md` ("Reply to the developer") · `docs/agent/bugs/C88.md` (the same dev thread) ·
modules `Code/Fix_{ShuttleTransportCache,VacuumWalks,ArrivalDeaths,ShuttleHubOffAvailable,StaleReservations,FreedHousingNotice,DomeFreeSpaceMismatch,ShelterReflex}.lua` ·
game source `Lua/Units/Colonist.lua`, `Lua/Buildings/Residence.lua`, `Lua/Buildings/Dome.lua`,
`Lua/Buildings/ShuttleHub.lua`, `Lua/_GameUtils.lua`, `Lua/LRManager.lua`, `Lua/LRTransport.lua` ·
archive `C:\Dev\SMR-SrcArchive\1.0.7.396349\Src` (same files).

## 7 · The live todo list — required, and required to stay current

The owner reads it to decide when to step in. Build it before starting, **one item per commit-and-verify unit**
(each of the seven functions in S1 is its own item; each module verdict in S2 is its own item). Mark each complete
the moment it completes, keep exactly one in progress, and rewrite the list when reality diverges. Put the state in
the item text ("S2: 5/8 modules, ShuttleTransportCache STILL NEEDED").

## 8 · This brief deletes itself

One-off. When the report is delivered, the entries are updated and the checklist item is filed, `git rm` this file
in the same commit and remove its row from `prompts/README.md`. Git history keeps it.
