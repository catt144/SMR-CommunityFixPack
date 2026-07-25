# Community Fix Pack — Surviving Mars: Relaunched

A bug-fix mod for Surviving Mars: Relaunched. Every fix targets a **verified
defect in the game's shipped Lua source** — no balance changes, no opinions,
no game files modified. Fixes are applied at runtime in a mod-compatible way
and can be individually disabled.

**Status: in development, not yet released.**

## Current fixes

| Fix | What it does |
|-----|--------------|
| CaveInsNoDisasters | Cave-ins no longer occur when the "No Disasters" game rule is active. The underground marsquake scheduler was missing the rule check that every other disaster has. |

The full defect tracker (29 verified findings and counting) lives in
[docs/BUGS.md](docs/BUGS.md).

## For players

Install to `%AppData%\Surviving Mars Relaunched\Mods\` and enable
"Community Fix Pack" in the Mod Manager. To disable a single fix, create a tiny
mod that loads before this one containing e.g.
`SMRFixPack_Disabled = { CaveInsNoDisasters = true }`, or run it in the console.
Console command `SMRFixPack.ListFixes()` shows what's active.

Removing the mod is always safe — it stores nothing in your savegames.

## For modders

See [docs/FIX_POLICY.md](docs/FIX_POLICY.md). Short version: data patches and
chained wrappers over replacements; every fix self-checks the target code
before patching and deactivates itself (with a logged reason) if a game update
already fixed it; `SMRFixPack_Disabled` is the veto surface.

## Credits

- ChoGGi — the original Surviving Mars "Fix Bugs" mod documented several of
  these bug families years ago; this pack independently re-verified everything
  against the Relaunched source.
- LukeH — Martian Express patch research for the original game.
