# Project State — the one mandatory read

Kernel only: status + pointer, never derivation.
Eviction procedure: `agent/prompts/perma/STATE_EVICTION.md` (byte-budgeted by doccheck; owner ruling, checklist 42).
History newest-first in `docs/archive/SESSION_LOG.md`; pre-eviction STATE graves: `git show 541e626:docs/agent/STATE.md`
(post-v10, 09-13) · `git show 1aafdbf:docs/agent/STATE.md` (hotfix 2, 09-09) · `git show 3ef6fcb:docs/agent/STATE.md` (08-18).
Defect truth `agent/bugs/INDEX.md` · facts `agent/facts/INDEX.md` · doc map `docs/README.md`.
Authoring `agent/WORKFLOW.md` · code `agent/FIX_POLICY.md` · chains `agent/reports/CHAIN_METHOD.md`.

## Now
- ⭐ **v10 IS LIVE on both portals** (2026-09-13, owner's word): `pdx_id` **156049**, `steam_id` **3787202810**,
  tree `version` **11**, `pdx_version` "9", count word **Forty-nine**. C85 + C89 + C88 in, F37/F43+F118/F31 out.
- Shipping artifact: Steam-delivered `ModContent.fpk` **371,327 B** md5 `bef42a2d5405e06444b7e6efdf28cf38`
  (workshop folder, 09-13 00:25 local). ⛔ Never carry a pack size — predict with `tools/pack_predict.py`.
  ✅ The "56 vs 54" gap was a READER DEFECT, not a packaging one: `flpk_extract` re-read nested tables under the
  parent prefix and double-counted two entries (`reports/DOC_OVERHAUL_AUDIT.md` §1). v10 shipped **54**, matching
  the prediction exactly. Fixed + gated by doccheck's FLPK SELFTEST; `*/.agents/*` now pack-ignored, model **52**.
  PDX size unread; the two portals' sizes differed on v5/v6 (`RELEASE_PORTAL_PREP` §0.5(f)).
- ⛔ Pack route is main menu → MOD EDITOR → File → Pack Mod, NOT Mods Manager → Ctrl-E (⚠️ PORTAL_PREP §0.5 old).
- ⛔ **BASELINE IS 1.1.0.403908** + DLC, shipped 2026-09-08 (`EF-075`, ck168); 1.0.7 is history, no branch install,
  tree archived at `C:\Dev\SMR-SrcArchive\1.0.7.396349\Src` (`EF-083`). Old entries KEEP their version stamp.
- ⛔ Trust runtime over source (`EF-078`). ⛔ **1.0.7 SAVES CANNOT LOAD ON 1.1.0** (`EF-079`) — the fixture library
  is branch-locked; a 1.1.0 leg needs a NEW colony provisioned from scratch (hours). Override is triage-only (`EF-080`).
- ⛔ NEVER REPRODUCED, status HELD at `filed`/source-derived, never promote without a play leg: **F116** (repaired
  in-body `add94b3`), **F117** (`777249d`; station recipe in `bugs/F117.md` §Control, desk 8/8, ⛔ untested in play —
  a nil `CachedArgShape()` makes the control vacuous), **F118** (rider `0136af1`, no probe).
- 🚫 OWED — the post-upload sitting, ONE boot (ck144 a; recipes: checklist "THE SITTING RAN" block + `bugs/F117.md`):
  A3 (F118) · A10 · A5 c2 · A9 c4/c5 · F117's station recipe · the first `RunAll()` on the probe kit (re-stamps
  `WORKFLOW.md:537`, VOID since 09-09). ⛔ Kit verdicts are PREDICTIONS until then; still FAIL/ERROR by name:
  `C47OpenFarmSeedBufferShape` (Herbs 100→50), retired `LanderCargoRatchet`/`DroneUnreachableForever`/`AutoExportPriority`,
  `GhostFarmOxygen`/`LayoutTechLock`/`AnomalyCaveInMap` (modules retired 09-12; Wave14 wrap rows :116-117, :130 too).
- ⛔ **C89's B2 panel leg was NOT RUN, by owner ruling** — one unmeasured link (`CountDome` 0 leaves the panel clear, vanilla
  path). **Reopen C89 on a countering field report.** C85's `(daily)` arm and C88's same-type compare (structurally
  impossible — every supplyable prefab is `require_prefab`) are unavailable, not owed. Gate evidence: each entry's
  §Attended check, SESSION_LOG 09-12; ⛔ never re-derive a leg from the module.
- **C90** (Saint + Sinkhole apply-success guards) ships in v10 `fixed` but **UNEXERCISED** — `reports/C90_GUARDS_BUILD.md`.
  **C91** open candidate: vanilla leaks the Building Codes modifier on repeal. **C92** (P2, `cand` 09-13):
  `ResearchedAllTechs` counts hidden `UndergroundExploitation`; reporter-save census pins that barrier, repeatable cause WITHDRAWN — `bugs/C92.md`.
- ⛔ `SaintBlessing`'s kit probe PASSes **vacuously** with no domed Saint — not coverage; field reports are the detector
  (ck130). ✅ The heal itself fired in play 09-12.
- Post-launch LIVE: F105, F107, F108 (v4), F110 (v5), hotfix 2 (v6), C74+C77+C83 (v7), F119+C86 (v8), F59 repair +
  F60 out (v9), C85+C89+C88 in / F37+F43+F118+F31 out (v10); F104 NOT OURS. ⛔ F107 field route untested.
- ⛔ Read the GitHub tracker via `api.github.com/.../issues/<n>/comments`, never the HTML page.
- ✅ SITE DEPLOYED 2026-09-13 07:06Z, `d86a347`, state `success` (deployments API + live page read): **49** live rows
  (45 success + 4 question) = the card's Forty-nine, first agreement since 09-11. Live FAQ carries "Four judgment calls"
  and no longer promises the retired farm-oxygen repair. ⚖️ The deploy is the owner's act — `publish-site.yml` is
  `workflow_dispatch` only. ⛔ Never quote a stored "deployed = <sha>"; read the deployments API (`perma/SITE_AUDIT.md`).
  Owner's 2 pared files (`for-modders.md`, `install.md`) stay uncommitted = decision 47.
- ⭐ FR-1 TEMP WORKAROUND MOD LIVE 09-11 (Steam 3799500849 / PDX 158711). **ALL FR-1 / Linux / NVIDIA work →
  `prompts/perma/LINUX_DISPATCH.md`.** Field: 3 working (one 10xx), 1 failing (GTX 1070, log requested).
- ⏭ NEXT: no agent item blocks anything — v10 is closed out (`POST_UPLOAD_CLOSE` + `RELEASE.md` §5 ran 09-13).
  Owner OWES: ck144 (a) the boot · ck151 (b) dev-report scope. Handoff `prompts/perma/HANDOFF_ORCHESTRATOR.md` §3 LIVE.
  Desk `prompts/DLC_DEEP_CHECK.md` (`HUNT_AUDIT.md` §8). Chain `prompts/fixtoggles/` DEFERRED 09-12 (ck148, not started).
- Watches: `EF-066` subclass reach unmeasured, ck74 half-open · localisation: German only one SEEN (`EF-039`) ·
  C47 (unrun) · C48 opt-in · F02/F78/F81 organic · riders C42/F99/F80/F96-R2 · `EF-051` falsifier = stray save ·
  **F109 PARKED** (entry has it) · **F60** RETIRED 09-11 (ships in v9) · **C55** vanilla pre-sort read · FR-2/FR-3 OPEN.
  ⛔ Do NOT harden `DestroyedRebuild`'s `efVisible` guard; reopen ONLY with the hex's buildings list + mod list + a save.

## Hazards — each names an action an agent could take unattended; never do it
- **H-01** Tag `fixpack-v1.0.0` marks what actually gets packed. ⛔ Never move it again without an equivalent gate
  (the attended sitting + the one-time release-gate ruling, ck57).
- **H-02** ⛔ An agent NEVER opens the Mod Editor and NEVER hand-sets `version`/`version_major`/`version_minor`.
  Every editor save runs `version = version + 1` (`Mod.lua:967`) and `ValidateModBeforeUpload` force-saves a dirty
  mod (`GedModEditor.lua:836-844`), so the bump is the SITTING's; a hand-set on top DOUBLE-bumps (ck71, ck75).
  ✅ Every OTHER hand edit to `metadata.lua` (the `code` list per H-10, `last_changes`, descriptions) is ordinary work.
- **H-03** No script/console in a launched game may touch a portal API — the FIRST call **creates the listing**
  (`SteamWorkshop.lua:17-22`). Safe: `DbgPackMod`, `tools/upload_preflight.py`. Paradox before Steam.
- **H-04** ⛔ Never call a FUTURE release ready, and never treat "published" as covering anything the owner has not done.
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
- ⚖️ A vendor patch note saying "Fixed" is a **CLAIM, false until we confirm it** (owner, 09-08).
- Both-mods-loaded is the rig's normal config (08-12).
- Status words: `tested-attended`/`tested-unattended`; bare `tested` = legacy, closed to new work, never bulk-
  upgraded (08-15). Screen claims need an attended witness.
- ⛔ **Replies to players are PULL-ONLY (09-12, ck165; `WORKFLOW.md` rule 5b).** Never draft one unasked, never put
  one on the owner's owed list, never nudge a waiting `DRAFT`, never gate work on one. ✅ Triage into `bugs/` UNAFFECTED.
- ⛔ SKIPs BY NAME, never a total.
- Display name Relaunched Fix Pack; `id` + `[CommunityFixPack]` log tag KEPT (08-17).
- Never name fredware's mod on a player surface; no player load-order advice (`EF-054`, FIX_POLICY §8).
- STATE.md format: most efficient and safest — one fact per line, byte caps do the read job (08-18, item 42).
- ck118 (09-08): every module carrying a 1.1.0 body MUST decline on 1.0.7 by a behaviour test, never a label
  (`FIX_POLICY` §2a). 1.0.7 players are served by the frozen v5 GitHub build (`v5-game-1.0.7`), linked from card + site.
- ⛔ Every upload OVERWRITES both page bodies from `metadata.lua`; `description` IS the full card (08-24).
  `UPLOAD_WORKFLOW` §3 paste backups stay REQUIRED every cycle. Auto-fill is CLOSED (ck155, never re-ask).

## Open owner decisions (bodies in `docs/PLAYTEST_CHECKLIST.md` → "Decisions waiting on you")
- STILL OPEN: 53 harden now or in 1.0.1 · 47 two modder-page wordings · 152 c open · 133 two `FIX_POLICY` §2a
  lines (2 UNKNOWN-status policy, 4 `LuaRevision` label). ⛔ This enumeration feeds `WAITING_ON_YOU.md` — keep the
  literal `STILL OPEN:` and `Owner OWES: ck##` idioms, or the owner's register silently drops items.
- **53**: RULED 09-12 to pare the modder surface, so the hardening queue shrinks with it; rec 1.0.1.
- **47**: the owner's 2 pared site files ride on it.
- **133**: ⚠️ `prompts/SELFCHECK_PILOT.md` never fired and is now unreachable — removal RECOMMENDED, not done.
- **151 (b)** dev-report scope (ck165 lets you defer it) · **151 (c)** open. ⛔ F59 re-derived 09-11: the expedition
  claim CONFIRMED **+ a 2nd caller** (manual Set Residence on a full home OVERFILLS it, both branches); the repair
  must cover both, and the frozen `v5-game-1.0.7` download ships the same body with no version gate.
- **152 (c)** open (A1 source-derived, A2 `tested-attended`, (e) swept with v10).
- **169 ➋** DISCHARGED 09-13 — `faq.md` committed as `d86a347`; the site deploy itself is still the owner's act.

## Build state — `python tools/doccheck.py --emit-counts`, never hand-typed
```
BUILD STATE (emitted by tools/doccheck.py)
- modules: 46 registered (46 default-active, 0 optional-gated files)
- Code/*.lua files: 47
- TestKit probes: 97
- BUGS index rows: 119 F + 12 D + 92 C
```
Re-emit after any change. Records citing **1.0.7.396349** (`EF-014`) predate the baseline move; INSTALLED is **1.1.0**.
