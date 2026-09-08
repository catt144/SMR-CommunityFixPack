# Project State — the one mandatory read

Kernel only: status + pointer, never derivation.
Eviction procedure: `agent/prompts/STATE_EVICTION.md` (byte-budgeted by doccheck; owner ruling, checklist 42).
History newest-first in `docs/archive/SESSION_LOG.md`; full pre-eviction STATE = `git show 3ef6fcb:docs/agent/STATE.md`.
Defect truth `agent/bugs/INDEX.md` · facts `agent/facts/INDEX.md` · doc map `docs/README.md`.
Authoring `agent/WORKFLOW.md` · code `agent/FIX_POLICY.md` · chains `agent/reports/CHAIN_METHOD.md`.

## Now
- ⛔ GAME **1.1.0.403908** + DLC shipped 2026-09-08; rig auto-updated, `ModTools\Src` overwritten ⇒ the 1.0.7
  citation base is GONE from disk (`EF-075`). ⛔ Trust runtime over source reads: the desk audit predicted 6 self-disabled
  modules, the game measured 13 (`EF-078`).
  ⛔ **1.0.7 SAVES CANNOT LOAD ON 1.1.0** (`EF-079`) ⇒ the ENTIRE fixture library is branch-locked; a 1.1.0 leg
  needs a NEW colony provisioned from scratch (hours). Override exists but is triage-only (`EF-080`). Decision 98.
  ✅ F114 CAUSE CONFIRMED + GATED (ck106, `8bc6821`): the 1.0.7 `UnloadAll` copy indexed nil demand on 1.1.0
  ⇒ train never moved (`bugs/F114.md`).
  ✅ Opt-in pack UNTICKED (ck43): enumerated, ZERO `applied` lines on every boot since 15.21 — no confound.
  ✅ F113/F112 gates + F111 guard landed (2efbcf6); all three still `filed`.
  ✅ **F115 GATED** (ck109, `628ea4d`): 1.1.0 prepended `map` to `LandscapeForEachUnit` (`Landscaping.lua:509`)
  AND moved `Landscapes` to a MapVar ⇒ gate = the global is gone (`EF-082`). Body untouched, so `sigcheck` still
  reads MISMATCH here and that is CORRECT (`bugs/F115.md`).
  ✅ **F116 REPAIRED in-body** (`add94b3`), NOT gated: our 1.0.7 copy lacked 1.1.0's PRE-SORT `node_idx`
  revalidation (`TrackElement.lua:473-476`). P1→P2, source-derived, NEVER reproduced. ⛔ The ONLY new code.
  ⛔ NAME sweeps are BLIND to arity and body changes; **17 of 22 full-body replacements are still UNDIFFED** on
  1.1.0 and nothing we own bounds body divergence (F114 was invisible to all three).
  ✅✅ **BOTH GATES MEASURED 2026-09-08** (owner boot `17.51.09`, `archive/logs/gated110_*`): **63 applied /
  17 inactive / 14 named**, exactly as predicted, **0 error-shaped lines**. Both hand-written (F114) and
  `Require`-native (F115) `update_suspect` routes CONFIRMED. ⛔ MENU-ONLY (~2 min, no game loaded) ⇒ trains and
  landscaping were NOT exercised; the throws are impossible by construction, not observed-absent. Untested ≠ clean.
  ⚖️ Owner rule 09-08: a patch note saying "Fixed" is a **CLAIM, false until we confirm it**.
- ⭐ PUBLISHED both portals — `pdx_id` **156049**, `steam_id` **3787202810**, tree `version` **5** (F110, 08-30).
  ⛔ Never re-upload to "fix" a version number — each upload bumps again (H-02). ⛔ Every upload OVERWRITES both
  page bodies from `metadata.lua`; `description` IS the full card (08-24). ⛔ Auto-fill has NEVER delivered a
  clean page in 2 cycles ⇒ `UPLOAD_WORKFLOW` §3 paste backups REQUIRED.
- ⭐ SITE deployed 08-30, **82** live fix-list entries. ⛔ `publish-site.yml` is `workflow_dispatch` only —
  committing never publishes. ⛔ Never quote a stored "deployed = <sha>"; read the deployments API
  (`prompts/SITE_AUDIT.md`).
- Post-launch LIVE: F105, F107, F108 (v4), F110 (v5); F104 NOT OURS. ⛔ F107 field route untested. ⛔ Read the
  GitHub tracker via `api.github.com/.../issues/<n>/comments`, never the HTML page. ⚠️ Passage Network ENABLED
  on the rig — untick before any clean leg.
- Shipping artifact: packed `.fpk` = 85 files (`tools/pack_predict.py`); v5 pack verified 08-30 (app **3215050**).
  ⛔ Pack route is main menu → MOD EDITOR → File → Pack Mod, NOT Mods Manager → Ctrl-E (⚠️ PORTAL_PREP §0.5 old).
- Watches: `EF-066` subclass reach unmeasured, ck74 half-open · localisation: German only one SEEN (`EF-039`) ·
  C47 (unrun) · C48 opt-in · F02/F78/F81 organic · riders C42/F99/F80/F96-R2 · `EF-051` falsifier = stray save ·
  **F109 PARKED** (entry has it). ⛔ Do NOT harden `DestroyedRebuild`'s `efVisible` guard; reopen ONLY with the
  hex's buildings list + mod list + a save.

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
- ⛔ 98 1.0.7 branch: pin back or rebaseline (GATES 99-101) · 99 disposition of the 6 self-disabled modules ·
  100 say anything to players yet (rec no) · 101 accept the re-verification chain shape.
- 73 blame surface — harden or not · 76 confirm (a) was a ruling not a leaning · 53 harden now or in 1.0.1
  (rec 1.0.1) · 51 both-packs leg timing (rec after launch) · 50 chain-vs-replace wording · 47 two modder-page
  wordings · 43 opt-in pack re-tick · 41 dialog wording + sweep cap 5→8 · 40 `smr_shuttles` name · 39 dialog re-fire.

## Build state — `python tools/doccheck.py --emit-counts`, never hand-typed
```
BUILD STATE (emitted by tools/doccheck.py)
- modules: 80 registered (80 default-active, 0 optional-gated files)
- Code/*.lua files: 81
- TestKit probes: 100
- BUGS index rows: 116 F + 12 D + 53 C
```
Re-emit after any change. Game: records describe **1.0.7.396349** (`EF-014`); INSTALLED is now **1.1.0** (`EF-075`).
