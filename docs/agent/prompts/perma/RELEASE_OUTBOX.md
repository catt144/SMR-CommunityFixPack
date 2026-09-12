# Release outbox — player-facing changes staged for the NEXT upload

**What this is.** A running ledger of every change that has landed in the tree
**since the last upload** and must appear on a player surface when the next
version ships. It is the single answer to "what is in the next release?" — the
`last_changes` change note, the new fix-list rows, and the store-card count word
all come from here. `RELEASE.md` reads it, applies every entry to the surfaces,
and **clears it** (moves the entries to *Released* below) once the upload is done.

**Live tree version:** `metadata.lua` `version` — read it, never hand-set (H-02).
**Live count word:** whatever `metadata.lua`'s `description` currently says
(`grep -oE '[A-Z][a-z]+(-[a-z]+)? repairs' metadata.lua` — one hit; zero is a FAIL). Each pending fix that has a
player surface bumps it by one on release.

## How to use it
- **When a player-facing fix lands** (added, retired, or materially re-scoped —
  the `PUBLIC_SURFACE_SWEEP.md` §0.4 test): append a `### Pending` entry below,
  filled in. A pack-internal fix that never shipped broken (the F107 case) gets
  **no entry** — it has no player surface.
- **When the owner is ready to upload:** run `RELEASE.md`. It consumes every
  `### Pending` entry, then rewrites this file with those entries moved under
  *Released in vN* and the *Pending* section empty.
- ⛔ Never delete a pending entry by hand — that silently drops a fix from the
  change note. Retire one only through a release (it moves to *Released*) or by
  recording explicitly why it was withdrawn.

---

## Pending — goes out with the next upload

### Pending — F119 Trade-rocket fuel request refresh

- **F119 · `Fix_TradeRocketFuelRefresh`** (`2c68bb1`) — an Earth-sent Trade
  rocket can keep its landing-time fuel requests after the live trip cost
  changes, leaving surplus fuel nothing unloads or a shortfall no drone fills.
  The staged repair refreshes those requests on the pad and selectively
  refreshes a pre-stuck Trade rocket when a save loads. Player-facing example:
  the Wildfire cure rocket can otherwise wait forever and stop the mystery.
  Count 48 → 49.
- **Status:** **`tested-attended` 2026-09-11** (checklist 149): 11/11 desk demands,
  then in play — fix off for one rocket reproduced the stuck rocket on the real
  Advanced Martian Engines trigger; a save/load of that stuck rocket was healed
  (`refreshed 1`) and it left; fix on re-sized it at once and it left. Not
  covered: the Wildfire loop itself, a player's real save. Entry §Attended check.

### Pending — C86 Advanced Orbital Probe scan downgrade

- **C86 · `Fix_ScanDowngrade`** (`5ca9a0f`) — an Advanced Orbital Probe fired
  without Adapted Probes can change an already deep-scanned neighbouring sector
  back to “Scanned,” inviting a pointless repeat deep scan. The staged repair
  makes the three shipped scan statuses monotonic while preserving equal,
  upward, unknown and foreign-subclass calls. Count 49 → 50.
- **Status:** **`tested-attended` 2026-09-11** (checklist 149): 7/7 desk demands,
  then the probe's own scan call on real sectors kept a deep-scanned sector deep
  and still scanned its neighbour. Fix-off leg desk-only; a real probe object not
  fired. Entry §Attended check.

### Pending — F59 vacancy notification repaired (our own regression)

- **F59 · `Fix_FreedHousingNotice`** (`3b41d9f`, audited `74b2c8f`) — ⚠️ **this is
  a repair to OUR OWN module, not a new game bug.** The fix that offers a freed bed
  to the dome's homeless was firing *inside* larger housing operations that still
  needed the bed. Two harms, both measured at the desk: using **Set Residence** on a
  full home could leave it **over capacity** with the eviction silently undone (both
  game versions, present since the module was written), and a colonist boarding an
  **expedition** could lose the home the game had just reserved for their return
  (1.1.0 only). The repair defers the notification until the game's own operation
  has finished, then re-decides. **Count unchanged** — the fix already exists on the
  fix list and its player-facing description ("A bed that fell vacant sat empty
  while colonists were homeless") is still accurate.
- **Status:** **`tested-attended` 2026-09-11 for the MANUAL-ASSIGN half only**
  (owner granted, checklist 152). In play on 1.1.0, owner at the keyboard: a full
  residence read `residents=14` against `cap=20 closed=6` — no overfill, where the
  unrepaired module reads 15 — and the evicted resident landed in the incoming
  colonist's old bed, a slot that only frees *after* the old fire point, so the
  ordering itself was witnessed. `HasAnyFreeLivingSpace()=false` on the dome proved
  the check was not vacuous. ⛔ **Not covered:** the expedition half (no expedition
  was boarded, still source-derived); the broken side was never run in play; the
  original defect has never been reproduced in a game on either version.
  Desk: 18/18 + 27/27 + 10/10, each with a control that defeats the deferral and
  brings the harms back. Entry: `bugs/F59.md`.
- ⚠️ **For `last_changes`:** worth a player-facing line — the manual-assign harm was
  reachable by an ordinary four-click action and left a visibly wrong resident count.
  Suggested wording: *"Assigning a colonist to a residence that was already full
  could leave that home with more residents than it has beds, and fail to evict the
  colonist it displaced. Fixed."*
- ⛔ **The frozen 1.0.7 download (`v5-game-1.0.7`) still ships the unrepaired body.**
  Owner ruled 1.0.7 stays frozen (ck151 e), so this is knowingly not delivered there.

### Pending — F60 retired (fix removed from the pack)

- **F60 · `Fix_DomeFreeSpaceMismatch`** (`9bc4360`) — **RETIRED and DELETED** by
  owner ruling (checklist 151 a / 152 b). On game 1.1.0 the admission gate stopped
  reading the housing tally this fix corrected — `Community:HasFreeLivingSpaceFor`
  iterates residences directly — so the fix no longer repaired births or migration,
  and what it still changed (the launch housing estimate) it changed *optimistically
  against the gate*, i.e. it could promise room the game would then refuse.
  Historically correct on 1.0.7 and left on the record as such.
  **Count 50 → 49.** ✅ Already applied: `items.lua` + `metadata.lua` code list
  (`9bc4360`), count word in all five copies (`0392162`), fix-list entry removed
  (`SMR-CommunityMods` `a061665`).
- **Status:** desk-controlled (16/16) and source-verified; **no player outcome was
  measured** — the control is an enabled-but-unpowered residence plus a passenger
  rocket, and nobody ran it. The ruling was taken on the source position.
- ⚠️ **For `last_changes`:** a retirement is a player-facing change — the count drops
  and a listed fix disappears. Suggested wording: *"One older fix has been retired:
  the game's own 1.1.0 changes made the dome housing-total repair unnecessary, so it
  has been removed rather than left to change numbers it no longer corrects."*
- ⚠️ **Loose end, not release-blocking:** the TestKit probe `DomeFreeSpaceMismatch`
  (`30_Probes_Wave3.lua`) still targets the deleted module and will fail on the next
  kit run. TestKit is local-only by design.

---

## Released — history, newest first (cleared here by RELEASE.md)

### Released in v7 (2026-09-10) — C74+C77 and C83
- **C74 + C77 · `Fix_SilentHitMomentFX`** — the missing animation-moment FX
  restored on seven units: Rare Metals Extractor hammer, classic MOXIE, both
  Water Extractor pumps, Shuttle Hub shuttles, RC Driller, RC Dozer, The
  Excavator. Cosmetic only; the drill Rare Metals skin and the white (CP3) MOXIE
  are silent by design. Metatron deliberately out. Count 46 → 47.
- **C83 · `ArrivalDeaths` extended** — arriving colonists no longer overflow into
  a switched-off, quarantined or unsupplied dome when a working, open, supplied
  dome is reachable. C84 (player-forced homeless move) stays intentional. Count
  47 → 48.
- Card: count word **Forty-eight**, C83 headliner, the owner's "SEVEN MACHINES
  THAT WORKED IN SILENCE" section, three gallery screenshots via
  `screenshot1..3` (description 6,206 chars). `last_changes` = v7's three-line
  note. Judgment-call count unchanged. Both entries `tested-attended` on
  1.1.0.403908.

### Released in v6 (2026-09-09) — hotfix 2, the game-1.1.0 patch
- Nothing passed through *Pending*: the whole release was a chain
  (`prompts/hotfix2/README.md`, every commit by link) and its text link (06)
  wrote the surfaces directly, then link 100 re-swept them after the audit.
- **36 modules DELETED** — game 1.1.0 repairs those defects itself; 36 fix-list
  entries removed (`SMR-CommunityMods` `7cef4f3`), count word Eighty-two →
  **Forty-six**, "Under the hood" four → three, judgment calls six → three.
- **Repaired or re-copied on 1.1.0 bodies:** F114 `TrainCargoDumping`, F115
  `LandscapeUnitFilter`, F116 track salvage, F117 `ArrivalDeaths` (`777249d`),
  F118 rider, `SaintBlessing`, `StaleReservations`, `ShelterReflex` half (b),
  `RocketDroneChurn`, `PayloadTemplateRefill`, `VacuumWalks`; the F95 residue
  pass in `90_SaveSanitizer` (ck126). `last_changes` rewritten wholesale as v6's
  note (five bullets, the last a disclaimer — nothing watched in a running
  colony on 1.1.0). ⛔ No "Fixed" anywhere; every "works again" is a claim
  until the post-upload sitting.
- New on the card: the "Still playing on game version 1.0.7?" section pointing
  at the frozen v5 build (`v5-game-1.0.7`, ck118).

### Released in v5 (2026-08-30)
- **F110 · `Fix_JumboCaveReinforcementWedge`** — a Jumbo Cave mystery could get
  stuck forever clearing waste rock the drones could not reach, so the
  Reinforcement never built and the mystery never completed. Fix-list row in
  *Story & mysteries*; headliner bullet added; count word Eighty-one → Eighty-two;
  `last_changes` rewritten as v5's change note. Not a judgment call.

*(The v4 release and earlier predate this ledger.)*
