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

⚠️ **This is untested.** It was changed on 2026-08-24, after the last upload, so
no upload has ever actually used it. Step 3 tells you how to check and what to
paste if it did not work. Assume you may need to paste until it has worked once.

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

Eighty-one repairs, each one written up on the fix list with what you would
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
· The Extractor AI breakthrough capped your staffed extractors and could lock a sponsor's high-Performance extractor goal.
· You were never warned about running out of Food or maintenance resources.
· Independent Terraforming gave half the discount it advertises.
· Researching a technology threw an error while a landscaping job was running.
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
    SMRFixPack_Disabled["DustDevilSpawnGate"] = true

The id is the key, not a list entry — a plain list looks valid and switches off
nothing. "Before the pack loads" means your mod has to load first.

Source, and the reasoning behind every fix:
https://github.com/catt144/SMR-CommunityFixPack
```

#### 📋 Steam Workshop — description (BBCode, paste as-is)

```
Bug fixes for [i]Surviving Mars: Relaunched[/i].

[b]Eighty-one repairs[/b], each one written up on the fix list with what you would have seen and what was actually wrong. Every one targets something the game's own code gets wrong — the code says one thing, does another, and the fix makes it do what it says. It fixes bugs; it does not rebalance the game. Preferences and features are deliberately not in it.

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
[*]The Extractor AI breakthrough capped your staffed extractors and could lock a sponsor's high-Performance extractor goal.
[*]You were never warned about running out of Food or maintenance resources.
[*]Independent Terraforming gave half the discount it advertises.
[*]Researching a technology threw an error while a landscaping job was running.
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
SMRFixPack_Disabled["DustDevilSpawnGate"] = true[/code]
The id is the key, not a list entry — a plain list looks valid and switches off nothing. "Before the pack loads" means your mod has to load first.

[b]Source, and the reasoning behind every fix:[/b] [url=https://github.com/catt144/SMR-CommunityFixPack]github.com/catt144/SMR-CommunityFixPack[/url]
[url=https://mods.paradoxplaza.com/mods/156049/Any]Also on Paradox Mods[/url]
```

#### 📋 Change note (both stores — Paradox CHANGELOG / Steam Change Notes)

Usually auto-fills. If it is missing under **CHANGELOG** (Paradox) or **Change
Notes** (Steam), paste this:

```
- Fixed a base-game issue where the Extractor AI breakthrough held Metals and Rare Metals Extractors at 50 Performance even when they were fully staffed, which could make a sponsor goal that needs high-performance extractors impossible to finish. Staffed extractors now earn their full performance; unstaffed ones still run at 50.
- Fixed a base-game error when a technology that reduces building costs finished researching while a terrain-levelling or rock-clearing job was active anywhere on the map.
- Safe to install on a save where this is already happening; the levelling job can stay where it is.
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
