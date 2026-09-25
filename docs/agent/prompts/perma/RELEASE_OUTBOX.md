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

### Pending — C114 Colonists on a passage hub can reach the dome beside it (2026-09-24)

**No hold: the hub set is merged and audited** (`docs/agent/reports/HUBSET_AUDIT_2026-09-24.md`,
merge `8cb1727`). Desk harness `tools/desk_c114_hub_access.py` (25 of 25 demands, five
module-removed controls). In game (07B, 2026-09-24, instrument-read on both builds): with the fix
off a colonist on PassageHub(2692) was booked a shuttle rescue home; with the fix on the same
shape walked into a dome unbooked (C114 `tested-unattended`).
Source of the report: a player's save (TheGodUncle) and the hub source audit, 2026-09-24.

C114 is a new public row:

> A colonist standing on a passage hub, or crossing a passage attached to one, next to a large
> dome is no longer judged unable to reach that dome and sent a shuttle rescue home instead of
> walking the passage. The game measured reach to the dome's centre, which a large dome puts out
> of range even from its own hub.

Developer detail: `Colonist:HasLocalAccess` falls back to `DefaultOutsideWorkplacesRadius` (20
hexes) measured to the destination's centre (`ColonistTransport.lua:293-299`). The pack widens a
false result only when the colonist is physically on a live hub or in flight on one of its
passages and a hub-linked dome's network contains the destination; every native true answer and
every home-relative query stays native. Passages attached to a hub only.

### Pending — C115 An obsolete rescue pickup no longer pulls a colonist back outside (2026-09-24)

**No hold: merged and audited.** Desk harness `tools/desk_c115_home_rescue.py` (12 PASS; the
module-absent control fails the fixed demand). Not exercised in play: the 07 sitting found no
own-home rescue at load in either build (C115 `fixed`).
Source of the report: a player's save (TheGodUncle) and the hub source audit, 2026-09-24.

C115 is a new public row:

> A shuttle rescue booked while a colonist was crossing a passage kept its pickup point out on
> the passage. A colonist who then reached home on foot walked back out to that pickup, and could
> suffocate waiting. A rescue to the colonist's own dome is now cancelled at the dome instead.

Developer detail: the pickup anchor is taken once at booking (`LRTransport.lua:106-123`) and
`Colonist:Transport` walks to it without rechecking home (`Colonist.lua:3963-4013`). At Transport
start, an uncommitted own-home task whose colonist already stands inside that dome is cleaned up
through the task's native `Cleanup`; every other ride enters native Transport unchanged.

### Pending — C116 A colonist's hub marker is cleared once it has left the hub (2026-09-24)

**No hold: merged and audited.** Desk harness `tools/desk_c116_hub_marker.py` (11 PASS; the
module-removed control keeps the stale marker). Not exercised in play: no colonist walked off a
hub with a stale marker during the sittings; the ramp-shelter reading held on both builds
(C116 `fixed`; harm conditional).
Source of the report: the hub source audit and a player's save (TheGodUncle), 2026-09-24.

C116 is a new public row:

> The marker that shelters a colonist while it stands on a passage hub could outlive its stay
> there, so a colonist who had walked away from the hub was still treated as sheltered. The marker
> is now cleared once the colonist has physically left the hub, and outside conditions apply again.

Developer detail: `PassageBase:TraverseTunnel` clears `passage_hub` only on a dome-side exit
(`Passage.lua:1231-1235`). The pack observes synchronous movement and holder transitions and
clears the marker, and a stale hub holder, only after both the logical and the visual position
have left the hub hex; a live traversal always keeps shelter. Existing saves heal on the next
movement; no load-time sweep.

### Pending — C117 Salvaging a busy hub passage lets its colonists arrive first (2026-09-24)

**No hold: merged and audited.** Desk harness `tools/desk_c117_hub_salvage.py` (21 of 21 demands,
fix-removed and old-shape controls). In game (07B, 2026-09-24, log-read on both builds): with the
fix off, 43 of 43 colonists crossing a salvaged spoke landed on the hub without holder or marker;
with the fix on, 0 of 37 (C117 `tested-unattended`).
Source of the report: the hub source audit, 2026-09-24.

C117 is a new public row:

> Salvaging a hub passage that still had another exit disconnected it while colonists were
> crossing it, leaving them outside at the hub end. Crossing colonists now arrive before the
> passage disconnects, and no new colonist enters a passage being salvaged while another exit
> exists.

Developer detail: `WouldStrandHubColonists` returns false as soon as a sibling tunnel is active
(`Passage.lua:1134-1136`), so `OnDemolish` disconnects before its traverser wait. The pack keeps
the pre-disconnect wait alive while valid traversers remain and refuses fresh entries only while
a usable sibling exists; the last exit keeps native behaviour.

### Pending — C111 A rescue back to the colonist's own dome says so (2026-09-24)

**No hold: merged, audited and owner-watched.** Desk harness `tools/desk_c111_rescue_text.py`
(11 PASS; `--without-fix` fails). In game (07B, 2026-09-24): the owner watched the info panel
read "Returning to Dome: Brussels" on a colonist whose home is Brussels; on the unfixed build the
same colonist read "Moving to a new Dome: Brussels" (C111 `tested-attended`). Wording approved by
the owner (2026-09-24).
Source of the report: the migration source audit, 2026-09-24.

C111 is a new public row:

> A shuttle rescue that brings a colonist back to its own dome no longer reads "Moving to a new
> Dome" followed by the dome it already lives in. It reads "Returning to Dome" with the same link.
> Real moves to a new dome keep their original text.

Developer detail: `Transport`, `TransportByFoot` and `MigrateStep` share one command text
(`Colonist.lua:4647-4649`). The pack wraps the synchronous UI getter only, for a task with no
source dome or migration destination whose destination is the colonist's home. The new line is
`Untranslated`, so it is English in every language until the pack ships its own translations.

### Pending — F127 The pack's arrival reroute now moves the bed reservation with the colonist (2026-09-24)

**No hold: merged and audited; desk-verified by the owner's scope cut.** Desk harness
`tools/desk_f127_arrival_booking.py` (12 of 12 demands; the reserve-only old shape fails on a
full habitat; `desk_c83_arrivals.py` still 12 of 12). Our own defect in the C83 fix that shipped
in earlier releases; no reporter.

F127 respecifies the existing C83 row; it is not a new public row. Change-note line:

> When new arrivals are redirected from a dome that cannot take them to one that can, the bed
> reserved for them in the first dome is now released. Before, that bed stayed reserved and sat
> empty.

Developer detail: the C83 reroute in `Fix_ArrivalDeaths.lua` called `ChooseDome` for a new
destination but left `reserved_residence` pointing at the rejected dome. It now cancels that
booking before reserving in the new destination, so a full habitat cannot keep an orphaned slot.

## Last released

**v15** (2026-09-23). Its entry and every earlier release are in
`docs/archive/RELEASE_HISTORY.md`, oldest first.
