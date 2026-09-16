# Project State — pull; read it when a task, a prompt or the owner calls for status

## Must_Read_Header
<!-- RULES -->
This file contains current status and pointers. Binding duties live in `CLAUDE.md`, document-local headers, and task documents.
<!-- /RULES -->

## Now
- ⭐ **v10 IS LIVE on both portals** (2026-09-13, owner's word): `pdx_id` **156049**, `steam_id` **3787202810**,
  tree `version` **11**, `pdx_version` "9", count word **Forty-nine**. C85 + C89 + C88 in, F37/F43+F118/F31 out.
- Shipping artifact: Steam-delivered `ModContent.fpk` **371,327 B** md5 `bef42a2d5405e06444b7e6efdf28cf38`
  (workshop folder, 09-13 00:25 local). Pack-size predictor: `tools/pack_predict.py`.
  ✅ The "56 vs 54" gap was a READER DEFECT, not a packaging one: `flpk_extract` re-read nested tables under the
  parent prefix and double-counted two entries (`reports/DOC_OVERHAUL_AUDIT.md` §1). v10 shipped **54**, matching
  the prediction exactly. Fixed + gated by doccheck's FLPK SELFTEST; `*/.agents/*` now pack-ignored, model **52**.
  PDX size unread; the two portals' sizes differed on v5/v6 (`RELEASE_PORTAL_PREP` §0.5(f)).
- Current version 1.1.0.403908 + DLC
- Previous version 1.0.7 w/ tree archived at `C:\Dev\SMR-SrcArchive\1.0.7.396349\Src` (`EF-083`)
- Post-launch LIVE: F105, F107, F108 (v4), F110 (v5), hotfix 2 (v6), C74+C77+C83 (v7), F119+C86 (v8), F59 repair +
  F60 out (v9), C85+C89+C88 in / F37+F43+F118+F31 out (v10); F104 NOT OURS. ⛔ F107 field route untested.
- ✅ SITE DEPLOYED 2026-09-13 07:06Z, `d86a347`, state `success` (deployments API + live page read): **49** live rows
  (45 success + 4 question) = the card's Forty-nine, first agreement since 09-11. Live FAQ carries "Four judgment calls"
  and no longer promises the retired farm-oxygen repair. ⚖️ The deploy is the owner's act; `publish-site.yml` is
  `workflow_dispatch` only. Live-deployment read route: `agent/support/LIVE_SITE_READ.md`.
  Owner's 2 pared files (`for-modders.md`, `install.md`) stay uncommitted = decision 47.
- ⭐ FR-1 TEMP WORKAROUND MOD LIVE 09-11 (Steam 3799500849 / PDX 158711). **ALL FR-1 / Linux / NVIDIA work →
  `prompts/perma/LINUX_DISPATCH.md`.** Field: GTX 1070 confirmed working; the reported failure was user error (owner, 09-15).
- ⭐ **`docs/archive/prompts/smrtk/` CLOSED 2026-09-14 — 99 (Fable) verdict SHIP WITH CHANGES**, `reports/SMRTK_AUDIT.md`. The
  SMR Tool Kit is the owner's to use (TestKit-only, never uploads). Taint half of (A) measured CLEAN in 02/08/08b
  (`cheats_count=0` after 490 dispatches; 19-leaf sample on the rebuilt tree); eligibility stays `UNAVAILABLE:sandbox`
  (`EF-096`), adjudicated by closed enumeration (5 reason handlers), not an observed PASS. Changes C-1…C-8 in the
  report; ✅ **the Code link (C-1/3/5/6) LANDED 09-15, kit `f5fa650`**, desk gates GREEN, ⛔ unwitnessed until the first
  sitting → ✅ **witnessed 09-15** (C-1, C-6, 08b item 9); C-3 REFUTED in play (white text stays, low priority by owner
  word); C-5 unwitnessed. ⚖️ **ck184 RULED + CLOSED 09-15**: the probe-sweep GATE is an age (24 h / a warranting change,
  satisfied at the next playtest); ⛔ **no agent or kit code refuses work or overrides the owner over it**; text chip
  stands. ⛔ **NOTHING from the toolkit chain is owed.** Stamper parked (`FUTURE_IDEAS` 5, not agent-tracked).

## Open owner decisions (bodies in `docs/PLAYTEST_CHECKLIST.md` → "Decisions waiting on you")
  Owner OWES: ck151 (b) dev-report scope.
- STILL OPEN: 53 harden now or in 1.0.1 · 47 two modder-page wordings · 152 c open · 185 C95/C96 builds · 133 two `FIX_POLICY` §2a
  lines (2 UNKNOWN-status policy, 4 `LuaRevision` label). `WAITING_ON_YOU.md` parses the literal `STILL OPEN:` and
  `Owner OWES: ck##` idioms.

## Build state — emitted by `python tools/doccheck.py --emit-counts`
```
BUILD STATE (emitted by tools/doccheck.py)
- modules: 46 registered (46 default-active, 0 optional-gated files)
- Code/*.lua files: 47
- TestKit probes: 97
- BUGS index rows: 119 F + 13 D + 97 C
```
