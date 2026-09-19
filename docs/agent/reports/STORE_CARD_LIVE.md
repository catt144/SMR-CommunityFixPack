# Store card — the LIVE page body, reworked 2026-08-20 on the owner's brief

## ⭐⭐ 2026-08-24 — THESE TWO BLOCKS ARE NOW OPTIONAL POLISH, NOT THE PAGE BODY

**Owner ruling, after the 1.0.x upload wiped the hand-pasted Paradox page.** Both
portals refill the page from `metadata.lua`'s `description` on *every* upload, so
a pasted body can never survive one — and the paste was never the whole job
either: **the headings and bold do NOT come across with the text** (owner,
measured — they were applied by hand with the editor's H/B buttons). So the old
arrangement cost a paste *plus* a full re-format, on both stores, every release.

⇒ **`metadata.lua`'s `description` now carries the card body itself.** The
automatic result is complete and correct rather than a 779-char summary. These
two blocks remain as the *styled* versions — re-apply them when you want the
formatting, never because the page is wrong.

⛔ **The shipped string is PORTAL-NEUTRAL and must stay that way.** Two passages
here are false on the other store and were rewritten out of it:
* *"This page has no comment section"* — true on Paradox, false on Steam.
* the trailing *"Also on the Steam Workshop"* cross-link — self-referential there.
⇒ **Never paste either block into `metadata.lua` verbatim.** The shipped body is
**5,342** chars as of 2026-09-09; ✅ **ACCEPTED by both portals at the v6 upload
(2026-09-09, owner-seen: both pages auto-filled with the full card, nothing
pasted — the first clean auto-fill in three cycles).** The §3 backups stay.
⛔ **The "5,124" this line carried until today was stale** — it predated the
F105/F108/F110 additions, and the body that actually shipped as v5 measured
**5,228**. So the upload path is known to accept at least 5,228; this rewrite is
+114 on that, not a leap past the 5,165 the web editor took.

---

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
  - **46** — entries on the fix list. ⭐ **RECOUNTED 2026-09-09 (hotfix 2, link 06):
    82 → 46**, after link 02 removed 36 entries whose fixes game 1.1.0 repairs
    itself (`SMR-CommunityMods` `7cef4f3`). Emitted, not typed:
    `grep -c '^??? ' content/fix-list.md`, and the section tally sums to the same
    (1+13+4+3+9+4+7+2+3). ⚠️ It is worded as *"forty-six repairs"*, not
    *"46 bugs"* — one entry covers two defects ("Two story-scripting defects…"),
    so entries is the honest unit. ⛔ The history: 79 → 80 (F105, 08-24) → 82
    (F108, F110) → 46. Never type it from this line either — recount.
  - **3** — the fix list's own audited section *"Under the hood: these three repair
    things you cannot see today."* ⛔ Not a classification invented for the card.
    ⭐ **WAS 4**; the battery/tank rate-modifier entry went with the 36, and the
    section's own prose still said "four" until link 06 corrected it.
  - **3** — judgment calls, down from six (Biorobots · colonists sheltering in
    vacuum · Edit Payload). The card states no number for these, which is why it
    never drifted; the site's `index.md` and `faq.md` did, in four places, and
    link 06 corrected all four.
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

## Links block — every link, and how each one was confirmed

| link | status |
|---|---|
| Paradox Mods page | ✅ **owner-supplied, pasted from their browser**: `https://mods.paradoxplaza.com/mods/156049/Any` |
| Steam Workshop page | ✅ **owner-verified 2026-08-20 — they opened it and it resolves**: `https://steamcommunity.com/sharedfiles/filedetails/?id=3787202810` *(it was written as the conventional form for item `3787202810` and held open as unverified until that click)* |
| Source code (fix pack) | ✅ confirmed from `git remote`: `https://github.com/catt144/SMR-CommunityFixPack` |
| The full fix list | ✅ **LIVE and verified 2026-08-20**: `https://catt144.github.io/SMR-CommunityMods/fix-list/` returns **HTTP 200**, and the live page carries both 08-20 fixes. The URL was derived from the Pages domain + the built path and then **checked rather than trusted** — it happened to be right |
| Issue tracker | ⚠️ `https://github.com/catt144/SMR-CommunityFixPack/issues` — already linked from the site's FAQ since 2026-08-13, ⛔ **but nobody in this project has recorded clicking it.** One click before this goes on two store pages |

✅ **Both store links are LIVE on the site** as of `SMR-CommunityMods` `c4e55c4`
(installing page buttons + landing page line), with the console route named —
Paradox Mods serves Xbox and PlayStation, which a console player cannot infer.

---

## ═══ PARADOX MODS — plain text, paste as-is ═══

⚠️ The cross-link at the foot points at STEAM. The Steam version below points
back at Paradox. ⛔ Do not paste the same block on both.

```
Bug fixes for Surviving Mars: Relaunched.

Fifty-five repairs, each one written up on the fix list with what you would
have seen and what was actually wrong. Every one targets something the game's
own code gets wrong — the code says one thing, does another, and the fix makes
it do what it says. It fixes bugs; it does not rebalance the game. Preferences
and features are deliberately not in it.

Some of them you could hardly miss: an entire train line and every train on it
deleted by salvaging a single hex, colonists suffocating on a walk between two
domes, an artificial lake burying the rover that was building it.

More of them you would never have blamed on a bug, because the game looked
perfectly normal while the arithmetic underneath it was wrong — a reward for
freeing the wisps that paid about a thousandth of what its own message promised,
a researched breakthrough the game restored to only one of the three wind
turbine types it covers, a track refund that paid a stub's worth of Metals
however long the line was, a train travel-time figure that counted the platform
wait twice.

And two of them repair things you cannot see at all today: real defects that
the shipped numbers happen to hide, which another mod, a game patch or a DLC
could walk straight into.


FEATURED: EXPEDITION CREWS COME HOME

Colonists living in habitats can join expeditions again, and they come back to
the habitat they left. If their habitat is too far from the landing site to
walk, they are set down at its door, the same way the rocket picked them up. If
the habitat is gone or unusable, they go to the nearest dome that is working and
has air.

One gotcha. If every dome is switched off and only habitats are alive, and those
habitats refuse the colonist through their filters, the colonist still walks to
the nearest dome and dies there. That is the game's own safety system choosing
where a homeless colonist goes, and this mod does not override it. Changing it
would mean rewriting how the game houses colonists, which is not what a bug-fix
mod should do.


SOME OF WHAT IT FIXES

· Colonists walked across the surface between domes and suffocated.
· Rocket loads of new arrivals died on their way to a dome.
· New arrivals moved into a dome that was switched off, quarantined or without air.
· A bed that fell vacant sat empty while colonists were homeless.
· Night-shift colonists never came back to work after midnight.
· A building clogged by a dust storm never started again.
· An Outside Ranch under Open Domes left food where drones could not reach it.
· Building an artificial lake buried the rover that built it.
· Salvaging one piece of track deleted the whole line, and its trains with it.
· Demolishing a station permanently deleted the trains parked there.
· Meteor-damaged track could not be salvaged at all.
· Automatic rockets and landers took off with nothing aboard.
· A Jumbo Cave mystery could get stuck clearing waste rock and never complete.
· The Philosopher's Stone mystery hung one step from the end.

The full list — every fix, what you would have seen, and what was actually
wrong — is here:
https://catt144.github.io/SMR-CommunityMods/fix-list/


SEVEN MACHINES THAT WORKED IN SILENCE

The Rare Metals Extractor's hammer, the MOXIE, the Water Extractor, Shuttle Hub
shuttles, the RC Driller, the RC Dozer and The Excavator all had sounds or
effects made for them that never played. They play now.

Two of them also have a skin that is silent by design, so if one of these stays
quiet, check its skin before you blame the fix:
· Rare Metals Extractor — the hammer strikes and puffs steam; the drill never
  strikes. NASA, SpaceY, BlueSun, Brazil, Roscosmos, Japan and ISRO colonies
  get the drill by default.
· MOXIE — the double-pump skin thumps and puffs; the blocky one is silent.

Select the building and press Change Skin (the paintbrush on its panel) to
switch. The screenshots on this page show which skin is which.


HOW IT WORKS

· No game files are modified. The pack wraps the game's own code while it runs.
· Safe to add to a save you have already played. It writes almost nothing into
  your savegame, and removing it simply lets the original bugs come back.
· Every fix checks the game's code before it touches anything, and stands down
  by itself if what it was written for has been renamed, removed or reshaped.
  A fix that stands down does nothing at all — it never guesses. Every game
  patch is read against the pack as well, and the fixes it changed are updated
  or retired.
· A few of the fixes are judgment calls rather than plain repairs. Those are
  marked as such on the fix list, with the reasoning, rather than folded in
  quietly.


FOUND A BUG, OR ONE THIS PACK DID NOT FIX?

Reports are read and acted on, and a save file where it reliably happens is
worth more than any description of it.

· Issue tracker — the route for everyone, and the only one that can carry a
  save file or a log:
  https://github.com/catt144/SMR-CommunityFixPack/issues
  It needs a free GitHub account and works from a browser on any device.

· On Steam you can also just use the comments on the mod's page.

This page has no comment section, so if you installed from Paradox Mods —
which includes every Xbox and PlayStation player — the tracker is the route.
On console there is nothing to attach in the first place, and a plain
description in your own words is genuinely useful.


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
    SMRFixPack_Disabled["LakeEntombment"] = true

The id is the key, not a list entry — a plain list looks valid and switches off
nothing. "Before the pack loads" means your mod has to load first.

Source, and the reasoning behind every fix:
https://github.com/catt144/SMR-CommunityFixPack

Also on the Steam Workshop:
https://steamcommunity.com/sharedfiles/filedetails/?id=3787202810


STILL PLAYING ON GAME VERSION 1.0.7?

This pack tracks the current version of the game. If you stayed on 1.0.7, there
is a separate frozen build for it, with instructions:
https://catt144.github.io/SMR-CommunityMods/legacy-1-0-7/
```

## ═══ STEAM WORKSHOP — BBCode; fall back to the plain block if tags render literally ═══

⚠️ Same words. Only try this after the plain version is safely in place.

```
Bug fixes for [i]Surviving Mars: Relaunched[/i].

[b]Fifty-five repairs[/b], each one written up on the fix list with what you would have seen and what was actually wrong. Every one targets something the game's own code gets wrong — the code says one thing, does another, and the fix makes it do what it says. It fixes bugs; it does not rebalance the game. Preferences and features are deliberately not in it.

Some of them you could hardly miss: an entire train line and every train on it deleted by salvaging a single hex, colonists suffocating on a walk between two domes, an artificial lake burying the rover that was building it.

More of them you would never have blamed on a bug, because the game looked perfectly normal while the arithmetic underneath it was wrong — a reward for freeing the wisps that paid about a thousandth of what its own message promised, a researched breakthrough the game restored to only one of the three wind turbine types it covers, a track refund that paid a stub's worth of Metals however long the line was, a train travel-time figure that counted the platform wait twice.

And [b]two[/b] of them repair things you cannot see at all today: real defects that the shipped numbers happen to hide, which another mod, a game patch or a DLC could walk straight into.

[h2]Featured: expedition crews come home[/h2]
Colonists living in habitats can join expeditions again, and they come back to the habitat they left. If their habitat is too far from the landing site to walk, they are set down at its door, the same way the rocket picked them up. If the habitat is gone or unusable, they go to the nearest dome that is working and has air.

[b]One gotcha.[/b] If every dome is switched off and only habitats are alive, and those habitats refuse the colonist through their filters, the colonist still walks to the nearest dome and dies there. That is the game's own safety system choosing where a homeless colonist goes, and this mod does not override it. Changing it would mean rewriting how the game houses colonists, which is not what a bug-fix mod should do.

[h2]Some of what it fixes[/h2]
[list]
[*]Colonists walked across the surface between domes and suffocated.
[*]Rocket loads of new arrivals died on their way to a dome.
[*]New arrivals moved into a dome that was switched off, quarantined or without air.
[*]A bed that fell vacant sat empty while colonists were homeless.
[*]Night-shift colonists never came back to work after midnight.
[*]A building clogged by a dust storm never started again.
[*]An Outside Ranch under Open Domes left food where drones could not reach it.
[*]Building an artificial lake buried the rover that built it.
[*]Salvaging one piece of track deleted the whole line, and its trains with it.
[*]Demolishing a station permanently deleted the trains parked there.
[*]Meteor-damaged track could not be salvaged at all.
[*]Automatic rockets and landers took off with nothing aboard.
[*]A Jumbo Cave mystery could get stuck clearing waste rock and never complete.
[*]The Philosopher's Stone mystery hung one step from the end.
[/list]

[b]The full list[/b] — every fix, what you would have seen, and what was actually wrong:
[url=https://catt144.github.io/SMR-CommunityMods/fix-list/]the complete fix list[/url]

[h2]Seven machines that worked in silence[/h2]
The Rare Metals Extractor's hammer, the MOXIE, the Water Extractor, Shuttle Hub shuttles, the RC Driller, the RC Dozer and The Excavator all had sounds or effects made for them that never played. They play now.

Two of them also have a skin that is [b]silent by design[/b], so if one of these stays quiet, check its skin before you blame the fix:
[list]
[*][b]Rare Metals Extractor[/b] — the hammer strikes and puffs steam; the drill never strikes. NASA, SpaceY, BlueSun, Brazil, Roscosmos, Japan and ISRO colonies get the drill by default.
[*][b]MOXIE[/b] — the double-pump skin thumps and puffs; the blocky one is silent.
[/list]
Select the building and press [b]Change Skin[/b] (the paintbrush on its panel) to switch. The screenshots on this page show which skin is which.

[h2]How it works[/h2]
[list]
[*][b]No game files are modified.[/b] The pack wraps the game's own code while it runs.
[*][b]Safe to add to a save you have already played.[/b] It writes almost nothing into your savegame, and removing it simply lets the original bugs come back.
[*][b]It stands down instead of guessing.[/b] Every fix checks the game's code before it touches anything, and switches itself off if what it was written for has been renamed, removed or reshaped. Every game patch is read against the pack as well, and the fixes it changed are updated or retired.
[*]A few fixes are judgment calls rather than plain repairs. Those are marked on the fix list, with the reasoning.
[/list]

[h2]Found a bug, or one this pack did not fix?[/h2]
Reports are read and acted on, and a save file where it reliably happens is worth more than any description of it.
[list]
[*][b]The comments below[/b] — easiest if you are on Steam, and no extra account needed.
[*][b]The issue tracker[/b] — [url=https://github.com/catt144/SMR-CommunityFixPack/issues]github.com/catt144/SMR-CommunityFixPack/issues[/url]. Comment sections cannot carry files, so this is the only place a save or a log can actually reach us. Free GitHub account, works from any browser.
[/list]

[h2]For modders[/h2]
The pack is built to share the game with your mod rather than take it over. It hooks the game's functions and calls the original where it can, so another mod that touches the same function keeps working. Where a bug sits in the middle of a function and cannot be hooked, the fix copies the corrected body instead — those are the ones most likely to clash, and each one names in its source the game file and lines it came from.

Any single fix can be switched off from another mod, without touching this one. Set the fix's id as a key on the veto table before the pack loads:
[code]SMRFixPack_Disabled = rawget(_G, "SMRFixPack_Disabled") or {}
SMRFixPack_Disabled["LakeEntombment"] = true[/code]
The id is the key, not a list entry — a plain list looks valid and switches off nothing. "Before the pack loads" means your mod has to load first.

[b]Source, and the reasoning behind every fix:[/b] [url=https://github.com/catt144/SMR-CommunityFixPack]github.com/catt144/SMR-CommunityFixPack[/url]
[url=https://mods.paradoxplaza.com/mods/156049/Any]Also on Paradox Mods[/url]

[h2]Still playing on game version 1.0.7?[/h2]
This pack tracks the current version of the game. If you stayed on 1.0.7, there is a separate frozen build for it, with instructions: [url=https://catt144.github.io/SMR-CommunityMods/legacy-1-0-7/]Playing on 1.0.7[/url]
```

## ⭐ 2026-08-24 — one headliner added, and why it qualifies

**"Researching a technology threw an error while a landscaping job was running"**
(F105). It clears the bar the rest of this list is held to — *player-facing and
recognisable* — on three counts the others mostly manage one of:

* **A player SAW it.** It is the only entry on either card that came from a field
  report against the live listings rather than from our own reading.
* **It is reproduced.** Four attended legs on 2026-08-24 — pack off, 14 and 12
  raises; pack on, zero (`F105`, section "THE FIELD ROUTE, REPRODUCED").
* **It answers the question a reader of this card is most likely to have**, which
  is whether installing the pack mid-game is safe. Leg D measured exactly that.

⛔ The count moved 79 → 80 with it. Re-derived, never typed:
`grep -c '^??? ' content/fix-list.md` in `C:\Dev\SMR-CommunityMods`.
⛔ These blocks are our RECORD of what gets pasted — the live pages do not change
until the owner pastes them at a sitting.

## ⭐ 2026-08-28 — one more headliner added (F108), and why it qualifies

**"The Extractor AI breakthrough held your staffed extractors at 50 Performance"**
(F108). It clears the bar on the same three counts as F105:

* **A player SAW it.** It came from a Steam Workshop comment on the live listing,
  not from our own reading.
* **It is reproduced.** Attended on 2026-08-28 — a staffed extractor held at ~120
  after the breakthrough instead of collapsing to 50, an unstaffed one read 50,
  and the sponsor's own "3 Extractors at 160 Performance" goal ticked to 3/3.
* **It answers a concrete, checkable question** — whether a breakthrough can brick
  a sponsor goal — and shows it no longer does.

⛔ The count moved 80 → 81 with it. Re-derived, never typed:
`grep -c '^??? ' content/fix-list.md` in `C:\Dev\SMR-CommunityMods`.

## ⭐ 2026-09-09 — hotfix 2's doc sweep (`100_DOCSWEEP`): the description did NOT move, the change note did

Re-verified by script (`verify_sync.py`, link 06's shape), not by eye:
`metadata.lua` `description` == `UPLOAD_WORKFLOW` §3 plain block, 0 differing
lines; the two BBCode blocks identical; this file's plain block +143 chars = the
two portal passages only; count word *Forty-six* in all five copies. Recounted:
`grep -c '^??? '` = **46**, "Under the hood" = **3**, judgment calls = **3**.

What moved, and it lives in `metadata.lua` `last_changes` + `UPLOAD_WORKFLOW` §3
only (this file carries no change note): bullet 2's Astrogeologist sentence now
says the leftover bonus **is removed on the next load** (ck126 KEEP, `bugs/F95.md`)
instead of "cannot take back"; bullet 4 gains the F117 line (ck127(a), `777249d`,
`bugs/F117.md`). ⛔ Both are CLAIMS until the sitting; bullet 5 says so.

## ⭐ 2026-09-10 — v7 words (`RELEASE.md` step 1): count 46 → 48, one headliner (C83)

Recounted, not typed: `grep -c '^??? '` = **48** in `SMR-CommunityMods`, tally
1+14+4+4+9+4+7+2+3; "Under the hood" still **3**, judgment calls still **3**.
Checked by script (the `verify_sync` shape, rewritten in the session scratchpad
because the original was never committed): `description` == UPLOAD_WORKFLOW
plain block; the two BBCode blocks identical; this file's plain block differs only
in the two portal passages; `last_changes` == the §3 change-note backup; count word
*Forty-eight* in all five copies. Description now **5,428** chars (+86 on the
5,342 both portals accepted at v6).

**New headliner — "New arrivals moved into a dome that was switched off,
quarantined or without air"** (C83), placed under the F53 arrivals bullet it is
easily confused with. It clears the F105/F108 bar: **a player saw it** (a Steam
discussion comment, 2026-09-10), **it is reproduced** (the owner's attended
layout, the arrivals split into the dead dome), and the fix was **watched** keeping
every arrival out of it for a sol. ⛔ It says "without air", not "suffocated":
the run saw the warning, not a death.
**C74+C77 stays in the "… and a good deal more" tail** — cosmetic, and the skin
caveat it needs (drill extractor and white MOXIE silent by design) does not fit
a one-line headliner. It carries that caveat on the fix list and in `last_changes`.

## ⭐ 2026-09-10 (later) — OWNER RULING: feature the silent machines + the two skins, with pictures

Supersedes the "stays in the tail" call directly above. The owner asked for the card
to **feature the sound fixes, explain the two extractors' skins, and point players at
pictures** of them. New section **"SEVEN MACHINES THAT WORKED IN SILENCE"** between the
fix-list link and the 1.0.7 section, in all five copies (plain ×3, BBCode ×2). Every
sentence traces to C74/C77 (tested-attended) or the owner's screenshots: the drill
never strikes, the blocky (CP3) MOXIE is silent, the sponsor list is C74's, "Change
Skin" is the paintbrush button (owner's screenshots show its tooltip). The owner's
"Water Extractor" image shows the **MOXIE** (owner confirmed) — the Water Extractor has
no silent skin (C77 fixed both). The "screenshots on this page" are REAL: three gallery
images now upload from `metadata.lua` `screenshot1..3` (`tools/store_screenshots.py`
builds them; `ignore_files` keeps them out of the pack — pack_predict 50 files, 3
IGNORED). Checked by script: `description` == UPLOAD plain; BBCode copies identical;
this file's plain block differs only in the portal passages; count word Forty-eight ×5.
⚠️ **Length now 6,206** (+778). Steam's cap is 8,000; **Paradox has accepted 5,342 and
its cap is not on record** — if the Paradox page comes out cut or the upload refuses the
text, the §3 paste backup is the route and the owner reports it (UPLOAD_WORKFLOW §2).

## ⭐ 2026-09-10 (night) — v7 LIVE: what arrived (the two first-time facts)

Read from the live Steam page HTML after the owner said both stores were live:
**Steam gallery: all three images arrived** (3 `highlight_strip_screenshot` items) — the
first use of `screenshot1..3`. **Steam body: WHOLE** — every section through the final
GitHub link, count word "Forty-eight". ⚠️ It renders **bold**, which the plain `description`
has none of ⇒ the §3 BBCode block was most likely pasted (owner to confirm; auto-fill
unknown this cycle). **Paradox: UNREAD** — the page is JavaScript-only from here (3,444 B
shell). Whether its gallery took the three images and whether the 6,206-char body arrived
whole are OWED from the owner (checklist receipt 2026-09-10); until then **5,342** stays the
largest Paradox-accepted length on record.
✅ **Owner, same night (verbatim):** "Everything seems to be correct, I had to use the copy and
paste ones to get the formatting right but thats ok I am used to the workflow now. Steam
doesn't show a v number". ⇒ Both pages carry the §3 paste blocks (pasted for FORMATTING, not
because auto-fill failed — auto-fill's own result was not observed this cycle). The Paradox
UPLOAD path accepted the 6,206-char `description` (the upload returned `pdx_version` "6"); what
the page shows is the pasted block. The owner's Steam screenshot shows all three gallery images.
Paradox's gallery was covered only by "everything seems to be correct", not itemised.

## ⭐ 2026-09-11 — release words for vNEXT (`RELEASE.md` step 1): count 48 → 50, one headliner (F119)

Recounted, not typed: `grep -c '^??? '` = **50** in `SMR-CommunityMods`, tally
1+14+4+5+9+5+7+2+3; "Under the hood" still **3**, judgment calls still **3**
(neither F119 nor C86 is one). Count word *Fifty* now in all five copies
(`metadata.lua`, this file's two blocks, `UPLOAD_WORKFLOW.md`'s two blocks).

**New headliner — "An Earth-sent Trade rocket, most often the Wildfire
mystery's cure rocket, could get stuck on the landing pad forever"** (F119),
added after the empty-launch rocket bullet it sits next to in the fix list.

It clears the F105/F108/C83 bar: **players saw it** (two independent Reddit
reports, r/SurvivingMars, PC + PS5, "Game-breaking bug for the Wildfire
mystery"), **it is reproduced** (the owner's attended A/B, `F119.md` §Attended
check — fix off reproduced the exact reported "20 fuel to unload"; a save/load
healed a pre-stuck rocket; fix on re-sized it at once), and it answers a
permanent-soft-lock question players can check for themselves. ⛔ No Beta
label — the owner cut it 2026-09-11 after the attended check (checklist 149).

**C86 (scan downgrade) stays in the "and a good deal more" tail** — P3, a
wasted deep scan and a misleading map reading, not a loss a player would
recognise as a headline the way F119's stuck rocket is. It is on the fix list
(`Buildings & economy`) and in `last_changes`.

### ⭐ 2026-09-11 later — count 50 → **49**: F60 RETIRED

`Fix_DomeFreeSpaceMismatch` was deleted from the pack the same day (owner ruling,
ck151 a / ck152 b, commit `9bc4360`), so the card's count drops by one. Count word
**Forty-nine** now in all five copies (`metadata.lua`, this file's two blocks,
`UPLOAD_WORKFLOW.md`'s two blocks) — they move together or the paste backups drift
from the live card.

⛔ **49 IS NOT TRUE UNTIL THE SITE ROW GOES.** `grep -c '^??? '` in
`SMR-CommunityMods/content/fix-list.md` still reads **50**; the F60 entry
(`:113-122`, "A dome read as full while its power was out") has NOT been removed
yet, and its "births and new arrivals refused … After the fix: they agree" body is
false on 1.1.0 regardless of the retirement (ck152 e). ⇒ **remove that entry before
the upload**, or the card will claim 49 while the fix list shows 50.

⚠️ Do not read the card count off the module count. They are different axes: 46
registered modules / 47 `Code/*.lua` against 49 repairs, because one module can
carry several fixes (`Fix_ArrivalDeaths` → F53/C83/F117, `Fix_SilentHitMomentFX` →
C74+C77) and `00_Core.lua` is not a fix. The card number is the **fix-list entry
count**, recounted with `grep -c '^??? '`, never derived from `Code/`.
✅ **Discharged 2026-09-11 (site `a061665`):** the F60 row is gone and `grep -c '^??? '`
reads **49** (tally 1+13+4+5+9+5+7+2+3); the F51 and F58 rows were narrowed in the same
commit. ⛔ UNDEPLOYED — the live site still serves `398a1b0` (50 entries) until the owner
publishes it with v9.

## ⭐ 2026-09-11 (night) — v8 LIVE as READ from Steam; v9 words (`RELEASE.md` step 1): F59 repair + F60 retirement

**v8 arrived without anyone recording it.** The Steam changelog's newest entry,
"Update: Sep 11 @ 1:50pm", carries the F119/C86 note verbatim; the live body carries the count word
**Fifty**; the workshop folder took a new `ModContent.fpk` (331,428 B) at
16:55 local; the tree carried the writeback (`version` 8, `pdx_version` "7"); the site
deployed `398a1b0` at 21:10Z. **Paradox: UNREAD** (JavaScript page). Whether either
page auto-filled or was pasted is OWED from the owner (checklist 155). ⇒ Until v9 is
uploaded the live pages correctly say **Fifty** and list the F60 row, while every copy
in this tree says **Forty-nine** — a known, deliberate gap, closed by the v9 upload.

**v9 words.** Count word **Forty-nine** verified ×5 by grep (`metadata.lua`, this file's
two blocks, `UPLOAD_WORKFLOW.md`'s two blocks) — set at `0392162`, unchanged here.
**No headliner moves:** F59's bullet ("A bed that fell vacant sat empty while colonists
were homeless") is still the accurate player sentence — the repair fixed OUR module's
side effect, not the description — and F60 never had a bullet ("A dome sat half empty
and still refused to house anyone" is F58's, `fix-list.md:105`). Judgment calls still
**3**. `last_changes` rewritten wholesale as v9's note (two bullets: the manual-assign
overfill repaired and watched on 1.1.0, the expedition half stated as code-verified
only; the F60 retirement and the count drop stated plainly). ⛔ The F59 line names the
defect as the pack's own — it was never a game bug and gets no fix-list row.

## ⚖️ 2026-09-12 — HOW IT WORKS bullet 3 REWORDED (owner ruling, checklist 112 = (a) / 133)

**The owner ruled "do the reword", reversing the 2026-09-09 deferral that had chosen instead to
repair the capability so the old sentence would become true.** The old bullet promised a fix
would stand down *"if an official patch changes what it was written for"*. `SMRFixPack.Require`
cannot do that: it is an existence-and-surface test, so it catches a target renamed, removed or
reshaped and cannot catch a patch that keeps the name and rewrites the body — **F115 was exactly
that shape**. The replacement is the pack's own honesty limit, already written in
`Code/00_Core.lua:620-625`.

**Shipped wording** (⛔ the second sentence is unchanged — it was true and stays verbatim):

> Every fix checks the game's code before it touches anything, and stands down by itself if what
> it was written for has been renamed, removed or reshaped. A fix that stands down does nothing
> at all — it never guesses. Every game patch is read against the pack as well, and the fixes it
> changed are updated or retired.

The third sentence is not a promise but a description of what has already happened twice: the
after-every-patch extraction diff (`WORKFLOW.md`) is what produced hotfix 2 (36 modules retired,
10 re-copied for 1.1.0) and v9 (F60 retired).

**Applied to all five copies in one commit, and they are byte-identical by script:** the shipped
`metadata.lua` description, the Paradox plain block and the Steam BBCode block in
`UPLOAD_WORKFLOW.md` §3, and both blocks here. The BBCode form keeps its bold lead-in
(*"It stands down instead of guessing."*) and takes the same clause change.

⚠️ **Length: 6,267 → 6,383 characters (+116).** Both portals accepted 6,267 at v9, and the web
editor has taken every increase so far; this is the largest single body to date. ⛔ Nothing was
uploaded — it ships with **v10**, and `version` was not touched (`editor/version rail (agent/prompts/perma/RELEASE.md § Release rails)`).

⭐ **No other surface needed changing, and this was checked rather than assumed.** `README.md`
and the site (`content/faq.md`, `content/for-modders.md` in `SMR-CommunityMods`) already said
"shape", and the FAQ already carries an explicit note about the body-rewrite case. The store card
was the last surface still carrying the old promise.

## ⭐ 2026-09-12 — v10 words (`RELEASE.md` step 1): count word UNCHANGED, headliners 21 → 20

The biggest single batch since hotfix 2, and the only one where **the count word does not move**.

**Count: Forty-nine → Forty-nine.** Three retirements (F37 ghost farm oxygen, F43 layout tech
lock, F31 cave-in on a missing map — all ruled, modules already deleted in `560343a`) and three
additions (C85 clogged-after-a-dust-storm, C88 Building Codes prefabs, C89 faction dome size).
⛔ **Re-derived, not carried:** `WORDING_RULED.md`'s arithmetic predicted **Forty-six** because it
priced the retirements alone, before the three v10 builds joined the same release. The number
comes from `grep -c '^??? ' content/fix-list.md` = **49**, section tally summing to 49.

**Headliners 21 → 20.** OFF: F37's *"A salvaged farm kept supplying its dome with oxygen forever."*
and F31's *"A story step asked for a cave-in on a map that does not exist, and the story stopped."*
REWORDED: F58's bullet to the ruled headline, *"Beds stayed reserved for colonists who were never
going to take them."* ON: **C85**, *"A building clogged by a dust storm never started again."* —
it clears §2's *recognisable* bar (two independent player reports, and the symptom is a building
visibly stuck with an on-screen reason). C88 and C89 stay in the *"… and a good deal more"* tail:
C88 is specific to one law, and C89 is a judgment call whose row belongs on the fix list.

**Intro paragraph, two ruled changes.** F21's example *"a Comfort penalty billed for longer than
the journey actually took"* → *"a train travel-time figure that counted the platform wait twice"*
(1.1.0 removed the Comfort charge; the travel-time figure is what the fix still corrects). And
*"three of them repair things you cannot see at all today"* → **two** — F43 leaves that set, which
now holds F57a and F29 only. The site's *Under the hood* intro moved with it.

**Judgment calls three → four** for C89, in all three `content/faq.md` places (`:24`, `:141`,
`:145-148`) plus the fix-list `??? question` marker. Derived: `grep -c '^??? .*judgment call\*"$'`
= **4**. The card's judgment-call sentence states no number, so it did not change.

**Applied to all five copies and verified by script, not by eye:** `metadata.lua`'s `description`
is byte-identical to `UPLOAD_WORKFLOW.md` §3's plain backup, and this file's BBCode block is
byte-identical to §3's BBCode backup; this file's plain block differs from the neutral body only
by the by-design Paradox cross-link paragraph and footer. Length 6,383 → **6,298 characters**
(two bullets out, one in). ⛔ Nothing uploaded; `version` untouched (`editor/version rail (agent/prompts/perma/RELEASE.md § Release rails)`).

**Twelve fix-list rows re-worded** from `reports/still-needed/WORDING_RULED.md` (items 1, 2, 3, 5,
6, 7, 8, 9, 10, 11, 12, 14; item 4 F52 held, item 13 F31 is the retirement). ⛔ Those are **not**
in `last_changes`: a wording correction is not a game repair (outbox, Held §Change note).

## ⭐ 2026-09-16 — v11 words (`release_prompt.md` §1): count 49 → 52, one headliner (C93)

**Count: Forty-nine → Fifty-two.** C93 (Outside Ranch under Open Domes), C95 (habitat residents
and automatic expedition drafts, judgment call) and C96 (rover subclasses on expeditions) land;
nothing retires. Derived from `SMR-CommunityMods` `content/fix-list.md`: `^??? ` rows = **52**,
section tally 2+15+4+6+9+6+6+2+2 = 52.

**Headliners 20 → 21.** ON: **C93**, *"An Outside Ranch under Open Domes left food where drones
could not reach it."* — two independent player reports and food visibly stranded, the bar C85
cleared. C96 has one report and stays in the tail; C95 is a judgment call whose row belongs on the
fix list, as C89 did.

**Judgment calls four → five** for C95: `content/faq.md` (three places), the fix-list
`??? question` marker (`^??? .*judgment call\*"$` = **5**), and `content/index.md`, which still
said **three** after v10 and now says five. The card's judgment-call sentence states no number.

## ⭐ 2026-09-17 — v12 words (`release_prompt.md` §1): count 52 → 53, headliners 21 → 14, a FEATURED section

**Count: Fifty-two → Fifty-three.** C102 (a returning crew whose home is gone) lands as a new row,
and C95's existing row turns from a judgment call into a plain repair; nothing retires. Derived
from `SMR-CommunityMods` `content/fix-list.md`: `^??? ` rows = **53**, section tally
2+16+4+6+9+6+6+2+2 = 53.

**⚖️ Headliners 21 → 14 — the owner's task, decided 2026-09-17**, not a count that drifted. Seven
bullets cut, each with its reason recorded in `RELEASE_OUTBOX.md`: the stale-reservation premise
narrowed on 1.1.0 by the module's own header; "paralysed" outran the Drone Hub symptom; the
destroyed tunnel needed a reload and nobody noticed it; Gene Forging was provable only by console
read; the connector-hex line was already covered by the two salvage lines; the Domes Overview tint
carries a known PT-09 regression; and the Trade rocket line the owner judged long and only alright.
⛔ The surviving 14 were verified true the same day — each has a module in `Code/` registered in
`metadata.lua`'s code list, none rests on a retired, parked or opt-in fix. Do not re-QA or reword
them.

**⚖️ A FEATURED section for C95**, above the headline list, from the owner's approved draft. The
gotcha paragraph ships as written: with every dome switched off and only filter-refusing habitats
alive, the colonist still walks to the nearest dome and dies there, and the card names that as the
game's own safety system rather than a gap in the pack. Owner: *"Explain that its a safety system
that we cannot over ride (I know we likely could but thats a massive rewrite and I am not)."*
[C106](../bugs/C106.md) is the filed, unfixed arrival-side sibling and is deliberately not on the card.

**⚖️ Two more cuts, same ruling.** The *"… and a good deal more"* tail sentence is GONE — the
heading already says "some", and the full list is linked. The 1.0.7 section MOVED to the very
bottom, after FOR MODDERS.

**Judgment calls five → four** as C95 leaves the class: `content/faq.md` (three places, including
the "in four of them the game's code is not wrong at all" sub-count, now **three** of four), the
fix-list `??? question` marker (`^??? .*judgment call` = **4**), and `content/index.md`. The card's
judgment-call sentence still states no number, which is why the store has never drifted on it.

**Length 6,376 → 6,551 chars** (+175; 6,431 → 6,597 UTF-8 bytes) — a small increment over a body
that demonstrably went through the upload path at v11, which is the only length data point worth
anything here. ⚠️ `tools/upload_preflight.py` prints **6,689 chars** for the same string and is not
contradicting this: its parser unescapes `\"` and `\\` but leaves each `\n` as two characters, so
it reads the literal, not the body. 6,695 escaped − 6 quote escapes = 6,689. Compare like with
like before quoting either number.

⚖️ **RULED 2026-09-17 — the divergence is deliberate, not rot.** This file's PARADOX plain block is
not byte-equal to `docs/UPLOAD_WORKFLOW.md`'s: it keeps a Paradox-specific FOUND A BUG section
("This page has no comment section…") and a trailing Steam Workshop link, where the workflow copy
and the shipped `metadata.lua` string are portal-neutral and agree byte for byte. The owner's
reason: *"users have no comment or discussion section on paradox, github is the only way they can
reach out to us."* The two BBCode blocks are byte-identical, and v12's edits were applied to each
block in place, so the divergence is exactly what it was.

⛔ **But the Paradox page does not show this block — it shows the NEUTRAL one.** `description`
auto-fills BOTH storefronts from `metadata.lua` (`ParadoxMods.lua:34`), and §3's paste backup is
the neutral plain block, used only when the auto-fill comes out blank. So the Paradox-specific
wording here has never been what a Paradox reader sees; it is a better rendering of that page,
not a record of it. ⚠️ Do not "sync" this block to the workflow copy on that basis, and do not
push its wording into `metadata.lua`: "This page has no comment section" would be flatly FALSE on
Steam, which is fed by the same string.

The neutral body is what covers both, and it already handles the owner's point without naming a
portal: the tracker is introduced as *"the route for everyone, and the only one that can carry a
save file or a log"*, and the comment clause is conditional — *"If this page has a comment section"*
— so on Paradox it simply resolves to nothing. ⚖️ Open, cheap, and NOT owed: giving Paradox the
direct sentence would mean the owner hand-pasting a Paradox-specific body at every upload, on top
of the styling pass. Left alone at v12 as not worth a per-release manual step.

## ⭐ 2026-09-17 (afternoon) — v12 LIVE: read back from Steam, not inferred from the tree

Owner's word was *"uploaded"*. Everything below is READ from the storefront on 2026-09-17, so it is
evidence rather than a handoff claim. Page `3787202810`, 111,423 bytes fetched.

- **Count word live: "Fifty-three repairs"** — 1 hit, and **0** hits for "Fifty-two".
- **Headline bullets live: 14**, counted as `<li>` elements between the *Some of what it fixes* and
  *Seven machines* headings. The cut is real on the page, not just in the tree: "Domes Overview
  stopped marking" returns **0**.
- **The FEATURED section is live** — "expedition crews come home" present.
- **The tail sentence is gone** — "a good deal more" returns **0**.
- **The 1.0.7 section is last** — its heading index sits after *For modders* (68,746 > 67,298).
- **Change note posted** as the newest entry, *"Update: Sep 17 @ 11:26am"*, carrying "One repair
  reworked, one added" and C102's "has not been watched in a real game yet".

⛔ **The train sentence is absent from the POSTED changelog too** ("comes home by train" returns 0 on
the changelog page). That independently confirms the edit happened in the Mod Editor box before the
upload, not afterwards in the tree, and that the storefront half of the outbox's disclosure ruling is
genuinely missing rather than merely uncommitted. See `metadata.lua`'s `last_changes` comment.

**Tree writeback:** `version` 14 → **16** (two saves), `pdx_version` "10" → **"11"**, `code_hash` and
`saved` rewritten. Comments stripped from both shipped files (389 and 52 lines) and restored from
`16445b6`, keeping every written-back value.

⚠️ **NOT verified, and not claimed:** the Paradox page version was not stated by the owner, and the
Paradox body was not read back. **The site is NOT published** — newest `publish-site.yml` run is #11
(2026-09-16, `74a336e`, which is v11's fix list), so the live card says Fifty-three while the
deployed fix list still shows 52 rows and still marks the habitat row a judgment call. Same gap as
the v11 close; it clears when the owner runs the workflow (`UPLOAD_WORKFLOW.md` §4).

## ⭐ 2026-09-18 — v13 words (`release_prompt.md` §1): count 53 → 54, headliners unchanged

**Count: Fifty-three → Fifty-four.** C107 (Dry Farming reaches the four Feeding the Future plant
farms) lands as a new row under *Buildings & economy*; nothing retires. Derived from
`SMR-CommunityMods` `content/fix-list.md`: `^??? ` rows = **54**, section tally
2+16+4+7+9+6+6+2+2 = 54. Body copies moved together: `Fifty-four repairs` = 1 (`metadata.lua`) +
2 (this file) + 2 (`UPLOAD_WORKFLOW.md` §3), and 0 body hits left for Fifty-three.

Headliners stay at the owner's 14; C107 is a P3 water figure, not a loud consequence. Judgment
calls stay at four: C107's Fungal/Insect exclusion follows the base game's own curation and is
written as a "Worth knowing" note, not as a judgment call.

## ⭐ 2026-09-18 (evening) — v13 LIVE: read back from Steam, not inferred from the tree

Owner's word was *"uploaded"*. Read from the storefront on 2026-09-18: page `3787202810`, 111,558
bytes fetched. **Count word live: "Fifty-four repairs"** — 1 hit, **0** for "Fifty-three". Change
note posted as the newest entry, *"Update: Sep 18 @ 5:35pm"*, carrying "Dry Farming on the Feeding
the Future farms", "checked in a running game" and "fifty-three to fifty-four" — the tree draft,
unedited this time.

**Tree writeback:** `version` 16 → **17**, `pdx_version` "11" → **"12"**, `code_hash` and `saved`
rewritten; comments restored from `94c19d3`.

**Paradox page shows v16** (owner, 2026-09-18), one below the tree's 17, as at v11.
⚠️ **NOT verified, and not claimed:** the Paradox body was not read back. **The site is NOT published** — newest `Publish docs site` run is #12 (`c5ac193`, v12's
fix list), so the live card says Fifty-four while the deployed fix list shows 53 rows.

## ⭐ 2026-09-19 — v14 words (`release_prompt.md` §1): count 54 → 55, headliners unchanged

**Count: Fifty-four → Fifty-five.** C108 (the Wildfire cure reaches infected colonists served from
home) lands as a new row at the top of *Story & mysteries*; nothing retires. Derived from
`SMR-CommunityMods` `content/fix-list.md` (`92c853f`): `grep -c '^??? '` = **55**, section tally
4+9+2+7+7+16+2+6+2 = 55. Body copies moved together: `Fifty-five repairs` = 1 (`metadata.lua`) +
2 (this file) + 2 (`UPLOAD_WORKFLOW.md` §3), and 0 body hits left for `Fifty-four repairs` in the
three files' body lines.

Headliners stay at the owner's 14: the Wildfire stall is a mystery that cannot end, worked around by
the reporter, not a loud consequence on the card's bar. Judgment calls stay at four. The change note
says plainly that the pack loads cleanly in game but the cure itself has not been watched (the owner
skipped that check on 2026-09-18), rather than "checked in a running game".

## Provenance of the headliners

⛔ **Not invented for the card.** Every bullet is a compressed form of an entry
already on the audited fix list (`SMR-CommunityMods` `content/fix-list.md`),
which is written in player voice and was terminal-audited before launch. The two
newest — the SpaceY description and the three untranslated strings — are the
`C50`/`C51` repairs the owner watched working on 2026-08-20.

⚠️ **Selection bias is deliberate and worth naming:** these are the loudest
consequences (crashes, freezes, deaths, permanent losses), not a representative
sample. The *"and a good deal more"* line used to carry that caveat; v12 cut it on
the owner's ruling, so the heading word *"some"* and the fix-list link are now the
only things keeping the card from implying the list is exhaustive.
