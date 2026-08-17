# Parked opt-in references — the restore record for the solo launch

**Created 2026-08-17 by `agent/prompts/SHIP_SOLO_PREP_fable.md`** (self-consumed;
grave `git show <sha>:docs/agent/prompts/SHIP_SOLO_PREP_fable.md`). Modelled on
`SHELVED_F85_DISTRESS_PAUSE.md`, and for the same reason: *"it's in git
history"* was explicitly rejected as an answer to "don't lose it".

**The owner's ruling, 2026-08-17:** the fix pack launches ALONE. The opt-in mod
is not ready and must not gate anything; every player-facing surface must
describe a product that stands completely on its own. The owner explicitly did
not want the opt-in text lost — hence this record. **Silence was chosen over
"coming soon"** (checklist 35 Q1 recommendation, applied as the reversible
default): a teaser is a promise with no date on a mod the owner judged not
ready, and it re-couples the two products. If the owner overrides, the teaser
goes in ONE place (the site FAQ), never the store card or `metadata.lua`.

⭐ **Nothing here was ever seen by a player.** This is a first release; the
opt-in behaviours were never in a shipped pack. Removing a reference loses
nothing and creates no gap — verified: no store page exists, Pages is OFF,
and no version of either mod has ever been uploaded.

---

## ⭐ THE RESTORE TRIGGER, in one sentence

**The opt-in mod publishes.**

## Restore checklist — mechanical, surface by surface

Do these in order; each step names its passage(s) below by id. After all steps:
re-measure every count the restores move (④ sheet §2/§3, the 12 metadata
string counts), re-prove STORE↔RELEASE VERBATIM for the fix pack, run
`python tools/doccheck.py` and `python -m mkdocs build --strict` in the site
repo, and bump the fix pack's version if `metadata.lua` strings change after
upload (they cannot change without a re-upload).

1. **Site `content/index.md`** — restore P1 (two-mod intro), P2 (dial caveat),
   P3 (preferences clause), P4 ("Do I need both?"), P5 (heading back to
   "three things"), P6 ("Which one is which" tab group), P7 (footer note).
2. **Site `content/install.md`** — restore P8 (no-links note), P9 ("Both mods
   wrap"), P10 (optional-mod save paragraph), P11 ("The optional modules"
   section + Apply admonition), P12 (no-options admonition original), P13
   (console line).
3. **Site `content/faq.md`** — restore P14–P27b in place (whole questions
   among them: toggles-reset, "Do I need both mods?", Retirement-Dome hotel,
   classic rockets, second sun — P19, P20, P25, P26, P27).
4. **Site `content/fix-list.md`** — restore P28 (boundary paragraph).
5. **Site `content/for-modders.md`** — restore P29–P35.
6. **Site `mkdocs.yml` + `README.md`** — restore P35b (site_description),
   P36 (upload note), P37 (table row).
7. **Fix pack `metadata.lua`** — restore P38 (`description`) and P39
   (`last_changes`) ⛔ **only with a version bump and re-upload**; on a
   restore, `last_changes` should instead describe the actual change ("the
   opt-in mod is now available…"), so P39 is context, not paste material.
8. **Store card** — restore P40a–P40d into BOTH
   `RELEASE_DESCRIPTION_FIXPACK.md` and `STORE_FIXPACK.md` (identical player
   text, then diff-prove VERBATIM). Un-park FILL-IN 2 (marker line P40c goes
   back into the card only) and the front-matter row/notes marked
   *parked 2026-08-17*.
9. **④ sheet `RELEASE_PORTAL_PREP.md`** — reverse every *PARKED 2026-08-17*
   marker: two-mod upload order, opt-in paste row, marker count, body-size
   row, metadata columns, packaging row, §7 row.
10. **`RELEASE_DESCRIPTION_OPTIN.md`** — remove its parked banner; it is the
    paste source for the opt-in upload, body already audited.
11. Editing done → re-measure, re-prove, doccheck + `mkdocs --strict`, and
    update checklist item 35 + `STATE.md`.

## Already-proven at parking time (2026-08-17)

| claim | proof |
|---|---|
| every passage below matched its source file byte-for-byte before deletion | `tools`-free check: python script compared each `VERBATIM src=` block against the pre-edit working tree (identical to `HEAD`, tree was clean); all blocks PASS — see the parking commit message |
| the fix pack stands alone in CODE | grep of `Code/` for `OptIn|SMROptInPack|CommunityOptInPack`: one hit, a comment in `00_Core.lua:457` describing the pack's own dormant option vocabulary; no runtime read of any opt-in global; `items.lua` carries no Mod Options (comments only) |
| no player-facing string still promises opt-in behaviour | post-edit grep across `metadata.lua` strings, both card player-text blocks, all five site pages: zero hits outside Lua comments and agent notes |
| STORE↔RELEASE VERBATIM re-proven after the edits | diff of the two `═══ PLAYER TEXT ═══` blocks, recorded on the ④ sheet |
| counts re-measured, not inherited | ④ sheet §2/§3 cells re-measured post-edit (same method as the 2026-08-16 checkup); `--emit-counts` unchanged (75 modules / 76 files / 96 probes — no code moved) |
| `mkdocs build --strict` GREEN after the site edits | run in `C:\Dev\SMR-CommunityMods` at parking time |

⛔ **What this parking did NOT change:** no `Code/` file, no probe, no counts
emitted by doccheck, no bug entry, no fact. Agent-facing records (bugs, facts,
WORKFLOW, STATE, FIX_POLICY, archived reports) keep their opt-in references on
purpose — they are engineering history, not player surfaces.

---

# The passages, VERBATIM

Each block is the exact pre-edit text. `src=` names the file it came from;
"now reads" states the replacement so the surrounding context is re-findable
even if the page drifts. Blocks were byte-compared against the pre-edit files
before the deletions were made.

## Site — `C:\Dev\SMR-CommunityMods`

### P1 · `content/index.md` — the two-mod intro (page opening, after the H1)

Now reads: *"The **Community Fix Pack** repairs defects in the game's own code
rather than rebalancing the game, and it is built to be added to a save you
have already played."* (one mod, one sentence).

<!-- VERBATIM src="content/index.md" -->
````text
Two mods, and they are deliberately different things.

The **Community Fix Pack** repairs defects in the game's own code rather than
rebalancing the game, and it is built to be added to a save you have already
played. The **Opt-In Modules** mod is the other side of that line: optional
changes to designed behaviour, every one of them off, or sitting at the game's
own setting, until you switch it on.
````

### P2 · `content/index.md` — the drone-dial caveat under "Is it safe…"

Now reads: *"It is built to be safe to add or remove at any time."*

<!-- VERBATIM src="content/index.md" -->
````text
It is built to be safe to add or remove at any time. There is one caveat, and it
belongs to the *optional* mod's drone dials: [read it before you
uninstall](faq.md#how-do-i-get-it-out).
````

### P3 · `content/index.md` — the preferences clause under "Does it change how the game is balanced?"

Now reads: *"Preferences and features are not in the fix pack."*

<!-- VERBATIM src="content/index.md" -->
````text
Preferences and features are not in the fix pack. They live in the optional mod,
which you do not need.
````

### P4 · `content/index.md` — the whole "Do I need both?" question

Removed whole (nothing replaces it).

<!-- VERBATIM src="content/index.md" -->
````text
### Do I need both?

**No.** Each works on its own, and they work together. If you only want your bugs
fixed, install the fix pack and stop there.
````

### P5 · `content/index.md` — the section heading (count changed 3 → 2)

Now reads: `## The two things people ask before installing`.

<!-- VERBATIM src="content/index.md" -->
````text
## The three things people ask before installing
````

### P6 · `content/index.md` — the whole "Which one is which" tab group

Now reads: a plain `## What is in it` prose section carrying the fix-pack tab's
content minus *"This is the one most people want."* (a comparison with nothing
to compare to). The opt-in tab is fully parked.

<!-- VERBATIM src="content/index.md" -->
````text
## Which one is which

=== "Community Fix Pack"

    Bug fixes only. Nothing to configure, nothing to switch on — it works the
    moment it loads. This is the one most people want.

    Its repairs cover disasters and weather, colonists and domes, drones and
    logistics, buildings and economy, trains, rockets and asteroids, story
    sequences, and the numbers on your screen. Several of them also repair damage
    already sitting in your save when you load it.

    [Every fix in it →](fix-list.md)

=== "Community Fix Pack: Opt-In Modules"

    Eight optional modules — things the developers deliberately decided against,
    or that we merely disagree with. Seven ship switched off; the two drone dials
    ship at the game's own values, where they do exactly nothing. (One of the
    eight also carries a real repair, because lifting a limit the game set walks
    you straight into a defect the game never had to handle.)

    You turn on what you want in *Options → Mod Options*, on any platform,
    controller included. Install it only if you want something from its list.
````

### P7 · `content/index.md` — the footer note (plural → singular)

Now reads: *"The mod is not on a store as this page is written, so there is no
store link on it. When there is, it goes on the [installing page](install.md)."*

<!-- VERBATIM src="content/index.md" -->
````text
!!! note "Nothing here is published yet"
    Neither mod is on a store as this page is written, so there are no store
    links on it. When there are, they go on the [installing page](install.md).
````

### P8 · `content/install.md` — the no-store-links note (plural → singular)

Now reads: *"The mod has not been published yet, so there is nothing to link
to. This page gets the link when it exists."*

<!-- VERBATIM src="content/install.md" -->
````text
!!! note "No store links yet"
    Neither mod has been published, so there is nothing to link to. This page
    gets the links when they exist.
````

### P9 · `content/install.md` — "Both mods wrap" (plural → singular)

Now reads: *"Nothing is patched on disk. The mod wraps the game's own code
while it runs, and no game file is modified."*

<!-- VERBATIM src="content/install.md" -->
````text
Nothing is patched on disk. Both mods wrap the game's own code while it runs, and
no game file is modified.
````

### P10 · `content/install.md` — the optional mod's save-data paragraph

Removed whole (the fix pack's own list above it is untouched).

<!-- VERBATIM src="content/install.md" -->
````text
The optional mod stores four things: a "you have seen this warning" mark on a
building, a "closed to new residents" flag on a dome, a "move jobseekers out" flag
on a dome, and — only if you move a drone dial off its base setting — an ordinary
bonus of the kind the game hands out itself. The first three mean nothing to the
unmodded game. **The fourth is the one caveat worth thirty seconds of your time**
and it is written out in the [FAQ](faq.md#how-do-i-get-it-out).
````

### P11 · `content/install.md` — the whole "The optional modules" section

Removed whole, including the Apply-vs-restart admonition (which contrasts the
optional page's Apply with the Mod Manager restart — no optional page, no
contrast).

<!-- VERBATIM src="content/install.md" -->
````text
## The optional modules

Seven of the optional mod's eight modules ship switched off. The eighth is a pair
of drone dials, which ship at the game's own values, where they do nothing at all
until you move them. Everything lives in **Options → Mod Options → Community Fix
Pack: Opt-In Modules**, reachable from the main menu or in game, and it works with
a controller.

**Changes take effect as soon as you press Apply, in both directions — no restart
needed.** That goes for the switches and for the dials alike: nothing you choose
on that page does anything until Apply, so a player who sets a dial and backs out
of Options has changed nothing.

!!! warning "That is a different question from the one above"
    Turning a **module** on or off is immediate. Turning the **mod itself** on or
    off in the Mod Manager needs a full game restart.
````

### P12 · `content/install.md` — the no-options admonition (split story dropped)

Now reads the same admonition with its first sentence replaced by *"There is
nothing to configure, so you will not find it in Mod Options — nothing is
missing, and nothing is broken."*

<!-- VERBATIM src="content/install.md" -->
````text
!!! note "The fix pack has no options page, and that is correct"
    Every setting moved to the optional mod when the two were split. If you have
    only the fix pack installed you will not find it in Mod Options — nothing is
    missing, and nothing is broken. There is no way to switch off an individual
    *fix* from inside the game; see [For modders](for-modders.md) for the one
    route that exists.
````

### P13 · `content/install.md` — the console-players line about the optional mod

Removed whole (the achievements paragraph above it stands alone).

<!-- VERBATIM src="content/install.md" -->
````text
The optional mod's switches work on every platform, controller included.
````

### P14 · `content/faq.md` — the "anything from the optional modules" bullet

Removed whole from the "things we do on purpose" list.

<!-- VERBATIM src="content/faq.md" -->
````text
- **Anything from the optional modules**, if you installed that second mod. Those
  are changes to designed behaviour, and each one can be undone where you turned
  it on: *Options → Mod Options*. Seven are switches; the eighth is the pair of
  drone dials, which you undo by putting them back to their base settings.
````

### P15 · `content/faq.md` — the drone-dial uninstall warning

Removed whole from "How do I get it out?". ⛔ On restore this is the
single most consequential passage in this file — it is the one that saves a
player's save.

<!-- VERBATIM src="content/faq.md" -->
````text
!!! warning "If you used the optional pack's drone dials, do this first"
    A drone dial left off its base setting is stored in your savegame as an
    ordinary bonus, and it keeps boosting your drones after the mod is gone —
    permanently, with nothing left in the game to say where it came from.

    **With your colony loaded**, set both dials back to base, press Apply, then
    save the game — and then uninstall. Setting them to base clears the boost
    from the colony you are playing; saving is what clears it from the file. Done
    from the main menu it clears nothing, because there is no colony to clear.
````

### P16 · `content/faq.md` — "every setting lives in the optional mod" clause

Now reads: *"…on any platform. The fix pack has no options page at all, and the
developer console cannot un-apply a fix, because…"* (clause dropped, rest
untouched).

<!-- VERBATIM src="content/faq.md" -->
````text
**You cannot switch off one individual fix from inside the game**, on any
platform. The fix pack has no options page at all — every setting lives in the
optional mod — and the developer console cannot un-apply a fix, because the fixes
are installed long before the game reaches a point where you could type anything.
````

### P17 · `content/faq.md` — "one tracker covers both mods"

Now reads: *"It needs a free GitHub account."* (sentence ends there).

<!-- VERBATIM src="content/faq.md" -->
````text
  It needs a free GitHub account. One tracker covers both mods — say which one
  you were running and we will sort it out from there.
````

### P18 · `content/faq.md` — "Can I remove it later?" dial-caveat tail

Now reads: *"Yes — see [How do I get it out?](#how-do-i-get-it-out) above."*

<!-- VERBATIM src="content/faq.md" -->
````text
Yes — see [How do I get it out?](#how-do-i-get-it-out) above, including the one
drone-dial caveat if you use the optional pack.
````

### P19 · `content/faq.md` — the whole "Do I need both mods?" question

Removed whole.

<!-- VERBATIM src="content/faq.md" -->
````text
### Do I need both mods?

No. The **Community Fix Pack** is bug fixes and works entirely on its own. The
**Community Fix Pack: Opt-In Modules** is a separate mod of optional changes,
also standing on its own. Neither needs the other, and they work together.

If you only want your bugs fixed, install the fix pack and stop there.
````

### P20 · `content/faq.md` — the whole "Why did my toggles and dials reset?" question

Removed whole. ℹ️ It answered a question only a pre-split tester could ask; no
player ever had the combined mod. On restore, reconsider whether it belongs at
all — the opt-in mod publishing fresh gives new players no toggles to lose.

<!-- VERBATIM src="content/faq.md" -->
````text
### Why did my toggles and dials reset?

Because the optional modules moved into their own mod. A new mod is a new set of
options as far as the game is concerned, so previous settings do not carry over.
One visit to *Options → Mod Options* sets them again, and they stay set. Your
savegames are not affected — this is only the mod's own settings.
````

### P21 · `content/faq.md` — balance answer, the optional-mod clause

Now reads: *"Preferences and features are not in it."*

<!-- VERBATIM src="content/faq.md" -->
````text
Preferences and features are not in it; they live in the optional mod,
which you do not need.
````

### P22 · `content/faq.md` — "the optional pack is the opposite" paragraph

Removed whole from "How do I turn one fix off?".

<!-- VERBATIM src="content/faq.md" -->
````text
The optional pack is the opposite: everything in it is reachable in *Options →
Mod Options*, on every platform, controller included — seven switches and a pair
of dials.
````

### P23 · `content/faq.md` — console-players second bullet

Now reads: *"**Switching off an individual *fix*** takes a second mod written
for the purpose, so it is a thing a modder does rather than something you can
do from inside the game, on any platform, console or PC."*

<!-- VERBATIM src="content/faq.md" -->
````text
- **The optional mod's settings work everywhere**, from the main menu or in
  game, with a controller. Switching off an individual *fix* is a different
  matter: it takes a second mod written for the purpose, so it is a thing a
  modder does rather than something you can do on any platform, console or PC.
````

### P24 · `content/faq.md` — the Acknowledged-warnings remedy paragraph

Removed whole; the "Building Not Working" answer now ends at *"arguably the
opposite of what you want."* — the question it answers ("why does it come
back") is fully answered without the remedy pointer.

<!-- VERBATIM src="content/faq.md" -->
````text
The annoyance is real, so the **optional** mod carries a module for it:
*Acknowledged warnings* changes dismissal to mean "I have seen these particular
buildings". The ones you dismissed stay quiet until they actually recover, if one
later breaks again you are told, and a newly broken building always warns
immediately. It is off until you turn it on.
````

### P25 · `content/faq.md` — the whole Retirement-Dome hotel question

Removed whole — its answer turns on the optional Nursery/Retirement Dome
policy, which a fix-pack-only player cannot have.

<!-- VERBATIM src="content/faq.md" -->
````text
### My Retirement Dome's hotel is filling up with jobseekers

Leave the Hotel on **"Tourists Only"**. Switched to "Any Colonist" a Hotel stops
being tourist housing and becomes ordinary housing — so an arriving jobseeker
gets a *room*, which means they are not homeless, which means the optional
Nursery / Retirement Dome policy will not move them out. That policy moves
unemployed colonists who have no home in that dome — anyone working there stays,
and a hotel room counts as a home.
````

### P26 · `content/faq.md` — the whole classic-rocket-refuelling question

Removed whole — it documents an opt-in module (D01).

<!-- VERBATIM src="content/faq.md" -->
````text
### I switched on classic rocket refuelling and my parked rocket did nothing

That is deliberate. A rocket that is *already* sitting parked when you enable the
module picks the behaviour up the next time it lands; rockets that land after you
enable it fill immediately. The alternative was reaching into rockets mid-flight
cycle, and we would rather leave a working system alone. If it bothers you, land
the rocket once.
````

### P27 · `content/faq.md` — the whole second-Artificial-Sun question

Removed whole — it documents an opt-in module (D04).

<!-- VERBATIM src="content/faq.md" -->
````text
### I put up a second Artificial Sun and my old solar panels ignore it

Panels that were already standing keep ignoring a second sun until you save and
load. Panels built after you switch the module on bind straight away, and a
reload snaps the older ones into place.
````

### P27b · `content/faq.md` — "Why isn't X fixed?", the destination clause

Now reads: *"**It is not a defect, it is a design we disagree with.** Those are
not bug fixes, and they do not ship in the pack."* ⚠️ Found by the A4
end-to-end re-read, NOT by the survey grep — "optional mod" matches no
`opt-in`-shaped pattern. A restore sweep must grep for `optional` too.

<!-- VERBATIM src="content/faq.md" -->
````text
- **It is not a defect, it is a design we disagree with.** Those go in the
  optional mod, off by default, or nowhere.
````

### P28 · `content/fix-list.md` — the boundary paragraph in "What is not on this page"

Now reads: *"**Things we merely disagree with.** Preferences, quality-of-life
changes and behaviour the game clearly intends are not bug fixes, and they are
not in the pack."* — the boundary is still explained; only the destination mod
is unnamed.

<!-- VERBATIM src="content/fix-list.md" -->
````text
**Things we merely disagree with.** Preferences, quality-of-life changes and
behaviour the game clearly intends live in a separate mod, *Community Fix Pack:
Opt-In Modules*, which you do not need to install. Seven of its eight modules
ship switched off; the eighth is a pair of drone dials that sit at the game's own
values, where they do nothing at all until you move them.
````

### P29 · `content/for-modders.md` — "either mod" (plural → singular)

Now reads: *"…nothing here is needed to use the mod."*

<!-- VERBATIM src="content/for-modders.md" -->
````text
This page is for people writing or debugging mods. If you are playing the game,
you want the [FAQ](faq.md) instead — nothing here is needed to use either mod.
````

### P30 · `content/for-modders.md` — section head + "Both mods patch"

Now reads: `## What this mod does to the game` / *"Nothing on disk. The mod
patches the game's code **at runtime** — wrapping, chaining…"*

<!-- VERBATIM src="content/for-modders.md" -->
````text
## What these mods do to the game

Nothing on disk. Both mods patch the game's code **at runtime** — wrapping,
chaining and, where there is no alternative, replacing individual functions while
the game runs. No game file is modified and no asset is overwritten.
````

### P31 · `content/for-modders.md` — the opt-in veto example

Removed whole (the fix pack's own example above it is untouched).

<!-- VERBATIM src="content/for-modders.md" -->
````text
The optional-modules mod has the same mechanism under its own name:

```lua
SMROptInPack_Disabled = SMROptInPack_Disabled or {}
SMROptInPack_Disabled["NoHomeless"] = true
```
````

### P32 · `content/for-modders.md` — the opt-in identifier-rule sentence

Removed; the paragraph now ends at *"…registers `SaveSanitizer`."*

<!-- VERBATIM src="content/for-modders.md" -->
````text
The one exception is the save-repair module, `Code/90_SaveSanitizer.lua`, which
registers `SaveSanitizer`. The optional mod follows the same rule with its own
`Opt_` prefix: `Code/Opt_NoHomeless.lua` registers `NoHomeless`.
````

### P33 · `content/for-modders.md` — the repo links + plural sentence

Now reads: one link (the fix pack repository) and *"That repository is public
on purpose. Every fix carries a header explaining the defect, citing the game's
own code by file and line, and the development notes behind them are in the
same tree."*

<!-- VERBATIM src="content/for-modders.md" -->
````text
- [Community Fix Pack repository](https://github.com/catt144/SMR-CommunityFixPack)
- [Opt-In Modules repository](https://github.com/catt144/SMR-CommunityOptInPack)

Those repositories are public on purpose. Every fix carries a header explaining
the defect, citing the game's own code by file and line, and the development
notes behind them are in the same tree.
````

### P34 · `content/for-modders.md` — the two listing calls

Now reads: *"The pack exposes a listing call — `SMRFixPack.ListFixes()` — which
walks every registered fix and writes its identifier, status and title through
the mod's logging path."*

<!-- VERBATIM src="content/for-modders.md" -->
````text
Each pack exposes a listing call — `SMRFixPack.ListFixes()` and
`SMROptInPack.ListFixes()` — which walks every registered fix and writes its
identifier, status and title through the mod's logging path.
````

### P35 · `content/for-modders.md` — the two-mod Save data section

Now reads: *"The mod writes a small, enumerated set of fields into savegames,
and all but one of them mean nothing to the game once the mod is gone. The
exception is deliberate and documented on the [installing
page](install.md#what-it-puts-in-your-save) — where a repair put back a bonus
that a broken patch migration dropped, that bonus is an ordinary one of the
kind the game hands out itself and keeps working after the mod is gone. The
full enumeration lives in the development notes in the repository above."*
⚠️ On restore, note the original's "exception" was the OPT-IN dial bonus; the
rewritten page's "exception" is the fix pack's own restored-bonus item. Restore
the original wording whole, do not merge.

<!-- VERBATIM src="content/for-modders.md" -->
````text
Both mods write a small, enumerated set of fields into savegames, and all but one
of them mean nothing to the game once the mod is gone. The exception is
documented in plain language on the [FAQ](faq.md#how-do-i-get-it-out) — an
optional drone dial left off its base setting stores an ordinary bonus that
survives uninstalling.

⚠️ **One thing that will mislead you if nobody says it:** the optional mod's
persisted fields carry the **fix pack's** prefix, not its own. They were kept
byte-identical when the two mods were split so that existing savegames did not
have to be migrated. If you are inspecting a save, do not attribute a field to a
mod by its prefix alone. The full enumeration lives in the development notes in
the repositories above.
````

### P35b · site `mkdocs.yml` — the HTML meta description

Now reads: `site_description: "Bug fixes for Surviving Mars: Relaunched."` —
this string lands in the page `<meta name="description">` and is what search
results display. ⚠️ Found by the post-edit wide sweep, not the survey — the
brief recorded `mkdocs.yml: 0 hits` because it grepped opt-in-shaped patterns
and this says "optional modules".

<!-- VERBATIM src="mkdocs.yml" -->
````text
site_description: "Bug fixes and optional modules for Surviving Mars: Relaunched."
````

### P36 · site `README.md` — the unfinished-marker paragraph (plural → singular)

Now reads: *"…there are no store links, because the mod has not been
uploaded."*

<!-- VERBATIM src="README.md" -->
````text
⚠️ **One thing on them is deliberately unfinished, and it is marked in place:**
there are no store links, because neither mod has been uploaded. Bug reports are
routed as of 2026-08-13 — mod-page comments first, this project's issue tracker
for reports carrying a save or a log.
````

### P37 · site `README.md` — the opt-in row of the mods table

Removed row (the site's pages no longer document that mod, so the table saying
so would be false). The repo link itself is public and unchanged.

<!-- VERBATIM src="README.md" -->
````text
| **Community Fix Pack: Opt-In Modules** | [`catt144/SMR-CommunityOptInPack`](https://github.com/catt144/SMR-CommunityOptInPack) | optional changes to how the game behaves, all off until you turn them on |
````

## Fix pack — `c:\Dev\SMR-BugFixPack`

### P38 · `metadata.lua` — the `description` player string

⛔ Ships inside the mod; changing it after upload needs a version bump and a
re-upload. Now reads the same string with the separate-mod clause replaced by
*"preferences and features are deliberately not in it"*. The brief's survey
classed this line as fixed already; it was not — the clause named the opt-in
mod and was found by this prompt's own re-survey.

<!-- VERBATIM src="metadata.lua" -->
````text
	'description', "Bug fixes for Surviving Mars: Relaunched. Almost every fix targets a defect verified in the game's own code — the code says one thing, does another, and the fix makes it do what it says. It fixes bugs rather than rebalancing the game: preferences and features live in a separate mod, Community Fix Pack: Opt-In Modules, and neither mod needs the other. Nothing is patched on disk; the mod wraps the game's own code at runtime and no game files are modified. Safe to add to a save you have already played — the pack writes almost nothing into your savegame, and removing it simply lets the original bugs come back. Every fix checks the game's code before it patches anything and stands down if an official patch changes what it was written for. Five of the fixes are judgment calls rather than plain repairs, and the mod page says which and why.",
````

### P39 · `metadata.lua` — the `last_changes` player string

Now reads: `'last_changes', "Initial release.",` — ⛔ on restore do NOT paste
this back; a changelog describes the release it ships with. Context only.

<!-- VERBATIM src="metadata.lua" -->
````text
	'last_changes', "Initial release: the bug fixes. The optional modules moved to their own mod, Community Fix Pack: Opt-In Modules.",
````

### P40 · the store card — `RELEASE_DESCRIPTION_FIXPACK.md` + `STORE_FIXPACK.md` (identical player text, both edited in lockstep)

**P40a — the separate-mod clause** (both files). Now reads: *"Preferences and
features are not in here."* with the bullet re-wrapped:

<!-- VERBATIM src="docs/agent/reports/STORE_FIXPACK.md" -->
````text
- **It fixes bugs rather than rebalancing the game.** Almost every fix targets
  something we verified in the game's own code: the code says one thing, does
  another, and we make it do what it says. Preferences and features are not in
  here; they live in a separate mod you do not need. **Five of them are judgment
  calls rather than plain repairs** — in two of those the game's code is not
  wrong at all and we made a call anyway, and one of them changes how the game
  feels. All five are listed further down, with our reasoning, rather than
  quietly folded in.
````

**P40b — the companion-mod bullet** (both files). Now reads: *"**You do not
need anything else.** The pack works on its own."*

<!-- VERBATIM src="docs/agent/reports/STORE_FIXPACK.md" -->
````text
- **You do not need anything else.** The pack works on its own. There is a
  companion mod, *Community Fix Pack: Opt-In Modules*, and neither mod needs the
  other — each works alone, and they work together.
````

**P40c — the FILL-IN 2 marker line** (card only; the STORE file never carried
the marker):

<!-- VERBATIM src="docs/agent/reports/RELEASE_DESCRIPTION_FIXPACK.md" -->
````text
>>> FILL-IN 2 — store link to the opt-in mod, or DELETE THIS LINE <<<
````

**P40d — the uninstall cross-reference** (both files). The paragraph now ends
at *"…takes effect after you restart the game."*

<!-- VERBATIM src="docs/agent/reports/STORE_FIXPACK.md" -->
````text
 Turning this pack off in the mod manager takes effect after you
restart the game. If you also use *Community Fix
Pack: Opt-In Modules*, read the uninstall note on that mod's page before you
remove **it**: it has settings that leave something behind in your save, and its
page tells you the two steps that avoid it.
````

---

## Passages checked and deliberately LEFT

| place | why it stays |
|---|---|
| `metadata.lua` / `items.lua` Lua comments | engineering context, never player-visible (brief §A1 table) |
| card + STORE *"Individual fixes can be switched off, but only by a companion mod that loads before this one — a modder's facility…"* | that "companion mod" is a hypothetical modder-authored veto mod (the `SMRFixPack_Disabled` mechanism), not the opt-in product; true and load-bearing on its own |
| every `docs/agent/` bug entry, fact, WORKFLOW, STATE, FIX_POLICY reference | agent-facing records; the split and the handoffs are history, not promises to players |
| `docs/archive/**` | append-only, frozen |
| `RELEASE_DESCRIPTION_OPTIN.md` / `STORE_OPTIN.md` bodies | not shipped now; they are the audited paste source for the day the opt-in publishes — banner added, body untouched |
| `RELEASE_DESCRIPTION_RESCUE.md` opt-in mentions | the rescue tool's publish trigger is dial residue, which only the opt-in's dials can create — if the contingency ever fires, the opt-in is necessarily already published, so its mentions are correct in every world where the card ships |
