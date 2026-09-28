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

### Pending — F128: the RC Driller's hammer sound lines up with its three strikes (2026-09-28)

**READY for the next upload, with one owner check open.** The strike times were measured in game
and heard in sync by the owner through a live swap of the same data. The updated module has not
booted yet; a boot and a listen would make it `tested-attended`. [F128](../../bugs/F128.md).
`Code/Fix_SilentHitMomentFX.lua` (`SilentHitMomentFX`).

Player surface for the next release: our v7 fix gave Roscosmos's RC Driller a drill-hit sound that
played twice per work loop, out of time with the hammer. It now plays on each of the hammer's
three strikes. A Driller already drilling picks up the new timing at its next deposit.

### Pending — C120: automatic rockets to Earth launch instead of waiting forever for deportees (2026-09-28)

**READY for the next upload: the attended A/B passed on 2026-09-28** on a copy of the owner's
colony. The fix-off stall reproduced; with the fix on, 195 deportees boarded and the launch gate
opened; Cancel Flight handed the held deportees back; and the save loaded clean after the pack was
disabled and the game restarted. The take-off itself is inferred from source, not logged.
[C120](../../bugs/C120.md) "Sitting" holds the logs and readings. `Code/Fix_DeportRocketLaunch.lua`
(`DeportRocketLaunch`). The release seat still runs the normal upload gates.

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
