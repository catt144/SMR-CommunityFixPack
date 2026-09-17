# C95 + C102 build — habitat residents go on expeditions and come home; nobody is sent to a dead dome

One-off, authored 2026-09-17 at the owner's ask. Tool-neutral and model-neutral. `git rm` this file
**and its `prompts/README.md` row in the same commit** that lands the close-out. Records:
[C95](../bugs/C95.md) · [C102](../bugs/C102.md) ·
[exploration report](../reports/C95_RETURN_HOME_EXPLORATION.md).

Start with `git log --oneline -6`, `git pull`, `git status --short`. Authored against repo `006cc07`
and game 1.1.0.403908 build `6a91a190` (Steam build 24995074); find this file's own commit with
`git log -1 --format=%h -- docs/agent/prompts/C95_RETURN_HOME_BUILD.md` and re-derive only the §5
rows whose paths moved since.

⛔ **This is a BUILD brief.** The exploration is done, audited by a second vendor, and its design is
chosen. Do not re-run it. What is decided is in §1; where you have licence is in §2.

## 0 · How to work this

Open a live progress list before touching anything: one item per commit-and-verify unit, exactly one
in progress, rewritten when reality changes. Minimum shape: orient and staleness · return-home
module · C102 safe fallback · the draft's new rule and the v11 module's fate · desk suites · live
legs · entries, report, outbox and checklist close-out. The owner reads that list to decide when to
step in.

## 1 · Decided — settled input, not work items

1. ⚖️ **Habitat residents go back into the expedition draft and come home to their own habitat.**
   Owner, 2026-09-16: *"allow habitat residents to be in the pool but remember their home and return
   to it. That would be the right way to fix this."* The v11 exclusion was the workaround.
2. ⚖️ **When the home cannot be used, the returnee goes to the nearest SAFE dome.** Owner,
   2026-09-17: *"Then it should be nearest safe dome. But with our fix extended so that they don't
   pick an unpowered dome with no life support."* That is C102's repair, and it is built in this job.
   No waiting aboard, no refused departure, no shelter rule.
3. **The seam is the prototype's** (`tools/arming/payloads/97_C95Home.lua.txt`, report §"Prototype
   and measured result"): hand the shipped `Colonist:GetExpeditionReturnDome` a private copy of the
   reachable list that also holds this colonist's own held habitat, so the home is chosen **before**
   the receiver reserves a fallback bed; and run housing before the job picker when a colonist
   rejoins a reserved habitat. Both receivers call that one selector (`RocketBase.lua:1974`,
   `CargoTransporterNew.lua:1084`), so one wrapper covers legacy and 1.1.0 rockets. No body is copied.
4. **No new persistent state, no threads, no stored callbacks** (`FIX_POLICY.md` §3, §3a layer 3).
   The prototype meets this; the shipped module must too.

## 2 · Defaults — depart with a reason, and list every departure in the report

- **The draft's new rule.** DEFAULT: a habitat resident is draftable **only when their home is
  returnable from this rocket** by the same test the return selector uses; otherwise they stay out
  of the automatic draft, as v11 has it. Why: the return repair admits a home only on foot or over a
  verified train route, so a resident of a far habitat with neither would be drafted and lose their
  home again. That is the original report's colony shape, and v11 protects it today. ⚠️ One bounded
  check rides on it: does an expedition rocket unload where it loaded? If it can land elsewhere the
  draft-time test is weaker than it looks; say so. This default also leaves an all-habitat colony
  whose habitats are unreturnable unable to crew, which is ck200's open question. ⛔ Do not settle
  that one; report what your rule does to that colony.
- **Shuttles.** `NaturalHabitatBase` inherits `ShuttleLanding`, and the exploration left shuttle
  routes out. A bounded look: can the return dispatch book one? If yes and it is cheap, admit it and
  the unreturnable class shrinks. If not, say why in three lines and move on.
- **Where C102's repair lives.** Extending `Fix_ArrivalDeaths` or a new module is your call. The two
  inherited constraints are not: the destination must be corrected before the fallback reservation
  at `CargoTransporterNew.lua:1091-1093` (and the legacy twin), and the return dispatch bypasses
  `Colonist:Idle`, where the arrival repair lives. Reuse `is_welcoming_arrival_dome`'s definition of
  safe; do not write a second one.
- **No welcoming dome anywhere.** DEFAULT: preserve vanilla's assignment, as C83 does, log it once,
  and list it as unruled. ⛔ Do not invent a rule for it.
- **The rejoin hook's width.** It also fires for an ordinary migrant rejoining a reserved habitat
  with no residence. The audit accepted that as the habitat's own job rule applied consistently;
  narrow it if you find a cost.
- **The v11 module.** Reshape `Fix_HabitatExpeditionDraft.lua` into the conditional rule or replace
  it; never leave a commit where residents are draftable and the return repair is not registered.
  ⭐ The module as shipped in v11 is already archived at the owner's ask, byte-for-byte:
  `docs/archive/code/Fix_HabitatExpeditionDraft.v11-4ec3e32.lua.txt`, sha256 `064a5cb6…2c613d`
  (`sha256sum` it against `git show 4ec3e32:Code/Fix_HabitatExpeditionDraft.lua`). Cite that path in
  the new module's header and in C95; the archive is append-only, so never edit the copy.
- Module names, ids, file split, log wording, desk-suite layout.

House requirements that are not negotiable, stated once: `SMRFixPack.Register` / `Require`
preflight that does not fail the module when one receiver is absent, the §2b pinned-defect manifest
for every body you depend on, a veto id per module, idempotent apply, `items.lua` and
`metadata.lua`'s code list updated together (doccheck MODULE SETS).

## 3 · Evidence you owe

**Desk.** Extend `tools/desk_c95_return_home.py` (30 demands today) to the shipped module, and keep
`tools/desk_c95_habitat_draft.py` honest for whatever the draft rule becomes. ⭐ A fix invalidates
its own tests: base every harm leg on the pre-fix body and run both suites whole. Add: the
conditional draft on returnable and unreturnable homes · C102 with a dead `safety_dome` and a live
alternative, with no alternative, and for an ordinary dome returnee · selector delegation for every
non-habitat colonist · exact behaviour with one receiver absent.

**Live, unattended.** The arming legs `tools/arming/legs/c95-explore*.json` and the driver are
reusable; copy saves, never write the owner's folder
(`C:\Users\stkot\Saved Games\Surviving Mars Relaunched\76561198020568696`) except files you made,
and run `tasklist /FI "IMAGENAME eq Mars.exe"` before every launch. Before any live leg run the
probe sweep in `docs/agent/WORKFLOW.md` "Probe hygiene" and put its evidence in the progress list.

- the nearby-full A/B again, on the **registered module**, not the payload;
- a drafted run: the real gather picks a habitat resident, they fly or are unloaded, they come home;
- C102: the nearest dome to the pad switched off, a live dome further away, one returnee whose home
  is unusable. Switching a dome off **is** the mechanism's condition and is the only permitted setup
  mutation; name it in the result;
- save mid-return and reload; then a cold restart on that save with the pack disabled. Report what
  the colonist does in each. These are release gates the exploration left unrun.

⛔ No forced housing, mass reassignment or teleported subjects in any leg that reads the mechanism
(`EF-104` records one such fixture that lied). State each fixture's layout: habitat-to-pad distance,
whether it was full, what domes stood in walking range.

**The rail leg needs a fixture that does not exist.** Fixture `lD1jaGcMJOxaiFcU` has no station
route from its pad to its habitat. Do not fake it at the desk and do not build a railway by script.
Hand it to the owner as a sitting (next paragraph) and say it is provisioning, not a warm-up.

**The owner's sitting.** Rewrite ck200 into a Run item with the shortest sitting that closes what
you could not: an ordinary crewed expedition sent through the UI from a colony with a habitat, the
rail return if they have or can provision one, and the dead-dome leg. Copy-paste console lines only,
one line each, no `--` comments, a first-screen witness per leg. `tested-attended` is the owner's
word; nothing you ran earns it, and v11's attended verdict does not transfer to new code.

## 4 · Close-out

- Entries through the `smr-bug-library` skill: C95 and C102 carry what was built, what was run and
  what was not. Status words describe what was **tested**; do not promote on opinion.
- A build report beside the exploration report: design as shipped, **DEPARTURES** from this brief
  with reasons, **SUGGESTIONS**, the no-yield re-check for every wrapped call, and what you did not
  open.
- `docs/agent/prompts/perma/RELEASE_OUTBOX.md`: append the Pending entry. C95's public row changes
  from a marked judgment call to a repair, and C102 is a new row; write both in the public voice
  (plain for players, precise for the devs). ⛔ No upload, no version edit: the release prompt owns
  those.
- `python tools/doccheck.py` GREEN; commit with a pathspec; push.

**What may not be claimed.** "Comes home" without a physical return observed is "desk-passes". A leg
run through direct `LoadPassengers` / `UnloadPassengers` is a receiver test, not a mission. A
MarsDebug pass is not retail evidence (`EF-044`). Probe tallies carry their build and name their
SKIPs.

## 5 · Derived facts and falsifiers

All on 1.1.0.403908, Steam build 24995074. An empty
`git diff --stat 006cc07..HEAD -- Code/ tools/ docs/agent/bugs/C95.md docs/agent/bugs/C102.md docs/agent/facts/`
means none of these needs re-reading.

| fact | how measured | falsifier |
|---|---|---|
| A full habitat is dropped from the return list before distance is tested: the list is built with an argument-less `CanVisit()` and the habitat's own body needs the colonist to admit a held resident | SOURCE `_GameUtils.lua:399`, `MicroGHabitat.lua:58-72`; MEASURED control log `c95_home_…00.07.16…log:270` (`original_list_contains_home=false`, `walk=true`) | the call at `:399` passes a colonist |
| Reserving a fallback bed clears `expedition_residence`, so a wrapper on the return command is too late | SOURCE `Residence.lua:290-307`, `:385-399` | `CancelResidenceReservation` no longer writes that field |
| Returnees get `arriving` set and may be dispatched by train without entering the walking body | SOURCE `ColonistTransport.lua:204-207`, `:381-502` | no `ReturnFromExpedition_TransportDestination` member |
| One selector serves both receivers | `grep -rn "GetExpeditionReturnDome(" <SRC>/Lua` hits the definition and two calls | a third caller |
| The prototype brought resident 2000002122 home to habitat 2692; the same save without it sent them to dome 1076 and a `MetalsExtractor` job | archived logs `c95_home_…00.05.53…` `:281` and `…00.07.16…` `:277`, audited `8d9c4d4` | re-grep `C95HOME` in both |
| `SetDome` runs `UpdateWorkplace` before `UpdateResidence`; `SetResidence` calls neither, so the rejoin hook cannot recurse | SOURCE `Colonist:SetDome`, `Colonist:SetResidence` | a call to either inside `SetResidence` |
| `safety_dome` is picked by distance with no welcoming test and seeds `ChooseDome` | SOURCE `_GameUtils.lua:398-412`, `:486-501` | `is_welcoming_community` applied to `safety_dome` |
| The arrival repair is keyed on `self.arriving` inside a `Colonist:Idle` pre-wrapper | `Code/Fix_ArrivalDeaths.lua:381-383` | the gate moves |

Read path, by file: the two entries and the report above, `docs/agent/FIX_POLICY.md` (§1, §2, §2b,
§3, §3a), facts `EF-103`, `EF-104`, `EF-107`, and `Code/Fix_HabitatExpeditionDraft.lua`,
`Fix_ArrivalDeaths.lua`, `Fix_StaleReservations.lua`, `Fix_FreedHousingNotice.lua`,
`Fix_VacuumWalks.lua`. `docs/agent/bugs/INDEX.md` and `docs/agent/facts/INDEX.md` are the grep route
to anything else. Reach: every platform, ordinary play; the reporter is a retail player.

## 6 · Stop and report instead of pushing on when

- a wrapped call can yield, or the design cannot stay inside `FIX_POLICY.md` §3a. Show it; that is
  an answer, and a full-body replacement is the owner's call to make, not yours;
- the build needs a rule about what the game meant that §1 does not give (the no-dome case, ck200);
- a live leg needs the owner's hands, their save folder written, or their running game touched.
