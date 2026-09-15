# Upload workflow — owner

## Must_Read_Header
<!-- RULES -->
Rule: Keep this file limited to the owner-facing upload procedure. [A3: pass]
Rule: Keep the backup page-copy blocks byte-matching `metadata.lua` descriptions and `docs/agent/reports/STORE_CARD_LIVE.md`. [A3: pass]
<!-- /RULES -->

**The order is: mod → store pages → site.** The store pages are what players
actually see; the site is a place people have to choose to visit.

---

## Before you start

Nothing. The agent does the words — fix list, change note, descriptions — and
tells you when it is ready. If nobody has said "ready to upload", ask.

---

## 1 · Pack

1. Main menu → **MOD EDITOR**.
2. It asks to restart the game. **Yes.** It reopens into the editor.
3. On the right, read the **Last changes** box. That text is the change note
   players will see on both stores. If it is wrong or still describes the last
   release, stop and say so.
4. **File → Pack Mod.**

⛔ Do not press the Save (floppy) button. It bumps the version for nothing.

---

## 2 · Upload

**Paradox Mods first. Steam second.** Always this order — doing it backwards
pushes the two stores' version numbers further apart, and that cannot be undone.

These are **meant** to upload by themselves, with nothing pasted:

- the page description
- the short summary
- the title and tags
- the change note
- **the three screenshots** (new in v7: the two Rare Metals Extractor skins and the
  MOXIE skins). On each page, check the gallery shows all three. If an upload refuses
  them, or the Paradox description comes out cut off (it is longer than any Paradox
  has taken before), tell the agent — the paste copies in step 3 still work.

✅ **They do fill themselves — that is settled** (owner, 2026-09-12, checklist 155):
the descriptions **always** auto-fill. What does **not** survive is the formatting,
so step 3 is a styling pass rather than a rescue, and the paste copies there stay
current for it. Not an open question any more — nobody needs to report the result.

**Two things that look wrong and are not:**

- The version number goes up. That is the upload doing its job.
- **The two stores show different version numbers.** They always have. It is how
  the two portals work, not a mistake. ⛔ Never re-upload to make them match —
  that bumps again and makes the gap bigger.

---

## 3 · Check the store pages — and paste if you need to

Open both pages and read the **description**.

**Does it start with "Bug fixes for Surviving Mars: Relaunched." and run all the
way down to the modder section?**

### ✅ Yes — the automatic fill worked

The normal case, every time. **Nothing to report** — the agent already knows this is
what happens (step 5). Nothing to paste either, unless you want the styling below,
which is the part the fill never carries. Go to step 4.

### ❌ No — it is short, stale, or missing

The automatic fill did not work. Paste the matching block below by hand — these
are your backup copies, kept current every sweep, so you never have to leave this
page. **Paradox:** paste the plain block, then re-apply headings/bold with the
editor's formatting buttons (Paradox eats plain-text line breaks, so it will look
like a wall until you do). **Steam:** paste the BBCode block as-is — its tags
render.

The public-surface sweep maintains the backup copy below alongside its two canonical peers.

#### 📋 Paradox Mods — description (plain text, paste as-is)

```
Bug fixes for Surviving Mars: Relaunched.

Forty-nine repairs, each one written up on the fix list with what you would
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


SOME OF WHAT IT FIXES

· Colonists walked across the surface between domes and suffocated.
· Rocket loads of new arrivals died on their way to a dome.
· New arrivals moved into a dome that was switched off, quarantined or without air.
· Beds stayed reserved for colonists who were never going to take them.
· A bed that fell vacant sat empty while colonists were homeless.
· Night-shift colonists never came back to work after midnight.
· A building clogged by a dust storm never started again.
· Building an artificial lake buried the rover that built it.
· Drone Hubs paralysed themselves every time an Extender flickered.
· Salvaging one piece of track deleted the whole line, and its trains with it.
· Demolishing a station permanently deleted the trains parked there.
· Meteor-damaged track could not be salvaged at all.
· Two train buildings fought over the same connector hex forever.
· A destroyed tunnel still worked as a shortcut.
· Automatic rockets and landers took off with nothing aboard.
· An Earth-sent Trade rocket, most often the Wildfire mystery's cure rocket, could get stuck on the landing pad forever.
· A Jumbo Cave mystery could get stuck clearing waste rock and never complete.
· The Philosopher's Stone mystery hung one step from the end.
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

· If this page has a comment section, that works too for anything you can
  describe in words. Only the tracker can carry a file.

On console — every Xbox and PlayStation player — there is nothing to attach in
the first place, and a plain description in your own words is genuinely useful.


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
```

#### 📋 Steam Workshop — description (BBCode, paste as-is)

```
Bug fixes for [i]Surviving Mars: Relaunched[/i].

[b]Forty-nine repairs[/b], each one written up on the fix list with what you would have seen and what was actually wrong. Every one targets something the game's own code gets wrong — the code says one thing, does another, and the fix makes it do what it says. It fixes bugs; it does not rebalance the game. Preferences and features are deliberately not in it.

Some of them you could hardly miss: an entire train line and every train on it deleted by salvaging a single hex, colonists suffocating on a walk between two domes, an artificial lake burying the rover that was building it.

More of them you would never have blamed on a bug, because the game looked perfectly normal while the arithmetic underneath it was wrong — a reward for freeing the wisps that paid about a thousandth of what its own message promised, a researched breakthrough the game restored to only one of the three wind turbine types it covers, a track refund that paid a stub's worth of Metals however long the line was, a train travel-time figure that counted the platform wait twice.

And [b]two[/b] of them repair things you cannot see at all today: real defects that the shipped numbers happen to hide, which another mod, a game patch or a DLC could walk straight into.

[h2]Some of what it fixes[/h2]
[list]
[*]Colonists walked across the surface between domes and suffocated.
[*]Rocket loads of new arrivals died on their way to a dome.
[*]New arrivals moved into a dome that was switched off, quarantined or without air.
[*]Beds stayed reserved for colonists who were never going to take them.
[*]A bed that fell vacant sat empty while colonists were homeless.
[*]Night-shift colonists never came back to work after midnight.
[*]A building clogged by a dust storm never started again.
[*]Building an artificial lake buried the rover that built it.
[*]Drone Hubs paralysed themselves every time an Extender flickered.
[*]Salvaging one piece of track deleted the whole line, and its trains with it.
[*]Demolishing a station permanently deleted the trains parked there.
[*]Meteor-damaged track could not be salvaged at all.
[*]Two train buildings fought over the same connector hex forever.
[*]A destroyed tunnel still worked as a shortcut.
[*]Automatic rockets and landers took off with nothing aboard.
[*]An Earth-sent Trade rocket, most often the Wildfire mystery's cure rocket, could get stuck on the landing pad forever.
[*]A Jumbo Cave mystery could get stuck clearing waste rock and never complete.
[*]The Philosopher's Stone mystery hung one step from the end.
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
```

#### 📋 Change note (both stores — Paradox CHANGELOG / Steam Change Notes)

Usually auto-fills. If it is missing under **CHANGELOG** (Paradox) or **Change
Notes** (Steam), paste this:

```
Housing and migration fixes, reviewed against the 1.1.0 patch:

- Freed housing notice - REPAIRED. Assigning a colonist to a residence that was already full could leave that home with more residents than it has beds, and fail to evict the colonist it displaced. That was this pack's own doing, not the game's. The notice now waits until the move that freed the bed has finished. Watched working in a running colony on 1.1.0. The same repair should also stop a colonist boarding an expedition from losing the home held for their return; that half is checked in the code only.
- Dome housing total - RETIRED. 1.1.0 changed how a dome decides whether it has room, and it no longer uses the total this fix corrected. Rather than leave it adjusting a number that no longer feeds the decision, the fix has been removed. The fix list drops from fifty to forty-nine.
```

#### 📋 Short summary (only if it also came out blank)

```
Bug fixes for Surviving Mars: Relaunched — it repairs defects verified in the game's own code rather than rebalancing the game, and it is safe to add to a save you have already played.
```

This one **is** worth reporting, because it is the exception: tell the agent the
description came out short, stale or missing, and what the page showed instead. That
is step 5's "anything that looked wrong", not the auto-fill question.

### Either way: the styling pass

The fill gives you plain text — correct, but no headings or bold, and **the formatting
never survives an upload** (owner, 2026-09-12). So this pass runs every time: paste the
matching styled block above and apply the headings with the editor buttons, on **both**
Steam and Paradox.

⚠️ Cosmetic, and the owner calls it minor — the auto-fill gives the page something
until the cleanup lands. Skip it whenever you like; the page is still correct without
it. ⛔ It is not optional for the **agent**, though: keeping those blocks current every
sweep is what makes the pass possible.

---

## 4 · Publish the site

The site does **not** update when the agent commits. It only updates when you
run this:

1. Go to **github.com/catt144/SMR-CommunityMods**
2. **Actions** tab
3. **Publish docs site** in the left-hand list
4. **Run workflow** → **Run workflow**

Give it a minute, then check the fix list page shows the new entry.

---

## 5 · Tell the agent

Three things, and then you are done:

1. The **version number the Paradox page shows** (Steam shows none — confirmed 2026-09-10).
2. Anything that **looked wrong** on either page.
3. Whether the **site published**.

The agent writes the rest down.

> ⛔ **Agents: two questions are ANSWERED — never ask them again.** The owner ruled
> this on **2026-09-12** (checklist 155) after being asked once too often:
>
> - **"Did the descriptions fill themselves?"** — **Yes. They always auto-fill.**
> - **"Did you have to paste?"** — **Yes, always, for the formatting.** The auto-fill
>   does not carry the styling, so the owner pastes the step-3 backups and does a
>   **cleanup pass on both Steam and Paradox**. It is minor: the auto-fill gives the
>   page something until the cleanup lands. **The method is satisfactory.**
>
> ⇒ Record that as the known state of every upload; do not open it as a question, and
> do not report a cycle as "auto-fill result unknown". ⛔ The step-3 paste backups stay
> **REQUIRED** and current every sweep — the owner's answer is *why*, not a reason to
> drop them.

---

## If something goes wrong

| what you see | what to do |
|---|---|
| The mod editor asks to save before uploading | Stop. Tell the agent. Something changed that should not have. |
| An upload is rejected | Stop. Tell the agent what it said, word for word. |
| The description came out short | Paste it by hand (step 3), then tell the agent — this is the exception, not the norm. |
| You uploaded Steam before Paradox | Not fixable, and not worth chasing. Say so, carry on. |

---

## FR-1 temporary workaround mod: store pages (copy-paste)

⭐ **LIVE since 2026-09-11:** Paradox Mods **158711**, Steam Workshop **3799500849** (public). The copy in your Mods
folder holds these numbers and is the master; the agent's source copy is synced from it. Any later update goes out from that folder.

**This is a separate mod, not the fix pack:** `SMR_FR1TempWorkaround`, "TEMPORARY - Linux NVIDIA 580 Crash Workaround".
It sits in your Windows Mods folder; its source copy is in `C:\Dev\SMR-FR1-TempMod-2026-09-11\`. Checklist item **145** has
the background.

> ✅ **P1 passed, and the page is ready as written** (you, 09-11). The packed mod works, including a cold boot straight into a
> colony, and it also ran with Reflections Low, High and Ultra. You don't need to pack again: the upload re-packs the folder itself,
> with the new text and picture.
> ✅ Reflections wording settled (you, 09-11): it loads with Reflections on, but that isn't properly tested and will very likely
> look glitchy, so keeping Reflections Off is a recommendation, not a requirement.

**Uploading it (different from the fix pack):**
- **Steam first is fine here, if Steam is the only store.** If you also do Paradox, do Paradox first, as usual.
- **Steps:** on the dev PC, main menu → **MOD EDITOR** (yes to the restart) → open **TEMPORARY - Linux NVIDIA 580 Crash
  Workaround** → press **Upload to Steam** on the editor's **top toolbar** (the Steam icon; it is not in the File menu). **No
  separate Pack step:** the upload packs the folder itself. If it asks "The mod needs to be saved before uploading. Continue?",
  answer **Yes**. Wait for "Mod … was successfully uploaded!". For Paradox, use **Upload to Paradox** (same toolbar), before Steam.
- **After the upload, open the new Steam item and check its visibility.** Whether a brand-new item starts public or hidden is
  decided inside Steam, and the agent can't read that code. If it's hidden, set it to Public on the item's page.
- Because this is a **new** mod, the first upload **saves
  it by itself** and creates the listing. That is expected this once (it is the fix pack's "stop, tell the agent" case only
  for the fix pack). Afterwards the copy in your Mods folder holds the listing number, so tell the agent: that copy becomes
  the master.
- The description, short summary, change note and preview picture are **meant to fill themselves**. They come from the
  mod's `metadata.lua`, which matches the blocks below. If a page comes out short, plain, or missing, paste the matching block.
  **Paradox:** paste the plain block, then re-apply the headings with the editor buttons. **Steam:** paste the BBCode block as-is.

#### 📋 Title

```
TEMPORARY - Linux NVIDIA 580 Crash Workaround
```

#### 📋 Short summary

```
TEMPORARY, Linux only: stops the NVIDIA driver 580 crash when you start a New Game or load a save in 1.1.0. Best with Reflections Off. Remove it once Paradox fixes the crash.
```

#### 📋 Paradox Mods — description (plain text, paste as-is)

```
TEMPORARY WORKAROUND. LINUX ONLY. Remove it as soon as Paradox fixes this crash.


WHO THIS IS FOR

You play Surviving Mars: Relaunched on Linux (through Steam's Proton) with an
NVIDIA graphics card on driver 580, and the game crashes to the desktop as soon
as you start a New Game or load a save.

If that is not you, you do not need this mod:
· Windows: this crash does not happen on Windows. Do not install it there.
· Steam Deck, AMD or Intel graphics: not affected. The mod switches itself off.
· NVIDIA driver 595: not affected (we tested it).


WHAT IT DOES

On driver 580, NVIDIA's shader compiler crashes while the game prepares its
screen-space reflection shaders, and the game prepares them even with
Reflections turned Off. This mod swaps those shaders for an empty stand-in, so
there is nothing left to crash on and the world loads.

The trade-off: the mod empties the shaders the game uses for screen-space
reflections. The game still loads and runs with Reflections on (we tried Low,
High and Ultra), but reflections have not been properly tested that way and will
very likely look wrong or glitchy. We recommend keeping Reflections Off.


HOW TO USE IT

1. Subscribe to this mod.
2. Start the game. On the main menu, open MOD MANAGER and enable
   "TEMPORARY - Linux NVIDIA 580 Crash Workaround".
3. Recommended: open Options, then Video, and set Reflections to Off.
4. Quit the game completely, then start it again.
5. Start a New Game or load your save.

That is all: no launch options and no files to edit. The mod does not change
your saves.


REMOVE IT WHEN PARADOX FIXES THE CRASH

This is a stopgap, not a fix, and Paradox is aware of the crash. As soon as a
game update fixes it:
1. Unsubscribe from this mod (or disable it in MOD MANAGER).
2. Restart the game.

After any game update the mod switches itself off anyway, because it only fits
game version 1.1.0.403908. Please still remove it then. Removing it is safe: it
writes nothing into your saves, and saves made with it do not need it.


WHAT WE TESTED IT ON

· Alienware m15 R4 laptop, NVIDIA GeForce RTX 3070 Laptop GPU
  (hybrid graphics, PRIME On-Demand)
· Linux Mint 22.2 (X11), kernel 7.0.0-31
· NVIDIA driver 580.173.02
· Steam Proton Hotfix (hotfix-20260828)
· Surviving Mars: Relaunched 1.1.0.403908, mostly with Reflections Off
  (it also loaded with Low, High and Ultra)

With the mod on, New Game and existing saves loaded and played normally. With
it off, the same laptop crashed on every world load.


IT MAY NOT WORK FOR EVERY SETUP

We could test only one machine. Other NVIDIA cards (especially the older GTX 900
and 1000 series), other 580 driver builds, other Linux distributions, Wayland,
or other Proton versions may behave differently. If it does not help, disable
it, restart the game, and tell us in the comments: your graphics card, driver
version, Linux distribution and Proton version.

This is an unofficial fan workaround, not made or supported by Paradox. Use it
at your own risk.

From the maintainer of the Relaunched Fix Pack. It is a separate mod; the fix
pack does not include it.
```

#### 📋 Steam Workshop — description (BBCode, paste as-is)

```
[h1]TEMPORARY WORKAROUND. LINUX ONLY.[/h1]
[b]Remove it as soon as Paradox fixes this crash.[/b]

[h2]Who this is for[/h2]
You play [i]Surviving Mars: Relaunched[/i] on [b]Linux[/b] (through Steam's Proton) with an [b]NVIDIA graphics card on driver 580[/b], and the game crashes to the desktop as soon as you start a New Game or load a save.

If that is not you, you do not need this mod:
[list]
[*][b]Windows:[/b] this crash does not happen on Windows. Do not install it there.
[*][b]Steam Deck, AMD or Intel graphics:[/b] not affected. The mod switches itself off.
[*][b]NVIDIA driver 595:[/b] not affected (we tested it).
[/list]

[h2]What it does[/h2]
On driver 580, NVIDIA's shader compiler crashes while the game prepares its screen-space reflection shaders, and the game prepares them even with Reflections turned Off. This mod swaps those shaders for an empty stand-in, so there is nothing left to crash on and the world loads.

[b]The trade-off:[/b] the mod empties the shaders the game uses for screen-space reflections. The game still loads and runs with Reflections on (we tried Low, High and Ultra), but reflections have not been properly tested that way and will very likely look wrong or glitchy. [b]We recommend keeping Reflections Off.[/b]

[h2]How to use it[/h2]
[olist]
[*]Subscribe to this mod.
[*]Start the game. On the main menu, open [b]MOD MANAGER[/b] and enable [b]TEMPORARY - Linux NVIDIA 580 Crash Workaround[/b].
[*][b]Recommended:[/b] open [b]Options → Video[/b] and set [b]Reflections[/b] to [b]Off[/b].
[*]Quit the game completely, then start it again.
[*]Start a New Game or load your save.
[/olist]
That is all: no launch options and no files to edit. The mod does not change your saves.

[h2]Remove it when Paradox fixes the crash[/h2]
This is a stopgap, not a fix, and Paradox is aware of the crash. As soon as a game update fixes it:
[olist]
[*][b]Unsubscribe[/b] from this mod (or disable it in MOD MANAGER).
[*]Restart the game.
[/olist]
After any game update the mod switches itself off anyway, because it only fits game version 1.1.0.403908. Please still remove it then. Removing it is safe: it writes nothing into your saves, and saves made with it do not need it.

[h2]What we tested it on[/h2]
[list]
[*]Alienware m15 R4 laptop, NVIDIA GeForce RTX 3070 Laptop GPU (hybrid graphics, PRIME On-Demand)
[*]Linux Mint 22.2 (X11), kernel 7.0.0-31
[*]NVIDIA driver 580.173.02
[*]Steam Proton Hotfix (hotfix-20260828)
[*]Surviving Mars: Relaunched 1.1.0.403908, mostly with Reflections Off (it also loaded with Low, High and Ultra)
[/list]
With the mod on, New Game and existing saves loaded and played normally. With it off, the same laptop crashed on every world load.

[h2]It may not work for every setup[/h2]
We could test only one machine. Other NVIDIA cards (especially the older GTX 900 and 1000 series), other 580 driver builds, other Linux distributions, Wayland, or other Proton versions may behave differently. If it does not help, disable it, restart the game, and [b]tell us in the comments[/b]: your graphics card, driver version, Linux distribution and Proton version.

[i]This is an unofficial fan workaround, not made or supported by Paradox. Use it at your own risk.[/i]

From the maintainer of the Relaunched Fix Pack. It is a separate mod; the fix pack does not include it.
```

#### 📋 Change note (both stores)

```
First release: a temporary workaround for the Linux + NVIDIA driver 580 crash on New Game or loading a save (game 1.1.0.403908).
```
