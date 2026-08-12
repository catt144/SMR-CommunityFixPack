# Trains — the costed route to ship-ready (PT-60 audit deliverable, 2026-08-12)

> ✅ **RULED 2026-08-12, same day — the owner chose OPTION A: the train group
> ships at `fixed` and the verification queue is CLOSED** (checklist item 12).
> No future chain may propose a train leg; F80's symptom-triggered tap is the
> only surviving ask. Decided alongside the pre-release freeze of the whole
> `fixed`→`tested` campaign (checklist item 14). ⭐ Inventory correction from
> the audit review: **F65 and F66** (station↔tunnel grid + connector, both
> `tested`) belong to this group too — 17 entries, not 15, and two more of
> them keyboard-verified than the table below counts.

**Why this exists.** Owner ask, mid-`corun-pt60` sitting (checklist item 12):
*"a route that moves the train items into the ready-to-ship column, instead of
every chain re-proposing a train leg."* The sitting recorded two framing
corrections that bind here: **nothing train-related blocks the release today**
(F21 ships as `fixed`; PT-62's remainder is explicitly NOT a release gate), and
**C42 is not a train item** (it is dome passages; it merely shared F21's
missing-instrument skip reason). ⛔ The standard question — is `fixed` enough
to ship, or is owner-witnessed `tested` wanted first — **belongs to the owner**;
this report only prices each answer.

## The inventory, so nobody recounts it

Fifteen train/track/platform entries. **Done or closed (7):** `tested` F44 ·
F45 · F46 · F47; `fixed*` F49 ((d) tested, (c) wontfix, (a) guard stripped —
nothing owed); `wontfix` F62 · F79. **Open (3):** F80 `investigating` · F99
`filed` (rate) · C45 `filed` (rate). **`fixed`, never owner-witnessed (5):**
F11 · F21 · F48 · F64 · F91 — these five are the "ready-to-ship column"
question.

## Per-item: what a `tested` grant would need, and what it costs you

| item | the read it would take | organic or forced? | attended cost | honest ceiling |
|---|---|---|---|---|
| **F11** (platform wedge) | an organic wedge, then the wrapper seen releasing it | ⛔ **no demonstrated producer** — your own 08-10 ruling (trigger A refuted at the keyboard); 08-04 already witnessed 7 trains / 340 removals / 0 wedges | **cannot be bought at any price** | ships `fixed` |
| **F21** (wait-time penalty) | you watching one boarding while the 08-10 reader shows `start_wait` restamp (`spent_time_sum`/`spent_time_values`) — the restamp was already WITNESSED organically 08-10; only your spoken verdict is missing | organic boarding, forced instrument | ⭐ **~10–15 min** on a staged `TEST2H TRAIN` copy | `tested` is buyable |
| **F48** (station connectors) | the repair is invisible by design — it prevents a state; the only artifact is a log line, and a log-only sign-off is ceremony (house rule) | n/a | **cannot be bought honestly** | ships `fixed` — now with 08-12 organic execution evidence (3 of 7 tracks repaired in YOUR campaign, repair persisted through save/reload) |
| **F64** (prefab leak) | demolish a station, watch the train survive into storage (pre-fix behaviour family-witnessed by you 08-01) | stageable | ⭐ **~5–10 min**, same fixture, same sitting as F21 | `tested` is buyable |
| **F91** (shell wipe) | the heal firing on REAL shells — but no save carrying shells exists, and the pack itself now prevents their creation; PT-60 read a controlled zero (0 of 7 tracks, both loads) and the probe covers the mechanism | ⛔ **forced-only forever** | **cannot be bought** | ships `fixed` |
| **F80** (skipped passengers) | the tap when the symptom appears in YOUR game, before you mitigate (exact predicate known: `TrainTransport.lua:374`) | organic-only, symptom-gated | **0 scheduled** — ~5 min when it fires | stays `investigating`; not a ship blocker |
| **F99 / C45** (rate items) | whole-log watch on every archived log (PT-60 audit: 0 hits for both) | log-side | **0** | stay `filed` |

## The route, then — one decision, two options

* **Option A — ship the train group at `fixed`.** Zero attended minutes. F11,
  F48, F91 are at their honest ceiling anyway; F21 and F64 ship on mechanism +
  witnessed-instance evidence. F80/F99/C45 stay as watches. The train queue
  CLOSES: no future chain may propose a train leg, only the F80 tap if its
  symptom arrives.
* **Option B — buy the buyable two first.** One **~20–30 min rider block**
  (F21 boarding-watch + F64 demolish-watch) on any co-run that stages
  `TEST2H TRAIN` — **the natural host is the PT-20 redo already queued**, so
  this costs a longer sitting, not a new one. Then ship; everything else as
  option A.

Either answer ends the recurring ask. **Recommendation: option B folded into
the PT-20 redo** — it converts the two entries where your eyes actually add
information, at rider price, and leaves nothing a future chain could
legitimately re-open. The decision itself stays yours (checklist item 12).
