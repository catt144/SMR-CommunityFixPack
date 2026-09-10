# DLC DEEP CHECK — new bugs in *Feeding the Future* and the sponsor pack

Paste into a fresh Claude Code session. Written **2026-09-08**, to fire **after
the current fix pack is patched, pushed and stable** (owner instruction).
**Start with `git log --oneline -15` + `git pull`.** Read `docs/agent/STATE.md`
(mandatory), `docs/agent/FIX_POLICY.md`, `docs/agent/reports/CHAIN_METHOD.md`,
and **`prompts/vanillahunt/README.md` §7 + link 03's "For dlccheck" section of
`reports/vanillahunt/TRIAGE.md`** — the two efforts overlap by design. *(The
brief `VANILLA_DIFF_HUNT.md` was consumed into that chain on 2026-09-10; its
§2 taxonomy, §4 finding contract and §7 subagent rules now live in that README
as §2, §3 and §4. ⛔ Fire this brief only after that chain's 99 has run — its
owner report carries your kickoff line and the base-game seam result you
inherit rather than redo.)*

> 🎯 **YOUR JOB IS TO AUTHOR A CHAIN, NOT TO RUN THE CHECK.** Handoff brief in
> the shape of `HOTFIX_2_HANDOFF.md`. Decompose into `prompts/dlccheck/` with a
> terminal audit. ⛔ 17k lines of new content will not fit one context.

> ⚖️ **THE THESIS, in the owner's words:** *"when they add a core new feature
> they are always lax on QC … the bug check QC rep is horrendous on DLC."*
> ⇒ Assume the new content is **under-tested**, and assume nobody checked what
> it does to the game a player already had.

## 0 · What is on disk RIGHT NOW — no preconditions, this is all readable today

⭐ **There are TWO DLCs, not one.** Both are installed (`appmanifest_3215050.acf`
lists `dlcappid` **3889420** and **3889430**), both ship as `.fpk` in
`…\Project Spark\DLC\`, and — ⭐ **crucially — both have their Lua and presets
extracted into the ModTools tree**, so this is a source effort, not a
reverse-engineering one.

| tree | what it is | size |
|---|---|---|
| `ModTools\Src\DLC\norman\` | ***Feeding the Future*** — the food DLC | **138** `.lua`, **15,794** lines |
| `ModTools\Src\DLC\thomas\` | a **sponsor / faction pack** — `AssemblyOfPlanets` sponsor, `LawOffice`, colony colour schemes, mission logos, `SponsorGoals`, `DumbAIDef` | **13** `.lua`, **1,273** lines |

`norman/Code`: `FoodUtils`, `Replicator`, `FungalFarm`, `Bakery`,
`AutomatedFarm`, `FarmInsect`, `PanoramicRestaurant`, `FarmSmall`, `Hints`,
`Resources`, plus `AmbientLife/`, `BuildingTemplate/`, `XDef/`.
`norman/Presets`: `CropPreset`, `Meal`, `Animal`, `Resource`, `LawDef`,
`PolicyDef`, `Achievement`, `Tech`, `Cargo`, `EncyclopediaArticle`,
`OnScreenHint`, `PopupNotifications`, `Event/`, `FXPreset/`, `AmbientLife/`.

⚠️ **`thomas` is small enough to sweep cheaply and completely.** Do not let it
fall off the end behind the big one — a 1,273-line pack read in full is a
guaranteed-complete result, which `norman` will never be.

## 1 · ⭐ THE STRUCTURAL FINDING THAT SHOULD SHAPE THE WHOLE CHAIN

**The DLC's own Lua is almost entirely ADDITIVE.** Its functions are new classes
— `AutomatedFarmBase`, `BakeryBase`, `FarmInsectBase`, `FungalFarmBase`,
`PanoramicRestaurant`, `Replicator` — and there are only **four** `OnMsg` hooks
in the whole of `norman/Code`. ⛔ **It does not broadly override base-game
functions.**

⇒ **So the old × new breakage the owner predicts is NOT mostly inside the DLC
folder.** It is in three other places, and the chain should be built around
them rather than around a file-by-file read of `norman/`:

1. ⭐ **Base-game changes made TO ACCOMMODATE the DLC — which ship to EVERYONE,
   DLC or not.** These land in the 1.1.x vanilla diff, so they are shared
   territory with the `vanillahunt` chain, whose link 04 reads exactly this set
   and writes `TRIAGE.md` → "For dlccheck". **Inherit it; do not duplicate.**
2. ⭐ **The non-owner path.** Base Lua **references DLC content in 12 files** —
   including `Building.lua`, `ConstructionSite.lua`, `FoodServiceBuilding.lua`,
   `Resources.lua`, `UpgradeUnlocks.lua` — while `IsDlcAvailable("norman")`
   appears **3 times** in the entire base tree and `("thomas")` **once**.
   ⚠️ **That gap is a hypothesis, not a finding.** Several of those references
   are to things that also exist in the BASE game (there is a base
   `Lua/Buildings/FungalFarm.lua` *and* a DLC `FungalFarmBase`), so **a name
   match is not a DLC dependency.** ⛔ Enumerate which references genuinely
   require DLC content and which do not — this is exactly the
   absence/presence discipline in `prompts/vanillahunt/README.md` §2, and getting it wrong
   in either direction is easy.
3. ⭐ **Presets and data, which is where DLC QC is worst and where our
   instruments are weakest.** `CropPreset`, `Meal`, `Resource`, `LawDef`,
   `PolicyDef`, `Tech`, `Cargo` all mutate **shared registries** the base game
   iterates. `sigcheck`/`bodycheck` see none of it. `EF-078` is the precedent:
   the source-read predicted 6 self-disabled modules, the game measured 13, and
   the miss was *"preset/DATA checks invisible to any symbol sweep"*.

## 2 · The seams to work, in priority order

The DLC adds a food economy on top of a game that already had food. Every place
the new economy touches an existing system is a seam:

- ⭐ **new-game start under Linux/Proton (added 2026-09-10, owner).** Players
  report every new game crashing since the update, in a thread titled with the
  DLC's name (`prompts/vanillahunt/README.md` §2b, FR-1). Read that chain's
  **FR-1** and **FR-1(b)** results in `reports/vanillahunt/TRIAGE.md` before
  starting: the DLC code that runs at new game (map setup, starting resources,
  `thomas`'s sponsor, preset injection) is the DLC half of that surface, and
  the one the base-game chain was fenced out of. ⚠️ **Re-ranked the same day:
  the crash persists with all DLC content disabled**, and the base-game
  upscaler lead (DLSS 2 → 4) was itself refuted the same day (anti-aliasing
  Off / FXAA still crashes, README §2b), so DLC-internal code is an unlikely
  cause — read the chain's FR-1 result before spending effort here;
- **the existing `Food` resource** — production, storage, consumption, trade,
  the `Meal` layer on top of it;
- **colonist needs and services** — `FoodServiceBuilding` is already patched in
  base; the DLC adds `PanoramicRestaurant` and `Bakery`;
- **domes, oxygen and life support** — `CreateLifeSupportElements` is overridden
  by three DLC farm classes; `ApplyOxygenProductionMod` by two;
- **storage / depots / drones** — new resources need depots and drone routing;
- **rockets, cargo and trade** — `Cargo` preset;
- **tech tree, laws, policies** — `Tech`, `LawDef`, `PolicyDef` inject into
  shared preset groups; `GatherLawTraitWeights` is one of the four DLC hooks;
- **save / load** — `PersistGatherPermanents` is another of the four. ⛔ Weight
  this: a save-breaking DLC bug is the worst class for a player, and
  `SavegameFixups` for the new content is exactly the under-tested surface;
- **achievements** — `Achievement.lua` in both DLC trees plus base
  `Data/TrophyGroup.lua`;
- **`thomas`'s sponsor** — a new sponsor changes starting resources, goals and
  faction behaviour, all of which the base game's mission setup reads.

## 3 · ⛔ What a source read CANNOT settle here — and the play leg

Say this up front in your chain, do not bury it. Much of a DLC's defect surface
is **balance, UI, localisation, art and progression**, none of which a Lua read
reaches. ⚠️ And `EF-079`: **1.0.7 saves cannot load on 1.1.0**, so any play
fixture must be provisioned fresh — hours, not a warm-up.

⇒ Your chain should end with a **short, scripted play leg** the owner can
actually run — a numbered list of things to build and watch, with predictions
written down FIRST so a difference is a finding rather than something adjusted
afterwards. ⭐ Owner time is the scarce resource: **batch it into one sitting**
and make every step earn its place. ⛔ Do not propose "play the DLC and see".

## 4 · What a finding must contain

As `prompts/vanillahunt/README.md` §3 — route re-derived, file:line, who reaches it,
**a falsifier**, severity in player terms — plus one more that is specific here:

⭐ **Does it affect players who do NOT own the DLC?** That single question sorts
findings into two very different severities, and it is the one the developers
are least likely to have tested.

⛔ Nothing is `tested` from a source read. ⛔ A finding is a **candidate defect**,
filed — never automatically a fix-pack module. The pack just shed 36 modules;
the bar for adding one is `FIX_POLICY` and it is the owner's decision.

## 5 · Bindings

- ⛔ **Never modify the game directory** — including the `DLC/*.fpk` files.
- ⛔ `H-02` no Mod Editor, no `version` edit, **no upload**. `H-08` never pull a
  junction. `H-09` never stage a packed folder beside a live one.
- ⚠️ Archive `ModTools\Src` before any game update (`C:\Dev\SMR-SrcArchive\`,
  standing rule in its README). A DLC patch overwrites the DLC source too.
- `python tools/doccheck.py` GREEN before any doc commit; a WARN goes
  **verbatim** into your summary. `git commit -F <file>`, then push.
- ⚠️ Explicit FILE paths on every `git add` — ⛔ never `add -A`, never a
  directory pathspec (both swept a peer's work on 2026-09-08).

## 6 · Your deliverable

`prompts/dlccheck/` — a chain per `CHAIN_METHOD.md`, README manifest, inbox and
outbox per link, terminal adversarial audit. Size each link to one context and
**split up front** rather than mid-link.

A defensible first cut, to argue with:
1. `thomas` **in full** — small, completable, and it banks a real result early;
2. the **non-owner path** — enumerate base-game references to DLC content and
   separate genuine dependencies from name collisions (§1.2);
3. **presets and data** — the shared registries the DLC injects into (§1.3);
4. `norman` **Code**, by seam from §2, hardest last;
5. the **scripted play leg** for the owner, predictions written first;
99. terminal audit — re-derive a sample from scratch, and rule on whether §1's
    "mostly additive" premise actually held, since the whole chain shape rests
    on it.

⭐ **Build the subagent fan-out of §7 into links 3 and 4** — the preset pass and
the seam pass are parent-orchestrates-agents work, not one session reading
15,794 lines.

⛔ **That premise is the thing most worth attacking.** It came from a function-
name sweep and an `OnMsg` count on 2026-09-08 — a shallow instrument, of exactly
the kind this project keeps getting caught by. **Re-derive it before building on
it**, and if the DLC turns out to patch base behaviour more than it appears to,
say so loudly: the chain is then shaped wrong and should be rebuilt.

## 7 · ⭐ USE SUBAGENTS — this effort is big enough to warrant it (owner instruction)

⚖️ **Owner, 2026-09-08: where the work is large enough to warrant it, the hunts
should split it across subagents.** `norman` qualifies at **138 files / 15,794
lines** across genuinely separable subsystems. ⚠️ **`thomas` does not** — 13
files / 1,273 lines is one agent, or just read it. Fanning out work that fits in
one head costs more than it saves.

### The principle: fan out the READING, keep the JUDGEMENT central

⭐ Each agent burns a large context reading source and returns a small
structured result. One session cannot hold 15,794 lines of new content plus the
base-game systems it touches — but it can hold the verdicts.

### ✅ WHERE IT WORKS HERE

- **One agent per SEAM from §2** — food resource, colonist needs and services,
  domes and life support, storage and drones, cargo and trade, tech/laws/
  policies, save-load, achievements. The seams are the natural unit because each
  is "this new thing meets that old system", which is one question.
- **One agent per PRESET GROUP** (`CropPreset`, `Meal`, `Resource`, `LawDef`,
  `PolicyDef`, `Tech`, `Cargo`) — each injects into a different shared registry,
  and §1.3 says this is where DLC QC is worst and our instruments blindest.
- **The non-owner enumeration (§1.2)** — 12 base files referencing DLC content,
  each independently answerable: *is this a genuine DLC dependency or a name
  collision?* ⛔ Both directions, per §1.2's warning.

### ⛔ WHERE IT DOES NOT

- **Ruling on §1's "mostly additive" premise.** The whole chain shape rests on
  it, 99 is told to attack it, and it is a judgement about the DLC as a whole —
  ⛔ not something to assemble from fragments that each saw one file.
- **Designing the play leg.** It is one scarce sitting of owner time; it needs
  one author who knows everything the chain found.
- **Synthesis and the verdict.**
- ⛔ **ANY WRITE TO A SHARED FILE.** Subagents READ and REPORT; **the parent
  writes.** Several sessions edit this tree at once and the git index is shared.

### ⛔ WHAT A SUBAGENT MUST RETURN — evidence, never a verdict alone

**file:line · what the new content does · which existing system it touches · the
route, re-derived · who reaches it · the falsifier · ⭐ and does it affect
players who do NOT own the DLC** (§4's question — it sorts severity and the
developers are least likely to have tested it).

⛔ **"Looks fine" is a rejected result.** An agent returning a conclusion without
its route has produced the shallow-instrument failure this hunt exists to catch.

### ⛔ THE CONTROL — a fan-out that cannot be falsified is not evidence

**"Nine agents found nothing" is indistinguishable from "nine agents read
badly."** Seed known positives into the pool without flagging them and check
they come back — and here the seeds must be REAL, because unlike the vanilla
diff this content has no catalogue of known defects yet. ⇒ ⭐ **derive two or
three yourself, by hand, before fanning out**, and use those as the calibration.
⚠️ **Report the control's hit rate in the chain's output**; a "nothing found"
pass means nothing without it.

### Practical notes

- ⛔ **`Explore` is the WRONG agent type for this.** It reads excerpts to LOCATE
  code; it does not review it. Use it to find where a preset is consumed, never
  to judge whether the interaction is broken.
- ⚠️ **Presets are DATA, and an agent skimming Lua will skim past them.** If you
  fan out preset work, say explicitly that the deliverable is field-level — which
  key, what value, which base-game consumer reads it.
- ⚠️ **Subagents are parallelism WITHIN a link** — not a substitute for splitting
  the chain (`CHAIN_METHOD` rule 4), and ⛔ **not a substitute for the terminal
  audit**. A fan-out is many shallow reads; an audit is one adversarial fresh
  context. You need both.
