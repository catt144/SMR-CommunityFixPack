# Project State — the one mandatory read

Kernel only: status + pointer, never derivation.
Eviction procedure: `agent/prompts/STATE_EVICTION.md` (byte-budgeted by doccheck; owner ruling, checklist 42).
History newest-first in `docs/archive/SESSION_LOG.md`; full pre-eviction STATE = `git show 2a7ba46:docs/agent/STATE.md`.
Defect truth `agent/bugs/INDEX.md` · facts `agent/facts/INDEX.md` · doc map `docs/README.md`.
Authoring `agent/WORKFLOW.md` · code `agent/FIX_POLICY.md` · chains `agent/reports/CHAIN_METHOD.md`.

## Now
- ⭐⭐ **Release = the fix pack ALONE at 1.0.0 (owner 08-17).**
- ⭐⭐ **④ upload sitting PAUSED mid-sitting on the owner's word — NOTHING IS PUBLISHED.** Upload is owner-attended.
- ⛔⛔ **Next = `agent/prompts/prelaunch-sweep/99b_VERDICT_REVIEW_fable.md`**, an independent session that tries
  to break the audit's verdict BEFORE it is acted on. **The upload waits on 99b, then the owner.**
- ⭐⭐ **Terminal audit consumed 08-19 — verdict UPLOAD**, taken on convergence clause 3 (the cap, named as a cap,
  not as cleanliness). Record `reports/99_TERMINAL_AUDIT.md`; owner-facing = checklist 53.
- ⭐⭐ **Release gate PASSED: run B scored 10 of 10** (08-19, attended; packed, TestKit off, opt-in off).
  ⭐ **Packed ≡ unpacked at module level** — the 75 applied names are set-identical to the unpacked leg.
- ⭐⭐ **Both `2f077e8` core fixes PROVEN in a running game** (act 1, attended): `update_suspect` nil, `#order` 75.
- **Pre-launch sweep chain `agent/prompts/prelaunch-sweep/` is CLOSED — links 1–8 consumed, lens pool EXHAUSTED**,
  plus 2 no-lens interludes (97 verification launch, 98 launch rehearsal). ⛔ **1 launch blocker, found and fixed.**
  - Findings `SWEEP_FINDINGS.md` (⛔ forbidden to links) · coverage `SWEEP_LEDGER.md` · reports `reports/L1..L8_*.md`,
    `97_VERIFICATION_LAUNCH.md`, `98_LAUNCH_REHEARSAL.md`. STATE carries no link verdicts (H-05).
- ⭐ **Shipping artifact:** `.fpk` 362,894 B, md5 `8dcb0692…`, at
  `%LOCALAPPDATA%\Temp\…\ModUpload\Pack\ModContent.fpk` — **80/80 byte-identical** to the tree tag `fixpack-v1.0.0`
  marks. Predictor `tools/pack_predict.py`, reader `tools/pack_list.py`, upload guard `tools/upload_preflight.py`.
- ⛔ **The console is NOT a route to pack or reload** — `DbgPackMod`/`ReloadLua` are both nil in `_G` at the retail
  console (measured). Only route = Mods Manager → Edit (`Ctrl-E`) → **File → Pack Mod**; ⚠️ it loads a scratch colony.
- ✅ **Rig restored 08-19:** all 3 junctions present, fix pack + TestKit re-ticked, opt-in pack still OFF
  (checklist 43). Rig runs cheats. Baseline suite `80/0/16/0` of 96 (`archive/c47suite4_*`), gates `75/75`+`8/8`.
- **Owner decisions open** (bodies in `docs/PLAYTEST_CHECKLIST.md` → "Decisions waiting on you"):
  53 (harden now or in 1.0.1; rec 1.0.1) · 51 (both-packs leg timing; rec after launch) · 50 (chain-vs-replace
  wording) · 47 (two modder-page wordings) · 43 (opt-in pack re-tick) · 41 (dialog wording + sweep cap 5→8) ·
  40 (`smr_shuttles` name) · 39 (dialog re-fire) · 37 Q1 (mirror core fixes to opt-in) · 37 Q2 (Steam, after
  Paradox) · 34 (C49–C52 timing; QA owed first).
- Watches: C47 speed thread (descending ladder, unrun) · C48 CANDIDATE (opt-in territory; no seed-family fix code
  here, 08-16) · F02/F78/F81 organic · riders C42/F99/F80/F96-R2 post-release · EF-051 falsifier = any stray save.

## Hazards — each names an action an agent could take unattended; never do it
- **H-01** Tag `fixpack-v1.0.0` was MOVED onto its close-out commit by the terminal audit (08-19, brief §9
  authority) and now marks what actually gets packed. Never move it again without an equivalent gate.
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
- modules: 75 registered (75 default-active, 0 optional-gated files)
- Code/*.lua files: 76
- TestKit probes: 96
- BUGS index rows: 103 F + 12 D + 53 C
```
Re-emit after any change; game pinned **1.0.7.396349** (`EF-014`).
