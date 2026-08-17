# Relaunched Fix Pack — Surviving Mars: Relaunched

A bug-fix mod for Surviving Mars: Relaunched. Almost every fix repairs a
**defect verified in the game's own shipped Lua** — the code says one thing,
does another, and the fix makes it do what it says. No rebalancing, no
features, no game files modified: everything is patched at runtime, in a
mod-compatible way, against game version **1.0.7.396349**.

**Status: version 1.0.0 — prepared for first release, not yet on a store.**

## What it fixes

**75 fix modules**, covering disasters and weather, colonists and domes,
drones and logistics, buildings and economy, trains, rockets and asteroids,
story sequences, and the numbers on your screen. Several of them also repair
damage already sitting in your save when you load it. Five fixes are judgment
calls rather than plain repairs — each one is disclosed on the mod page, with
the reasoning.

The full player-facing list, one entry per fix, lives on the companion docs
site: [fix-list](https://github.com/catt144/SMR-CommunityMods/blob/main/content/fix-list.md)
(the rendered site goes live alongside the store release). The engineering
tracker behind it is in this tree: [docs/agent/bugs/INDEX.md](docs/agent/bugs/INDEX.md)
— 167 tracked findings, ranging from verified-and-fixed to open candidates.

## For players

Install to `%AppData%\Surviving Mars Relaunched\Mods\` (or from the mod page,
once it is live) and enable **"Relaunched Fix Pack"** in the Mod Manager.
**Then restart the game** — enabling or disabling any mod only takes effect on
a full restart.

There is nothing to configure. The pack has no options page — it repairs bugs,
so "on" is the whole interface — and there is no in-game way to switch off an
individual fix on any platform (see [For modders](#for-modders) for the one
route that exists).

**Your save is safe, including a long one.** The pack writes almost nothing
into your savegame: a timestamp on a housing reservation, a timestamp on a
colonist who has just taken shelter, a "the player has set this payload" flag
on a rocket, and a handful of small stamps that let a repair know it has
already run. None of it means anything to the game without the pack. One item
is deliberately not inert: where a repair put back a bonus that a broken patch
migration dropped, that bonus is an ordinary one of the kind the game hands
out itself and keeps working after the mod is gone — which is the point of
restoring it. Removing the mod is always safe: the bugs it was holding back
come back, and repairs already made to your save stay made.

**Consoles and the Microsoft Store version:** while any mod is enabled, the
game does not unlock achievements on Xbox, PlayStation or the Microsoft Store.
That is the game's own rule and it applies to every mod; Steam and other PC
versions are unaffected.

Before anything ships, an automated suite of **96 checks** is run against the
game with the pack installed and without it.

## Reporting a bug

Comments on the mod page are fine for quick reports. If you have a savegame or
a log, [open an issue](https://github.com/catt144/SMR-CommunityFixPack/issues)
— this tracker is watched.

## For modders

See [docs/agent/FIX_POLICY.md](docs/agent/FIX_POLICY.md) for the house rules:
patch the smallest thing that fixes the bug, chain rather than clobber,
additive message handlers, fail safe rather than fail clever. Every fix
inspects the code it is about to patch and stands down with a logged reason if
a game update changed its shape.

`SMRFixPack_Disabled` is the veto surface. Setting a fix's identifier in that
global table **before the fix pack loads** vetoes the fix — the pack registers
it, marks it disabled, and never applies it:

```lua
SMRFixPack_Disabled = SMRFixPack_Disabled or {}
SMRFixPack_Disabled["DustDevilSpawnGate"] = true
```

Identifiers are the fix file names minus the `Fix_` prefix
(`Code/Fix_DustDevilSpawnGate.lua` registers `DustDevilSpawnGate`); the
save-repair module `Code/90_SaveSanitizer.lua` registers `SaveSanitizer`. The
developer console is not a route — the veto table is read at load, long before
anything can be typed. `SMRFixPack.ListFixes()` walks every registered fix and
writes its identifier, status and title through the mod's logging path.

## Credits

- ChoGGi — the original Surviving Mars "Fix Bugs" mod documented several of
  these bug families years ago; this pack independently re-verified everything
  against the Relaunched source.
- LukeH — Martian Express patch research for the original game.
