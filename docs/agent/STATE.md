# Project State — the one mandatory read

Kernel only: status + pointer, never derivation.
Eviction procedure: `agent/prompts/STATE_EVICTION.md` (byte-budgeted by doccheck; owner ruling, checklist 42).
History newest-first in `docs/archive/SESSION_LOG.md`; pre-eviction STATE graves: `git show 1aafdbf:docs/agent/STATE.md`
(hotfix 2, 09-09) · `git show 3ef6fcb:docs/agent/STATE.md` (08-18).
Defect truth `agent/bugs/INDEX.md` · facts `agent/facts/INDEX.md` · doc map `docs/README.md`.
Authoring `agent/WORKFLOW.md` · code `agent/FIX_POLICY.md` · chains `agent/reports/CHAIN_METHOD.md`.

## Now
- ⭐ **v7 IS LIVE** (2026-09-10, owner's word; Steam page read: updated 3:59pm PT, 325.512 KB, "Forty-eight", 3 gallery images,
  change notes carry v7): C74+C77 `SilentHitMomentFX` + C83 `ArrivalDeaths`. Tree `version` **7**, `pdx_version` "6" (PDX display
  lags by one, ck71: never chase). ✅ Owner: both pages correct after the §3 paste (for formatting); Steam shows no version number.
- v6 = hotfix 2 (09-09): 36 modules DELETED (1.1.0 fixes them), 10 re-copied; `prompts/hotfix2/README.md`, `reports/HOTFIX_2_AUDIT.md`.
  ⚖️ Owner rule 09-08: a patch note saying "Fixed" is a **CLAIM, false until we confirm it**.
- ⛔ GAME **1.1.0.403908** + DLC shipped 2026-09-08 (`EF-075`); installed Steam build still **24995074** = the archived 1.1.0
  tree. 1.0.7 tree ARCHIVED `C:\Dev\SMR-SrcArchive\1.0.7.396349\Src` (`ad5f93d`, `EF-083`). ⛔ Trust runtime over source (`EF-078`).
  ⛔ **1.0.7 SAVES CANNOT LOAD ON 1.1.0** (`EF-079`) ⇒ the ENTIRE fixture library is branch-locked; a 1.1.0 leg
  needs a NEW colony provisioned from scratch (hours). Override exists but is triage-only (`EF-080`).
- ⛔ NEVER REPRODUCED, status HELD at `filed`/source-derived: **F116** (repaired in-body `add94b3`), **F117** (`777249d`,
  behaviour probe picks `ChooseDome`'s argument; passenger-station recipe in `bugs/F117.md` §Control, desk 8/8, ⛔ untested in
  play — `CachedArgShape()` nil ⇒ vacuous), **F118** (rider `0136af1`, no probe). Saint heal SHIPS UNEXERCISED (ck130).
  ✅ **F114 + F115 OBSERVED FIXED IN PLAY** 09-09 (attended; SESSION_LOG 09-09 sitting entries).
- 🚫 OWED — the post-upload sitting, ONE boot, now on v7 (ck144 a; recipes: checklist "THE SITTING RAN" block + `bugs/F117.md`):
  A3 (F118) · A10 · A5 c2 · A9 c4/c5 · F117's station recipe · the first `RunAll()` on the 94-probe kit (re-stamps
  `WORKFLOW.md:407`, VOID since 09-09). ⛔ Kit verdicts are PREDICTIONS until then; still FAIL/ERROR by name:
  `C47OpenFarmSeedBufferShape` (Herbs 100→50), retired `LanderCargoRatchet`/`DroneUnreachableForever`/`AutoExportPriority`.
- ⏭ NEXT: FR-1 cache v2 READ 09-11 (FINDINGS §11): Q2's no-reload overlay LOADS worlds on 580 (no-op 18×, 36 FULL, 0 faults);
  R2 reverses it; C2 valid. ck145: TEMPORARY mod BUILT (5d; `C:\Dev\SMR-FR1-TempMod-2026-09-11`); P1 PACKED WORKS (owner; FINDINGS §12); pages in UPLOAD_WORKFLOW.
  Then desk `prompts/DLC_DEEP_CHECK.md` (shape: `HUNT_AUDIT.md` §8).
  FR-1 options `reports/FR1_OPTIONS_2026-09-10.md`; EF-088 cache, EF-089 mod timing; dev reply POSTED. Owner: ck144 (v7 checks + sounds thread).
  vanillahunt CLOSED 09-10 (99): instruments SOUND WITH STATED GAPS — 1,281 table-level hunks in 368 rowed hand files listed by
  no instrument (§1.4); 12 P2s re-derived: 6 hold, 5 weakened, **C80 REFUTED**; **C82** filed by the audit (Incident reactors stay
  off); every P2 is a gain/cosmetic except C82/C66/C63; ck142 = hotfix-3 list (rec none). FR-1/2/3 OPEN; FR-1 next bench is ck145.
- ⭐ PUBLISHED both portals — `pdx_id` **156049**, `steam_id` **3787202810**, tree `version` **7** (v7, 09-10).
  ⛔ Never re-upload to "fix" a version number — each upload bumps again (H-02). ⛔ Every upload OVERWRITES both
  page bodies from `metadata.lua`; `description` IS the full card (08-24). ✅ v6 auto-fill delivered BOTH pages clean
  (owner-seen) — the first clean cycle of three; `UPLOAD_WORKFLOW` §3 paste backups stay REQUIRED.
- ⭐ SITE deployed 2026-09-10 23:08Z (`13e8b75` per the deployments API), **48** live fix-list entries (45 success + 3 ?), the two
  "built against" lines read 1.1.0.403908. ⛔ `publish-site.yml` is `workflow_dispatch` only — committing never publishes.
  ⛔ Never quote a stored "deployed = <sha>"; read the deployments API (`prompts/SITE_AUDIT.md`).
- Post-launch LIVE: F105, F107, F108 (v4), F110 (v5), hotfix 2 (v6), C74+C77+C83 (v7); F104 NOT OURS. ⛔ F107 field route untested. ⛔ Read the
  GitHub tracker via `api.github.com/.../issues/<n>/comments`, never the HTML page. ✅ Passage Network UNTICKED 09-09.
- ✅ C74+C77 `SilentHitMomentFX` BUILT + TESTED-ATTENDED 09-10: all seven intended units function across two
  no-power-cycle loads; 0 Lua errors. Metatron excluded; drill Rare Metals skin + white CP3 MOXIE silent by design. LIVE in v7 (09-10).
- ✅ **C83 `ArrivalDeaths` BUILT + TESTED-ATTENDED 09-10:** ordinary safe landing stayed silent; forced overflow all
  entered the working dome, logged one reroute, and stayed out of the dead/quarantined dome for one sol; 0 errors. LIVE in v7 (09-10).
- Shipping artifact: v7 pack = **50** files (`tools/pack_predict.py`); Steam-delivered `ModContent.fpk` **325,512 B**
  md5 `c58eea7e3b51de227adf1759e7bbc61e` (workshop folder, 09-10 19:09); PDX size unread — the two portals'
  sizes differed on v5/v6 (documented, `RELEASE_PORTAL_PREP` §0.5(f)). Tag `fixpack-v1.0.0` NOT moved (H-01).
  ⛔ Pack route is main menu → MOD EDITOR → File → Pack Mod, NOT Mods Manager → Ctrl-E (⚠️ PORTAL_PREP §0.5 old).
- Watches: `EF-066` subclass reach unmeasured, ck74 half-open · localisation: German only one SEEN (`EF-039`) ·
  C47 (unrun) · C48 opt-in · F02/F78/F81 organic · riders C42/F99/F80/F96-R2 · `EF-051` falsifier = stray save ·
  **F109 PARKED** (entry has it) · **F60** REMOVE candidate for hotfix 3 (audit F-4) · **C55** vanilla pre-sort read.
  ⛔ Do NOT harden `DestroyedRebuild`'s `efVisible` guard; reopen ONLY with the hex's buildings list + mod list + a save.

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
- ck118 (09-08): every module carrying a 1.1.0 body MUST decline on 1.0.7 by a behaviour test, never a label (`FIX_POLICY` §2a).
  1.0.7 players are served by the frozen v5 GitHub build (`v5-game-1.0.7`), linked from the card and the site.

## Open owner decisions (bodies in `docs/PLAYTEST_CHECKLIST.md` → "Decisions waiting on you")
- 98 rig half only (⛔ Steam = ONE branch at a time, owner 09-08) · 99 disposition of the self-disabled ·
  100 say anything to players yet (rec no) · 101 accept the re-verification chain shape.
- 112 DEFERRED 09-09 · **125** RULED+LANDED 09-09: F66 guard yields to `force` (desk-controlled, untested); wrapper re-read → 99.
- **130 RULED 09-09**: Saint heal SHIPS UNEXERCISED — condition is historical, unforgeable (`EF-080` override yields
  `restored 0`); additive-only and cannot throw (`Lua/TraitPreset.lua:77-95` no throwing path, `WhenActive` is a gate not
  a trap). ⛔ Its kit probe PASSes vacuously with no domed Saint — NOT coverage. Field reports are the detector.
- ✅ **131** RULED promote + LANDED 09-09 late (`tools/desk_*.py`) · **132** STATE.md warn: raise 12288 again or accept
  per-session eviction (this close-out evicted the pre-release material; measure, never quote) · **133** six
  self-check-promise decisions (`reports/SELFCHECK_PROMISE_COMBINED.md` §7), routed 09-09 · **134** assign the vanillahunt
  chain's models (5 links; rec 03 + 99 Fable), routed 09-10.
- 73 blame surface — harden or not · 76 confirm (a) was a ruling not a leaning · 53 harden now or in 1.0.1
  (rec 1.0.1) · 51 both-packs leg timing (rec after launch) · 50 chain-vs-replace wording · 47 two modder-page
  wordings · 43 opt-in pack re-tick · 41 dialog wording + sweep cap 5→8 · 40 `smr_shuttles` name · 39 dialog re-fire.

## Build state — `python tools/doccheck.py --emit-counts`, never hand-typed
```
BUILD STATE (emitted by tools/doccheck.py)
- modules: 45 registered (45 default-active, 0 optional-gated files)
- Code/*.lua files: 46
- TestKit probes: 94
- BUGS index rows: 118 F + 12 D + 84 C
```
Re-emit after any change. Game: records describe **1.0.7.396349** (`EF-014`); INSTALLED is now **1.1.0** (`EF-075`).
