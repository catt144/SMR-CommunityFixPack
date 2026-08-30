# Project State — the one mandatory read

Kernel only: status + pointer, never derivation.
Eviction procedure: `agent/prompts/STATE_EVICTION.md` (byte-budgeted by doccheck; owner ruling, checklist 42).
History newest-first in `docs/archive/SESSION_LOG.md`; full pre-eviction STATE = `git show 3ef6fcb:docs/agent/STATE.md`.
Defect truth `agent/bugs/INDEX.md` · facts `agent/facts/INDEX.md` · doc map `docs/README.md`.
Authoring `agent/WORKFLOW.md` · code `agent/FIX_POLICY.md` · chains `agent/reports/CHAIN_METHOD.md`.

## Now
- ⭐ PUBLISHED on both portals — Paradox `pdx_id` **156049**, Steam `steam_id` **3787202810**; both carry tree
  `version` **4** (measured 08-29 off the subscribed Steam copy: 84 entries, 82 byte-identical to the tree).
  ✅ Nothing owed on either listing. ⛔ Never re-upload to "fix" a version number — each upload bumps again (H-02).
  ⛔ Every upload OVERWRITES both page bodies from `metadata.lua`; since the 08-24 ruling `description` IS the full
  card, so that auto-fill is the CORRECT result — a hand paste is optional polish only.
- ⭐ SITE deployed 08-29 18:44Z `fcb2aa9`, status `success`, nothing undeployed — **81** live fix-list entries;
  audited clean `reports/SITE_AUDIT_0829.md`. ⛔ `publish-site.yml` is `workflow_dispatch` only — committing the
  site never publishes it. ⛔ Never quote a stored "deployed = <sha>" line as current (one was 4 days + 2 deploys
  stale, repeated twice 08-29); read the deployments API, route in `prompts/SITE_AUDIT.md`.
- Post-launch fixes shipped + LIVE on both listings (v4): F105 (`Fix_LandscapeCostRefresh`), F107 (a defect in
  our own F105 fix, caught pre-player; ⛔ field route still untested), F108 (`Fix_ExtractorStaffedPerformance`,
  full field route 3/3). F104 CLOSED, NOT OURS (GitHub issue #1, reporter confirmed). Derivation in entries
  F104/F105/F107/F108.md; digest in the newest SESSION_LOG. ⛔ Read the GitHub tracker via
  `api.github.com/.../issues/<n>/comments`, never the HTML page. ⚠️ Passage Network is ENABLED on the rig —
  untick before any clean leg.
- Blame surface (checklist 73, OPEN): `EF-065`(a) fires on ANY throw under a wrapped target (105 measured);
  2 field sightings 08-23/24, neither ours. Owner decision: harden or not.
- Next effort: the **opt-in pack** (owner 08-20, checklist 68) — kickoff reads that repo's STATE +
  `reports/PARKED_OPTIN_REFERENCES.md`.
- Rig (08-20 sitting): 3 junctions present, fix pack + TestKit ticked, opt-in pack OFF (checklist 43); runs
  cheats (the normal config).
- Shipping artifact: expected packed `.fpk` = 84 files (80 `Code/*.lua` + `items.lua` + `metadata.lua` +
  `LICENSE` + `preview.png`, `tools/pack_predict.py`). ⛔ md5/bytes exist only after the owner packs — never quote
  one (blank row = `PORTAL_PREP` §0.5(f)). ⛔ Pack route is main menu → MOD EDITOR → File → Pack Mod, NOT Mods
  Manager → Ctrl-E; full corrected route in the newest SESSION_LOG (⚠️ PORTAL_PREP §0.5 still cites the old one).
- Watches: `EF-066` swept 08-24 — 105 declared targets, 97 reach every subclass; the 8 leftovers re-declare
  subclasses (biggest: `Fix_ShuttleHubOffAvailable` misses ~578 under `Building`); which are ever INSTANTIATED is
  unmeasured, checklist 74 stays half-open on it · German is the only localisation ever SEEN, the other 7 stay
  CSV-measured (`EF-039`) · C47 speed thread (unrun) · C48 opt-in candidate · F02/F78/F81 organic · riders
  C42/F99/F80/F96-R2 post-release · `EF-051` falsifier = any stray save ·
  **F109 PARKED/unconfirmed** (Reddit, not our tracker; meteor-destroyed Atomic Accumulator REBUILT ⇒ ~50 stacked
  objects on one hex). ⛔ No cause claimed, no save, mod load unknown; the ~50 malfunction messages are the only
  derivation (`SetMalfunction` latches ⇒ ~50 OBJECTS). ⛔ Do NOT harden `DestroyedRebuild`'s `efVisible` guard on
  it. Reopen ONLY with the Command Center buildings list at that hex + mod list + a save.

## Hazards — each names an action an agent could take unattended; never do it
- **H-01** Tag `fixpack-v1.0.0` marks what actually gets packed (moved onto the close-out audit's commit 08-20).
  ⛔ Never move it again without an equivalent gate (the attended sitting + one-time release-gate ruling, ck57).
- **H-02** `metadata.lua`'s version is the SITTING's to set — never an agent's, and never by hand. The 1.0.0
  freeze is RETIRED (owner 08-24, ck75): open field reports + a patch being prepared = a patch cycle, no freeze
  assumed. What binds is mechanical: (1) an agent NEVER opens the Mod Editor — every save runs `version = version
  + 1` (`Mod.lua:967`) and `ValidateModBeforeUpload` force-saves a dirty mod (`GedModEditor.lua:836-844`), so the
  bump is the sitting's; (2) an agent NEVER hand-sets `version`/`version_major`/`version_minor` — a hand-set on
  top of the auto-bump DOUBLE-bumps, widening the portal gap ck71 says never to chase. ✅ Every OTHER hand edit to
  `metadata.lua` (the `code` list per H-10, `last_changes`, descriptions) is ordinary agent work.
- **H-03** No script/console in a launched game may touch a portal API — the FIRST call **creates the listing**
  (`SteamWorkshop.lua:17-22`). Safe: `DbgPackMod`, `tools/upload_preflight.py`. Paradox before Steam.
- **H-04** ⛔ Never call a FUTURE release ready, and never treat "published" as covering anything the owner has not
  done (successor of the discharged 08-20 upload hazard).
- **H-05** Sweep fence: no session reads `prompts/prelaunch-sweep/SWEEP_FINDINGS.md` or the link reports to reach
  a verdict, and neither STATE nor SESSION_LOG ever restates a link verdict — point at the ledger instead.
- **H-06** `EF-056`: loading a COPY of a campaign still runs that campaign's autosave rotation and **deletes the
  owner's autosaves** — pre-copy every autosave first.
- **H-07** Never restore the ~46 parked opt-in references before the opt-in pack launches; that is ITS launch
  obligation. Verbatim parking: `reports/PARKED_OPTIN_REFERENCES.md`.
- **H-08** ⛔ Pulling a mod's junction COSTS its enable and restoring the folder does NOT buy it back (`EF-055`);
  recovery = owner tick + restart, never an agent's. ⚠️ The cost lands when the **id vanishes**; a folder-for-
  folder swap under the **same id KEEPS** the enable (the opt-in pack is in that state now, ck43).
- **H-09** Never stage a packed folder beside a live junction — at equal version the **unpacked one WINS**,
  silently (`Mod.lua:1770`), and the leg measures nothing.
- **H-10** Never add, rename or drop a `Code/*.lua` module without updating `items.lua` — `SaveDef` rebuilds
  `metadata.lua`'s `code` list solely from its items (`Mod.lua:816-840`, `:973`) and both portals force that save
  on a first upload (Steam's BEFORE packing), so a module absent from `items.lua` **ships absent** (ck46).

## Rules in force (owner rulings; bodies in checklist/SESSION_LOG)
- Ship line FROZEN (08-12): `fixed` + suite + self-checks + verified save-safety IS the bar.
- A green suite does NOT authorise an upload — config B is the gate (08-17).
- ⛔ The gate was ONE-TIME, not a per-change tax (08-20, item 57). Post-release = patch-note-driven maintenance:
  `items.lua` entry (H-10) + one boot `applied` log + doccheck counts. ⛔ Never quote `FIX_POLICY` §3a's per-module
  cost for a single added fix — run B / lens sweep / audit return only for a **major overhaul**.
- Both-mods-loaded is the rig's normal config (08-12).
- Status words: `tested-attended`/`tested-unattended`; bare `tested` = legacy, closed to new work, never bulk-
  upgraded (08-15). Screen claims need an attended witness.
- ⛔ SKIPs BY NAME, never a total.
- Display name Relaunched Fix Pack; `id` + `[CommunityFixPack]` log tag KEPT (08-17).
- Never name fredware's mod on a player surface; no player load-order advice (`EF-054`, FIX_POLICY §8).
- STATE.md format: most efficient and safest — one fact per line, byte caps do the read job (08-18, item 42).

## Open owner decisions (bodies in `docs/PLAYTEST_CHECKLIST.md` → "Decisions waiting on you")
- 73 blame surface — harden or not · 76 confirm (a) was a ruling not a leaning · 53 harden now or in 1.0.1
  (rec 1.0.1) · 51 both-packs leg timing (rec after launch) · 50 chain-vs-replace wording · 47 two modder-page
  wordings · 43 opt-in pack re-tick · 41 dialog wording + sweep cap 5→8 · 40 `smr_shuttles` name · 39 dialog re-fire.
- ⭐ 08-30 — **F110 (was C25) FIXED + VERIFIED ATTENDED**: Jumbo Cave reinforcement wedged on an unreachable waste
  rock; `Fix_JumboCaveReinforcementWedge.lua` (proactive NewHour + LoadGame self-heal), attended A/B control line,
  mystery auto-completed. ⛔ NOT yet on listings — ships next patch. `bugs/F110.md`.
- Closed 08-29: 37 (both listings v4); 79 + 81 DONE; 80 WITHDRAWN IN FULL.

## Build state — `python tools/doccheck.py --emit-counts`, never hand-typed
```
BUILD STATE (emitted by tools/doccheck.py)
- modules: 80 registered (80 default-active, 0 optional-gated files)
- Code/*.lua files: 81
- TestKit probes: 100
- BUGS index rows: 110 F + 12 D + 53 C
```
Re-emit after any change; game pinned **1.0.7.396349** (`EF-014`).
