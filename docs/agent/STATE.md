# Project State — the one mandatory read

Kernel only: status + pointer, never derivation.
Eviction procedure: `agent/prompts/STATE_EVICTION.md` (byte-budgeted by doccheck; owner ruling, checklist 42).
History newest-first in `docs/archive/SESSION_LOG.md`; full pre-eviction STATE = `git show 2326bd3:docs/agent/STATE.md`.
Defect truth `agent/bugs/INDEX.md` · facts `agent/facts/INDEX.md` · doc map `docs/README.md`.
Authoring `agent/WORKFLOW.md` · code `agent/FIX_POLICY.md` · chains `agent/reports/CHAIN_METHOD.md`.

## Post-launch issues — field reports against the LIVE listings (newest first; entries carry the derivation)
- **F108 ✅ FIXED + VERIFIED-ATTENDED 08-28; ⭐ LIVE ON PARADOX 08-28 (v4/pdx3), ⛔ NOT on Steam — Steam field report.**
  Extractor AI (`automation=1`/`auto_performance=50` on MetalsExtractor+PreciousMetalsExtractor labels) caps STAFFED
  extractors at 50 via `Workplace.lua:197`, so Russia's `ExtractorPerformance` goal (3 @ 160, `SponsorGoals.lua:467`,
  Roscosmos goal_4) is permanently unreachable once researched. Fix `Fix_ExtractorStaffedPerformance` (owner: FLOOR not
  ceiling) — chained post-wrapper, scoped `MetalExtractorWorkplace`, composes with C39. ⭐⭐ Attended A/B
  (`archive/f108_attended_Mars.exe-20260828-16.41.41.log`): staffed 119→(research)→**122 not 50**, workers held 12;
  unmanned control **50** (floor). ⭐ FULL FIELD ROUTE: Roscosmos goal ticked **3/3 COMPLETE** (workers Workaholic +
  high comfort, no Genius). Mechanism was F36's supporting analysis. Entry F108.md.
- **F104 ✅ CLOSED 08-24 — NOT OURS, and fully discharged.** Reply POSTED on GitHub issue **#1** 03:40Z,
  issue closed 06:01Z (`completed`), **reporter CONFIRMED 19:24Z** ("i had a hunch that mod might be the
  problem but thanks for checking"). Passage Network's `CreateDomeNetworks` override returns nothing;
  vanilla indexes the nil (`Passage.lua:1117`). ⭐ CONFIRMED live on the rig 08-23. Steam+Paradox builds
  byte-identical, so no fixed build exists. We are NAMED only as a stack pass-through (`EF-065`(a)).
  ⛔ **NEVER read the tracker through the issue's HTML page — 3 fetches returned "zero comments" when there
  were 3, and a whole owner-facing finding was built on it. Use `api.github.com/.../issues/<n>/comments`;
  the list endpoint's `comments` count is the control.** F105 = issue **#2**, OPEN, and it ALREADY has a
  posted explanation (08-24T06:04:29Z, NOT Draft B, 4 sentences stronger than the tree — itemised in
  `reports/FIELD_REPORT_REPLIES.md`, ⛔ never copy them to a player surface). ⚠️ PN is ENABLED on the rig (`H-08`) — untick
  before any clean leg. Its unmaintained state is logged as an opt-in candidate in THAT repo's FUTURE_IDEAS.
- **F105 ✅ FIXED 2026-08-24** (`Fix_LandscapeCostRefresh`; owner ruled "number 1 fix priority", checklist 72).
  ⭐⭐ **FIELD ROUTE REPRODUCED + FIX VERIFIED, attended A/B 08-24** — `archive/f105_leg{A,B}_*.log`:
  pack OFF = **14 × `:673`** raises (real Flatten job, `state=clean`, live `.WasteRock`, verified BEFORE firing);
  pack ON = **zero**; leg C is a 2nd pack-OFF control, **12 raises, `[CommunityFixPack]` 0 hits** (cleanest).
  ⛔ Triggers are 3 techs ONLY. ⛔ CORRECTION: each raise logs TWICE (uncaught `[LUA ERROR]` **+** console
  `pcall`) — 6+6 leg C, 7+7 leg A — so the uncaught path DOES fire. What never fires is `ReportModLuaError`
  (`Mod Flagged` = 0 in all 3): pack OFF ⇒ no name to match. ⇒ checklist 73 = pack ON + module OFF, cheap.
  ⭐⭐ **Leg D = INSTALL-AFTER-THE-FACT, clean** (`f105_legD_*.log`): save made WITH the defect already fired,
  pack ticked on, full exit, reload → applied, **zero `:673`**. ⇒ a player needs NO clean save; evidence for
  "safe to add to an existing save" for this defect, and the empirical case for checklist 72(a) over (b).
  ⛔ NOT a repair — the site stays broken, the guard makes it harmless. ⚠️ "EXACTLY 3 techs" is the LABEL-SWEEP
  set only; `OnMsg.ConstructionCostChanged` (`ConstructionSite.lua:2832`) is a 2nd, class-filtered reader route,
  not ruled out by measurement — same guard covers it.
- **F107 ✅ FIXED + RIG-VERIFIED 08-24, SHIPPED on Paradox 08-28** (checklist 74(a), receipt 76). Was a defect in
  our own F105 fix, found before any player had it. ⛔ Field route STILL untested. Detail evicted 08-29; entry F107.md.
- **Blame surface (checklist 73)** — `EF-065`(a) fires whenever ANY error throws under one of our
  wrapped targets (**105 measured**, not the ~60 estimated). 2 field sightings 08-23/24, neither ours. Checklist 73.

## Now
- ⭐⭐⭐ **PUBLISHED 2026-08-20 — ④ IS DONE, BOTH PORTALS, by the owner.** Paradox Mods `pdx_id` **156049**
  ships **1.0.0**; Steam `steam_id` **3787202810** ships **1.0.2** — same 78 modules, byte-identical code.
  ⚠️ The split is mechanical, not a mistake: Paradox saves AFTER upload, Steam saves BEFORE packing, so running
  both in one sitting put the bump inside Steam's archive (checklist 71; `PORTAL_PREP` §0.5(c)). ⛔ Do NOT
  re-upload to "fix" the number — a further upload bumps again. This retires 37 Q2, decided by circumstance.
- ⛔ **Owed on the live listings** (owner's hands). ✅ **§0.5(d) DISCHARGED 08-24 — it was never a task:**
  the page reads **350453** automatically (`RecommendedGameVersion = lua_revision`, `ParadoxMods.lua:153`);
  the 08-19 audit grepped `RequiredGameVersion`, the wrong parameter name, and invented the obligation.
  §0.5(f) Paradox 1.0.x captured: **MOD VER 2 · 382.57 KB · changelog v2 posted 21:55**.
  ⛔⛔ **RE-PASTE BOTH CARD BODIES — EVERY upload OVERWRITES the page text** from `metadata.lua`
  (`LongDescription`/`ShortDescription`/`DisplayName`/`Tags`; Steam sends the same). MEASURED 08-24: the
  1.0.x upload wiped the pasted Paradox body back to the short description. **PER-UPLOAD, forever.**
  ⛔⛔ **A COUNT CLAIM IS NOW LIVE AND UNBACKED**: since the 08-24 ruling `description` IS the full card, so the
  08-28 upload published **"Eighty-one repairs"** on Paradox while the deployed site shows **79** — checklist 80(b).
  ✅ §1 steps 2–4 DONE (store links in the site, Pages ON, card carries site links, 0 FILL-IN markers left).
- ⛔ **SITE IS THREE COMMITS BEHIND (F105 + F108) — checklist 79, now URGENT.** `publish-site.yml` is
  `workflow_dispatch` ONLY by design, so committing the site never publishes it. Deployed `a97b8b0` = **79**
  fix-list entries, repo `fcb2aa9` = **81**, and the LIVE Paradox body says "Eighty-one". ⇒ the falsifiable
  count is no longer a risk, it is live. Derive the live count from the deployed commit, never off the page.
- ⭐⭐ **Close-out chain (5 links) CONSUMED 08-20 — VERDICT SHIP, 0 launch blockers; all 5 challenges held.**
  `C50`+`C51` IN 1.0.0 (checklist 58), `C52` `parked`/FROZEN. Ruling receipt checklist 66.
  ⚠️ Link 5 left NO report: its record is commit `2326bd3`'s message + fact `EF-066`.
- ⭐⭐ **`C50`+`C51` are `tested-attended` (08-20, EN+DE, owner at the keyboard): 77 applied, suite 74/0/24/0 of 98.**
  Report `reports/04_ATTENDED_SITTING.md`; logs `archive/link4{en,de,lang}_*`.
  ⛔ SKIPPED BY NAME: `C50`'s challenge landing-spot site, and the in-game Mission Profile on a SpaceY colony.
- ⭐⭐ **THE SITTING HAPPENED — PARADOX UPLOADED 2026-08-28** (F105+F108). Tree `version` **4**, `pdx_version` **"3"**,
  `saved` 08-28T22:41:38Z; the editor round-trip was committed 08-29 with the §0.5(e) comment restore.
  ⛔ **STEAM DID NOT RUN, on the version arithmetic** — ONE bump per sitting = Paradox only (Steam saves BEFORE
  packing and adds a second). Same tell at 08-24. ⇒ Steam still ships the 08-20 build: **no F105, no F108**.
  ⚠️ INFERRED from `metadata.lua`, never read off the store — **checklist 80**. Next effort: the **opt-in pack**
  (owner 08-20, checklist 68); kickoff reads that repo's STATE + `reports/PARKED_OPTIN_REFERENCES.md`.
- ⛔ **Shipping artifact: NO PACKED `.fpk` MATCHES THIS TREE.** Expected shape **83 files = 79 `Code/*.lua` +
  `items.lua` + `metadata.lua` + `LICENSE` + `preview.png`** (`tools/pack_predict.py .`, re-emitted 08-24 — F105's
  module made it 79; the old "82 = 78" was one module stale).
  ⛔ **The md5/bytes exist only after the owner packs at the sitting — never quote one**; the blank row that
  receives them is `PORTAL_PREP` §0.5(f). Reader `tools/pack_list.py`, upload guard `tools/upload_preflight.py`.
- ⛔ **The console is NOT a route to pack or reload** — `DbgPackMod`/`ReloadLua` are both nil in `_G` at the retail
  console (measured). ⛔ **CORRECTED 2026-08-24 at the sitting — the route this line gave was WRONG and cost the
  owner time.** It is NOT "Mods Manager → Edit (`Ctrl-E`)": `Ctrl-E` is the MAP editor's *Selection editor*
  (`EditorShortcuts.generated.lua:727`), and MOD MANAGER is a different main-menu entry.
  ✅ **Real route: main menu → `MOD EDITOR`** (own bottom-toolbar button, `idModEditor`,
  `PGMenuRemastered.generated.lua:134`) → it prompts *"Opening the mod editor requires a restart of the game"* →
  **Yes** → `ModsRestartApp("debug_mode")` restarts INTO the editor → **File → Pack Mod**.
  ⭐ That restart re-reads `metadata.lua` from disk, so a hand edit lands without a separate relaunch.
  ⚠️ The "debugging mode for mod creators" launch option skips the restart next time.
- ✅ **Rig at the 08-20 sitting: all 3 junctions present, fix pack + TestKit ticked, opt-in pack OFF** (checklist 43).
  The rig runs cheats — the normal config.
- **Owner decisions open** (bodies in `docs/PLAYTEST_CHECKLIST.md` → "Decisions waiting on you"):
  **80 (Steam has no F105/F108 — confirm + decide; and the live count) · 79 (one button: publish the site)** ·
  76 (confirm (a) was a ruling not a leaning; the boot is done) ·
  53 (harden now or in 1.0.1; rec 1.0.1) · 51 (both-packs leg timing; rec after launch) · 50 (chain-vs-replace
  wording) · 47 (two modder-page wordings) · 43 (opt-in pack re-tick) · 41 (dialog wording + sweep cap 5→8) ·
  40 (`smr_shuttles` name) · 39 (dialog re-fire) · 37 Q2 (Steam, after Paradox).
- Watches: `EF-066` SWEPT 08-24 — **105** declared targets (not ~60), 97 reach every subclass; the 8 leftovers
  are re-declaring subclasses (biggest: `Fix_ShuttleHubOffAvailable` misses ~578 under `Building`). ⛔ Which of
  them are ever INSTANTIATED is NOT measured and checklist 74 stays half open on it ·
  ⚠️ German is the ONLY localisation ever SEEN; the other 7 packs stay CSV-measured (`EF-039`) · TestKit wave-12
  clause 1 taxonomy (other repo, `EF-066`) · C47 speed thread (descending ladder, unrun) · C48 CANDIDATE (opt-in
  territory; no seed-family fix code here) · F02/F78/F81 organic · riders C42/F99/F80/F96-R2 post-release ·
  `EF-051` falsifier = any stray save.

## Hazards — each names an action an agent could take unattended; never do it
- **H-01** Tag `fixpack-v1.0.0` was MOVED AGAIN 08-20 onto the close-out audit's commit and now marks what actually
  gets packed. ⛔ Its gate is the ATTENDED SITTING + the one-time release-gate ruling (checklist 57), NOT run B.
  Never move it again without an equivalent gate.
- **H-02** `metadata.lua`'s **version is the SITTING's to set — never an agent's, and never by hand.**
  ⭐ **The 1.0.0 FREEZE IS RETIRED (owner ruling 2026-08-24, checklist 75).** Standing rule: **open field
  reports + a patch being prepared = a patch cycle, and NO freeze is assumed.** A freeze that survives into a
  patch cycle blocks the thing the pack exists to do. ⛔ What still binds is mechanical, not a policy:
  (1) an agent NEVER opens the Mod Editor — every save runs `version = version + 1` (`Mod.lua:967`) and
  `ValidateModBeforeUpload` force-saves a dirty mod (`GedModEditor.lua:836-844`), so the bump is the sitting's;
  (2) an agent NEVER hand-sets `version`/`version_major`/`version_minor` — the sitting bumps automatically and a
  hand-set value on top DOUBLE-bumps, widening the portal gap checklist 71 says never to chase.
  ✅ Every OTHER hand edit to `metadata.lua` (the `code` list per `H-10`, `last_changes`, descriptions) is
  ordinary agent work and always was.
- **H-03** No script/console in a launched game may touch a portal API — the FIRST call **creates the listing**
  (`SteamWorkshop.lua:17-22`). Safe: `DbgPackMod`, `tools/upload_preflight.py`. Paradox before Steam.
- **H-04** ✅ **DISCHARGED 2026-08-20 — the owner uploaded; ④ is done and this is the one moment striking it is
  correct.** It stays listed because its successor binds: ⛔ **never call a FUTURE release ready, and never treat
  "published" as covering anything the owner has not done** — the post-upload items above are still open.
- **H-05** Sweep fence, still binding after both chains closed: no session reads
  `prompts/prelaunch-sweep/SWEEP_FINDINGS.md` or the link reports to reach a verdict, and neither STATE nor
  SESSION_LOG ever restates a link verdict — point at the ledger instead.
- **H-06** `EF-056`: loading a COPY of a campaign still runs that campaign's autosave rotation and
  **deletes the owner's autosaves** — pre-copy every autosave first.
- **H-07** Never restore the ~46 parked opt-in references here before the opt-in pack launches; that is ITS
  launch obligation, recorded in that repo. Verbatim parking: `reports/PARKED_OPTIN_REFERENCES.md`.
- **H-08** ⛔ **Pulling a mod's junction COSTS its enable and restoring the folder does NOT buy it back**
  (`EF-055`). Recovery = owner tick + restart, never an agent's. Never pull one to reach a configuration without
  booking that cost. ⚠️ The cost lands when the **id vanishes**; a folder-for-folder swap under the **same id KEEPS**
  the enable. **The opt-in pack is in that state now** (checklist 43).
- **H-09** Never stage a packed folder beside a live junction to reach a packed reading: with both present at
  equal version the **unpacked one WINS**, silently (`Mod.lua:1770`), and the leg measures nothing.
- **H-10** Never add, rename or drop a `Code/*.lua` module without updating `items.lua` — `SaveDef` rebuilds
  `metadata.lua`'s `code` list SOLELY from its items (`Mod.lua:816-840`, `:973`) and both portals force that save
  on a first upload (Steam's BEFORE packing), so a module absent from `items.lua` **ships absent** (checklist 46).

## Rules in force (owner rulings; bodies in checklist/SESSION_LOG)
- Ship line FROZEN (08-12): `fixed` + suite + self-checks + verified save-safety IS the bar.
- A green suite does NOT authorise an upload — config B is the gate (08-17).
- ⛔ **The gate was ONE-TIME, not a per-change tax (08-20, item 57).** Post-release = patch-note-driven
  maintenance: `items.lua` entry (H-10) + one boot `applied` log + doccheck counts. ⛔ Never quote
  `FIX_POLICY` §3a's per-module cost for a single added fix — run B / lens sweep / audit return only for a
  **major overhaul**.
- Both-mods-loaded is the rig's normal config (08-12).
- Status words: `tested-attended`/`tested-unattended`; bare `tested` = legacy, closed to new work,
  never bulk-upgraded (08-15). Screen claims need an attended witness.
- ⛔ SKIPs BY NAME, never a total.
- Display name Relaunched Fix Pack; `id` + `[CommunityFixPack]` log tag KEPT (08-17).
- Never name fredware's mod on a player surface; no player load-order advice (`EF-054`, FIX_POLICY §8).
- STATE.md format: most efficient and safest — one fact per line, byte caps do the read job (08-18, item 42).

## Build state — `python tools/doccheck.py --emit-counts`, never hand-typed
```
BUILD STATE (emitted by tools/doccheck.py)
- modules: 79 registered (79 default-active, 0 optional-gated files)
- Code/*.lua files: 80
- TestKit probes: 100
- BUGS index rows: 108 F + 12 D + 53 C
```
Re-emit after any change; game pinned **1.0.7.396349** (`EF-014`).
