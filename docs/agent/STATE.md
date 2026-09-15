# Project State — pull; read it when a task, a prompt or the owner calls for status

## Must_Read_Header
<!-- RULES -->
This file contains current status and pointers. Binding duties live in `CLAUDE.md`, document-local headers, and task documents.
<!-- /RULES -->

Eviction procedure: `agent/prompts/perma/STATE_EVICTION.md` (byte-budgeted by doccheck; owner ruling, checklist 42).
History newest-first in `docs/archive/SESSION_LOG.md`; pre-eviction STATE graves: `git show 541e626:docs/agent/STATE.md`
(post-v10, 09-13) · `git show 1aafdbf:docs/agent/STATE.md` (hotfix 2, 09-09) · `git show 3ef6fcb:docs/agent/STATE.md` (08-18).
Defect truth `agent/bugs/INDEX.md` · facts `agent/facts/INDEX.md` · doc map `docs/README.md`.
Authoring `agent/WORKFLOW.md` · code `agent/FIX_POLICY.md` · chains `agent/reports/CHAIN_METHOD.md`.

## Now
- ⭐ **v10 IS LIVE on both portals** (2026-09-13, owner's word): `pdx_id` **156049**, `steam_id` **3787202810**,
  tree `version` **11**, `pdx_version` "9", count word **Forty-nine**. C85 + C89 + C88 in, F37/F43+F118/F31 out.
- Shipping artifact: Steam-delivered `ModContent.fpk` **371,327 B** md5 `bef42a2d5405e06444b7e6efdf28cf38`
  (workshop folder, 09-13 00:25 local). Pack-size predictor: `tools/pack_predict.py`.
  ✅ The "56 vs 54" gap was a READER DEFECT, not a packaging one: `flpk_extract` re-read nested tables under the
  parent prefix and double-counted two entries (`reports/DOC_OVERHAUL_AUDIT.md` §1). v10 shipped **54**, matching
  the prediction exactly. Fixed + gated by doccheck's FLPK SELFTEST; `*/.agents/*` now pack-ignored, model **52**.
  PDX size unread; the two portals' sizes differed on v5/v6 (`RELEASE_PORTAL_PREP` §0.5(f)).
- Pack route: main menu → MOD EDITOR → File → Pack Mod (`UPLOAD_WORKFLOW.md`; PORTAL_PREP §0.5 is old).
- **BASELINE IS 1.1.0.403908** + DLC, shipped 2026-09-08 (`EF-075`, ck168); 1.0.7 is history, with
  its tree archived at `C:\Dev\SMR-SrcArchive\1.0.7.396349\Src` (`EF-083`) and its entry version stamps retained.
- Runtime evidence outranks source (`EF-078`). **1.0.7 SAVES CANNOT LOAD ON 1.1.0** (`EF-079`) — the fixture library
  is branch-locked; a 1.1.0 leg needs a NEW colony provisioned from scratch (hours). Override is triage-only (`EF-080`).
- **F116**, **F117**, and **F118** remain HELD at `filed`/source-derived pending a play leg: F116 (repaired
  in-body `add94b3`), F117 (`777249d`; station recipe in `bugs/F117.md` §Control, desk 8/8, untested in play —
  a nil `CachedArgShape()` makes the control vacuous), **F118** (rider `0136af1`, no probe).
- ✅ **ck144 (a) DISCHARGED 09-15** (ck184 b/d; `reports/CK144A_CLOSEOUT_SITTING.md`): the first `RunAll()` on the
  rebuilt kit ran under a SAME-DAY stamp — 69 PASS / 4 FAIL / 18 SKIP / 6 ERROR, identical to 08b, nothing regressed;
  the play clauses (A5 c2 · A9 c4/c5 · F117 station) are closed by FIELD EVIDENCE, A3 + A10 struck. ⛔ Nothing owed.
  ⚠️ The probe-MAINTENANCE list is instrument health, not a sitting: FAIL/ERROR by name: `C47OpenFarmSeedBufferShape` (Herbs 100→50), retired `LanderCargoRatchet`/`DroneUnreachableForever`/
  `AutoExportPriority`, `LayoutTechLock`/`AnomalyCaveInMap` (modules retired 09-12; Wave14 wrap rows :116-117, :130 too),
  `DomeFreeSpaceMismatch` (08 flagged, untriaged). ⭐ **NEWLY NAMED 09-14, and NOT regressions from 08b** (UI-only edits):
  `ClassicRockets`/`CohortHousing`/`NoHomeless` — all `nil value` on game methods (`UniversalRocket:1894`,
  `Colonist:3268`), the 1.1.0-drift shape. ⛔ Cannot be proven pre-existing: there was no prior RunAll to diff.
- **C89's B2 panel leg was NOT RUN, by owner ruling** — one unmeasured link (`CountDome` 0 leaves the panel clear, vanilla
  path). Its reopening trigger is a countering field report. C85's `(daily)` arm and C88's same-type compare (structurally
  impossible — every supplyable prefab is `require_prefab`) are unavailable, not owed. Gate evidence: each entry's
  §Attended check and SESSION_LOG 09-12.
- **C90** (Saint + Sinkhole apply-success guards) ships in v10 `fixed` but **UNEXERCISED** — `reports/C90_GUARDS_BUILD.md`.
  **C91** open candidate: vanilla leaks the Building Codes modifier on repeal. **C92** (P2, `cand`):
  `ResearchedAllTechs` counts hidden unreachable `UndergroundExploitation`; placement pass done (`reports/C92_PLACEMENT.md`).
  ⭐ **ck172 RULED 09-13: build the RESTORATION, ⛔ SHIPPING HELD until the owner lifts it in words** —
  brief `prompts/C92_ACHIEVEMENT_BUILD.md`; ck171 (scope) stays OPEN. Achievement testing = `EF-094`.
- **C93** (P2, `cand` 09-13): Outside Ranch produce stranded at the centre — a missing entity spot makes the
  stockpile controller fall back to `Origin`. NOT ours; ⛔ cause UNRESOLVED, needs the reporter's log line +
  mod list (pull-only, owner's call). **D14** + `prompts/STANDDOWN_AUDIT.md`: 21 of 45 modules replace a body
  and cannot ride a vendor fix; the gap is bodycheck's own class-c blind spot.
- ⭐ **TWO NEW FIXES `filed` 09-15, repairs DELIBERATELY UNAUTHORED until the owner says build (ck185).**
  **C95** habitat residents are drafted for expeditions and cannot be returned home — ⭐ REPRODUCED IN PLAY;
  repair = exclude them from the draft; ⚖️ classed an **oversight bug solved by a judgment call**, main pack
  **with the mark**, ⛔ not opt-in. **C96** a rover subclass never satisfies its base class — ⛔ the obvious
  one-token repair is VACUOUS, and its playtest needs an ESA colony. **C94** stays `cand`, control retired.
  Engine properties behind them: `EF-103` (habitat is a Community, never a `Dome`) · `EF-104` (expedition
  crew is drafted colony-wide and boards by teleport; ⛔ carries ONE unexplained draft observation).
- **C97** (P3, `cand` 09-15): the never-before-audited 1.1.0 tutorial rewrite (`TutorialsNew.lua`) — 4 stalls
  that can strand a tutorial run + 5 flag contracts the rewrite orphaned. ⛔ **NOT OURS** (both pack modules
  touching tutorial code proven neutral in source) and ⛔ **NO NORMAL-PLAY REACH** — `g_Tutorial` is a plain
  global, never a GameVar, and a tutorial never continues into a colony. ⛔ Source only, NOT reproduced.
  3 fact candidates await acceptance in the entry's last section; ⛔ do not re-audit the file to find them.
- ⛔ `SaintBlessing`'s kit probe PASSes **vacuously** with no domed Saint — not coverage; field reports are the detector
  (ck130). ✅ The heal itself fired in play 09-12.
- Post-launch LIVE: F105, F107, F108 (v4), F110 (v5), hotfix 2 (v6), C74+C77+C83 (v7), F119+C86 (v8), F59 repair +
  F60 out (v9), C85+C89+C88 in / F37+F43+F118+F31 out (v10); F104 NOT OURS. ⛔ F107 field route untested.
- GitHub tracker read route: `prompts/perma/PUBLIC_SURFACE_SWEEP.md` §4 (JSON API, including comments).
- ✅ SITE DEPLOYED 2026-09-13 07:06Z, `d86a347`, state `success` (deployments API + live page read): **49** live rows
  (45 success + 4 question) = the card's Forty-nine, first agreement since 09-11. Live FAQ carries "Four judgment calls"
  and no longer promises the retired farm-oxygen repair. ⚖️ The deploy is the owner's act; `publish-site.yml` is
  `workflow_dispatch` only. Live-deployment read route: `perma/SITE_AUDIT.md`.
  Owner's 2 pared files (`for-modders.md`, `install.md`) stay uncommitted = decision 47.
- ⭐ FR-1 TEMP WORKAROUND MOD LIVE 09-11 (Steam 3799500849 / PDX 158711). **ALL FR-1 / Linux / NVIDIA work →
  `prompts/perma/LINUX_DISPATCH.md`.** Field: 3 working (one 10xx), 1 failing (GTX 1070, log requested).
- ⭐ **`prompts/smrtk/` CLOSED 2026-09-14 — 99 (Fable) verdict SHIP WITH CHANGES**, `reports/SMRTK_AUDIT.md`. The
  SMR Tool Kit is the owner's to use (TestKit-only, never uploads). Taint half of (A) measured CLEAN in 02/08/08b
  (`cheats_count=0` after 490 dispatches; 19-leaf sample on the rebuilt tree); eligibility stays `UNAVAILABLE:sandbox`
  (`EF-096`), adjudicated by closed enumeration (5 reason handlers), not an observed PASS. Changes C-1…C-8 in the
  report; ✅ **the Code link (C-1/3/5/6) LANDED 09-15, kit `f5fa650`**, desk gates GREEN, ⛔ unwitnessed until the first
  sitting → ✅ **witnessed 09-15** (C-1, C-6, 08b item 9); C-3 REFUTED in play (white text stays, low priority by owner
  word); C-5 unwitnessed. ⚖️ **ck184 RULED + CLOSED 09-15**: the probe-sweep GATE is an age (24 h / a warranting change,
  satisfied at the next playtest); ⛔ **no agent or kit code refuses work or overrides the owner over it**; text chip
  stands. ⛔ **NOTHING from the toolkit chain is owed.** Stamper parked (`FUTURE_IDEAS` 5, not agent-tracked).
- ⏭ NEXT: `prompts/STANDDOWN_AUDIT.md` (no blocker) · probe maintenance at the desk (the FAIL/ERROR names above;
  Codex leg) · `prompts/C92_ACHIEVEMENT_BUILD.md` (build+test; ck172's shipping hold remains) · then the
  playtest sitting. ⛔ `SELFCHECK_PILOT` REMOVED 09-13 (`cf8d51f`).
  Owner OWES: ck151 (b) dev-report scope.
  08 is a separate clean-taint boot from ck144 (a). ✅ Fixture CHOSEN 09-14: `SMRTK08 Fixture Sol 490` (C92 reporter's colony,
  1.1.0.403908, `CheatsUsed` read scalar from disk against a TAINTED positive control; 4 byte copies exist). Handoff `prompts/perma/HANDOFF_ORCHESTRATOR.md` §3 LIVE.
  Desk `prompts/DLC_DEEP_CHECK.md` (`HUNT_AUDIT.md` §8). Chain `prompts/fixtoggles/` DEFERRED 09-12 (ck148, not started).
- Watches: `EF-066` subclass reach unmeasured, ck74 half-open · localisation: German only one SEEN (`EF-039`) ·
  C47 (unrun) · C48 opt-in · F02/F78/F81 organic · riders C42/F99/F80/F96-R2 · `EF-051` falsifier = stray save ·
  **F109 PARKED** (entry has it) · **F60** RETIRED 09-11 (ships in v9) · **C55** vanilla pre-sort read · FR-2/FR-3 OPEN.
  `DestroyedRebuild` hardening is closed; its reopening evidence is the hex's buildings list, mod list, and a save.

## Hazard pointers — moderate harm · universal reach · no machine gate
Module lists are gated by `tools/doccheck.py` MODULE SETS + `tools/upload_preflight.py` (membership + order).
- **H-03** Portal API mechanism and safe pack routes: `SteamWorkshop.lua:17-22`, `UPLOAD_WORKFLOW.md`, `perma/RELEASE.md`.
- **H-05** Sweep-fence authority: `prompts/prelaunch-sweep/00_CHAIN_SPEC.md`; public pointer: `prompts/README.md`.
- **H-08** Junction-enable behavior and recovery: `EF-055`.
- **H-09** Packed-folder/junction precedence: `EF-055`, `prompts/DLC_DEEP_CHECK.md`.

## Governing pointers (owner rulings; bodies in checklist/SESSION_LOG)
- **H-04** Future-release and publication scope: `perma/RELEASE.md` release rails.
- Shipping bar and major-overhaul costs: `FIX_POLICY.md` §3a and `WORKFLOW.md`.
- Vendor patch-note evidence: `FIX_POLICY.md` §4.
- Both-mods rig and attendance protocol: `WORKFLOW.md`.
- Player replies: `WORKFLOW.md` rule 5b.
- Skip reporting: `WORKFLOW.md` testing protocol.
- Display name and preserved internal identifiers: checklist ruling 08-17.
- Player-surface naming and load-order boundary: `EF-054`, `FIX_POLICY.md` §8.
- State format: `prompts/perma/STATE_EVICTION.md` § Formatting.
- Branch guards: `FIX_POLICY.md` §2a.
- 1.0.7 service: frozen GitHub build `v5-game-1.0.7`, linked from card and site.
- Upload page-body source and backup cycle: `perma/RELEASE.md`, `UPLOAD_WORKFLOW.md` §3.

## Open owner decisions (bodies in `docs/PLAYTEST_CHECKLIST.md` → "Decisions waiting on you")
- STILL OPEN: 53 harden now or in 1.0.1 · 47 two modder-page wordings · 152 c open · 185 C95/C96 builds · 133 two `FIX_POLICY` §2a
  lines (2 UNKNOWN-status policy, 4 `LuaRevision` label). `WAITING_ON_YOU.md` parses the literal `STILL OPEN:` and
  `Owner OWES: ck##` idioms.
- **53**: RULED 09-12 to pare the modder surface, so the hardening queue shrinks with it; rec 1.0.1.
- **47**: the owner's 2 pared site files ride on it.
- **133**: `prompts/SELFCHECK_PILOT.md` ✅ REMOVED 2026-09-13 (owner's word); (2) and (4) still open.
- **151 (b)** dev-report scope (ck165 permits indefinite deferral) · **151 (c)** open. F59 re-derived 09-11: the expedition
  claim CONFIRMED **+ a 2nd caller** (manual Set Residence on a full home OVERFILLS it, both branches); both branches
  are in the repair scope, and the frozen `v5-game-1.0.7` download ships the same body with no version gate.
- **152 (c)** open (A1 source-derived, A2 `tested-attended`, (e) swept with v10).
- **169 ➋** DISCHARGED 09-13 — `faq.md` committed as `d86a347`; the site deploy itself is still the owner's act.

## Build state — emitted by `python tools/doccheck.py --emit-counts`
```
BUILD STATE (emitted by tools/doccheck.py)
- modules: 46 registered (46 default-active, 0 optional-gated files)
- Code/*.lua files: 47
- TestKit probes: 97
- BUGS index rows: 119 F + 13 D + 97 C
```
Records citing **1.0.7.396349** (`EF-014`) predate the baseline move; INSTALLED is **1.1.0**.
