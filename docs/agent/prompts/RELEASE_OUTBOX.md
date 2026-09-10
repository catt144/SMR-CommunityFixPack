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

### Pending — C74 + C77: restore seven units' missing animation-moment FX

- **Count impact:** +1 player-facing repair / fix-list row (46 → 47 when
  `RELEASE.md` applies the outbox).
- **Fix-list scope:** buildings and vehicles — Rare Metals Extractor hammer,
  classic MOXIE, both Water Extractor pumps, Shuttle Hub shuttles, RC Driller,
  RC Dozer and The Excavator. Cosmetic only; no production or balance change.
- **Change-note line:** Restored the missing strike, pump, landing, drilling,
  shovel and bucket effects on seven machines and vehicles.
- **Required skin note:** the drill Rare Metals Extractor skin and the white
  (CP3) MOXIE are silent by design; changing the extractor to its hammer skin
  exposes the repaired strikes. Screenshots:
  `agent/reports/c74_skins/` (drill default → Change Skin → hammer).
- **Evidence:** `C74` + `C77` are `tested-attended` on 1.1.0.403908; two loads,
  no power cycle, owner heard/saw every intended effect, 0 Lua errors.
- **Judgment-call count:** unchanged. Metatron is deliberately out of scope.

### Pending — C83: keep arriving colonists out of dead domes

- **Count impact:** +1 player-facing repair / fix-list row (47 → 48 after the
  earlier pending C74+C77 entry).
- **Fix-list scope:** passenger-rocket and lander arrivals whose vanilla safety
  fallback is reachable but switched off, quarantined or without life support.
- **Change-note line:** Arriving colonists no longer overflow into a nearby dead
  or quarantined dome when a working, open and supplied dome is reachable.
- **Evidence:** `C83` is `tested-attended` on 1.1.0.403908; the ordinary safe
  route stayed silent, the forced overflow rerouted into the working dome, and
  nobody moved into the bad dome during the following sol; 0 Lua errors.
- **Judgment-call count:** unchanged. C84's player-forced homeless move remains
  intentional and out of scope.

---

## Released — history, newest first (cleared here by RELEASE.md)

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
