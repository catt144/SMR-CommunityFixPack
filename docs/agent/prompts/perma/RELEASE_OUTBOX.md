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

### Pending — C107 Dry Farming reaches the Feeding the Future plant farms (2026-09-18)

**Hold for C107's in-game control before upload.** The build is desk-tested only
(`tools/desk_c107_dry_farming.py`, 19 checks, 7 falsifying variants); the TestKit probe
`DryFarmingFarms` and the control in `docs/agent/bugs/C107.md` have not run in a game.
Source of the report: a Steam comment, 2026-09-18.

C107 is a new public row:

> The Dry Farming breakthrough now halves crop water on the Feeding the Future farms too:
> Small Farm, Underground Farm, Small Underground Farm and Automated Farm. Fungal and
> Insect Farms stay excluded, as the base game excludes Fungal Farms.

Developer detail: `Techs.DryFarming` pays three class labels (`Data/Tech.lua:787-801`); a
building joins only its own class label, so the norman farm templates were never reached.
Four `Effect_ModifyLabel` entries are appended at data load, copying the shipped percent,
and saves that researched the tech earlier are healed once on load. No version, store page,
public site or upload changed in this job.

## Last released

**v12** (2026-09-17). Its entry and every earlier release are in
`docs/archive/RELEASE_HISTORY.md`, oldest first.
