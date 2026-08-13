# Questions

!!! warning "LAYOUT SPECIMEN"
    These are real questions, drawn from ones actually asked during testing
    rather than invented — but the answers are drafts and two of them are
    deliberately incomplete. See the holes marked below.

## Can I add this to a save I have already played?

Yes. It is designed for exactly that, and it has been loaded onto
several-hundred-sol campaign saves during testing.

## Can I remove it later?

Yes — removing it simply lets the original bugs come back.

!!! danger "One real exception, and it is worth reading"
    If you used the optional **drone stat dials** and left one off its base
    setting, that boost is stored in your savegame as an ordinary game value.
    Remove the mod and **the boost stays, permanently.** Set both dials back to
    base and load the save once before uninstalling if you want a clean save.

## Do I need both mods?

No. Neither one requires the other. Install the fix pack alone, the optional
modules alone, or both — all three combinations work.

## Why did my toggles and dials reset?

The optional modules moved into their own mod, which means the game files them
under a new name and your previous settings do not carry over. Set them once and
they stay set. Your **savegames are unaffected** — this only touches the mod's
own options.

## Does this change game balance?

The fix pack, no. The optional pack, yes — deliberately, per module, and only
for the ones you switch on.

## Why isn't *X* fixed?

Some things that look like bugs are the game working as designed, and some
repairs would need changes large enough to count as a redesign. A few fixes sit
on the line between "bug" and "design choice"; those are called out rather than
presented as plain repairs.

## What happens when the game updates?

Each fix checks its own target at load. If a game update changes something a fix
depends on, that fix reports itself inactive instead of running against code it
no longer recognises.

---

!!! note "Holes this specimen is deliberately leaving open"
    - **Uninstall and leftover data in general** — waits on the D13 chain's
      disposition table, and on whether the save-rescue tool is published at all.
    - **Load order and other mods** — needs a real answer, not a guess.
    - **Console / gamepad players** — unknown; must be checked, not assumed.
