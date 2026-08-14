# Release description — Community Fix Pack (the file the owner pastes from at ④)

**Assembled 2026-08-14 by `agent/prompts/release-3/01_BUILD_DESCRIPTIONS.md`.**
This **supersedes `docs/archive/MOD_DESCRIPTION.md`** for this product. That file
is FROZEN and known-false in at least six places; nothing was carried across from
it here.

⭐ **The player text below is VERBATIM from `STORE_FIXPACK.md`'s audited block**
(built 2026-08-13, six sweeps + terminal audit 2026-08-14, R1 applied). This file
re-authored **nothing**. What it adds is only the two things a paste-ready file
needs and a report does not: **every hole rendered as an unmissable `>>> FILL-IN
<<<` marker**, and the instruction for each one beside it below.

⛔ **Not published. Rule 5 — the owner pastes; no agent does.**

---

## Before you paste — the four fill-ins, and what each one needs

Each marker appears in the text as `>>> FILL-IN n — … <<<` on its own line.
**Every one of them is a link that does not exist yet**, so each has a
*delete-instead* answer that is always safe.

| n | where | needs | if it does not exist yet |
|---|---|---|---|
| **1** | end of "What it fixes" intro | link to the **fix list** page | ⛔ **delete the whole marker line.** The section reads correctly without it — it is an offer of more detail, not a promise |
| **2** | "You do not need anything else" bullet | **store link** to *Community Fix Pack: Opt-In Modules* | delete the marker. The sentence already names the mod, which is enough for a search |
| **3** | end of "Damage that already happened" | link to the **save-repair detail** | ⛔ delete the marker line |
| **4** | end of "Other mods" | link to the **for-modders page** | ⛔ delete the marker line. ⚠️ This one is the weakest without its link — the paragraph says an identifier exists and does not give it. That is deliberate (rule 4 bars identifiers from player text), but if the site is not on, consider deleting the *whole* second paragraph of "Other mods" rather than leaving a dead-end offer |

### The site links (1, 3, 4) — what they resolve to

The site is **built and terminal-audited** (`SITE_BUILD_AUDIT.md`, 2026-08-14)
and lives at `C:\Dev\SMR-CommunityMods\content\`, five pages. ⛔ **Nothing is on
the web**: the publish workflow is `workflow_dispatch`-only and Pages is OFF
(`.github/workflows/publish-site.yml:25-26`), so **these links exist only after
you switch Pages on** — which is a step in the portal-prep sheet, and it comes
*after* the store upload for a reason stated there.

The page each marker wants, verified against the built tree and `mkdocs.yml`'s
`nav`:

| n | page file | path under the site root |
|---|---|---|
| 1 | `content/fix-list.md` | `fix-list/` |
| 3 | `content/faq.md`, section *"Will it fix a save that is already broken?"* | `faq/#will-it-fix-a-save-that-is-already-broken` |
| 4 | `content/for-modders.md` | `for-modders/` |

⚠️ **The site root is not yet a fact.** `mkdocs.yml` sets no `site_url`, so the
address comes from GitHub Pages, and for the repo `catt144/SMR-CommunityMods`
that is the standard project-pages form — but ⛔ **do not type it from memory:
GitHub prints the real address on the repository's Pages settings screen the
moment you enable it. Copy it from there.** (`use_directory_urls` is left at its
default `true`, which is why every path above ends in `/` and not `.md`.)

### The store link (2)

Does not exist until you have uploaded the other mod and the portal has given it
a URL. **Upload both mods first, then come back and fill this in** — the
portal-prep sheet sequences it.

⚠️ There is a **second**, optional place a companion-mod link fits: the last
sentence of *"Removing the pack"*, which tells the reader to read that mod's
uninstall note. It is left unmarked on purpose — one link per page is enough and
two invites a dead one. Add it only if your portal makes links cheap.

---

## ⚠️ One sentence is deliberately absent, and it is your call at ④

**The uninstall-cleanliness sentence is NOT in the text below and its absence is
intentional** (`PUBLIC_DOCS_DESIGN.md` §8, the row that says *do not place it*).
The card states the *shape* of removal — the bugs come back, the repairs stay,
the bookkeeping fields sit unread — and stops short of a claim about how cleanly
the pack comes out, because that wording depends on a decision only you can make:

* **Reading A — the pack alone.** The pack comes out as cleanly as it can on its
  own, and the drone-dial caveat lives on the *other* mod's page where the dials
  are.
* **Reading B — the pack plus a cleaner.** The sentence is rewritten to say a
  separate tool finishes the job, which **only works if Save Rescue is published**
  (checklist 17, "build ≠ publish").

⇒ **This is one of the three calls that must be answered together at ④**:
checklist **17** (does Save Rescue publish), **28** (the rescue dialog's text),
and this one. The portal-prep sheet asks them as a single question, in order.
⛔ **Nothing below assumes either reading**, so the text is paste-ready whichever
way you rule.

---

═══════════════════════════ PLAYER TEXT — BEGIN ═══════════════════════════

## Community Fix Pack — Surviving Mars: Relaunched

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
  here; they live in a separate mod you do not need. **Five of them are judgment
  calls rather than plain repairs** — in two of those the game's code is not
  wrong at all and we made a call anyway, and one of them changes how the game
  feels. All five are listed further down, with our reasoning, rather than
  quietly folded in.
- **You do not need anything else.** The pack works on its own. There is a
  companion mod, *Community Fix Pack: Opt-In Modules*, and neither mod needs the
  other — each works alone, and they work together.
>>> FILL-IN 2 — store link to the opt-in mod, or DELETE THIS LINE <<<
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
suite of 94 checks is run against the game with the pack and without it.

**And what does not.** We cannot test every combination of other mods, every
colony shape, every save state or every future game patch. If a save matters to
you, back it up before adding *any* mod to it for the first time — that advice
is not specific to this pack, it is just true, and most people learn it the
expensive way.

### What it fixes

Rather than a list of every repair, here is the shape of what is in scope, with
one example each. Some of these also repair damage already sitting in your save
when you load it, wherever the pack can positively identify what went wrong.
>>> FILL-IN 1 — link to the full searchable fix list, or DELETE THIS LINE <<<

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
promise that it will repair *yours*.
>>> FILL-IN 3 — link to the save-repair detail, or DELETE THIS LINE <<<

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
restart the game. If you also use *Community Fix
Pack: Opt-In Modules*, read the uninstall note on that mod's page before you
remove **it**: it has settings that leave something behind in your save, and its
page tells you the two steps that avoid it.

### Other mods

Built to coexist. We patch the smallest thing that fixes each bug, chain
politely with other mods' hooks, and every fix checks the game's code first — so
if an official patch changes the shape of the code a fix was written for, our
version of that fix stands down instead of fighting it. The pack is built against game version 1.0.7.396349, and a fix that
no longer recognises the code it was written for switches itself off rather than
guessing.

Individual fixes can be switched off, but only by a companion mod that loads
before this one — a modder's facility rather than a player's, and there is no
in-game switch for it on any platform.
>>> FILL-IN 4 — link to the for-modders page, or DELETE THIS LINE (and consider deleting this paragraph with it) <<<

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

## Provenance, and the counts re-emitted at assembly time

⚠️ **This is a report and reports are not authority.** The claim-by-claim source
table for every sentence above is `STORE_FIXPACK.md`'s own — not duplicated here,
because a second copy is a second thing to go stale.

**Counts in the player text, re-emitted at assembly (rule 3, never copied from
prose):**

| count in the text | re-emitted | source |
|---|---|---|
| "an automated suite of **94** checks" | `python tools/doccheck.py --emit-counts`, 2026-08-14: `TestKit probes: 94` | the emitter, this session |
| "**Five** of them are judgment calls" | re-derived at the audited fix list, 2026-08-14: exactly five entries carry the `— *judgment call*` title mark (`content/fix-list.md:95, 283, 323, 344, 669`), and they are the same five the card bullets | the shipped page, independently of the card |
| "game version **1.0.7.396349**" | `EF-014`; `STATE.md`'s pinned build line | the fact, not prose |

⛔ **No exposed-set count appears in player text in any form**
(`PUBLIC_DOCS_DESIGN.md` §8's standing bar) — the footprint is enumerated in
player words instead, which is a different artifact from the derivation.

### What changed between `STORE_FIXPACK.md` and this file

**Nothing in any sentence.** Four `>>> FILL-IN <<<` marker lines were placed
(three replacing the card's `⛔ HOLE` notations in place, one — number 2 — newly
placed at the companion-mod sentence, which the card's notes enumerate as hole 3
but never marked in the text). Marker lines are not player text and every one of
them says how to delete itself.
