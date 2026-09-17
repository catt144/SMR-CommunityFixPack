# C95 exploration — let habitat residents go on expeditions and come home

One-off, authored 2026-09-16 at the owner's ask. Tool-neutral and model-neutral (Claude or Codex).
`git rm` this file and its prompt-map row in the commit that lands the report.

Start with `git log --oneline -6`, `git pull` and `git status --short`. Authored at `7dc8a22`;
`git diff --stat 7dc8a22..HEAD -- Code/ docs/agent/bugs/C95.md docs/agent/bugs/C102.md
docs/agent/facts/` empty means nothing in §3 needs re-reading.

## 0 · The decision, and what you are for

**The owner has reopened C95's repair shape.** Their words, 2026-09-16:

> *"I want to know if we can allow habitat residents to be in the pool but remember their home and
> return to it. That would be the right way to fix this, even if it means a full lua rewrite, which
> we try not to do."*

C95's entry says the return-path repair was declined and must not be re-litigated. That ruling was
the owner's and so is this one; the entry's "⛔ do not re-litigate" does not bind this job.

What shipped in v11 keeps habitat residents out of the automatic expedition draft. It works, and it
has a hole the reporter walked into the same night: **their whole colony lives in habitats**, so
once the fix runs for them no expedition can ever crew (C95, "REPORTER FOLLOW-UP"; checklist ck200).
Excluding people was always the workaround. The right repair is the one the game half-built itself:
it saves the home, reserves the bed, and then throws the reservation away on return.

**End state: one report that tells the owner whether that repair can be built, the best shape you
found for it, what it costs, and a prototype that shows it bringing a habitat resident home.**
`docs/agent/reports/C95_RETURN_HOME_EXPLORATION.md`.

## 1 · Your licence

This is exploration. Be inventive.

- ⭐ **Read anything.** The live source tree (`SRC` in `tools/luafn.py`), the archived 1.0.7 tree,
  the packs, the TestKit, every log and the archive. `docs/agent/bugs/INDEX.md` and
  `docs/agent/facts/INDEX.md` are the lookup route for records this brief does not name; grep them,
  do not read them whole.
- ⭐ **Any technique is on the table**, a full-body replacement included. `FIX_POLICY.md` §1 ranks
  techniques by invasiveness; rank your candidates against it and say what each one buys, but do not
  let the ranking stop you finding the design that actually works. The owner asked for the right
  fix first and the cheap fix second.
- ⭐ **Everything in §3 is a claim.** It was read and measured tonight by one session under time
  pressure. Overturn what is wrong; "the brief was wrong about X" is a good result.
- ⭐ **You may launch the game.** Run `tasklist /FI "IMAGENAME eq Mars.exe"` first and never start or
  kill a game while the owner's is running. Work on **copies** of saves; the owner's folder
  (`C:\Users\stkot\Saved Games\Surviving Mars Relaunched\76561198020568696`) is read-only to you
  except for files you created. Fixture `lD1jaGcMJOxaiFcU` has a Naturalist Habitat with 5 residents
  and a rocket on the pad (C95, "Historical failed sitting"). If you cannot drive the game far
  enough unattended, say exactly where you stopped and hand the owner the shortest sitting that
  finishes it; do not fake the leg at the desk.
- ⭐ **Widen the question if the code says to.** C102 (returnees marched to a switched-off dome) is
  the same function two lines further down. If one design closes both, that is worth more than two
  repairs; if it does not, say why.

Fixed, because they are house process and not limits on thinking:

- ⛔ **Nothing ships from this job.** No file in `Code/`, no edit to `items.lua` or `metadata.lua`.
  doccheck's MODULE SETS gate reds an unlisted file in `Code/`, so the prototype lives elsewhere:
  the desk harness (`tools/deskbench.py`, shape in `tools/desk_c95_habitat_draft.py`) or the local
  TestKit tree for live runs. The v11 module stays as it is until the owner rules on your report.
- ⛔ **`tested-attended` is the owner's word.** A live run you drove is `tested-unattended` at most.
- ⛔ **Shared tree.** Check `git log` / `git status` before every write; Codex peers are invisible to
  `ListAgents`; commit with a pathspec.

Keep a **live todo list** for the whole job, one item per commit-and-verify unit, exactly one in
progress, rewritten when reality changes. The owner reads it to decide when to step in.

## 2 · What the design has to answer

Leads, not a checklist. Drop any that the code makes moot and add your own.

1. **Where exactly is the home lost, and what is the smallest place to stop losing it?** The bed is
   already reserved when they leave. Is the repair in who gets chosen as the destination, in how the
   colonist travels there, or in what `ReturnFromExpedition` cancels?
2. **How do they physically get home?** A habitat is reachable on foot only, as far as the return
   path knows. The owner watched a displaced resident ride the rail back unaided, so ordinary
   migration can route there. A design that names the right destination and then walks a colonist
   across 2 km of vacuum is F52 and F53 over again; read `Fix_VacuumWalks.lua` and
   `Fix_ArrivalDeaths.lua` before you route anybody anywhere.
3. **The window between landing and home.** EF-107: a displaced resident can be hired inside a dome,
   and a colonist's own workplace then pulls them back to that dome for good. Whatever you build has
   to survive the hours a returnee spends in transit.
4. **What happens to the v11 exclusion?** Retired, kept as a fallback, or inverted (draft residents
   only when nobody else can go)? The all-habitat colony is the test of any answer.
5. **Everyone the return path touches who is not a habitat resident.** The design must leave a dome
   resident's return exactly as it is unless you can show it improves it.
6. **Saves.** A crew already away when the fix lands; a save made mid-return; the pack removed with
   returnees in flight. `FIX_POLICY.md` §3 and §3a are the bar.
7. **Both receivers.** `CargoTransporterNew:UnloadPassengers` is what 1.1.0 plays;
   `RocketBase:Disembark` is the legacy twin. C95's first build targeted the wrong one and was inert.
   Name the concrete class of the object your repair acts on in a live save.
8. **Cost.** If the honest answer is a full-body replacement, say which bodies, how many lines, what
   a game patch to them would do to us, and whether `bodycheck` can watch them.

## 3 · What is already known — verify what you lean on

All on game 1.1.0.403908 (build `6a91a190`), repo `7dc8a22`. Each line: the claim, how it was
reached, one way to falsify it.

| claim | how | falsifier |
|---|---|---|
| The home is saved and the bed reserved on boarding; the reservation is cancelled on return when the chosen dome is not the reserved one | SOURCE, C95 "The game ALREADY holds their bed" | `grep -n "expedition_residence" <SRC>/Lua/Units/Colonist.lua` shows no save at `EnterTransporter` or no cancel in `ReturnFromExpedition` |
| A standalone habitat enters the return path's `domes` list by walking distance only; the train sweep harvests `labels.Dome` and a habitat is a `Community`, not a `Dome` | SOURCE, EF-103, C95 "AMENDED 2026-09-15" | the station sweep in `GetDomesReachableByColonists` (`_GameUtils.lua:390`) iterates `labels.Community` |
| `safety_dome` is chosen by distance with no welcoming test, and `ChooseDome` seeds its answer with it | SOURCE, C102 | `_GameUtils.lua:398-412` applies `is_welcoming_community` to `safety_dome` |
| Our dead-dome repair covers new arrivals only | MEASURED, `grep -n "ReturnFromExpedition\|UnloadPassengers" Code/Fix_ArrivalDeaths.lua` hits one comment line | a second hit that is code |
| All four expedition launches set the Expedition type before `CmdLoad`, and the player cannot hand-pick an expedition crew | SOURCE, C95 "REPORTER FOLLOW-UP" | a `ChangeRocketType(g_RocketTypes.Expedition)` in `Data/FlightPolicyDef.lua` that follows its `SetCommand("CmdLoad"` |
| The picker refuses dome jobs only while `residence` is a habitat; the emigration scorer never consults that rule | SOURCE + MEASURED, EF-107 | `Workforce:HasFreeWorkplacesAroundForSpecialist` calls `IsSuitableWorkplace` |
| A short crew is an indefinite wait, and the short-crew branch evaluates `#nil` with unknown result | SOURCE, EF-104 | the branch at `CargoTransporterNew.lua:168` guards the nil |
| F58 protects an away colonist's `expedition_residence` reservation from its staleness sweep | SOURCE, header of `Code/Fix_StaleReservations.lua` | the header no longer cites `Colonist.lua:5027-5031` |

Read path, by file: `docs/agent/bugs/C95.md` (sections "REPORTER FOLLOW-UP", "The game ALREADY
holds their bed", "The mechanism", "AMENDED"), `docs/agent/bugs/C102.md`, `docs/agent/bugs/C100.md`
("MEASURED 2026-09-16" only), facts `EF-103`, `EF-104`, `EF-107`, `docs/agent/FIX_POLICY.md`,
`docs/agent/reports/C95_HABITAT_DRAFT_BUILD.md`, and `Code/Fix_HabitatExpeditionDraft.lua`,
`Fix_ArrivalDeaths.lua`, `Fix_StaleReservations.lua`, `Fix_FreedHousingNotice.lua`,
`Fix_VacuumWalks.lua`. `python tools/doccheck.py --emit-fingerprint` says whether those facts still
describe the installed game.

## 4 · The report

Lead with the answer: **buildable or not, and the shape you would build.** Then:

- the candidate designs you considered, each with what it fixes, what it breaks, its technique
  layer, its save footprint, and why you ranked it where you did;
- the prototype: where it lives, what it was run against, and the raw lines that show a habitat
  resident leaving on an expedition and ending up back in their own habitat, or the exact point
  where that failed;
- the all-habitat colony, the far habitat and the habitat beside a dome, each stated separately;
  say which you ran and which you reasoned;
- whether C102 falls out of the same design;
- **DEPARTURES** from this brief with reasons, and **SUGGESTIONS** the owner did not ask for;
- what you did not open.

**What may not be claimed.** "Works" without a live return observed is "desk-passes". A forced
fixture (mass reassignment, teleported colonists, cheated housing) that intersects the mechanism
invalidates the reading; EF-104 records one that did. Probe tallies carry their build; never use a
MarsDebug pass as retail evidence (`EF-044`). Before any live leg, run the probe sweep in
`docs/agent/WORKFLOW.md` "Probe hygiene" and put its evidence in the todo list.

Route the owner's decision to `docs/PLAYTEST_CHECKLIST.md` by rewriting ck200 around your finding,
not by adding a second item. Anything you find outside this scope goes to its own entry through the
`smr-bug-library` skill; finding it does not authorise fixing it.

## 5 · Stop and report instead of pushing on when

- the design needs a rule about what the game *meant* that the owner has not given;
- a live leg needs the owner's hands, their save folder written, or their running game touched;
- the only working shape cannot meet `FIX_POLICY.md` §3a. Say so and show it; that is an answer.
