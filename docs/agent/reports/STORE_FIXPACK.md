# Store description — Relaunched Fix Pack (build, release item ③)

**Built 2026-08-13 by `agent/prompts/public-docs/03_BUILD_STORE.md`.** Design:
`PUBLIC_DOCS_DESIGN.md` (§4 tiers, §4.2 order, §4.4 no count, §4.5 vocabulary).
Raw material: `docs/archive/MOD_DESCRIPTION.md` (FROZEN — split, never edited).

> ⚠️ **This is a report, and reports are not authority.** Where it disagrees
> with an `agent/bugs/` entry or an `agent/facts/` fact, the entry wins.
> Every count in the player text was re-emitted with `--emit-counts` at the
> moment it was written (2026-08-13), never copied.

⛔ **Everything between the two `═══ PLAYER TEXT ═══` rules is player-facing and
is governed by chain rule 4** — no file path, no function name, no `F##`/`D##`
id, no house word. The notes above and below that block are agent material and
cite freely. **Anything marked `⛔ HOLE` is not publishable and is not filled in
by guessing.**

**Not yet published anywhere, by rule 5.** The owner posts this; no agent does.

---

═══════════════════════════ PLAYER TEXT — BEGIN ═══════════════════════════

## Relaunched Fix Pack — Surviving Mars: Relaunched

Bug fixes for *Surviving Mars: Relaunched* — it repairs defects in the game's
own code rather than rebalancing the game, and it is safe to add to a save you
have already played.

**Four things before the list, because they are what actually decide whether you
want this.**

- **Your existing save is fine, including a long one.** The pack writes almost
  nothing into your savegame, and here is everything it stores by name: a
  timestamp on a housing reservation, a timestamp on a colonist who has just
  taken shelter, a "the player has set this payload" flag on a rocket, and a
  handful of small stamps and flags that let a repair know it has already run,
  or hold one decision for as long as a single weather event lasts. None of that
  means anything to the game without the pack, a couple of the stamps clear
  themselves the next time you save, and older ones left by earlier versions are
  deleted as they are found. **One item is deliberately not inert:** where a
  repair put back a bonus
  that a broken patch migration dropped, that bonus is an ordinary one of the
  kind the game hands out itself, and it goes on working without us — which is
  the entire point of restoring it. It is a list rather than a summary on
  purpose.
- **It fixes bugs rather than rebalancing the game.** Almost every fix targets
  something we verified in the game's own code: the code says one thing, does
  another, and we make it do what it says. Preferences and features are not in
  here. **Five of them are judgment calls rather than plain repairs** — in two
  of those the game's code is not wrong at all and we made a call anyway, and
  one of them changes how the game feels. All five are listed further down,
  with our reasoning, rather than quietly folded in.
- **You do not need anything else.** The pack works on its own.
- **You can take it out again.** It is built to be safe to add or remove at any
  time. Remove it and the bugs it was holding back come back; repairs it already
  made to your save stay made.

**Playing on Xbox, PlayStation or the Microsoft Store version?** One platform
rule to know before you install, and it applies to every mod rather than to this
one: **while any mod is enabled, the game does not unlock achievements on Xbox,
PlayStation or the Microsoft Store.** Steam and other PC versions are not
affected — achievements keep unlocking there with mods enabled.

**What stands behind that, plainly.** Every fix inspects the game's own code
before it patches anything and switches itself off if the game no longer looks
the way that fix expects — so an official patch that changes the shape of the
code a fix was written for retires our version of it instead of fighting it.
That check notices shape: a function renamed, removed or restructured. A patch
that quietly rewrites the inside of the same function is beyond it, which is why
we watch official patches and update rather than promising the pack retires
itself. Nothing is patched on disk; the mod wraps
the game's own code while it runs, and no game files are modified. An automated
suite of 96 checks is run against the game with the pack and without it.

**And what does not.** We cannot test every combination of other mods, every
colony shape, every save state or every future game patch. If a save matters to
you, back it up before adding *any* mod to it for the first time — that advice
is not specific to this pack, it is just true, and most people learn it the
expensive way.

### What it fixes

Rather than a list of every repair, here is the shape of what is in scope, with
one example each. Some of these also repair damage already sitting in your save
when you load it, wherever the pack can positively identify what went wrong.
⛔ HOLE — [site link: the full searchable fix list].

- **Disasters & weather** — a meteor storm that ended could switch your weather
  off for the rest of the colony's life: no rains, no cold waves, no dust
  storms, and one mystery stuck with them. Colonies already in that state are
  put right the moment you load them.
- **Colonists & domes** — colonists walking between two nearby domes went across
  the surface instead of through the passage you built for them, a walk their
  oxygen only survives if nothing delays them.
- **Drones & logistics** — a landed automatic rocket cancelled the orders of
  every drone walking towards it, once per game hour, so any delivery that took
  longer than an hour could never finish no matter what priority you set.
- **Buildings & economy** — salvaging an upgraded building left its dome-wide
  and colony-wide bonuses behind forever, and rebuilding stacked another copy on
  top. Bonuses already leaked into your save are cleaned up when you load it.
- **Trains** — salvaging a single piece of track could delete the whole line and
  every train assigned to it, instantly and with no confirmation. Curves and
  short tracks were the worst of it.
- **Rockets & asteroids** — landing a lander manually made it treat the fuel
  reserved for the trip home as surplus and unload it. On an asteroid with no
  drones, that was permanent.
- **Story, mysteries & the numbers on your screen** — eleven rows of the Command
  Center's resource panel rendered as blank space; freeing the wisps in St.
  Elmo's Fire produced about a thousandth of the power the game promised.

**One fix moves numbers you will see.** The Automation policies take half the
workers from every building they cover and are meant to raise output per worker
so overall production stays where it was; some of the buildings on those
policies — the Workshops, the Security Stations and Posts, the Drone Assembler
and the *Experiment 1: Big Drop* site — never received that pay-back and lost
roughly half their output. Now they receive it like everything else, so while
one of those policies is active, their numbers — workshop comfort, security
coverage, drone production, research — visibly rise to where the policy was
always meant to leave them.

### A few of these are judgment calls, and we would rather say so

Almost everything in this pack is a plain repair: the game's code says one
thing, does another, and we make it do what it says. **Five are not that
simple.** They are still repairs we stand behind — but each one required us to
decide what the game *meant*, and reasonable people could decide differently.
They are marked in the list, they cannot be switched off from the game's own
menus on any platform, and here is what each one is:

- **Drones writing a building off after one blocked approach** — a comment in
  the game's own code says that permanent mark is deliberate. In a real colony
  the condition that clears it does not reliably happen, and we think that
  effect is harmful enough to override the comment. *(behaviour change,
  defended)*
- **Biorobots and Dust Sickness** — there is no coding error here. A dust
  illness that infects synthetic colonists is a thematic judgment, and we made
  it. *(design judgment)*
- **Colonists sheltering in vacuum** — we added a reflex the game does not have,
  rather than repairing one it has. An absence, not a mistake. *(added safety
  behaviour)*
- **Edit Payload remembering what you told it** — treating the flight policy's
  list as a *default* rather than a *refill* is arguably how it was designed. We
  think a row you deliberately emptied should stay empty. *(design judgment)*
- **Dust devil wave sizes** — this restores the wave sizes the map settings were
  written for. On some map settings that means noticeably more dust devils than
  the game has ever actually delivered, in either the original or the remaster.
  *(restores authored settings — more devils on some maps)*

### Your save, and what happens when the pack is gone

**Damage that already happened.** Most fixes help immediately: anything about
ongoing behaviour — drones, colonists, schedulers, rockets — starts working
correctly the moment you load. Some damage needs active repair, and the pack
tries: every time you load, it looks for specific damage already sitting in your
save and undoes what it can positively identify. Every pass is deliberately
conservative, does nothing when unsure, and does nothing at all the second time
it runs. It is a genuine attempt at repairing an already-damaged save, not a
promise that it will repair *yours*. ⛔ HOLE — [site link: the save-repair page].

**History that is gone stays gone.** Colonists who already died stay dead,
destroyed buildings stay destroyed, expeditions lost to the lander bugs are
lost. Trains voided by the station bug cannot be restored exactly — but you can
build replacement trains at any station for Metals and Electronics.

**Removing the pack.** It comes out as cleanly as we could make it: the bugs
come back, the repairs already applied to your save stay, and the bookkeeping
fields listed at the top sit there unread by the unmodded game — a couple of
them clear themselves the next time you save. If a save happened to catch the pack
part-way through a piece of work, that leftover finishes on the game's own code
and stops. Turning this pack off in the mod manager takes effect after you
restart the game.

### Other mods

Built to coexist. We patch the smallest thing that fixes each bug, chain
politely with other mods' hooks, and every fix checks the game's code first — so
if an official patch changes the shape of the code a fix was written for, our
version of that fix stands down instead of fighting it. The pack is built against game version 1.0.7.396349, and a fix that
no longer recognises the code it was written for switches itself off rather than
guessing.

Individual fixes can be switched off, but only by a companion mod that loads
before this one — a modder's facility rather than a player's, and there is no
in-game switch for it on any platform. ⛔ HOLE — [site link: the modders page].

### Reporting a bug

Tell us what happened, roughly when it started, and whether it survives a
save and reload. A save file where the bug reliably happens is worth a thousand
words. On PC the game's logs are usually in your
`%AppData%\Surviving Mars Relaunched\logs` folder, and Ctrl+F1 opens the
official bug reporter (on Steam Deck the game leaves that one out). On Xbox and
PlayStation there are no logs or console commands to collect, and a plain
description —
platform, what happened, when it started, whether it survives a save and reload
— is still genuinely useful.

### Credits

- **ChoGGi**, whose "Fix Bugs" collection for the original *Surviving Mars*
  documented dozens of these bug families years before the remaster. Every fix
  here was independently re-verified against the Relaunched code.
- **LukeH**, for Martian Express patch research on the original game.
- Everyone reporting bugs on the Paradox forums and Steam discussions — many
  fixes here started as your report.

═══════════════════════════ PLAYER TEXT — END ═══════════════════════════

---

## Notes — what is deliberate, what is a hole, what a later prompt must do

### The holes, in order of appearance

| # | hole | who closes it |
|---|---|---|
| 1 | **Site links ×3** (fix list · save-repair detail · for-modders page) | the site is `workflow_dispatch` only and Pages is off; links exist when the owner turns it on |
| 2 | ~~**The fifth judgment-call bullet** — the dust-devil scale word~~ ✅ **CLOSED 2026-08-13 by the owner** (*"change any wordings to their accurate versions"*). The bullet is in the text above, in the phrasing approved 08-02: *"on some map settings"*. ✅ Checklist line struck by the terminal audit 2026-08-13 after re-deriving the bullet from `F97.md` | done |
| 3 | **Store links** to the companion mod | do not exist until upload (design §12 hole 8) — ⚖️ **PARKED 2026-08-17**: the opt-in mod does not publish at this launch and its sentence left the card (`PARKED_OPTIN_REFERENCES.md` P40a–P40d) |
| 4 | **The uninstall-cleanliness sentence** | ⛔ deliberately **not placed** — Reading A vs B is an owner call at launch (design §8) |

### 22b — closed by the owner 2026-08-13, and what is still owed

**The owner's words:** *"You can change any wordings to their accurate
versions."* ⇒ the fifth bullet is now in the player text above, in the phrasing
approved 2026-08-02 — *"on some map settings"*. ⛔ **"Most" was NOT used**, even
though it is defensible at five of six presets: drifting from an approved phrase
is the exact failure 22b was raised to stop, and the approved phrase is true.

**Re-derived from `F97.md:334-352` — the entry's own table, not from prose:**

| preset | change |
|---|---|
| `Low` · `High` | +50% each |
| **`VeryHigh` — the heaviest shipped preset** | **0%, the only untouched one** |
| `VeryHigh_1` | +25% |
| `VeryHigh_2` | **+125%** |
| `VeryHigh_3` | +5% |

⚠️ Five of the six map-selectable presets rise (`VeryLow` is `forbidden = true`
and excluded). ⛔ **Do not quote the +170% figure** the design report attributes
to the class defaults: that row is `CrystalBig`/`CrystalSmall`, both
`use_in_gen = false` and marker-driven, and the entry says their
natural-scheduler numbers are probably dead.

✅ **The checklist line 22b was struck by the terminal audit 2026-08-13** after
independently re-deriving the bullet from `F97.md` (rate table `:334-352`; the
both-games clause from the OG disassembly `:407-421`) — the shipped wording is
the owner-approved 08-02 phrase and it is accurate. ⚠️ The bullet landed
**after** the six sweeps; it has now been through the terminal audit's
independent evidence and route sweeps in addition to the by-hand rule-4/§4.5
check, and it passed all of them.

### unattended-3 — applied 2026-08-15 by that chain's terminal audit (`03_AUDIT_FABLE.md`)

Five player-text edits, forced by the two modules that chain shipped (F85
`Fix_DistressPopupPause`, C39 `Fix_AutomationLawCompensation`), all counts from
`--emit-counts` at edit time, all claims control-checked against Src/modules
BEFORE the entries' own reasoning was read (the firewall):

1. "Five of them are judgment calls … in two of those … All five" → **Six … in
   three … All six** (tier 0). The F85 flip meets the card's own definition
   exactly — the game's code is not wrong and we overrode a deliberate dev
   choice — and its module header carries the ⚖️ DISCLOSURE. Settled as SIX
   everywhere (card, metadata, site FAQ, fix list), reasoning here.
2. "suite of 94 checks" → **96** (emitted; delta is exactly the two new probes).
3. "Six are not that simple." + a sixth judgment-call bullet (distress-call
   confirmation), placed before the dust-devils closer, same `*(design
   judgment)*` tag family.
4. NEW paragraph after the category bullets — the C39 disclosure the owner's
   08-15 ruling still owed ("the card must still say this moves
   gameplay-visible numbers"). Names are display names; the four families never
   watched in a game are not upgraded by the wording ("meant to", "rise to
   where the policy was always meant to leave them" — no per-building
   measurement implied).
⛔⛔ **EDITS 1 AND 3 WERE REVERSED THE SAME DAY — read them as history, not as
the current card.** The owner ruled (checklist 31) that `Fix_DistressPopupPause`
be REMOVED: the popup it pauses is dead-coded out of the retail build, so the
fix could never fire for a player. The judgment-call count is back to **FIVE …
in two … All five**, *"Five are not that simple."*, and the distress-call bullet
is **deleted** from the card. Edit 2's suite count also moves **96 → 95** (the
F85 probe left with its module). Edits 4 and 5 stand unchanged. The module and
its probe are preserved verbatim, with a re-arm trigger, in
`SHELVED_F85_DISTRESS_PAUSE.md`; if it is ever re-applied, every number here
moves back by one and the card bullet must be **rewritten, not restored**.

⛔ **2026-08-16 public-docs checkup: that "96 → 95" was a PREDICTION and it did
not survive the measurement.** The `C47` wave-11 probe (`61_Probes_Wave11.lua`)
landed the same day F85's probe left, and the real launch read **`80/0/16/0` of
96** (`archive/c47suite4_*`, 2026-08-15, gates `75/75` + `8/8`, SKIP set
unchanged BY NAME). The card's sentence is corrected to **96**, re-emitted
2026-08-16 — the 95 sat on this card and its release copy for a day because it
was inherited from the prediction instead of re-emitted.

5. No change to the tier-1 save-footprint list: both new modules persist
   NOTHING (F85 Layer 3, C39 Layer 2 by construction — stated on both modules
   and both entries), so the enumerated footprint is unchanged.

### R1 — applied 2026-08-14 by the site chain's terminal audit (`06_AUDIT.md`)

The patch-retirement claim was narrowed in both places it appears: "changes the
code a fix was written for" → "changes the **shape** of the code", and the tier-1
version now carries the honest limit in two sentences (shape = renamed / removed /
restructured; a same-named body rewrite is invisible to the check, so we watch
patches rather than promising self-retirement). Re-derived from
`00_Core.lua:492-497` at apply time. Licence: 22d item 1 (this exact claim,
approved 2026-08-13) + the 22b standing word ("change any wordings to their
accurate versions"). ⚠️ `metadata.lua`'s `description` keeps the conditional the
owner approved verbatim in 22d(1) ("stands down if an official patch changes what
it was written for") — one notch softer than the site's shape-formulation;
release prep re-checks portal limits anyway and can adopt the shape wording then.

### Deliberate departures from the design, and why

1. **Tier 0 does not say "it does not change how the game is balanced."** §4.1's
   draft sentence did. Under the design's own §5.1 refutation that is a tier-0
   claim tier 2 has to widen (five judgment calls; more dust devils on some map
   settings), which is exactly what §4.1 forbids. *"Repairs defects in the
   game's own code rather than rebalancing the game"* survives the standalone
   test and keeps the install-gating force. ⚠️ **The tier-1 bullet was the same
   defect and was caught in arbitration, not in the write** — see
   `STORE_BUILD_AUDIT.md`, sweep 5 finding F2/F7.
2. **Seven category lines, not §4.2's "four or five".** §4.3 proposes eight
   buckets; seven is the honest merge (interface and story share a line). Bucket
   sizes are prompt 5's to re-derive, and the count is not load-bearing here.
3. **The per-fix disable paragraph is one identifier-free sentence on the card,
   and the modder instructions are routed off it.** the chain's QA prompt flagged the
   tension — the rewritten paragraph is useless without an identifier, and rule
   4 bars identifiers from player text. Silence is worse than a pointer, because
   the frozen file promised something here; so the card names the route and its
   limit, and the identifier-carrying instructions go to a for-modders corner of
   the site. ⚠️ **The load-order half is an open hole** (design §12 hole 3): we
   have no measured answer for how a modder guarantees loading first, so the
   sentence states the condition and promises no method.
4. **No console instruction anywhere, and no claim that anything is listed on
   screen.** §9.1 as corrected: the console route works for an unpredictable
   minority of fixes and a player cannot tell which. Hole 11 (does the list
   command put anything on screen at all) is unsettled until the sitting.
5. **The "no other mod has held itself to this standard" sentence is absent**,
   with its whole surrounding paragraph. It is entangled with the deferred
   uninstall-cleanliness call, and §7's rule bars saying what other mods do not
   do. The engine explanation it carried is kept in substance — the footprint is
   a list rather than a summary — without any comparison.
6. **Neither `F76` draft block was carried across in any form** (§5.6). Both sit
   quarantined at `MOD_DESCRIPTION.md:225-249`.
7. **The "dismissed warnings come back" essay is not here.** It is an FAQ
   question by §6.1, and the module that addresses it lives in the other mod.

### What this text asserts, and where each assertion comes from

| claim | source |
|---|---|
| save footprint enumeration | `D13_EXPOSED_SET.md` §2b rows D1–D11 (fix-pack rows only), MEASURED where marked; §2c for the negative half |
| ~~the engine's mod-reference notice on the next load, self-clearing~~ **STRUCK from the card 2026-08-14 (checklist 29, owner-ruled)**: the measured line is LOG-only and the on-screen warning skips `optional_mod` mods — no player of this mod ever sees it | `D13_EXPOSED_SET.md` §10.9(4) — whose "sees one notice" aside was a rig-console inference; route: `Mod.lua:1199` (ModLog), `SavegameMetadata.lua:97-99` (optional filter) |
| repairs already applied stay | §2b D10 (`SMRFixPack_F35_*`) + D11, both on the KEEP list (§5) |
| suite of **96** checks, modded vs unmodded | `python tools/doccheck.py --emit-counts`, re-emitted 2026-08-16: `TestKit probes: 96`; measured `80/0/16/0` of 96 (`archive/c47suite4_*`, 2026-08-15). History: 94 → 96 (`unattended-3` probes) → 95 (item-31 **prediction**, F85's probe out) → 96 (the `C47` wave-11 probe landed the same day); A/B pair `WORKFLOW.md:274` |
| **five** judgment calls (briefly six on 2026-08-15, reverted the same day) | the five modules by name: `Fix_DroneUnreachableForever` · `Fix_DustSicknessBiorobots` · `Fix_ShelterReflex` · `Fix_PayloadTemplateRefill` · `Fix_DustDevilSpawnGate`. ⛔ `Fix_DistressPopupPause` was the sixth for a few hours and is **REMOVED** (owner ruling, checklist 31 — its popup is dead-coded out of retail); census re-run 2026-08-15 after the removal |
| Automation-policy disclosure paragraph | `C39.md` §2026-08-15 (owner ruling: scope ships as built, disclosure still owed); building names are DISPLAY names re-read at the templates 2026-08-15 (`BottomlessPitResearchCenter` displays as **"Experiment 1: Big Drop"** — never call it "the Bottomless Pit" in player text); consumers `SecurityStation.lua:13`, `DroneFactory.lua:75-79`, `BottomlessPitResearchCenter.lua:45`, `TVStudioWorkshop.lua:100`, `ArtWorkshop.lua:24` |
| ~~distress-call judgment bullet~~ **DELETED from the card 2026-08-15 (checklist 31, owner-ruled) along with its module** | `F85.md` §2026-08-15 (later): `DistressCallPopup`'s sole caller is compiled behind a literal `local cond = false` (`POIAdditionalContent.generated.lua:89-111`), so no player can raise that dialog and the fix could never fire. Module + probe preserved verbatim in `SHELVED_F85_DISTRESS_PAUSE.md` |
| game version 1.0.7.396349, self-check stand-down | `EF-014`; per-fix `apply()` self-checks |
| achievements on Xbox / PlayStation / Microsoft Store | `Achievement.lua:61-63`, consumed `:77`; re-derived by the chain QA, recorded `PUBLIC_DOCS_DESIGN.md` §6.2 |
| neither mod needs the other | opt-in split chain, measured both directions 2026-08-12 (checklist 15) |
| disasters example | `F81` (`tested`, PROVEN; heal-on-load observed organically 2026-08-02) |
| colonists example | `F52` (`tested`) |
| drones example | `F50` (`tested`, PT-04 PASS) |
| buildings example | `F03` (`tested`, PT-02 PASS; sanitizer clears existing saves) |
| trains example | `F44` (`tested`, PT-03 PASS post-rework) |
| rockets example | `F69` (`tested`, PT-16 PASS) |
| interface + story examples | `F13` (`tested`, PT-08 PASS) · `F07` (`tested`, MEASURED + owner-witnessed) |
| replacement trains for Metals + Electronics | chain QA route sweep, re-walked by this build's sweep 4 (`customStation.generated.lua:14-29`, `Station.lua:628-634`) — walkable on all three platforms; the "game never tells you" claim was cut as overstated |
| mod disable needs a full restart | D13 / `STATE.md` gate line |

### Owed elsewhere

* `metadata.lua`'s `description` and `short_description` — ✅ **APPLIED at the
  owner's word 2026-08-13 (`1ac1187`)**, superseding the fence routing: the live
  `description` had carried the false console claim and the dead working title,
  and the draft strings carried the same two faults, corrected before apply.
  ⚠️ Portal character limits are still unchecked (`STORE_METADATA_STRINGS.md`)
  — that half stays with release prep.
* This text becomes release item ③'s input, not a replacement for it.
