# Upload workflow — owner

Everything you do to put an update live, in order, and nothing else.

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

✅ **It has worked once** — at the v6 upload (2026-09-09) both pages filled
themselves in full with nothing pasted. Once is not a habit yet, so still do
step 3's check; the paste copies there stay current in case it does not.

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

Nothing to paste. **Tell the agent it worked** — that is the thing we are waiting
to find out. Go to step 4, unless you want the styling below.

### ❌ No — it is short, stale, or missing

The automatic fill did not work. Paste the matching block below by hand — these
are your backup copies, kept current every sweep, so you never have to leave this
page. **Paradox:** paste the plain block, then re-apply headings/bold with the
editor's formatting buttons (Paradox eats plain-text line breaks, so it will look
like a wall until you do). **Steam:** paste the BBCode block as-is — its tags
render.

> ⚠️ **These are BACKUP COPIES and must match two other places** — `metadata.lua`'s
> `description` (the auto-fill source) and `docs/agent/reports/STORE_CARD_LIVE.md`
> (the agent record). The public-surface sweep updates all three together; if the
> repair-count word here disagrees with the store page, tell the agent.

#### 📋 Paradox Mods — description (plain text, paste as-is)

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

#### 📋 Change note (both stores — Paradox CHANGELOG / Steam Change Notes)

Usually auto-fills. If it is missing under **CHANGELOG** (Paradox) or **Change
Notes** (Steam), paste this:

```
- New arrivals are no longer sent into a nearby dome that is switched off, quarantined or without life support when the working domes they can reach have no free homes. They go to the nearest working dome instead, even if some of them have to wait there for a home.
- The missing strike, pump, landing, drilling, shovel and bucket effects are back on seven machines and vehicles: the Rare Metals Extractor's hammer, the classic MOXIE, the Water Extractor, Shuttle Hub shuttles, the RC Driller, the RC Dozer and The Excavator. Sound and visuals only. The drill-style Rare Metals Extractor and the white MOXIE are silent by design; use Change Skin to switch the extractor to its hammer.
- Both were watched working in a running colony on game 1.1.0.
```

#### 📋 Short summary (only if it also came out blank)

```
Bug fixes for Surviving Mars: Relaunched — it repairs defects verified in the game's own code rather than rebalancing the game, and it is safe to add to a save you have already played.
```

Then **tell the agent it did not work**, and what the page showed instead.

### Optional either way: make it pretty

Even when the automatic fill works, the page comes out as plain text — correct,
but no headings or bold. The two blocks above are the styled versions; paste one
and apply the headings with the editor buttons.

⚠️ Cosmetic only, and **it does not survive the next upload.** Skip it whenever
you like; the page is still correct without it.

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

Four things, and then you are done:

1. The **version number each store shows**.
2. **Whether the descriptions filled themselves**, or you had to paste. This is
   the one we do not know yet.
3. Anything else that **looked wrong** on either page.
4. Whether the **site published**.

The agent writes the rest down.

---

## If something goes wrong

| what you see | what to do |
|---|---|
| The mod editor asks to save before uploading | Stop. Tell the agent. Something changed that should not have. |
| An upload is rejected | Stop. Tell the agent what it said, word for word. |
| The description came out short | Paste it by hand (step 3), then tell the agent it did not fill itself. |
| You uploaded Steam before Paradox | Not fixable, and not worth chasing. Say so, carry on. |
