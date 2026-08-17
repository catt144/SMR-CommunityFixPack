# B·02 — the attended check · ⚠️ OWNER AT THE KEYBOARD · ~15 min

Read `README.md`, then `STATE.md`, then this, then `## Notes from upstream` —
01 fills in the real steps there.

## 0 · Staleness check
```
git log --oneline -10
git pull
```
⛔ Do not start if 01 has not filled in §2.

## 1 · 🗒 Live todo list from your first action — and keep the sent/checked/
outstanding ledger so the owner does not have to (`WORKFLOW` co-runs).

## 2 · The queue — decider first

*(01 fills in the specifics.)*

1. ⭐ **`C51`, the decider.** Options → Language → a non-English pack (nine ship;
   **German is the one whose strings we verified**, so it is the cheapest to
   judge). Then: the terraforming overview heading, and a Universal Rocket's
   *Back to Earth* rollover. **Correct = both render in that language.**
   Then switch back.
2. **`C50`.** Start a new game far enough to see the sponsor list; read SpaceY's
   description. **Correct = the Drone Hub command-capacity line is present**, and
   the rest of the bullet list is unchanged and still translated.
3. **Marker gate**, if built. Needs a colony where `DustStormsDisabled` is true —
   observe whether marker dust devils still spawn.
4. **`C35` ride-along** *(no fix involved — evidence only)*: a lander with drones
   on the cargo ramp, Edit Payload, change something, confirm. Chain A's detector
   logs any drone filtered while in `Embark`. ⛔ **This tests nothing of ours** —
   it is the trigger for a vanilla defect whose harm has never been witnessed.

## 3 · Rules for the sitting

1. ⭐⭐ **Relay every owner verbatim through the log-note primitive as it is
   spoken.** A transcript-only quote cannot be re-read by the audit, ever — this
   has already cost the project the provenance of a status grant.
2. **Judge by the log, flushed — not the screen** (corun-pt60).
3. **The owner may reorder live**; that is a feature, and their deviation is
   never scored against the estimate.
4. **Re-confirm every fixture at sitting time.** One has evaporated between prep
   and sitting before, costing 25 minutes.
5. ⚠️ **Language switching is the one step that could look alarming** — the whole
   UI changes. Tell the owner up front that switching back is one setting.

## 4 · Scope fence
**IN:** the four checks, the readings, the owner's verbatims, the log.
**OUT:** ⛔ fixing anything discovered mid-sitting · ⛔ granting statuses (03
weighs those) · ⛔ any `C52` or `C25` work.

## 5 · Stop conditions
- A module reads `inactive` or errors at load → stop that item, bank the rest.
- The language pack does not appear in Options → **that is a finding about the
  install, not about our fix** — record it and skip to item 2.
- Owner wants to stop → stop, bank what ran.

## 6 · ⛔ What may not be claimed
- ⛔ **`tested-attended`** for anything the owner did not personally see resolve.
  One screenshot per claim; no claim without one.
- ⛔ **"Every language works"** from German alone. German is the pack we verified
  at the data level; the others are inference and must be labelled so.
- ⛔ **Any `C35` verdict.** The detector firing proves the forbidden state was
  reached. Whether a drone was *harmed* needs a separate observation, and the
  entry says so.
- ⛔ A status promotion decided in the sitting. Route it to 03.

## 7 · Close-out
One commit: readings on the entries with provenance per row · **owner verbatims
in the archived log** · log archived `git add -f` · outbox to `03_AUDIT` ·
checklist line struck · manifest row struck · `git rm` this file · doccheck GREEN
· grave named · push.

## Notes from upstream
