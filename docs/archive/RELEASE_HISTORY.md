# Release history — every upload's player-facing changes

Append-only. `docs/agent/prompts/perma/release_prompt.md` appends one
`### Released in v<N> (date)` section here when it closes a confirmed upload,
so the newest release is LAST. The outbox keeps only what has not shipped.

Moved here from `RELEASE_OUTBOX.md` on 2026-09-16 on the owner's word: every
block below is verbatim, reordered oldest first.

*(The v4 release and earlier predate this ledger.)*

### Released in v5 (2026-08-30)
- **F110 · `Fix_JumboCaveReinforcementWedge`** — a Jumbo Cave mystery could get
  stuck forever clearing waste rock the drones could not reach, so the
  Reinforcement never built and the mystery never completed. Fix-list row in
  *Story & mysteries*; headliner bullet added; count word Eighty-one to Eighty-two;
  `last_changes` rewritten as v5's change note. Not a judgment call.

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

### Released in v11 (2026-09-16) — C93, C95, C96 landed
- **Card:** count word **Forty-nine → Fifty-two** (site `^??? ` rows = 52, section tally sums);
  headliners 20 → 21 (C93's ranch bullet); judgment calls four → **five** (C95) in `faq.md`,
  the fix-list marker and `index.md` (which had still said three). Site commit `74a336e`, words
  commit `e2df30a`.
- **Shipped `last_changes` is the owner's box text**, not the tree draft: it names the RC Generator
  as covered (desk-covered by the suite; never flown) and drops the "one way only" clause. Kept as
  shipped, as at v9.
- **Cleared on the owner's word ("uploaded", 2026-09-16) plus READ evidence:** Steam changelog
  newest entry "Update: Sep 16 @ 2:27pm" carries the shipped note; live Steam body reads
  "Fifty-two repairs" (0 "Forty-nine"). Tree writeback `version` 11 → **14** (three saves),
  `pdx_version` "9" → **"10"**, `code_hash`/`saved` rewritten; comments stripped in both files and
  restored in the close-out commit. **Paradox page shows v13** (owner, 2026-09-16; Steam shows no
  version) — one below the tree's 14, consistent with `VersionDisplayName` being sent before
  Paradox's own save bumps it (`ParadoxMods.lua:156`, `:173`). ⚠️ **Receipt gap at close:** the
  **site was NOT published** — newest `Publish docs site` run is `d86a347`
  (2026-09-13) and the live fix list read 49 entries with no ranch row at 17:30 local, so the
  card's Fifty-two disagrees with the page it links until the owner runs the workflow.

The three staged entries, moved here verbatim:

#### C95 habitat expedition draft (staged 2026-09-16)

- **C95 · `Fix_HabitatExpeditionDraft`**, main-pack **judgment call**, authorized
  by ck185. ✅ **`tested-attended` 2026-09-16**: the automatic-draft repair passed with the
  owner watching (ck189 CLOSED). The lander and space-elevator player-choice controls stay
  **desk-verified, not playtested**, by the owner's ruling recorded in ck189.
- Automatic expedition drafts leave Naturalist and Micro-G habitat residents
  at home; deliberate player transfers and lander passenger choices remain.
  Forward-only: residents already away are not rescued.
- Fix-list row, judgment-call reasoning and FAQ are drafted in
  [the build report](../../reports/C95_HABITAT_DRAFT_BUILD.md#public-copy-draft--for-the-release-pass).
  Release pass derives the public count from its actual row set. No version bump,
  store edit, upload or publication was performed by this build.

#### C93 Outside Ranch stockpiles under Open Domes (staged 2026-09-16)

- **C93 · `Fix_OpenPastureStockpiles`**, main pack, **plain repair** — the entry records no
  judgment call. Ship ruled by the owner 2026-09-16 (recorded in ck185: *"Both of those, and
  both of the ones we are setting up to test right now are the planned fixes"*).
- **What players saw:** once the Open Domes law passes, an Outside Ranch left three of its
  nine stockpiles where drones could not reach them, so that share of its output was never
  collected. The ranch works normally before the law.
- **What changes:** the Outside Ranch keeps the model that has all nine stockpile spots, and
  a ranch already affected in a save recovers its stranded piles on load. No resource is
  created, moved or lost.
- ⚠️ **State the visible tradeoff publicly:** under Open Domes an Outside Ranch keeps its
  closed look. Atmosphere, consumption and every other effect of the law are unchanged.
- ✅ **Verification — `tested-attended` 2026-09-16:** the owner reloaded an affected save and
  watched the repair end to end — stranded piles reattached, drones cleared them, no food stuck
  (checklist 191 CLOSED). It may be described as watched working in a running colony. ⛔ Do not
  claim a newly built ranch was tested (not stated).
- No public-copy draft exists. Authority: [C93](../../bugs/C93.md) and
  [the build report](../../reports/C93_RANCH_OPEN_DOMES_BUILD.md).

#### C96 RC Seeker and other rover subclasses on expeditions (staged 2026-09-16)

- **C96 · `Fix_RoverSubclassManifest`**, main pack, **plain repair** — the entry records no
  judgment call. Ship ruled by the owner 2026-09-16, ck185 (b).
- **What players saw:** an expedition asking for an RC Commander refused an RC Seeker with
  "Not enough Rovers", although the Seeker is a Commander model. A Europe colony whose only
  rover was a Seeker could never send that expedition. The same refusal applied to every RC
  rover model built on another one.
- **What changes:** a rover model now fills a request for the rover type it is built on, and
  the cargo panel shows the rover actually loaded (for example *Seeker 1/1*). It works one
  way only — an expedition asking for a Seeker still refuses a plain Commander — and a colony
  that owns the exact rover keeps the game's own choice. When the only matching rover is
  busy, the panel now says "Rovers are busy" instead of showing no warning.
- ✅ **Verification — `tested-attended` 2026-09-16:** watched in a running colony on 1.1.0 —
  the expedition launched with the Seeker aboard (cargo Seeker 1/1, Commander 0/0) and came back
  with the same single Seeker; the owner counted one before, none while away, one after. It
  may be described as watched working. ⛔ Do not claim the RC Generator was flown (desk only) or
  that removing the pack mid-expedition was tested.
- No public-copy draft exists. Authority: [C96](../../bugs/C96.md) and
  [the build report](../../reports/C96_ROVER_SUBCLASS_BUILD.md).

### Released in v12 (2026-09-17) — C95 reworked into a repair, C102 landed, card cut to 14 headliners

- **Card:** count word **Fifty-two → Fifty-three** (site `^??? ` rows = 53, section tally
  2+16+4+6+9+6+6+2+2 sums); headliners **21 → 14** on the owner's store-card task (seven cuts, each
  reason recorded below); a new FEATURED section for C95 from the owner's approved draft; the
  "… and a good deal more" tail sentence cut; the 1.0.7 section moved to the very bottom. Judgment
  calls **five → four** as C95 leaves the class, in `faq.md` (three places), the fix-list marker and
  `index.md`. Site commit `c5ac193`, words commit `a426d73`.
- **Shipped `last_changes` is the owner's box text**, not the tree draft — the third time, after v9
  and v11. The line *"Not watched yet: a crew that comes home by train."* is at `16445b6` and absent
  from the writeback. Kept as shipped. ⚠️ The outbox ruled that the public words say plainly that
  neither the train return nor the live C102 reroute was watched; C102's sentence survived and C95's
  did not, so that half of the disclosure now lives only on the fix-list row, not on the storefront.
- **Cleared on the owner's word ("uploaded", 2026-09-17) plus tree evidence:** writeback `version`
  14 → **16** (two saves), `pdx_version` "10" → **"11"**, `code_hash` and `saved` rewritten; comments
  stripped from both files (389 and 52 lines) and restored from `16445b6` with every written-back
  value kept.
- ⛔ **Not verified at close, and not claimed:** the Paradox page version was not stated, and the
  site is **NOT published** — the newest `publish-site.yml` run is #11 (2026-09-16, `74a336e`, which
  is v11's fix list), so the store card reads Fifty-three while the deployed fix list still shows 52
  rows and still marks the habitat row a judgment call. Same gap as the v11 close.

#### Pack-internal: `00_Core.lua` hardening (staged 2026-09-16)

Built, no public row or count change: `Code/00_Core.lua` hardening rows 1 + 2 (checklist 53,
2026-09-16) — non-table pre-load globals are replaced and logged, veto reads are `pcall`'d. Desk
control `tools/desk_ck53_hostile_globals.py`; not playtested, by the owner's condition. The shipped
Code changed, so the next upload carries it; do not look for a fix-list row.

#### Pending — C95 return-home repair and C102 safe expedition fallback (2026-09-17)

⭐ **Cleared to ship, 2026-09-17.** The owner watched three legs: an ordinary UI expedition home on
the reporter's own save, a far-pad return on their rail colony, and a pack-disabled full restart
mid-return. C95 is `tested-attended`; 0 Lua errors. ⚖️ **Waived by the owner the same day:** a train
return and a positive live C102 reroute — *"waive it, its working and much better than our previous
builds"* — so the public words must say plainly that neither was watched in play. Evidence and
scope: `docs/agent/reports/C95_PLACE_HOME_BUILD.md`, entries C95 and C102.

#### ⚖️ Owner's store-card task for this release (2026-09-17, decided — EXECUTED)

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

### Released in v13 (2026-09-18) — C107 landed

- **Card:** count word **Fifty-three → Fifty-four** (site `^??? ` rows = 54, section tally
  2+16+4+7+9+6+6+2+2 sums); headliners unchanged at 14; judgment calls unchanged at four. Words
  commit `ad3614b`, site commits `f3661e2` (fix-list row) and `b45b873` (the owner's 09-12 item-53
  modder-page paring, stranded uncommitted for six days and committed on the owner's word).
- **Shipped `last_changes` is the tree draft**, unedited in the Mod Editor box this time.
- **Cleared on the owner's word ("uploaded", 2026-09-18) plus evidence:** writeback `version`
  16 → **17** (one save), `pdx_version` "11" → **"12"**, `code_hash` and `saved` rewritten; comments
  stripped from both files and restored from `94c19d3` with every written-back value kept. Steam
  read back 2026-09-18: body says "Fifty-four repairs" (0 hits for Fifty-three), newest change note
  *"Update: Sep 18 @ 5:35pm"* carries the v13 text.
- ⛔ **Not verified at close, and not claimed:** the Paradox page version was not stated, and the
  site is **NOT published** — the newest `Publish docs site` run is #12 (2026-09-17, `c5ac193`, v12's
  fix list), so the deployed fix list has 53 rows and the modder page still shows the old veto
  snippet.

### Pending — C107 Dry Farming reaches the Feeding the Future plant farms (2026-09-18)

**No hold: C107's in-game legs are done.** Desk harness `tools/desk_c107_dry_farming.py` (23
checks, 10 falsifying variants). The first build went `error` on the owner's first boot
(2026-09-18) and was corrected. The correction then passed in game: clean boot, and the kit probe
PASS on new research, across a save/reload, and after the load heal on a save that researched Dry
Farming before the fix (C107 "In game").
Source of the report: a Steam comment, 2026-09-18.

C107 is a new public row:

> The Dry Farming breakthrough now halves crop water on the Feeding the Future farms too:
> Small Farm, Underground Farm, Small Underground Farm and Automated Farm. Fungal and
> Insect Farms stay excluded, as the base game excludes Fungal Farms.

Developer detail: `Techs.DryFarming` pays three class labels (`Data/Tech.lua:787-801`); a
building joins only its own class label, so the norman farm templates were never reached.
Four `Effect_ModifyLabel` entries are appended at data load, copying the shipped percent,
and saves that researched the tech earlier are healed once on load. No version, store page,
public site or upload changed in this job.

#### Addendum to v13 (2026-09-18, after close-out `c307253`)

**Paradox page shows v16** (owner, 2026-09-18) — one below the tree's written-back 17, the same
pattern as v11 (page v13, tree 14), consistent with `VersionDisplayName` being sent before the
forced save bumps `version`. This settles the "Paradox page version was not stated" line above; the
site line stands.

### Released in v14 (2026-09-19) — C108 landed

- **Card:** count word **Fifty-four → Fifty-five** (site `^??? ` rows = 55, section tally
  4+9+2+7+7+16+2+6+2 sums); headliners unchanged at 14; judgment calls unchanged at four. Words
  commit `f7f6ffc`, site commit `92c853f` (the Wildfire row, top of *Story & mysteries*).
- **Shipped `last_changes` is the owner's box text, not the tree draft:** the sentence "It loads
  cleanly in a running game; the cure itself has not been watched yet." was removed in the Mod Editor
  box (present at `f7f6ffc`, absent from the writeback and from Steam's note). Kept as shipped, as at
  v9, v11 and v12. The public note therefore carries no "not watched" disclosure; the fix list row
  does not claim an in-game cure either.
- **Cleared on the owner's word ("uploaded", 2026-09-19) plus evidence:** writeback `version`
  17 → **19** (two bumps, not the one of v13; kept as written, never normalised), `pdx_version`
  "12" → **"13"**, `code_hash` and `saved` rewritten; comments stripped from both files (0 left) and
  restored from `f7f6ffc` with every written-back value kept. Steam read back 2026-09-19: body says
  "Fifty-five repairs" (1 hit, 0 for Fifty-four), newest change note *"Update: Sep 19 @ 7:35am"*
  carries the v14 text.
- ⛔ **Not verified at close, and not claimed:** the Paradox page version was not stated and its body
  was not read back. Site: `Publish docs site` run #14 (`92c853f`) completed with success, and the
  deployed fix list serves the Wildfire row (1 hit for its title, read 2026-09-19).

### Pending — C108 Infected colonists visit a medical building once the Wildfire cure is found (2026-09-18)

**No hold: the boot is done.** Desk harness `tools/desk_c108_wildfire_cure.py` (20 of 20 demands,
7 falsifying variants; the unfixed pack fails the cure demand). The owner's boot on 2026-09-18
(`Mars.exe-20260918-23.44.18-6a91a190.log` :144) logged `WildfireCureVisit: applied`, and logscan
read 52 of 52 modules applied with no error-shaped line (C108 "In game"). The cure itself has not
been watched in game; the owner skipped that check for now (2026-09-18).
Source of the report: r/SurvivingMars, 2026-09-18.

C108 is a new public row:

> Once the Wildfire cure is found, infected colonists now go to a medical building and are cured.
> Colonists whose dome's medical care kept them healthy never went, so the mystery could not finish.

Developer detail: 1.1.0 pays each serviced category's stats at home on rest
(`ApplyResidenceAdditiveStats`), medical included, so under a Medical Center an infected colonist
never drops below the 70 Health that sends them to `MedicalBuilding:Service`, the only place the
cure runs. The pack wraps `PickInterest` so that an infected colonist's daily interest is
`needMedical` while vaccination is on. This needs no DLC.

### Released in v15 (2026-09-23) — the 1.1.1 patch takes seventeen rows

- **Card:** count word **Fifty-five → Thirty-eight** (site `^??? ` rows = 38, section tally
  2+13+4+4+5+5+3+2 sums); headliners **14 → 9**; judgment calls unchanged at four. Seventeen rows
  left the list against sixteen retired modules, because `Fix_WispRewards` backed both wisp rows.
  *The text and numbers on your screen* lost both its rows and the section went with them. Words
  commit `a431638`, site commit `ee270dc`.
- **Shipped `last_changes` IS the tree draft this time**, byte for byte — unlike v9, v11, v12 and
  v14, the owner did not edit the Ged box, so no disclosure was lost between draft and post. The
  `description`, `short_description` and `title` are unchanged from the draft as well.
- **Cleared on the owner's word ("uploaded", 2026-09-23) plus evidence:** writeback `version`
  19 → **20** (one bump), `saved_with_revision` 403908 → **405907**, `pdx_version` "13" → **"14"**,
  `code_hash` and `saved` rewritten; comments stripped from both files (0 left in each) and restored
  from `9cd60f0` with every written-back value kept — the whole diff against that commit is those
  five fields and nothing else. Steam read back 2026-09-23: body says "Thirty-eight repairs" (1 hit,
  **0** for "Fifty-five repairs"), none of the five removed headliner bullets appear, and the newest
  change note *"Update: Sep 23 @ 12:49pm"* carries the v15 text.
- ⛔ **Not verified at close, and not claimed:** the Paradox page version was not stated and its
  body was not read back.
- ⛔ **THE SITE IS NOT PUBLISHED.** Read 2026-09-23 past cache: the deployed fix list still serves
  three of the retired row titles and has **0** hits for the new known-issue section, so it is still
  v14's build. `ee270dc` is pushed and waiting; the owner still owes the **Publish docs site**
  workflow run (`UPLOAD_WORKFLOW.md` §4). Until then the store card says thirty-eight repairs while
  the site lists fifty-five.

### Pending — game 1.1.1 response (2026-09-23)

- Track salvage retains the vendor's repair-site ownership and indexing changes
  while preserving curved/short-track salvage, refunds and whole-track cleanup.
- Vacuum migration retains the vendor's direct and multi-leg routing; both
  passage decisions are repaired. Legacy clogged-building recovery becomes
  load-only and accepts only saves written before 1.1.1. Already-resaved ambiguous
  state remains untouched so a healthy native timer is not cut short.
- Retire `BrokenTrackSalvage`, `BuildingCodesPrefab`, `DestroyedTunnels`,
  `DomeOverviewHighlight`, `FounderTraitNotification`, `GeneForging`,
  `GraphConsumedCaption`, `MirrorSphereSite`, `NightShiftWork`,
  `OpenPastureStockpiles`, `SinkholeIndestructible`, `TradeRocketFuelRefresh`,
  `TrainCargoDumping`, `TrainWaitTime`, `TrainsToVoid` and `WispRewards`.
- Evidence and limits: [build report](../../reports/GAMEPATCH_1.1.1_BUILD_2026-09-23.md).
  Desk/source results do not replace the separate owner audit or retail legs.
- **Known issue for the patch notes, owner's ruling 2026-09-23 — document, do not fix.**
  Player-facing wording: *if your Outside Ranch still looks closed after terraforming
  opens your domes, salvage it and rebuild it once; it will come back open.* Affects only
  colonies that ran an earlier pack with Open Domes already enacted — the retired
  `OpenPastureStockpiles` deliberately held those ranches on the closed entity, and
  nothing reopens them once it is gone. It is cosmetic: all nine stockpile anchors exist
  on either entity, so no resources strand. New ranches are unaffected. Evidence:
  [playtest plan](../../reports/PLAYTEST_PLAN_1.1.1_2026-09-23.md), "FINDING — removal
  residue". **Not fixed, and the reason is permanence, not effort** (owner, 2026-09-23):
  the only remedy is a load-time sweep, and a load-time sweep can never be retired,
  because no date exists by which every affected save has provably loaded once — a player
  may update today or return in six months, and the sweep must be present on *their*
  first post-update load. So it is not a small temporary fix but a permanent module,
  carried and re-verified against every future game patch, doing entity swaps — the same
  class this very release retired sixteen of. That cost is paid forever to spare a
  one-time salvage and rebuild. A future session proposing to "just add the sweep later"
  should read this clause first.
- **Change-note framing, owner's ruling 2026-09-23.** Lead with the vendor, not with the
  subtraction: *"the devs fixed X number of fixes in the 1.1.1 patch, so we are removing
  our versions of these from the pack."* The count of retired **modules** is 16 and the
  pack is 36 modules, but neither is the player-facing number: `content/fix-list.md`
  entries carry no module names or F/C ids, so the retired set maps to fix-list rows **by
  meaning**, one module possibly touching one row, none, or a shared one. Re-derive every
  count with `grep -c '^??? '` after the rows are edited; never compute it as 55 minus
  anything. Also rewrite `metadata.lua`'s historical note block rather than patching it:
  it still cites `Fix_TrainCargoDumping.lua:89`, a file this release deletes, and "22
  full-body replacements", a figure two releases stale.
- Release surfaces are pending the release job: reconcile the site fix list,
  store-card copies, description/count word and change notes from the retired
  names and surviving modules. This build does not change a version or publish.

**The site published** (owner, 2026-09-23), settling the "THE SITE IS NOT PUBLISHED" line in the v15
block above. Read back past cache the same day: the deployed fix list serves **38** rows (34
`success` + 4 `question` details blocks, so judgment calls are four there too), **0** hits for any of
the five sampled retired row titles and **0** for the removed *The text and numbers on your screen*
heading; the *One known issue after this update* section and the Outside Ranch advice are live, and
the dust-storm clog row serves its rewritten body. `install.md`'s load-repair list serves the new
wording and `index.md`'s coverage sentence serves the shortened one. Store card and site now agree
at thirty-eight.

**Paradox page shows v19** (owner, 2026-09-23), against the tree's written-back `version` 20 and
`pdx_version` "14" — three different numbers for one upload. This settles the "the Paradox page
version was not stated" line in the v15 block above, and it is the **last** release to carry that
line at all.

⚖️ **Owner ruling, 2026-09-23 — stop tracking per-store version numbers.** *"because of the way the
V's tick up because of just single save presses or uploads, and other issues, we aren't going to
track what v is on each site anymore. We only track our V number internally and check the steam
version to confirm upload."* A store page's number moves on a bare editor save as well as on an
upload, so it never measured what the releases were using it for. From v16 on: `metadata.lua`'s
`version` is the only version this project tracks, and the newest `Update:` entry on the Steam
changelog is what confirms an upload landed. The receipt drops to two items — anything that looked
wrong on either store, and whether the site published. Carried into
`release_prompt.md` (Release rails, §3, §6), `support/POST_UPLOAD_CLOSE.md` (preconditions, §1, §3)
and `UPLOAD_WORKFLOW.md` §5. Earlier blocks in this file keep their page-version lines: they record
what was true when written.

### Released in v16 (2026-09-24) — the hub set: C114, C115, C116, C117, C111 and F127

- **Card:** count word **Thirty-eight → Forty-three** (site `^??? ` rows = 43, section tally
  2+18+4+4+5+5+3+2 sums); five new rows in *Colonists & domes*, F127 as one sentence on C83's
  arrivals row; headliners unchanged at nine; judgment calls unchanged at four. Words commit
  `40cc10c`, site commit `110db81`.
- **Shipped change note is NOT the tree draft.** Steam's *"Update: Sep 24 @ 8:29pm"* carries the
  draft minus five passages: the three "Seen working / Seen in a running game" sentences, "The new
  line is in English in every language for now." and the whole line "The rescue shuttle, hub shelter
  and bed repairs have not been watched happening in a running game yet." The writeback's
  `last_changes` is still the full draft, so the cut was made after the editor saved (on the store
  page, not in the Ged box). The tree keeps the writeback as written; the disclosures live on the
  fix list (C111's *Worth knowing*) and in the bug entries.
- **Cleared on the owner's word ("uploaded", 2026-09-24) plus evidence:** writeback `version`
  20 → **21** (one bump), `pdx_version` "14" → **"15"**, `code_hash` and `saved` rewritten; comments
  stripped from both files (0 left in each) and restored from `0c7b55a` with every written-back
  value kept — the whole diff against that commit is those four fields and nothing else. Steam read
  back 2026-09-24: body says "Forty-three repairs" (1 hit, **0** for "Thirty-eight repairs").
- ⛔ **Not verified at close, and not claimed:** the Paradox body was not read back (the page is
  JavaScript-only).
- ⛔ **THE SITE IS NOT PUBLISHED.** Read 2026-09-24 past cache: **0** hits for the C114 row title
  and **0** for F127's new sentence. `110db81` was not pushed at close, so no publish run could carry
  it; it needs a push and then the owner's **Publish docs site** run (`UPLOAD_WORKFLOW.md` §4).
  Until then the store card says forty-three repairs while the site lists thirty-eight.

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
