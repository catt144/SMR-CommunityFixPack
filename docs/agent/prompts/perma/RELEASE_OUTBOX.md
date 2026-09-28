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

### Pending — C120: automatic rockets to Earth launch instead of waiting forever for deportees (2026-09-28)

**BUILT, NOT READY: desk-verified on archived 1.1.1 Lua only; the proposed in-game sitting in
[C120](../../bugs/C120.md) "Build" has not run.** `Code/Fix_DeportRocketLaunch.lua` (`DeportRocketLaunch`).

Player surface for the next release: with a deport law on (or tourists or Earthsick colonists
waiting), an automatic rocket to Earth no longer sits on the pad drafting "dozen after dozen". Once
everything else is ready, it takes aboard the leaving colonists it can take right away and
launches. Colonists still walking or riding over stay on Mars, as they do after a manual
Launch, and catch the next rocket. A landed rocket with no destination no longer collects
departing colonists, and hands back any it was holding. No limit is placed on how many
colonists a rocket takes.

## Last released

**v17** (2026-09-26). Its entry and every earlier release are in
`docs/archive/RELEASE_HISTORY.md`, oldest first.
