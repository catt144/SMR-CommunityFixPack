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

⚠️ Three entries below, all landed 2026-09-12 by `prompts/C85_C88_BUILD.md`. They ride v10 **together with** the Held batch — do not ship them separately, and re-derive every count at apply time.

### Pending — C85 · `Fix_CloggedBuildingRelease` (`59c8c47`, 2026-09-12)

**`last_changes` bullet (owner's list style, one line, `NEW`):**
> NEW: a building left "Clogged after a Dust Storm." is switched back on — including one that is already stuck in your save.

**Fix-list row (voice rule: what it does and for whom).**
- *What you saw:* an extractor or factory stopped after a dust storm, said "Clogged
  after a Dust Storm.", and never started again — destroy and rebuild was the only
  way out. Two players reported it.
- *What was wrong:* the dust-storm event switches the building off before it asks you
  what to do, and if that question is ever lost — a save and reload while it is on
  screen, for instance — nothing switches the building back on. The game already has
  the timer that would have done it; this event does not use it.
- *After the fix:* the building is switched back on, on load and once a day. A
  building that is already stuck in your save recovers the next time you load it.
  A building still waiting on your answer, or waiting because you chose "we'll fix it
  after the storm", is left alone.

Count impact **+1**. Judgment-call count unchanged.
⚠️ Status is `fixed`, desk-controlled — **not** a playtest word. The attended A/B is
checklist 158 and has not run. Entry: `bugs/C85.md` (2026-09-12 section) carries every
limit, including the one case deliberately not repaired (an armed "fix it after the
storm" follow-up that never gets its storm).

### Pending — C89 · `Fix_FactionDomeSizeGate` (`98d0461`, 2026-09-12) ⚖️ JUDGMENT CALL

⚖️ **This is a judgment call, not a repair of a code error, and every surface must say
so the way F40 and F73 do** (owner, 2026-09-12): the site row uses the `??? question`
block with "— *judgment call*" in the headline and the "⚠️ Worth knowing: this one is a
judgment call" paragraph; the **FAQ judgment-call count goes three → four in all three
places** (`PUBLIC_SURFACE_SWEEP.md` §6); the card's judgment-call sentence is updated
if it lists them by name. ⛔ Nothing here may be worded as "the game was wrong".

**`last_changes` bullet (owner's list style, one line, `NEW`):**
> NEW: all five factions now use the same ten-colonist rule before they dislike a dome's unemployment or homelessness (judgment call).

**Fix-list row.**
- *What you saw:* a faction turning on you over "unemployment" in a dome of a handful
  of colonists that was still being built, with nobody unemployed in the colony.
- *What was wrong:* four of the five factions count any dome, however small, so one
  idle colonist in a dome of three is "more than 10% unemployment". The Justice
  Movement's identical dislike waits until a dome has ten colonists.
- *After the fix:* all five use the same ten-colonist rule, for homelessness too.

Count impact **+1**. **Judgment-call count three → four.**
⚠️ Status on the defect question stays `cand` — it is a judgment call. The module is
desk-controlled and has **not** run in a game: 🎮 the owner flagged C89 for an A/B they
will observe themselves, `tested-attended` is theirs to grant, and the recipe is
checklist 158. Entry: `bugs/C89.md`.

### Pending — C88 · `Fix_BuildingCodesPrefab` (`4dc5073`, 2026-09-12)

**`last_changes` bullet (owner's list style, one line, `NEW`):**
> NEW: the Building Codes law now applies to buildings deployed from prefabs, as its description says — for buildings completed after this update.

**Fix-list row.**
- *What you saw:* with Building Codes enacted, a building deployed from a prefab kept
  ordinary maintenance — under Strict it never got the lower maintenance the law
  promises.
- *What was wrong:* both versions of the law skip prefab-deployed buildings, and
  neither description mentions it.
- *After the fix:* prefab-deployed buildings get the same maintenance change as any
  other, at whatever value the law is set to. This applies to buildings completed
  after this update.

⚖️ **Worth saying on the row, because it is the strongest thing we can say:** a Paradox
developer answered the reporter's thread — excluding prefabs is wrong, it is fixed in
their next patch, and they asked us to carry the fix meanwhile. When their patch lands
this fix stands itself down on its own.

Count impact **+1**. Judgment-call count unchanged.
⚠️ "Applies to buildings completed after this update" is a **scope statement, not a
hedge** — keep it. Buildings already standing cannot be repaired: the game does not
record that a finished building came from a prefab. Status is `fixed`, desk-controlled;
the attended A/B is checklist 158. Entry: `bugs/C88.md`.

### ⛔ Notes for whoever runs `RELEASE.md` on this batch

- **Re-derive every count.** These three are **+3** on the fix count, but the Held
  section above retires F37, F43 (+F118 rider) and — per
  `reports/SURFACE_AUDIT_2026-09-12.md` — possibly **F31**, so the net is not +3.
  Read the live count word and `doccheck --emit-counts` at apply time; never carry a
  number from here.
- **Judgment-call count: three → four**, in all three places, for C89 only.
- ⚠️ **`deskbench` has one REFUTED row that is not part of this batch and is
  pre-existing since `9bc4360` (09-11):** `tools/desk_migration_cluster.py` still
  loads `Code/Fix_DomeFreeSpaceMismatch.lua`, which F60's retirement deleted.
  Confirmed by running it at `59c8c47^`. It needs repairing before `deskbench` can be
  read as a release signal — otherwise a real failure hides behind a known one.
- **Two new candidate entries were filed by this build and neither is a player
  surface:** `C90` (a defect in the pack's own core — a declined `DataPatch`
  self-check still patches shipped data; reaches `Fix_SaintBlessing` and
  `Fix_SinkholeIndestructible`) and `C91` (vanilla leaks the Building Codes
  maintenance modifier on repeal; a dev-report candidate). Neither gets an outbox
  entry; both want owner attention separately.

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
