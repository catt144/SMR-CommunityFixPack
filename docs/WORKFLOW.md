# Development Workflow

## Layout

- **Dev repo (this folder):** `C:\Dev\SMR-BugFixPack` — git-versioned, canonical.
- **Game install:** `A:\SteamLibrary\steamapps\common\Project Spark`
  (Surviving Mars: Relaunched; "Project Spark" is the Steam folder codename).
- **Shipped Lua source (read-only reference):** `<game>\ModTools\Src`
  (`Lua\`, `CommonLua\`, `Data\`, `DLC\`). We never modify anything under the game folder.
- **Mod install point:** `%AppData%\Surviving Mars Relaunched\Mods\SMR-BugFixPack`
  — a directory junction into the dev repo (see below), so edits are live.
- **Docs:** `docs\BUGS.md` (canonical defect tracker — keep current!),
  `docs\FIX_POLICY.md` (how to patch), `docs\RESEARCH.md` (community bug catalog).

## Install for testing

```powershell
New-Item -ItemType Directory -Force "$env:APPDATA\Surviving Mars Relaunched\Mods" | Out-Null
New-Item -ItemType Junction -Path "$env:APPDATA\Surviving Mars Relaunched\Mods\SMR-BugFixPack" -Target "C:\Dev\SMR-BugFixPack"
```

Then enable "Community Fix Pack" in the game's Mod Manager. After editing Lua,
restart the game (or use the in-game console `ReloadLua()` if available — mod
code re-runs on `OnMsg.ReloadLua`; our Register calls re-apply, and wraps that
captured `orig` at first load chain harmlessly).

In-game checks: console `SMRFixPack.ListFixes()` prints each fix's status
(active / inactive+reason / disabled / error).

## fpk verification (required per fix, before release)

All BUGS.md line numbers come from `ModTools\Src`, but the game executes
`Packs\Lua.fpk` + `Data.fpk`, whose file dates are slightly newer than the Src
tree. A fix that assumes un-hotfixed code must verify its target. Options:
1. Runtime check inside `apply` (preferred, already policy): confirm the
   function/table still exhibits the bug shape before patching; bail with a
   reason string otherwise.
2. Unpack the fpk (Haemimont .hpk-family archive; community unpackers exist for
   Surviving Mars/JA3 — verify tool compatibility before trusting output) and
   diff the target function against Src.
3. In-game console: print the source via `debug.getinfo` / inspect behavior.

## Testing checklist per fix

1. Load a save (or new game) where the bug reproduces; confirm reproduction
   with the mod disabled.
2. Enable mod; confirm fixed behavior.
3. Confirm no error spam in the log (`%AppData%\Surviving Mars Relaunched\logs`
   if present, or console).
4. Save with mod enabled → disable mod → load: game must not break.
5. Update BUGS.md status to `tested`.

## Release (later)

- Set real `author` in metadata.lua; bump `version`; write player-facing fix
  list in description + README.
- Upload via in-game Mod Editor (Paradox Mods / Steam Workshop) — it packs this
  folder. Keep `docs\`/`.git` out of the upload if the packer includes them
  (check on first upload; if needed, maintain a clean staging copy).
- Credit ChoGGi's "Fix Bugs" (original game) for prior documentation of several
  bug families; all remaster findings independently verified against Relaunched source.

## Context-wall resume protocol (for Claude)

If a session dies mid-work:
1. Read `docs\BUGS.md` — statuses tell you exactly what's done/next.
2. Read `docs\FIX_POLICY.md` before writing any fix.
3. Memory files (`bug-sweep-findings`, `mod-project-requirements`) summarize the
   same content; BUGS.md is canonical when they disagree.
4. Work top-down by severity within BUGS.md; update statuses in the same turn a
   fix is written; commit to git with one fix per commit.
