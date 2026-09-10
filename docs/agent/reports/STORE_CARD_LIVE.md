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

Forty-eight repairs, each one written up on the fix list with what you would
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
however long the line was, a Comfort penalty billed for longer than the journey
actually took.

And three of them repair things you cannot see at all today: real defects that
the shipped numbers happen to hide, which another mod, a game patch or a DLC
could walk straight into.


SOME OF WHAT IT FIXES

· Colonists walked across the surface between domes and suffocated.
· Rocket loads of new arrivals died on their way to a dome.
· New arrivals moved into a dome that was switched off, quarantined or without air.
· A dome sat half empty and still refused to house anyone.
· A bed that fell vacant sat empty while colonists were homeless.
· Colonists stayed homeless after you built a Shuttle Hub.
· Night-shift colonists never came back to work after midnight.
· A salvaged farm kept supplying its dome with oxygen forever.
· Building an artificial lake buried the rover that built it.
· Drone Hubs paralysed themselves every time an Extender flickered.
· Salvaging one piece of track deleted the whole line, and its trains with it.
· Demolishing a station permanently deleted the trains parked there.
· Meteor-damaged track could not be salvaged at all.
· Two train buildings fought over the same connector hex forever.
· A destroyed tunnel still worked as a shortcut.
· Automatic rockets and landers took off with nothing aboard.
· A Jumbo Cave mystery could get stuck clearing waste rock and never complete.
· The Philosopher's Stone mystery hung one step from the end.
· A story step asked for a cave-in on a map that does not exist, and the story stopped.
· The Gene Forging research did nothing at all.
· The Domes Overview stopped marking domes in trouble.

… and a good deal more, including quieter repairs to drones, shuttles, domes,
rockets, research, storylines and the interface.

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


STILL PLAYING ON GAME VERSION 1.0.7?

This pack tracks the current version of the game. If you stayed on 1.0.7, there
is a separate frozen build for it, with instructions:
https://catt144.github.io/SMR-CommunityMods/legacy-1-0-7/


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
```

## ═══ STEAM WORKSHOP — BBCode; fall back to the plain block if tags render literally ═══

⚠️ Same words. Only try this after the plain version is safely in place.

```
Bug fixes for [i]Surviving Mars: Relaunched[/i].

[b]Forty-eight repairs[/b], each one written up on the fix list with what you would have seen and what was actually wrong. Every one targets something the game's own code gets wrong — the code says one thing, does another, and the fix makes it do what it says. It fixes bugs; it does not rebalance the game. Preferences and features are deliberately not in it.

Some of them you could hardly miss: an entire train line and every train on it deleted by salvaging a single hex, colonists suffocating on a walk between two domes, an artificial lake burying the rover that was building it.

More of them you would never have blamed on a bug, because the game looked perfectly normal while the arithmetic underneath it was wrong — a reward for freeing the wisps that paid about a thousandth of what its own message promised, a researched breakthrough the game restored to only one of the three wind turbine types it covers, a track refund that paid a stub's worth of Metals however long the line was, a Comfort penalty billed for longer than the journey actually took.

And [b]three[/b] of them repair things you cannot see at all today: real defects that the shipped numbers happen to hide, which another mod, a game patch or a DLC could walk straight into.

[h2]Some of what it fixes[/h2]
[list]
[*]Colonists walked across the surface between domes and suffocated.
[*]Rocket loads of new arrivals died on their way to a dome.
[*]New arrivals moved into a dome that was switched off, quarantined or without air.
[*]A dome sat half empty and still refused to house anyone.
[*]A bed that fell vacant sat empty while colonists were homeless.
[*]Colonists stayed homeless after you built a Shuttle Hub.
[*]Night-shift colonists never came back to work after midnight.
[*]A salvaged farm kept supplying its dome with oxygen forever.
[*]Building an artificial lake buried the rover that built it.
[*]Drone Hubs paralysed themselves every time an Extender flickered.
[*]Salvaging one piece of track deleted the whole line, and its trains with it.
[*]Demolishing a station permanently deleted the trains parked there.
[*]Meteor-damaged track could not be salvaged at all.
[*]Two train buildings fought over the same connector hex forever.
[*]A destroyed tunnel still worked as a shortcut.
[*]Automatic rockets and landers took off with nothing aboard.
[*]A Jumbo Cave mystery could get stuck clearing waste rock and never complete.
[*]The Philosopher's Stone mystery hung one step from the end.
[*]A story step asked for a cave-in on a map that does not exist, and the story stopped.
[*]The Gene Forging research did nothing at all.
[*]The Domes Overview stopped marking domes in trouble.
[/list]
… and a good deal more, including quieter repairs to drones, shuttles, domes, rockets, research, storylines and the interface.

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

[h2]Still playing on game version 1.0.7?[/h2]
This pack tracks the current version of the game. If you stayed on 1.0.7, there is a separate frozen build for it, with instructions: [url=https://catt144.github.io/SMR-CommunityMods/legacy-1-0-7/]Playing on 1.0.7[/url]

[h2]How it works[/h2]
[list]
[*][b]No game files are modified.[/b] The pack wraps the game's own code while it runs.
[*][b]Safe to add to a save you have already played.[/b] It writes almost nothing into your savegame, and removing it simply lets the original bugs come back.
[*][b]It stands down instead of guessing.[/b] Every fix checks the game's code before it touches anything, and switches itself off if an official patch changes what it was written for.
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
GitHub link, "Forty-eight repairs". ⚠️ It renders **bold**, which the plain `description`
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
