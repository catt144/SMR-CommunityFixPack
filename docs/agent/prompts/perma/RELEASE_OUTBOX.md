# Release outbox — player-facing changes staged for the NEXT upload

## Must_Read_Header
<!-- RULES -->
Rule: Append a filled `### Pending` entry whenever a player-facing fix is added, retired, or materially respecified. [A3: pass]
Rule: Do not append a pending entry for a pack-internal fix that never shipped broken. [A3: pass]
Rule: Move every pending entry under `Released in vN` and empty `Pending` only through `release_prompt.md` after upload. [A3: pass]
Rule: Do not delete a pending entry except through a release or with an explicit withdrawal reason. [A3: pass]
<!-- /RULES -->

This ledger tracks every player-facing tree change since the last upload.
`docs/agent/prompts/perma/release_prompt.md` derives `last_changes`, fix-list
rows and the store-card count from it, then moves Pending entries to Released
after upload. `docs/agent/support/RELEASE_SURFACES.md` defines which changes
have a player surface.

**Live tree version:** `metadata.lua` `version` — read it, never hand-set (editor/version rail (`docs/agent/prompts/perma/release_prompt.md` § Release rails)).
**Live count word:** whatever `metadata.lua`'s `description` currently says
(`grep -oE '[A-Z][a-z]+(-[a-z]+)? repairs' metadata.lua` — one hit; zero is a FAIL). Each pending fix that has a
player surface bumps it by one on release.

## Pending — goes out with the next upload

(empty — v10's batch below cleared by `RELEASE.md` §5, 2026-09-13, upload confirmed both portals)

## Released — history, newest first (cleared here by `release_prompt.md`)

### Released in v10 (2026-09-13) — C85, C89, C88 landed; F37, F43+F118, F31 retired
- **C85 · `Fix_CloggedBuildingRelease`** (`59c8c47`) — a building clogged by a dust
  storm never restarted on its own; it now switches back on, on load and once a
  day, and one already stuck in a save recovers on next load. `fixed`,
  desk-controlled; the attended A/B ran checklist 158. Count **+1**.
- **C89 · `Fix_FactionDomeSizeGate`** (`98d0461`), **judgment call** — all five
  factions now use the same ten-colonist rule before disliking a dome's
  unemployment or homelessness (four of five previously counted any dome,
  however small). `cand`/desk-controlled; owner's own A/B is checklist 158, B2's
  panel leg NOT run by ruling. Count **+1**; judgment-call count three to **four**.
- **C88 · `Fix_BuildingCodesPrefab`** (`4dc5073`) — Building Codes now applies its
  maintenance change to buildings deployed from prefabs too, for buildings
  completed after this update (a Paradox developer asked us to carry this until
  their own patch). `fixed`, desk-controlled; attended A/B ran checklist 158.
  Count **+1**.
- **F37 (farm oxygen), F43 + F118 rider (layout research lock), F31** — RETIRED
  and their modules deleted: 1.1.0 handles the salvaged-farm oxygen leak and the
  layout research check itself, and the F31 cave-in map fix repaired a situation
  that cannot arise (`reports/SURFACE_AUDIT_2026-09-12.md`, checklist 156/159).
  Net count change **0** (−3 retired, +3 added) — stays **Forty-nine**.
- Also built, no public row/count change: `Fix_StaleReservations` per-colonist
  `pcall` hardening (queue row 3, ck168); C90's apply-success guards in
  `Fix_SaintBlessing` + `Fix_SinkholeIndestructible` (`reports/C90_GUARDS_BUILD.md`).
- Card: count word **Forty-nine** stays; headliners 21 to **20**; judgment calls
  three to **four**; 5 card copies byte-checked; `README.md`'s six stale claims
  fixed (§3b, checklist 160).
- **Cleared on the owner's word this sitting** (both portals ran): tree
  writeback `version` 10 to **11**, `pdx_version` "8" to **"9"**. Steam subscribed
  archive re-read: `ModContent.fpk` **371,327 B** md5 `bef42a2d5405e06444b7e6efdf28cf38`
  at 00:25 local 09-13, `pack_list.py` counts **56** entries against `pack_predict.py`'s
  **54** — 2 extra non-Code doc entries (`smr-bug-library/SKILL.md`,
  `smr-orientation/SKILL.md`) present in the delivered archive but absent from the
  current source tree, unexplained (see owner report). Paradox has no local
  auto-download to check; its own `pdx_version` bump is the only receipt read.
  §0.5(d) required-game-version field: not offered on the page this upload.

### Released in v9 (2026-09-12) — F59 repaired, F60 retired
- **F59 · `Fix_FreedHousingNotice`** (`3b41d9f`, audited `74b2c8f`) — repair to OUR OWN
  module: the freed-bed notification fired inside larger housing operations (manual
  Set Residence on a full home overfilled it; an expedition boarder could lose the home
  reserved for their return). Deferred until the game's own operation finishes.
  `tested-attended` 2026-09-11 for the manual-assign half only (checklist 152); the
  expedition half is code-only and the change note says so. Count unchanged.
- **F60 · `Fix_DomeFreeSpaceMismatch`** (`9bc4360`) — RETIRED and deleted: 1.1.0's
  admission gate no longer reads the tally it corrected. Count 50 to 49; site row gone
  (`SMR-CommunityMods` `a061665`, still UNDEPLOYED — owner holds the deploy for v10).
- Card: count word **Forty-nine** ×5; `last_changes` = the owner's list shape, header +
  one REPAIRED / RETIRED bullet each (shipped text differs from the tree's draft by the
  owner's box edits — em-dashes, no space after the bullet dash — kept as shipped).
- **Cleared on READ evidence, not the owner's word** (receipts owed, checklist 155):
  Steam changelog newest entry "Update: Sep 11 @ 9:11pm" (Pacific) carries this note
  verbatim; live body "Forty-nine repairs"; workshop pack **337,653 B** md5
  `222b0f60d00319516c1bcc7beeb97491` at 00:25 local 09-12; tree writeback `version` 8 to
  **10** (two saves in the sitting), `pdx_version` "7" to "8", committed stripped inside
  `1583dcd` and restored by merge in the close-out. The Paradox page is unread.

### Released in v8 (2026-09-11) — F119 and C86
- **F119 · `Fix_TradeRocketFuelRefresh`** (`2c68bb1`) — an Earth-sent Trade rocket
  (most often the Wildfire cure rocket) kept its landing-time fuel request after the
  live trip cost changed and could sit on the pad forever; the request is refreshed
  on the pad and a pre-stuck rocket is healed on load. `tested-attended` 2026-09-11
  (checklist 149: fix-off reproduced the reported "20 fuel to unload", the load heal
  and the fix-on leg both left). Count 48 to 49.
- **C86 · `Fix_ScanDowngrade`** (`5ca9a0f`) — an Advanced Orbital Probe fired
  without Adapted Probes no longer knocks a deep-scanned neighbour back to
  "Scanned". `tested-attended` 2026-09-11. Count 49 to 50.
- Card: count word **Fifty**, F119 headliner added; `last_changes` = the two-line
  note plus "watched working on 1.1.0". Judgment-call count unchanged (three).
- **Cleared on READ evidence, not the owner's word** (the session holding the
  v8 close-out ended without running it; closed by the v9 release session, which
  asked for the receipt in checklist 155): the Steam changelog's newest entry,
  "Update: Sep 11 @ 1:50pm", carries this exact note; the live Steam body says
  "Fifty repairs"; the workshop pack (331,428 B, md5 `ec4cfd88d4adfeb24211823972f456d2`)
  landed 16:55 local; the tree carries the writeback (`version` 8, `pdx_version`
  "7"); the site deployed `398a1b0` at 21:10Z. The Paradox page is unread.

### Released in v7 (2026-09-10) — C74+C77 and C83
- **C74 + C77 · `Fix_SilentHitMomentFX`** — the missing animation-moment FX
  restored on seven units: Rare Metals Extractor hammer, classic MOXIE, both
  Water Extractor pumps, Shuttle Hub shuttles, RC Driller, RC Dozer, The
  Excavator. Cosmetic only; the drill Rare Metals skin and the white (CP3) MOXIE
  are silent by design. Metatron deliberately out. Count 46 to 47.
- **C83 · `ArrivalDeaths` extended** — arriving colonists no longer overflow into
  a switched-off, quarantined or unsupplied dome when a working, open, supplied
  dome is reachable. C84 (player-forced homeless move) stays intentional. Count
  47 to 48.
- Card: count word **Forty-eight**, C83 headliner, the owner's "SEVEN MACHINES
  THAT WORKED IN SILENCE" section, three gallery screenshots via
  `screenshot1..3` (description 6,206 chars). `last_changes` = v7's three-line
  note. Judgment-call count unchanged. Both entries `tested-attended` on
  1.1.0.403908.

### Released in v6 (2026-09-09) — hotfix 2, the game-1.1.0 patch
- Nothing passed through *Pending*: the whole release was a chain
  (`docs/archive/prompts/hotfix2/README.md`, every commit by link) and its text link (06)
  wrote the surfaces directly, then link 100 re-swept them after the audit.
- **36 modules DELETED** — game 1.1.0 repairs those defects itself; 36 fix-list
  entries removed (`SMR-CommunityMods` `7cef4f3`), count word Eighty-two to
  **Forty-six**, "Under the hood" four to three, judgment calls six to three.
- **Repaired or re-copied on 1.1.0 bodies:** F114 `TrainCargoDumping`, F115
  `LandscapeUnitFilter`, F116 track salvage, F117 `ArrivalDeaths` (`777249d`),
  F118 rider, `SaintBlessing`, `StaleReservations`, `ShelterReflex` half (b),
  `RocketDroneChurn`, `PayloadTemplateRefill`, `VacuumWalks`; the F95 residue
  pass in `90_SaveSanitizer` (ck126). `last_changes` rewritten wholesale as v6's
  note (five bullets, the last a disclaimer — nothing watched in a running
  colony on 1.1.0). No "Fixed" anywhere; every "works again" is a claim
  until the post-upload sitting.
- New on the card: the "Still playing on game version 1.0.7?" section pointing
  at the frozen v5 build (`v5-game-1.0.7`, ck118).

### Released in v5 (2026-08-30)
- **F110 · `Fix_JumboCaveReinforcementWedge`** — a Jumbo Cave mystery could get
  stuck forever clearing waste rock the drones could not reach, so the
  Reinforcement never built and the mystery never completed. Fix-list row in
  *Story & mysteries*; headliner bullet added; count word Eighty-one to Eighty-two;
  `last_changes` rewritten as v5's change note. Not a judgment call.

*(The v4 release and earlier predate this ledger.)*
