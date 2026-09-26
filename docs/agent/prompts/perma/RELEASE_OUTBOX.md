# Release outbox — player-facing changes staged for the NEXT upload

## Must_Read_Header
<!-- RULES -->
Rule: Append a filled `### Pending` entry whenever a player-facing fix is added, retired, or materially respecified. [A3: pass]
Rule: Do not append a pending entry for a pack-internal fix that never shipped broken. [A3: pass]
Rule: Append every pending entry to `docs/archive/RELEASE_HISTORY.md` and empty `Pending` only through `release_prompt.md` after upload. [A3: pass]
Rule: Do not delete a pending entry except through a release or with an explicit withdrawal reason. [A3: pass]
<!-- /RULES -->

This ledger tracks every player-facing tree change since the last upload.
`docs/agent/prompts/perma/release_prompt.md` derives `last_changes`, fix-list
rows and the store-card count from it, then appends Pending entries to
`docs/archive/RELEASE_HISTORY.md` after upload. `docs/agent/support/RELEASE_SURFACES.md` defines which changes
have a player surface.

**Live tree version:** `metadata.lua` `version` — read it, never hand-set (editor/version rail (`docs/agent/prompts/perma/release_prompt.md` § Release rails)).
**Live count word:** whatever `metadata.lua`'s `description` currently says
(`grep -oE '[A-Z][a-z]+(-[a-z]+)? repairs' metadata.lua` — one hit; zero is a FAIL). Each pending fix that has a
player surface bumps it by one on release.

## Pending — goes out with the next upload

### Pending — C119: clear stale power cells when a colony loads (2026-09-26)

**HOLD: the reporter load cleared 355 stale cells; the clean colony, powered
topology, Excavator and Open Farm controls passed. The owner confirmed the new
reporter cable run was isolated, explaining its unpowered grid. A run joined
to an existing powered network and a visual check remain.** [C119](../../bugs/C119.md) records the retail logs,
the owner-ruled load-only scope and the remaining check. A restored powered
area has not yet been witnessed.

Player surface for the next release: a colony whose old power-connection cells
outlived their objects can use the affected area again after loading. Cables and
powered buildings placed there should connect normally. The repair touches
electricity only and runs at load; the source of the first stale cell remains
unknown.

### Pending — LoadFirst: the pack moves itself to the front of the mod load order (2026-09-25)

**MERGED to `main` at `fa0893a` (2026-09-26) after the owner-watched sitting; NOT uploaded.** The record is
[LOAD_ORDER_FIRST_BUILD_2026-09-25.md §19](../../reports/LOAD_ORDER_FIRST_BUILD_2026-09-25.md#19--the-attended-sitting--every-leg-as-predicted-order-restored-2026-09-26)
(audit verdict §17, preparation §18). Legs A–D by the owner (notice once, hot enable with
Restart now, opt-out and opt-in, diagnostic Paradox log-out/log-in with the order untouched),
E by the seat (order restored, read back on `main`). The production module is unchanged
since `8ea5449`. Next: the upload on the owner's go. Release note: Paradox-installed
players see the notice again after each update the sync applies (§17).
Ships on the owner's go for the upload. The consumed brief's
authority and unfinished requirements are retained in that report.
The normal promotion/restart/Passage Network evidence remains valid on this rig; the ordinary
desk harness and its behavioral controls pass; the remaining failures concern the sitting plan.
Owner-watched sitting 2026-09-26 (§19).
Owner's choice of option B, 2026-09-25.

Player surface, three parts, none of them a fix-list row unless the release seat decides so:

> The pack now moves itself to the front of your mod load order the first time it starts, so its
> repairs are applied before other mods change the same parts of the game. Your other mods keep
> their order. It tells you when a restart is needed, and you can turn this off under Options >
> Mod Options > Relaunched Fix Pack.

- **The pack lists on the Mod Options page again**, with one toggle, "Load this pack first"
  (default on). The 2026-08-12 "no options" shape is reversed for this one control.
- **The C canary in `metadata.lua`** (`SMRFP-LOADORDER-CANARY-2026-09-25-b7e1`, inert hand-written
  code in option C's shape). ⛔ The post-upload seat runs its three-part check BEFORE restoring the
  comments (`support/POST_UPLOAD_CLOSE.md` §1); the check and the per-portal prediction are in the
  report, "The C canary", qualified by §§11–13 R6. Record the portal and whether a save preceded
  packing; a stripped package decides only that tested path.

Build detail at `8ea5449`: `Code/01_LoadFirst.lua`, registered `LoadFirst` (`optional = true`); rebuilds
`AccountStorage.LoadMods` through `TurnModOff`/`TurnModOn` with every other mod's relative order
kept, requests the account save through a changed `WriteModPersistentData`, and honours
`SMRFixPack_Disabled["LoadFirst"]`. Each promotion schedules its notice. A full foreign slot
refuses the write without data loss or a promotion save request; persistence then depends on
a later game save. The already-first account-LoadAllMods path deliberately does not probe.

## Last released

**v16** (2026-09-24). Its entry and every earlier release are in
`docs/archive/RELEASE_HISTORY.md`, oldest first.
