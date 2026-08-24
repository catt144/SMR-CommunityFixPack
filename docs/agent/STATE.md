# Project State — the one mandatory read

Kernel only: status + pointer, never derivation.
Eviction procedure: `agent/prompts/STATE_EVICTION.md` (byte-budgeted by doccheck; owner ruling, checklist 42).
History newest-first in `docs/archive/SESSION_LOG.md`; full pre-eviction STATE = `git show 2326bd3:docs/agent/STATE.md`.
Defect truth `agent/bugs/INDEX.md` · facts `agent/facts/INDEX.md` · doc map `docs/README.md`.
Authoring `agent/WORKFLOW.md` · code `agent/FIX_POLICY.md` · chains `agent/reports/CHAIN_METHOD.md`.

## Post-launch issues — field reports against the LIVE listings (newest first; entries carry the derivation)
- **F104 ⛔ NOT OURS, pending closure.** Passage Network's `CreateDomeNetworks` override returns nothing;
  vanilla indexes the nil (`Passage.lua:1117`). ⭐ CONFIRMED live on the rig 08-23. Steam+Paradox builds
  byte-identical, so no fixed build exists. We are NAMED only as a stack pass-through (`EF-065`(a)).
  Owed: reporter reply (DRAFTED, `reports/FIELD_REPORT_REPLIES.md`) + their confirmation, then close. ⚠️ PN is ENABLED on the rig (`H-08`) — untick
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
  ⚠️ Live listings ONE module behind; that module's **F107** is REPAIRED and RIG-VERIFIED (see F107 above).
- **F107 ✅ FIXED + RIG-VERIFIED 08-24 (checklist 74(a), receipt 76).** Was: `prev` **nil** on all 3 leaf
  classdefs ⇒ delegation dead code. Now ONE wrap on `ConstructionSite`, which declares it (`:665`).
  MEASURED unattended (`archive/f107_*.log`): suite **76/0/24/0** of 100, gate 78/78, clause 1 STILL PASS ×3,
  new clause 3 proves the widening (ungathered ok, gathered `set_to=90 start_cost=50`), sweep `UNREACHED=3 ⇒ 0`
  and TOTAL `clean=97 ⇒ 98`. Zero unexplained error lines. ⛔ Field route STILL untested (F105).
- **F106 ✅ CLOSED — REFUTED 08-24 by measurement**, filed and refuted same day. The pack applies at file-LOAD,
  BEFORE the builder (`00_Core.lua:452` < raise `lib.lua:371`), so the builder copies OUR wrap down; F33 clean.
  ⛔ `classes.lua:986-988` states the split INVERTED — never cite it. ⛔ Only `DataPatch` waits for ClassesBuilt.
- **Blame surface (checklist 73)** — `EF-065`(a) fires whenever ANY error throws under one of our
  wrapped targets (**105 measured**, not the ~60 estimated). 2 field sightings 08-23/24, neither ours. Checklist 73.

## Now
- ⭐⭐⭐ **PUBLISHED 2026-08-20 — ④ IS DONE, BOTH PORTALS, by the owner.** Paradox Mods `pdx_id` **156049**
  ships **1.0.0**; Steam `steam_id` **3787202810** ships **1.0.2** — same 78 modules, byte-identical code.
  ⚠️ The split is mechanical, not a mistake: Paradox saves AFTER upload, Steam saves BEFORE packing, so running
  both in one sitting put the bump inside Steam's archive (checklist 71; `PORTAL_PREP` §0.5(c)). ⛔ Do NOT
  re-upload to "fix" the number — a further upload bumps again. This retires 37 Q2, decided by circumstance.
- ⛔ **Owed on the live listings** (owner's hands): `PORTAL_PREP` §0.5(d) required game version **350453** ·
  §0.5(f) delivered-bytes ⚠️ **Paradox only** against md5 `6621384b…`/391,567 B; ⛔ Steam's archive legitimately
  differs (385,131 B — its save stripped comments and bumped the version before packing) · then §1 steps 2–4:
  store links into the site, Pages on, site link back onto both store pages.
- ⭐⭐ **Close-out chain (5 links) CONSUMED 08-20 — VERDICT SHIP, 0 launch blockers; all 5 challenges held.**
  `C50`+`C51` IN 1.0.0 (checklist 58), `C52` `parked`/FROZEN. Ruling receipt checklist 66.
  ⚠️ Link 5 left NO report: its record is commit `2326bd3`'s message + fact `EF-066`.
- ⭐⭐ **`C50`+`C51` are `tested-attended` (08-20, EN+DE, owner at the keyboard): 77 applied, suite 74/0/24/0 of 98.**
  Report `reports/04_ATTENDED_SITTING.md`; logs `archive/link4{en,de,lang}_*`.
  ⛔ SKIPPED BY NAME: `C50`'s challenge landing-spot site, and the in-game Mission Profile on a SpaceY colony.
- **A 1.0.x update IS queued since 2026-08-24** (F105's module; supersedes 08-20's "no queued 1.0.1").
  ✅ **UNBLOCKED 08-24: `H-02` reworded by owner ruling (checklist 75), F107 built + rig-verified.
  Nothing is owed but the OWNER'S SITTING** — ⚠️ plus `last_changes`, which still reads "Initial release."
  and is a hand edit an agent may make (see `H-02`).
  After that upload the next effort is the **opt-in pack** (owner 08-20, checklist 68); its kickoff reads
  that repo's own STATE + `reports/PARKED_OPTIN_REFERENCES.md`.
- ⛔ **Shipping artifact: NO PACKED `.fpk` MATCHES THIS TREE.** Expected shape **82 files = 78 `Code/*.lua` +
  `items.lua` + `metadata.lua` + `LICENSE` + `preview.png`** (`tools/pack_predict.py`, emitted).
  ⛔ **The md5/bytes exist only after the owner packs at the sitting — never quote one**; the blank row that
  receives them is `PORTAL_PREP` §0.5(f). Reader `tools/pack_list.py`, upload guard `tools/upload_preflight.py`.
- ⛔ **The console is NOT a route to pack or reload** — `DbgPackMod`/`ReloadLua` are both nil in `_G` at the retail
  console (measured). Only route = Mods Manager → Edit (`Ctrl-E`) → **File → Pack Mod**; ⚠️ it loads a scratch colony.
- ✅ **Rig at the 08-20 sitting: all 3 junctions present, fix pack + TestKit ticked, opt-in pack OFF** (checklist 43).
  The rig runs cheats — the normal config.
- **Owner decisions open** (bodies in `docs/PLAYTEST_CHECKLIST.md` → "Decisions waiting on you"):
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
- modules: 78 registered (78 default-active, 0 optional-gated files)
- Code/*.lua files: 79
- TestKit probes: 100
- BUGS index rows: 107 F + 12 D + 53 C
```
Re-emit after any change; game pinned **1.0.7.396349** (`EF-014`).
