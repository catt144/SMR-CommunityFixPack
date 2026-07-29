# Development Workflow

## Reading path for a new session

1. `docs/ENGINE_FACTS.md` — the proven engine behaviors (several are the
   opposite of what the code suggests). Read before writing or reviewing any
   fix.
2. `docs/STATUS.md` — current state: authoritative build counts, open user
   decisions, next gates. Session history lives in
   `docs/archive/SESSION_LOG.md` (append-only, newest first).
3. `docs/BUGS.md` — the canonical defect tracker (index + full entries).
   Update it in the same change that adds or edits a fix; statuses live in
   TWO places (index row + heading tag) — never flip one without the other.
4. `docs/FIX_POLICY.md` — how we patch. Binding for every fix.
5. `docs/PLAYTEST_CHECKLIST.md` — the owner's live playtest queue, the
   verified console-command table, and the reporting protocol.

## Layout

- **Dev repo (this folder):** `C:\Dev\SMR-BugFixPack` — git-versioned, canonical.
- **Game install:** `A:\SteamLibrary\steamapps\common\Project Spark`
  (Surviving Mars: Relaunched; "Project Spark" is the Steam folder codename).
- **Shipped Lua source (read-only reference):** `<game>\ModTools\Src`
  (`Lua\`, `CommonLua\`, `Data\`, `DLC\`). We never modify anything under the
  game folder.
- **Mod install point:** `%AppData%\Surviving Mars Relaunched\Mods\SMR-BugFixPack`
  — a directory junction into the dev repo (see below), so edits are live.
- **Companion TestKit** (never shipped): `C:\Dev\SMR-BugFixPack-TestKit`
  (own git repo, local-only by decision — see its README).

## Install for testing

```powershell
New-Item -ItemType Directory -Force "$env:APPDATA\Surviving Mars Relaunched\Mods" | Out-Null
New-Item -ItemType Junction -Path "$env:APPDATA\Surviving Mars Relaunched\Mods\SMR-BugFixPack" -Target "C:\Dev\SMR-BugFixPack"
```

Then enable "Community Fix Pack" in the game's Mod Manager. After editing Lua,
restart the game. **Opt-module first-enable caveat is FIXED (audit 2026-07-29):**
hooks now install at file scope, so a first mid-session Mod Options enable
works without a relaunch.

In-game checks: console `SMRFixPack.ListFixes()` prints each fix's status
(active / inactive+reason / disabled / error).

## Per-fix discipline

1. Every fix links to a BUGS.md entry with file:line evidence (FIX_POLICY §4).
2. Before patching, re-verify the target against the cited Src lines; the
   apply() self-check then guards it at runtime and returns a reason string
   (never errors) if a game update changed it.
3. Parse sweep before any commit that touches Lua: python + `luaparser`,
   `ast.parse(open(f, encoding='utf-8-sig').read())` over every edited file —
   a syntax error in ANY listed file breaks the whole pack at load.
4. One commit per fix or tight group; BUGS.md updated in the same commit;
   MOD_DESCRIPTION.md updated in the same commit as the code change it
   describes.

## fpk verification — RELEASE GATE, re-run after every game update

All BUGS.md line numbers come from `ModTools\Src`; the game executes
`Packs\Lua.fpk` + `Data.fpk`. **Parity is PROVEN for the current build
(1.0.7.396349, extraction diff 2026-07-29): 2,250/2,256 shipped Lua files
byte-identical to Src; the 5 divergences are engine/tooling only** (details in
ENGINE_FACTS.md). The discipline guards *future* updates:

1. After every game patch, re-extract `Packs\Lua.fpk` (FLPK container, zstd
   per file) and diff against the new Src tree; re-verify every replacement
   fix's target function byte-for-byte (the ~29 full replacements are the
   pack's patch-rot exposure — C1 in AUDIT_FINDINGS.md).
2. Runtime self-checks stay mandatory in every apply() regardless (existence/
   layout checks only — the sandbox has no introspection; they catch renamed/
   removed targets, NOT an edited same-named function — hence step 1).

## Testing checklist per fix

1. Load a save (or new game) where the bug reproduces; confirm reproduction
   with the mod disabled.
2. Enable mod; confirm fixed behavior.
3. Confirm no error spam in the log (`%AppData%\Surviving Mars Relaunched\logs`).
4. Save with mod enabled → disable mod → load: game must not break (PT-20
   shape; FIX_POLICY §3).
5. Update BUGS.md status to `tested` (both places) per the checklist's
   reporting protocol.

The TestKit's `SMRTest.RunAll()` A/B pair (baseline vs full pack) is the
regression harness; run it as pre-flight when STATUS says one is owed.

## Release steps

- Owner tasks first: preview image (PDX ≤2 MB / Steam ≤1 MB), screenshots,
  portal rules check for console publishing (AUDIT_FINDINGS plan 2.5).
- metadata.lua: bump `version_major`/`version_minor`, refresh `last_changes`.
  `short_description`, `ignore_files`, `optional_mod` are already in place
  (audit 2.1). `lua_revision` stays 350453.
- MOD_DESCRIPTION.md: delete the `[DRAFT NOTE]` markers; do NOT promise the
  ClassicRockets export half; sync the fix list with BUGS.md statuses.
- Upload via the in-game Mod Editor (Paradox Mods / Steam Workshop). The
  editor round-trip is SAFE since audit 2.2: items.lua carries one
  `ModItemCode` per Code/ file in metadata order, so SaveDef regenerates the
  same `code` list. If a Code/ file is ever added/removed/reordered, update
  BOTH metadata.lua `code` AND items.lua in the same commit, same order.
- The TestKit must NOT be uploaded.
- Credit ChoGGi (Fix Bugs) + LukeH (Martian Express) as prior art.
