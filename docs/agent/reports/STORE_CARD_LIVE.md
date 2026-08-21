# Store card — the LIVE page body, reworked 2026-08-20 on the owner's brief

⭐ **This supersedes `RELEASE_DESCRIPTION_FIXPACK.md` for the PAGE BODY only.**
That card stays as the pre-launch record and as the source of the wording this
one inherits. ⛔ It does **not** supersede `metadata.lua`'s `description` — that
string ships inside the mod and cannot change without a version bump.

**The owner's brief, 2026-08-20, at the live pages:** *"our steam and paradox
descriptions formatting looks a bit rough and I want the links on there and we
don't list bug counts. And I would like a list to include of the headliner fixes,
I know we can't list all but maybe the player facing ones and then a line that
says … and more to see a full list and other information along with a bit of
modder info and it being mod friendly."*

## What this pays off, beyond the ask

- ⚖️ **COUNTS: reversed by the owner, same evening.** The first draft carried none,
  on the grounds that every earlier surface's number drifted (68 → 66 → 67 → …).
  The owner then asked for *"a total number of bugs fixed"* and an indication of
  how many are invisible. ⇒ Two numbers are used and **both are checkable by the
  reader on the page the card links to**, which is the only thing that makes a
  count safe here:
  - **79** — entries on the fix list. Emitted, not typed: `grep -c '^??? '`, and
    the section tally sums to the same (18+11+9+9+7+7+7+7+4). ⚠️ It is worded as
    *"seventy-nine repairs"*, not *"79 bugs"* — one entry covers two defects
    ("Two story-scripting defects…"), so entries is the honest unit.
  - **4** — the fix list's own audited section *"Under the hood: these four repair
    things you cannot see today."* ⛔ Not a classification invented for the card.
  - ⛔ **MAINTENANCE DEBT ACCEPTED KNOWINGLY:** adding a fix now means editing two
    store pages as well as the site, or the number is a lie. That is the cost the
    no-counts draft was avoiding; the owner priced it and chose findability.
- ⛔⛔ **TWO OVERCLAIMS CAUGHT AND CUT before this was pasted — the owner asked for
  "possible crashes" and the record does not support the word.**
  - *"Arriving at an asteroid with subsurface Exotic Minerals froze it"* was in the
    first draft's headliners. ⛔ The fix list's own entry says: *"we could not
    reproduce the freeze on our own hardware, so we cannot tell you this cures
    it"* — a Linux/NVIDIA report, fix removes the likely cause, cure unclaimed.
    **Cut.**
  - *"Completing the last milestone crashed the game"* is the fix list's heading,
    but that entry's own **What you saw** is *"the end-of-game milestone popup
    never arriving"* — a script erroring mid-count, which in this engine aborts a
    function rather than killing the client. **Reworded to the symptom.**
  - ⇒ **The pack repairs no confirmed client crash, and the card must not imply
    one.** What it does repair, and what the opening now leads with instead:
    irreversible losses, colonist deaths, things that stop forever, and silent
    arithmetic.
- ✅ **Checklist 47(a)** — the published veto snippet used
  `SMRFixPack_Disabled = SMRFixPack_Disabled or {}`, which reads a name that may
  not exist and trips the engine's strict-global guard. **The safe form is used
  below**, the same one the pack's own code uses.
- ✅ **Checklist 47(b)** — *"it does not matter whether yours or ours is created
  first"* was misleading. **Stated plainly below**: the veto must be set before
  the pack loads, which means the other mod loads first.
- ✅ **Checklist 50** — *"chain rather than clobber"* promised an outcome the code
  delivers at most sites but not all. ⛔ **No count is claimed** (the census tool
  was refuted, `99_TERMINAL_AUDIT` L8-F4); the sentence below says what is true:
  it chains where it can, and copies a corrected body where the bug sits
  mid-function.
- ⛔ **`EF-054` respected** — no other mod is named anywhere.
- ⛔ **No load-order advice to players.** The one ordering sentence is in the
  modder section and is about a modder's own file.

## ⚠️ Markup: unverified per portal — paste PLAIN first

⛔ **Neither portal's markup support has been verified by this project.** The
plain-text version below is written so it reads as structured text with **no
markup at all** — blank lines, capitals, and `·` bullets. It cannot render as
literal garbage anywhere.

⇒ **Paste the plain version first on both.** Then, if you want, try the Steam
BBCode variant — Steam Workshop is widely BBCode-capable, but ⚠️ **this project
has not confirmed it**, so check the preview and revert to plain if the tags show
up as text.

## Links block — ⚠️ two are confirmed, two are not

| link | status |
|---|---|
| Paradox Mods page | ✅ **owner-supplied, pasted from their browser**: `https://mods.paradoxplaza.com/mods/156049/Any` |
| Steam Workshop page | ✅ **owner-verified 2026-08-20 — they opened it and it resolves**: `https://steamcommunity.com/sharedfiles/filedetails/?id=3787202810` *(it was written as the conventional form for item `3787202810` and held open as unverified until that click)* |
| Source code (fix pack) | ✅ confirmed from `git remote`: `https://github.com/catt144/SMR-CommunityFixPack` |
| The full fix list | ⏳ **needs the site.** Pages source is set to GitHub Actions; the first workflow run prints the URL. The build implies `…/fix-list/`, ⛔ **which is derived, not read** — take the deployed URL. Fallback that works today: `https://github.com/catt144/SMR-CommunityMods/blob/main/content/fix-list.md` |

✅ **Both store links are LIVE on the site** as of `SMR-CommunityMods` `c4e55c4`
(installing page buttons + landing page line), with the console route named —
Paradox Mods serves Xbox and PlayStation, which a console player cannot infer.

---

## ═══ PARADOX MODS — plain text, paste as-is ═══

⚠️ The cross-link at the foot points at STEAM. The Steam version below points
back at Paradox. ⛔ Do not paste the same block on both.

```
Bug fixes for Surviving Mars: Relaunched.

Seventy-nine repairs, each one written up on the fix list with what you would
have seen and what was actually wrong. Every one targets something the game's
own code gets wrong — the code says one thing, does another, and the fix makes
it do what it says. It fixes bugs; it does not rebalance the game. Preferences
and features are deliberately not in it.

Some of them you could hardly miss: an entire train line and every train on it
deleted by salvaging a single hex, colonists suffocating on a walk between two
domes, a lander that unloaded its own return fuel and could never come home.

More of them you would never have blamed on a bug, because the game looked
perfectly normal while the arithmetic underneath it was wrong — a trait's
colony-wide bonus that never reached a single colonist, upgrade bonuses left
behind by demolished buildings and stacking every time you rebuilt, a technology
providing a 10% discount where its own text promises 20%, a Comfort penalty
billed for longer than the journey actually took.

And four of them repair things you cannot see at all today: real defects that
the shipped numbers happen to hide, which another mod, a game patch or a DLC
could walk straight into.


SOME OF WHAT IT FIXES

· The end-of-game popup never arrived in games with No Terraforming or No Politics.
· Eleven rows of the Command Center's resource panel rendered as blank space.
· Colonists walked across the surface between domes and suffocated.
· Rocket loads of new arrivals died on their way to a dome.
· A dome sat half empty and still refused to house anyone.
· Salvaging one piece of track deleted the whole line, and its trains with it.
· Demolishing a station permanently deleted the trains parked there.
· A train parked at a platform and blocked the line forever.
· An asteroid lander unloaded its own return fuel and stranded itself.
· Meteors struck every few hours instead of every day or two.
· A meteor storm ended and the weather stopped, permanently.
· Building an artificial lake buried the rover that built it.
· The Gene Forging research did nothing at all.
· Salvaging an upgraded building left its bonuses behind forever.
· You were never warned about running out of Food or maintenance resources.
· Independent Terraforming gave half the discount it advertises.
· Three pieces of interface text stayed in English in every other language.

… and a good deal more, including quieter repairs to drones, shuttles, domes,
tourism, research, storylines and the interface.

The full list — every fix, what you would have seen, and what was actually
wrong — is here:
https://catt144.github.io/SMR-CommunityMods/fix-list/


HOW IT WORKS

· No game files are modified. The pack wraps the game's own code while it runs.
· Safe to add to a save you have already played. It writes almost nothing into
  your savegame, and removing it simply lets the original bugs come back.
· Every fix checks the game's code before it touches anything, and stands down
  by itself if an official patch changes what it was written for. A fix that
  stands down does nothing at all — it never guesses.
· A few of the fixes are judgment calls rather than plain repairs. Those are
  marked as such on the fix list, with the reasoning, rather than folded in
  quietly.


FOR MODDERS

The pack is built to share the game with your mod rather than take it over. It
hooks the game's functions and calls the original where it can, so another mod
that touches the same function keeps working. Where a bug sits in the middle of
a function and cannot be hooked, the fix copies the corrected body instead —
those are the ones most likely to clash, and each one names in its source the
game file and lines it came from.

Any single fix can be switched off from another mod, without touching this one.
Set the fix's id as a key on the veto table before the pack loads:

    SMRFixPack_Disabled = rawget(_G, "SMRFixPack_Disabled") or {}
    SMRFixPack_Disabled["DustDevilSpawnGate"] = true

The id is the key, not a list entry — a plain list looks valid and switches off
nothing. "Before the pack loads" means your mod has to load first.

Source, and the reasoning behind every fix:
https://github.com/catt144/SMR-CommunityFixPack

Also on the Steam Workshop:
https://steamcommunity.com/sharedfiles/filedetails/?id=3787202810
```

## ═══ STEAM WORKSHOP — BBCode; fall back to the plain block if tags render literally ═══

⚠️ Same words. Only try this after the plain version is safely in place.

```
Bug fixes for [i]Surviving Mars: Relaunched[/i].

[b]Seventy-nine repairs[/b], each one written up on the fix list with what you would have seen and what was actually wrong. Every one targets something the game's own code gets wrong — the code says one thing, does another, and the fix makes it do what it says. It fixes bugs; it does not rebalance the game. Preferences and features are deliberately not in it.

Some of them you could hardly miss: an entire train line and every train on it deleted by salvaging a single hex, colonists suffocating on a walk between two domes, a lander that unloaded its own return fuel and could never come home.

More of them you would never have blamed on a bug, because the game looked perfectly normal while the arithmetic underneath it was wrong — a trait's colony-wide bonus that never reached a single colonist, upgrade bonuses left behind by demolished buildings and stacking every time you rebuilt, a technology providing a 10% discount where its own text promises 20%, a Comfort penalty billed for longer than the journey actually took.

And [b]four[/b] of them repair things you cannot see at all today: real defects that the shipped numbers happen to hide, which another mod, a game patch or a DLC could walk straight into.

[h2]Some of what it fixes[/h2]
[list]
[*]The end-of-game popup never arrived in games with No Terraforming or No Politics.
[*]Eleven rows of the Command Center's resource panel rendered as blank space.
[*]Colonists walked across the surface between domes and suffocated.
[*]Rocket loads of new arrivals died on their way to a dome.
[*]A dome sat half empty and still refused to house anyone.
[*]Salvaging one piece of track deleted the whole line, and its trains with it.
[*]Demolishing a station permanently deleted the trains parked there.
[*]A train parked at a platform and blocked the line forever.
[*]An asteroid lander unloaded its own return fuel and stranded itself.
[*]Meteors struck every few hours instead of every day or two.
[*]A meteor storm ended and the weather stopped, permanently.
[*]Building an artificial lake buried the rover that built it.
[*]The Gene Forging research did nothing at all.
[*]Salvaging an upgraded building left its bonuses behind forever.
[*]You were never warned about running out of Food or maintenance resources.
[*]Independent Terraforming gave half the discount it advertises.
[*]Three pieces of interface text stayed in English in every other language.
[/list]
… and a good deal more, including quieter repairs to drones, shuttles, domes, tourism, research, storylines and the interface.

[b]The full list[/b] — every fix, what you would have seen, and what was actually wrong:
[url=https://catt144.github.io/SMR-CommunityMods/fix-list/]the complete fix list[/url]

[h2]How it works[/h2]
[list]
[*][b]No game files are modified.[/b] The pack wraps the game's own code while it runs.
[*][b]Safe to add to a save you have already played.[/b] It writes almost nothing into your savegame, and removing it simply lets the original bugs come back.
[*][b]It stands down instead of guessing.[/b] Every fix checks the game's code before it touches anything, and switches itself off if an official patch changes what it was written for.
[*]A few fixes are judgment calls rather than plain repairs. Those are marked on the fix list, with the reasoning.
[/list]

[h2]For modders[/h2]
The pack is built to share the game with your mod rather than take it over. It hooks the game's functions and calls the original where it can, so another mod that touches the same function keeps working. Where a bug sits in the middle of a function and cannot be hooked, the fix copies the corrected body instead — those are the ones most likely to clash, and each one names in its source the game file and lines it came from.

Any single fix can be switched off from another mod, without touching this one. Set the fix's id as a key on the veto table before the pack loads:
[code]SMRFixPack_Disabled = rawget(_G, "SMRFixPack_Disabled") or {}
SMRFixPack_Disabled["DustDevilSpawnGate"] = true[/code]
The id is the key, not a list entry — a plain list looks valid and switches off nothing. "Before the pack loads" means your mod has to load first.

[b]Source, and the reasoning behind every fix:[/b] [url=https://github.com/catt144/SMR-CommunityFixPack]github.com/catt144/SMR-CommunityFixPack[/url]
[url=https://mods.paradoxplaza.com/mods/156049/Any]Also on Paradox Mods[/url]
```

## Provenance of the headliners

⛔ **Not invented for the card.** Every bullet is a compressed form of an entry
already on the audited fix list (`SMR-CommunityMods` `content/fix-list.md`),
which is written in player voice and was terminal-audited before launch. The two
newest — the SpaceY description and the three untranslated strings — are the
`C50`/`C51` repairs the owner watched working on 2026-08-20.

⚠️ **Selection bias is deliberate and worth naming:** these are the loudest
consequences (crashes, freezes, deaths, permanent losses), not a representative
sample. The *"and a good deal more"* line exists so the card does not imply the
list is exhaustive, and the link is what makes the claim checkable.
