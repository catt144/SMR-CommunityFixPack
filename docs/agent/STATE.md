# Project State — the one mandatory read

Kernel only: status + pointer, never derivation.
Eviction procedure: `agent/prompts/STATE_EVICTION.md` (byte-budgeted by doccheck; owner ruling, checklist 42).
History newest-first in `docs/archive/SESSION_LOG.md`; full pre-eviction STATE = `git show 2a7ba46:docs/agent/STATE.md`.
Defect truth `agent/bugs/INDEX.md` · facts `agent/facts/INDEX.md` · doc map `docs/README.md`.
Authoring `agent/WORKFLOW.md` · code `agent/FIX_POLICY.md` · chains `agent/reports/CHAIN_METHOD.md`.

## Now
- ⭐⭐ **Release = the fix pack ALONE at 1.0.0 (owner 08-17).**
- ⭐⭐ **④ upload sitting PAUSED mid-sitting on the owner's word — NOTHING IS PUBLISHED.** Upload is owner-attended.
- ⭐⭐ **⑤ TERMINAL AUDIT (link 5) CONSUMED 08-20 — VERDICT: SHIP; TAG MOVED (H-01).** Close-out chain fully
  consumed; `C50`+`C51` IN 1.0.0 (checklist 58), `C52` `parked`/FROZEN. All five challenges held; 0 blockers;
  audit re-derivation = `EF-066` (composed `Init` — wave-12 probe's "later mod" line misattributes; TestKit-only).
  **The upload waits on the owner alone** — ruling receipt checklist 66; sitting steps `RELEASE_PORTAL_PREP` §0.5.
- ⭐⭐ **④ SITTING RAN 08-20 ATTENDED: BOTH FIXES WORK AND WERE SEEN, IN ENGLISH AND GERMAN.** Both now
  `tested-attended`; 77 applied; suite **74/0/24/0 of 98** (checklist 60 discharged). Report
  `reports/04_ATTENDED_SITTING.md`; logs `archive/link4{en,de,lang}_*`. ⛔ SKIPPED BY NAME: `C50`'s
  challenge landing-spot site, and the in-game Mission Profile on a SpaceY colony.
- ⚖️ **Two code changes DURING that sitting.** `C50` now stands down while a game runs (owner, checklist 61 —
  the in-game Goals panel double-counted the sponsor bonus: 60 for a cap of 40). `C51`'s rocket half was a
  ⛔ NO-OP as built — the button is not a direct child — and now uses `XWindow:ResolveId`.
- ⭐⭐ **`EF-039`'s standing unobserved note CLOSED, positively** — repointed AND borrowed shipped ids both
  rendered German on screen. ⚠️ German only; the other 7 packs remain CSV-measured, not seen.
- ⇒ **This repo is CLOSED once the owner uploads** — no queued 1.0.1; next effort is the **opt-in pack**
  (owner 08-20; its kickoff reads = that repo's own STATE + `reports/PARKED_OPTIN_REFERENCES.md`).
- ⭐⭐ **99b VERDICT REVIEW consumed 08-19 — ruling UPHELD.** Run-B criteria, the act-1 core-fix reads and two
  audit verifications re-derived from primary evidence; only wording broke (VR-1…VR-6, chain `SWEEP_FINDINGS.md`).
  **The upload now waits on the owner alone** (checklist 54; delivered-bytes check added, PORTAL_PREP §0.5(f)).
- ⭐⭐ **Terminal audit consumed 08-19 — verdict UPLOAD**, taken on convergence clause 3 (the cap, named as a cap,
  not as cleanliness). Record `reports/99_TERMINAL_AUDIT.md`; owner-facing = checklist 53.
- ⭐⭐ **Release gate PASSED: run B scored 10 of 10** (08-19, attended; packed, TestKit off, opt-in off).
  ⭐ **Packed ≡ unpacked at module level** — the 75 applied names are set-identical to the unpacked leg.
- ⭐⭐ **Both `2f077e8` core fixes PROVEN in a running game** (act 1, attended): `update_suspect` nil, `#order` 75.
  Evidence logs archived 08-19 by 99b (`archive/act1_*`) — they had lived only in the rotating live-logs dir.
- **Pre-launch sweep chain `agent/prompts/prelaunch-sweep/` is CLOSED — links 1–8 consumed, lens pool EXHAUSTED**,
  plus 2 no-lens interludes (97 verification launch, 98 launch rehearsal). ⛔ **1 launch blocker, found and fixed.**
  - Findings `SWEEP_FINDINGS.md` (⛔ forbidden to links) · coverage `SWEEP_LEDGER.md` · reports `reports/L1..L8_*.md`,
    `97_VERIFICATION_LAUNCH.md`, `98_LAUNCH_REHEARSAL.md`. STATE carries no link verdicts (H-05).
- ⛔ **Shipping artifact: NO PACKED `.fpk` MATCHES THIS TREE** (link 3, 08-20). The 08-17 archive — 362,894 B,
  md5 `8dcb0692…`, 80/80 against the tag — is SUPERSEDED by `C50`+`C51`. Expected shape **82 files = 78
  `Code/*.lua` + `items.lua` + `metadata.lua` + `LICENSE` + `preview.png`** (`tools/pack_predict.py`, emitted).
  ⛔ **The new md5/bytes exist only after the owner packs at the sitting — never quote one**; `PORTAL_PREP`
  §0.5(f) now records it there. Reader `tools/pack_list.py`, upload guard `tools/upload_preflight.py`.
- ⛔ **The console is NOT a route to pack or reload** — `DbgPackMod`/`ReloadLua` are both nil in `_G` at the retail
  console (measured). Only route = Mods Manager → Edit (`Ctrl-E`) → **File → Pack Mod**; ⚠️ it loads a scratch colony.
- ✅ **Rig restored 08-19:** all 3 junctions present, fix pack + TestKit re-ticked, opt-in pack still OFF
  (checklist 43). Rig runs cheats. Baseline suite `80/0/16/0` of 96 (`archive/c47suite4_*`), gates `75/75`+`8/8`.
- **Owner decisions open** (bodies in `docs/PLAYTEST_CHECKLIST.md` → "Decisions waiting on you"):
  53 (harden now or in 1.0.1; rec 1.0.1) · 51 (both-packs leg timing; rec after launch) · 50 (chain-vs-replace
  wording) · 47 (two modder-page wordings) · 43 (opt-in pack re-tick) · 41 (dialog wording + sweep cap 5→8) ·
  40 (`smr_shuttles` name) · 39 (dialog re-fire) · 37 Q2 (Steam, after Paradox). 34 DISCHARGED by 56+58.
- ✅ **Sibling rulings CARRIED OUT 08-20 (checklist 55)** — no fix-pack file touched, shipping surface re-diffed
  empty: the two `2f077e8` core fixes are MIRRORED into `SMR-OptInPack` (`2cedf7d`, parse+doccheck green, sites
  code-identical after namespace normalisation; ⛔ unverified in a running game there), and the rescue mod's
  missing `items.lua` is a LAUNCH GATE in `SMR-CommunitySaveRescue/CLAUDE.md` (`9c912b3`) with its consequence
  carried as ⛔ NOT DERIVED. Src path (`EF-014`) is `…\Project Spark\ModTools\Src\CommonLua\Classes\Mod.lua`.
- Watches: C47 speed thread (descending ladder, unrun) · C48 CANDIDATE (opt-in territory; no seed-family fix code
  here, 08-16) · F02/F78/F81 organic · riders C42/F99/F80/F96-R2 post-release · EF-051 falsifier = any stray save.

## Hazards — each names an action an agent could take unattended; never do it
- **H-01** Tag `fixpack-v1.0.0` was MOVED AGAIN 08-20 onto the close-out audit's commit (link 5 §3 authority;
  first move 08-19) and now marks what actually gets packed. ⛔ Its gate is the ATTENDED SITTING + the one-time
  release-gate ruling (checklist 57), NOT run B alone. Never move it again without an equivalent gate.
- **H-02** `metadata.lua` is **FROZEN** at 1.0.0 — no version bump, no Mod Editor save
  (every editor save runs `version = version + 1`, `Mod.lua:967`).
- **H-03** No script/console in a launched game may touch a portal API — the FIRST call **creates the listing**
  (`SteamWorkshop.lua:17-22`). Safe: `DbgPackMod`, `tools/upload_preflight.py`. Paradox before Steam.
- **H-04** Never strike ④/release holds or call the pack ready — ④ is not imminent without the owner's word.
- **H-05** Sweep fence: links never read `SWEEP_FINDINGS.md` or link reports; boring chain commit subjects;
  links 3+ RECORD ONLY except launch-blocking. STATE carries no link verdicts.
- **H-06** `EF-056`: loading a COPY of a campaign still runs that campaign's autosave rotation and
  **deletes the owner's autosaves** — pre-copy every autosave first.
- **H-07** Never restore the ~46 parked opt-in references here before the opt-in pack launches; that is ITS
  launch obligation, recorded in that repo. Verbatim parking: `reports/PARKED_OPTIN_REFERENCES.md`.
- **H-08** ⛔ **Pulling a mod's junction COSTS its enable and restoring the folder does NOT buy it back**
  (`EF-055`). Recovery = owner tick + restart, never an agent's. Never pull one to reach a configuration without
  booking that cost. ⚠️ NARROWED 08-19: the cost lands when the **id vanishes**; a folder-for-folder swap under
  the **same id KEEPS** the enable. **The opt-in pack is in that state now** (checklist 43).
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
- modules: 77 registered (77 default-active, 0 optional-gated files)
- Code/*.lua files: 78
- TestKit probes: 98
- BUGS index rows: 103 F + 12 D + 53 C
```
Re-emit after any change; game pinned **1.0.7.396349** (`EF-014`).
