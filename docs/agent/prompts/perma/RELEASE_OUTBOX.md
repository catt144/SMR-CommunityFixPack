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

### Pending — C108 Infected colonists visit a medical building once the Wildfire cure is found (2026-09-18)

**No hold: the boot is done.** Desk harness `tools/desk_c108_wildfire_cure.py` (20 of 20 demands,
7 falsifying variants; the unfixed pack fails the cure demand). The owner's boot on 2026-09-18
(`Mars.exe-20260918-23.44.18-6a91a190.log` :144) logged `WildfireCureVisit: applied`, and logscan
read 52 of 52 modules applied with no error-shaped line (C108 "In game"). The cure itself has not
been watched in game; that attended check needs a Wildfire save at the cure stage and is the
owner's call.
Source of the report: r/SurvivingMars, 2026-09-18.

C108 is a new public row:

> Once the Wildfire cure is found, infected colonists now go to a medical building and are cured.
> Colonists whose dome's medical care kept them healthy never went, so the mystery could not finish.

Developer detail: 1.1.0 pays each serviced category's stats at home on rest
(`ApplyResidenceAdditiveStats`), medical included, so under a Medical Center an infected colonist
never drops below the 70 Health that sends them to `MedicalBuilding:Service`, the only place the
cure runs. The pack wraps `PickInterest` so that an infected colonist's daily interest is
`needMedical` while vaccination is on. This needs no DLC.

## Last released

**v13** (2026-09-18). Its entry and every earlier release are in
`docs/archive/RELEASE_HISTORY.md`, oldest first.
