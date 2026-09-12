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

*(empty — cleared 2026-09-12 by the v9 close-out; the next batch is the **Held** section below)*

---

## Held — still-needed follow-through AFTER v9, not Pending

**Do not consume this section in the v9 change note/upload.** It records review
proposals, not landed player-facing changes. Pending F59/F60 above is unchanged.
Audit `reports/STILL_NEEDED_SWEEP.md` (2026-09-12): 46 reviewed; **2 RETIRE,
0 REBUILD, 30 KEEP, 14 KEEP-BUT-FIX-CLAIM**. No module/public changes were applied.

**✅ 2026-09-12: v9 is closed and checklist 156 is RULED** — retire F37 and F43 (+F118
rider), frozen 1.0.7 build untouched, wording batch approved with the owner's
corrections. ⚖️ **The text to apply is `reports/still-needed/WORDING_RULED.md`**, not
`SURFACE_PLAN.md`, and its VOICE RULE binds. F21 STAYS (panel line, source-settled
there); F31 and F52 are HELD. **TAKEABLE WHEN** `prompts/SURFACE_AUDIT_FABLE.md` has
reported and the owner has ruled on anything it moved. Then run PUBLIC_SURFACE_SWEEP
in full, apply, and turn this section into the Pending entries for v10.

- **Retirement candidates:** F37 ordinary farm oxygen leak is cleared by current
  vanilla working transition; F43 normal layout admission already has the outer
  research/prefab gate. F118 rider follows its parent. Owner decides 1.0.7/orphan/
  custom/race scope; no all-routes or fresh player-cure proof.
- **Retained claim batch:** F54 dust-storm example; Saint dome/Religious scope;
  F58 ordinary-foot cleanup/actual age tests/headline; F52 available-passage
  headline/intro (INFERRED wording risk); F21 obsolete Comfort example -> train/
  track statistics; F34 drones rather than colonists; F77 two-second grouping/
  registered title; F30 obstruction-clearing constructor exemption/eligible
  command rescue; F06 ten-sol window/title; F50 interruption rather than universal
  long-trip impossibility; F40 dormant/historical target scope; F48 corrected
  vanilla migration/historical latch/limited rollback; F31 insurance rather than
  unconfirmed stopped-story account. Exact review text: `reports/still-needed/SURFACE_PLAN.md`.
- **Aggregates:** current tree49 rows/46 modules/47 Code/21 headlines. Retirement
  choices predict49 ->48(one) ->47(both); derive actual final counts once.
  Current-data-hidden claim supports **two**, not three, rows (F57a and F29, not
  subfix counting); judgment rows still3, Lake key ships, seven-machine scope true.
  Full proposed F31+F37 headline removal gives19; headlines are not repair count.
- **All maintained copies:** metadata description, both STORE_CARD_LIVE blocks,
  both UPLOAD_WORKFLOW backups, complete site rows and FAQ/editorial tallies.
  Recheck intro examples/categories, not only bullets. No live body/deploy read
  was made by the audit; execute owner's upload -> cards -> site order on release.
- **F46:** native suspended Station demand remained positive2500, flags restored
  exactly. KEEP, no new row/count request; actual unloading/route cure not witnessed.
- **Change note:** one plain line per actually changed fix, tagged appropriately;
  a wording correction is not a new game repair or an attended witness. Existing
  metadata version10/pdx8 writeback predates this sweep and is untouched; never
  hand-set versions or infer upload receipt from it.

---

## Released — history, newest first (cleared here by RELEASE.md)

### Released in v9 (2026-09-12) — F59 repaired, F60 retired
- **F59 · `Fix_FreedHousingNotice`** (`3b41d9f`, audited `74b2c8f`) — repair to OUR OWN
  module: the freed-bed notification fired inside larger housing operations (manual
  Set Residence on a full home overfilled it; an expedition boarder could lose the home
  reserved for their return). Deferred until the game's own operation finishes.
  `tested-attended` 2026-09-11 for the manual-assign half only (checklist 152); the
  expedition half is code-only and the change note says so. Count unchanged.
- **F60 · `Fix_DomeFreeSpaceMismatch`** (`9bc4360`) — RETIRED and deleted: 1.1.0's
  admission gate no longer reads the tally it corrected. Count 50 → 49; site row gone
  (`SMR-CommunityMods` `a061665`, ⚠️ still UNDEPLOYED — owner holds the deploy for v10).
- Card: count word **Forty-nine** ×5; `last_changes` = the owner's list shape, header +
  one REPAIRED / RETIRED bullet each (shipped text differs from the tree's draft by the
  owner's box edits — em-dashes, no space after the bullet dash — kept as shipped).
- ⚠️ **Cleared on READ evidence, not the owner's word** (receipts owed, checklist 155):
  Steam changelog newest entry "Update: Sep 11 @ 9:11pm" (Pacific) carries this note
  verbatim; live body "Forty-nine repairs"; workshop pack **337,653 B** md5
  `222b0f60d00319516c1bcc7beeb97491` at 00:25 local 09-12; tree writeback `version` 8 →
  **10** (two saves in the sitting), `pdx_version` "7" → "8", committed stripped inside
  `1583dcd` and restored by merge in the close-out. The Paradox page is unread.

### Released in v8 (2026-09-11) — F119 and C86
- **F119 · `Fix_TradeRocketFuelRefresh`** (`2c68bb1`) — an Earth-sent Trade rocket
  (most often the Wildfire cure rocket) kept its landing-time fuel request after the
  live trip cost changed and could sit on the pad forever; the request is refreshed
  on the pad and a pre-stuck rocket is healed on load. `tested-attended` 2026-09-11
  (checklist 149: fix-off reproduced the reported "20 fuel to unload", the load heal
  and the fix-on leg both left). Count 48 → 49.
- **C86 · `Fix_ScanDowngrade`** (`5ca9a0f`) — an Advanced Orbital Probe fired
  without Adapted Probes no longer knocks a deep-scanned neighbour back to
  "Scanned". `tested-attended` 2026-09-11. Count 49 → 50.
- Card: count word **Fifty**, F119 headliner added; `last_changes` = the two-line
  note plus "watched working on 1.1.0". Judgment-call count unchanged (three).
- ⚠️ **Cleared on READ evidence, not the owner's word** (the session holding the
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
