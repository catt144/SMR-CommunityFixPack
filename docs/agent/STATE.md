# Project State — the one mandatory read

Kernel only: status + pointer, never derivation.
Eviction procedure: `agent/prompts/STATE_EVICTION.md` (byte-budgeted by doccheck; owner ruling, checklist 42).
History newest-first in `docs/archive/SESSION_LOG.md`; full pre-eviction STATE = `git show d30a10d:docs/agent/STATE.md`.
Defect truth `agent/bugs/INDEX.md` · facts `agent/facts/INDEX.md` · doc map `docs/README.md`.
Authoring `agent/WORKFLOW.md` · code `agent/FIX_POLICY.md` · chains `agent/reports/CHAIN_METHOD.md`.

## Now
- ⭐⭐ **Release = the fix pack ALONE at 1.0.0 (owner 08-17).**
- ⭐⭐ **④ upload sitting PAUSED mid-sitting on the owner's word — NOTHING IS PUBLISHED.** Upload is owner-attended.
- **Active: pre-launch sweep chain `agent/prompts/prelaunch-sweep/`.**
  - Links 1–4 consumed: L1 structure · L2 lifecycle · L3 save/exit · L4 player experience.
  - **Nothing blocks launch so far.** Artifacts `reports/L1..L4_*.md`.
  - Findings `SWEEP_FINDINGS.md` (⛔ forbidden to links) · coverage `SWEEP_LEDGER.md`.
  - Owner kicks each step; next = `97_VERIFICATION_LAUNCH.md` interlude (run A pulled forward, spec §6.5 launch
    obligation — no lens, record-only except launch-blocking), then link 5 (failure/containment, pending item-41 cap ruling).
- ⛔ **Unverified in any running game:** `00_Core.lua` fixes `2f077e8` (stale update-suspect ×2 · registry double-append)
  and link 2's reload fix (`data_edited` memo). No launch since 08-17.
- ⛔⛔ **Gate B has NEVER run** (packed install, junction pulled, TestKit+opt-in off) — THE release gate
  (owner: A = information, B = the gate).
  - Every suite number ever taken is unpacked, TestKit-on, single-load (L2).
  - Baseline `80/0/16/0` of 96 (`archive/c47suite4_*`), gates `75/75`+`8/8`; rig runs cheats.
- **Owner decisions open** (bodies in `docs/PLAYTEST_CHECKLIST.md` → "Decisions waiting on you"):
  34 (C49–C52 timing; QA owed first) · 37 Q1 (mirror core fixes to opt-in) · 37 Q2 (Steam version, after Paradox) ·
  39 (dialog re-fire) · 40 (`smr_shuttles` name) · 41 (dialog wording + sweep cap 5→8).
- Watches: C47 speed thread (descending ladder, unrun) · C48 CANDIDATE (opt-in territory; no seed-family fix code here,
  08-16) · F02/F78/F81 organic · riders C42/F99/F80/F96-R2 post-release · EF-051 falsifier = any stray save at next launch.

## Hazards — each names an action an agent could take unattended; never do it
- **H-01** Tag `fixpack-v1.0.0` sits at `7824cbc`, one commit behind HEAD, **ON PURPOSE** (fixes unverified).
  Never move, re-push, or "fix" it.
- **H-02** `metadata.lua` is **FROZEN** at 1.0.0 — no version bump, no Mod Editor save
  (every editor save runs `version = version + 1`, `Mod.lua:967`).
- **H-03** No script/console in a launched game may touch a portal API — the FIRST call **creates the listing**
  (`SteamWorkshop.lua:17-22`). Safe: `DbgPackMod`, `tools/upload_preflight.py`. Paradox before Steam.
- **H-04** Never strike ④/release holds or call the pack ready — ④ is not imminent without the owner's word.
- **H-05** Sweep fence: links never read `SWEEP_FINDINGS.md` or link reports; boring chain commit subjects;
  links 3+ RECORD ONLY except launch-blocking. STATE carries no link verdicts.
- **H-06** `EF-056`: loading a COPY of a campaign still runs that campaign's autosave rotation and
  **deletes the owner's autosaves** — pre-copy every autosave first.
- **H-07** The opt-in pack does **NOT** publish and gates nothing; ~46 parked references restore via
  `reports/PARKED_OPTIN_REFERENCES.md` at ITS launch (obligation in that repo).

## Rules in force (owner rulings; bodies in checklist/SESSION_LOG)
- Ship line FROZEN (08-12): `fixed` + suite + self-checks + verified save-safety IS the bar.
- A green suite does NOT authorise an upload — config B is the gate (08-17).
- Both-mods-loaded is the rig's normal config (08-12); AMENDED inside the sweep chain only:
  A/B readings are re-derived, never compared to three-mod baselines.
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
- BUGS index rows: 103 F + 12 D + 52 C
```
Re-emit after any change; game pinned **1.0.7.396349** (`EF-014`).
