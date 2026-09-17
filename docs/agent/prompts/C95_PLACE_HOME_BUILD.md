# C95 rebuild: expedition crews go back the way they were taken

One-off, authored 2026-09-17 at the owner's ruling. Tool-neutral and model-neutral. `git rm` this
file **and its `prompts/README.md` row in the same commit** that lands the close-out.

Start with `git log --oneline -6`, `git pull` and `git status --short`. Authored against `a5f24bc`
plus this file's own commit (`git log -1 --format=%h -- docs/agent/prompts/C95_PLACE_HOME_BUILD.md`),
on game 1.1.0.403908, build `6a91a190`, Steam 24995074.

Records: [C95](../bugs/C95.md), [C102](../bugs/C102.md), and the build this replaces:
[C95_RETURN_HOME_BUILD.md](../reports/C95_RETURN_HOME_BUILD.md).

Open a live progress list before touching anything: one item per commit-and-verify unit, exactly one
in progress, rewritten when reality changes. Minimum shape: orient and staleness · placement in the
return module · draft route gate retired · desk suites · probe sweep · live legs · ck200 rewrite ·
entries, report and outbox. The owner reads that list to decide when to step in.

## The decision

⚖️ **Owner, 2026-09-17:** *"Lets do it, thats the more elegent solution anyway, honest the solution
the devs should have built imo, its like they built only half of a new system."*

The expedition draft takes a colonist from anywhere: `EnterTransporter` attaches them to the rocket
where they stand, with no route (`Colonist.lua:5025-5044`, `Unit.lua:1292-1306`). The return makes
them walk (`CargoTransporterNew.lua:1080-1094`, `Colonist.lua:5102-5122`), so a home outside walking
range is never offered. The current build handles that asymmetry by refusing to draft such
residents. In the reporter's own save that refusal left an expedition at 0/6 with no explanation
(evidence below).

**End state:** a habitat resident is draftable exactly as vanilla drafts anyone. On return, a
returnee whose held habitat is usable but out of reach is placed into that habitat, as directly as
they were taken. When the home is not usable, C102's nearest safe dome applies unchanged. The
route gate in the draft is gone.

⚖️ **The owner's one condition, verbatim:** *"The only think I would want to be sure of is it
wouldn't some how interfere with truely new colonists from earth getting randomly teleported
somewhere."* This is **fixed**: placement applies only to a unit whose `expedition_residence` is a
`MicroGHabitatBase`. That field is written in one place, at expedition boarding from the colonist's
existing residence (`Colonist.lua:5027-5031`). Earth arrivals come from `GenerateArrivals` and the
`Arrive` path, not the returnee loop. Prove non-interference at the desk and live, not by argument.

This makes ck200's policy (a) moot ("no returnable home means no automatic crew"). Policy (b), no
safe dome anywhere, stays unruled; do not invent a rule for it.

## Your judgement

Depart from any of these with a reason; list every departure in the report.

- **When to place instead of walk.** DEFAULT: keep the proven walk when the home is in walking range,
  and place only when it is not. If placing always is simpler and no worse, say so and choose.
- **Train.** C95 records that the train sweep never contributes a habitat (`_GameUtils.lua:450-478`,
  C95 "AMENDED 2026-09-15"), yet the current `can_return_home` admits `GetTransportRoute`. Decide
  whether rail stays a route or placement makes it redundant.
- **How to place.** The game's own precedent is `dome:RandPlaceColonist` after repeated failed
  entries (`ColonistTransport.lua:519-526`). The seam, ordering, and whether the colonist first
  disembarks at the rocket are yours. The selector still has to keep the home before the fallback
  reservation clears `expedition_residence` (`Residence.lua:290-307`, `:385-399`).
- **Other maps.** Boarding crosses maps (`TransferToMap`, `Unit.lua:1296-1298`); the current predicate
  requires `IsSameMap`. The reporter's map has an underground layer. Admit a cross-map home if the
  engine supports it cleanly, otherwise report why not.
- **Covert ops** also adds units to `transported_passengers` (`CovertOps.lua:184`). Establish whether
  they can carry a habitat `expedition_residence`, and scope accordingly.
- **The draft module.** Retire the route gate. Keep the automatic exclusion when the return module is
  inactive, as today, unless you find a reason not to. Never leave a commit where residents are
  draftable and the return repair is unregistered.
- **The placement's admission test.** The home must be valid, working, accepting and alive, and must
  still take this colonist. A player filter that now forbids them is a real case: in the reporter's
  save every habitat forbids everyone but geologists. Say what happens.

## Evidence you owe

**Desk.** Extend `tools/desk_c95_return_home.py` and `tools/desk_c95_habitat_draft.py`. A fix
invalidates its own tests: base harm legs on the pre-fix body and run both suites whole. Required
legs: an out-of-reach home placed; an in-range home still walked (or your departure); an unusable
home falling to C102; a unit with no habitat `expedition_residence`, including a fresh arrival,
untouched; the draft taking a resident whose home has no route.

**Live, unattended.** Run the probe sweep in `docs/agent/WORKFLOW.md` "Probe hygiene" first and put
its evidence in the progress list. Copy saves; never write the owner's save folder except files you
made, and never touch a running game. Required: a drafted far-habitat resident placed home; an
in-range resident home as before; a passenger rocket from Earth landing in the same run, with its
arrivals on the vanilla/C83 path; save mid-return and reload.

**Fixture.** The reporter's colony is the case: `saves/game/BUG.savegame.sav` (Brazil, sol 43,
BlankBig_02, four Naturalist Habitats, three unpowered domes). Copy it. As shipped, its habitat
filters forbid every specialization but geologists and its expeditions need botanists, officers or
medics. To crew it, the owner stripped the filters and imported six botanists. Both mutations change
who may live where, which your admission test reads, so name them in any result that uses them.

**Owner sitting.** Rewrite ck200 into the shortest sitting that closes what you could not: an
ordinary UI expedition on a copy of the reporter's save, crewed from a far habitat, witnessed home;
and a pack-disabled cold restart mid-return. One paste-safe console line per read, no `--` comments,
a first-screen witness per leg. Carry ck200's rail and C102 gates forward unchanged; they remain the
owner's to waive.

**What may not be claimed.** "Comes home" without a physical return observed is "desk-passes". A leg
driven through direct `LoadPassengers` / `UnloadPassengers` is a receiver test, not a mission.
`tested-attended` is the owner's word.

## Close-out

C95 and C102 through the `smr-bug-library` skill. A build report beside the one this replaces, with
DEPARTURES, SUGGESTIONS, the no-yield re-check for each wrapped call, and what you did not open.
Rewrite the Pending entry in `docs/agent/prompts/perma/RELEASE_OUTBOX.md`: its C95 row still says
automatic crews need a walking or train route home. No upload and no version edit. doccheck GREEN;
commit with a pathspec; push.

## Derived facts and falsifiers

Empty `git diff --stat a5f24bc..HEAD -- Code/ tools/desk_c95_* docs/agent/bugs/C95.md docs/agent/bugs/C102.md`
means none needs re-reading. Source paths are under `<game>\ModTools\Src\Lua`.

| fact | how measured | falsifier |
|---|---|---|
| Boarding attaches without travel | SOURCE `Unit.lua:1292-1306` | a route or walk inside `Unit:EnterTransporter` |
| `expedition_residence` is set only at expedition boarding | `grep -rn "\.expedition_residence\s*=" --include=*.lua . \| grep -v "= false"` over all of `Src` (DLC included) gives only `Colonist.lua:5030` | a second hit |
| The draft is all-or-nothing | SOURCE `CargoTransporterNew.lua:278-285` | a partial list returned below `amount` |
| The route gate held back a far-habitat botanist and the expedition read 0/6 | LIVE 2026-09-17, `docs/archive/logs/c95_sitting_20260917_Mars.exe-20260917-09.39.38-6a91a190.log:766-771` (`2000002934 … home_ok false walk false`); five others `true` | re-grep `C95 DRAFT` in that log |
| The reporter's habitats forbid all but geologists | same log `:587-597` (`C83 FILTER`) | re-grep `C83 FILTER` |
| One selector serves both receivers | `grep -rn "GetExpeditionReturnDome(" Lua` finds the definition plus `RocketBase.lua:1974`, `CargoTransporterNew.lua:1084` | a third caller |

The archived log was normalized CRLF to LF; raw sha256 `1c5a6be8…193357`, stored `d9593658…aac5d34`.

Read by file: this brief, C95 and C102 (their "Current build" sections first), the report above,
`docs/agent/FIX_POLICY.md`, `Code/Fix_HabitatExpeditionReturn.lua`,
`Code/Fix_HabitatExpeditionDraft.lua`, `Code/Fix_ArrivalDeaths.lua`. Grep
`docs/agent/bugs/INDEX.md` and `docs/agent/facts/INDEX.md` for anything else. Reach: every platform,
ordinary play; the reporter is a retail player.

**Out of scope, route and do not fix:** C83's arrival fallback also sends colonists to habitats that
refuse them (seen in this sitting; its own record), and any other defect you meet.

## Stop and report when

- the placement needs a copied body, a yielding wrapped call, or persisted state;
- the owner's non-interference condition cannot be proven at the desk or live;
- a leg needs the owner's hands, their save folder written, or their running game touched.
