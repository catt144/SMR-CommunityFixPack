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

Built, no public row or count change: `Code/00_Core.lua` hardening rows 1 + 2 (checklist 53,
2026-09-16) — non-table pre-load globals are replaced and logged, veto reads are `pcall`'d. Desk
control `tools/desk_ck53_hostile_globals.py`; not playtested, by the owner's condition. The shipped
Code changed, so the next upload carries it; do not look for a fix-list row.

### Pending — C95 return-home repair and C102 safe expedition fallback (2026-09-17)

⭐ **Cleared to ship, 2026-09-17.** The owner watched three legs: an ordinary UI expedition home on
the reporter's own save, a far-pad return on their rail colony, and a pack-disabled full restart
mid-return. C95 is `tested-attended`; 0 Lua errors. ⚖️ **Waived by the owner the same day:** a train
return and a positive live C102 reroute — *"waive it, its working and much better than our previous
builds"* — so the public words must say plainly that neither was watched in play. Evidence and
scope: `docs/agent/reports/C95_PLACE_HOME_BUILD.md`, entries C95 and C102.

⚖️ **Owner's ask for this release: C95 is the FEATURED fix.** Short, plain: what it does, and the one
gotcha, in the owner's own framing — if every dome is off and only habitats are live, and those
habitats refuse the colonist, a returnee still walks to the nearest dome and dies. Say it is the
game's own safety system, which the pack does not override; overriding it would be a rewrite we are
not doing. (The related arrival-side case is C106, filed, not fixed.) The featured section is new,
so the fix list makes room for it: the owner asked for about six of the weakest headline lines to
come out, and a truth pass over all 21 rides with it.

C95 replaces its existing marked judgment-call row with a repair:

> Habitat residents can join expeditions like anyone and come back to their own habitat. If the
> habitat is out of walking range of the landing, they are set down at its door, the same way the
> rocket picked them up. If that home can no longer be used, they go to the nearest safe dome.

C102 is a new public row:

> Expedition returnees whose home is unavailable avoid switched-off or lifeless domes
> when a safe reachable dome is available, even if its housing is full.

Developer detail: the held habitat is selected before fallback housing reservations, whatever the
route; only a returnee holding a habitat expedition reservation and outside walking range is moved,
to the habitat's entrance at their native walk order, and native entry takes them in. New arrivals,
migrants and covert-ops recruits are never moved. Cross-map homes are not admitted. Housing is
restored before employment on rejoin. C102 reuses the existing arrival safety rule. No safe
destination anywhere still preserves the game's assignment. ⚖️ **RULED 2026-09-17: that stands** —
with no safe dome anywhere the game's own choice is kept. Update C95's
old exclusion/judgment-call wording wherever the release prompt finds it. No version, store page,
public site or upload changed in this job.

## Last released

**v11** (2026-09-16). Its entry and every earlier release are in
`docs/archive/RELEASE_HISTORY.md`, oldest first.
