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

### ⚖️ Owner's store-card task for this release (2026-09-17, decided — EXECUTED)

⭐ **Executed 2026-09-17**, in the v12 prepare commit: all four card copies, the shipped
`description` and `last_changes`, and the site (fix list 52 → 53, judgment calls 5 → 4). The ruling
below is kept verbatim as decided — it is what §5 appends to `RELEASE_HISTORY.md` after the upload,
and it is no longer work to be done.

Every change below lands in **all four copies together**, which a 2026-09-17 check found byte-identical:
`docs/UPLOAD_WORKFLOW.md` plain (`:116-141`) and BBCode (`:239-263`),
`docs/agent/reports/STORE_CARD_LIVE.md` (`:163`, `:292`), and the shipping string
`metadata.lua:96`. Re-derive every count word from the site list rather than hand-editing it; the
headline count in `metadata.lua`'s comment block moves 21 → 14.

**1. A new FEATURED section for C95**, placed above "Some of what it fixes". Owner-approved draft:

> **Featured: expedition crews come home**
>
> Colonists living in habitats can join expeditions again, and they come back to the habitat they
> left. If their habitat is too far from the landing site to walk, they are set down at its door, the
> same way the rocket picked them up. If the habitat is gone or unusable, they go to the nearest dome
> that is working and has air.
>
> One gotcha. If every dome is switched off and only habitats are alive, and those habitats refuse
> the colonist through their filters, the colonist still walks to the nearest dome and dies there.
> That is the game's own safety system choosing where a homeless colonist goes, and this mod does not
> override it. Changing it would mean rewriting how the game houses colonists, which is not what a
> bug-fix mod should do.

Owner on the gotcha: *"Explain that its a safety system that we cannot over ride (I know we likely
could but thats a massive rewrite and I am not)."* The arrival-side sibling is [C106](../../bugs/C106.md),
filed and not fixed; do not mention it on the card.

**2. Cut these seven headline lines**, 21 → 14:

| cut | why the owner/QA dropped it |
|---|---|
| Beds stayed reserved for colonists who were never going to take them | the module's own header says the premise narrowed on 1.1.0 (`Fix_StaleReservations.lua:70-86`): vanilla now expires the ordinary case, and the fix is a belt for two residual paths. Players never saw reservations either |
| Drone Hubs paralysed themselves every time an Extender flickered | the fix debounces, it does not stop the rebuild — separated edges still each rebuild (`F77.md:18`) — and "paralysed" outruns the symptom (drone Idle churn). Only card line whose entry still reads PT pending |
| A destroyed tunnel still worked as a shortcut | needs a destroyed tunnel plus a reload; nobody noticed it |
| The Gene Forging research did nothing at all | a hidden trait-draw weight, provable only by console read |
| Two train buildings fought over the same connector hex forever | reads as "track won't connect"; the two salvage lines already cover that cluster |
| The Domes Overview stopped marking domes in trouble | a missing tint in a side panel, and PT-09 found the restored highlight paints Satisfaction red across a mature colony (`F14.md`) |
| An Earth-sent Trade rocket, most often the Wildfire mystery's cure rocket, could get stuck on the landing pad forever | owner, 2026-09-17: long, and just alright |

⛔ The other 14 lines were verified true on 2026-09-17: each has a module in `Code/` that is
registered in `metadata.lua`'s code list, none rests on a retired, parked or opt-in fix. Do not
re-QA them; do not reword them.

**3. Cut the tail sentence** "… and a good deal more, including quieter repairs to drones, shuttles,
domes, rockets, research, storylines and the interface" (plain `:140`, BBCode `:263`). Owner: the
heading already says "some", and the full list is linked.

**4. Move "Still playing on game version 1.0.7?"** (plain `:165-169`, BBCode `:278-279`) to the very
bottom of the card, after "For modders".

Net effect on length: roughly neutral, which is the owner's intent.

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
