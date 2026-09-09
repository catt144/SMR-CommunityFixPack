# 02 · The deletion sweep — every module that leaves, in one pass

Chain: `prompts/hotfix2/README.md` (its binding rules are yours). Runs after 01.
**You are the only prompt in this chain permitted to touch `items.lua` or
`metadata.lua`'s `code` list.** That is deliberate — see §1.

## 0 · Start

`git log --oneline -10` · `git pull` · `ListAgents`. Staleness anchor: link 01's
close-out commit. Todo list before you touch anything: one item per
commit-and-verify unit, and this job has several.

**Read path:** `agent/STATE.md` · `VANILLA_FIX_QA.md` §0 (**before** any report
row — it corrects the report in four places) · `PACK_1_1_0_REVERIFICATION.md`
§1b (the rows) and §1h (the rebreak pass) · `docs/PLAYTEST_CHECKLIST.md` items
98, 115, 117, 118 · `agent/FIX_POLICY.md` · your inbox below.

## ⛔ 1 · BLOCKED until two decisions are ruled

**Do not start without both.** They are in the checklist under "Decisions
waiting on you"; if either is still open, say so and STOP.

- **ck98 — is there a 1.0.7 line?** Decides **delete vs gate** for every row
  below. No 1.0.7 line ⇒ delete the file and its `items.lua` entry. A 1.0.7 line
  ⇒ each module STAYS and gains a 1.1.0 self-check that declines, and this
  becomes a very different, much larger job. ⚠️ ck118 is relevant context, not an
  answer: 1.0.7 players are served a frozen v5 download, which is an argument
  for deleting, but the owner rules it, not you.
- **ck117 — do non-Steam players matter?** Decides `90_SaveSanitizer` (R-36)
  alone. Keep ⇒ its F35 and F48 passes stay and only its dead F03 pass goes
  (R-5). Remove ⇒ the whole module goes with the rest.

## 2 · Why one prompt owns this

`H-10` normally protects against a module missing from `items.lua` shipping
absent. **On this patch it inverts**: 36 modules are leaving, and the failure
mode is a file deleted from `Code/` but left in `items.lua`, or the reverse.
Both portals force a `SaveDef` on upload that rebuilds `metadata.lua`'s `code`
list **solely from `items.lua`** (`Mod.lua:816-840`, `:973`), so an inconsistency
here is not a lint error — it decides what ships.

⇒ Get `Code/`, `items.lua` and the `code` list into ONE consistent state, and
prove it with `python tools/doccheck.py --emit-counts` before you commit.

## 3 · The list — 36 full deletions plus one half-module edit

Every row's evidence is `PACK_1_1_0_REVERIFICATION.md` §1b (and §1h for the
rebreak read). ⛔ **Re-derive the route before deleting**: open the 1.1.0 body
and confirm the defect really is gone. A verdict you inherit is a verdict you
cannot defend to link 99.

**From the REMOVE block (ck115) — R-1…R-19, R-21…R-35, minus R-7:**

`LowStorageWarning` · `LanderCargoRatchet` · `TouristSatisfaction` ·
`AutomationLawCompensation` · `UpgradeModifierLeak` · `SmallLandscapeSites` ·
`DroneUnreachableForever` · `MeteorFrequency` · `MeteorStormWedge` ·
`AsteroidLanderAvailable` · `GridGlobalStorage` · `LastTransmissionStorage` ·
`RainsDeadlock` · `DustSicknessDamage` · `IndependenceTerraforming` ·
`UniversityOvertraining` · `CaveInsNoDisasters` · `CommandCenterNumbers` ·
`DustDevilSpawnGate` · `DustDevilsDescrMap` · `DustStormUndergroundBreaks` ·
`ExtractorStaffedPerformance` · `LanderReturnFuel` · `LandscapeCostRefresh` ·
`LocalizedUIText` · `MilestoneCrash` · `MoraleComfortTooltip` ·
`SpaceYDroneCapBullet` · `StorageRateModifiers` · `TechDescriptionBuilding` ·
`TouristApplicants` · `TrainMinors` · `TrainPlatformWedge`  **(33)**

**Plus the three applies-today harms whose disposition is REMOVE:**

- `FirstAsteroidPrefabs` (F-4) — no cleanup owed. Note for the patch notes:
  prefabs already granted on 1.1.0 saves cannot be taken back, and the
  `SMRFixPack_FirstAsteroidPrefabs` GameVar is absent-tolerant.
- `AstrogeologistExtractors` (F-5) — ⛔ **owes a save cleanup**, §4.
- `DisasterPredictionLeak` (R-20) — the sixth harm, promoted by the QA (§0.1).
  Whole module; nothing to keep. Its `NewDay` sweep clears the game's own
  notification-less `DisasterNormalRains` flag, so a dust storm or cold wave can
  start on top of an incoming rain warning.

**Plus the half-module (R-7), which is an EDIT, not a deletion:**
`Fix_DroneTransportMinors.lua` — delete `repair_unreachables` and
`OnMsg.OnPassabilityChanged` (`:139-160`). ⛔ **Keep half (a)** — it is K-8 on
the KEEP list and still correct. The file stays in `items.lua`.

**Conditional on ck117:** `90_SaveSanitizer` (R-36).

⛔ **Do NOT "repair" the two rename false negatives instead of removing them**
(`DustSicknessDamage` R-15, `IndependenceTerraforming` R-16). The QA explains
why; reopening that is out of fence.

## 4 · The save cleanup F-5 owes (QA §0.2)

Our two `Effect_ModifyLabel` entries live in the **persisted**
`UIColony.label_modifiers`. Deleting the module leaves +10% `production_per_day1`
on AutomaticMetalsExtractors and +10% `water_production` on
MicroGAutoWaterExtractors in every 1.1.0 save that ran under the pack, with
nothing left to clean them.

Key the one-shot cleanup on **`prop` + label**, exactly as the module's own heal
already does (`Fix_AstrogeologistExtractors.lua:207-215`) — read that code before
writing the replacement, and put the cleanup where it survives the module's
deletion (`90_SaveSanitizer` is the home for exactly this class, which is a
second reason ck117's answer matters to you).

⚠️ Vanilla's own key shape on 1.1.0 was NOT checked by the QA reader
(`GetLabelModifierId(parent)`, their "not opened" list) — verify ours cannot
collide with vanilla's before you delete by key.

**Control this owes the owner (~3 min, batch it with 03's):** load an
Astrogeologist save that ran under the pack and confirm the two extractors no
longer carry the +10% — `AutomaticMetalsExtractor` (`production_per_day1`) and
`MicroGAutoWaterExtractor` (`water_production`). ⛔ Route it to
`docs/PLAYTEST_CHECKLIST.md`; a cleanup nobody watched run is a claim, and this
one silently edits a persisted save field.

## 5 · Per-module close-out — all five, every time

1. `Code/Fix_<Name>.lua` deleted.
2. Its `items.lua` entry deleted (`H-10`).
3. The bug entry `agent/bugs/<ID>.md` gains a **dated 1.1.0 observation** —
   ⛔ never a rewritten citation, never a deleted one. The 1.0.7 record stays
   true; you are adding what 1.1.0 changed.
4. The site's fix-list entry (repo `SMR-CommunityMods`, `content/fix-list.md`).
   ⚠️ Committing there does not publish — `publish-site.yml` is
   `workflow_dispatch` only.
5. A patch-note line, drafted for link 06. ⛔ You do not edit `metadata.lua`'s
   `last_changes` — 06 owns it.

## 6 · Consequences to hand forward, not swallow

- `ExtractorStaffedPerformance` (F108) and `LandscapeCostRefresh` (F107) are
  **named on live store surfaces and the site**. Removing them makes those
  claims stale. Route to link 06 with the exact wording that needs to change.
- `TrainMinors` removal leaves **two displays stale** (QA §0.8, R-34) — a
  patch-note item, not a silent drop.
- `LowStorageWarning` (R-1): 1.1.0 **deleted** the Food/maintenance warning
  branches rather than fixing them, so a 1.1.0 player simply gets no low-Food
  warning. That is a feature request if the owner wants it back, not a fix —
  route it to the checklist, do not build it.
- Four rows are marginally WORSE than vanilla today (`SmallLandscapeSites`,
  `TouristApplicants`, `SpaceYDroneCapBullet`, `DustStormUndergroundBreaks`).
  Worth one sentence in your outbox: their removal is a small improvement, not
  neutral.

## 7 · Scope fence

**In:** the deletions above, `items.lua`, the R-7 edit, the F-5 save cleanup,
bug-entry observations, site fix-list entries, drafted patch-note lines.
**Out:** `00_Core.lua`; every FIX-set module (03 and 04 own those); the KEEP set;
`metadata.lua` `last_changes` and any store text; `version` (⛔ `H-02`).
Found something out of fence? **File it, do not fix it.**

## 8 · Stop conditions

- ck98 or ck117 unruled ⇒ STOP, say which.
- A row's defect is NOT actually gone when you re-derive it ⇒ **STOP AND ASK.**
  That is a flipped verdict and it is the owner's call, not a judgement you make
  mid-sweep. The QA flipped none in 46 rows, so a flip is a real finding —
  capture it as drift evidence for 99 either way.
- The F-5 cleanup key could collide with vanilla's ⇒ stop and report.
- `doccheck --emit-counts` disagrees with your expected module count ⇒ stop.
  Do not "fix" the count by editing a doc.

## 9 · What may NOT be claimed

- ⛔ Not "the removed fixes were never needed". They were correct on 1.0.7. What
  is true is that 1.1.0 fixes them itself.
- ⛔ Not "removal is verified safe". You verified it in source. Nothing has run.
- ⛔ Not "no player is affected" — a 1.0.7 player who updates loses these
  (ck118). Say it plainly.
- ⛔ No status moves on evidence you did not witness.

## 10 · Close-out

Green gates (README rule 9) plus `doccheck --emit-counts` re-emitted into
`STATE.md`'s build-state block. Expected boot-log consequence, for 99 to check:
every removed module **gone** from the `[CommunityFixPack]` block — not
`inactive`, absent.

Append your outbox to `03`, `04`, `06` and `99`. Strike your README row,
`git rm` this file, commit together, push.

## Notes from upstream

*(From the authoring session, `smr-bugfixpack-91`, 2026-09-08.)*

- ⚠️ From `smr-bugfixpack-cd`, which built `sigcheck.py`/`logscan.py` and wrote
  the re-verification brief: **36 of 80 modules leaving is 44% of the pack, and
  the 08-20 ruling scoped the full release gate's return to "a major overhaul".**
  Hotfix 1 correctly priced itself as maintenance (4 files, +78/-2); do not
  inherit that costing by analogy. This is filed for the owner as part of ck118's
  block — if you conclude it is still maintenance, **say so with reasoning
  rather than by omission**.
- `tools/logscan.py --build <id>` is the safe way to read a boot log; a
  hand-rolled grep undercounted throws 30 vs 157 on 2026-09-08 because the engine
  writes the `[LUA ERROR]` header in two forms. A log copied while `Mars.exe` is
  running is a PARTIAL log and has already cost this project two wrong counts.
- PT-20 uninstall safety was verified on **1.0.7 only**, never on 1.1.0. Removing
  modules that wrote into saves is exactly the class that test covered.
